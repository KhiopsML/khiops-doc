#!/usr/bin/env bash
set -euo pipefail

# generate-python-api-nav.sh - Generate the "API Python" nav section
# from the actual files in docs/api-docs/python-api/
#
# Usage: generate-python-api-nav.sh <docs-dir>
# Outputs YAML to stdout.

DOCS_DIR="${1:?Usage: generate-python-api-nav.sh <docs-dir>}"
P="api-docs/python-api"

nav_entry() {
  local label="$1" path="$2"
  if [ -f "${DOCS_DIR}/${path}" ]; then
    echo "${label}: ${path}"
  fi
}

# Collect submodule pages per directory
emit_subdir() {
  local dir="$1" indent="$2"
  local idx="${DOCS_DIR}/${P}/${dir}/index.md"
  if [ ! -d "${DOCS_DIR}/${P}/${dir}" ]; then return; fi
  echo "${indent}- ${dir}:"
  if [ -f "$idx" ]; then
    echo "${indent}    - ${P}/${dir}/index.md"
  fi
  for f in "${DOCS_DIR}/${P}/${dir}"/*.md; do
    [ -f "$f" ] || continue
    local base
    base=$(basename "$f" .md)
    [ "$base" = "index" ] && continue
    echo "${indent}    - ${base}: ${P}/${dir}/${base}.md"
  done
}

# --- Main output ---
echo "  - API Python:"
echo "      - ${P}/index.md"

# API Reference
echo "      - API Reference:"
for subdir in sklearn core tools internal; do
  emit_subdir "$subdir" "          "
done

# Tutorials
if [ -d "${DOCS_DIR}/${P}/tutorials" ]; then
  echo "      - Tutorials and Code Samples:"
  if [ -f "${DOCS_DIR}/${P}/tutorials/index.md" ]; then
    echo "          - Tutorials: ${P}/tutorials/index.md"
  fi
  for f in "${DOCS_DIR}/${P}/samples"/*.md; do
    [ -f "$f" ] || continue
    base=$(basename "$f" .md)
    # Derive label from filename
    label=$(echo "$base" | sed 's/_/ /g; s/\b\(.\)/\u\1/g')
    echo "          - ${label}: ${P}/samples/${base}.md"
  done
fi

# Other Topics
has_other="false"
for f in multi_table_primer.md notes.md; do
  [ -f "${DOCS_DIR}/${P}/${f}" ] && has_other="true"
done
if [ "$has_other" = "true" ]; then
  echo "      - Other Topics:"
  [ -f "${DOCS_DIR}/${P}/multi_table_primer.md" ] && \
    echo "          - Multi-Table Learning Primer: ${P}/multi_table_primer.md"
  [ -f "${DOCS_DIR}/${P}/notes.md" ] && \
    echo "          - Notes: ${P}/notes.md"
fi
