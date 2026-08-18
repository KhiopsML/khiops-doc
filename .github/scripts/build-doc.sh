#!/usr/bin/env bash
set -euo pipefail

# build-doc.sh — Full Khiops doc build pipeline, shared by CI
# (.github/actions/build-doc) and local-build.sh.
#
# Usage:
#   build-doc.sh [OPTIONS]
#
# Options:
#   --khiops-version VER              Khiops core version (for site content)
#   --khiops-python-repo URL_OR_DIR   khiops-python repo to build docs from
#   --khiops-python-ref REF           khiops-python Git ref to build docs from
#   --khiops-python-version VER       khiops Python version (for site content)
#   --khiops-samples-version VER      khiops-samples release
#   --khiops-python-tutorial-ref REF  khiops-python-tutorial Git ref
#   --khiops-viz-version VER          Khiops Visualization version
#   --khiops-gcs-driver-version VER   Khiops GCS driver version
#   --khiops-s3-driver-version VER    Khiops S3 driver version
#   --khiops-azure-driver-version VER Khiops Azure driver version
#   --execute-tutorials               Execute khiops-doc's own tutorial
#                                      notebooks (docs/tutorials/sourced-notebooks)

KHIOPS_VERSION=""
KHIOPS_PYTHON_REPO="https://github.com/KhiopsML/khiops-python.git"
KHIOPS_PYTHON_REF="main"
KHIOPS_PYTHON_VERSION=""
KHIOPS_SAMPLES_VERSION="main"
KHIOPS_PYTHON_TUTORIAL_REF="main"
KHIOPS_VIZ_VERSION=""
KHIOPS_GCS_DRIVER_VERSION=""
KHIOPS_S3_DRIVER_VERSION=""
KHIOPS_AZURE_DRIVER_VERSION=""
EXECUTE_TUTORIALS="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --khiops-version) KHIOPS_VERSION="$2"; shift 2 ;;
    --khiops-python-repo) KHIOPS_PYTHON_REPO="$2"; shift 2 ;;
    --khiops-python-ref) KHIOPS_PYTHON_REF="$2"; shift 2 ;;
    --khiops-python-version) KHIOPS_PYTHON_VERSION="$2"; shift 2 ;;
    --khiops-samples-version) KHIOPS_SAMPLES_VERSION="$2"; shift 2 ;;
    --khiops-python-tutorial-ref) KHIOPS_PYTHON_TUTORIAL_REF="$2"; shift 2 ;;
    --khiops-viz-version) KHIOPS_VIZ_VERSION="$2"; shift 2 ;;
    --khiops-gcs-driver-version) KHIOPS_GCS_DRIVER_VERSION="$2"; shift 2 ;;
    --khiops-s3-driver-version) KHIOPS_S3_DRIVER_VERSION="$2"; shift 2 ;;
    --khiops-azure-driver-version) KHIOPS_AZURE_DRIVER_VERSION="$2"; shift 2 ;;
    --execute-tutorials) EXECUTE_TUTORIALS="true"; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
export PIP_NO_CACHE_DIR=1

cleanup() {
  echo "--- Cleaning up build workspace"
  rm -rf ./khiops_samples docs/api-docs/python-api docs/tutorials/notebooks
  git checkout -- zensical.toml 2>/dev/null || true
  git checkout -- docs/api-docs/python-api.md 2>/dev/null || true
}
trap cleanup EXIT

# 1. Install khiops-core
uv pip install khiops-core=="$KHIOPS_VERSION"

# 2. Install khiops-doc's own Python dependencies
echo "=== Installing documentation requirements ==="
if [ "$EXECUTE_TUTORIALS" = "true" ]; then
  uv sync --frozen --extra notebooks --extra tutorials --extra pythonapi
else
  uv sync --frozen --extra notebooks --extra pythonapi
fi

# 3. Download khiops-samples for khiops-doc's own tutorial notebooks
#    (only needed if they are actually executed)
if [ "$EXECUTE_TUTORIALS" = "true" ]; then
  echo "=== Downloading khiops-samples ${KHIOPS_SAMPLES_VERSION} ==="
  rm -rf ./khiops_samples
  wget -q -O khiops_samples.zip \
    "https://github.com/KhiopsML/khiops-samples/releases/download/${KHIOPS_SAMPLES_VERSION}/khiops-samples-${KHIOPS_SAMPLES_VERSION}.zip"
  mkdir -p ./khiops_samples && unzip -q khiops_samples.zip -d ./khiops_samples
  rm -f khiops_samples.zip
fi
export KHIOPS_SAMPLES_DIR="$(pwd)/khiops_samples"
export EXECUTE_KHIOPS_TUTORIALS="$EXECUTE_TUTORIALS"

# 4. Convert khiops-doc's own tutorial notebooks
echo "=== Converting khiops-doc tutorial notebooks ==="
uv run python scripts/convert_notebooks.py

# 5. Prepare Python API doc sources from khiops-python (always executes
#    khiops-python's own tutorials via create-doc -t -d — requires a real
#    Khiops core + khiops-python install, independent of --execute-tutorials)
echo "=== Preparing Python API doc sources ==="
bash "${SCRIPT_DIR}/prepare-python-api-doc.sh" \
  --khiops-python-repo "$KHIOPS_PYTHON_REPO" \
  --khiops-python-ref "$KHIOPS_PYTHON_REF" \
  --khiops-samples-version "$KHIOPS_SAMPLES_VERSION" \
  --khiops-python-tutorial-ref "$KHIOPS_PYTHON_TUTORIAL_REF"

# 6. Substitute environment variables into the Zensical configuration file
echo "=== Injecting the environment variables into zensical.toml"
echo "  KHIOPS_VERSION = ${KHIOPS_VERSION}"
echo "  KHIOPS_PYTHON_VERSION = ${KHIOPS_PYTHON_VERSION}"
echo "  KHIOPS_SAMPLES_VERSION = ${KHIOPS_SAMPLES_VERSION}"
echo "  KHIOPS_VIZ_VERSION = ${KHIOPS_VIZ_VERSION}"
echo "  KHIOPS_GCS_DRIVER_VERSION = ${KHIOPS_GCS_DRIVER_VERSION}"
echo "  KHIOPS_S3_DRIVER_VERSION = ${KHIOPS_S3_DRIVER_VERSION}"
echo "  KHIOPS_AZURE_DRIVER_VERSION = ${KHIOPS_AZURE_DRIVER_VERSION}"
KHIOPS_VERSIONING_VARS=$(printf '${%s} ' \
  KHIOPS_VERSION \
  KHIOPS_PYTHON_VERSION \
  KHIOPS_SAMPLES_VERSION \
  KHIOPS_VIZ_VERSION \
  KHIOPS_GCS_DRIVER_VERSION \
  KHIOPS_S3_DRIVER_VERSION \
  KHIOPS_AZURE_DRIVER_VERSION)
export KHIOPS_VERSION KHIOPS_PYTHON_VERSION KHIOPS_VIZ_VERSION \
  KHIOPS_SAMPLES_VERSION KHIOPS_GCS_DRIVER_VERSION \
  KHIOPS_S3_DRIVER_VERSION KHIOPS_AZURE_DRIVER_VERSION
envsubst "${KHIOPS_VERSIONING_VARS}" \
  < zensical.toml \
  > zensical.tmp.toml \
  && mv zensical.tmp.toml zensical.toml

# 7. Build the whole site with Zensical
echo "=== Building site with Zensical in dir $(pwd) ==="
uv run zensical build --clean --strict

echo "=== Done — site built in ./site ==="
