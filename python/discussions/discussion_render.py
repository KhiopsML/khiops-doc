"""Render discussion content and collect safe GitHub attachments."""

import hashlib
import html
import logging
import re
import unicodedata
import urllib.parse
import urllib.request
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import PurePosixPath

import bleach
from markdown_it import MarkdownIt
from markdown_it.token import Token
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from python.discussions.discussion_content import InvalidDiscussion


MAX_ATTACHMENT_BYTES = 100_000
logger = logging.getLogger(__name__)
SCRIPT_EXTENSIONS = {".py", ".sh", ".r"}
IMAGE_EXTENSIONS = {"image/png": ".png", "image/jpeg": ".jpg", "image/gif": ".gif", "image/webp": ".webp"}
TAGS = {
    "a", "abbr", "b", "blockquote", "br", "code", "del", "details", "div",
    "em", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "i", "img", "li",
    "ol", "p", "pre", "s", "span", "strong", "sub", "summary", "sup",
    "table", "tbody", "td", "th", "thead", "tr", "ul",
}
ATTRIBUTES = {
    "a": ["href", "title"], "img": ["src", "alt", "title", "width", "height"],
    "code": ["class"], "span": ["class"], "th": ["align"], "td": ["align"],
}
ALERT_CLASSES = {
    "NOTE": "admonition note",
    "TIP": "admonition tip",
    "IMPORTANT": "admonition important example",
    "WARNING": "admonition warning",
    "CAUTION": "admonition caution danger",
}
INLINE_MATH = re.compile(r"\$(?![\s$])((?:\\.|[^\\$\n])+?)(?<!\s)\$(?!\d)")
BACKTICK_MATH = re.compile(r"\$`([^`\n]+)`\$")
DISPLAY_MATH = re.compile(r"\$\$((?:\\.|[^\\])+?)\$\$")


def allowed_attribute(tag, name, value):
    """Allow only supported attributes and generated CSS classes."""
    if name == "class" and tag == "div":
        return value in {"highlight", "arithmatex"} or value in ALERT_CLASSES.values()
    if name == "class" and tag == "p":
        return value == "admonition-title"
    return name in ATTRIBUTES.get(tag, ())


def math_match(text, start, end):
    """Match a supported math expression at the specified position."""
    return (
        DISPLAY_MATH.match(text, start, end)
        or BACKTICK_MATH.match(text, start, end)
        or INLINE_MATH.match(text, start, end)
    )


def math_html(match, unescape=False):
    """Wrap a matched expression in MathJax delimiters and escape its content."""
    display = match.group(0).startswith("$$")
    opening, closing = (r"\[", r"\]") if display else (r"\(", r"\)")
    expression = html.unescape(match.group(1)) if unescape else match.group(1)
    return '<span class="arithmatex">' + opening + html.escape(expression, quote=False) + closing + "</span>"


def math_inline(state, silent):
    """Convert GitHub math delimiters before Markdown parses their contents."""
    if state.src[state.pos] != "$":
        return False
    match = math_match(state.src, state.pos, state.posMax)
    if not match:
        return False
    if not silent:
        token = state.push("discussion_math", "", 0)
        token.markup = match.group(0)
        token.content = math_html(match)
    state.pos = match.end()
    return True


class InlineCodeTracker(HTMLParser):
    """Track whether inline HTML tokens are inside code or preformatted text."""

    def __init__(self):
        """Start with no open code elements."""
        super().__init__()
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        """Enter a code or preformatted element."""
        if tag in {"code", "pre"}:
            self.depth += 1

    def handle_endtag(self, tag):
        """Leave a code or preformatted element."""
        if tag in {"code", "pre"} and self.depth:
            self.depth -= 1


class HtmlMathRewriter(HTMLParser):
    """Convert math in raw HTML text while preserving markup and code."""

    def __init__(self):
        """Initialize the output, text buffer, and protected-element depth."""
        super().__init__(convert_charrefs=False)
        self.output = []
        self.text = []
        self.code_depth = 0

    def flush_text(self):
        """Convert buffered math outside protected elements and append it."""
        text = "".join(self.text)
        self.text.clear()
        if self.code_depth:
            self.output.append(text)
            return
        start = 0
        position = 0
        while position < len(text):
            position = text.find("$", position)
            if position < 0:
                break
            previous = position - 1
            while previous >= 0 and text[previous] == "\\":
                previous -= 1
            backslashes = position - previous - 1
            match = None if backslashes % 2 else math_match(text, position, len(text))
            if match:
                self.output.extend((text[start:position], math_html(match, unescape=True)))
                position = start = match.end()
            else:
                position += 1
        self.output.append(text[start:])

    def handle_starttag(self, tag, attrs):
        """Preserve the start tag and track protected elements."""
        self.flush_text()
        self.output.append(self.get_starttag_text())
        if tag in {"code", "pre", "script", "style"}:
            self.code_depth += 1

    def handle_startendtag(self, tag, attrs):
        """Preserve a self-closing tag after flushing text."""
        self.flush_text()
        self.output.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        """Preserve the closing tag and leave any protected element."""
        self.flush_text()
        self.output.append(f"</{tag}>")
        if tag in {"code", "pre", "script", "style"} and self.code_depth:
            self.code_depth -= 1

    def handle_data(self, data):
        """Buffer text for math conversion."""
        self.text.append(data)

    def handle_entityref(self, name):
        """Buffer a named entity alongside surrounding text."""
        self.text.append(f"&{name};")

    def handle_charref(self, name):
        """Buffer a numeric entity alongside surrounding text."""
        self.text.append(f"&#{name};")

    def handle_comment(self, data):
        """Preserve an HTML comment without parsing its contents."""
        self.flush_text()
        self.output.append(f"<!--{data}-->")

    def handle_decl(self, decl):
        """Preserve an HTML declaration."""
        self.flush_text()
        self.output.append(f"<!{decl}>")

    def handle_pi(self, data):
        """Preserve a processing instruction."""
        self.flush_text()
        self.output.append(f"<?{data}>")

    def unknown_decl(self, data):
        """Preserve an unrecognized declaration."""
        self.flush_text()
        self.output.append(f"<![{data}]>")


def finalize_math(state):
    """Finalize math tokens and convert raw HTML blocks, excluding code."""
    for token in state.tokens:
        if token.type == "html_block":
            rewriter = HtmlMathRewriter()
            rewriter.feed(token.content)
            rewriter.close()
            rewriter.flush_text()
            token.content = "".join(rewriter.output)
            continue
        if token.type != "inline" or not token.children:
            continue
        code = InlineCodeTracker()
        for child in token.children:
            if child.type == "html_inline":
                code.feed(child.content)
            elif child.type == "discussion_math":
                if code.depth:
                    child.type = "text"
                    child.content = child.markup
                else:
                    child.type = "html_inline"


def github_alerts(state):
    """Replace supported GitHub alert blockquotes with site admonitions."""
    tokens = state.tokens
    pairs = []
    stack = []
    titles = []
    for index, token in enumerate(tokens):
        if token.type == "blockquote_open":
            stack.append(index)
        elif token.type == "blockquote_close":
            pairs.append((stack.pop(), index))
    for start, end in pairs:
        if start + 3 >= end or tokens[start + 1].type != "paragraph_open":
            continue
        inline = tokens[start + 2]
        if inline.type != "inline" or not inline.children:
            continue
        children = inline.children
        match = re.fullmatch(r"\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]", children[0].content)
        if children[0].type != "text" or not match:
            continue
        if len(children) > 1 and children[1].type not in ("softbreak", "hardbreak"):
            continue
        kind = match.group(1)
        tokens[start].tag = "div"
        tokens[start].attrSet("class", ALERT_CLASSES[kind])
        tokens[end].tag = "div"
        del children[:2 if len(children) > 1 else 1]
        if not children:
            for token in tokens[start + 1:start + 4]:
                token.hidden = True
        title = Token("html_block", "", 0)
        title.content = f'<p class="admonition-title">{kind.title()}</p>\n'
        titles.append((start + 1, title))
    for index, title in sorted(titles, reverse=True):
        tokens.insert(index, title)


class AttachmentError(InvalidDiscussion):
    """Report an attachment that prevents publication of a discussion."""
    def __init__(self, url, reason):
        """Associate a rejected attachment URL with its error message."""
        self.url = url
        super().__init__(f"{reason}: {url}")


def github_attachment(url):
    """Return whether a URL points to a supported GitHub attachment path."""
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != "github.com" or parsed.username or parsed.password:
        return False
    return parsed.path.startswith(("/user-attachments/assets/", "/user-attachments/files/"))


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    """Restrict attachment redirects to approved HTTPS hosts."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        """Follow attachment redirects only to approved HTTPS hosts."""
        parsed = urllib.parse.urlsplit(newurl)
        allowed = (
            parsed.hostname == "github.com"
            or parsed.hostname == "github-production-user-asset-6210df.s3.amazonaws.com"
            or parsed.hostname == "objects.githubusercontent.com"
        )
        if parsed.scheme != "https" or not allowed or parsed.username or parsed.password:
            raise ValueError(f"Untrusted attachment redirect: {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download_attachment(url):
    """Download a trusted GitHub attachment and return its bytes and MIME type.

    Reject untrusted URLs and attachments exceeding MAX_ATTACHMENT_BYTES.
    """
    if not github_attachment(url):
        raise ValueError(f"Untrusted attachment URL: {url}")
    request = urllib.request.Request(url, headers={"User-Agent": "khiops-doc-discussion-import"})
    with urllib.request.build_opener(SafeRedirect()).open(request, timeout=30) as response:
        content = response.read(MAX_ATTACHMENT_BYTES + 1)
        if len(content) > MAX_ATTACHMENT_BYTES:
            raise AttachmentError(url, "attachment exceeds 100,000 bytes")
        return content, response.headers.get_content_type()


def topic_slug(topic):
    """Create a readable topic slug with a hash of the original label."""
    name = re.sub(r"[^a-z0-9]+", "-", topic.removeprefix("Topic/").lower()).strip("-") or "topic"
    return f"{name}-{hashlib.sha256(topic.encode()).hexdigest()[:8]}"


def attachment_section_slug(text):
    """Make a bounded, readable filename component from a heading."""
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")[:60].rstrip("-") or "discussion"


def heading_text(value):
    """Normalize and escape a title for Markdown, HTML and site templates."""
    value = " ".join(value.split())
    value = html.escape(value, quote=False)
    value = value.replace("{{", "&#123;&#123;").replace("{%", "&#123;%")
    return re.sub(r"([\\`*_{}\[\]()#+.!|>-])", r"\\\1", value)


class HeadingLevels(HTMLParser):
    """Find the shallowest heading level in sanitized discussion HTML."""

    def __init__(self):
        """Initialize the minimum level to the deepest supported heading."""
        super().__init__()
        self.minimum = 6

    def handle_starttag(self, tag, attrs):
        """Update the minimum when a heading start tag is encountered."""
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.minimum = min(self.minimum, int(tag[1]))


class AttachmentRewriter(HTMLParser):
    """Rewrite attachment URLs and heading levels in sanitized discussion HTML."""
    def __init__(self, item, downloader, heading_shift):
        """Initialize output and collected assets for one discussion."""
        super().__init__(convert_charrefs=False)
        self.item = item
        self.downloader = downloader
        self.heading_shift = heading_shift
        self.output = []
        self.assets = {}
        self.attachment_section = attachment_section_slug(item.title)
        self.heading = None
        self.heading_parts = []
        self.attachment_counts = defaultdict(int)
        self.attachment_paths = {}

    def heading_tag(self, tag):
        """Shift heading levels without exceeding HTML's h6 limit."""
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            return f"h{min(6, int(tag[1]) + self.heading_shift)}"
        return tag

    def handle_starttag(self, tag, attrs):
        """Copy supported attachments and rewrite their URLs in a start tag.

        Relative links are resolved against the source discussion. Downloaded
        assets are stored by site-relative path for the caller to publish.
        """
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.heading = tag
            self.heading_parts = []
        attrs = dict(attrs)
        key = "src" if tag == "img" else "href" if tag == "a" else None
        if key and key in attrs:
            url = attrs[key]
            parsed = urllib.parse.urlsplit(url)
            script = tag == "a" and PurePosixPath(parsed.path).suffix.lower() in SCRIPT_EXTENSIONS
            if github_attachment(url) and (tag == "img" or script):
                extension = PurePosixPath(parsed.path).suffix.lower() if script else None
                readable = tag == "img" or extension == ".py"
                category = "images" if tag == "img" else "discussion-scripts"
                attachment_key = (category, self.attachment_section, url)
                if readable and attachment_key in self.attachment_paths:
                    path = self.attachment_paths[attachment_key]
                else:
                    content, content_type = self.downloader(url)
                    if len(content) > MAX_ATTACHMENT_BYTES:
                        raise AttachmentError(url, "attachment exceeds 100,000 bytes")
                    if tag == "img":
                        extension = IMAGE_EXTENSIONS.get(content_type)
                        if extension is None:
                            raise AttachmentError(url, f"unsupported image type {content_type}")
                    if readable:
                        count_key = (category, self.attachment_section)
                        self.attachment_counts[count_key] += 1
                        filename = (
                            f"{self.item.number}-{self.attachment_section}-"
                            f"{self.attachment_counts[count_key]}{extension}"
                        )
                        self.attachment_paths[attachment_key] = (
                            f"assets/{category}/q-and-a/{topic_slug(self.item.topic)}/{filename}"
                        )
                        path = self.attachment_paths[attachment_key]
                    else:
                        digest = hashlib.sha256(url.encode()).hexdigest()[:16]
                        path = f"assets/discussion-scripts/q-and-a/{topic_slug(self.item.topic)}/{digest}{extension}"
                    self.assets[path] = content
                attrs[key] = "/" + path
            elif not parsed.scheme and not url.startswith(("#", "/")):
                attrs[key] = urllib.parse.urljoin(self.item.url + "/", url)
        attributes = "".join(
            f' {name}="{html.escape(value, quote=True)}"' for name, value in attrs.items() if value is not None
        )
        self.output.append(f"<{self.heading_tag(tag)}{attributes}>")

    def handle_startendtag(self, tag, attrs):
        """Process self-closing tags like start tags."""
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        """Append a closing tag to the rendered output."""
        if tag == self.heading:
            self.attachment_section = attachment_section_slug("".join(self.heading_parts))
            self.heading = None
        self.output.append(f"</{self.heading_tag(tag)}>")

    def handle_data(self, data):
        """Preserve text content in the rendered output."""
        if self.heading:
            self.heading_parts.append(data)
        self.output.append(data)

    def handle_entityref(self, name):
        """Preserve a named HTML entity in the rendered output."""
        if self.heading:
            self.heading_parts.append(html.unescape(f"&{name};"))
        self.output.append(f"&{name};")

    def handle_charref(self, name):
        """Preserve a numeric HTML entity in the rendered output."""
        if self.heading:
            self.heading_parts.append(html.unescape(f"&#{name};"))
        self.output.append(f"&#{name};")


class BareLinkRewriter(HTMLParser):
    """Linkify text without reparsing or changing existing HTML and code."""

    def __init__(self):
        """Initialize the output, text buffer, and excluded-element stack."""
        super().__init__(convert_charrefs=False)
        self.output = []
        self.text = []
        self.skipped = []

    def flush_text(self):
        """Linkify buffered text unless it belongs to an excluded element."""
        text = "".join(self.text)
        self.text.clear()
        self.output.append(text if self.skipped else bleach.linkify(text, callbacks=[]))

    def handle_starttag(self, tag, attrs):
        """Preserve the tag and track elements excluded from linkification."""
        self.flush_text()
        self.output.append(self.get_starttag_text())
        if (self.skipped and tag not in {"br", "hr", "img"}) or tag in {"a", "code", "pre"} or (
            tag in {"span", "div"} and "arithmatex" in dict(attrs).get("class", "").split()
        ):
            self.skipped.append(tag)

    def handle_startendtag(self, tag, attrs):
        """Preserve a self-closing tag after flushing text."""
        self.flush_text()
        self.output.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        """Preserve the closing tag and update the excluded-element stack."""
        self.flush_text()
        self.output.append(f"</{tag}>")
        if self.skipped and self.skipped[-1] == tag:
            self.skipped.pop()

    def handle_data(self, data):
        """Buffer text for linkification."""
        self.text.append(data)

    def handle_entityref(self, name):
        """Buffer a named entity alongside surrounding text."""
        self.text.append(f"&{name};")

    def handle_charref(self, name):
        """Buffer a numeric entity alongside surrounding text."""
        self.text.append(f"&#{name};")


def render_content(item, downloader=download_attachment):
    """Render and sanitize one discussion, returning HTML and copied assets."""
    def highlight_code(code, language, _attributes):
        """Highlight known languages and safely render unknown ones as text."""
        if not language:
            return html.escape(code, quote=False)
        try:
            lexer = get_lexer_by_name(language, stripnl=False, ensurenl=False)
        except ClassNotFound:
            logger.warning("Unknown code language %r in %s; rendering as plain text", language, item.url)
            return html.escape(code, quote=False)
        return highlight(code, lexer, HtmlFormatter(nowrap=True))

    def render_fence(renderer, tokens, index, options, env):
        """Render math fences for MathJax and other fences as highlighted code."""
        if tokens[index].info.strip() == "math":
            code = html.escape(tokens[index].content, quote=False)
            return '<div class="arithmatex">\\[\n' + code + '\\]</div>\n'
        return '<div class="highlight">\n' + renderer.fence(tokens, index, options, env) + "</div>\n"

    md = MarkdownIt("commonmark", {"html": True, "highlight": highlight_code}).enable(["table", "strikethrough"])
    md.inline.ruler.before("escape", "math", math_inline)
    md.add_render_rule("fence", render_fence)
    md.core.ruler.after("inline", "finalize_math", finalize_math)
    md.core.ruler.after("inline", "github_alerts", github_alerts)
    rendered = md.render(item.content)
    clean = bleach.clean(rendered, tags=TAGS, attributes=allowed_attribute, protocols={"http", "https", "mailto"}, strip=True)
    linkifier = BareLinkRewriter()
    linkifier.feed(clean)
    linkifier.close()
    linkifier.flush_text()
    clean = "".join(linkifier.output)
    headings = HeadingLevels()
    headings.feed(clean)
    headings.close()
    parser = AttachmentRewriter(item, downloader, max(0, 3 - headings.minimum))
    parser.feed(clean)
    parser.close()
    # Prevent the site's template engine from evaluating discussion text.
    output = "".join(parser.output).replace("{{", "&#123;&#123;").replace("{%", "&#123;%")
    return output, parser.assets


def render_pages(items, downloader=download_attachment):
    """Render topic pages and an overview from publishable discussions.

    Return pages, assets and attachment errors. Discussions with rejected
    attachments are omitted.
    """
    grouped = defaultdict(list)
    for item in items:
        grouped[item.topic].append(item)
    pages = {}
    assets = {}
    invalid = []
    overview = [
        "# Questions and answers",
        "",
        "These questions and answers are imported from "
        "[Khiops Discussions on GitHub](https://github.com/orgs/KhiopsML/discussions).",
        "",
    ]
    for topic in sorted(grouped):
        entries = []
        title = heading_text(grouped[topic][0].topic_title)
        for item in sorted(grouped[topic], key=lambda value: value.number):
            try:
                content, files = render_content(item, downloader)
            except AttachmentError as exc:
                invalid.append({"url": item.url, "number": item.number, "file": exc.url, "reason": str(exc)})
                continue
            assets.update(files)
            entries.append((item, content))
        if not entries:
            continue
        slug = topic_slug(topic)
        overview += [f"## {title}", ""]
        page = [f"# {title}", ""]
        for item, content in entries:
            anchor = f"discussion-{item.number}"
            safe_title = heading_text(item.title)
            overview.append(f"- [{safe_title}]({slug}.md#{anchor})")
            page.extend([
                f'<a id="{anchor}"></a>',
                f"## {safe_title}",
                "",
                content,
                "",
                f"*Source: [discussion #{item.number}]({item.url})*",
                "",
            ])
        overview.append("")
        pages[f"q-and-a/{slug}.md"] = "\n".join(page)
    pages["q-and-a/overview.md"] = "\n".join(overview)
    return pages, assets, invalid
