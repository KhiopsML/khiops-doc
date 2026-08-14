#!/usr/bin/env bash
set -euo pipefail

# local-build.sh — Build the Khiops doc site locally with Zensical
# (no Docker, no multi-version/mike support).
#
# Prerequisites:
#   - uv (https://docs.astral.sh/uv/), conda/Miniforge
#   - git, wget, unzip
#
# Usage:
#   ./local-build.sh [OPTIONS]

usage() {
  cat <<EOF
Usage: ./local-build.sh [OPTIONS]

Build the Khiops doc site locally with Zensical.

Options:
  -h, --help                       Show this help message and exit
  --khiops-version VER             Khiops core version to install via Conda
                                    (required)
  --local-khiops-python DIR        Use a local khiops-python repo instead of
                                    cloning from GitHub
  --khiops-python-ref REF          khiops-python Git ref to build docs from
                                    when not using --local-khiops-python
                                    (default: main)
  --khiops-samples-version VER     khiops-samples release to download
                                    (default: main)
  --khiops-python-tutorial-ref REF khiops-python-tutorial Git ref (default: main)
  --khiops-viz-version VER         Khiops Visualization version (default: unknown)
  --khiops-gcs-driver-version VER  Khiops GCS driver version (default: unknown)
  --khiops-s3-driver-version VER   Khiops S3 driver version (default: unknown)
  --execute-tutorials              Execute khiops-doc's own tutorial notebooks
  --serve                          Run 'zensical serve' after building
EOF
  exit 0
}

LOCAL_KHIOPS_PYTHON=""
KHIOPS_PYTHON_REF="main"
KHIOPS_SAMPLES_VERSION="main"
KHIOPS_PYTHON_TUTORIAL_REF="main"
KHIOPS_VERSION=""
KHIOPS_VIZ_VERSION="unknown"
KHIOPS_GCS_DRIVER_VERSION="unknown"
KHIOPS_S3_DRIVER_VERSION="unknown"
EXECUTE_TUTORIALS="false"
SERVE="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage ;;
    --khiops-version) KHIOPS_VERSION="$2"; shift 2 ;;
    --local-khiops-python) LOCAL_KHIOPS_PYTHON="$2"; shift 2 ;;
    --khiops-python-ref) KHIOPS_PYTHON_REF="$2"; shift 2 ;;
    --khiops-samples-version) KHIOPS_SAMPLES_VERSION="$2"; shift 2 ;;
    --khiops-python-tutorial-ref) KHIOPS_PYTHON_TUTORIAL_REF="$2"; shift 2 ;;
    --khiops-viz-version) KHIOPS_VIZ_VERSION="$2"; shift 2 ;;
    --khiops-gcs-driver-version) KHIOPS_GCS_DRIVER_VERSION="$2"; shift 2 ;;
    --khiops-s3-driver-version) KHIOPS_S3_DRIVER_VERSION="$2"; shift 2 ;;
    --execute-tutorials) EXECUTE_TUTORIALS="true"; shift ;;
    --serve) SERVE="true"; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

: "${KHIOPS_VERSION:?--khiops-version is required}"

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR"

if ! command -v conda &>/dev/null; then
  echo "Error: conda not found. Install Miniforge."
  exit 1
fi

CONDA_ENV_NAME="khiops-doc-build"
CONDA_ENV_ACTIVE="false"

trap '
  if [ "$CONDA_ENV_ACTIVE" = "true" ]; then
    conda deactivate 2>/dev/null
    conda env remove -y -n "$CONDA_ENV_NAME" --quiet 2>/dev/null
  fi
' EXIT

# Install Khiops core via Conda (always needed — building the Python API
# docs always executes khiops-python's own tutorial notebooks)
echo "--- Creating Conda env with Khiops core ${KHIOPS_VERSION}"
conda create -y -n "$CONDA_ENV_NAME" python=3.12 --quiet
eval "$(conda shell.bash hook 2>/dev/null)"
conda activate "$CONDA_ENV_NAME"
CONDA_ENV_ACTIVE="true"
conda install -y -c conda-forge khiops-core="$KHIOPS_VERSION"

ARGS=(
  --khiops-version "$KHIOPS_VERSION"
  --khiops-python-ref "$KHIOPS_PYTHON_REF"
  --khiops-samples-version "$KHIOPS_SAMPLES_VERSION"
  --khiops-python-tutorial-ref "$KHIOPS_PYTHON_TUTORIAL_REF"
  --khiops-viz-version "$KHIOPS_VIZ_VERSION"
  --khiops-gcs-driver-version "$KHIOPS_GCS_DRIVER_VERSION"
  --khiops-s3-driver-version "$KHIOPS_S3_DRIVER_VERSION"
)
[ -n "$LOCAL_KHIOPS_PYTHON" ] && ARGS+=(--khiops-python-repo "$LOCAL_KHIOPS_PYTHON")
[ "$EXECUTE_TUTORIALS" = "true" ] && ARGS+=(--execute-tutorials)

bash .github/scripts/build-doc.sh "${ARGS[@]}"

if [ "$SERVE" = "true" ]; then
  uv run zensical serve
fi
