from pyright_analysis import __version__
from pyright_analysis._utils import project_link


def test_project_link() -> None:
    assert project_link() == (
        '<a href="https://github.com/mjpieters/pyright-analysis">pyright-analysis '
        f"v{__version__}</a>"
    )
