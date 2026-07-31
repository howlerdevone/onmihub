# omnihub

![PyPI version](https://img.shields.io/pypi/v/omnihub.svg)

Python Boilerplate contains all the boilerplate you need to create a Python package.

* [GitHub](https://github.com/nanishb/omnihub/) | [PyPI](https://pypi.org/project/omnihub/) | [Documentation](https://nanishb.github.io/omnihub/)
* Created by [omnihub](https://omnihub.com) | GitHub [@nanishb](https://github.com/nanishb) | PyPI [@nanishb](https://pypi.org/user/nanishb/)
* MIT License

## Features

* TODO

## Documentation

Documentation is built with [Zensical](https://zensical.org/) and deployed to GitHub Pages.

* **Live site:** https://nanishb.github.io/omnihub/
* **Preview locally:** `just docs-serve` (serves at http://localhost:8000)
* **Build:** `just docs-build`

API documentation is auto-generated from docstrings using [mkdocstrings](https://mkdocstrings.github.io/).

Docs deploy automatically on push to `main` via GitHub Actions. To enable this, go to your repo's Settings > Pages and set the source to **GitHub Actions**.

## Development

To set up for local development:

```bash
# Clone your fork
git clone git@github.com:your_username/omnihub.git
cd omnihub

# Install in editable mode with live updates
uv tool install --editable .
```

This installs the CLI globally but with live updates - any changes you make to the source code are immediately available when you run `omnihub`.

Run tests:

```bash
uv run pytest
```

Run quality checks (format, lint, type check, test):

```bash
just qa
```

## Author

omnihub was created in 2026 by omnihub.

Built with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
