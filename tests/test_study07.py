"""Synthetic graph boundaries, committed hashes and optional source reproduction."""

import csv
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import duckdb
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies/07-lineage"
spec = importlib.util.spec_from_file_location("study07", STUDY / "build.py")
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


def job(key):
    return dict(generation_id=key, generation_type="image", model_identifier="model")


def asset(key, producer=None, metadata=None):
    return dict(
        asset_id=key,
        generation_id=producer,
        asset_type="image",
        metadata_json=metadata,
        source_asset_id=None,
    )


def usage(key, consumer, role="input_image", path="params.medias[0].data", ref=None):
    return dict(
        asset_id=key,
        generation_id=consumer,
        asset_role=role,
        parameter_path=path,
        reference_element_id=ref,
    )


def test_typed_graph_deduplicates_consumers_and_retains_disconnected_nodes():
    g = study.graph(
        [job(k) for k in ["parent", "a", "b", "detached"]],
        [asset("source", "parent", '{"raw":{},"min":{}}'), asset("unused")],
        [
            usage("source", "a", ref="element"),
            usage("source", "a", "input_asset", "params.input_images[0]"),
            usage("source", "b"),
            usage("style", "a", "input_asset", "params.style"),
        ],
        [
            dict(
                reference_element_id="element",
                metadata_json='{"medias":[{"id":"source"}]}',
            )
        ],
    )
    assert g["media"]["source"] == {"a", "b"}
    assert "style" not in g["media"]
    assert g["raw"]["style"] == {"a"}
    assert g["adjacency"]["parent"] == {"a", "b"}
    assert ("generation", "detached") in g["nodes"]
    assert ("asset", "unused") in g["nodes"]
    assert len(g["nodes"]) == 8
    assert {e[4] for e in g["edges"]} >= {
        "produces",
        "media_input",
        "preset_input",
        "reference_binding",
        "groups_media",
    }
    assert g["missing_assets"] == {"style"}
    # Two representations remain one asset without comparing content or URLs.
    assert sum(k == "asset" for k, _ in g["nodes"]) == 3


def test_unknown_conflicting_self_producers_never_invent_lineage():
    g = study.graph(
        [job(k) for k in ["a", "b", "c"]],
        [asset("ambiguous", "a"), asset("self", "c")],
        [
            usage("ambiguous", "b", "output"),
            usage("ambiguous", "c"),
            usage("external", "c"),
            usage("self", "c"),
        ],
        [],
    )
    assert g["producers"]["ambiguous"] == {"a", "b"}
    assert "ambiguous" not in g["resolved"]
    assert not g["parents"]
    assert g["self_inputs"] == {("self", "c")}
    assert ("asset", "external") in g["nodes"]
    assert study.binding_kind("input_asset", None) == "unknown"
    assert (
        study.binding_kind("input_asset", "params.multi_prompt[2].preset") == "preset"
    )
    assert study.binding_kind("input_asset", "params.input_video") == "media"
    assert study.parse(None) == ("unavailable", None)
    assert study.parse("") == ("empty", None)
    assert study.parse("{")[0] == "invalid"
    assert study.parse("null")[0] == "nonobject"


def test_review_closure_diamond_cycle_and_isolation():
    adj = {"a": {"b", "c"}, "b": {"d"}, "c": {"d"}, "d": {"b"}}
    assert study.reachable(adj, ["a"]) == {"b", "c", "d"}
    assert study.reachable(adj, ["b"]) == {"d"}
    assert study.reachable(adj, ["missing"]) == set()
    assert study.cyclic_nodes(adj, {"a", "b", "c", "d", "isolated"}) == {"b", "d"}
    sizes, isolated = study.components({"a", "b", "c"}, [("a", "b")])
    assert sizes == [2, 1]
    assert isolated == ["c"]


def test_sql_prevents_cross_film_collision():
    db = duckdb.connect()
    for table, schema in {
        "eligible": "film_id VARCHAR",
        "generations": "film_id VARCHAR,generation_id VARCHAR",
        "assets": "film_id VARCHAR,asset_id VARCHAR,generation_id VARCHAR",
        "asset_usages": "film_id VARCHAR,generation_id VARCHAR,asset_id VARCHAR",
        "reference_elements": "film_id VARCHAR,reference_element_id VARCHAR",
    }.items():
        db.execute(f"CREATE TABLE {table}({schema})")
    db.execute("INSERT INTO eligible VALUES ('a')")
    db.execute("INSERT INTO generations VALUES ('a','same'),('b','same')")
    db.execute("INSERT INTO asset_usages VALUES ('a','same','x'),('b','same','x')")
    db.execute("INSERT INTO assets VALUES ('b','x','same')")
    db.execute((STUDY / "measures.sql").read_text())
    assert db.sql("SELECT * FROM bindings").fetchall() == [("a", "same", "x")]
    assert db.sql("SELECT * FROM film_assets").fetchall() == []
    db.close()


def test_film_first_weights_and_unavailable_denominators():
    f = pd.DataFrame(
        [
            dict(
                film_id="a",
                jobs=10,
                chained_jobs=9,
                media_input_assets=0,
                reused_media_assets=0,
            ),
            dict(
                film_id="b",
                jobs=90,
                chained_jobs=0,
                media_input_assets=0,
                reused_media_assets=0,
            ),
        ]
    )
    a = study.aggregate(f, []).set_index("metric")
    assert a.loc["chained_jobs", "equal_film_mean"] == pytest.approx(0.45)
    assert a.loc["chained_jobs", "pooled_share"] == pytest.approx(0.09)
    assert a.loc["reused_media_assets", "measured_films"] == 0
    assert pd.isna(a.loc["reused_media_assets", "pooled_share"])


def test_committed_provenance_and_panel_contract():
    manifest = json.loads((STUDY / "outputs/reproduction.json").read_text())
    for path, expected in manifest["inputs"].items():
        assert study.digest(ROOT / path) == expected, path
    for path, expected in manifest["outputs"].items():
        assert study.digest(STUDY / "outputs" / path) == expected, path
        assert (STUDY / "outputs" / path).stat().st_size < 1_000_000
    maps = json.loads((STUDY / "outputs/panel_maps.json").read_text())
    assert len(maps) == 16
    assert sum(m["review"] is not None for m in maps) == 13
    with (STUDY / "outputs/case_evidence.csv").open(newline="") as f:
        cases = list(csv.DictReader(f))
    assert sum(r["code_id"].startswith("07.") for r in cases) == 80
    assert len(study.read_csv(STUDY / "outputs/film_metrics.csv")) == 157
    policy = json.loads((STUDY / "invalidation_policy.json").read_text())
    assert policy["evidence_label"] == "proposed"


def test_build_reproduces_committed_outputs(tmp_path):
    if not (ROOT / "data/SHA256SUMS").is_file():
        pytest.skip("Fetch verified snapshot to run Study 07 reproduction")
    subprocess.run(
        [
            sys.executable,
            str(STUDY / "build.py"),
            "--data",
            str(ROOT / "data"),
            "--output",
            str(tmp_path / "small"),
            "--large-output",
            str(tmp_path / "large"),
            "--check",
        ],
        cwd=ROOT,
        check=True,
    )
