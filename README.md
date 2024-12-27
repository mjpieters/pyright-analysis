# Generate a treemap graph from Pyright verifytypes output.

[![PyPI version](https://img.shields.io/pypi/v/pyright-analysis.svg)](https://pypi.python.org/pypi/ruff)
[![License](https://img.shields.io/pypi/l/pyright-analysis.svg)](https://pypi.python.org/pypi/ruff)
![Python versions supported](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fmjpieters%2Fpyright-analysis%2Fmain%2Fpyproject.toml)
[![Built with uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Checked with Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with Pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)

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

![pyright-analysis help output](https://raw.githubusercontent.com/mjpieters/pyright-analysis/refs/heads/main/assets/cmd-help.png)  <!-- created with termshot cli -->

## Features

- Interactive responsive graph. Hover over each package to get more detail about symbol counts and completeness, or click on packages to zoom in.
- Export options:
    - Full stand-alone HTML page.
    - HTML div snippet with configurable HTML id.
    - Static image export as PNG, JPG, WebP, SVG or PDF.
    - Plotly JSON graph representation.
