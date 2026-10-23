"""Synthetic iteration boundaries and complete release-backed reproduction."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import duckdb
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies/09-iteration"
spec = importlib.util.spec_from_file_location("study09", STUDY / "build.py")
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


def job(
    gid,
    text="keep the shape",
    model="still",
    typ="image",
    batch=None,
    raw="{}",
    date="2026-01-01T00:00:00Z",
):
    return dict(
        generation_id=gid,
        prompt=text,
        model_identifier=model,
        generation_type=typ,
        generation_batch_id=batch,
        parameters_json=raw,
        created_at=date,
    )


def usage(gid, asset, role="input_image", path="params.medias[0].data", ref=None):
    return dict(
        generation_id=gid,
        asset_id=asset,
        asset_role=role,
        parameter_path=path,
        reference_element_id=ref,
    )


def asset(aid, producer=None):
    return dict(asset_id=aid, generation_id=producer, asset_type="image")


def test_overlapping_groups_do_not_transitively_merge_or_invent_versions():
    ctx, graph, groups, flags = study.analyse(
        [job("a"), job("b"), job("c"), job("d")],
        [asset("x"), asset("y")],
        [
            usage("a", "x"),
            usage("b", "x"),
            usage("b", "y"),
            usage("c", "y"),
            usage("d", "preset", "input_asset", "params.style"),
        ],
        [],
    )
    assert groups["shared_asset"] == [("x", ["a", "b"]), ("y", ["b", "c"])]
    assert groups["input_set"] == groups["lineage"] == []
    assert not any(f["rerun_candidate"] for f in flags.values())
    assert flags["b"]["shared_asset_member"] == 1
    assert flags["d"]["supported_member"] == 0
    assert study.comparison_pairs("shared_asset", groups["shared_asset"], ctx) == []
    assert not graph["parents"]


def test_input_set_reruns_controls_and_unknown_text_are_distinct():
    ctx, _, groups, flags = study.analyse(
        [
            job("a", raw='{"seed":1,"is_inpaint":false}'),
            job("b", raw='{"seed":2,"is_inpaint":false}'),
            job("c", text=None),
            job("d", text=""),
            job("e", model=None),
        ],
        [],
        [usage(g, "x") for g in "abcde"] + [usage("b", "x", "reference_image")],
        [],
    )
    assert len(groups["input_set"]) == 1
    assert flags["a"]["rerun_candidate"] == flags["b"]["rerun_candidate"] == 1
    assert (
        flags["c"]["rerun_candidate"]
        == flags["d"]["rerun_candidate"]
        == flags["e"]["rerun_candidate"]
        == 0
    )
    delta = study.delta(ctx["a"], ctx["b"])
    assert (
        delta["text_equal"]
        == delta["controls_changed"]
        == delta["role_bindings_changed"]
        == 1
    )
    assert delta["inputs_changed"] == 0
    assert study.delta(ctx["c"], ctx["d"])["text_comparable"] == 0
    assert study.delta(ctx["a"], ctx["e"])["model_changed"] == 0
    assert (
        study.raw_selected_controls('{"is_inpaint":false}')["is_inpaint"]["raw_value"]
        is False
    )
    assert (
        study.raw_selected_controls('{"is_inpaint":null}')["is_inpaint"]["state"]
        == "null"
    )
    assert study.raw_selected_controls("{}")["is_inpaint"]["state"] == "absent"
    assert study.raw_selected_controls("broken")["is_inpaint"]["state"] == "invalid"


def test_lineage_adoption_deduplicates_channels_and_excludes_conflicts_self():
    _, _, groups, flags = study.analyse(
        [job("a"), job("b"), job("c")],
        [asset("known", "a"), asset("conflict", "a"), asset("self", "b")],
        [
            usage("b", "known"),
            usage("b", "known", "reference_image"),
            usage("c", "conflict", "output"),
            usage("b", "conflict"),
            usage("b", "self"),
        ],
        [],
    )
    assert groups["lineage"] == [("a:b", ["a", "b"])]
    assert flags["a"]["adopted"] == 1
    assert flags["b"]["adopted"] == flags["c"]["adopted"] == 0
    assert all("approved" not in v for v in flags.values())


def test_deltas_do_not_infer_specificity_or_semantic_replacement():
    ctx, _, _, _ = study.analyse(
        [job("a", "red red cup"), job("b", "preserve the blue cup", model="other")],
        [],
        [usage("a", "old"), usage("b", "new")],
        [],
    )
    d = study.delta(ctx["a"], ctx["b"])
    for key in [
        "token_addition",
        "token_deletion",
        "longer_text",
        "preservation_added",
        "input_replacement_candidate",
        "model_changed",
    ]:
        assert d[key] == 1
    assert "specificity" not in d and "direction_change" not in d
    assert study.controls('{"prompt":"one","medias":[],"seed":0}')[1] == {"seed": 0}
    assert study.controls('{"prompt":"two","medias":[1],"seed":0}')[1] == {"seed": 0}


def test_batch_requires_actual_members_and_similarity_is_candidate_only():
    text = "one two three four five six seven eight nine ten eleven twelve"
    jobs = [
        job("a", text, batch="same"),
        job("b", text, batch="same", date="2026-01-01T23:59:59Z"),
        job("c", text, batch="singleton", date="2026-01-03T00:00:00Z"),
        job("d", text, model=None),
    ]
    ctx, _, groups, flags = study.analyse(jobs, [], [], [])
    assert groups["batch"] == [("same", ["a", "b"])]
    assert groups["similarity_time"] == [("a:b", ["a", "b"])]
    assert flags["a"]["similarity_time_member"] == 1
    assert flags["c"]["supported_member"] == flags["d"]["supported_member"] == 0
    assert study.comparison_pairs("batch", groups["batch"], ctx) == [("a", "b")]


def test_film_first_and_undefined_denominator():
    frame = pd.DataFrame(
        [
            dict(film_id="a", yes=9, jobs=10, missing=0),
            dict(film_id="b", yes=0, jobs=90, missing=0),
        ]
    )
    out = study.summarize(frame, [("yes", "jobs"), ("yes", "missing")])
    assert out.iloc[0].equal_film_mean == pytest.approx(0.45)
    assert out.iloc[0].pooled_share == pytest.approx(0.09)
    assert out.iloc[1].measured_films == 0
    assert pd.isna(out.iloc[1].pooled_share)


def test_sql_keeps_film_scope_on_repeated_entity_ids():
    with duckdb.connect() as db:
        for table, columns in {
            "eligible": "film_id VARCHAR",
            "generations": "film_id VARCHAR,generation_id VARCHAR",
            "assets": "film_id VARCHAR,asset_id VARCHAR,generation_id VARCHAR",
            "asset_usages": "film_id VARCHAR,generation_id VARCHAR,asset_id VARCHAR",
            "reference_elements": "film_id VARCHAR,reference_element_id VARCHAR",
        }.items():
            db.execute(f"CREATE TABLE {table}({columns})")
        db.execute("INSERT INTO eligible VALUES ('one')")
        db.execute("INSERT INTO generations VALUES ('one','same'),('two','same')")
        db.execute(
            "INSERT INTO asset_usages VALUES ('one','same','x'),('two','same','x')"
        )
        db.execute("INSERT INTO assets VALUES ('two','x','same')")
        db.execute((STUDY / "measures.sql").read_text())
        assert db.sql("SELECT * FROM bindings").fetchall() == [("one", "same", "x")]
        assert db.sql("SELECT * FROM film_assets").fetchall() == []


def test_artifact_contract_and_hashes():
    manifest = json.loads((STUDY / "outputs/reproduction.json").read_text())
    for name, expected in manifest["inputs"].items():
        assert study.digest(ROOT / name) == expected, name
    for name, expected in manifest["outputs"].items():
        path = STUDY / "outputs" / name
        assert study.digest(path) == expected, name
        assert path.stat().st_size < 1_000_000
    film = study.read(STUDY / "outputs/film_metrics.csv")
    assert len(film) == 157 and film.jobs.sum() == 130704
    assert (
        film.prompt_nonempty + film.prompt_empty + film.prompt_unavailable == film.jobs
    ).all()
    assert len(study.read(STUDY / "outputs/case_evidence.csv")) == 64
    checks = study.read(STUDY / "outputs/structural_check.csv")
    assert (checks.matches == checks.upstream_matches).all()
    proposal = json.loads((STUDY / "review_states.json").read_text())
    assert proposal["evidence_label"] == "proposed"
    assert "approved" in proposal["candidate_state"]


def test_build_reproduces_committed_outputs(tmp_path):
    if not (ROOT / "data/SHA256SUMS").is_file():
        pytest.skip("Fetch verified release to run Study 09 integration reproduction")
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
