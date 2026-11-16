# Vendored Fonts

This directory contains locally vendored font binaries used by the documentation site.

## Files

- `inter-latin-400.woff2`
  - Family: Inter
  - Scope: Latin subset
  - Source CSS endpoint:
    - https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap
  - Binary source host:
    - https://fonts.gstatic.com/
  - License file in this directory:
    - `LICENSE-Inter-OFL.txt`

- `roboto-mono-latin-400.woff2`
  - Family: Roboto Mono
  - Scope: Latin subset
  - Source CSS endpoint:
    - https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500;700&display=swap
  - Binary source host:
    - https://fonts.gstatic.com/
  - License file in this directory:
    - `LICENSE-RobotoMono-Apache-2.0.txt`

## Notes

- Fonts are served locally via `@font-face` rules defined in `overrides/assets/stylesheets/main.css`.
- Theme-level external font loading is disabled in `mkdocs.yml` (`theme.font: false`).
- Retrieval date: 2026-07-24.
