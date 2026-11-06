"""Render discussion content and collect safe GitHub attachments."""

import hashlib
import html
import re
import urllib.parse
import urllib.request
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import PurePosixPath

import bleach
import markdown

from python.discussions.discussion_content import InvalidDiscussion


MAX_ATTACHMENT_BYTES = 100_000
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


class AttachmentError(InvalidDiscussion):
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


def heading_text(value):
    """Normalize and escape a title for Markdown, HTML and site templates."""
    value = " ".join(value.split())
    value = html.escape(value, quote=False)
    value = value.replace("{{", "&#123;&#123;").replace("{%", "&#123;%")
    return re.sub(r"([\\`*_{}\[\]()#+.!|>-])", r"\\\1", value)


class AttachmentRewriter(HTMLParser):
    def __init__(self, item, downloader):
        """Initialize output and collected assets for one discussion."""
        super().__init__(convert_charrefs=False)
        self.item = item
        self.downloader = downloader
        self.output = []
        self.assets = {}

    def handle_starttag(self, tag, attrs):
        """Copy supported attachments and rewrite their URLs in a start tag.

        Relative links are resolved against the source discussion. Downloaded
        assets are stored by site-relative path for the caller to publish.
        """
        attrs = dict(attrs)
        key = "src" if tag == "img" else "href" if tag == "a" else None
        if key and key in attrs:
            url = attrs[key]
            parsed = urllib.parse.urlsplit(url)
            script = tag == "a" and PurePosixPath(parsed.path).suffix.lower() in SCRIPT_EXTENSIONS
            if github_attachment(url) and (tag == "img" or script):
                content, content_type = self.downloader(url)
                if len(content) > MAX_ATTACHMENT_BYTES:
                    raise AttachmentError(url, "attachment exceeds 100,000 bytes")
                if tag == "img":
                    extension = IMAGE_EXTENSIONS.get(content_type)
                    if extension is None:
                        raise AttachmentError(url, f"unsupported image type {content_type}")
                    category = "images"
                else:
                    extension = PurePosixPath(parsed.path).suffix.lower()
                    category = "discussion-scripts"
                digest = hashlib.sha256(url.encode()).hexdigest()[:16]
                path = f"assets/{category}/q-and-a/{topic_slug(self.item.topic)}/{digest}{extension}"
                self.assets[path] = content
                attrs[key] = "/" + path
            elif not parsed.scheme and not url.startswith(("#", "/")):
                attrs[key] = urllib.parse.urljoin(self.item.url + "/", url)
        attributes = "".join(
            f' {name}="{html.escape(value, quote=True)}"' for name, value in attrs.items() if value is not None
        )
        self.output.append(f"<{tag}{attributes}>")

    def handle_startendtag(self, tag, attrs):
        """Process self-closing tags like start tags."""
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        """Append a closing tag to the rendered output."""
        self.output.append(f"</{tag}>")

    def handle_data(self, data):
        """Preserve text content in the rendered output."""
        self.output.append(data)

    def handle_entityref(self, name):
        """Preserve a named HTML entity in the rendered output."""
        self.output.append(f"&{name};")

    def handle_charref(self, name):
        """Preserve a numeric HTML entity in the rendered output."""
        self.output.append(f"&#{name};")


def render_content(item, downloader=download_attachment):
    """Render and sanitize one discussion, returning HTML and copied assets."""
    rendered = markdown.markdown(item.content, extensions=["fenced_code", "tables", "sane_lists"])
    clean = bleach.clean(rendered, tags=TAGS, attributes=ATTRIBUTES, protocols={"http", "https", "mailto"}, strip=True)
    parser = AttachmentRewriter(item, downloader)
    parser.feed(clean)
    parser.close()
    # Prevent the site's template engine from evaluating discussion text.
    output = "".join(parser.output).replace("{{", "&#123;&#123;").replace("{%", "&#123;%")
    return output, parser.assets


def render_pages(items, downloader=download_attachment, include_manifest=False):
    """Render topic pages and an overview from publishable discussions.

    Return pages, assets and attachment errors; optionally append a manifest
    keyed by discussion ID. Discussions with rejected attachments are omitted.
    """
    grouped = defaultdict(list)
    for item in items:
        grouped[item.topic].append(item)
    pages = {}
    assets = {}
    invalid = []
    manifest = {}
    overview = ["# Questions and answers", ""]
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
            digest = hashlib.sha256()
            digest.update(item.title.encode())
            digest.update(b"\0")
            digest.update(content.encode())
            for path, data in sorted(files.items()):
                digest.update(path.encode())
                digest.update(b"\0")
                digest.update(data)
            manifest[item.id] = {
                "number": item.number,
                "title": item.title,
                "url": item.url,
                "topic": item.topic,
                "topic_title": item.topic_title,
                "digest": digest.hexdigest(),
            }
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
    result = (pages, assets, invalid)
    return (*result, manifest) if include_manifest else result
