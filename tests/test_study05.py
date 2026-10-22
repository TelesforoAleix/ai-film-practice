"""Synthetic image-route boundaries and data-optional full reproduction."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import duckdb
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies/05-image"
spec = importlib.util.spec_from_file_location("study05", STUDY / "build.py")
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


def test_request_does_not_create_mechanism_and_missing_is_not_empty():
    assert study.classify(None, 0, 0, "unknown") == "unknown"
    assert study.classify({}, 0, 0, "unknown") == "unknown"
    assert study.classify({"input_images": []}, 0, 0, "unknown") == "fresh_candidate"
    assert study.classify({"input_images": []}, 0, 1, "unknown") == "unknown"
    assert (
        study.classify(
            {"input_images": [], "input_image": {"id": "unresolved"}}, 0, 0, "unknown"
        )
        == "unknown"
    )
    assert (
        study.classify(
            {"prompt": "replace the sign", "is_inpaint": False}, 2, 0, "unknown"
        )
        == "multi_input"
    )
    assert study.classify({"is_inpaint": True}, 1, 0, "unknown") == "local_edit"
    assert study.parse("{")[0] == "invalid"
    assert study.parse("")[0] == "empty"
    assert study.parse(None)[0] == "unavailable"
    assert study.state({}, "is_inpaint") == ("absent", None)
    assert study.state({"is_inpaint": None}, "is_inpaint") == ("null", None)
    assert study.state({"is_inpaint": False}, "is_inpaint") == ("bool", "false")
    assert study.mechanisms(
        {"prompt": "use a mask", "layers": [], "nested": {"mask": None}}
    ) == [
        ("$.layers", "empty_list", None, False),
        ("$.nested.mask", "null", None, False),
    ]


def test_upscale_and_reframe_need_model_scoped_controls():
    assert (
        study.classify({"width": 640, "output_width": 640}, 1, 0, "topaz_image")
        == "reference_guided"
    )
    assert (
        study.classify({"width": 640, "output_width": 1280}, 1, 0, "topaz_image")
        == "upscale"
    )
    assert (
        study.classify({"width": 640, "output_width": 1280}, 0, 0, "topaz_image")
        == "unknown"
    )
    assert (
        study.classify({"rotate_degree": 0}, 1, 0, "qwen_camera_control")
        == "reference_guided"
    )
    assert (
        study.classify({"rotate_degree": 90}, 1, 0, "qwen_camera_control") == "reframe"
    )
    assert study.classify({"expand_left": 50}, 1, 0, "flux_2_pro_outpaint") == "reframe"


def test_compound_edges_presets_and_duplicate_channels():
    db = duckdb.connect()
    db.execute("CREATE TABLE eligible(film_id VARCHAR)")
    db.execute("INSERT INTO eligible VALUES ('a'),('b')")
    db.execute(
        "CREATE TABLE generations(film_id VARCHAR,generation_id VARCHAR,"
        "generation_type VARCHAR)"
    )
    db.execute(
        "INSERT INTO generations VALUES ('a','parent','image'),('a','child','image'),"
        "('b','child','image'),('a','clip','video')"
    )
    db.execute(
        "CREATE TABLE assets(film_id VARCHAR,asset_id VARCHAR,"
        "generation_id VARCHAR,asset_type VARCHAR)"
    )
    db.execute("INSERT INTO assets VALUES ('a','source','parent','image')")
    db.execute(
        "CREATE TABLE asset_usages(film_id VARCHAR,generation_id VARCHAR,"
        "asset_id VARCHAR,asset_role VARCHAR,parameter_path VARCHAR,"
        "reference_element_id VARCHAR)"
    )
    db.execute("""INSERT INTO asset_usages VALUES
        ('a','child','source','input_asset','params.input_images[0]',NULL),
        ('a','child','source','reference_image','params.reference_elements[0]',NULL),
        ('a','child','lens','input_asset','params.camera_lens',NULL),
        ('a','child','style','input_asset','params.style',NULL),
        ('b','child','source','input_image','params.medias[0].data',NULL),
        ('a','clip','source','input_start_image','params.start_image',NULL)""")
    db.execute((STUDY / "measures.sql").read_text())
    assert db.sql(
        "SELECT film_id,generation_id,image_inputs,other_inputs,"
        "image_parents,video_consumer FROM image_jobs ORDER BY ALL"
    ).fetchall() == [
        ("a", "child", 1, 0, 1, False),
        ("a", "parent", 0, 0, 0, True),
        ("b", "child", 1, 0, 0, False),
    ]
    assert db.sql("SELECT producer FROM attachments WHERE film_id='b'").fetchone() == (
        None,
    )
    db.close()


def test_weights_and_unavailable_denominator():
    frame = pd.DataFrame(
        [
            dict(film_id="a", jobs=10, edits=9, text=0),
            dict(film_id="b", jobs=90, edits=0, text=0),
        ]
    )
    result = study.aggregate(frame, [("edits", "jobs"), ("edits", "text")], [])
    assert result.iloc[0].equal_film_mean == pytest.approx(0.45)
    assert result.iloc[0].pooled_share == pytest.approx(0.09)
    assert pd.isna(result.iloc[1].pooled_share)
    assert result.iloc[1].measured_films == 0


def test_committed_provenance_and_contracts():
    manifest = json.loads((STUDY / "outputs/reproduction.json").read_text())
    for path, expected in manifest["inputs"].items():
        assert study.digest(ROOT / path) == expected, path
    for path, expected in manifest["outputs"].items():
        assert study.digest(STUDY / "outputs" / path) == expected, path
        assert (STUDY / "outputs" / path).stat().st_size < 1_000_000
    contracts = json.loads((STUDY / "contracts.json").read_text())
    assert contracts["evidence_label"] == "proposed"
    assert len(contracts["operations"]) == 6
    assert len(study.read_csv(STUDY / "outputs/case_evidence.csv")) == 80


def test_build_reproduces_committed_outputs(tmp_path):
    if not (ROOT / "data/SHA256SUMS").is_file():
        pytest.skip("Fetch verified snapshot to run Study 05 reproduction")
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
