"""Generate reviewable Q&A documentation from GitHub Discussions."""

import argparse
import json
import os
import sys
from pathlib import Path

from python.discussions.discussion_content import InvalidDiscussion, extract
from python.discussions.discussion_render import download_attachment, heading_text, render_pages, topic_slug
from python.discussions.discussion_source import GitHubError, fetch_discussions


BEGIN = "  # BEGIN GENERATED DISCUSSION NAVIGATION"
END = "  # END GENERATED DISCUSSION NAVIGATION"
OVERSIZED = Path(".github/discussion-sync/oversized.json")
GENERATED_DIRECTORIES = (
    Path("docs/q-and-a"),
    Path("docs/assets/images/q-and-a"),
    Path("docs/assets/discussion-scripts/q-and-a"),
)


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def navigation(text, discussions):
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ValueError("Generated discussion navigation markers must each occur exactly once")
    start = text.index(BEGIN) + len(BEGIN)
    end = text.index(END)
    if start >= end:
        raise ValueError("Generated discussion navigation markers are out of order")
    topics = {}
    for item in discussions:
        topic, title = item.topic, item.topic_title
        if topic in topics and topics[topic] != title:
            raise ValueError(f"Inconsistent label descriptions for {topic}")
        topics[topic] = title
    lines = ['  { "Q&A" = [', '      { "Overview" = "q-and-a/overview.md" },']
    for topic, title in sorted(topics.items()):
        lines.append(f"      {{ {json.dumps(title, ensure_ascii=False)} = "
                     f'{json.dumps("q-and-a/" + topic_slug(topic) + ".md")} }},')
    lines.append("    ] },")
    return text[:start] + "\n" + "\n".join(lines) + "\n" + text[end:]


def report_text(file_changes, unlabelled, invalid):
    lines = ["# Discussion synchronization", "", "## Generated file changes", ""]
    for action in ("added", "updated", "removed"):
        lines.extend([f"### {action.title()}", ""])
        lines.extend(
            [f"- `{name}`" for name in file_changes[action]]
            or ["None."]
        )
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


def checked_path(root, name):
    path = Path(name)
    path = root / path
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Unsafe generated output path: {name}")
    relative = path.relative_to(root)
    if any(root.joinpath(*relative.parts[:i]).is_symlink() for i in range(1, len(relative.parts) + 1)):
        raise ValueError(f"Symlink in generated output path: {name}")
    return path


def checked_output(root, name):
    path = Path(name)
    if not any(path.is_relative_to(directory) for directory in GENERATED_DIRECTORIES):
        raise ValueError(f"Unexpected generated output path: {name}")
    return checked_path(root, name)


def existing_generated_files(root):
    files = set()
    for directory in GENERATED_DIRECTORIES:
        base = root / directory
        if base.is_symlink():
            raise ValueError(f"Symlink in generated output path: {directory}")
        if not base.exists():
            continue
        if not base.is_dir():
            raise ValueError(f"Generated output path is not a directory: {directory}")
        for current, directories, filenames in os.walk(base, followlinks=False):
            current_path = Path(current)
            for name in directories:
                if (current_path / name).is_symlink():
                    raise ValueError(f"Symlink in generated output path: {current_path / name}")
            for name in filenames:
                path = current_path / name
                relative = path.relative_to(root).as_posix()
                checked_output(root, relative)
                files.add(relative)
    return files


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
        path = checked_output(root, name) if name.startswith("docs/") else checked_path(root, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_bytes() != content:
            path.write_bytes(content)
    for name in sorted(old_files - generated.keys()):
        path = checked_output(root, name)
        if path.exists():
            path.unlink()


def synchronize(root, discussions, downloader=download_attachment):
    root = Path(root)
    published, unlabelled, invalid = extract_discussions(discussions)
    pages, assets, attachment_errors = render_pages(published, downloader)
    invalid.extend(attachment_errors)
    invalid.sort(key=lambda d: d["number"])
    generated = {f"docs/{name}": value.encode() for name, value in pages.items()}
    generated.update({f"docs/{name}": value for name, value in assets.items()})
    old_files = existing_generated_files(root)
    nav_path = root / "zensical.toml"
    new_nav = navigation(nav_path.read_text(encoding="utf-8"), published)
    generated["zensical.toml"] = new_nav.encode()
    oversized = [item for item in attachment_errors if "exceeds 100,000 bytes" in item["reason"]]
    generated[OVERSIZED.as_posix()] = json_text(oversized).encode()

    file_changes = {"added": [], "updated": [], "removed": []}
    for name, content in generated.items():
        path = checked_output(root, name) if name.startswith("docs/") else checked_path(root, name)
        if not path.exists():
            file_changes["added"].append(name)
        elif path.read_bytes() != content:
            file_changes["updated"].append(name)
    file_changes["removed"] = sorted(old_files - generated.keys())
    for action in file_changes:
        file_changes[action].sort()
    report = report_text(file_changes, unlabelled, invalid)

    write_generated_files(root, generated, old_files)
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
