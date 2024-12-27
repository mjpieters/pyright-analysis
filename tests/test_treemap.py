import pytest
from syrupy.assertion import SnapshotAssertion

from pyright_analysis.schema import (
    PyrightJsonResults,
    Symbol,
    SymbolCategory,
    SymbolName,
)
from pyright_analysis.treemap import ModuleInfo, to_treemap


@pytest.fixture
def symbol() -> Symbol:
    return Symbol.model_validate_json("""
{
    "category": "class",
    "name": "foobar.MontyPython",
    "referenceCount": 1,
    "isExported": true,
    "isTypeKnown": false,
    "isTypeAmbiguous": false,
    "diagnostics": []
}
""")


class TestModuleInfo:
    def test_add_symbol_name(self):
        mi = ModuleInfo(
            SymbolName("foo.bar"), exported=42, known=12, ambiguous=10, unknown=20
        )

        # not known and not ambiguous == unknown increments
        unknown_symbol = Symbol(
            category=SymbolCategory.class_,
            name=SymbolName("foo.bar.baz.Viking"),
            reference_count=1,
            is_exported=True,
            is_type_known=False,
            is_type_ambiguous=False,
        )
        with_unknown = mi + unknown_symbol
        assert with_unknown == ModuleInfo(
            mi.parent, exported=43, known=12, ambiguous=10, unknown=21
        )

        ambiguous_symbol = unknown_symbol.model_copy(update={"is_type_ambiguous": True})
        with_ambiguous = mi + ambiguous_symbol
        assert with_ambiguous == ModuleInfo(
            mi.parent, exported=43, known=12, ambiguous=11, unknown=20
        )

        known_symbol = unknown_symbol.model_copy(
            update={"is_type_ambiguous": False, "is_type_known": True}
        )
        with_known = mi + known_symbol
        assert with_known == ModuleInfo(
            mi.parent, exported=43, known=13, ambiguous=10, unknown=20
        )

    def test_add_module_info(self) -> None:
        base = ModuleInfo(
            SymbolName("foo.bar"), exported=17, known=5, ambiguous=1, unknown=11
        )
        other = ModuleInfo(
            SymbolName("foo.bar.baz"), exported=11, known=7, ambiguous=3, unknown=1
        )

        assert (base + other) == ModuleInfo(
            base.parent, exported=28, known=12, ambiguous=4, unknown=12
        )

    @pytest.mark.parametrize(
        "known,exported,expected", ((42, 117, 0.358974358974359), (42, 0, 1))
    )
    def test_completeness_score(
        self, known: int, exported: int, expected: float
    ) -> None:
        mi = ModuleInfo(SymbolName("foo.bar"), exported=exported, known=known)
        assert mi.completeness_score == pytest.approx(expected)


def test_to_treemap(
    pyright_results: PyrightJsonResults, snapshot: SnapshotAssertion
) -> None:
    figure = to_treemap(pyright_results.type_completeness)
    assert figure.to_json(pretty=True) == snapshot
