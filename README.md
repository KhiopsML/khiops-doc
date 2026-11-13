# Khiops Documentation Website

This is the technical repository for the Khiops documentation website.

## Local Development

### Setup

Install `uv` first (required for all commands below):

- Official installation instructions: https://docs.astral.sh/uv/getting-started/installation/

Then install dependencies with `uv`:

```bash
uv sync --frozen --extra notebooks --extra pythonapi --extra dev
```

Building the site locally also requires `git`, plus `curl` to resolve omitted
versions from GitHub (included with Git Bash on Windows).

On Windows, run the build from Git Bash with `bash` (not `sh`). From an existing
Command Prompt session at the repository root, select Git Bash explicitly
(adjust the Git installation path if necessary):

```cmd
"C:\Program Files\Git\bin\bash.exe" ./local-build.sh
```

In PowerShell, prefix that command with `&`. A bare `bash` command may launch
WSL instead of Git Bash; use `where bash` in Command Prompt to check. WSL needs
its own Linux installation of `uv` and the build dependencies; it does not use
the Windows `uv.exe` installation.

### Run

The Python API pages (`docs/api-docs/python-api/`) are generated from the `khiops-python` source (not fetched as prebuilt HTML). Run:

```bash
./local-build.sh
```

No parameters are mandatory. Omitted core, Python and samples versions are
resolved independently from the latest published GitHub releases of
[KhiopsML/khiops](https://github.com/KhiopsML/khiops/releases/latest),
[KhiopsML/khiops-python](https://github.com/KhiopsML/khiops-python/releases/latest),
and [KhiopsML/khiops-samples](https://github.com/KhiopsML/khiops-samples/releases/latest).
This uses GitHub's latest release, not a development branch or prerelease.
Network or release lookup failures stop the build with an error.
You can override any version independently, or pin all three for reproducibility:

```bash
./local-build.sh --khiops-version VERSION --khiops-python-version PYVERSION --khiops-samples-version SAMPLESVERSION
```

CI continues to use the samples version pinned in `environment.env`. A newer
samples release may not be compatible with older tutorials or Python versions.

Core and Python release versions can differ. The Python source ref must also
support Zensical: it needs `doc/util/create-doc` and `zensical.toml`. The Python
release tag `11.0.1.0` still uses Sphinx and cannot be built by this pipeline.
Resolving the latest release does not guarantee that it has migrated to Zensical;
the build reports an error for incompatible releases rather than silently using
another ref. For a local preview using the newer documentation sources on `main`,
run from Windows Command Prompt:

```cmd
"C:\Program Files\Git\bin\bash.exe" ./local-build.sh --khiops-python-ref main
```

This documents and installs the Python sources from `main`, not the exact
latest release; `--khiops-python-version` (or its resolved default) only sets the
displayed version when a separate ref is supplied. For release-accurate documentation, use a
compatible Zensical-based release ref and its matching version instead.

`PYVERSION` must be an existing, compatible `khiops-python` Git ref unless you
specify `--khiops-python-ref REF` separately. You can list the available release
tags with `git ls-remote --tags https://github.com/KhiopsML/khiops-python.git`.

This installs the selected Khiops core version via Uv, clones `khiops-python`
(at the selected Python release tag by default; use `--local-khiops-python DIR` to build from a local checkout
instead), converts its docstrings into the `docs/api-docs/python-api/` tree,
regenerates the Python API nav, and builds the whole site with Zensical into
`./site`. The script uses a separate `.venv-local-build` environment, which is
removed automatically when it exits; your normal `.venv` is left untouched.

Useful flags (see `./local-build.sh --help` for the full list):

- `--khiops-version VER` - Khiops core version to install via Uv (default: latest GitHub release)
- `--local-khiops-python DIR` - build from a local `khiops-python` checkout
- `--khiops-python-version VER` - Khiops Python version to document in the built site (default: latest GitHub release)
- `--khiops-python-ref REF` - Git ref to build from when not local (default: `khiops-python-version` if supplied, otherwise the latest Python release tag)
- `--khiops-samples-version VER` - published `khiops-samples` release used by the tutorials (default: latest GitHub release); branch names such as `main` are not release archives
- `--khiops-python-tutorial-ref REF` - `khiops-python-tutorial` Git ref (default: `main`)
- `--khiops-viz-version VER`, `--khiops-gcs-driver-version VER`, `--khiops-s3-driver-version VER`, `--khiops-azure-driver-version VER` - versions displayed/linked on the site (default: `unknown`)
- `--execute-tutorials` - also execute khiops-doc's own tutorial notebooks (`docs/tutorials/sourced-notebooks/`)
- `--serve` - launch `zensical serve` (live-reloading) after the build

To preview a build without `--serve`, serve the output directory directly:

```bash
python -m http.server --directory site
```

Then open in a web browser the indicated URL, usually http://127.0.0.1:8000/.
After rebuilding the site, force-refresh the page (Ctrl+F5 on Windows/Linux or
Cmd+Shift+R on macOS) if the browser still shows the previous version.

### Editing Tutorial Notebooks

- Edit source notebooks in `docs/tutorials/sourced-notebooks/` (`.ipynb` files).
- Generated Markdown pages are written to `docs/tutorials/notebooks/` by the converter.
- After changing a source notebook, regenerate pages with:

```bash
uv run python scripts/convert_notebooks.py
```

### pre-commit

The setup step installs the `pre-commit` tool. This allows to automatize some tasks such as formatting and cleaning of the notebooks. To use it, it is necessary to install it locally:

```bash
uv run pre-commit install
```

The configured tasks will run every time you make a commit. You may also run them at any time with the line

```bash
uv run pre-commit run --verbose --all-files
```

### Highlighting Khiops Dictionary Code

The Khiops Dictionary Language code can be highlighted by using the `kdic` syntax in code blocks:

```kdic
Dictionary Example
{
  Categorical target;
  Numerical feature;
};
```

The rule signatures can be highlighted with the `kdic-api-docs` syntax:

```kdic-api-docs
Numerical Diff(Numerical value1, Numerical value2);
```

## Production

### Basics

The CI/CD workflow (`.github/workflows/ci.yml`) installs Khiops core (via Uv)
and then runs the same build pipeline as `local-build.sh`: it clones
`khiops-python` (at the Git tag given by `KHIOPS_PYTHON_VERSION` by default in
the CI, unless overriden via the `KHIOPS_PYTHON_REF` variable in
`environment.env`), prepares its Zensical-based API doc sources via `create-doc
-p` (see `.github/scripts/prepare-python-api-doc.sh`), copies them into
`docs/api-docs/python-api/`, regenerates the Python API nav, and builds the
resulting site with Zensical. This shared pipeline lives in
`.github/scripts/build-doc.sh`, used by both the CI workflow and
`local-build.sh` - there is no separate `build-doc` composite action.

Only a single version of the site is built and deployed.

### CI/CD Usage

The CI/CD can only be launched manually, from the GitHub interface. A pull request is not necessary to this end and has no effect on the CI/CD execution.

The CI/CD supports the following `workflow_dispatch` inputs, all with sensible defaults:

- `execute-khiops-tutorials` (boolean, default `false`) - also execute khiops-doc's own tutorial notebooks
- `deploy-gh-pages` (boolean, default `false`) - deploy the built site to GH Pages
- `check-links` (boolean, default `false`) - check the built site for broken links

By default, the CI only builds the documentation and uploads it as a GitHub workflow artifact, without deploying it to GitHub Pages.

### Local Inspection of the Khiops Website

The artifact created by the CI/CD at the build stage allows for manual, local inspection of the documentation build.

To do this, unzip the artifact into a directory, then, within that directory, launch an HTTP server, via, for example:

```bash
python -m http.server
```

Then open in a web browser the following URL: http://127.0.0.1:8000/.

You don't need to restart the server every time but you need to refresh the pages when you modify files.

### Deploy to khiops.org

To deploy the web site to khiops.org, launch the "Website" workflow manually: go to the "Actions" tab, run the workflow on the `dev` branch, and set the `deploy-gh-pages` input to `true`.
