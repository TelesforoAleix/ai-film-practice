"""Synthetic join/state boundaries and data-optional Study 03 reproduction."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import duckdb
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies/03-elements"
spec = importlib.util.spec_from_file_location("study03", STUDY / "build.py")
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


@pytest.mark.parametrize(
    ("raw", "state"),
    [
        (None, "unavailable"),
        ("", "empty_document"),
        ("{", "invalid_json"),
        ("[]", "other_document"),
        ("{}", "absent"),
        ('{"reference_elements": null}', "null"),
        ('{"reference_elements": []}', "empty_array"),
        ('{"reference_elements": [{}]}', "nonempty_array"),
        ('{"reference_elements": false}', "other_value"),
        ('{"reference_elements": ""}', "other_value"),
    ],
)
def test_reference_states_do_not_imply_attachments(raw, state):
    assert study.reference_state(raw) == state
    assert study.field_state(None) == "unavailable"
    assert study.field_state("") == "empty"
    assert study.field_state(" ") == "nonempty"


def test_compound_joins_and_duplicate_usage_channels():
    db = duckdb.connect()
    db.execute("CREATE TABLE eligible(film_id VARCHAR)")
    db.execute("INSERT INTO eligible VALUES ('a'),('b')")
    db.execute("""CREATE TABLE generations(film_id VARCHAR,generation_id VARCHAR)
    """)
    db.execute(
        "INSERT INTO generations VALUES ('a','job'),('a','producer'),('b','job')"
    )
    db.execute("""CREATE TABLE assets(film_id VARCHAR,asset_id VARCHAR,
        generation_id VARCHAR)""")
    db.execute("INSERT INTO assets VALUES ('a','asset','producer')")
    db.execute("""CREATE TABLE reference_elements(film_id VARCHAR,
        reference_element_id VARCHAR,name VARCHAR,category VARCHAR,
        description VARCHAR)""")
    db.execute("""INSERT INTO reference_elements VALUES
        ('a','ref','v2','auto:prop',''),('b','ref','v2','auto:prop',NULL)""")
    db.execute("""CREATE TABLE asset_usages(film_id VARCHAR,generation_id VARCHAR,
        asset_id VARCHAR,reference_element_id VARCHAR,asset_role VARCHAR,
        parameter_path VARCHAR)""")
    db.execute("""INSERT INTO asset_usages VALUES
        ('a','job','asset','ref','reference_image','params.reference_elements[0]'),
        ('a','job','asset',NULL,'input_image','params.media[0]'),
        ('b','job','asset','ref','reference_image','params.reference_elements[0]'),
        ('b','job','other',NULL,'output','output')""")
    db.execute((STUDY / "measures.sql").read_text())
    assert db.sql("SELECT count(*) FROM input_pairs").fetchone()[0] == 2
    assert db.sql("SELECT consumers FROM refs ORDER BY film_id").fetchall() == [
        (1,),
        (1,),
    ]
    assert db.sql(
        "SELECT attached_asset_ids FROM refs ORDER BY film_id"
    ).fetchall() == [
        (1,),
        (1,),
    ]
    assert db.sql("SELECT producer FROM attachments WHERE film_id='b'").fetchone() == (
        None,
    )
    assert db.sql("""SELECT film_id,input_assets,attached_references,resolved_input
        FROM job_channels WHERE generation_id='job' ORDER BY film_id""").fetchall() == [
        ("a", 1, 1, True),
        ("b", 1, 1, False),
    ]
    assert study.checked_edges(db, "b", "producer", "job") == []
    db.close()


def test_weighting_and_zero_denominator_is_undefined():
    frame = pd.DataFrame(
        [
            dict(
                film_id="small",
                cohort="one",
                jobs=10,
                input_jobs=9,
                elements=0,
                used_elements=0,
            ),
            dict(
                film_id="large",
                cohort="one",
                jobs=90,
                input_jobs=0,
                elements=0,
                used_elements=0,
            ),
        ]
    )
    result = study.aggregate(frame, ["cohort"])
    row = result.query("dimension=='all' and metric=='input_jobs'").iloc[0]
    assert row.equal_film_mean == pytest.approx(0.45)
    assert row.pooled_share == pytest.approx(0.09)
    assert row.denominator == 100 and row.measured_films == 2
    row = result.query("dimension=='all' and metric=='used_elements'").iloc[0]
    assert row.denominator == 0 and row.measured_films == 0
    assert pd.isna(row.pooled_share) and pd.isna(row.equal_film_mean)


def test_manifest_and_scoped_output_contract():
    manifest = json.loads((STUDY / "outputs/reproduction.json").read_text())
    for name, expected in manifest["inputs"].items():
        assert study.digest(ROOT / name) == expected, name
    for name, expected in manifest["outputs"].items():
        path = STUDY / "outputs" / name
        assert study.digest(path) == expected, name
        assert path.stat().st_size < 1_000_000
    packages = json.loads((STUDY / "outputs/reference_packages.json").read_text())
    assert len(packages) == 16
    for package in packages:
        assert package["media_content_state"] == "unobservable"
        assert package["fulfillment_state"] == "unknown"
        for context in package["contexts"]:
            assert context["film_id"] == package["evidence"]["film_id"]
    versions = json.loads((STUDY / "outputs/versions.json").read_text())
    assert len(versions) == 6
    for version in versions:
        assert version["relationship"] == "inferred_derivative"
        assert version["approval_state"] == "unknown"
        assert version["edges"] and version["requested_changes"]
    schema = json.loads((STUDY / "schemas.json").read_text())

    # Schema references must resolve; approval must require an actor and event.
    def walk(value):
        if isinstance(value, dict):
            if "$ref" in value:
                assert value["$ref"].split("/")[-1] in schema["$defs"]
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(schema)
    review = schema["$defs"]["review"]["allOf"][0]["then"]["properties"]
    assert review["actor_id"]["minLength"] == 1
    assert review["decision_event_id"]["minLength"] == 1


def test_build_reproduces_committed_outputs(tmp_path):
    data = ROOT / "data"
    if not (data / "SHA256SUMS").is_file():
        pytest.skip("Fetch verified snapshot to run Study 03 reproduction")
    subprocess.run(
        [
            sys.executable,
            str(STUDY / "build.py"),
            "--data",
            str(data),
            "--output",
            str(tmp_path),
            "--check",
        ],
        cwd=ROOT,
        check=True,
    )
