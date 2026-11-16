#!/usr/bin/env bash
set -euo pipefail

# local-build.sh - Build the Khiops doc site locally with Zensical
#
# Prerequisites:
#   - uv (https://docs.astral.sh/uv/)
#   - git
#   - curl (only to resolve the Khiops Visualization version when it is given
#     neither on the command line nor in environment.env)
#   - envsubst (gettext)
#   - wget and unzip (only with --execute-tutorials)
#
# Versions not specified on the command line are read from environment.env (same
# file as for the CI). All of them are mandatory, except:
#   - the Khiops Visualization version (latest release when omitted),
#   - the khiops-python Git reference (defaults to the khiops-python version),
#   - the khiops-python-tutorial Git reference (defaults to `main`).
#
# Unlike the CI, which runs on a reviewed repository state, this script cannot
# assume that environment.env is correct: it therefore fails on missing
# mandatory versions instead of passing empty values to build-doc.sh, and
# defaults to `main` for the tutorial repository reference.
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
                                     (default: read from environment.env)
  --local-khiops-python DIR         Use a local khiops-python Git repo instead of
                                     cloning from GitHub (commits not yet pushed
                                     can be used; uncommitted changes are not
                                     included)
  --khiops-python-ref REF           khiops-python Git ref (tag, branch or commit)
                                     to build docs from, in the GitHub repo or
                                     in the local one (--local-khiops-python)
                                     (default: read from environment.env,
                                      otherwise, equal to the khiops-python
                                      version)
  --khiops-python-version VER       Khiops Python version (for the website)
                                     (default: read from environment.env)
  --khiops-samples-version VER      khiops-samples release to download
                                     (default: read from environment.env)
  --khiops-python-tutorial-ref REF  khiops-python-tutorial Git ref
                                     (default: read from environment.env,
                                      otherwise equal to `main`)
  --khiops-viz-version VER          Khiops Visualization version
                                     (default: read from environment.env,
                                      otherwise the latest GitHub release)
  --khiops-gcs-driver-version VER   Khiops GCS driver version
                                     (default: read from environment.env)
  --khiops-s3-driver-version VER    Khiops S3 driver version
                                     (default: read from environment.env)
  --khiops-azure-driver-version VER Khiops Azure driver version
                                     (default: read from environment.env)
  --execute-tutorials               Execute khiops-doc's own tutorial notebooks
  --serve                           Serve the built site (./site) on
                                     http://127.0.0.1:8000 after building
                                     (no live reload; rebuild to see changes)

Except for the Khiops Visualization version, the khiops-python Git reference and
the khiops-python-tutorial Git reference, a version that is neither passed on the
command line nor defined in environment.env makes the script fail.
EOF
  exit 0
}

KHIOPS_SAMPLES_VERSION=""
KHIOPS_PYTHON_TUTORIAL_REF=""
KHIOPS_VERSION=""
KHIOPS_PYTHON_VERSION=""
LOCAL_KHIOPS_PYTHON=""
KHIOPS_PYTHON_REF=""
KHIOPS_VIZ_VERSION=""
KHIOPS_GCS_DRIVER_VERSION=""
KHIOPS_S3_DRIVER_VERSION=""
KHIOPS_AZURE_DRIVER_VERSION=""
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

ENV_FILE="$SCRIPT_DIR/environment.env"

# Print the value of KEY from environment.env (empty if absent). Lines are
# filtered like in the CI (comments and blank lines dropped) and the file is
# parsed, not sourced, so nothing in it is executed.
env_file_value() {
  local line=""
  if [ -f "$ENV_FILE" ]; then
    line=$(tr -d '\r' < "$ENV_FILE" | grep -vE '^(#|$)' | grep -E "^$1=" | tail -n 1) || true
  fi
  printf '%s' "${line#*=}"
}

# CLI value (if any) wins; otherwise take the value from environment.env
: "${KHIOPS_VERSION:=$(env_file_value KHIOPS_VERSION)}"
: "${KHIOPS_PYTHON_VERSION:=$(env_file_value KHIOPS_PYTHON_VERSION)}"
: "${KHIOPS_PYTHON_REF:=$(env_file_value KHIOPS_PYTHON_REF)}"
: "${KHIOPS_SAMPLES_VERSION:=$(env_file_value KHIOPS_SAMPLES_VERSION)}"
: "${KHIOPS_PYTHON_TUTORIAL_REF:=$(env_file_value KHIOPS_PYTHON_TUTORIAL_VERSION)}"
: "${KHIOPS_PYTHON_TUTORIAL_REF:=main}"
: "${KHIOPS_VIZ_VERSION:=$(env_file_value KHIOPS_VIZ_VERSION)}"
: "${KHIOPS_GCS_DRIVER_VERSION:=$(env_file_value KHIOPS_GCS_DRIVER_VERSION)}"
: "${KHIOPS_S3_DRIVER_VERSION:=$(env_file_value KHIOPS_S3_DRIVER_VERSION)}"
: "${KHIOPS_AZURE_DRIVER_VERSION:=$(env_file_value KHIOPS_AZURE_DRIVER_VERSION)}"

# Fail unless the value comes from the CLI or from environment.env
require_value() {
  local value="$1" cli_option="$2" env_name="$3"
  if [ -z "$value" ]; then
    echo "Error: ${env_name} is specified neither via ${cli_option} nor in ${ENV_FILE}." >&2
    exit 1
  fi
}
require_value "$KHIOPS_VERSION" --khiops-version KHIOPS_VERSION
require_value "$KHIOPS_PYTHON_VERSION" --khiops-python-version KHIOPS_PYTHON_VERSION
require_value "$KHIOPS_SAMPLES_VERSION" --khiops-samples-version KHIOPS_SAMPLES_VERSION
require_value "$KHIOPS_GCS_DRIVER_VERSION" --khiops-gcs-driver-version KHIOPS_GCS_DRIVER_VERSION
require_value "$KHIOPS_S3_DRIVER_VERSION" --khiops-s3-driver-version KHIOPS_S3_DRIVER_VERSION
require_value "$KHIOPS_AZURE_DRIVER_VERSION" --khiops-azure-driver-version KHIOPS_AZURE_DRIVER_VERSION

KHIOPS_PYTHON_REF=${KHIOPS_PYTHON_REF:-$KHIOPS_PYTHON_VERSION}

# Synchronize Python and Uv versions with the CI (.github/workflows/ci.yml)
CI_PYTHON_VERSION="3.14"
CI_UV_VERSION="0.13.5"

if ! command -v uv &>/dev/null; then
  echo "Error: uv not found. Install it or make sure its directory is on PATH."
  echo "On Windows, use Git Bash explicitly; a bare 'bash' command may launch WSL instead."
  echo "WSL requires its own Linux installation of uv and the build dependencies."
  exit 1
fi
for tool in git envsubst; do
  command -v "$tool" &>/dev/null || { echo "Error: $tool not found." >&2; exit 1; }
done
if [ "$EXECUTE_TUTORIALS" = "true" ]; then
  for tool in wget unzip; do
    command -v "$tool" &>/dev/null || { echo "Error: $tool not found." >&2; exit 1; }
  done
fi
UV_INSTALLED_VERSION=$(uv --version | cut -d' ' -f2)
if [ "$UV_INSTALLED_VERSION" != "$CI_UV_VERSION" ]; then
  echo "--- Warning: uv ${UV_INSTALLED_VERSION} is installed, the CI uses ${CI_UV_VERSION}"
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

if [ -z "$KHIOPS_VIZ_VERSION" ]; then
  KHIOPS_VIZ_VERSION=$(latest_release_tag KhiopsML/khiops-visualization-desktop)
  KHIOPS_VIZ_VERSION="${KHIOPS_VIZ_VERSION#v}"
  echo "--- Latest Khiops Visualization Desktop release: ${KHIOPS_VIZ_VERSION}"
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

# Create the build virtual environment (Khiops core is installed into it by
# build-doc.sh; it is always needed, as building the Python API docs always
# executes khiops-python's own tutorial notebooks)
echo "--- Creating Python virtualenv (Khiops core ${KHIOPS_VERSION} will be installed by build-doc.sh)"
uv venv --clear --python "$CI_PYTHON_VERSION" "$BUILD_VENV"
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
