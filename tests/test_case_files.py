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
        row_counts={"generations": 2, "generation_prompts": 3, "asset_usages": 2},
        reading_register=[dict(generation_id="job", reasons=["model coverage"])],
        field_states={
            "generations": {"prompt": dict(unavailable=1, empty=0, nonempty=1)}
        },
        generations={"model_identifier": [dict(value="example", count=2)]},
        prompt_states=dict(unavailable=1, empty=0, nonempty=1, distinct_nonempty=1),
        text_roles=[dict(value="primary", count=3)],
        usage_roles=[dict(value="output", count=2)],
        parameter_controls=[dict(model="example", path="duration", value="5", count=2)],
        invalid_parameters=[],
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


@pytest.mark.parametrize(
    "mutation", ["prompt", "distinct", "text_role", "usage_role", "control", "compound"]
)
def test_rejects_measure_denominator_or_compound_key_mismatch(mutation):
    profile, rows, edges = scope_fixture()
    if mutation == "prompt":
        profile["prompt_states"]["empty"] = 1
    elif mutation == "distinct":
        profile["prompt_states"]["distinct_nonempty"] = 2
    elif mutation == "text_role":
        profile["text_roles"][0]["count"] = 2
    elif mutation == "usage_role":
        profile["usage_roles"][0]["count"] = 3
    elif mutation == "control":
        profile["parameter_controls"][0]["count"] = 1
    else:
        rows[0]["entity_ids"] += "; other-film/asset:example"
    with pytest.raises(ValueError):
        case_check.validate_profile(profile, rows, edges)


def registration_fixture():
    title = "Invented title "
    counts = dict(generations=2, folders=3, reference_elements=4)
    return (
        [dict(title=title)],
        dict(title=title, row_counts=counts),
        dict(title=title, **{k: str(v) for k, v in counts.items()}),
    )


def test_preserves_literal_registered_title():
    case_check.validate_registration(*registration_fixture())


@pytest.mark.parametrize(
    "mutation", ["row_title", "profile_title", "jobs", "folders", "references"]
)
def test_rejects_registration_mismatch(mutation):
    rows, profile, registered = registration_fixture()
    if mutation == "row_title":
        rows[0]["title"] = rows[0]["title"].strip()
    elif mutation == "profile_title":
        profile["title"] = profile["title"].strip()
    else:
        field = {
            "jobs": "generations",
            "folders": "folders",
            "references": "reference_elements",
        }[mutation]
        profile["row_counts"][field] += 1
    with pytest.raises(ValueError):
        case_check.validate_registration(rows, profile, registered)


def test_all_four_batches_required():
    panel = {f"film-{i}": {"batch": str(i)} for i in range(1, 5)}
    case_check.validate_completed(set(panel), panel)
    with pytest.raises(ValueError, match="Completed batches"):
        case_check.validate_completed(set(panel) - {"film-4"}, panel)
    with pytest.raises(ValueError, match="Completed batches"):
        case_check.validate_completed(set(panel) | {"unregistered"}, panel)


def test_exhaustive_reading_policy_needs_all_jobs():
    profile, rows, edges = scope_fixture()
    profile["reading_policy"] = "all_job_contexts"
    with pytest.raises(ValueError, match="Exhaustive reading"):
        case_check.validate_profile(profile, rows, edges)


def test_invalid_parameters_preserve_valid_control_denominator():
    profile, rows, edges = scope_fixture()
    profile["invalid_parameters"] = ["unparseable-job"]
    profile["invalid_parameters_by_model"] = [dict(value="example", count=1)]
    profile["parameter_controls"][0]["count"] = 1
    case_check.validate_profile(profile, rows, edges)
    profile["parameter_controls"][0]["count"] = 2
    with pytest.raises(ValueError, match="Control distribution"):
        case_check.validate_profile(profile, rows, edges)
    profile["invalid_parameters_by_model"][0]["count"] = 0
    with pytest.raises(ValueError, match="Invalid parameter model counts"):
        case_check.validate_profile(profile, rows, edges)
