from __future__ import annotations

import os
import re
import shutil
from html import escape
from pathlib import Path

import nbformat
from nbconvert import MarkdownExporter
from nbconvert.preprocessors import ExecutePreprocessor


ROOT_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT_DIR / "docs" / "tutorials" / "sourced-notebooks"
OUTPUT_DIR = ROOT_DIR / "docs" / "tutorials" / "notebooks"
MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
HTML_OUTPUT_MARKERS = ("<div", "<table", "<img", "<style", "<svg")


def env_flag(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def notebook_prompt(kind: str, execution_count: int | None) -> str:
    count = execution_count if execution_count is not None else " "
    return f"{kind} [{count}]:"


def wrap_notebook_cell(kind: str, prompt: str, body: str, *, parse_markdown: bool = False) -> str:
    classes = f"khiops-notebook-cell khiops-notebook-{kind}"
    markdown_attr = ' markdown="1"' if parse_markdown else ""
    return (
        f'<div class="{classes}" data-prompt="{escape(prompt)}"{markdown_attr}>\n\n'
        f"{body.strip()}\n\n"
        "</div>"
    )


def split_code_cell_body(body: str) -> tuple[str, str]:
    lines = body.splitlines(keepends=True)
    fence_start = next((index for index, line in enumerate(lines) if line.startswith("```")), None)

    if fence_start is None:
        return body, ""

    fence_end = next(
        (index for index, line in enumerate(lines[fence_start + 1 :], start=fence_start + 1) if line.startswith("```")),
        None,
    )

    if fence_end is None:
        return body, ""

    return "".join(lines[: fence_end + 1]), "".join(lines[fence_end + 1 :])


def ensure_python_fence(body: str) -> str:
    if body.startswith("```\n"):
        return "```python\n" + body.removeprefix("```\n")
    return body


def has_html_output(body: str) -> bool:
    return any(marker in body for marker in HTML_OUTPUT_MARKERS)


def convert_markdown_images(body: str) -> str:
    def replace_image(match: re.Match[str]) -> str:
        alt_text, image_path = match.groups()
        return f'<img alt="{escape(alt_text, quote=True)}" src="{escape(image_path, quote=True)}" />'

    return MARKDOWN_IMAGE_RE.sub(replace_image, body.strip())


def render_output_body(body: str) -> str:
    body = body.strip()
    if has_html_output(body):
        return body
    if MARKDOWN_IMAGE_RE.search(body):
        return convert_markdown_images(body)
    return f"<pre>{escape(body)}</pre>"


def normalize_notebook_target(link_target: str, notebook_stems: set[str]) -> str | None:
    if not link_target or "://" in link_target or link_target.startswith("mailto:") or link_target.startswith("#"):
        return None

    base_target, hash_sep, fragment = link_target.partition("#")
    base_target, query_sep, query = base_target.partition("?")

    normalized_target = base_target.rstrip("/")
    prefixes = (
        "/tutorials/Notebooks/",
        "/tutorials/sourced-notebooks/",
        "/tutorials/notebooks/",
        "/tutorials/notebook-pages/",
        "/tutorials/",
        "../",
        "./",
    )

    candidate = normalized_target
    for prefix in prefixes:
        if candidate.startswith(prefix):
            candidate = candidate[len(prefix) :]
            break

    candidate = candidate.rstrip("/")
    for suffix in (".ipynb", ".md"):
        if candidate.endswith(suffix):
            candidate = candidate[: -len(suffix)]

    if candidate not in notebook_stems:
        return None

    rewritten = f"./{candidate}"
    if query_sep:
        rewritten += f"?{query}"
    if hash_sep:
        rewritten += f"#{fragment}"
    return rewritten


def rewrite_markdown_notebook_links(body: str, notebook_stems: set[str]) -> str:
    def replace_link(match: re.Match[str]) -> str:
        link_text, link_target = match.groups()
        rewritten_target = normalize_notebook_target(link_target.strip(), notebook_stems)
        if rewritten_target is None:
            return match.group(0)
        return f"[{link_text}]({rewritten_target})"

    return MARKDOWN_LINK_RE.sub(replace_link, body)


def convert_cell(
    exporter: MarkdownExporter,
    cell: nbformat.NotebookNode,
    resources: dict,
    cell_index: int,
    notebook_stems: set[str],
) -> tuple[str, dict]:
    cell = cell.copy()
    cell.setdefault("id", f"generated-{cell_index}")
    cell_notebook = nbformat.v4.new_notebook(cells=[cell])
    body, resources = exporter.from_notebook_node(cell_notebook, resources=resources)

    if cell.cell_type != "code":
        return rewrite_markdown_notebook_links(body.strip(), notebook_stems), resources

    execution_count = cell.get("execution_count")
    input_body, output_body = split_code_cell_body(body)
    input_body = ensure_python_fence(input_body)
    converted_parts = [
        wrap_notebook_cell("input", notebook_prompt("In", execution_count), input_body, parse_markdown=True)
    ]

    if output_body.strip():
        converted_parts.append(
            wrap_notebook_cell("output", notebook_prompt("Out", execution_count), render_output_body(output_body))
        )

    return "\n\n".join(converted_parts), resources


def convert_notebook(notebook_path: Path, execute: bool, notebook_stems: set[str]) -> None:
    notebook = nbformat.read(notebook_path, as_version=4)

    if execute:
        executor = ExecutePreprocessor(timeout=-1, kernel_name="python3", allow_errors=False)
        executor.preprocess(notebook, {"metadata": {"path": str(SOURCE_DIR)}})

    exporter = MarkdownExporter()
    converted_cells = []
    output_resources = {}
    for cell_index, cell in enumerate(notebook.cells):
        resources = {
            "metadata": {"path": str(SOURCE_DIR)},
            "output_files_dir": f"{notebook_path.stem}_files",
            "unique_key": f"{notebook_path.stem}_{cell_index}",
        }
        cell_body, resources = convert_cell(exporter, cell, resources, cell_index, notebook_stems)
        if cell_body:
            converted_cells.append(cell_body)
        output_resources.update(resources.get("outputs", {}))

    body = "\n\n".join(converted_cells)

    header = (
        "<!-- Generated by scripts/convert_notebooks.py; do not edit by hand. -->\n\n"
        '<div class="khiops-notebook-download" markdown="1">'
        f"[:material-download: Download source notebook](../sourced-notebooks/{notebook_path.name})"
        "</div>\n\n"
    )
    (OUTPUT_DIR / f"{notebook_path.stem}.md").write_text(header + body, encoding="utf-8")

    for relative_path, content in output_resources.items():
        output_path = OUTPUT_DIR / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(content)


def prepare_output_dir() -> None:
    if SOURCE_DIR.name.lower() == OUTPUT_DIR.name.lower():
        raise RuntimeError(f"Refusing to generate notebook pages into {OUTPUT_DIR}")

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)


def main() -> None:
    execute = env_flag("EXECUTE_KHIOPS_TUTORIALS")
    prepare_output_dir()

    notebooks = sorted(SOURCE_DIR.glob("*.ipynb"))
    notebook_stems = {notebook_path.stem for notebook_path in notebooks}
    for notebook_path in notebooks:
        convert_notebook(notebook_path, execute, notebook_stems)
        action = "Executed and converted" if execute else "Converted"
        print(f"{action} {notebook_path.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()