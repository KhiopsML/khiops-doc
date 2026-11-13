#!/usr/bin/env bash
set -euo pipefail

# local-build.sh - Build the Khiops doc site locally with Zensical
#
# Prerequisites:
#   - uv (https://docs.astral.sh/uv/)
#   - git
#   - curl (for resolving omitted versions)
#
# Usage:
#   ./local-build.sh [OPTIONS]

usage() {
  cat <<EOF
Usage: ./local-build.sh [OPTIONS]

Build the Khiops doc site locally with Zensical.

Options:
  -h, --help                        Show this help message and exit
  --khiops-version VER              Khiops core version to install via Pip / Uv
                                     (default: latest GitHub release)
  --local-khiops-python DIR         Use a local khiops-python repo instead of
                                     cloning from GitHub
  --khiops-python-ref REF           khiops-python Git ref to build docs from
                                     when not using --local-khiops-python
                                     (default: khiops-python-version, or the
                                      latest release tag when omitted)
  --khiops-python-version VER       Khiops Python version (for the website)
                                     (default: latest GitHub release)
  --khiops-samples-version VER      khiops-samples release to download
                                     (default: latest GitHub release)
  --khiops-python-tutorial-ref REF  khiops-python-tutorial Git ref (default: main)
  --khiops-viz-version VER          Khiops Visualization version (default: unknown)
  --khiops-gcs-driver-version VER   Khiops GCS driver version (default: unknown)
  --khiops-s3-driver-version VER    Khiops S3 driver version (default: unknown)
  --khiops-azure-driver-version VER Khiops Azure driver version (default: unknown)
  --execute-tutorials               Execute khiops-doc's own tutorial notebooks
  --serve                           Run 'zensical serve' after building
EOF
  exit 0
}

KHIOPS_SAMPLES_VERSION=""
KHIOPS_PYTHON_TUTORIAL_REF="main"
KHIOPS_VERSION=""
KHIOPS_PYTHON_VERSION=""
LOCAL_KHIOPS_PYTHON=""
KHIOPS_PYTHON_REF=""
KHIOPS_VIZ_VERSION="unknown"
KHIOPS_GCS_DRIVER_VERSION="unknown"
KHIOPS_S3_DRIVER_VERSION="unknown"
KHIOPS_AZURE_DRIVER_VERSION="unknown"
EXECUTE_TUTORIALS="false"
SERVE="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage ;;
    --khiops-version) KHIOPS_VERSION="$2"; shift 2 ;;
    --khiops-python-version) KHIOPS_PYTHON_VERSION="$2"; shift 2 ;;
    --local-khiops-python) LOCAL_KHIOPS_PYTHON="$2"; shift 2 ;;
    --khiops-python-ref) KHIOPS_PYTHON_REF="$2"; shift 2 ;;
    --khiops-samples-version) KHIOPS_SAMPLES_VERSION="$2"; shift 2 ;;
    --khiops-python-tutorial-ref) KHIOPS_PYTHON_TUTORIAL_REF="$2"; shift 2 ;;
    --khiops-viz-version) KHIOPS_VIZ_VERSION="$2"; shift 2 ;;
    --khiops-gcs-driver-version) KHIOPS_GCS_DRIVER_VERSION="$2"; shift 2 ;;
    --khiops-s3-driver-version) KHIOPS_S3_DRIVER_VERSION="$2"; shift 2 ;;
    --khiops-azure-driver-version) KHIOPS_AZURE_DRIVER_VERSION="$2"; shift 2 ;;
    --execute-tutorials) EXECUTE_TUTORIALS="true"; shift ;;
    --serve) SERVE="true"; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
cd "$SCRIPT_DIR"

if ! command -v uv &>/dev/null; then
  echo "Error: uv not found. Install it or make sure its directory is on PATH."
  echo "On Windows, use Git Bash explicitly; a bare 'bash' command may launch WSL instead."
  echo "WSL requires its own Linux installation of uv and the build dependencies."
  exit 1
fi

latest_release_tag() {
  local repository="$1"
  local release_url
  local tag_prefix="https://github.com/${repository}/releases/tag/"

  if ! command -v curl &>/dev/null; then
    echo "Error: curl is required to resolve the latest ${repository} release. Install it or specify its version explicitly." >&2
    return 1
  fi
  if ! release_url=$(curl --fail --silent --show-error --location \
      --connect-timeout 15 --max-time 60 --output /dev/null \
      --write-out '%{url_effective}' "https://github.com/${repository}/releases/latest"); then
    echo "Error: could not resolve the latest ${repository} release. Check your connection or specify its version explicitly." >&2
    return 1
  fi
  if [[ "$release_url" != "$tag_prefix"* ]]; then
    echo "Error: GitHub did not return a release tag for ${repository}: ${release_url}" >&2
    return 1
  fi
  local tag="${release_url#"$tag_prefix"}"
  if [[ -z "$tag" || "$tag" == */* || "$tag" == *[[:space:]]* ]]; then
    echo "Error: GitHub returned an invalid release tag for ${repository}: ${tag}" >&2
    return 1
  fi
  printf '%s\n' "$tag"
}

if [ -z "$KHIOPS_VERSION" ]; then
  KHIOPS_VERSION=$(latest_release_tag KhiopsML/khiops)
  KHIOPS_VERSION="${KHIOPS_VERSION#v}"
  echo "--- Latest Khiops core release: ${KHIOPS_VERSION}"
fi
if [ -z "$KHIOPS_PYTHON_VERSION" ]; then
  KHIOPS_PYTHON_TAG=$(latest_release_tag KhiopsML/khiops-python)
  KHIOPS_PYTHON_VERSION="${KHIOPS_PYTHON_TAG#v}"
  KHIOPS_PYTHON_REF=${KHIOPS_PYTHON_REF:-$KHIOPS_PYTHON_TAG}
  echo "--- Latest Khiops Python release: ${KHIOPS_PYTHON_VERSION}"
fi
KHIOPS_PYTHON_REF=${KHIOPS_PYTHON_REF:-$KHIOPS_PYTHON_VERSION}
if [ -z "$KHIOPS_SAMPLES_VERSION" ]; then
  KHIOPS_SAMPLES_VERSION=$(latest_release_tag KhiopsML/khiops-samples)
  echo "--- Latest Khiops samples release: ${KHIOPS_SAMPLES_VERSION}"
fi

BUILD_VENV=".venv-local-build"
VENV_ACTIVATED=false
export UV_PROJECT_ENVIRONMENT="$BUILD_VENV"

cleanup() {
  if [ "$VENV_ACTIVATED" = true ]; then
    deactivate
  fi
  rm -rf "$BUILD_VENV"
}
trap cleanup EXIT

# Install Khiops core via Pip (always needed - building the Python API
# docs always executes khiops-python's own tutorial notebooks)
echo "--- Creating Python virtualenv env with Khiops core ${KHIOPS_VERSION}"
uv venv --clear "$BUILD_VENV"
if [ -f "$BUILD_VENV/Scripts/activate" ]; then
  . "$BUILD_VENV/Scripts/activate"
elif [ -f "$BUILD_VENV/bin/activate" ]; then
  . "$BUILD_VENV/bin/activate"
else
  echo "Error: could not find the virtualenv activation script."
  exit 1
fi
VENV_ACTIVATED=true

ARGS=(
  --khiops-version "$KHIOPS_VERSION"
  --khiops-python-version "$KHIOPS_PYTHON_VERSION"
  --khiops-python-ref "$KHIOPS_PYTHON_REF"
  --khiops-samples-version "$KHIOPS_SAMPLES_VERSION"
  --khiops-python-tutorial-ref "$KHIOPS_PYTHON_TUTORIAL_REF"
  --khiops-viz-version "$KHIOPS_VIZ_VERSION"
  --khiops-gcs-driver-version "$KHIOPS_GCS_DRIVER_VERSION"
  --khiops-s3-driver-version "$KHIOPS_S3_DRIVER_VERSION"
  --khiops-azure-driver-version "$KHIOPS_AZURE_DRIVER_VERSION"
)
[ -n "$LOCAL_KHIOPS_PYTHON" ] && ARGS+=(--khiops-python-repo "$LOCAL_KHIOPS_PYTHON")
[ "$EXECUTE_TUTORIALS" = "true" ] && ARGS+=(--execute-tutorials)

bash .github/scripts/build-doc.sh "${ARGS[@]}"

if [ "$SERVE" = "true" ]; then
  uv run zensical serve
fi
