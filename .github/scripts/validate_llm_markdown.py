#!/usr/bin/env python3
"""Validate Zensical's LLM index and Markdown exports after a site build.

The shared build runs this read-only check after copying static KNI resources
into the site. It uses the llmstxt section selectors and excluded source
patterns from the Zensical configuration to check that:

* Every Markdown source is selected or excluded, but not both.
* Selected pages have nonempty exports linked from a nonempty index, while
  excluded pages are not linked from it.
* Local index links and images resolve to files within the built site, and no
  ``llms-full.txt`` aggregate is present.

External destinations and URLs outside the configured site base path are not
checked. Fragments and links inside exported pages are not validated, and no
artifacts are rewritten. Failures are reported as ``ValidationError`` and
cause the command to exit with a nonzero status.
"""

import argparse
import fnmatch
import posixpath
import re
import tomllib
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urljoin, urlsplit

import markdown


class ValidationError(RuntimeError):
    """Raised when an LLM documentation artifact is invalid."""


class IndexLinks(HTMLParser):
    """Collect link and image destinations from the rendered Markdown index."""

    def __init__(self):
        super().__init__()
        self.destinations: list[str] = []

    def handle_starttag(self, tag, attrs):
        """Collect href and src attributes from anchor and image tags."""
        attributes = dict(attrs)
        if tag == "a" and "href" in attributes:
            self.destinations.append(attributes["href"])
        elif tag == "img" and "src" in attributes:
            self.destinations.append(attributes["src"])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def _origin(url):
    """Return a normalized scheme, host and port for a parsed URL."""
    try:
        port = url.port
    except ValueError as error:
        raise ValidationError(f"Invalid URL port in {url.geturl()!r}") from error
    if port is None:
        port = {"http": 80, "https": 443}.get(url.scheme.lower())
    return url.scheme.lower(), (url.hostname or "").lower(), port


def _decode_path(path):
    """Decode URL path segments, rejecting invalid encoding and separators."""
    decoded = []
    for segment in path.split("/"):
        if re.search(r"%(?![0-9A-Fa-f]{2})", segment):
            raise ValidationError(f"Invalid percent encoding in path {path!r}")
        try:
            value = unquote(segment, errors="strict")
        except UnicodeDecodeError as error:
            raise ValidationError(f"Invalid UTF-8 in path {path!r}") from error
        if "/" in value or "\\" in value or "\x00" in value:
            raise ValidationError(f"Invalid path segment in {path!r}")
        decoded.append(value)
    return "/".join(decoded)


def _check_relative_traversal(path, index_name):
    """Reject relative destinations that escape the site from the index."""
    if path.startswith("/"):
        return
    parts = list(PurePosixPath(index_name).parent.parts)
    if parts == ["."]:
        parts = []
    for part in _decode_path(path).split("/"):
        if part == "..":
            if not parts:
                raise ValidationError("destination escapes the site directory")
            parts.pop()
        elif part and part != ".":
            parts.append(part)


def _index_targets(site_dir, site_url, index_name, content):
    """Resolve local index destinations to existing files under the site.

    Markdown is rendered before links and images are collected, so reference
    links are supported and code is ignored. External destinations and
    absolute URLs outside the site base path are skipped. Query strings and
    fragments do not participate in the file existence check.
    """
    base = urlsplit(site_url)
    if (
        base.scheme.lower() not in ("http", "https")
        or not base.hostname
        or base.username
        or base.password
        or base.query
        or base.fragment
    ):
        raise ValidationError(f"Invalid site URL: {site_url!r}")
    origin = _origin(base)
    base_path = _decode_path(base.path or "/").rstrip("/")
    index_url = urljoin(site_url.rstrip("/") + "/", index_name)
    links = IndexLinks()
    links.feed(markdown.markdown(content, extensions=["fenced_code"]))
    targets = set()
    for destination in links.destinations:
        try:
            original = urlsplit(destination)
            resolved = urlsplit(urljoin(index_url, destination))
            if resolved.scheme.lower() not in ("http", "https"):
                continue
            if resolved.username or resolved.password or _origin(resolved) != origin:
                continue
            if not original.scheme and not original.netloc:
                _check_relative_traversal(original.path, index_name)
            path = _decode_path(resolved.path)
            if base_path and path != base_path and not path.startswith(base_path + "/"):
                if original.scheme or original.netloc or original.path.startswith("/"):
                    continue
                raise ValidationError("destination escapes the configured site base path")
            relative = path[len(base_path):].lstrip("/")
            normalized = posixpath.normpath(relative)
            if normalized == ".." or normalized.startswith("../"):
                raise ValidationError("destination escapes the site directory")
            target = (site_dir / normalized).resolve()
            if not target.is_relative_to(site_dir):
                raise ValidationError("destination escapes the site directory")
            if not target.is_file():
                raise ValidationError("local target does not exist")
            targets.add(target)
        except (ValueError, ValidationError) as error:
            raise ValidationError(
                f"{index_name}: destination {destination!r}: {error}"
            ) from error
    return targets


def _settings(configuration):
    """Extract and validate the configured selectors and exclusion patterns."""
    try:
        sections = configuration["plugins"]["llmstxt"]["sections"]
        excluded = configuration["extra"]["llmstxt"]["excluded_sources"]
    except (KeyError, TypeError) as error:
        raise ValidationError(
            "Zensical config must define llmstxt sections and extra.llmstxt.excluded_sources."
        ) from error
    if not isinstance(sections, dict) or not isinstance(excluded, list):
        raise ValidationError("Invalid llmstxt sections or excluded_sources configuration.")
    selectors = []
    for section, entries in sections.items():
        if not isinstance(entries, list):
            raise ValidationError(f"Invalid llmstxt page list in section {section!r}.")
        for entry in entries:
            if isinstance(entry, str):
                selector = entry
            elif isinstance(entry, dict) and len(entry) == 1:
                selector = next(iter(entry))
            else:
                raise ValidationError(f"Invalid llmstxt selector in section {section!r}: {entry!r}")
            selectors.append(selector)
    for pattern in selectors + excluded:
        if (
            not isinstance(pattern, str)
            or not pattern
            or "\\" in pattern
            or PurePosixPath(pattern).is_absolute()
            or ".." in PurePosixPath(pattern).parts
        ):
            raise ValidationError(f"Invalid documentation source pattern: {pattern!r}")
    return selectors, excluded


def _selected_sources(source_root, selectors):
    """Return all Markdown sources and those matched by the index selectors.

    Like Zensical, treat a selector as a glob only when it contains ``*``;
    each selector must match at least one source.
    """
    sources = {
        path.relative_to(source_root).as_posix()
        for path in source_root.rglob("*.md")
        if path.is_file() and not path.is_symlink()
    }
    selected = set()
    for pattern in selectors:
        # Zensical treats a selector as a glob only when it contains '*'.
        if "*" in pattern:
            matches = {source for source in sources if fnmatch.fnmatchcase(source, pattern)}
        else:
            matches = {pattern} & sources
        if not matches:
            raise ValidationError(f"Selected documentation pattern {pattern!r} matches no Markdown source.")
        selected.update(matches)
    return sources, selected


def _excluded_sources(source_root, patterns):
    """Expand exclusion globs into safe source paths relative to the root."""
    excluded = set()
    for pattern in patterns:
        try:
            candidates = source_root.glob(pattern)
            for path in candidates:
                if not path.is_file() or path.suffix.lower() != ".md":
                    continue
                if path.is_symlink() or not path.resolve().is_relative_to(source_root):
                    raise ValidationError(f"Excluded documentation source escapes source directory: {path}")
                excluded.add(path.relative_to(source_root).as_posix())
        except (NotImplementedError, ValueError) as error:
            raise ValidationError(f"Invalid excluded documentation pattern {pattern!r}: {error}") from error
    return excluded


def _export_path(source, directory_urls):
    """Map a source path to its expected Zensical Markdown export path."""
    source_path = PurePosixPath(source)
    if not directory_urls or source_path.name == "index.md":
        return source_path
    return source_path.with_suffix("") / "index.md"


def _read_index(site_root, index_name):
    """Read the built index and reject missing, empty or unwanted artifacts."""
    index_relative = Path(index_name)
    if index_relative.is_absolute() or ".." in index_relative.parts:
        raise ValidationError(f"Index path must stay inside the site: {index_name!r}")
    index = (site_root / index_relative).resolve()
    if not index.is_relative_to(site_root) or not index.is_file():
        raise ValidationError(f"Built native index does not exist or escapes the site: {index_name}")
    content = index.read_text(encoding="utf-8")
    if not content.strip():
        raise ValidationError(f"Built native index is empty: {index_name}")
    if (site_root / "llms-full.txt").exists():
        raise ValidationError("The built site must not contain llms-full.txt; disable full_output.")
    return content


def _validate_source_coverage(source_root, configuration):
    """Check configuration and classify every source as selected or excluded."""
    selectors, excluded_patterns = _settings(configuration)
    sources, selected = _selected_sources(source_root, selectors)
    excluded = _excluded_sources(source_root, excluded_patterns)
    overlap = sorted(selected & excluded)
    if overlap:
        raise ValidationError("Documentation sources are both selected and excluded: " + ", ".join(overlap))
    unclassified = sorted(sources - selected - excluded)
    if unclassified:
        raise ValidationError(
            "Markdown sources must be selected for llms.txt or explicitly excluded: "
            + ", ".join(unclassified)
        )
    return selected, excluded


def _validate_exports(site_root, site_url, index_name, content, configuration, selected, excluded):
    """Check index destinations and the selected and excluded export paths."""
    targets = _index_targets(site_root, site_url, index_name, content)
    directory_urls = configuration.get("use_directory_urls", True)
    if not isinstance(directory_urls, bool):
        raise ValidationError("use_directory_urls must be a boolean.")
    for source in sorted(selected):
        export = (site_root / _export_path(source, directory_urls)).resolve()
        if not export.is_relative_to(site_root) or not export.is_file():
            raise ValidationError(f"Selected source {source!r} has no generated Markdown export.")
        if not export.read_bytes().strip():
            raise ValidationError(f"Selected source {source!r} has an empty Markdown export.")
        if export not in targets:
            raise ValidationError(f"Selected Markdown export is missing from {index_name}: {source}")
    for source in sorted(excluded):
        export = (site_root / _export_path(source, directory_urls)).resolve()
        if export in targets:
            raise ValidationError(f"Excluded source is listed in {index_name}: {source}")


def validate_site(site_dir, site_url, configuration, source_dir, index_name="llms.txt"):
    """Validate index destinations, source coverage and selected exports.

    Paths are resolved against the provided site and source directories.
    Raise ``ValidationError`` on an invalid artifact or configuration; leave
    the site unchanged on both success and failure.
    """
    site_root = Path(site_dir).resolve()
    source_root = Path(source_dir).resolve()
    if not site_root.is_dir():
        raise ValidationError(f"Built site directory does not exist: {site_root}")
    if not source_root.is_dir():
        raise ValidationError(f"Documentation source directory does not exist: {source_root}")

    content = _read_index(site_root, index_name)
    selected, excluded = _validate_source_coverage(source_root, configuration)
    _validate_exports(site_root, site_url, index_name, content, configuration, selected, excluded)


def main(argv=None):
    """Load CLI options and configuration, then report validation results."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", default="site")
    parser.add_argument("--config", default="zensical.toml")
    parser.add_argument("--index", default="llms.txt")
    args = parser.parse_args(argv)
    config_path = Path(args.config)
    try:
        with config_path.open("rb") as file:
            configuration = tomllib.load(file)
        site_url = configuration.get("site_url")
        source_dir = configuration.get("docs_dir", "docs")
        if not isinstance(site_url, str) or not site_url:
            raise ValidationError(f"Zensical config {config_path} has no valid site_url.")
        if not isinstance(source_dir, str) or not source_dir:
            raise ValidationError(f"Zensical config {config_path} has no valid docs_dir.")
        source_dir = config_path.resolve().parent / source_dir
        validate_site(args.site_dir, site_url, configuration, source_dir, args.index)
    except (OSError, UnicodeError, tomllib.TOMLDecodeError, ValidationError) as error:
        parser.exit(1, f"LLM artifact validation failed: {error}\n")
    print("LLM index and selected artifacts validated.")


if __name__ == "__main__":
    main()
