#!/usr/bin/env python3
"""
generate_python_api_nav.py  (standard-library only, no third-party dependencies)

This script:

  1. Parses the source file's "project.nav" as-is.
  2. Optionally normalizes the source nav's first entry from a titled
     mapping (e.g. { "Home" = "index.md" }) to a nav entry with a custom title
     (e.g. {"Python API = "index.md"}), via --source-index-title,
     --source-index-file and --target-index-title.
  3. Optionally prepends a path prefix to every relative file path in the
     source nav, via --path-prefix, so paths remain valid once merged into
     a document with a different docs root.
  4. Parses the target file into a plain Python structure.
  5. Locates the top-level nav entry whose single key equals --section
     and replaces its value with the source's
     (possibly normalized/prefixed) nav.
  6. Serializes the whole structure back to TOML text and writes it out.

Requires Python 3.11+ (for the built-in `tomllib` parser). No third-party
packages are used. The target file's original formatting/comments are not
preserved.

Usage:
    python generate_python_api_nav.py \
        --source zensical_python.toml \
        --target zensical.toml \
        --output zensical.toml \
        --section "API Python" \
        --source-index-title "Home" \
        --source-index-file "index.md" \
        --target-index-title "Python API" \
        --path-prefix "api-docs/python-api/
"""

import argparse
import sys

try:
    import tomllib
except ModuleNotFoundError:
    print(
        "Error: this script requires Python 3.11+ for the built-in "
        "'tomllib' module (standard library TOML parser).",
        file=sys.stderr,
    )
    sys.exit(1)


# ----------------------------------------------------------------------
# Extract the source nav (no conversion needed: same syntax as target)
# ----------------------------------------------------------------------


def load_source_nav(source_path):
    """Parse the source TOML file and return its 'project.nav' list as-is"""
    with open(source_path, "rb") as f:
        source_doc = tomllib.load(f)

    project = source_doc.get("project")
    if project is None:
        raise KeyError(f"No top-level 'project' table found in {source_path}")

    raw_nav = project.get("nav")
    if raw_nav is None:
        raise KeyError(f"No 'nav' key found under 'project' in {source_path}")

    return raw_nav


# ----------------------------------------------------------------------
# Normalise the index entry ({ "Key" = "index.md" } -> "index.md"
# ----------------------------------------------------------------------


def normalise_index_entry(nav, source_title, source_file, target_title):
    """
    If the first item of nav is the single-key mapping
    { source_title = source_file } (e.g. { "Home" = "index.md" }), replace the
    single-key mapping in place with an entry in the nav which has target_title
    as its title.

    This turns a titled index-page entry into an MkDocs-style differently-titled
    index entry, so the section's nav entry has the custom title.
    """
    if not nav:
        return

    first = nav[0]
    if isinstance(first, dict) and len(first) == 1:
        ((title, file_),) = first.items()
        if title == source_title and file_ == source_file:
            nav[0] = {target_title: [file_]}


# -------------------------------------------------------------------------
# Prepend path prefix to every file path ("index.md" -> "path/to/index.md))
# -------------------------------------------------------------------------


def prefix_nav_files(nav, prefix):
    """
    Recursively prepend `prefix` to every relative file path found in a
    MkDocs-style nav list (bare strings, and string values of single-key
    mappings), leaving external links (absolute URLs, i.e. containing
    "://") untouched.

    This is required when nav entries are copied from a project whose file
    paths are relative to its own docs root (e.g. zensical_python.toml)
    into a nav section of a project with a different docs root (e.g.
    zensical.toml): without this adjustment, Zensical cannot locate the
    referenced Markdown files and falls back to treating the raw nav value
    as a literal external link, which is why the built URLs would
    otherwise retain a dangling ".md" extension.
    """

    def prefix_value(value):
        if "://" in value:
            return value
        return prefix + value

    result = []
    for item in nav:
        if isinstance(item, str):
            result.append(prefix_value(item))
        elif isinstance(item, dict) and len(item) == 1:
            ((title, value),) = item.items()
            if isinstance(value, str):
                result.append({title: prefix_value(value)})
            elif isinstance(value, list):
                result.append({title: prefix_nav_files(value, prefix)})
            else:
                raise ValueError(
                    f"Unsupported nav value type for {title!r}: {type(value)!r}"
                )
        else:
            raise ValueError(f"Unsupported nav item: {item!r}")
    return result


# ----------------------------------------------------------------------
# Locate & replace the matching entry in the target nav (MkDocs-style)
# ----------------------------------------------------------------------


def replace_section_nav(target_nav, section_title, new_nav):
    """
    Replace, in place, the value of the single-key mapping entry
    { section_title = ... } found in target_nav (a MkDocs-style nav list).
    """
    for i, entry in enumerate(target_nav):
        if isinstance(entry, dict) and len(entry) == 1:
            ((key, _value),) = entry.items()
            if key == section_title:
                target_nav[i] = {section_title: new_nav}
                return

    raise KeyError(f"No nav entry with key == {section_title!r} found")


# ----------------------------------------------------------------------
# Minimal generic TOML serialiser (standard-library only)
# ----------------------------------------------------------------------


def toml_str(s):
    """Render a Python string as a double-quoted TOML string literal"""
    escaped = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_value(value, indent=""):
    """Render a Python value in the TOML format according to its type"""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return toml_str(value)
    if isinstance(value, list):
        return render_array(value, indent)
    if isinstance(value, dict):
        return render_inline_table(value, indent)
    raise TypeError(f"Unsupported value type: {type(value)!r} ({value!r})")


def render_array(items, indent, unit="  "):
    """Render Python list as a TOML array"""
    if not items:
        return "[]"
    child_indent = indent + unit
    lines = ["["]
    for item in items:
        lines.append(f"{child_indent}{render_value(item, child_indent)},")
    lines.append(f"{indent}]")
    return "\n".join(lines)


def render_inline_table(d, indent):
    """Render Python dictionary as a sequence of TOML key-value pairs"""
    parts = [f"{toml_str(k)} = {render_value(v, indent)}" for k, v in d.items()]
    return "{ " + ", ".join(parts) + " }"


def dumps(doc):
    """Serialise a top-level dict (parsed TOML document) back to TOML text"""
    lines = [f"{toml_str(key)} = {render_value(value)}" for key, value in doc.items()]
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------


def main():
    """Main driver"""
    parser = argparse.ArgumentParser(
        description=(
            "Copy the MkDocs-style 'project.nav' section of a TOML file "
            "into a matching top-level nav entry of a Zensical TOML file "
            "that also uses MkDocs-style nav syntax. Uses only the Python "
            "standard library; the target file's original formatting/"
            "comments are not preserved."
        )
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path to the TOML file to read 'project.nav' from.",
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Path to the Zensical TOML file to update.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path to write the resulting TOML file to (defaults to --target).",
    )
    parser.add_argument(
        "--section",
        required=True,
        help="Key of the top-level nav entry whose value is replaced.",
    )
    index_group = parser.add_argument_group(
        "index page normalisation",
        "Optional: if used, all three options below must be provided together."
    )
    index_group.add_argument(
        "--source-index-title",
        default=None,
        help="Title of the source nav's first entry to treat as its index page.",
    )
    index_group.add_argument(
        "--source-index-file",
        default=None,
        help="File path of the source nav's first entry to treat as its index page.",
    )
    index_group.add_argument(
        "--target-index-title",
        default=None,
        help="Target of the index file, to be displayed and linked to in the nav sections."
    )
    parser.add_argument(
        "--path-prefix",
        default=None,
        help=(
            "Prefix to prepend to every relative file path in the source "
            "nav (e.g. 'api-docs/python-api/'), so paths remain valid "
            "relative to the target file's docs root."
        ),
    )

    args = parser.parse_args()

    index_args = (
        args.source_index_title,
        args.source_index_file,
        args.target_index_title
    )
    if any(index_args) and not all(index_args):
        parser.error(
            "--source-index-title, --source-index-file and --target-index-title "
            "must all be provided together, or not at all."
        )

    output_path = args.output or args.target

    try:
        new_nav = load_source_nav(args.source)

        if all(index_args):
            normalise_index_entry(
                new_nav,
                args.source_index_title,
                args.source_index_file,
                args.target_index_title
            )

        if args.path_prefix:
            new_nav = prefix_nav_files(new_nav, args.path_prefix)

        with open(args.target, "rb") as f:
            target_doc = tomllib.load(f)

        target_nav = target_doc.get("nav")
        if target_nav is None:
            raise KeyError("No top-level 'nav' key found in the target document")

        replace_section_nav(target_nav, args.section, new_nav)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(dumps(target_doc))

    except (KeyError, ValueError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Successfully injected nav section '{args.section}' into {output_path}")


if __name__ == "__main__":
    main()
