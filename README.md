# Khiops Documentation Website
This is the technical repository for the Khiops documentation website.

## Local Development
### Setup
Install the development requirements

```bash
pip install -r requirements.txt
```

### Run
Then, to run locally just execute

```bash
mkdocs serve
```

Then open in a web browser the indicated URL, usually http://127.0.0.1:8000/ . You don't need to
restart the server every time because the site will refresh itself when you modify files.

#### pre-commit
The setup step will also install the `pre-commit` tool. This allows to automatize some tasks such
as formatting and cleaning of the notebooks.
To use it, it is necessary to install it locally:
```bash
pre-commit install
```

The configured tasks will run every time you make a commit. You may also run them at any time with
the line
```bash
pre-commit run --verbose --all-files
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
  - `KHIOPS_VIZ_VERSION`: version of the Khiops Visualization tool
  - `KHIOPS_COVIZ_VERSION`: version of the Khiops Covisualization tool
  - `KHIOPS_GCS_DRIVER_VERSION`: version of the Khiops GCS access driver
  - `KHIOPS_S3_DRIVER_VERSION`: version of the Khiops S3 access driver
* for the other version:
  - `KHIOPS_DOC_OTHER_REF`: revision of the current Git repository to be deployed
  - `KHIOPS_OTHER_VERSION`: version of the Khiops binaries package
  - `KHIOPS_PYTHON_OTHER_VERSION`: version of the Khiops Python library package
  - `KHIOPS_SAMPLES_OTHER_VERSION`: Git tag of the `khiops-samples` repository
  - `KHIOPS_VIZ_OTHER_VERSION`: version of the Khiops Visualization tool
  - `KHIOPS_COVIZ_OTHER_VERSION`: version of the Khiops Covisualization tool
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
