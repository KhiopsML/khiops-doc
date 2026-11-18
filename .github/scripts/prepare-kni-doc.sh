#!/usr/bin/env bash
set -euo pipefail

# Copy the KNI tutorial as static resources; do not generate documentation.
KNI_TUTORIAL_REPO="https://github.com/KhiopsML/KNI-tutorial.git"
KNI_TUTORIAL_REF=""
LOCAL_KNI_TUTORIAL=""
OUTPUT_DIR=""
WORK_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --kni-tutorial-repo) KNI_TUTORIAL_REPO="$2"; shift 2 ;;
    --kni-tutorial-ref) KNI_TUTORIAL_REF="$2"; shift 2 ;;
    --local-kni-tutorial) LOCAL_KNI_TUTORIAL="$2"; shift 2 ;;
    --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
    --work-dir) WORK_DIR="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

: "${OUTPUT_DIR:?--output-dir is required}"
if [[ -e "$OUTPUT_DIR" ]]; then
  echo "Error: refusing to overwrite KNI tutorial output: $OUTPUT_DIR" >&2
  exit 1
fi

if [[ -n "$LOCAL_KNI_TUTORIAL" ]]; then
  SOURCE_DIR=$(cd -- "$LOCAL_KNI_TUTORIAL" && pwd)
else
  : "${WORK_DIR:?--work-dir is required for a KNI checkout}"
  : "${KNI_TUTORIAL_REF:?--kni-tutorial-ref is required for a KNI checkout}"
  SOURCE_DIR="$WORK_DIR/KNI-tutorial"
  mkdir -p -- "$WORK_DIR"
  git clone --depth 1 --branch "$KNI_TUTORIAL_REF" -- \
    "$KNI_TUTORIAL_REPO" "$SOURCE_DIR"
  trap 'rm -rf -- "$SOURCE_DIR"' EXIT
fi


mkdir -p -- "$OUTPUT_DIR"
OUTPUT_DIR=$(cd -- "$OUTPUT_DIR" && pwd)
(
  cd -- "$SOURCE_DIR"
  # Copy regular files, excluding hidden files and directories.
  find . -mindepth 1 -name '.*' -prune -o -type f -print |
    while IFS= read -r file; do
      mkdir -p -- "$OUTPUT_DIR/$(dirname -- "$file")"
      cp -- "$file" "$OUTPUT_DIR/$file"
    done
)
