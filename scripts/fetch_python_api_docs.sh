#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${ROOT_DIR}/docs/api-docs/python-api/api"

# Priority: explicit argument > environment variable > default docs version.
KHIOPS_PYTHON_VERSION="${1:-${KHIOPS_PYTHON_VERSION:-11.0.1.0}}"
ARCHIVE_NAME="khiops-api-docs-${KHIOPS_PYTHON_VERSION}.zip"
DOWNLOAD_URL="https://github.com/KhiopsML/khiops-python/releases/download/${KHIOPS_PYTHON_VERSION}/${ARCHIVE_NAME}"
TMP_DIR="$(mktemp -d)"
ARCHIVE_PATH="${TMP_DIR}/${ARCHIVE_NAME}"

cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

echo "Fetching Khiops Python API docs ${KHIOPS_PYTHON_VERSION}"
echo "Source: ${DOWNLOAD_URL}"

curl -fL "${DOWNLOAD_URL}" -o "${ARCHIVE_PATH}"

rm -rf "${TARGET_DIR}"
mkdir -p "${TARGET_DIR}"

if command -v bsdtar >/dev/null 2>&1; then
  bsdtar --strip-components=3 -C "${TARGET_DIR}" -xvf "${ARCHIVE_PATH}" >/dev/null
else
  unzip -q "${ARCHIVE_PATH}" -d "${TMP_DIR}/unzipped"
  cp -R "${TMP_DIR}/unzipped"/*/doc/_build/html/* "${TARGET_DIR}/"
fi

# Keep API docs visually consistent with the site shell.
find "${TARGET_DIR}" -name "*.html" -print0 \
  | xargs -0 sed -i '' 's/div class="sidebar-logo-container"/div class="sidebar-logo-container" style="visibility: hidden; max-height: 0"/g'

echo "API docs extracted to ${TARGET_DIR}"
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${ROOT_DIR}/docs/api-docs/python-api/api"

# Priority: explicit argument > environment variable > docs default value.
KHIOPS_PYTHON_VERSION="${1:-${KHIOPS_PYTHON_VERSION:-11.0.1.0}}"
ARCHIVE_NAME="khiops-api-docs-${KHIOPS_PYTHON_VERSION}.zip"
DOWNLOAD_URL="https://github.com/KhiopsML/khiops-python/releases/download/${KHIOPS_PYTHON_VERSION}/${ARCHIVE_NAME}"
TMP_DIR="$(mktemp -d)"
ARCHIVE_PATH="${TMP_DIR}/${ARCHIVE_NAME}"

cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

echo "Fetching Khiops Python API docs ${KHIOPS_PYTHON_VERSION}"
echo "Source: ${DOWNLOAD_URL}"

curl -fL "${DOWNLOAD_URL}" -o "${ARCHIVE_PATH}"

rm -rf "${TARGET_DIR}"
mkdir -p "${TARGET_DIR}"

if command -v bsdtar >/dev/null 2>&1; then
  bsdtar --strip-components=3 -C "${TARGET_DIR}" -xvf "${ARCHIVE_PATH}" >/dev/null
else
  # Fallback for environments without bsdtar
  unzip -q "${ARCHIVE_PATH}" -d "${TMP_DIR}/unzipped"
  cp -R "${TMP_DIR}/unzipped"/*/doc/_build/html/* "${TARGET_DIR}/"
fi

find "${TARGET_DIR}" -name "*.html" -print0 \
  | xargs -0 sed -i '' 's/div class="sidebar-logo-container"/div class="sidebar-logo-container" style="visibility: hidden; max-height: 0"/g'

echo "API docs extracted to ${TARGET_DIR}"
