"""AF3b collection/report/release checks using synthetic records only."""

import argparse
import copy
import gzip
import hashlib
import importlib
import json
from pathlib import Path

import duckdb
import pandas as pd
import pytest

from film_practice.prompt_labels import COMPONENTS, digest


@pytest.fixture
def modules(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).parents[1] / "prompt-labels"))
    return importlib.import_module("report"), importlib.import_module("release")


def source(text="A red boat on sand.", film="film-a", generation="same-id"):
    return {
        "text_id": digest(text),
        "film_id": film,
        "generation_id": generation,
        "field_path": "params.prompt",
        "source_table": "generations",
        "source_record_file": "records/public.json",
        "generation_type": "image",
        "text_role": "primary",
        "model_identifier": "image-model",
        "population": "primary",
    }


def labels(**spans):
    return {
        name: {"present": name in spans, "span": spans.get(name)} for name in COMPONENTS
    }


def event(row=None, status="success", attempt=1, **extra):
    return {
        **(row or source()),
        "status": status,
        "attempt": attempt,
        "run_sha256": "run-a",
        "labels_version": "AF3a-v3",
        "labels": labels(subject="boat"),
        "joined_spans": ["subject"],
        "resolved_spans": [],
        "error_type": "ValueError",
        **extra,
    }


def write(path, rows, tail=b""):
    path.write_bytes(b"".join((json.dumps(row) + "\n").encode() for row in rows) + tail)
    return path


def db_factory(*_):
    db = duckdb.connect()
    db.execute(
        "CREATE TABLE primary_source("
        "film_id VARCHAR,generation_id VARCHAR,prompt VARCHAR)"
    )
    db.execute(
        "INSERT INTO primary_source VALUES "
        "('film-a','same-id','A red boat on sand.'), "
        "('film-b','same-id','A dog runs.')"
    )
    db.execute("CREATE VIEW generations AS SELECT * FROM primary_source")
    db.execute(
        "CREATE TABLE nested_source(film_id VARCHAR,generation_id VARCHAR,"
        "field_path VARCHAR,text VARCHAR)"
    )
    db.execute("CREATE VIEW generation_prompts AS SELECT * FROM nested_source")
    return db


def test_torn_tail_retry_and_last_terminal(modules, tmp_path):
    report, _ = modules
    row = source()
    first = event(status="failure")
    latest = event(attempt=2)
    path = write(
        tmp_path / "journal",
        [first, event(status="started", attempt=2), latest],
        b'{"text_id":',
    )
    before = path.read_bytes()
    final, info = report.collect([path], {row["text_id"]: row})
    assert final[row["text_id"]] == latest
    assert info["inputs"][0]["ignored_tail_bytes"] == 11
    assert info["inputs"][0]["sha256"] == hashlib.sha256(before[:-11]).hexdigest()
    assert path.read_bytes() == before
    # An unfinished later attempt cannot erase the last terminal event.
    write(path, [first, event(status="started", attempt=2)])
    final, info = report.collect([path], {row["text_id"]: row})
    assert final[row["text_id"]]["status"] == "failure"
    assert info["pending_attempts"] == {row["text_id"]: 2}


def test_snapshot_newline_only_and_concurrent_append(modules, tmp_path, monkeypatch):
    report, _ = modules
    row = event(confidence_rationale="Synthetic\u2028separator\u0085inside a string")
    path = tmp_path / "journal"
    original = (json.dumps(row, ensure_ascii=False) + "\n").encode()
    path.write_bytes(original)
    old_stat = Path.stat

    def append_after_stat(self, *args, **kwargs):
        result = old_stat(self, *args, **kwargs)
        if self == path:
            with path.open("ab") as stream:
                stream.write(b'{"later":true}\n')
        return result

    monkeypatch.setattr(Path, "stat", append_after_stat)
    rows, info = report.snapshot(path)
    assert rows == [row]
    assert info["consumed_bytes"] == len(original)
    assert path.read_bytes() == original + b'{"later":true}\n'


def test_release_privacy_refuses_without_echo(modules):
    _, release = modules
    candidate = "/" + "/".join(("home", "synthetic", "private-file"))
    with pytest.raises(ValueError) as error:
        release.privacy_check({"span": candidate})
    assert str(error.value) == "private_content_candidate_requires_owner_review"


@pytest.mark.parametrize(
    "change, message",
    [
        ({"run_sha256": "other"}, "mixed_run"),
        ({"labels_version": "other"}, "mixed_run"),
        ({"text_id": "outsider"}, "outside_sample"),
        ({"film_id": "other"}, "metadata_mismatch"),
        ({"attempt": 0}, "invalid_attempt"),
    ],
)
def test_collect_refuses_bad_records(modules, tmp_path, change, message):
    report, _ = modules
    row = source()
    path = write(
        tmp_path / "journal",
        [event(), event(attempt=2, **change)]
        if "attempt" not in change
        else [event(**change)],
    )
    with pytest.raises(ValueError, match=message):
        report.collect([path], {row["text_id"]: row})


def test_duplicate_and_malformed_complete_lines(modules, tmp_path):
    report, _ = modules
    sample = {source()["text_id"]: source()}
    path = write(tmp_path / "one", [event(), event()])
    with pytest.raises(ValueError, match="duplicate_final"):
        report.collect([path], sample)
    write(path, [event()])
    other = write(tmp_path / "two", [event(attempt=2)])
    with pytest.raises(ValueError, match="across_journals"):
        report.collect([path, other], sample)
    write(path, [], b"broken\n")
    with pytest.raises(ValueError, match="malformed_complete"):
        report.collect([path], sample)


def test_exact_span_and_join_checks(modules):
    report, _ = modules
    row = event()
    with db_factory() as db:
        result = report.check_successes(db, {row["text_id"]: row})
        assert result["joined_spans"] == 1
        assert result["positive_spans_denominator"] == 1
        assert result["component_decisions_denominator"] == 14
        for changes, error in [
            ({"labels": labels(subject="not in source")}, "unsupported_span"),
            ({"labels": {}}, "component_keys"),
            ({"resolved_spans": ["subject"]}, "overlapping"),
            ({"joined_spans": ["action"]}, "invalid_span_resolution"),
        ]:
            with pytest.raises(ValueError, match=error):
                report.check_successes(db, {row["text_id"]: {**row, **changes}})
        with pytest.raises(ValueError, match="source_hash_mismatch"):
            report.check_successes(db, {row["text_id"]: {**row, "film_id": "film-b"}})


def test_prevalence_weights_and_missing(modules):
    report, _ = modules
    sample = {
        str(i): {"film_id": "a" if i < 3 else "b" if i == 3 else "c"} for i in range(5)
    }
    predictions = {str(i): {name: i != 3 for name in COMPONENTS} for i in range(4)}
    summary = report.prevalence(sample, predictions)["summary"]
    assert summary["subject"]["per_film_mean"] == 0.5
    assert summary["subject"]["text_weighted"] == {
        "present": 3,
        "denominator": 4,
        "share": 0.75,
    }
    assert summary["subject"]["films_with_success_denominator"] == 2
    assert summary["subject"]["sample_films_denominator"] == 3
    assert summary["overall"]["text_weighted"]["denominator"] == 56
    assert report.prevalence(sample, {})["summary"]["subject"]["per_film_mean"] is None


def test_report_agreement_failures_and_bounds(modules):
    report, _ = modules
    a, b = source(), source("A dog runs.", "film-b")
    sample = {r["text_id"]: r for r in (a, b)}
    final = {a["text_id"]: event(a), b["text_id"]: event(b, status="failure")}
    jev = {
        key: {**r, "status": "success", "presence": {n: False for n in COMPONENTS}}
        for key, r in sample.items()
    }
    gold = {
        a["text_id"]: event(
            a, labels=labels(subject="boat", action="boat"), joined_spans=[]
        )
    }
    gold_run = copy.deepcopy(jev)
    gold_run[a["text_id"]]["presence"]["subject"] = True
    result = report.build_report(
        sample, final, {"pending_attempts": {}}, jev, gold_run, gold, {}, {}
    )
    assert result["coverage"]["failures"] == 1
    assert result["failure_error_types"] == {"ValueError": 1}
    assert (
        result["failure_concentration"]["per_film"]["groups_above_pooled_failure_share"]
        == 1
    )
    bounds = result["failure_sensitivity_bounds"]["subject"]
    assert bounds["if_all_failures_absent"] == 0.5
    assert bounds["if_all_failures_present"] == 1
    pair = result["agreement"]["primary_vs_gold"]
    assert pair["compared_texts"] == 1
    assert pair["micro"]["n"] == 14
    assert pair["disagreements"]["action"] == [a["text_id"]]
    assert pair["gold_reference_metrics"]["per_component"]["action"]["fn"] == 1
    assert (
        result["agreement"]["primary_vs_jev"]["per_component"]["subject"][
            "left_only_present"
        ]
        == 1
    )
    assert result["gold_limits"]["present_counts"]["action"] == 1
    assert result["agreement"]["jev_vs_gold"]["micro"]["both_present"] == 0
    assert result["agreement"]["jev_gold_run_vs_gold"]["micro"]["both_present"] == 1


def structural_files(tmp_path):
    features = tmp_path / "features.parquet"
    occurrences = tmp_path / "occurrences.parquet"
    rows = []
    for key, long in [("short", False), ("long", True), ("pilot", True)]:
        rows.append(
            {
                "text_id": key,
                "characters": 13000 if long else 20,
                "semantic_eligible": not long,
                "structured_json": False,
                "xml_like": False,
                "preservation_matches": int(long),
                "exclusion_matches": 0,
                "camera_matches": 0,
                "lens_matches": 0,
            }
        )
    pd.DataFrame(rows).to_parquet(features)
    pd.DataFrame(
        [
            {
                "text_id": key,
                "film_id": "film",
                "population": pop,
                "generation_type": typ,
                "text_role": "primary",
            }
            for key, pop, typ in [
                ("short", "primary", None),
                ("long", "primary", ""),
                ("long", "primary", ""),
                ("pilot", "supplemental", "image"),
            ]
        ]
    ).to_parquet(occurrences)
    return features, occurrences


def test_long_bias_distinct_primary_null_vs_empty(modules, tmp_path):
    report, _ = modules
    result = report.long_text_bias(*structural_files(tmp_path))
    assert result["primary_text_weighted"]["distinct_texts_denominator"] == 2
    assert result["primary_text_weighted"]["excluded_long_texts"] == 1
    assert len(result["by_stratum"]) == 2
    report.write_json(tmp_path / "bias.json", result)
    read = json.loads((tmp_path / "bias.json").read_text())
    assert {r["generation_type"] for r in read["by_stratum"]} == {None, ""}


def test_path_cleaning_and_full_field_withholding(modules):
    _, release = modules
    # Synthetic POSIX and Windows model locations; no local user identifiers.
    row = event(
        reported_model="/models/cache/qwen.gguf",
        requested_model="local-model",
        base_url="http://127.0.0.1:8080/v1",
        full_text="never export",
    )
    safe = release.clean(row)
    assert safe["reported_model"] == "qwen.gguf"
    assert "base_url" not in safe and "full_text" not in safe
    assert release.filename("Z:\\models\\qwen.gguf") == "qwen.gguf"
    row["labels"] = labels(subject="A red boat on sand.")
    with db_factory() as db:
        safe = release.withhold_full_field_spans(
            {row["text_id"]: row}, {row["text_id"]: source()}, db
        )[0]
    span = safe["labels"]["subject"]
    assert span["present"] is True and span["span"] is None
    assert span["span_withheld"] == "full_source_field"
    assert "A red boat on sand." not in json.dumps(safe)


def fixture_args(tmp_path, modules, monkeypatch):
    report, _ = modules
    monkeypatch.setattr(report, "connect", db_factory)
    a, b = source(), source("A dog runs.", "film-b")
    sample = [a, b]
    sample_path = write(tmp_path / "sample.jsonl", sample)
    gold_path = write(tmp_path / "gold.jsonl", [event(a)])
    journals = [write(tmp_path / "journal.jsonl", [event(a)])]
    jev_rows = [
        {
            **r,
            "status": "success",
            "attempt": 1,
            "configuration_sha256": "jev-config",
            "reported_model": "jev-test",
            "presence": {n: n == "subject" for n in COMPONENTS},
        }
        for r in sample
    ]
    jev_path = write(tmp_path / "jev.jsonl", jev_rows)
    jev_gold_path = write(tmp_path / "jev-gold.jsonl", jev_rows[:1])
    features, occurrences = structural_files(tmp_path)
    return argparse.Namespace(
        data=tmp_path,
        sample=sample_path,
        gold=gold_path,
        journals=journals,
        jev=jev_path,
        jev_gold=jev_gold_path,
        features=features,
        occurrences=occurrences,
        allow_partial=True,
        output=tmp_path / "release",
    )


def test_end_to_end_build_check_and_determinism(modules, tmp_path, monkeypatch):
    report, release = modules
    args = fixture_args(tmp_path, modules, monkeypatch)
    before = {p: p.read_bytes() for p in [*args.journals, args.jev, args.jev_gold]}
    release.build(args)
    assert release.check(args.output)["primary_final_records"] == 1
    manifest = json.loads((args.output / "manifest.json").read_text())
    assert manifest["partial"] is True
    assert manifest["counts"]["sample_texts"] == 2
    original = args.output
    args.output = tmp_path / "second"
    release.build(args)
    for path in original.iterdir():
        assert path.read_bytes() == (args.output / path.name).read_bytes()
    assert before == {p: p.read_bytes() for p in before}
    with gzip.open(original / "labels.jsonl.gz", "rt") as stream:
        assert json.loads(next(stream))["status"] == "success"
    args.allow_partial = False
    with pytest.raises(ValueError, match="unfinished_primary"):
        report.prepare(args)
    # Terminal failures count as complete, but do not become absent labels.
    with args.journals[0].open("a") as stream:
        stream.write(
            json.dumps(event(source("A dog runs.", "film-b"), status="failure")) + "\n"
        )
    args.output = tmp_path / "complete"
    release.build(args)
    assert json.loads((args.output / "manifest.json").read_text())["partial"] is False
    data = json.loads((args.output / "report.json").read_text())
    assert data["prevalence"]["summary"]["subject"]["text_weighted"]["denominator"] == 1


def test_check_rejects_tampering_and_unknown_assets(modules, tmp_path, monkeypatch):
    _, release = modules
    args = fixture_args(tmp_path, modules, monkeypatch)
    release.build(args)
    (args.output / "report.json").write_text("{}")
    with pytest.raises(ValueError, match="checksum"):
        release.check(args.output)
    (args.output / "extra").write_text("anything")
    with pytest.raises(ValueError, match="unexpected_release_files"):
        release.check(args.output)


@pytest.mark.parametrize(
    "mutation, message",
    [
        ({"full_text": "synthetic forbidden field"}, "release_record_schema"),
        ({"reported_model": "/models/synthetic.gguf"}, "unclean_model_name"),
        ({"labels": {}}, "release_component_keys"),
    ],
)
def test_offline_schema_check_even_with_updated_checksums(
    modules, tmp_path, monkeypatch, mutation, message
):
    report, release = modules
    args = fixture_args(tmp_path, modules, monkeypatch)
    release.build(args)
    asset = args.output / "labels.jsonl.gz"
    rows = list(report.read_rows(asset).values())
    rows[0].update(mutation)
    release.write_jsonl(asset, rows)
    manifest_path = args.output / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["assets"][asset.name] = {
        "sha256": release.sha256(asset),
        "bytes": asset.stat().st_size,
    }
    report.write_json(manifest_path, manifest)
    (args.output / "SHA256SUMS").write_text(
        "".join(
            f"{release.sha256(args.output / name)}  {name}\n"
            for name in sorted(release.ASSETS)
        )
    )
    with pytest.raises(ValueError, match=message):
        release.check(args.output)


def test_strict_jev_presence_and_configuration(modules, tmp_path):
    report, _ = modules
    row = {**source(), "status": "success", "presence": {n: False for n in COMPONENTS}}
    row["presence"]["subject"] = "false"
    with pytest.raises(ValueError, match="invalid_jev_presence"):
        report.presence({row["text_id"]: row}, "jev")
    sample = {source()["text_id"]: source()}
    events = [
        event(configuration_sha256="one"),
        event(attempt=2, configuration_sha256="two"),
    ]
    path = write(tmp_path / "jev", events)
    with pytest.raises(ValueError, match="mixed_run"):
        report.collect([path], sample, "jev")


def test_empty_journal_and_bad_source_hash(modules, tmp_path):
    report, _ = modules
    sample = {source()["text_id"]: source()}
    path = write(tmp_path / "journal", [], b"incomplete")
    final, info = report.collect([path], sample)
    assert final == {} and info["inputs"][0]["consumed_bytes"] == 0
    with db_factory() as db:
        wrong = copy.deepcopy(event())
        wrong["text_id"] = "wrong-hash"
        with pytest.raises(ValueError, match="source_hash_mismatch"):
            report.check_successes(db, {wrong["text_id"]: wrong})
