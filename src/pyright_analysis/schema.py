from collections.abc import Iterator
from enum import StrEnum, auto
from pathlib import Path
from typing import Annotated, Any, Self, TypedDict

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, GetCoreSchemaHandler
from pydantic.types import AwareDatetime
from pydantic_core import core_schema


def _mixed_case(identifier: str) -> str:
    first, *parts = identifier.split("_")
    return first + "".join([p.capitalize() for p in parts])


class SymbolName(str):
    @property
    def parent(self) -> Self:
        return next(self.parents)

    @property
    def parents(self) -> Iterator[Self]:
        *parts, _ = self.split(".")
        while parts:
            yield self.__class__(".".join(parts))
            parts.pop()
        yield self.__class__("")

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, SymbolName):
            return NotImplemented
        return self.split(".") < other.split(".")

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate, core_schema.str_schema()
        )

    @classmethod
    def validate(cls, input_value: str) -> "SymbolName":
        return cls(input_value)


class SymbolCategory(StrEnum):
    class_ = "class"
    function = auto()
    method = auto()
    constant = auto()
    variable = auto()
    module = auto()
    type_alias = "type alias"
    type_var = "type variable"
    indeterminate = "symbol"


class SeverityLevel(StrEnum):
    error = auto()
    warning = auto()
    information = auto()


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=_mixed_case, populate_by_name=True)


class Position(_Base):
    line: int
    character: int


class Range(_Base):
    start: Position
    end: Position


class Diagnostic(_Base):
    file: Path
    severity: SeverityLevel
    message: str
    range: Range | None = None
    rule: str | None = None


class Symbol(_Base):
    category: SymbolCategory
    name: SymbolName
    reference_count: int
    is_exported: bool
    is_type_known: bool
    is_type_ambiguous: bool
    diagnostics: list[Diagnostic] = Field(default_factory=list)
    alternate_names: list[str] | None = None


class SymbolCounts(_Base):
    with_known_type: int
    with_ambiguous_type: int
    with_unknown_type: int


class _NamedModule(TypedDict):
    name: str


def _unwrap_named_module(value: _NamedModule) -> str:
    return value["name"]


class TypeCompletenessReport(_Base):
    package_name: str
    package_root_directory: Path | None = None
    module_name: SymbolName
    module_root_directory: Path | None = None
    ignore_unknown_types_from_imports: bool
    py_typed_path: Path | None = None
    exported_symbol_counts: SymbolCounts
    other_symbol_counts: SymbolCounts
    missing_function_doc_string_count: int
    missing_class_doc_string_count: int
    missing_default_param_count: int
    completeness_score: float
    modules: list[Annotated[SymbolName, BeforeValidator(_unwrap_named_module)]]
    symbols: list[Symbol]


class ProcessSummary(_Base):
    files_analyzed: int
    error_count: int
    warning_count: int
    information_count: int
    time_in_sec: float


class PyrightJsonResults(_Base):
    version: str
    time: AwareDatetime
    general_diagnostics: list[Diagnostic]
    summary: ProcessSummary
    type_completeness: TypeCompletenessReport
