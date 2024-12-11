# Khiops Documentation Website
This is the technical repository for the Khiops documentation website.

## Setup
Install the development requirements

```bash
pip install -r requirements.txt
```

Then, to run locally just execute

```bash
mkdocs serve
```

Then open in a web browser the indicated URL, usually http://127.0.0.1:8000/ . You don't need to
restart the server every time because the site will refresh itself when you modify files.

### pre-commit
The previous step will also install the `pre-commit` tool. This allows to automatize some tasks such
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


## Maintainance
To update various versions in the website, you only have to change the following attributes in the
`extra` section of the `mkdocs.yml`:
- `KHIOPS_VERSION`: Khiops Core Executables
- `KHIOPS_PYTHON_VERSION`: Khiops Python Library
- `KHIOPS_SAMPLES_VERSION`: Khiops Sample Datasets
- `KHIOPS_VIZ_VERSION`: Khiops Visualization App
- `KHIOPS_COVIZ_VERSION`: Khiops Co-Visualization App


## Deploy to khiops.org
Once you have committed and pushed your changes, go to the "Actions" tab on Github and execute the
`Website` workflow on the `main` branch.
