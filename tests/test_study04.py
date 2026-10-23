"""Synthetic weighting, source-channel boundaries and optional full reproduction."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import duckdb
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies/04-prompts"
spec = importlib.util.spec_from_file_location("study04", STUDY / "build.py")
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


def test_weighting_keeps_failures_unknown_and_zero_coverage_visible():
    candidates = pd.DataFrame(
        [
            dict(film_id="a", generation_type=t, text_role="primary", text_id=str(i))
            for t, n in [("image", 8), ("video", 2), ("audio", 3)]
            for i in range(n)
        ]
    )
    sample = pd.DataFrame(
        [
            dict(
                film_id="a",
                generation_type=t,
                text_role="primary",
                text_id=str(i),
                success=ok,
            )
            for t, i, ok in [
                ("image", 0, True),
                ("image", 1, False),
                ("video", 0, True),
            ]
        ]
    )
    weighted, strata = study.weight_sample(sample, candidates)
    assert weighted.success_weight.tolist() == [8, 8, 2]
    assert weighted.sample_weight.tolist() == [4, 4, 2]
    audio = strata[strata.generation_type == "audio"].iloc[0]
    assert audio.candidate_texts == 3 and audio.sampled == 0
    assert pd.isna(audio.success_weight)
    # Weighting successes speaks only for covered strata, never missing strata.
    assert weighted.loc[weighted.success, "success_weight"].sum() == 10
    assert strata.candidate_texts.sum() == 13


def test_withheld_positive_is_not_absence_or_failed_label():
    base = dict(
        film_id="a",
        generation_id="g",
        generation_type="image",
        text_role="primary",
        text_id="t",
        field_path="p",
        model_identifier="m",
        status="success",
    )
    base["labels"] = {
        c: dict(present=True, span=None, span_withheld="full_source_field")
        for c in study.COMPONENTS
    }
    failed = {**base, "text_id": "u", "status": "failure", "labels": None}
    result = study.label_rows([base, failed])
    assert result.iloc[0].preservation == 1
    assert pd.isna(result.iloc[1].preservation)
    assert not result.iloc[1].success


def test_film_means_and_zero_denominator():
    f = pd.DataFrame(
        [dict(film_id="a", n=1, d=2, z=0), dict(film_id="b", n=0, d=18, z=0)]
    )
    result = study.summarize(f, [("n", "d"), ("n", "z")])
    assert result.iloc[0].equal_film_mean == 0.25
    assert result.iloc[0].pooled_share == 0.05
    assert result.iloc[1].measured_films == 0
    assert pd.isna(result.iloc[1].pooled_share)


def test_raw_controls_and_text_states():
    assert study.state(None) == "unavailable"
    assert study.state("") == "empty"
    assert study.controls("broken")["document_state"] == "invalid"
    assert study.controls(None)["document_state"] == "unavailable"
    c = study.controls('{"duration":0,"multi_shots":false,"model":null}')
    assert c["duration"]["value"] == 0
    assert c["multi_shots"]["value"] is False
    assert c["model"]["state"] == "null"
    assert c["resolution"]["state"] == "absent"


def test_sql_deduplicates_primary_and_keeps_compound_input_metadata_scope():
    with duckdb.connect() as db:
        for table, columns in {
            "eligible": "film_id VARCHAR",
            "generations": (
                "film_id VARCHAR,generation_id VARCHAR,"
                "prompt_source_path VARCHAR,prompt VARCHAR"
            ),
            "generation_prompts": (
                "film_id VARCHAR,generation_id VARCHAR,"
                "field_path VARCHAR,prompt_role VARCHAR,text VARCHAR"
            ),
            "asset_usages": (
                "film_id VARCHAR,generation_id VARCHAR,asset_id VARCHAR,"
                "asset_role VARCHAR,parameter_path VARCHAR,"
                "reference_element_id VARCHAR"
            ),
            "reference_elements": (
                "film_id VARCHAR,reference_element_id VARCHAR,description VARCHAR"
            ),
        }.items():
            db.execute(f"CREATE TABLE {table} ({columns})")
        db.execute("INSERT INTO eligible VALUES ('a')")
        db.execute(
            "INSERT INTO generations VALUES "
            "('a','same','params.prompt',NULL),"
            "('b','same','params.prompt','other')"
        )
        db.execute(
            "INSERT INTO generation_prompts VALUES "
            "('a','same','params.prompt','prompt_or_text',NULL),"
            "('a','same','params.negative_prompt','negative',''),"
            "('a','same','params.multi_prompt[0].prompt','prompt_or_text','move'),"
            "('a','same','params.prompt_language','prompt_or_text','en')"
        )
        db.execute(
            "INSERT INTO asset_usages VALUES "
            "('a','same','x','input_image','params.medias[0].data','ref'),"
            "('a','same','x','reference_image','params.refs[0]','ref'),"
            "('a','same','lens','input_asset','params.lens',NULL),"
            "('b','same','y','input_image','params.medias[0].data','ref')"
        )
        db.execute("INSERT INTO reference_elements VALUES ('b','ref','unrelated')")
        db.execute((STUDY / "measures.sql").read_text())
        assert db.sql(
            "SELECT text_role,text FROM text_fields ORDER BY text_role"
        ).fetchall() == [
            ("negative", ""),
            ("other_text", "en"),
            ("primary", None),
            ("shot_prompt", "move"),
        ]
        assert db.sql(
            'SELECT media_inputs,"references",metadata_descriptions FROM context_counts'
        ).fetchall() == [(1, 1, 0)]


def test_committed_artifact_integrity():
    manifest = json.loads((STUDY / "outputs/reproduction.json").read_text())
    for name, sha in manifest["inputs"].items():
        assert study.digest(ROOT / name) == sha, name
    for name, sha in manifest["outputs"].items():
        assert study.digest(STUDY / "outputs" / name) == sha, name
        assert (STUDY / "outputs" / name).stat().st_size < 1_000_000
    assert len(study.read(STUDY / "outputs/film_metrics.csv")) == 157
    assert len(study.read(STUDY / "outputs/case_evidence.csv")) == 96
    assert len(study.read(STUDY / "dependencies.csv")) == 35
    contract = json.loads((STUDY / "context_contract.json").read_text())
    assert contract["evidence_label"] == "proposed"
    assert len(contract["layers"]) == 7


def test_build_reproduces_committed_outputs(tmp_path):
    paths = [ROOT / "data", ROOT / "data/af11-labels-v1", ROOT / "data/af11-labels-v2"]
    if not all((p / "SHA256SUMS").is_file() for p in paths):
        pytest.skip("Fetch snapshot and both label releases for Study 04 reproduction")
    subprocess.run(
        [
            sys.executable,
            str(STUDY / "build.py"),
            "--data",
            str(paths[0]),
            "--v1",
            str(paths[1]),
            "--v2",
            str(paths[2]),
            "--output",
            str(tmp_path),
            "--check",
        ],
        cwd=ROOT,
        check=True,
    )
