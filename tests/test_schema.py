import pytest
from syrupy.assertion import SnapshotAssertion

from pyright_analysis.schema import PyrightJsonResults, SymbolName


def test_load_json(
    snapshot_pydantic: SnapshotAssertion, pyright_json_report: str
) -> None:
    results = PyrightJsonResults.model_validate_json(pyright_json_report)
    assert results == snapshot_pydantic


class TestSymbolName:
    @pytest.mark.parametrize(
        "name,expected",
        (
            ("foo.bar", "foo"),
            ("foo", ""),
        ),
    )
    def test_parent(self, name: str, expected: str) -> None:
        symbol = SymbolName(name)
        assert symbol.parent == expected

    def test_parents(self) -> None:
        symbol = SymbolName("foo.bar.baz")
        assert list(symbol.parents) == ["foo.bar", "foo", ""]

    def test_sort(self) -> None:
        names = [
            "foo.bar",
            "foo.spammy",
            "foo",
            "foo.spam",
            "foo.spammy.ham",
            "foobar.foo",
        ]
        symbols = [SymbolName(name) for name in names]
        assert sorted(symbols) == [
            "foo",
            "foo.bar",
            "foo.spam",
            "foo.spammy",
            "foo.spammy.ham",
            "foobar.foo",
        ]
