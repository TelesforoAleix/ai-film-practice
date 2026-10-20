"""Synthetic boundary checks and optional reproduction over fetched data."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import duckdb
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "studies/10-organisation"
spec = importlib.util.spec_from_file_location("study10_build", STUDY / "build.py")
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


def test_owner_requires_explicit_boolean_and_unknown_stays_unknown():
    assert study.owners(None) is None
    assert study.owners("") is None
    assert study.owners("{bad") is None
    assert study.owners("[]") is None
    assert study.owners('[{"id":"account","is_owner":"true"}]') is None
    assert study.owners('[{"id":"account","is_owner":true}]') == {"account"}
    assert study.ratio(0, 0) is None


def test_compound_edges_occurrences_and_unknown_states():
    db = duckdb.connect()
    db.execute("SET TimeZone='UTC'")
    db.execute("CREATE TABLE eligible(film_id VARCHAR,cohort_group VARCHAR)")
    db.execute("INSERT INTO eligible VALUES ('f1','both'),('f2','both')")
    db.execute("""CREATE TABLE generations(film_id VARCHAR,generation_id VARCHAR,
      author_user_id VARCHAR,created_at VARCHAR,prompt VARCHAR)""")
    db.executemany(
        "INSERT INTO generations VALUES (?,?,?,?,?)",
        [
            ("f1", "p", "a", "2026-01-01T23:00:00Z", "same"),
            ("f1", "c", "b", "2026-01-02T01:00:00Z", "same"),
            ("f1", "z", None, None, ""),
            ("f1", "u", "", "invalid", None),
            ("f2", "p", "x", "2026-01-01T23:00:00Z", "same"),
            ("f2", "c", "x", "2026-01-01T23:00:00Z", "same"),
        ],
    )
    db.execute(
        "CREATE TABLE assets(film_id VARCHAR,asset_id VARCHAR,generation_id VARCHAR)"
    )
    db.execute("INSERT INTO assets VALUES ('f1','asset','p'),('f2','asset','p')")
    db.execute("""CREATE TABLE asset_usages(film_id VARCHAR,generation_id VARCHAR,
      asset_id VARCHAR,asset_role VARCHAR)""")
    db.execute("""INSERT INTO asset_usages VALUES
      ('f1','c','asset','input_image'),('f1','c','asset','reference_image'),
      ('f2','c','asset','reference_image'),('f1','p','asset','output')""")
    db.execute("""CREATE TABLE generation_folders(film_id VARCHAR,
      generation_id VARCHAR,folder_id VARCHAR)""")
    db.execute("""INSERT INTO generation_folders VALUES
      ('f1','p','one'),('f1','p','two'),('f1','c','three'),
      ('f2','p','one'),('f2','c','one')""")
    db.execute("CREATE TABLE folders(film_id VARCHAR,folder_id VARCHAR)")
    db.execute("INSERT INTO folders VALUES ('f1','one'),('f1','two'),('f1','three')")
    db.execute(
        "CREATE TABLE asset_folders(film_id VARCHAR,asset_id VARCHAR,folder_id VARCHAR)"
    )
    db.execute(
        "INSERT INTO asset_folders VALUES ('f1','asset','one'),('f1','asset','two')"
    )
    db.execute("CREATE TABLE reference_elements(film_id VARCHAR)")
    db.execute(
        "CREATE TABLE films(film_id VARCHAR,title VARCHAR,"
        "creator VARCHAR,duration VARCHAR)"
    )
    db.execute(
        "INSERT INTO films VALUES ('f1','Invented','creator','120'),"
        "('f2','Other','creator','')"
    )
    db.execute((STUDY / "measures.sql").read_text())
    rows = db.sql(
        "SELECT * EXCLUDE(film_id_1) FROM film_measures ORDER BY film_id"
    ).df()
    first, second = rows.iloc[0], rows.iloc[1]
    assert first.jobs == 4 and first.authored == 2 and first.dated == 2
    assert first.prompt_empty == first.prompt_unavailable == 1
    assert first.prompt_nonempty == 2 and first.repeat_excess == 1
    assert first.active_utc_dates == 2
    assert first.event_span_days == pytest.approx(2 / 24)
    assert first.generation_placements == 3 and first.multiply_placed_jobs == 1
    assert first.asset_placements == 2 and first.placed_assets == 1
    assert first.multiply_placed_assets == 1
    assert first.resolved_job_pairs == first.cross_author_pairs == 1
    assert first.distinct_input_pairs == first.input_assets == 1
    assert first.reused_input_assets == 0
    assert first.disjoint_folder_pairs == 1 and second.disjoint_folder_pairs == 0
    assert second.cross_author_pairs == 0 and second.resolved_job_pairs == 1
    assert db.sql("SELECT count(*) FROM edges").fetchone()[0] == 2
    db.close()


def test_build_reproduces_committed_outputs(tmp_path):
    """Run explicitly after fetching; regular CI remains independent of network/data."""
    data = ROOT / "data"
    if not (data / "SHA256SUMS").is_file():
        pytest.skip(
            "Fetch verified snapshot to enable Study 10 integration reproduction"
        )
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


def test_committed_outputs_and_build_inputs_match_manifest():
    manifest = json.loads((STUDY / "outputs/reproduction.json").read_text())
    for name, expected in manifest["outputs"].items():
        path = STUDY / "outputs" / name
        assert study.digest(path) == expected, name
        assert path.stat().st_size < 1_000_000
    for name, expected in manifest["inputs"].items():
        assert study.digest(ROOT / name) == expected, name


def test_film_weights_and_unresolved_pair_denominators():
    rows = []
    for fid, jobs, repeat, pairs in [("small", 10, 0, 0), ("large", 90, 81, 20)]:
        rows.append(
            dict(
                film_id=fid,
                cohort_group="both",
                record_orientation="mixed",
                scale="small",
                organisation_proxy="flat",
                jobs=jobs,
                repeat_excess=repeat,
                prompt_nonempty=jobs,
                multiply_placed_jobs=0,
                reused_input_assets=0,
                input_assets=1,
                cross_author_pairs=pairs,
                authored_job_pairs=pairs,
                disjoint_folder_pairs=0,
                placed_job_pairs=pairs,
                owner_jobs=jobs,
                owner_comparable_jobs=jobs,
                folders=2,
                event_span_days=1,
                active_utc_dates=1,
            )
        )
    summaries = study.summaries(pd.DataFrame(rows)).query("dimension=='all'")
    repeats = summaries[summaries.metric == "repeat_share"].iloc[0]
    assert repeats.equal_film_mean == pytest.approx(0.45)
    assert repeats.pooled_share == pytest.approx(0.81)
    cross = summaries[summaries.metric == "cross_author_share"].iloc[0]
    assert cross.measured_films == 1 and cross.denominator == 20
    assert cross.equal_film_mean == 1
