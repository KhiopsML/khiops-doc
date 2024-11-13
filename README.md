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
pip install -r requirements.txt
```

## How to Run Locally
To run locally just execute

```bash
mkdocs serve
```

Then open in a web browser the indicated URL, usually http://127.0.0.1:8000/ . You don't need to
restart the server every time because the site will refresh itself when you modify files.

## Highlighting Khiops Dictionary Code
The Khiops Dictionary Language code maybe highlighted by using the `kdic` syntax in code blocks:
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

## Deploy to khiops.org
Once you have committed and pushed your changes. Use the `ci` workflow in the repo's actions.

