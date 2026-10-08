#!/usr/bin/env bash
set -euo pipefail

# prepare-kni-tutorial.sh - Clone the KNI tutorial repository for the LLM
# Markdown export.

KNI_TUTORIAL_REPO="https://github.com/KhiopsML/KNI-tutorial.git"
KHIOPS_VERSION=""
KNI_TUTORIAL_REF=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --khiops-version) KHIOPS_VERSION="$2"; shift 2 ;;
    --kni-tutorial-repo) KNI_TUTORIAL_REPO="$2"; shift 2 ;;
    --kni-tutorial-ref) KNI_TUTORIAL_REF="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

KNI_TUTORIAL_REF=${KNI_TUTORIAL_REF:-$KHIOPS_VERSION}
: "${KNI_TUTORIAL_REF:?--khiops-version or --kni-tutorial-ref is required}"

echo "=== Preparing KNI tutorial from ${KNI_TUTORIAL_REPO} @ ${KNI_TUTORIAL_REF} ==="
rm -rf ./kni-tutorial-src
git clone "$KNI_TUTORIAL_REPO" ./kni-tutorial-src
git -C ./kni-tutorial-src checkout "$KNI_TUTORIAL_REF"