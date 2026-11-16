# Khiops Documentation Website

This is the technical repository for the Khiops documentation website.

## Local Development

### Setup

Install `uv` first (required for all commands below):

- Official installation instructions: https://docs.astral.sh/uv/getting-started/installation/

Building the site locally also requires the following tools. `local-build.sh`
checks for them and stops with an error if one is missing (`curl` is only
needed, and checked, when the Khiops Visualization version has to be resolved):

- `git`;
- `envsubst` (provided by `gettext`);
- `curl`, only to resolve the Khiops Visualization version when it is neither
  passed on the command line nor set in `environment.env`;
- `wget` and `unzip`, only with `--execute-tutorials`.

The script creates its own Python 3.14 virtual environment (`uv` downloads
Python if needed) and warns if the installed `uv` differs from the version
pinned in the CI workflow, so that local builds stay as close as possible to
the CI builds.

#### Windows

Two setups are possible: native Windows, running the scripts through Git Bash
from a Command Prompt (described first), or WSL, which provides a Linux
environment closest to the CI.

##### Native Windows (Command Prompt with Git Bash)

1. Install [Git for Windows](https://git-scm.com/download/win), which provides
   Git Bash, `git` and `curl`. The commands below assume that Git's `bash.exe`
   is `C:\Program Files\Git\bin\bash.exe`; adjust the path if Git is installed
   elsewhere.
2. Before cloning anything, configure Git globally (recommended):

   ```cmd
   git config --global core.autocrlf input
   git config --global core.longpaths true
   ```

   The shell scripts of this repository are always checked out with LF line
   endings (`.gitattributes`), and the build forces LF line endings and long-path
   support in its own clone of `khiops-python`, whose scripts (such as
   `create-doc`) would otherwise be checked out with CRLF line endings under the
   Windows default `core.autocrlf=true` and fail in Bash. The global settings
   still matter for the clone of this repository itself and for repositories
   that `khiops-python`'s `create-doc` clones during the build (such as the
   tutorial repository), which follow your Git configuration. If you already
   cloned this repository with the default `core.autocrlf=true`, its shell
   scripts are still correct.
3. Clone this repository in a short path (for example `C:\dev\khiops-doc`):
   the build generates deeply nested files and Windows limits path lengths.
4. Install `uv` (see the Setup instructions above). Open a new Command Prompt
   after installing `uv`, so that the updated `PATH` is taken into account.
5. Check that the required tools are available to Git Bash:

   ```cmd
   "C:\Program Files\Git\bin\bash.exe" -c "command -v git curl envsubst uv"
   "C:\Program Files\Git\bin\bash.exe" -c "command -v wget unzip"
   ```

   Each command prints the location of every tool it finds; a tool that is not
   printed is missing. `wget` and `unzip` are only needed with
   `--execute-tutorials`.

   Git Bash does not provide `wget` or `unzip`, and may not provide `envsubst`.
   Install the missing ones with a Windows package manager and make sure they
   are on the Windows `PATH`, which Git Bash inherits. For example, with
   [Scoop](https://scoop.sh/):

   ```cmd
   scoop install wget unzip gettext
   ```

6. Run the build from a Command Prompt at the repository root, calling Git Bash
   explicitly:

   ```cmd
   "C:\Program Files\Git\bin\bash.exe" ./local-build.sh
   ```

   In PowerShell, prefix that command with `&`. Do not use a bare `bash`
   command: it may launch WSL instead of Git Bash; use `where bash` in Command
   Prompt to check. Every `./local-build.sh ...` command in the next section
   is run the same way on native Windows, with the same prefix and the same options.

Windows-specific notes:

- With `--local-khiops-python DIR`, give the path with forward slashes
  (`C:/dev/khiops-python`), or quote it if it contains spaces.
- Stop `--serve` with Ctrl+C. If the terminal does not respond, close it and
  delete the `.venv-local-build` directory manually. Deleting that directory can
  also fail temporarily if an antivirus or indexer locks its files; running the
  script again recreates it.

##### WSL

WSL runs the build in a Linux environment, like the CI. It needs its own Linux
installation of `uv` and of the build dependencies; it does not use the Windows
`uv.exe` installation. For example, on Ubuntu:

```bash
sudo apt-get install git curl gettext-base wget unzip
```

Clone this repository inside the WSL file system (for example under `~/`),
not under `/mnt/c`: the Windows drive is much slower and can introduce CRLF
line endings. The server started by `--serve` can be opened from the Windows
browser at the indicated `http://127.0.0.1:8000/` URL.

#### Python development environment (optional)

This step is not needed to run `local-build.sh`, which creates its own virtual
environment. It is only needed to edit the tutorial notebooks, to use
`pre-commit`, or to run `uv run …` commands directly. Once the repository is
cloned (on native Windows, from a Command Prompt at the repository root), run:

```bash
uv sync --frozen --extra notebooks --extra pythonapi --extra dev
```

### Run

The Python API pages (`docs/api-docs/python-api/`) are generated from the `khiops-python` source (not fetched as prebuilt HTML). Run:

```bash
./local-build.sh
```

On native Windows, run this and every other `./local-build.sh ...` command of this
section from a Command Prompt as
`"C:\Program Files\Git\bin\bash.exe" ./local-build.sh ...` (see Setup).

The versions used by the build are read from `environment.env`, the same file
that drives the CI. To build another version, edit that file (it is the only
file you should need to edit before a build), or override any value on the
command line; command-line options take precedence over `environment.env`:

```bash
./local-build.sh --khiops-version VERSION --khiops-python-version PYVERSION --khiops-samples-version SAMPLESVERSION
```

Unlike the CI, which runs on a reviewed repository state, the script cannot
assume that `environment.env` is correct. It therefore stops with an error if a
mandatory version is neither passed on the command line nor defined in
`environment.env`: the Khiops core, Khiops Python and `khiops-samples`
versions, and the GCS, S3 and Azure driver versions. The remaining values have
defaults:

- the `khiops-python` Git ref (`KHIOPS_PYTHON_REF`) defaults to the Khiops
  Python version;
- the `khiops-python-tutorial` Git ref (`KHIOPS_PYTHON_TUTORIAL_VERSION` in
  `environment.env`) defaults to `main`;
- the Khiops Visualization version (`KHIOPS_VIZ_VERSION`) defaults to the
  latest GitHub release of
  [KhiopsML/khiops-visualization-desktop](https://github.com/KhiopsML/khiops-visualization-desktop/releases/latest),
  as in the CI. This is the only version resolved from the network; the build
  itself still needs network access to install packages and to clone
  `khiops-python` (which can also be cloned from a local repository).

Values already exported in your shell are ignored. Only `environment.env` and the
command line are used.

A `khiops-samples` release passed on the command line that differs from the one
in `environment.env` may not be compatible with older tutorials or Python
versions.

Core and Python release versions can differ. The Python source ref must also
support Zensical: it needs `doc/util/create-doc` and `zensical.toml`. The Python
release tag `11.0.1.0` still uses Sphinx and cannot be built by this pipeline.
The build reports an error for incompatible refs rather than silently using
another ref. For a local preview using the newer documentation sources on `main`,
pass the ref explicitly (or uncomment `KHIOPS_PYTHON_REF=main` in
`environment.env`):

- on native Windows:

  ```cmd
  "C:\Program Files\Git\bin\bash.exe" ./local-build.sh --khiops-python-ref main
  ```

- on Linux, macOS and WSL:

  ```bash
  ./local-build.sh --khiops-python-ref main
  ```

This documents and installs the Python sources from `main`, not the exact
release; `--khiops-python-version` (or its value in `environment.env`) only sets
the displayed version when a separate ref is supplied. For release-accurate
documentation, use a compatible Zensical-based release ref and its matching
version instead.

Unless `--khiops-python-ref REF` (or `KHIOPS_PYTHON_REF`) is specified,
`PYVERSION` is also used as the `khiops-python` Git ref, so it must be an
existing, compatible Git ref. You can list the available release tags with
`git ls-remote --tags https://github.com/KhiopsML/khiops-python.git`.

This installs the selected Khiops core version via Uv, clones `khiops-python`
(checked out at the selected ref, by default the tag matching the Khiops Python
version), converts its docstrings into the `docs/api-docs/python-api/` tree,
regenerates the Python API nav, and builds the whole site with Zensical into
`./site`. The script uses a separate `.venv-local-build` environment, which is
removed automatically when it exits; your normal `.venv` is left untouched.

During the build, `zensical.toml` is temporarily modified (versions and Python
API navigation), `docs/api-docs/python-api.md` is removed, and generated files
are created under `docs/api-docs/python-api/` and `docs/tutorials/notebooks/`.
All of this is restored or removed when the build ends, therefore do not edit
these files while a build is running.

Use `--local-khiops-python DIR` to clone a local `khiops-python` Git repository
instead of the GitHub one. Commits that have not been pushed can be used, but
uncommitted changes are not included. The ref (tag, branch or commit) is looked
up in that local repository, so pass `--khiops-python-ref` when the default tag
does not exist there.

Useful flags (see `./local-build.sh --help` for the full list). Unless stated
otherwise, the default is the value read from `environment.env`:

- `--khiops-version VER` - Khiops core version to install via Uv
- `--local-khiops-python DIR` - build from a local `khiops-python` Git repository
- `--khiops-python-version VER` - Khiops Python version to document in the built site
- `--khiops-python-ref REF` - `khiops-python` Git ref (tag, branch or commit) to build from, in the GitHub or the local repository (default: `KHIOPS_PYTHON_REF` in `environment.env`, otherwise the Khiops Python version)
- `--khiops-samples-version VER` - published `khiops-samples` release used by the tutorials and by the `khiops-python` documentation build; branch names such as `main` are not release archives
- `--khiops-python-tutorial-ref REF` - `khiops-python-tutorial` Git ref (default: `KHIOPS_PYTHON_TUTORIAL_VERSION` in `environment.env`, otherwise `main`)
- `--khiops-viz-version VER` - Khiops Visualization version (default: `KHIOPS_VIZ_VERSION` in `environment.env`, otherwise the latest GitHub release)
- `--khiops-gcs-driver-version VER`, `--khiops-s3-driver-version VER`, `--khiops-azure-driver-version VER` - driver versions displayed/linked on the site
- `--execute-tutorials` - also execute khiops-doc's own tutorial notebooks (`docs/tutorials/sourced-notebooks/`)
- `--serve` - after the build, serve the built `./site` on http://127.0.0.1:8000/ (no live reload; rebuild to see changes). Stop it with Ctrl+C.

To preview an already built site without rebuilding, serve the output directory directly:

```bash
python -m http.server --bind 127.0.0.1 --directory site
```

On Windows, use `py -m http.server --bind 127.0.0.1 --directory site` if
`python` is not on your `PATH`.

Then open in a web browser the indicated URL, usually http://127.0.0.1:8000/.
After rebuilding the site, force-refresh the page (Ctrl+F5 on Windows/Linux or
Cmd+Shift+R on macOS) if the browser still shows the previous version.

### Editing Tutorial Notebooks

- Edit source notebooks in `docs/tutorials/sourced-notebooks/` (`.ipynb` files).
- Generated Markdown pages are written to `docs/tutorials/notebooks/` by the converter (a local build removes this directory when it ends).
- After changing a source notebook, regenerate pages with the following command
  (this requires the Python development environment described in Setup):

```bash
uv run python scripts/convert_notebooks.py
```

### pre-commit

The Python development environment described in Setup (`uv sync`) installs the
`pre-commit` tool. This allows to automatize some tasks such as formatting and cleaning of the notebooks. To use it, it is necessary to install it locally:

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
the CI, unless overridden via the `KHIOPS_PYTHON_REF` variable in
`environment.env`), prepares its Zensical-based API doc sources via `create-doc
-p` (see `.github/scripts/prepare-python-api-doc.sh`), copies them into
`docs/api-docs/python-api/`, regenerates the Python API nav, and builds the
resulting site with Zensical. This shared pipeline lives in
`.github/scripts/build-doc.sh`, used by both the CI workflow and
`local-build.sh` - there is no separate `build-doc` composite action. Both read
the versions from `environment.env`, so a local build with no command-line
option uses the same versions as the CI.

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
python -m http.server --bind 127.0.0.1
```

On Windows, use `py -m http.server --bind 127.0.0.1` if `python` is not on your
`PATH`.

Then open in a web browser the following URL: http://127.0.0.1:8000/.

You don't need to restart the server every time but you need to refresh the pages when you modify files.

### Deploy to khiops.org

To deploy the web site to khiops.org, launch the "Website" workflow manually: go to the "Actions" tab, run the workflow on the `dev` branch, and set the `deploy-gh-pages` input to `true`.
