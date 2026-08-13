#!/usr/bin/env bash
set -euo pipefail

# local-build.sh — Build the Khiops doc site locally with Zensical
# (no Docker, no multi-version/mike support).
#
# Prerequisites:
#   - uv (https://docs.astral.sh/uv/)
#   - git, wget, unzip
#   - Optional: conda/Miniforge (only needed with --execute-tutorials, to
#     install a real Khiops core binary)
#
# Usage:
#   ./local-build.sh [OPTIONS]

usage() {
  cat <<EOF
Usage: ./local-build.sh [OPTIONS]

Build the Khiops doc site locally with Zensical.

Options:
  -h, --help                       Show this help message and exit
  --local-khiops-python DIR        Use a local khiops-python repo instead of
                                    cloning from GitHub
  --khiops-python-ref REF          khiops-python Git ref to build docs from
                                    when not using --local-khiops-python
                                    (default: main)
  --khiops-samples-version VER     khiops-samples release to download
                                    (default: main)
  --khiops-python-tutorial-ref REF khiops-python-tutorial Git ref (default: main)
  --khiops-version VER             Khiops core version to install via Conda
                                    (required with --execute-tutorials)
  --execute-tutorials              Actually execute the Khiops tutorials
                                    (requires Khiops core; installs it via Conda)
  --serve                          Run 'zensical serve' after building
EOF
  exit 0
}

LOCAL_KHIOPS_PYTHON=""
KHIOPS_PYTHON_REF="main"
KHIOPS_SAMPLES_VERSION="main"
KHIOPS_PYTHON_TUTORIAL_REF="main"
KHIOPS_VERSION=""
EXECUTE_TUTORIALS="false"
SERVE="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage ;;
    --local-khiops-python) LOCAL_KHIOPS_PYTHON="$2"; shift 2 ;;
    --khiops-python-ref) KHIOPS_PYTHON_REF="$2"; shift 2 ;;
    --khiops-samples-version) KHIOPS_SAMPLES_VERSION="$2"; shift 2 ;;
    --khiops-python-tutorial-ref) KHIOPS_PYTHON_TUTORIAL_REF="$2"; shift 2 ;;
    --khiops-version) KHIOPS_VERSION="$2"; shift 2 ;;
    --execute-tutorials) EXECUTE_TUTORIALS="true"; shift ;;
    --serve) SERVE="true"; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR"

export PIP_NO_CACHE_DIR=1

CONDA_ENV_NAME="khiops-doc-build"
CONDA_ENV_ACTIVE="false"

trap '
  rm -fr ./khiops_samples ./khiops-python-src docs/api-docs/python-api
  git checkout -- docs/api-docs/ mkdocs.yml 2>/dev/null || true
  if [ "$CONDA_ENV_ACTIVE" = "true" ]; then
    conda deactivate 2>/dev/null
    conda env remove -y -n "$CONDA_ENV_NAME" --quiet 2>/dev/null
  fi
' EXIT

# Sync khiops-doc's own build environment (uv-managed; shared by build-version.sh)
uv sync --extra notebooks

# Optionally install Khiops core via Conda to execute tutorials
if [ "$EXECUTE_TUTORIALS" = "true" ]; then
  if ! command -v conda &>/dev/null; then
    echo "Error: conda not found (required for --execute-tutorials). Install Miniforge."
    exit 1
  fi
  : "${KHIOPS_VERSION:?--khiops-version is required with --execute-tutorials}"
  echo "--- Creating Conda env with Khiops core ${KHIOPS_VERSION}"
  conda create -y -n "$CONDA_ENV_NAME" python=3.12 --quiet
  eval "$(conda shell.bash hook 2>/dev/null)"
  conda activate "$CONDA_ENV_NAME"
  CONDA_ENV_ACTIVE="true"
  conda install -y -c conda-forge khiops-core="$KHIOPS_VERSION"
fi

# Prepare the Python API doc sources (clone/checkout khiops-python, run
# create-doc -p, copy Markdown into docs/, regenerate the nav)
BUILD_VERSION_ARGS=(--khiops-samples-version "$KHIOPS_SAMPLES_VERSION" \
  --khiops-python-tutorial-ref "$KHIOPS_PYTHON_TUTORIAL_REF")
if [ -n "$LOCAL_KHIOPS_PYTHON" ]; then
  BUILD_VERSION_ARGS+=(--khiops-python-repo "$LOCAL_KHIOPS_PYTHON")
else
  BUILD_VERSION_ARGS+=(--khiops-python-ref "$KHIOPS_PYTHON_REF")
fi

EXECUTE_KHIOPS_TUTORIALS="$EXECUTE_TUTORIALS" KHIOPS_SAMPLES_DIR="$(pwd)/khiops_samples" \
  bash .github/scripts/build-version.sh "${BUILD_VERSION_ARGS[@]}" \
  2> >(grep -v "IPKernelApp" >&2)

# Build the whole site with Zensical
echo "=== Building site with Zensical ==="
uv run zensical build --strict

echo ""
echo "=== Done — site built in ./site ==="

if [ "$SERVE" = "true" ]; then
  uv run zensical serve
fi
