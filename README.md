# Khiops Documentation Website
This is the (technical) repository for the Khiops documentation website.

## Build Dependencies
To build the website locally you'll need the following python packages
- `mkdocs`
- `mkdocs-material`
- `mkdocs-jupyter`
- `./python/kdic_lexer` : Khiops Dictionary pygments lexer.

You may install them with `pip`

```bash
pip install mkdocs mkdocs-material mkdocs-jupyter
```

## How to Run Locally
To run locally just execute

```bash
mkdocs serve
```

Then open in a web browser the indicated URL, usually http://127.0.0.1:8000/ . You don't need to
restart the server every time because the site will refresh itself when you modify files.

## Deploy to khiops.org
Once you have committed and pushed your changes. Use the `ci` workflow in the repo's actions.

