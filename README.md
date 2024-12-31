# Generate a treemap graph from Pyright verifytypes output.

[![PyPI version](https://img.shields.io/pypi/v/pyright-analysis.svg)](https://pypi.python.org/project/pyright-analysis)
[![License](https://img.shields.io/pypi/l/pyright-analysis.svg)](https://pypi.python.org/pypi/ruff)
![Python versions supported](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fmjpieters%2Fpyright-analysis%2Fmain%2Fpyproject.toml)
[![Built with uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Checked with Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with Pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)
[![Python checks](https://github.com/mjpieters/pyright-analysis/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/mjpieters/pyright-analysis/actions/workflows/ci-cd.yml)
[![Coverage](https://codecov.io/gh/mjpieters/pyright-analysis/graph/badge.svg?token=ZRZO4XRBP6)](https://codecov.io/gh/mjpieters/pyright-analysis)

A simple cli tool to visualise the state of a Python project's _type completeness_, from the output of pyright's [`--outputjson --verifytypes` command](https://microsoft.github.io/pyright/#/typed-libraries?id=verifying-type-completeness):

![Sample graph output for prefect](https://raw.githubusercontent.com/mjpieters/pyright-analysis/refs/heads/main/assets/graph-screenshot.png)  <!-- 1980 × 1352 screenshot from Firefox, wrapped with https://shoteasy.fun/screenshot-beautifier/ to 4x3 ratio (2400 × 1800) -->

The interactive graph depicts a projects modules as a tree, with each the size of each module based on the number of exported symbols.

## Usage

Use a Python tool manager like [`uv tool`](https://docs.astral.sh/uv/guides/tools/) or [`pipx`](https://pipx.pypa.io/):

```sh
$ uv tool install pyright
$ uv tool install pyright-analysis
```

Then generate a type compleness JSON report for your package, and transform the report into a graph:

```sh
$ pyright --outputjson --ignoreexternal --verifytypes PACKAGE > PACKAGE.json
$ pyright-analysis PACKAGE.json
```

This will open the resulting graph in your browser.

Full help documentation is available on the command-line:

![pyright-analysis help output](https://raw.githubusercontent.com/mjpieters/pyright-analysis/refs/heads/main/assets/cmd-help.png)  <!-- created with termshot --columns 100 --show-cmd -->

## Features

- Interactive responsive graph. Hover over each package to get more detail about symbol counts and completeness, or click on packages to zoom in.
- Export options:
    - Full stand-alone HTML page.
    - HTML div snippet with configurable HTML id.
    - Static image export as PNG, JPG, WebP, SVG or PDF.
    - Plotly JSON graph representation.

## Development

This project uses [`uv`](https://docs.astral.sh/uv/) to handle Python dependencies and environments; use `uv sync` to get an up-to-date virtualenv with all dependencies. This includes development dependencies such as [Ruff](https://docs.astral.sh/ruff/) (used for linting and formatting) and [Pyright](https://microsoft.github.io/pyright/) (used to validate type annotations).

### Linting and formatting

While PRs and commits on GitHub are checked for linting and formatting issues, it's easier to check for issues locally first. After running `uv sync`, run `uv run pre-commit install` to install [pre-commit](https://pre-commit.com/) hooks that will run these tools and format your changes automatically on commits. These hooks also run `uv sync` whenever you working tree changes.

### Testing

This project uses `pytest` to run its tests: `uv run pytest`.
