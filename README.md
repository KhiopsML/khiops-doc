# Khiops Documentation Website
This is the technical repository for the Khiops documentation website.

## Setup
Install the website requirements

```bash
pip install -r requirements.txt
```

Then, to run locally just execute

```bash
mkdocs serve
```

Then open in a web browser the indicated URL, usually http://127.0.0.1:8000/ . You don't need to
restart the server every time because the site will refresh itself when you modify files.


## Maintainance
To update various versions in the website, you only have to change the following attributes in the
`extra` section of the `mkdocs.yml`:
- `KHIOPS_VERSION`: Khiops Core Executables
- `KHIOPS_PYTHON_VERSION`: Khiops Python Library
- `KHIOPS_SAMPLES_VERSION`: Khiops Sample Datasets
- `KHIOPS_VIZ_VERSION`: Khiops Visualization App
- `KHIOP_COVIZ_VERSION`: Khiops Co-Visualization App


## Deploy to khiops.org
Once you have committed and pushed your changes. Use the `ci` workflow in the repo's actions.
