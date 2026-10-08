#!/usr/bin/env python3
"""Generate the public Markdown mirror and the LLM navigation index."""

from __future__ import annotations

import argparse
import os
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse


def is_python_api(source: Path) -> bool:
    return source == Path("api-docs/python-api.md") or source.parts[:2] == ("api-docs", "python-api")


def write_llms_source(source_path: Path, output_path: Path, site_dir: Path) -> None:
    if not source_path.is_file():
        raise FileNotFoundError(f"LLM index source does not exist: {source_path}")

    content = source_path.read_text(encoding="utf-8").strip() + "\n"
    if not content.startswith("# "):
        raise ValueError(f"LLM index source must start with a Markdown title: {source_path}")

    missing: list[str] = []
    for link in re.findall(r"\[[^]]+\]\(([^)]+)\)", content):
        parsed = urlparse(link)
        if parsed.path.startswith(("/markdown/", "/api-docs/")):
            target = site_dir / parsed.path.lstrip("/")
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                missing.append(link)
    if missing:
        raise FileNotFoundError("LLM index points to missing site paths: " + ", ".join(missing))

    output_path.write_text(content, encoding="utf-8")


def template_values() -> dict[str, str]:
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
    text = source.read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"\{%\s*set\b.*?%\}\s*", "", text)
    for name, value in values.items():
        text = re.sub(r"\{\{\s*" + re.escape(name) + r"\s*\}\}", value, text)
    return text


def copy_markdown_sources(docs_dir: Path, output_dir: Path, values: dict[str, str]) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    for source in sorted(docs_dir.rglob("*.md")):
        relative_path = source.relative_to(docs_dir)
        if is_python_api(relative_path):
            continue
        target = output_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_markdown(source, values), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs-dir", type=Path, required=True)
    parser.add_argument("--site-dir", type=Path, required=True)
    parser.add_argument("--llms-source", type=Path, required=True)
    args = parser.parse_args()

    copy_markdown_sources(args.docs_dir, args.site_dir / "markdown", template_values())
    write_llms_source(args.llms_source, args.site_dir / "llms.txt", args.site_dir)
    print(
        f"Generated {args.site_dir / 'llms.txt'} and "
        f"{len(list((args.site_dir / 'markdown').rglob('*.md')))} Markdown pages"
    )


if __name__ == "__main__":
    main()