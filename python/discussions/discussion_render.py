"""Render discussion content and collect safe GitHub attachments."""

import hashlib
import html
import re
import unicodedata
import urllib.parse
import urllib.request
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import PurePosixPath

import bleach

from python.discussions.discussion_content import InvalidDiscussion

MAX_ATTACHMENT_BYTES = 100_000
SCRIPT_EXTENSIONS = {".py", ".sh", ".r"}
IMAGE_EXTENSIONS = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
}
TAGS = {
    "a",
    "abbr",
    "b",
    "blockquote",
    "br",
    "code",
    "del",
    "details",
    "div",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "i",
    "img",
    "li",
    "ol",
    "p",
    "pre",
    "s",
    "span",
    "strong",
    "sub",
    "summary",
    "sup",
    "table",
    "tbody",
    "td",
    "th",
    "thead",
    "tr",
    "ul",
}
ATTRIBUTES = {
    "a": ["href", "title"],
    "img": ["src", "alt", "title", "width", "height"],
    "code": ["class"],
    "span": ["class"],
    "th": ["align"],
    "td": ["align"],
}
ALERT_CLASSES = {
    "NOTE": "admonition note",
    "TIP": "admonition tip",
    "IMPORTANT": "admonition important example",
    "WARNING": "admonition warning",
    "CAUTION": "admonition caution danger",
}
SOURCE_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
SOURCE_HEADING = re.compile(r"^( {0,3})(#{1,6})(?:[ \t]+|$)(.*?)[ \t]*#*[ \t]*$")
MARKDOWN_LINK = re.compile(
    r"(?P<label>!?\[[^\]\n]*\])\(\s*(?P<destination><[^>\n]*>|(?:\\.|[^()\s]|\([^()\n]*\))+)"
    r"(?P<title>\s+(?:\"[^\"\n]*\"|'[^'\n]*'))?\s*\)"
)
HTML_TAG = re.compile(r"<!--.*?-->|</?[A-Za-z][A-Za-z0-9-]*(?=[\s/>])[^>]*>")
INLINE_CODE = re.compile(r"(`+)(.+?)\1")
BACKTICK_MATH = re.compile(r"\$`([^`\n]+)`\$")
BARE_URL = re.compile(r"(?<![\w/(\[\"'=<>])https?://[^\s<>]+")
UNSAFE_SCHEME = re.compile(r"^(?:javascript|data|vbscript):", re.IGNORECASE)
GITHUB_ALERT = re.compile(r"^ {0,3}>[ \t]*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\][ \t]*$")


def allowed_attribute(tag, name, value):
    """Allow only supported attributes and generated CSS classes."""
    if name == "class" and tag == "div":
        return value in {"highlight", "arithmatex"} or value in ALERT_CLASSES.values()
    if name == "class" and tag == "p":
        return value == "admonition-title"
    return name in ATTRIBUTES.get(tag, ())


class AttachmentError(InvalidDiscussion):
    """Report an attachment that prevents publication of a discussion."""

    def __init__(self, url, reason):
        """Associate a rejected attachment URL with its error message."""
        self.url = url
        super().__init__(f"{reason}: {url}")


def github_attachment(url):
    """Return whether a URL points to a supported GitHub attachment path."""
    parsed = urllib.parse.urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.hostname != "github.com"
        or parsed.username
        or parsed.password
    ):
        return False
    return parsed.path.startswith(
        ("/user-attachments/assets/", "/user-attachments/files/")
    )


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
        if (
            parsed.scheme != "https"
            or not allowed
            or parsed.username
            or parsed.password
        ):
            raise ValueError(f"Untrusted attachment redirect: {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download_attachment(url):
    """Download a trusted GitHub attachment and return its bytes and MIME type.

    Reject untrusted URLs and attachments exceeding MAX_ATTACHMENT_BYTES.
    """
    if not github_attachment(url):
        raise ValueError(f"Untrusted attachment URL: {url}")
    request = urllib.request.Request(
        url, headers={"User-Agent": "khiops-doc-discussion-import"}
    )
    with urllib.request.build_opener(SafeRedirect()).open(
        request, timeout=30
    ) as response:
        content = response.read(MAX_ATTACHMENT_BYTES + 1)
        if len(content) > MAX_ATTACHMENT_BYTES:
            raise AttachmentError(url, "attachment exceeds 100,000 bytes")
        return content, response.headers.get_content_type()


def topic_slug(topic):
    """Create a readable slug from the topic label."""
    name = (
        re.sub(r"[^a-z0-9]+", "-", topic.removeprefix("Topic/").lower()).strip("-")
        or "topic"
    )
    return name


def attachment_section_slug(text):
    """Make a bounded, readable filename component from a heading."""
    normalized = (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    return (
        re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")[:60].rstrip("-")
        or "discussion"
    )


def heading_text(value):
    """Normalize and escape a title for Markdown, HTML and site templates."""
    value = " ".join(value.split())
    value = html.escape(value, quote=False)
    value = value.replace("{{", "&#123;&#123;").replace("{%", "&#123;%")
    return re.sub(r"([\\`*_{}\[\]#+.!|>-])", r"\\\1", value)


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

    def rewrite_url(self, tag, url):
        """Localize supported attachments and resolve source-relative links."""
        parsed = urllib.parse.urlsplit(url)
        script = (
            tag == "a"
            and PurePosixPath(parsed.path).suffix.lower() in SCRIPT_EXTENSIONS
        )
        if github_attachment(url) and (tag == "img" or script):
            extension = (
                PurePosixPath(parsed.path).suffix.lower() if script else None
            )
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
                        raise AttachmentError(
                            url, f"unsupported image type {content_type}"
                        )
                if readable:
                    count_key = (category, self.attachment_section)
                    self.attachment_counts[count_key] += 1
                    filename = (
                        f"{self.item.number}-{self.attachment_section}-"
                        f"{self.attachment_counts[count_key]}{extension}"
                    )
                    path = (
                        f"assets/{category}/q-and-a/"
                        f"{topic_slug(self.item.topic)}/{filename}"
                    )
                    self.attachment_paths[attachment_key] = path
                else:
                    digest = hashlib.sha256(url.encode()).hexdigest()[:16]
                    path = (
                        f"assets/discussion-scripts/q-and-a/"
                        f"{topic_slug(self.item.topic)}/{digest}{extension}"
                    )
                self.assets[path] = content
            return "/" + path
        if not parsed.scheme and not url.startswith(("#", "/")):
            return urllib.parse.urljoin(self.item.url + "/", url)
        return url

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
            attrs[key] = self.rewrite_url(tag, attrs[key])
        attributes = "".join(
            f' {name}="{html.escape(value, quote=True)}"'
            for name, value in attrs.items()
            if value is not None
        )
        self.output.append(f"<{self.heading_tag(tag)}{attributes}>")

    def handle_startendtag(self, tag, attrs):
        """Process self-closing tags like start tags."""
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        """Append a closing tag to the rendered output."""
        if tag == self.heading:
            self.attachment_section = attachment_section_slug(
                "".join(self.heading_parts)
            )
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


def markdown_alerts(lines):
    """Convert GitHub alert blockquotes to the site's Markdown admonitions."""
    output = []
    index = 0
    in_fence = None
    while index < len(lines):
        line = lines[index]
        fence = SOURCE_FENCE.match(line)
        if in_fence:
            output.append(line)
            if fence and fence.group(1)[0] == in_fence[0] and len(fence.group(1)) >= len(in_fence):
                in_fence = None
            index += 1
            continue
        if fence:
            in_fence = fence.group(1)
            output.append(line)
            index += 1
            continue
        alert = GITHUB_ALERT.match(line.rstrip("\r\n"))
        if not alert:
            output.append(line)
            index += 1
            continue
        body = []
        index += 1
        while index < len(lines) and re.match(r"^ {0,3}>", lines[index]):
            body.append(re.sub(r"^ {0,3}> ?", "", lines[index]))
            index += 1
        kind = alert.group(1).lower()
        output.append(f'!!! {kind} "{kind.title()}"\n')
        output.extend("    " + content if content.strip() else "\n" for content in body)
    return output


def sanitize_html_tag(tag, rewriter):
    """Sanitize one raw HTML tag before applying attachment rewrites."""
    match = re.match(r"<\s*(/?)\s*([A-Za-z][A-Za-z0-9]*)\b", tag)
    if match and not tag.startswith("<!--"):
        closing, name = match.groups()
        if closing:
            clean = bleach.clean(
                f"<{name}>__DISCUSSION_TAG__{tag}",
                tags=TAGS,
                attributes=allowed_attribute,
                protocols={"http", "https", "mailto"},
                strip=True,
            )
            clean = clean.split("__DISCUSSION_TAG__", 1)[-1]
        elif tag.rstrip().endswith("/>") or name.lower() in {"br", "hr", "img"}:
            clean = bleach.clean(
                tag,
                tags=TAGS,
                attributes=allowed_attribute,
                protocols={"http", "https", "mailto"},
                strip=True,
            )
        else:
            clean = bleach.clean(
                f"{tag}__DISCUSSION_TAG__</{name}>",
                tags=TAGS,
                attributes=allowed_attribute,
                protocols={"http", "https", "mailto"},
                strip=True,
            )
            clean = clean.split("__DISCUSSION_TAG__", 1)[0]
    else:
        clean = bleach.clean(
            tag,
            tags=TAGS,
            attributes=allowed_attribute,
            protocols={"http", "https", "mailto"},
            strip=True,
        )
    start = len(rewriter.output)
    rewriter.feed(clean)
    output = "".join(rewriter.output[start:])
    del rewriter.output[start:]
    return output


def markdown_line(line, rewriter):
    """Rewrite links and sanitize raw HTML without rendering Markdown to HTML."""
    placeholders = []

    def stash(value):
        placeholders.append(value)
        return f"\x00DISCUSSION{len(placeholders) - 1}\x00"

    line = BACKTICK_MATH.sub(r"$\1$", line)
    line = INLINE_CODE.sub(lambda match: stash(match.group(0)), line)
    line = HTML_TAG.sub(lambda match: stash(sanitize_html_tag(match.group(0), rewriter)), line)

    def rewrite_link(match):
        destination = match.group("destination")
        angled = destination.startswith("<") and destination.endswith(">")
        url = destination[1:-1] if angled else destination
        if UNSAFE_SCHEME.match(urllib.parse.unquote(url)):
            url = "#"
        else:
            scheme = urllib.parse.urlsplit(url).scheme.lower()
            if scheme and scheme not in {"http", "https", "mailto"}:
                url = "#"
            else:
                tag = "img" if match.group("label").startswith("!") else "a"
                url = rewriter.rewrite_url(tag, url)
        wrapped_url = f"<{url}>" if angled else url
        return stash(
            f'{match.group("label")}({wrapped_url}{match.group("title") or ""})'
        )

    line = MARKDOWN_LINK.sub(rewrite_link, line)

    def linkify(match):
        url = match.group(0)
        suffix = ""
        while url and url[-1] in ".,;:!?)]}":
            suffix = url[-1] + suffix
            url = url[:-1]
        if not url:
            return match.group(0)
        return stash(f"[{url}]({url})") + suffix

    line = BARE_URL.sub(linkify, line)
    for index in reversed(range(len(placeholders))):
        line = line.replace(f"\x00DISCUSSION{index}\x00", placeholders[index])
    newline = "\n" if line.endswith("\n") else ""
    line = line[:-1] if newline else line
    trailing = len(line) - len(line.rstrip(" \t"))
    content = line.rstrip(" \t")
    if trailing >= 2 and content:
        line = content + " \\"
    elif trailing:
        line = content
    return line + newline


def render_content(item, downloader=download_attachment):
    """Sanitize discussion content while preserving it as Markdown."""
    normalized_content = item.content.replace("\r\n", "\n").replace("\r", "\n")
    lines = markdown_alerts(normalized_content.splitlines(keepends=True))
    minimum_heading = 6
    in_fence = None
    for line in lines:
        fence = SOURCE_FENCE.match(line)
        if in_fence:
            if fence and fence.group(1)[0] == in_fence[0] and len(fence.group(1)) >= len(in_fence):
                in_fence = None
            continue
        if fence:
            in_fence = fence.group(1)
            continue
        heading = SOURCE_HEADING.match(line.rstrip("\r\n"))
        if heading:
            minimum_heading = min(minimum_heading, len(heading.group(2)))
        for raw_level in re.findall(r"<h([1-6])\b", line, re.IGNORECASE):
            minimum_heading = min(minimum_heading, int(raw_level))

    parser = AttachmentRewriter(item, downloader, max(0, 3 - minimum_heading))
    output = []
    in_fence = None
    math_fence = False
    for line in lines:
        fence = SOURCE_FENCE.match(line)
        if in_fence:
            if fence and fence.group(1)[0] == in_fence[0] and len(fence.group(1)) >= len(in_fence):
                output.append("$$\n" if math_fence else line)
                in_fence = None
                math_fence = False
            else:
                output.append(line)
            continue
        if fence:
            in_fence = fence.group(1)
            math_fence = fence.group(2).strip() == "math"
            output.append("$$\n" if math_fence else line)
            continue

        heading = SOURCE_HEADING.match(line.rstrip("\r\n"))
        if heading:
            level = min(6, len(heading.group(2)) + parser.heading_shift)
            title = heading.group(3).strip()
            parser.attachment_section = attachment_section_slug(
                re.sub(r"[`*_~]", "", re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", title))
            )
            ending = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
            line = f"{heading.group(1)}{'#' * level} {title}{ending}"
        if re.match(r"^ {2}(?:[-+*]|\d+[.)])[ \t]+", line):
            line = "  " + line
        output.append(markdown_line(line, parser))

    parser.close()
    content = "".join(output)
    # Prevent the site's template engine from evaluating discussion text.
    content = content.replace("{{", "&#123;&#123;").replace("{%", "&#123;%")
    return content, parser.assets


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
        "This section highlights the most useful community questions about Khiops, "
        "selected for practical use in real projects.",
        "",
        "The objective is simple: help users find reliable guidance quickly, from "
        "first experiments to production-scale deployments.",
        "",
        "!!! question Have a question or request?",
        "    - **Ask in [GitHub Discussions](https://github.com/orgs/KhiopsML/discussions)**",
        "    - **Report bugs or request product changes in the "
        "[Khiops repository issues](https://github.com/KhiopsML/khiops/issues)**",
        "",
        "The questions and answers are imported from "
        "[Khiops Discussions on GitHub](https://github.com/orgs/KhiopsML/discussions),",
        "",
    ]
    for topic in sorted(grouped):
        entries = []
        title = heading_text(grouped[topic][0].topic_title)
        for item in sorted(grouped[topic], key=lambda value: value.number):
            try:
                content, files = render_content(item, downloader)
            except AttachmentError as exc:
                invalid.append(
                    {
                        "url": item.url,
                        "number": item.number,
                        "file": exc.url,
                        "reason": str(exc),
                    }
                )
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
            page.extend(
                [
                    f"## {safe_title} {{ #{anchor} }}",
                    "",
                    content,
                    "",
                    f"*Source: [discussion #{item.number}]({item.url})*",
                    "",
                ]
            )
        overview.append("")
        pages[f"q-and-a/{slug}.md"] = "\n".join(page)
    pages["q-and-a/overview.md"] = "\n".join(overview)
    return pages, assets, invalid
