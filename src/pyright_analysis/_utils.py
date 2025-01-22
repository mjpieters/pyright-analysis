from collections.abc import Iterator
from importlib.metadata import metadata


def project_link() -> str:
    """The name of this project as a HTML hyperlink"""
    md = metadata("pyright-analysis")
    entries: Iterator[tuple[str, str, str]] = (
        entry.partition(",") for entry in md.get_all("Project-URL", [])
    )
    github_link = next(
        url.strip() for label, _, url in entries if label.strip().lower() == "github"
    )
    return f'<a href="{github_link}">{md["Name"]} v{md["Version"]}</a>'
