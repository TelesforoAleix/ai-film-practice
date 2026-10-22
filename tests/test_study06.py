"""Synthetic video-route boundaries and optional full-source reproduction."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import duckdb
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies/06-video"
spec = importlib.util.spec_from_file_location("study06", STUDY / "build.py")
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


def test_route_evidence_and_orthogonal_controls():
    def route(
        obj=None,
        images=0,
        videos=0,
        audio=0,
        start=False,
        end=False,
        unknown=0,
        text="A subject moves.",
    ):
        return study.classify(obj, images, videos, audio, start, end, unknown, text)

    assert route() == "unknown"
    assert route({}) == "unknown"
    assert route({"medias": []}) == "text_candidate"
    assert route({"mode": "text-to-video"}) == "text_to_video"
    assert route({"mode": "text-to-video"}, audio=1) == "unknown"
    assert route({"medias": []}, text="") == "unknown"
    assert route({"medias": []}, unknown=1) == "unknown"
    assert route({"medias": [], "input_video": "unresolved"}) == "unknown"
    assert route({"multi_shots": True}, images=1) == "image_guided"
    assert route({"multi_shots": False}, images=1) == "image_guided"
    assert route({}, images=2, start=True, end=True) == "start_end"
    assert route({}, images=2, start=True) == "image_guided"
    assert route({}, images=2, end=True) == "image_guided"
    assert route({}, images=2, videos=1) == "video_guided"
    assert route({"model": "video_extension"}, videos=1) == "extension"
    assert route({"model": "video_extension"}) == "unknown"
    assert route({"model": "video_edit"}, videos=1) == "video_guided"


def test_control_states_preserve_types_and_false():
    assert study.control_state(None, "duration", "invalid") == (
        "invalid_document",
        None,
    )
    assert study.parse(None) == ("unavailable", None)
    assert study.parse("") == ("empty", None)
    assert study.parse("{") == ("invalid", None)
    assert study.parse("[]") == ("nonobject", None)
    assert study.state(None, "duration") == ("unavailable", None)
    assert study.state({}, "duration") == ("absent", None)
    assert study.state({"duration": None}, "duration") == ("null", None)
    assert study.state({"duration": 0}, "duration") == ("int", "0")
    assert study.state({"duration": "0"}, "duration") == ("str", '"0"')
    assert study.state({"multi_shots": False}, "multi_shots") == ("bool", "false")
    assert study.state({"model_version": ""}, "model_version") == ("empty_string", '""')


def test_compound_bindings_presets_and_duplicate_channels():
    db = duckdb.connect()
    db.execute("CREATE TABLE eligible(film_id VARCHAR)")
    db.execute("INSERT INTO eligible VALUES ('a'),('b')")
    db.execute(
        "CREATE TABLE generations(film_id VARCHAR,generation_id VARCHAR,"
        "generation_type VARCHAR)"
    )
    db.execute("""INSERT INTO generations VALUES
        ('a','still','image'),('a','clip','video'),('b','clip','video'),
        ('a','prior','video')""")
    db.execute(
        "CREATE TABLE assets(film_id VARCHAR,asset_id VARCHAR,generation_id VARCHAR)"
    )
    db.execute("INSERT INTO assets VALUES ('a','frame','still'),('a','v','prior')")
    db.execute(
        "CREATE TABLE asset_usages(film_id VARCHAR,generation_id VARCHAR,"
        "asset_id VARCHAR,asset_role VARCHAR,parameter_path VARCHAR,"
        "reference_element_id VARCHAR)"
    )
    db.execute("""INSERT INTO asset_usages VALUES
        ('a','clip','frame','input_start_image','params.medias[0].data',NULL),
        ('a','clip','frame','reference_image','params.reference_elements[0]',NULL),
        ('a','clip','end','input_end_image','params.medias[1].data',NULL),
        ('a','clip','v','input_asset','params.input_video',NULL),
        ('a','clip','v','input_video','params.medias[2].data',NULL),
        ('a','clip','snd','input_asset','params.input_audio',NULL),
        ('a','clip','lens','input_asset','params.camera_lens',NULL),
        ('a','clip','pace','input_asset','params.pacing',NULL),
        ('a','clip','preset','input_asset','params.multi_prompt[0].preset',NULL),
        ('b','clip','frame','input_image','params.medias[0].data',NULL)""")
    db.execute((STUDY / "measures.sql").read_text())
    assert db.sql(
        "SELECT film_id,generation_id,image_inputs,video_inputs,audio_inputs,"
        "has_start,has_end,image_parents,video_parents,unknown_inputs "
        "FROM video_jobs WHERE generation_id='clip' ORDER BY ALL"
    ).fetchall() == [
        ("a", "clip", 2, 1, 1, True, True, 1, 1, 0),
        ("b", "clip", 1, 0, 0, False, False, 0, 0, 0),
    ]
    assert db.sql("SELECT producer FROM attachments WHERE film_id='b'").fetchone() == (
        None,
    )
    db.close()


def test_film_weights_and_undefined_rates():
    frame = pd.DataFrame(
        [
            dict(film_id="a", jobs=10, matches=9, text=0),
            dict(film_id="b", jobs=90, matches=0, text=0),
        ]
    )
    result = study.aggregate(frame, [("matches", "jobs"), ("matches", "text")], [])
    assert result.iloc[0].equal_film_mean == pytest.approx(0.45)
    assert result.iloc[0].pooled_share == pytest.approx(0.09)
    assert result.iloc[1].measured_films == 0
    assert pd.isna(result.iloc[1].pooled_share)


def test_committed_provenance_and_specification():
    manifest = json.loads((STUDY / "outputs/reproduction.json").read_text())
    for path, expected in manifest["inputs"].items():
        assert study.digest(ROOT / path) == expected, path
    for path, expected in manifest["outputs"].items():
        assert study.digest(STUDY / "outputs" / path) == expected, path
        assert (STUDY / "outputs" / path).stat().st_size < 1_000_000
    node = json.loads((STUDY / "video_node.json").read_text())
    assert node["evidence_label"] == "proposed"
    assert len(node["revision_routes"]) == 6
    cases = study.read_csv(STUDY / "outputs/case_evidence.csv")
    assert len(cases) == 16 * 7
    film = study.read_csv(STUDY / "outputs/film_metrics.csv")
    route_columns = ["route_" + r for r in study.ROUTES]
    assert (film[route_columns].sum(axis=1) == film.jobs).all()
    assert (
        film.prompt_nonempty + film.prompt_empty + film.prompt_unavailable == film.jobs
    ).all()


def test_build_reproduces_committed_outputs(tmp_path):
    if not (ROOT / "data/SHA256SUMS").is_file():
        pytest.skip("Fetch verified snapshot to run Study 06 reproduction")
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
