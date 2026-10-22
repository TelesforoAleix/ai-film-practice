"""Synthetic workflow boundaries, artifact integrity and optional reproduction."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import duckdb
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies/08-workflow"
spec = importlib.util.spec_from_file_location("study08", STUDY / "build.py")
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


def job(key, model="model", kind="image"):
    return dict(generation_id=key, generation_type=kind, model_identifier=model)


def asset(key, producer=None):
    return dict(
        asset_id=key,
        generation_id=producer,
        asset_type="image",
        metadata_json=None,
        source_asset_id=None,
    )


def usage(
    asset_id, consumer, role="input_image", path="params.medias[0].data", ref=None
):
    return dict(
        asset_id=asset_id,
        generation_id=consumer,
        asset_role=role,
        parameter_path=path,
        reference_element_id=ref,
    )


def test_branches_stages_and_models_require_real_media_edges():
    jobs = [
        job("a", "still"),
        job("b", "still"),
        job("c", "motion", "video"),
        job("d", "unused_model", "video"),
    ]
    flags, pairs, triples, _ = study.motifs(
        jobs,
        [asset("first", "a"), asset("second", "b")],
        [
            usage("first", "b"),
            usage("first", "b", "input_asset", "params.input_images[0]"),
            usage("second", "c", ref="element"),
            usage("first", "c"),
            usage("preset", "d", "input_asset", "params.style"),
        ],
        [],
    )
    assert pairs == {("a", "b"), ("a", "c"), ("b", "c")}
    assert len(triples) == 3
    assert flags["b"]["shared_input"] == 1
    assert flags["b"]["cross_model"] == 0
    assert flags["c"]["cross_model"] == 1
    assert flags["c"]["convergent"] == flags["c"]["staged_refinement"] == 1
    assert flags["a"]["image_foundation"] == flags["b"]["image_foundation"] == 1
    assert flags["b"]["reference_preparation"] == 1
    assert flags["d"]["no_recorded_media"] == 1
    assert flags["d"]["cross_model"] == flags["d"]["chained"] == 0


def test_conflicting_self_external_and_unavailable_model_are_not_handoffs():
    flags, pairs, _, _ = study.motifs(
        [job("a", None), job("b", "motion", "video"), job("c")],
        [asset("uncertain", "a"), asset("known", "a"), asset("self", "b")],
        [
            usage("uncertain", "c", "output"),
            usage("uncertain", "b"),
            usage("known", "b"),
            usage("self", "b"),
            usage("external", "b"),
        ],
        [],
    )
    assert pairs == {("a", "b")}
    assert flags["b"]["chained"] == 1
    assert flags["b"]["cross_model"] == 0
    assert flags["b"]["media_bound"] == 1
    assert flags["a"]["no_recorded_media"] == 1


def test_declared_adapter_role_is_not_generation_type_or_output_success():
    flags, _, _, _ = study.motifs(
        [
            job("edit", "cinematic_video_editor", None),
            job("voice", "voice_change_merge", "video"),
            job("audio", "text2speech_v2", "audio"),
            job("other", "unseen", "video"),
        ],
        [],
        [],
        [],
    )
    assert flags["edit"]["finishing_job"] == 1
    assert flags["edit"]["video_candidate"] == 0
    assert flags["voice"]["voice_adapter"] == 1
    assert flags["voice"]["audio_job"] == flags["voice"]["video_candidate"] == 0
    assert flags["audio"]["audio_job"] == flags["audio"]["voice_adapter"] == 1
    assert flags["other"]["video_candidate"] == 1
    assert all("approved" not in f for f in flags.values())


def test_film_first_weights_and_zero_denominator():
    frame = pd.DataFrame(
        [
            dict(film_id="a", jobs=10, positive=9, missing=0),
            dict(film_id="b", jobs=90, positive=0, missing=0),
        ]
    )
    result = study.summarize(frame, [("positive", "jobs"), ("positive", "missing")])
    assert result.iloc[0].equal_film_mean == pytest.approx(0.45)
    assert result.iloc[0].pooled_share == pytest.approx(0.09)
    assert result.iloc[1].measured_films == 0
    assert pd.isna(result.iloc[1].pooled_share)
    assert result.iloc[0].film_ids == "a;b"


def test_sql_keeps_film_identity_and_cooccurrence_separate():
    with duckdb.connect() as db:
        for table, columns in {
            "eligible": "film_id VARCHAR",
            "generations": (
                "film_id VARCHAR,generation_id VARCHAR,model_identifier VARCHAR"
            ),
            "assets": "film_id VARCHAR,asset_id VARCHAR,generation_id VARCHAR",
            "asset_usages": "film_id VARCHAR,generation_id VARCHAR,asset_id VARCHAR",
            "reference_elements": "film_id VARCHAR,reference_element_id VARCHAR",
        }.items():
            db.execute(f"CREATE TABLE {table}({columns})")
        db.execute("INSERT INTO eligible VALUES ('a')")
        db.execute(
            "INSERT INTO generations VALUES "
            "('a','same','one'),('a','next','two'),('b','same','three')"
        )
        db.execute(
            "INSERT INTO asset_usages VALUES "
            "('a','same','source'),('b','same','source')"
        )
        db.execute("INSERT INTO assets VALUES ('b','source','same')")
        db.execute((STUDY / "measures.sql").read_text())
        assert db.sql("SELECT * FROM bindings").fetchall() == [("a", "same", "source")]
        assert db.sql("SELECT * FROM film_assets").fetchall() == []
        assert db.sql("SELECT * FROM cooccurrence").fetchall() == [("a", "one", "two")]


def test_committed_contract_and_hashes():
    manifest = json.loads((STUDY / "outputs/reproduction.json").read_text())
    for path, expected in manifest["inputs"].items():
        assert study.digest(ROOT / path) == expected, path
    for path, expected in manifest["outputs"].items():
        assert study.digest(STUDY / "outputs" / path) == expected, path
        assert (STUDY / "outputs" / path).stat().st_size < 1_000_000
    film = study.read(STUDY / "outputs/film_metrics.csv")
    assert len(film) == 157
    assert (film.media_bound + film.no_recorded_media == film.jobs).all()
    assert len(study.read(STUDY / "outputs/case_evidence.csv")) == 80
    assert (
        len(study.read(STUDY / "outputs/panel_role_matrix.csv").film_id.unique()) == 16
    )
    checks = study.read(STUDY / "outputs/structural_check.csv")
    assert (checks.matches == checks.upstream_matches).all()
    nodes = json.loads((STUDY / "node_contracts.json").read_text())
    assert nodes["evidence_label"] == "proposed"
    assert len(nodes["nodes"]) == 5


def test_build_reproduces_committed_outputs(tmp_path):
    if not (ROOT / "data/SHA256SUMS").is_file():
        pytest.skip("Fetch verified snapshot to run Study 08 reproduction")
    subprocess.run(
        [
            sys.executable,
            str(STUDY / "build.py"),
            "--data",
            str(ROOT / "data"),
            "--output",
            str(tmp_path),
            "--check",
        ],
        cwd=ROOT,
        check=True,
    )
