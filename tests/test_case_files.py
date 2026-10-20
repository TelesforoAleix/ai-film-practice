"""Synthetic assignment-contract tests; no released records or prompts."""

import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "case_check", Path(__file__).resolve().parents[1] / "case-files/check.py"
)
case_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(case_check)


def fixture():
    definitions = [dict(code_id="99.1", study="99", values="example")]
    row = {k: "synthetic evidence" for k in case_check.EVIDENCE}
    row.update(
        code_id="99.1",
        study="99",
        later_study="99",
        value="example",
        status="coded",
        codebook_version="1.0",
        evidence_label="observed",
    )
    return [row], definitions


def test_valid_assignment():
    rows, definitions = fixture()
    case_check.validate(rows, definitions, "1.0")


def test_committed_case_contract():
    # Validate production artifacts, without copying records into test fixtures.
    # The source release and ignored data directory are not opened.
    case_check.main()


@pytest.mark.parametrize(
    "mutation",
    ["missing", "duplicate", "state", "version", "evidence", "value", "study"],
)
def test_rejects_invalid_assignment(mutation):
    rows, definitions = fixture()
    if mutation == "missing":
        rows = []
    elif mutation == "duplicate":
        rows = rows * 2
    else:
        key, value = {
            "state": ("status", "absent"),
            "version": ("codebook_version", "0.1"),
            "evidence": ("excerpt", ""),
            "value": ("value", "invented"),
            "study": ("study", "98"),
        }[mutation]
        rows[0][key] = value
    with pytest.raises(ValueError):
        case_check.validate(rows, definitions, "1.0")


def test_unknown_is_not_empty_value():
    rows, definitions = fixture()
    rows[0].update(status="unknown", value=r"\N")
    case_check.validate(rows, definitions, "1.0")
    rows[0]["value"] = ""
    with pytest.raises(ValueError):
        case_check.validate(rows, definitions, "1.0")
