"Synthetic checks for Study 01 typing and evidence availability boundaries."

import importlib
import json
from pathlib import Path

import duckdb
import pandas as pd

STUDY = Path(__file__).resolve().parents[1] / "studies" / "01-corpus"


def test_dictionary_json_is_table_specific_and_invalid_is_not_repaired(
    tmp_path, monkeypatch
):
    monkeypatch.syspath_prepend(str(STUDY))
    build = importlib.import_module("build")
    typed = importlib.import_module("typed")
    monkeypatch.setattr(build, "TABLES", ("films", "reference_elements", "generations"))
    db = duckdb.connect()
    db.execute(
        "CREATE TABLE films(film_id VARCHAR, category VARCHAR, duration VARCHAR)"
    )
    db.execute(
        "INSERT INTO films VALUES ('f1','[]',''),('f2',NULL,'bad'),('f3','','12.5')"
    )
    db.execute(
        "CREATE TABLE reference_elements(film_id "
        "VARCHAR,reference_element_id VARCHAR,category VARCHAR)"
    )
    db.execute("INSERT INTO reference_elements VALUES ('f1','r1','character')")
    db.execute(
        "CREATE TABLE generations(film_id VARCHAR,generation_id "
        "VARCHAR,parameters_json VARCHAR)"
    )
    db.executemany(
        "INSERT INTO generations VALUES (?,?,?)",
        [
            ("f1", "g1", '{"medias":[{"value":null},{"value":""}]}'),
            ("f2", "g1", "{invalid}"),
            ("f3", "g2", None),
        ],
    )
    build.dictionary(db, tmp_path)
    frame = pd.read_csv(tmp_path / "dictionary.csv")
    assert (
        frame.query("table=='reference_elements' and column=='category'")
        .iloc[0]
        .derived_type
        == "VARCHAR"
    )
    assert (
        frame.query("table=='generations' and column=='parameters_json'")
        .iloc[0]
        .invalid_casts
        == 1
    )
    grains = json.loads((tmp_path / "grains.json").read_text())
    assert grains[2]["rows"] == grains[2]["distinct_candidate_keys"] == 3
    paths = pd.read_csv(tmp_path / "json_paths.csv", keep_default_na=False)
    assert set(paths.query("path=='$.medias[*].value'").json_type) == {"null", "string"}
    typed.add_typed_views(db, tmp_path / "dictionary.csv")
    assert db.execute("SELECT duration FROM films ORDER BY film_id").fetchall() == [
        ("",),
        ("bad",),
        ("12.5",),
    ]
    assert db.execute(
        "SELECT duration,duration__empty,duration__invalid FROM "
        "typed_films ORDER BY film_id"
    ).fetchall() == [(None, True, False), (None, False, True), (12.5, False, False)]
    assert db.execute(
        "SELECT parameters_json,parameters_json__invalid FROM "
        "typed_generations WHERE film_id='f2'"
    ).fetchone() == (None, True)
    assert (
        db.execute(
            "SELECT parameters_json FROM generations WHERE film_id='f2'"
        ).fetchone()[0]
        == "{invalid}"
    )
    db.close()


def test_unavailable_workspace_does_not_become_empty(monkeypatch):
    monkeypatch.syspath_prepend(str(STUDY))
    build = importlib.import_module("build")
    assert build.state(0, 0, 0, accessible=False) == "unavailable"
    assert build.state(0, 0, 0, accessible=True) == "empty"
    assert build.state(0, 0, 5, accessible=True) == "unavailable"
    assert build.state(0, 2, 5, accessible=True) == "empty"
