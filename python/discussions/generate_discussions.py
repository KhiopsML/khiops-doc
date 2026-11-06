"""Generate reviewable Q&A documentation from GitHub Discussions."""

import argparse
import json
import sys
from pathlib import Path

from python.discussions.discussion_content import InvalidDiscussion, extract
from python.discussions.discussion_render import download_attachment, heading_text, render_pages, topic_slug
from python.discussions.discussion_source import GitHubError, fetch_discussions


BEGIN = "  # BEGIN GENERATED DISCUSSION NAVIGATION"
END = "  # END GENERATED DISCUSSION NAVIGATION"
MANIFEST = Path(".github/discussion-sync/manifest.json")
OVERSIZED = Path(".github/discussion-sync/oversized.json")
OWNED_PREFIXES = (
    "docs/q-and-a/",
    "docs/assets/images/q-and-a/",
    "docs/assets/discussion-scripts/q-and-a/",
)


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def read_json(path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def navigation(text, discussions):
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ValueError("Generated discussion navigation markers must each occur exactly once")
    start = text.index(BEGIN) + len(BEGIN)
    end = text.index(END)
    if start >= end:
        raise ValueError("Generated discussion navigation markers are out of order")
    topics = {}
    for item in discussions.values():
        topic, title = item["topic"], item["topic_title"]
        if topic in topics and topics[topic] != title:
            raise ValueError(f"Inconsistent label descriptions for {topic}")
        topics[topic] = title
    lines = ['  { "Q&A" = [', '      { "Overview" = "q-and-a/overview.md" },']
    for topic, title in sorted(topics.items()):
        lines.append(f"      {{ {json.dumps(title, ensure_ascii=False)} = "
                     f'{json.dumps("q-and-a/" + topic_slug(topic) + ".md")} }},')
    lines.append("    ] },")
    return text[:start] + "\n" + "\n".join(lines) + "\n" + text[end:]


def changes(previous, current):
    result = {"added": [], "changed": [], "removed": []}
    for identifier in sorted(previous.keys() | current.keys()):
        old, new = previous.get(identifier), current.get(identifier)
        if old is None:
            result["added"].append(new)
        elif new is None:
            result["removed"].append(old)
        elif old != new:
            if old["topic"] != new["topic"]:
                result["removed"].append(old)
                result["added"].append(new)
            else:
                result["changed"].append(new)
    return result


def report_text(previous, current, unlabelled, invalid):
    lines = ["# Discussion synchronization", ""]
    grouped = changes(previous, current)
    for name in ("added", "changed", "removed"):
        lines.extend([f"## {name.title()}", ""])
        items = grouped[name]
        if not items:
            lines.extend(["None.", ""])
            continue
        topics = sorted({item["topic"] for item in items})
        for topic in topics:
            lines.extend([f"### {heading_text(topic)}", ""])
            for item in sorted((i for i in items if i["topic"] == topic), key=lambda i: i["number"]):
                lines.append(f'- [#{item["number"]} {heading_text(item["title"])}]({item["url"]})')
            lines.append("")
    lines.extend(["## Discussions without a Topic label", ""])
    lines.extend(
        [f'- [#{d["number"]} {heading_text(d["title"])}]({d["url"]})' for d in unlabelled]
        or ["None."]
    )
    lines.extend(["", "## Invalid discussions", ""])
    for item in invalid:
        reason = item["reason"]
        if "file" in item and reason.endswith(item["file"]):
            reason = reason[: -len(item["file"])].rstrip(": ")
        line = f'- [#{item["number"]}]({item["url"]}): {heading_text(reason)}'
        if "file" in item:
            line += f' ([attachment](<{item["file"]}>))'
        lines.append(line)
    if not invalid:
        lines.append("None.")
    return "\n".join(lines) + "\n"


def checked_output(root, name):
    if not any(name.startswith(prefix) for prefix in OWNED_PREFIXES):
        raise ValueError(f"Unexpected generated output path: {name}")
    path = root / name
    if not path.resolve().is_relative_to(root.resolve()) or any(
        part == ".." for part in Path(name).parts
    ):
        raise ValueError(f"Unsafe generated output path: {name}")
    relative = path.relative_to(root)
    if any((root.joinpath(*relative.parts[:i])).is_symlink() for i in range(1, len(relative.parts) + 1)):
        raise ValueError(f"Symlink in generated output path: {name}")
    return path


def extract_discussions(discussions):
    published, unlabelled, invalid = [], [], []
    for discussion in sorted(discussions, key=lambda d: d["number"]):
        try:
            item = extract(discussion)
        except InvalidDiscussion as exc:
            invalid.append({"number": discussion["number"], "url": discussion["url"], "reason": str(exc)})
            continue
        if item is None:
            unlabelled.append(discussion)
        else:
            published.append(item)
    return published, unlabelled, invalid


def write_generated_files(root, generated, old_files):
    for name, content in generated.items():
        path = checked_output(root, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_bytes() != content:
            path.write_bytes(content)
    for name in sorted(old_files - generated.keys()):
        path = checked_output(root, name)
        if path.exists():
            path.unlink()


def synchronize(root, discussions, downloader=download_attachment):
    root = Path(root)
    old = read_json(root / MANIFEST, {"discussions": {}, "files": []})
    published, unlabelled, invalid = extract_discussions(discussions)
    pages, assets, attachment_errors, current = render_pages(published, downloader, include_manifest=True)
    invalid.extend(attachment_errors)
    invalid.sort(key=lambda d: d["number"])
    generated = {f"docs/{name}": value.encode() for name, value in pages.items()}
    generated.update({f"docs/{name}": value for name, value in assets.items()})
    old_files = set(old["files"])
    for name in old_files | generated.keys():
        path = checked_output(root, name)
        if name not in old_files and path.exists():
            raise ValueError(f"Refusing to overwrite an unowned file: {name}")
    nav_path = root / "zensical.toml"
    new_nav = navigation(nav_path.read_text(encoding="utf-8"), current)
    report = report_text(old["discussions"], current, unlabelled, invalid)
    oversized = [item for item in attachment_errors if "exceeds 100,000 bytes" in item["reason"]]
    manifest = {"discussions": current, "files": sorted(generated)}

    write_generated_files(root, generated, old_files)
    nav_path.write_text(new_nav, encoding="utf-8")
    for path, data in ((MANIFEST, manifest), (OVERSIZED, oversized)):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json_text(data), encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = synchronize(args.root, fetch_discussions())
        args.report.write_text(report, encoding="utf-8")
    except (GitHubError, OSError, ValueError, KeyError) as exc:
        print(f"Discussion synchronization failed: {exc}", file=sys.stderr)
        return 1
    print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
