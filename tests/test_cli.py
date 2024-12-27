from collections.abc import Iterator, Sequence
from pathlib import Path
from unittest import mock

import pytest
from click.testing import Result
from typer.testing import CliRunner

from pyright_analysis.cli import FileFormat, IncludePlotlyJS, app


@pytest.fixture(scope="module")
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture()
def report_filename(pyright_json_report: str, tmp_path: Path) -> str:
    filename = tmp_path / "pyright_report.json"
    filename.write_text(pyright_json_report)
    return str(filename)


class TestCli:
    @pytest.fixture(autouse=True)
    def _setup(self, runner: CliRunner, pyright_json_report: str) -> Iterator[None]:
        self.runner = runner
        self.report = pyright_json_report
        with (
            mock.patch(
                "plotly.graph_objects.Figure.show", autospec=True
            ) as self.mock_show,
            mock.patch(
                "plotly.graph_objects.Figure.write_html", autospec=True
            ) as self.mock_write_html,
            mock.patch(
                "plotly.graph_objects.Figure.write_json", autospec=True
            ) as self.mock_write_json,
            mock.patch(
                "plotly.graph_objects.Figure.write_image", autospec=True
            ) as self.mock_write_image,
        ):
            yield

    def invoke(
        self, args: str | Sequence[str] | None = None, pipe_report: bool = False
    ) -> Result:
        return self.runner.invoke(
            app, args=args, input=self.report if pipe_report else None
        )

    def test_default_command_show(self, pyright_json_report: str) -> None:
        result = self.invoke(pipe_report=True)
        assert result.exit_code == 0
        self.mock_show.assert_called_once()

    def test_default_command_show_with_path(self, report_filename: str) -> None:
        result = self.invoke([report_filename])
        assert result.exit_code == 0
        self.mock_show.assert_called_once()

    def test_html_command(self, pyright_json_report) -> None:
        result = self.invoke(["html"], pipe_report=True)
        assert result.exit_code == 0
        self.mock_write_html.assert_called_once()
        call = self.mock_write_html.call_args
        assert call.args[1].name == "foobar.html"

    def test_html_command_filename(self, pyright_json_report) -> None:
        result = self.invoke(
            ["html", "--filename", "/spam/spam/wonderful_spam.html"], pipe_report=True
        )
        assert result.exit_code == 0
        self.mock_write_html.assert_called_once()
        call = self.mock_write_html.call_args
        assert call.args[1].name == "/spam/spam/wonderful_spam.html"

    @pytest.mark.parametrize(
        "include_js,expected",
        (
            ("embed", True),
            ("cdn", IncludePlotlyJS.cdn),
            ("directory", IncludePlotlyJS.directory),
            ("require", IncludePlotlyJS.require),
            ("omit", False),
        ),
    )
    def test_html_command_include_js(
        self, pyright_json_report, include_js: str, expected: IncludePlotlyJS | bool
    ) -> None:
        result = self.invoke(["html", "--include-js", include_js], pipe_report=True)
        assert result.exit_code == 0
        self.mock_write_html.assert_called_once()
        call = self.mock_write_html.call_args
        assert call.kwargs["include_plotlyjs"] == expected

    def test_html_command_stdout(self, pyright_json_report: str) -> None:
        result = self.invoke(["html", "--filename", "-"], pipe_report=True)
        assert result.exit_code == 0
        self.mock_write_html.assert_called_once()
        call = self.mock_write_html.call_args
        assert call.args[1].name == "<stdout>"

    def test_html_command_stdout_directory(self, pyright_json_report: str) -> None:
        result = self.invoke(
            ["html", "--include-js", "directory", "--filename", "-"], pipe_report=True
        )
        assert result.exit_code == 2
        assert "Can't write out javascript when writing to stdout" in result.output

    def test_json_command(self, pyright_json_report: str) -> None:
        result = self.invoke(["json"], pipe_report=True)
        assert result.exit_code == 0
        self.mock_write_json.assert_called_once()
        call = self.mock_write_json.call_args
        assert call.args[1].name == "foobar.json"

    def test_json_command_filename(self, pyright_json_report: str) -> None:
        result = self.invoke(
            ["json", "--filename", "/spam/spam/wonderful_spam.html"], pipe_report=True
        )
        assert result.exit_code == 0
        self.mock_write_json.assert_called_once()
        call = self.mock_write_json.call_args
        assert call.args[1].name == "/spam/spam/wonderful_spam.html"

    def test_image_command(self) -> None:
        result = self.invoke(["image"], pipe_report=True)
        assert result.exit_code == 0
        self.mock_write_image.assert_called_once()
        call = self.mock_write_image.call_args
        assert call.args[1].name == "foobar.png"

    def test_image_command_filename_extension_ignores_format(self) -> None:
        result = self.invoke(
            ["image", "--filename", "/spam/spam/wonderful_spam.svg", "--format", "pdf"],
            pipe_report=True,
        )
        assert result.exit_code == 0
        self.mock_write_image.assert_called_once()
        call = self.mock_write_image.call_args
        assert call.kwargs["format"] is None

    def test_image_command_valid_filename_extension_ignores_format(self) -> None:
        result = self.invoke(
            ["image", "--filename", "/spam/spam/wonderful_spam.svg", "--format", "pdf"],
            pipe_report=True,
        )
        assert result.exit_code == 0
        self.mock_write_image.assert_called_once()
        call = self.mock_write_image.call_args
        assert call.kwargs["format"] is None

    def test_image_command_invalid_filename_extension_keeps_format(self) -> None:
        result = self.invoke(
            [
                "image",
                "--filename",
                "/spam/spam/wonderful_spam.dat",
                "--format",
                "webp",
            ],
            pipe_report=True,
        )
        assert result.exit_code == 0
        self.mock_write_image.assert_called_once()
        call = self.mock_write_image.call_args
        assert call.kwargs["format"] == FileFormat.webp
