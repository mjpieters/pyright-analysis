import os
from enum import StrEnum, auto
from io import BufferedWriter, TextIOWrapper
from pathlib import Path
from typing import IO, Annotated, Any, NamedTuple

import click
import typer
from click import Context, File, Parameter
from typer.core import TyperGroup

from . import __version__ as VERSION
from .schema import PyrightJsonResults, TypeCompletenessReport
from .treemap import to_treemap

try:
    from plotly.io.kaleido import (  # pyright: ignore[reportMissingTypeStubs]
        scope as kaleido_scope,
    )
except RuntimeError as exc:  # pragma: no coverage
    if "Kaleido will try to detect it automatically" not in exc.args[0]:
        raise

    # Kaleido tried to find Chrome and failed; handle this separately
    # when attempting to use the image subcommand

    class _scope(NamedTuple):
        default_width: int | None = None
        default_height: int | None = None
        default_scale: float | None = None

    kaleido_scope = _scope()
    _kaleido_configured = False
else:
    _kaleido_configured = True


PLOTLY_CONFIG = {"displaylogo": False}


class ReportFromFile(File):
    def __init__(self) -> None:
        super().__init__()

    def convert(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        value: str | os.PathLike[str] | IO[Any],
        param: Parameter | None = None,
        ctx: Context | None = None,
    ) -> TypeCompletenessReport:
        fobj: IO[str] = super().convert(value, param, ctx)
        results = PyrightJsonResults.model_validate_json(fobj.read())
        return results.type_completeness


ReportArgument = Annotated[
    TypeCompletenessReport,
    typer.Argument(click_type=ReportFromFile(), default_factory=lambda: "-"),
]


class DefaultShowTyperGroup(TyperGroup):
    def parse_args(self, ctx: click.Context, args: list[str]) -> list[str]:
        args = super().parse_args(ctx, args)
        if not ctx.protected_args or ctx.protected_args[0] not in self.commands:
            ctx.protected_args.insert(0, "show")
        return args


app = typer.Typer(
    cls=DefaultShowTyperGroup,
    help=(
        """Generate a treemap graph from pyright JSON output.

        By default, the report is read from stdin, unless a filename is given.
        The special filename '-' can be used to force reading from stdin.
        
        The default command is "show", which opens the graph in your browser.

        """
    ),
)


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"pyright-analysis v{VERSION}")
        raise typer.Exit()


@app.callback()
def app_callback(
    _version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            help="Show program version and exit",
            callback=version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    pass


@app.command()
def show(report: ReportArgument) -> None:
    """Open the graph in your browser."""
    figure = to_treemap(report)
    figure.show(config=PLOTLY_CONFIG)  # pyright: ignore[reportUnknownMemberType]


class IncludePlotlyJS(StrEnum):
    embed = auto()
    cdn = auto()
    directory = auto()
    require = auto()
    omit = auto()


@app.command()
def html(
    report: ReportArgument,
    filename: Annotated[
        typer.FileTextWrite | None,
        typer.Option(
            show_default=False,
            help=(
                "Where to write the HTML data to. The default is to write it "
                "to the current directory, using the package name from the "
                "report plus '.html'. When set to '-' the output is written "
                "to stdout."
            ),
        ),
    ] = None,
    full_html: Annotated[
        bool,
        typer.Option(
            help=(
                "Generate a full HTML page, or just a div element suitable "
                "for embedding into a page"
            ),
        ),
    ] = True,
    include_js: Annotated[
        IncludePlotlyJS,
        typer.Option(
            help=(
                "Wether or not to embed the Plotly JS library in the output. "
                "If set to 'cdn', a script tag referencing the CDN-hosted "
                "version is used. 'directory' puts the JS file next to the "
                "HTML file in the same directory, and 'require' the script "
                "is loaded using require.js"
            )
        ),
    ] = IncludePlotlyJS.embed,
    div_id: Annotated[
        str | None,
        typer.Option(
            show_default=False,
            help="Provide a HTML id for the generated div. The default is to generate a UUID.",
        ),
    ] = None,
) -> None:
    """Write the generated treemap graph out as HTML."""
    match filename:
        case None:
            file = Path(".").joinpath(f"{report.package_name}.html")
        case TextIOWrapper(name="<stdout>"):
            file = filename
            if include_js is IncludePlotlyJS.directory:
                raise click.UsageError(
                    "Can't write out javascript when writing to stdout"
                )
        case _:
            file = filename
    figure = to_treemap(report)
    match include_js:
        case IncludePlotlyJS.embed:
            include_plotlyjs = True
        case IncludePlotlyJS.omit:
            include_plotlyjs = False
        case _:
            include_plotlyjs = include_js
    figure.write_html(  # pyright: ignore[reportUnknownMemberType]
        file,
        full_html=full_html,
        include_plotlyjs=include_plotlyjs,
        div_id=div_id,
        config=PLOTLY_CONFIG,
    )


@app.command()
def json(
    report: ReportArgument,
    filename: Annotated[
        typer.FileTextWrite | None,
        typer.Option(
            show_default=False,
            help=(
                "Where to write the JSON data to. The default is to write it "
                "to the current directory, using the package name from the "
                "report plus '.json'. When set to '-' the output is written "
                "to stdout."
            ),
        ),
    ] = None,
    pretty: Annotated[bool, typer.Option(help="Output pretty-printed JSON")] = False,
) -> None:
    """Write out JSON defining the graph."""
    match filename:
        case None:
            file = Path(".").joinpath(f"{report.package_name}.json")
        case _:
            file = filename

    figure = to_treemap(report)
    figure.write_json(file, pretty=pretty)  # pyright: ignore[reportUnknownMemberType]


class FileFormat(StrEnum):
    png = auto()
    jpg = auto()
    jpeg = jpg
    webp = auto()
    svg = auto()
    pdf = auto()


@app.command()
def image(
    report: ReportArgument,
    filename: Annotated[
        typer.FileBinaryWrite | None,
        typer.Option(
            show_default=False,
            help=(
                "Where to write the image to. The default is to write it "
                "to the current directory, using the package name from the "
                "report plus the image type extension. When set to '-' the "
                "output is written to stdout."
            ),
        ),
    ] = None,
    format: Annotated[
        FileFormat,
        typer.Option(
            help=(
                "What type of image to generate. If a filename is given that "
                "ends in a support image type extension, this argument is "
                "ignored."
            ),
        ),
    ] = FileFormat.png,
    width: Annotated[
        int | None,
        typer.Option(min=1, help="The width of the image, in layout pixels."),
    ] = kaleido_scope.default_width,
    height: Annotated[
        int | None,
        typer.Option(min=1, help="The height of the image, in layout pixels."),
    ] = kaleido_scope.default_height,
    scale: Annotated[
        float | None,
        typer.Option(
            min=0,
            help=(
                "The image scale; The physical output size of the image is "
                "scale * width by scale * height pixels"
            ),
        ),
    ] = kaleido_scope.default_scale,
) -> None:
    """Render the graph as an image.

    Image rendering requires that a Chromium-based browser is installed locally;
    by default this looks for a Chrome installation. Set the BROWSER_PATH environment
    variable to the path of an alternative Chromium-based browser (e.g. Brave) to
    configure this.

    """
    if not _kaleido_configured:
        raise click.UsageError(
            "Image rendering requires a Chromium-based browser installation "
            "but none was detected. Please set the BROWSER_PATH environment "
            "variable to an absolute path of such a browser before running "
            "this command."
        )
    file_format = format
    match filename:
        case None:
            file = Path(".").joinpath(f"{report.package_name}.{format.name}")
        case BufferedWriter(name="<stdout>"):  # pragma: no cover
            # pytest and CliRunner mess too much with stdout to bother trying to test
            # this with anything other than a manual test.
            file = filename
        case _:
            file = filename
            if file.name.endswith(tuple("." + ext for ext in FileFormat.__members__)):
                file_format = None

    figure = to_treemap(report)
    figure.write_image(  # pyright: ignore[reportUnknownMemberType]
        file, format=file_format, width=width, height=height, scale=scale
    )
