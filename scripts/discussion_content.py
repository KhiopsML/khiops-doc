"""Validate topic assignments and extract publishable discussion content."""

import re
from dataclasses import dataclass


HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


@dataclass(frozen=True)
class PublishedDiscussion:
    id: str
    number: int
    url: str
    topic: str
    topic_title: str
    title: str
    content: str


class InvalidDiscussion(ValueError):
    """A discussion cannot be published without editorial changes."""


def summary_section(text):
    """Find a level-three summary and its section boundary, outside fences."""
    lines = text.splitlines(keepends=True)
    headings = []
    fence_char = None
    fence_length = 0
    for index, line in enumerate(lines):
        fence = FENCE.match(line)
        if fence:
            marker = fence.group(1)
            if fence_char is None:
                fence_char, fence_length = marker[0], len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_length:
                fence_char = None
            continue
        if fence_char is not None:
            continue
        heading = HEADING.match(line.rstrip("\r\n"))
        if heading:
            headings.append((index, len(heading.group(1)), heading.group(2).strip()))
    matches = [h for h in headings if h[1] == 3 and h[2] == "Question summary"]
    if not matches:
        return None
    if len(matches) != 1:
        raise InvalidDiscussion("multiple Question summary sections")
    start = matches[0][0]
    end = next((index for index, level, _ in headings if index > start and level <= 3), len(lines))
    summary = "".join(lines[start + 1:end]).strip()
    if not summary:
        raise InvalidDiscussion("empty Question summary")
    content = ("".join(lines[:start]) + "".join(lines[end:])).strip()
    return summary, content


def extract(discussion):
    """Return a publication, or None for a discussion without a topic."""
    topics = [label for label in discussion["labels"] if label["name"].startswith("Topic/")]
    if not topics:
        return None
    if len(topics) > 1:
        raise InvalidDiscussion(
            "multiple topic labels: " + ", ".join(sorted(label["name"] for label in topics))
        )
    topic = topics[0]
    if not (topic.get("description") or "").strip():
        raise InvalidDiscussion(f"topic label {topic['name']} has no description")
    comments = discussion["comments"]
    section = summary_section(comments[0]["body"]) if comments else None
    if section is None:
        title, content = discussion["title"], discussion["body"]
    else:
        title, content = section
    return PublishedDiscussion(
        id=discussion["id"],
        number=discussion["number"],
        url=discussion["url"],
        topic=topic["name"],
        topic_title=topic["description"].strip(),
        title=title.strip(),
        content=content.strip(),
    )
