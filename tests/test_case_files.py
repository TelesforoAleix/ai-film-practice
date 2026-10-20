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


def scope_fixture():
    """Entirely invented film, job and field partitions."""
    rows, _ = fixture()
    rows[0].update(film_id="synthetic-film", entity_ids="synthetic-film/generation:job")
    profile = dict(
        film_id="synthetic-film",
        row_counts={"generations": 2},
        reading_register=[dict(generation_id="job", reasons=["model coverage"])],
        field_states={
            "generations": {"prompt": dict(unavailable=1, empty=0, nonempty=1)}
        },
        generations={"model": [dict(value="example", count=2)]},
    )
    edges = dict(film_id="synthetic-film", edges=[])
    return profile, rows, edges


def test_profile_scope_and_partitions():
    case_check.validate_profile(*scope_fixture())


@pytest.mark.parametrize(
    "mutation", ["film", "duplicate", "partition", "scope", "edge"]
)
def test_rejects_inconsistent_scope(mutation):
    profile, rows, edges = scope_fixture()
    if mutation == "film":
        edges["film_id"] = "other-film"
    elif mutation == "duplicate":
        profile["reading_register"] *= 2
    elif mutation == "partition":
        profile["field_states"]["generations"]["prompt"]["empty"] = 1
    elif mutation == "scope":
        rows[0]["entity_ids"] = "synthetic-film/generation:unread-job"
    else:
        edges["edges"] = [dict(producer="job", consumer="job", usages=[])]
    with pytest.raises(ValueError):
        case_check.validate_profile(profile, rows, edges)
