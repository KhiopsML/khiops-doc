---
description: "Use when changing GitHub Discussions import, Q&A generation, synchronization workflow, or discussion tests."
applyTo: "python/discussions/**, tests/discussions/**, .github/workflows/sync-discussions.yml, .github/discussion-sync/**, docs/q-and-a/**, docs/assets/images/q-and-a/**, docs/assets/discussion-scripts/q-and-a/**"
---

# Discussion synchronization

- Treat GitHub Discussions as the source of truth; change source discussions or the generator, not generated pages by hand. See [discussion synchronization](../../python/discussions/README.md) for the architecture and commands.
- Preserve publication for discussions with exactly one `Topic/` label and a nonempty label description. Use the discussion title and initial post unless the first reply has a `### Question summary`; then use that section as the title and the rest of the reply as content. Report invalid discussions without blocking valid ones.
- Preserve sanitized output and source links. Download only supported trusted GitHub attachments, never execute scripts, and omit and report a discussion if an attachment exceeds 100,000 bytes.
- Keep generated files deterministic and protect files not owned by the generator. Update only the marked discussion navigation block in `zensical.toml`.
- Keep synchronization reviewable through a pull request, not direct deployment. Preserve the oversized-file report and avoid duplicate PRs for unchanged, already merged reports.
- When changing behavior, update the contributor guidance and targeted tests. Run `uv run --frozen python -m unittest discover -s tests/discussions -v` from the repository root.
- The workflow uses `GITHUB_TOKEN` for cross-repository discussion access and PR creation; do not assume real Actions permissions have been verified by local tests.
