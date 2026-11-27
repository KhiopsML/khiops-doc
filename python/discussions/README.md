# Discussion synchronization

These scripts turn eligible [Khiops Discussions](https://github.com/orgs/KhiopsML/discussions)
into Q&A pages for the documentation site. Discussions are the source of truth:
edit the discussion rather than the generated pages. See the
[contributor guidance](../../README.md#editing-discussion-topics) for the label
and content conventions.

## Files

- [discussion_source.py](discussion_source.py) retrieves discussions, their
  labels and first reply from GitHub using `gh api graphql`. It handles
  pagination and reports API errors.
- [discussion_content.py](discussion_content.py) validates topic labels and
  selects the question and answer from either the initial post or the first
  reply's `### Question summary` section.
- [discussion_render.py](discussion_render.py) preserves supported discussion
  Markdown so Zensical can render it with the site's configured styling. It
  nests answer headings beneath their question, converts GitHub NOTE, TIP,
  IMPORTANT, WARNING and CAUTION alerts to site admonitions, sanitizes raw
  HTML, and rewrites supported attachment links to local assets. GitHub math
  fences are normalized to the site's math syntax; fenced code and ordinary
  Markdown tables, lists and links remain Markdown for site rendering. Bare
  URLs are turned into Markdown links outside code. Topic pages and attachment
  directories use the normalized topic label as their name. The overview
  identifies GitHub Discussions as the source and links to it. Images and
  Python scripts are named using the discussion number, the nearest preceding
  heading (or the discussion title), and a per-heading sequence number, for
  example `993-experiments-1.png` and `993-experiments-1.py`. Image and script
  sequences are independent. Names are deterministic but may change when
  headings or attachment order change. Repeated references to an attachment
  within the same heading share a file. Attachments over 100,000 bytes cause
  the discussion to be omitted and reported; downloaded scripts are not
  executed.
  Images and Python scripts are named using the discussion number, the nearest
  preceding heading (or the discussion title), and a per-heading sequence number,
  for example `993-experiments-1.png` and `993-experiments-1.py`. Image and
  script sequences are independent. Names are deterministic but may change when
  headings or attachment order change. Repeated references to an attachment
  within the same heading share a file.
  Attachments over 100,000 bytes cause the discussion to be omitted and
  reported; downloaded scripts are not executed.
- [generate_discussions.py](generate_discussions.py) ties the steps together.
  It updates generated files and navigation by comparing them with the
  repository, removes stale files only from the reserved Q&A output
  directories, maintains an oversized-attachment report, and summarizes
  generated file changes and invalid or unlabelled discussions.

## Workflow

The [synchronization workflow](../../.github/workflows/sync-discussions.yml)
runs the generator manually or on its enabled weekly schedule and proposes
changes in a pull request; it does not deploy the site. Generated pages and
attachments are written under `docs/`, navigation is updated in
`zensical.toml`, and synchronization state is stored in
`.github/discussion-sync/`.

To run the generator locally from the repository root, authenticate `gh` with
access to `KhiopsML/khiops` and run:

```bash
uv run --frozen python -m python.discussions.generate_discussions --report /tmp/discussion-report.md
```

This modifies generated files and navigation in the working tree. To run the
discussion tests without contacting GitHub:

```bash
uv run --frozen python -m unittest discover -s tests/discussions -v
```
