#!/usr/bin/env bash
set -euo pipefail

# prepare-python-api-doc.sh — Clone khiops-python, prepare its Zensical-based
# Python API doc sources (Markdown only, via `create-doc -p`), copy them into
# khiops-doc's docs/ tree, and regenerate the "API Python" nav section of
# mkdocs.yml. Does NOT build the site — that's done once, separately, for
# the whole khiops-doc site.
#
# Usage:
#   prepare-python-api-doc.sh [OPTIONS]
#
# Options:
#   --khiops-python-repo URL_OR_DIR   khiops-python repo to clone (Git URL or
#                                      local path). Default: KhiopsML/khiops-python
#   --khiops-python-ref REF           Git ref/tag/branch to check out.
#                                      Default: main
#   --khiops-samples-version VERSION  khiops-samples release to download.
#                                      Default: main
#   --khiops-python-tutorial-ref REF  khiops-python-tutorial Git ref used by
#                                      create-doc -g. Default: main

KHIOPS_PYTHON_REPO="https://github.com/KhiopsML/khiops-python.git"
KHIOPS_PYTHON_REF="main"
KHIOPS_SAMPLES_VERSION="main"
KHIOPS_PYTHON_TUTORIAL_REF="main"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --khiops-python-repo) KHIOPS_PYTHON_REPO="$2"; shift 2 ;;
    --khiops-python-ref) KHIOPS_PYTHON_REF="$2"; shift 2 ;;
    --khiops-samples-version) KHIOPS_SAMPLES_VERSION="$2"; shift 2 ;;
    --khiops-python-tutorial-ref) KHIOPS_PYTHON_TUTORIAL_REF="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

export PIP_NO_CACHE_DIR=1

cleanup() {
  echo "--- Cleaning up"
  rm -rf ./khiops_samples ./khiops-python-src
}
trap cleanup EXIT

echo "=== Preparing Python API docs from ${KHIOPS_PYTHON_REPO} @ ${KHIOPS_PYTHON_REF} ==="

# 1. Clone khiops-python
rm -rf ./khiops-python-src
git clone "$KHIOPS_PYTHON_REPO" ./khiops-python-src
git -C ./khiops-python-src checkout "$KHIOPS_PYTHON_REF"

# 2. Install khiops-python itself into the current (khiops-doc) environment,
#    so mkdocstrings can import/introspect it. Note: doc/util/requirements.txt
#    is NOT installed wholesale here — it pulls in its own zensical/mkdocstrings
#    pins, which khiops-doc already supplies via pyproject.toml.
uv pip install ./khiops-python-src
uv pip install nbformat mkdocstrings-python

# 4. Prepare doc sources (Markdown only — no Zensical build here)
echo "--- Preparing khiops-python doc sources (create-doc -p)"
(
  cd khiops-python-src
  uv run --active --frozen --no-sync kh-download-datasets --force-overwrite --version "$KHIOPS_SAMPLES_VERSION"
  cd doc/util
  bash create-doc -p -t -d -g "$KHIOPS_PYTHON_TUTORIAL_REF"
)

# 5. Copy prepared doc sources into the khiops-doc docs tree
echo "--- Copying doc sources into docs/api-docs/python-api/"
rm -rf docs/api-docs/python-api
mkdir -p docs/api-docs/python-api
for dir in core sklearn tools internal _templates; do
  [ -d "khiops-python-src/doc/site/$dir" ] && \
    cp -r "khiops-python-src/doc/site/$dir" docs/api-docs/python-api/
done
for f in index.md notes.md multi_table_primer.md; do
  [ -f "khiops-python-src/doc/site/$f" ] && \
    cp "khiops-python-src/doc/site/$f" docs/api-docs/python-api/
done

# Tutorials: only .md and .zip (no .ipynb — avoids mkdocs-jupyter conflicts)
if [ -d khiops-python-src/doc/site/tutorials ]; then
  mkdir -p docs/api-docs/python-api/tutorials
  find khiops-python-src/doc/site/tutorials -maxdepth 1 -name "*.md" \
    -exec cp {} docs/api-docs/python-api/tutorials/ \;
  find khiops-python-src/doc/site/tutorials -maxdepth 1 -name "*.zip" \
    -exec cp {} docs/api-docs/python-api/tutorials/ \;
fi

# Samples: .md, .py, .ipynb (the latter for download links)
if [ -d khiops-python-src/doc/site/samples ]; then
  mkdir -p docs/api-docs/python-api/samples
  cp khiops-python-src/doc/site/samples/*.md    docs/api-docs/python-api/samples/ 2>/dev/null || true
  cp khiops-python-src/doc/site/samples/*.py    docs/api-docs/python-api/samples/ 2>/dev/null || true
  cp khiops-python-src/doc/site/samples/*.ipynb docs/api-docs/python-api/samples/ 2>/dev/null || true
fi

# 6. Regenerate the "API Python" nav section of mkdocs.yml from khiops-python's
#    zensical.toml
echo "--- Generating Python API nav"
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
uv run --active --frozen --no-sync ${SCRIPT_DIR}/generate_python_api_nav.py \
  --source ./khiops-python-src/zensical.toml --target zensical.toml \
  --output zensical.toml --section "API Python" \
  --source-index-title "Home" \
  --source-index-file "index.md" \
  --target-index-title "Python API" \
  --path-prefix "api-docs/python-api/"

# 7. Remove stall Python API Markdown file
rm -f docs/api-docs/python-api.md

echo "=== Python API doc sources ready ==="
