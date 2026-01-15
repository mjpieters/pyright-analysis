import pathlib
from datetime import datetime
from typing import Any

import pytest
from pydantic import BaseModel
from syrupy.assertion import SnapshotAssertion
from syrupy.matchers import path_type

from pyright_analysis.schema import PyrightJsonResults


@pytest.fixture
def pyright_results(pyright_json_report: str) -> PyrightJsonResults:
    return PyrightJsonResults.model_validate_json(pyright_json_report)


@pytest.fixture
def pyright_json_report() -> str:
    return r"""
{
    "version": "1.1.391",
    "time": "1735043053980",
    "generalDiagnostics": [],
    "summary": {
        "filesAnalyzed": 376,
        "errorCount": 0,
        "warningCount": 0,
        "informationCount": 0,
        "timeInSec": 5.506
    },
    "typeCompleteness": {
        "packageName": "foobar",
        "moduleName": "foobar",
        "ignoreUnknownTypesFromImports": true,
        "exportedSymbolCounts": {
            "withKnownType": 9794,
            "withAmbiguousType": 852,
            "withUnknownType": 1599
        },
        "otherSymbolCounts": {
            "withKnownType": 90,
            "withAmbiguousType": 3,
            "withUnknownType": 16
        },
        "missingFunctionDocStringCount": 1087,
        "missingClassDocStringCount": 327,
        "missingDefaultParamCount": 0,
        "completenessScore": 0.7998366680277664,
        "modules": [
            {"name": "foobar"},
            {"name": "foobar.ham"},
            {"name": "foobar.spam"},            
            {"name": "foobar.spam.vikings"}
        ],
        "symbols": [
            {
                "category": "module",
                "name": "foobar.ham",
                "referenceCount": 1,
                "isExported": true,
                "isTypeKnown": true,
                "isTypeAmbiguous": false,
                "diagnostics": []
            },
            {
                "category": "class",
                "name": "foobar.MontyPython",
                "referenceCount": 1,
                "isExported": true,
                "isTypeKnown": false,
                "isTypeAmbiguous": false,
                "diagnostics": []
            },
            {
                "category": "function",
                "name": "foobar._private_function",
                "referenceCount": 1,
                "isExported": false,
                "isTypeKnown": false,
                "isTypeAmbiguous": false,
                "diagnostics": []
            },
            {
                "category": "method",
                "name": "foobar.MontyPython.__init__",
                "referenceCount": 1,
                "isExported": true,
                "isTypeKnown": false,
                "isTypeAmbiguous": false,
                "diagnostics": [
                    {
                        "file": "/.../foobar/__init__.py",
                        "severity": "error",
                        "message": "Type of parameter \"first_name\" is partially unknown\nParameter type is \"type[NameString]\"",
                        "range": {
                            "start": {
                                "line": 180,
                                "character": 8
                            },
                            "end": {
                                "line": 180,
                                "character": 16
                            }
                        }
                    },
                    {
                        "file": "/.../foobar/__init__.py",
                        "severity": "error",
                        "message": "Type of parameter \"last_name\" is partially unknown\n\u00a0\u00a0Parameter type is \"type[NameString]\"",
                        "range": {
                            "start": {
                                "line": 180,
                                "character": 8
                            },
                            "end": {
                                "line": 180,
                                "character": 16
                            }
                        }
                    }
                ]
            }
        ]
    }
}
"""


@pytest.fixture
def snapshot_pydantic(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    # Convert Pydantic models to their dict representation, with
    # pathlib values converted to posix path strings, and datetime objects
    # converted to their ISO 8601 representation.
    def replacer(
        data: BaseModel | pathlib.Path | datetime, _: Any
    ) -> dict[str, Any] | str:
        match data:
            case BaseModel():
                return data.model_dump()
            case pathlib.Path():
                return data.as_posix()
            case datetime():
                return data.isoformat()

    matcher = path_type(types=(BaseModel, pathlib.Path, datetime), replacer=replacer)
    return snapshot.with_defaults(matcher=matcher)
