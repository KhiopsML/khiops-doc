# Khiops Documentation Website
This is the technical repository for the Khiops documentation website.

## Local Development
### Setup
Install dependencies with uv

```bash
uv sync --frozen --extra notebooks
```

If you need to execute tutorials locally, install tutorial extras as well:

```bash
uv sync --frozen --extra notebooks --extra tutorials
```

### Run
Before running the local server, fetch the Python API docs that are normally injected by CI:

```bash
./scripts/fetch_python_api_docs.sh
```

Then, to run locally just execute

```bash
uv run zensical serve
```

Then open in a web browser the indicated URL, usually http://127.0.0.1:8000/ . You don't need to
restart the server every time because the site will refresh itself when you modify files.

### Editing Tutorial Notebooks
- Edit source notebooks in `docs/tutorials/sourced-notebooks/` (`.ipynb` files).
- Generated Markdown pages are written to `docs/tutorials/notebooks/` by the converter.
- After changing a source notebook, regenerate pages with:

```bash
uv run python scripts/convert_notebooks.py
```

#### pre-commit
The setup step installs the `pre-commit` tool. This allows to automatize some tasks such as
formatting and cleaning of the notebooks.
To use it, it is necessary to install it locally:
```bash
uv run pre-commit install
```

The configured tasks will run every time you make a commit. You may also run them at any time with
the line
```bash
uv run pre-commit run --verbose --all-files
```

### Highlighting Khiops Dictionary Code
The Khiops Dictionary Language code can be highlighted by using the `kdic` syntax in code blocks:
````md
```kdic
Dictionary Example
{
  Categorical target;
  Numerical feature;
};
```
````

The rule signatures can be highlighted with the `kdic-api-docs` syntax:
````md
```kdic-api-docs
Numerical Diff(Numerical value1, Numerical value2);
```
````

## Production
### Basics
The CI/CD of this repository fetches the Khiops Python Sphinx-built
documentation from the specified (see below) release of
https://github.com/KhiopsML/khiops-python and builds the specified revision of
the current repository documentation.

The current CI/CD supports building and deploying _two_ versions of the Khiops
documentation web site:

- the _current_ version, accessible at the https://khiops.org URL.
- the _other_ version, accessible at the https://khiops.org/x.y.z[-pre] URL.

### Maintenance
The versions are specified by the following variables, which are configured
in the `environment.env` file:
* for the current version:
  - `KHIOPS_VERSION`: version of the Khiops binaries package
  - `KHIOPS_PYTHON_VERSION`: version of the Khiops Python library package
  - `KHIOPS_SAMPLES_VERSION`: Git tag of the `khiops-samples` repository
  - `KHIOPS_VIZ_VERSION`: default version of the Khiops Visualization tool (if the variable is empty, the latest release is used)
  - `KHIOPS_GCS_DRIVER_VERSION`: version of the Khiops GCS access driver
  - `KHIOPS_S3_DRIVER_VERSION`: version of the Khiops S3 access driver
* for the other version:
  - `KHIOPS_DOC_OTHER_REF`: revision of the current Git repository to be deployed
  - `KHIOPS_OTHER_VERSION`: version of the Khiops binaries package
  - `KHIOPS_PYTHON_OTHER_VERSION`: version of the Khiops Python library package
  - `KHIOPS_SAMPLES_OTHER_VERSION`: Git tag of the `khiops-samples` repository
  - `KHIOPS_VIZ_OTHER_VERSION`: version of the Khiops Visualization tool (in the current version, the latest version is displayed automatically)
  - `KHIOPS_GCS_DRIVER_OTHER_VERSION`: version of the Khiops GCS access driver
  - `KHIOPS_S3_DRIVER_OTHER_VERSION`: version of the Khiops S3 access driver

Note: for the current version settings, the version of the current Git
repository the CI/CD is launched on will be used.

### CI/CD Usage
The CI/CD can only be launched manually, from the GitHub interface. A pull
request is not necessary to this end and has no effect on the CI/CD execution.

The CI/CD supports two Boolean inputs:
- whether to build the other version of the web site or not (`false` by default)
- whether to deploy or not (`false` by default).

Hence, by the default, the CI only builds the current version of the Khiops
documentation, but does not deploy it to GitHub pages.

When the CI is instructed to only build the documentation, without deploying it,
a GitHub workflow artifact is created with the contents of the built
documentation.

### Local Inspection of the Khiops Website
The artifact created by the CI/CD at the build stage allows for manual, local
inspection of the documentation build (with or without the other version).

To do this, unzip the artifact into a directory, then, within that directory, launch an HTTP server, via, for example:

```bash
python -m http.server
```

Then open in a web browser the following URL: http://127.0.0.1:8000/.

You don't need to
restart the server every time but you need to refresh the pages when you modify files.

### Deploy to khiops.org
To deploy the web site to khiops.org, you need to check the "Deploy to GH pages"
checkbox on the GitHub workflow user interface: go to the "Actions" tab and
execute the "Website" workflow on the `main` branch.

In order to deploy:
- "current" v10 + "other" (beta) v11: the GH workflow must be launched from the
  `dev-v10` branch;
- "current" (beta) v11 + "other" v10: the GH workflow must be launched
  from the `dev` branch.


