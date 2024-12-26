# Generate a treemap graph from Pyright verifytypes output.

A simple cli tool to visualise the state of a Python project's _type compleness_, from the output of pyright's [`--outputjson --verifytypes` command](https://microsoft.github.io/pyright/#/typed-libraries?id=verifying-type-completeness):

![Sample graph output for prefect](https://raw.githubusercontent.com/mjpieters/pyright-analysis/refs/heads/main/assets/graph-screenshot.png)

## Usage

Use a Python tool manager like [`uv tool`](https://docs.astral.sh/uv/guides/tools/) or [`pipx`](https://pipx.pypa.io/):

```sh
$ uv tool install pyright pyright-analysis
```

Then generate a type compleness JSON report for your package, and transform the report into a graph:

```sh
$ pyright --outputjson --ignoreexternal --verifytypes PACKAGE > PACKAGE.json
$ pyright-analysis PACKAGE.json
```

This will open the resulting graph in your browser.

Full help documentation is available on the command-line:

![pyright-analysis help output](https://raw.githubusercontent.com/mjpieters/pyright-analysis/refs/heads/main/assets/cmd-help.png)

## Features

- Interactive responsive graph. Hover over each package to get more detail about symbol counts and completeness, or click on packages to zoom in.
- Export options:
    - Full stand-alone HTML page.
    - HTML div snippet with configurable HTML id.
    - Static image export as PNG, JPG, WebP, SVG or PDF.
    - Plotly JSON graph representation.
