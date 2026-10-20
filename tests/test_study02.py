"""Synthetic boundaries and data-optional full Study 02 reproduction."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import duckdb
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies/02-planning"
spec = importlib.util.spec_from_file_location("study02", STUDY / "build.py")
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


def test_placeholders_are_not_substantive_and_null_is_not_empty():
    assert study.brief_sections(None) == []
    assert study.brief_sections("")[0]["state"] == "empty"
    text = (
        "🎬 Production\nSchedule, locations, crew, and logistics.\n"
        "🎨 Visuals\nReferences, mood, color palette, and creative direction.\n"
        "Use blue light.\n🚀 Status\n"
    )
    regions = study.brief_sections(text)
    assert [r["state"] for r in regions] == [
        "empty",
        "template_only",
        "mixed_candidate",
        "empty",
    ]
    assert regions[2]["characters"] == len(
        text[regions[2]["start"] : regions[2]["end"]]
    )
    assert study.FOLDER_SCENE.search("S07: Kitchen")
    assert not study.FOLDER_SCENE.search("Scenesetter")


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (None, "unavailable"),
        ("", "empty_document"),
        ("{", "invalid_json"),
        ("{}", "absent"),
        ('{"multi_shots":null}', "null"),
        ('{"multi_shots":false}', "false"),
        ('{"multi_shots":true}', "true"),
        ('{"multi_shots":"true"}', "other_value"),
        ('{"multi_shots":1}', "other_value"),
    ],
)
def test_controls_preserve_states(raw, expected):
    assert study.controls(raw) == expected


def test_crosswalk_and_asset_producers_use_compound_keys():
    db = duckdb.connect()
    db.execute("CREATE TABLE eligible(film_id VARCHAR)")
    db.execute("INSERT INTO eligible VALUES ('a'), ('b')")
    db.execute("""CREATE TABLE generations(film_id VARCHAR, generation_id VARCHAR,
        prompt_source_path VARCHAR, prompt VARCHAR)""")
    db.execute("""INSERT INTO generations VALUES
        ('a','same','params.prompt','Shot 1'),
        ('b','same','params.prompt',NULL)""")
    db.execute("""CREATE TABLE generation_prompts(film_id VARCHAR,
        generation_id VARCHAR, field_path VARCHAR,
        prompt_role VARCHAR, text VARCHAR)""")
    db.execute("""INSERT INTO generation_prompts VALUES
        ('a','same','params.prompt','primary','Shot 1'),
        ('a','same','params.multi_prompt[0].prompt','prompt_or_text',''),
        ('b','same','params.extra','prompt_or_text','other')""")
    db.execute("""CREATE TABLE assets(film_id VARCHAR, asset_id VARCHAR,
        generation_id VARCHAR)""")
    db.execute("INSERT INTO assets VALUES ('a','asset','producer-a')")
    db.execute("""CREATE TABLE asset_usages(film_id VARCHAR, generation_id VARCHAR,
        asset_id VARCHAR, asset_role VARCHAR, parameter_path VARCHAR,
        reference_element_id VARCHAR)""")
    db.execute("""INSERT INTO asset_usages VALUES
        ('a','same','asset','input_image','params.image',NULL),
        ('b','same','asset','input_image','params.image',NULL)""")
    db.execute((STUDY / "measures.sql").read_text())
    assert db.sql("SELECT count(*) FROM fields").fetchone()[0] == 4
    assert db.sql("SELECT count(*) FROM fields WHERE text IS NULL").fetchone()[0] == 1
    assert db.sql("SELECT count(*) FROM fields WHERE text=''").fetchone()[0] == 1
    assert db.sql("SELECT producer FROM usage_edges ORDER BY film_id").fetchall() == [
        ("producer-a",),
        (None,),
    ]
    db.close()


def test_equal_film_and_pooled_denominators_and_missing_labels():
    frame = pd.DataFrame(
        [
            dict(
                film_id="small",
                generation_type=None,
                jobs=10,
                multi_shot_jobs=9,
                prompt_nonempty=10,
            ),
            dict(
                film_id="large",
                generation_type=None,
                jobs=90,
                multi_shot_jobs=0,
                prompt_nonempty=90,
            ),
        ]
    )
    # The production aggregate requests additional measures; supply measured zeros.
    for c in [
        "sectioned_jobs",
        "reference_token_jobs",
        "multi_true",
        "multi_false_with_text",
    ]:
        frame[c] = 0
    result = study.aggregate(frame, ["generation_type"])
    row = result.query("dimension=='all' and metric=='multi_shot_jobs'").iloc[0]
    assert row.equal_film_mean == pytest.approx(0.45)
    assert row.pooled_share == pytest.approx(0.09)
    assert row.denominator == 100 and row.measured_films == 2
    assert result.query("dimension=='generation_type'").value.isna().all()


def test_manifest_and_panel_contract():
    manifest = json.loads((STUDY / "outputs/reproduction.json").read_text())
    for name, expected in manifest["inputs"].items():
        assert study.digest(ROOT / name) == expected, name
    for name, expected in manifest["outputs"].items():
        path = STUDY / "outputs" / name
        assert study.digest(path) == expected, name
        assert path.stat().st_size < 1_000_000
    maps = json.loads((STUDY / "outputs/panel_maps.json").read_text())
    assert len(maps) == 16 and len({m["film_id"] for m in maps}) == 16
    for record in maps:
        for link in record["links"]:
            assert link["film_id"] == record["film_id"]
            for key in [
                "evidence_label",
                "confidence_rationale",
                "denominator",
                "competing_explanation",
                "entity_ids",
                "source_path",
            ]:
                assert link[key]


def test_build_reproduces_committed_outputs(tmp_path):
    data = ROOT / "data"
    if not (data / "SHA256SUMS").is_file():
        pytest.skip("Fetch verified snapshot to run Study 02 reproduction")
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
