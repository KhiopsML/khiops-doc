#!/usr/bin/env python3
"""Generate the public Markdown mirror and the LLM navigation index."""

from __future__ import annotations

import argparse
import os
import re
import shutil
from pathlib import Path
from urllib.parse import quote, unquote, urlparse


KNI_TUTORIAL_EXPORT_SUFFIXES = {".c", ".h", ".java", ".kdic", ".md", ".py", ".txt"}

# A curated section whose links are validated and excluded from "## Others", but never published.
EXCLUDED_SECTION_RE = re.compile(r"\n## Excluded\b.*?(?=\n## |\Z)", re.DOTALL)

# khiops-python's doc stub files hold a single "::: dotted.module.path" directive.
DIRECTIVE_RE = re.compile(r"^:::\s*(\S+)\s*$", re.MULTILINE)
# numpydoc section titles (e.g. "Parameters\n----------") promoted to headings.
NUMPYDOC_SECTION_RE = re.compile(r"^([A-Za-z][A-Za-z0-9 ]*)\n-{3,}\n", re.MULTILINE)
# mkdocstrings/autorefs syntaxes with no meaning once flattened to plain Markdown.
AUTOREF_RE = re.compile(r"\[([^\[\]\n]+)\]\[[^\[\]\n]*\]")
SCOPED_CROSSREF_RE = re.compile(r"`([^`<>\n]+?)\s*<[^`<>\n]+>`")


def is_python_api_doc_page(source: Path) -> bool:
    """Return whether a documentation path is a rendered Python API doc page."""
    return source == Path("api-docs/python-api.md") or source.parts[:2] == ("api-docs", "python-api")


def _lineno(member) -> int:
    """Return a member's source line, or 0 if it is an unresolvable alias (e.g. an import)."""
    try:
        return member.lineno or 0
    except Exception:
        return 0


def write_llms_source(
    source_path: Path, output_path: Path, site_dir: Path, markdown_dir: Path
) -> None:
    """Validate the curated index and append links for unreferenced Markdown pages."""
    if not source_path.is_file():
        raise FileNotFoundError(f"LLM index source does not exist: {source_path}")

    content = source_path.read_text(encoding="utf-8").strip() + "\n"
    if not content.startswith("# "):
        raise ValueError(f"LLM index source must start with a Markdown title: {source_path}")

    missing: list[str] = []
    referenced_markdown: set[str] = set()
    markdown_url_prefix: str | None = None
    for link in re.findall(r"\[[^]]+\]\(([^)]+)\)", content):
        parsed = urlparse(link)
        if parsed.path.startswith(("/markdown/", "/api-docs/")):
            target = site_dir / unquote(parsed.path).lstrip("/")
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                missing.append(link)
        if parsed.path.startswith("/markdown/"):
            if markdown_url_prefix is None:
                markdown_url_prefix = parsed._replace(
                    path="/markdown/", params="", query="", fragment=""
                ).geturl()
            relative_path = Path(unquote(parsed.path.removeprefix("/markdown/")))
            target = markdown_dir / relative_path
            if target.is_dir():
                target /= "index.md"
            elif target.suffix != ".md" and target.with_suffix(".md").is_file():
                target = target.with_suffix(".md")
            if target.is_file():
                referenced_markdown.add(target.relative_to(markdown_dir).as_posix())
    if missing:
        raise FileNotFoundError("LLM index points to missing site paths: " + ", ".join(missing))

    # Links in "## Excluded" are validated and counted as referenced above, but the
    # section itself must not appear in the published llms.txt.
    content = EXCLUDED_SECTION_RE.sub("\n", content).rstrip() + "\n"

    others = [
        source.relative_to(markdown_dir).as_posix()
        for source in sorted(markdown_dir.rglob("*.md"))
        if source.relative_to(markdown_dir).as_posix() not in referenced_markdown
    ]
    if others:
        url_prefix = markdown_url_prefix or "/markdown/"
        content = content.rstrip() + "\n\n## Others\n\n" + "".join(
            f"- [{relative_path}]({url_prefix}{quote(relative_path, safe='/')})\n"
            for relative_path in others
        )

    output_path.write_text(content, encoding="utf-8")


def template_values() -> dict[str, str]:
    """Build template substitutions from configured version variables."""
    core_version = os.environ.get("KHIOPS_VERSION", "unknown")
    python_version = os.environ.get("KHIOPS_PYTHON_VERSION", "unknown")
    return {
        "KHIOPS_VERSION": core_version,
        "KHIOPS_PYTHON_VERSION": python_version,
        "KHIOPS_SAMPLES_VERSION": os.environ.get("KHIOPS_SAMPLES_VERSION", "unknown"),
        "KHIOPS_VIZ_VERSION": os.environ.get("KHIOPS_VIZ_VERSION", "unknown"),
        "KHIOPS_GCS_DRIVER_VERSION": os.environ.get("KHIOPS_GCS_DRIVER_VERSION", "unknown"),
        "KHIOPS_S3_DRIVER_VERSION": os.environ.get("KHIOPS_S3_DRIVER_VERSION", "unknown"),
        "KHIOPS_AZURE_DRIVER_VERSION": os.environ.get("KHIOPS_AZURE_DRIVER_VERSION", "unknown"),
        "PIP_KHIOPS_PYTHON_VERSION": python_version.replace("-rc.", "rc").replace("-b.", "b").replace("-a.", "a"),
        "CONDA_KHIOPS_PYTHON_VERSION": python_version.replace("-rc.", "rc.").replace("-b.", "b.").replace("-a.", "a."),
        "ROCKY_KHIOPS_VERSION": core_version.replace("-", "_"),
    }


def render_markdown(source: Path, values: dict[str, str]) -> str:
    """Remove build directives and substitute version variables in a Markdown source."""
    text = source.read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"\{%\s*set\b.*?%\}\s*", "", text)
    for name, value in values.items():
        text = re.sub(r"\{\{\s*" + re.escape(name) + r"\s*\}\}", value, text)
    return text


def copy_markdown_sources(docs_dir: Path, output_dir: Path, values: dict[str, str]) -> None:
    """Recreate the public Markdown mirror from documentation sources."""
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    for source in sorted(docs_dir.rglob("*.md")):
        relative_path = source.relative_to(docs_dir)
        if is_python_api_doc_page(relative_path):
            continue
        target = output_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_markdown(source, values), encoding="utf-8")


def _clean_docstring(text: str, heading_level: int) -> str:
    """Strip mkdocstrings/autorefs syntax and promote numpydoc sections to headings."""
    text = AUTOREF_RE.sub(lambda m: f"`{m.group(1)}`", text)
    text = SCOPED_CROSSREF_RE.sub(lambda m: f"`{m.group(1)}`", text)
    text = NUMPYDOC_SECTION_RE.sub(lambda m: f"{'#' * heading_level} {m.group(1)}\n\n", text)
    return text.strip()


def _signature(obj) -> str:
    """Build a best-effort Python signature line for a griffe class, function or attribute."""
    if obj.is_class:
        bases = ", ".join(str(base) for base in obj.bases)
        return f"class {obj.name}({bases}):" if bases else f"class {obj.name}:"
    if obj.is_attribute:
        annotation = f": {obj.annotation}" if obj.annotation is not None else ""
        return f"{obj.name}{annotation}"
    params = []
    for param in obj.parameters:
        if param.name in ("self", "cls"):
            continue
        piece = param.name
        if param.annotation is not None:
            piece += f": {param.annotation}"
        if param.default is not None:
            piece += f" = {param.default}"
        params.append(piece)
    returns = f" -> {obj.returns}" if obj.returns is not None else ""
    return f"def {obj.name}({', '.join(params)}){returns}:"


def _render_member(member, heading_level: int) -> str:
    """Render a class or function (and, recursively, a class's public members)."""
    obj = member.target if member.is_alias else member
    blocks = [
        f"{'#' * heading_level} {obj.name}",
        "",
        "```python",
        _signature(obj),
        "```",
        "",
        _clean_docstring(obj.docstring.value, heading_level + 1),
    ]
    if obj.is_class:
        for sub in sorted(obj.members.values(), key=_lineno):
            if sub.is_alias or sub.name in ("__init__",) or sub.name.startswith("_"):
                continue
            if sub.docstring is None or not (sub.is_function or sub.is_attribute):
                continue
            blocks.append("")
            blocks.append(_render_member(sub, heading_level + 1))
    return "\n".join(blocks)


def _render_module(module, heading_level: int) -> str:
    """Render a module's docstring and its public documented classes/functions."""
    blocks = [_clean_docstring(module.docstring.value, heading_level)] if module.docstring else []
    for member in sorted(module.members.values(), key=_lineno):
        if member.is_alias or member.name.startswith("_"):
            continue
        if member.docstring is None or not (member.is_class or member.is_function):
            continue
        blocks.append(_render_member(member, heading_level))
    return "\n\n".join(blocks).strip() + "\n"


def _resolve_module(root, dotted_path: str):
    """Walk a dotted path (e.g. 'khiops.sklearn.estimators') from a loaded griffe root."""
    obj = root
    for part in dotted_path.split(".")[1:]:
        obj = obj.members[part]
        if obj.is_alias:
            obj = obj.target
    return obj


def render_python_api_pages(docs_dir: Path, output_dir: Path) -> int:
    """Render the Python API Markdown pages directly from the khiops docstrings.

    The doc stub files only hold a mkdocstrings directive (e.g. `::: khiops
    .sklearn.estimators`); this resolves it via griffe and renders the actual
    docstring content, instead of relying on Zensical's HTML build (which
    bakes in web-only artifacts like same-page anchors and JS tooltips).
    """
    source_root = docs_dir / "api-docs" / "python-api"
    if not source_root.is_dir():
        return 0

    import griffe

    try:
        root = griffe.GriffeLoader().load("khiops")
    except ImportError:
        return 0

    exported = 0
    for source in sorted(source_root.rglob("*.md")):
        relative_path = source.relative_to(source_root)
        text = source.read_text(encoding="utf-8")
        match = DIRECTIVE_RE.search(text)
        if match:
            module = _resolve_module(root, match.group(1))
            prefix = text[: match.start()].rstrip("\n")
            body = _render_module(module, heading_level=2)
            text = f"{prefix}\n\n{body}" if prefix else body

        target = output_dir / "api-docs" / "python-api" / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        exported += 1
    return exported


def copy_kni_tutorial(source_dir: Path, output_dir: Path) -> int:
    """Copy supported KNI tutorial files into the Markdown mirror."""
    if not source_dir.is_dir():
        raise FileNotFoundError(f"KNI tutorial directory does not exist: {source_dir}")

    exported = 0
    for source in sorted(source_dir.rglob("*")):
        relative_path = source.relative_to(source_dir)
        if (
            not source.is_file()
            or any(part.startswith(".") for part in relative_path.parts)
            or source.suffix.lower() not in KNI_TUTORIAL_EXPORT_SUFFIXES
        ):
            continue

        target = output_dir / "tutorials" / "kni-tutorial" / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        exported += 1
    return exported


def main() -> None:
    """Generate the public Markdown mirror and LLM navigation index."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs-dir", type=Path, required=True)
    parser.add_argument("--site-dir", type=Path, required=True)
    parser.add_argument("--llms-source", type=Path, required=True)
    parser.add_argument("--kni-tutorial-dir", type=Path, required=True)
    args = parser.parse_args()

    markdown_dir = args.site_dir / "markdown"
    copy_markdown_sources(args.docs_dir, markdown_dir, template_values())
    python_api_pages = render_python_api_pages(args.docs_dir, markdown_dir)
    kni_files = copy_kni_tutorial(args.kni_tutorial_dir, markdown_dir)
    write_llms_source(
        args.llms_source, args.site_dir / "llms.txt", args.site_dir, markdown_dir
    )
    print(
        f"Generated {args.site_dir / 'llms.txt'} and "
        f"{len(list(markdown_dir.rglob('*.md')))} Markdown pages "
        f"({python_api_pages} Python API pages, {kni_files} KNI tutorial files)"
    )


if __name__ == "__main__":
    main()