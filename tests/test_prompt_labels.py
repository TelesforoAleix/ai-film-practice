"""AF3a behaviour checks: synthetic texts and loopback HTTP only."""

import importlib.util
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import duckdb
import pytest

from film_practice.prompt_labels import COMPONENTS, SCHEMA, digest, validate


def module(name):
    path = Path(__file__).parents[1] / "prompt-labels" / (name + ".py")
    spec = importlib.util.spec_from_file_location("af3a_" + name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


build = module("build")
harness = module("harness")
agreement = module("agreement")


def labels(**spans):
    return {
        key: {"present": key in spans, "span": spans.get(key)} for key in COMPONENTS
    }


def synthetic_db():
    db = duckdb.connect()
    db.execute(
        "CREATE TABLE generations(film_id VARCHAR,generation_id VARCHAR,prompt VARCHAR)"
    )
    rows = []
    for index, text in enumerate(["A red boat on sand.", "A dog runs."]):
        db.execute("INSERT INTO generations VALUES (?,?,?)", ["film", str(index), text])
        rows.append(
            {
                "film_id": "film",
                "generation_id": str(index),
                "source_table": "generations",
                "field_path": "params.prompt",
                "text_id": digest(text),
            }
        )
    return db, rows


@pytest.mark.parametrize(
    "bad",
    [
        {},
        {**labels(), "extra": {}},
        labels(subject="not in source"),
        {**labels(), "subject": {"present": 1, "span": "boat"}},
        {**labels(), "subject": {"present": False, "span": "boat"}},
        {**labels(), "subject": {"present": True, "span": ""}},
    ],
)
def test_invalid_labels(bad):
    with pytest.raises(ValueError):
        validate(bad, "A boat.")


def test_features_are_structural():
    f = build.features("CAMERA:\n35mm pan.\nKeep the frame unchanged.\nNo text. @ref1")
    assert f["lens_matches"] == 1
    assert f["camera_matches"] == 2
    assert f["section_matches"] == 1
    assert f["preservation_matches"] == 2
    assert f["exclusion_matches"] == 1
    assert f["reference_matches"] == 1
    assert f["reference_excerpt"] == "@ref1"
    assert build.features('{"camera": "wide"}')["structured_json"]
    assert not build.features("{not json}")["structured_json"]
    assert not build.features("x" * 12001)["semantic_eligible"]
    assert (
        build.features(
            ("A repeated long line with enough characters for the rule\n") * 2
        )["repeated_lines"]
        == 1
    )


def test_balanced_global_dedup_and_rare_operations():
    rows = []
    for film, size in [("small", 2), ("large", 100)]:
        for i in range(size):
            rows.append(
                {
                    "film_id": film,
                    "generation_type": "image" if i % 2 else "video",
                    "text_role": "primary",
                    "text_id": str(i),
                }
            )
    selected = build.balanced(rows, 10, "test")
    assert len(selected) == len({r["text_id"] for r in selected}) == 10
    assert sum(r["film_id"] == "small" for r in selected) == 2
    assert {r["generation_type"] for r in selected if r["film_id"] == "small"} == {
        "image",
        "video",
    }
    assert selected == build.balanced(list(reversed(rows)), 10, "test")


def test_http_retry_interruption_resume_and_metadata(tmp_path):
    requests = []
    responses = [
        "invalid",
        labels(subject="boat"),
        labels(subject="dog", action="runs"),
    ]

    class Stub(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            requests.append((self.path, body))
            reply = {
                "model": "stub-reported",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {"content": json.dumps(responses.pop(0))},
                    }
                ],
            }
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(reply).encode())

    server = ThreadingHTTPServer(("127.0.0.1", 0), Stub)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    db, rows = synthetic_db()
    output = tmp_path / "labels.jsonl"
    base = f"http://127.0.0.1:{server.server_port}/v1"
    calls = 0

    def interrupted(url, payload, timeout):
        nonlocal calls
        calls += 1
        if calls == 3:
            raise KeyboardInterrupt
        return harness.post(url, payload, timeout)

    try:
        with pytest.raises(KeyboardInterrupt):
            harness.run(db, rows, output, base, "stub-requested", transport=interrupted)
        records = [json.loads(x) for x in output.read_text().splitlines()]
        assert [r["status"] for r in records] == [
            "started",
            "failure",
            "started",
            "success",
            "started",
        ]
        with output.open("ab") as stream:
            stream.write(b'{"partial":')
        harness.run(db, rows, output, base, "stub-requested")
        count = len(requests)
        harness.run(db, rows, output, base, "stub-requested")
        assert len(requests) == count == 3
        final = [json.loads(x) for x in output.read_text().splitlines()]
        successes = [r for r in final if r["status"] == "success"]
        assert len(successes) == 2
        assert all(r["reported_model"] == "stub-reported" for r in successes)
        assert all(r["requested_model"] == "stub-requested" for r in final)
        assert all(r["request_settings"]["temperature"] == 0 for r in final)
        assert all(len(r["template_sha256"]) == 64 for r in final)
        assert successes[-1]["attempt"] == 2
        assert requests[0][0] == "/v1/chat/completions"
        assert requests[0][1]["response_format"]["json_schema"]["schema"] == SCHEMA
        with pytest.raises(ValueError, match="configuration_mismatch"):
            harness.run(db, rows, output, base, "changed-model")
    finally:
        db.close()
        server.shutdown()
        server.server_close()
        thread.join()


def test_terminal_failures_and_hash_validation(tmp_path):
    db, rows = synthetic_db()
    calls = []

    def invalid(*args):
        calls.append(1)
        return {"model": "fake", "choices": []}

    output = tmp_path / "failures.jsonl"
    harness.run(
        db,
        rows,
        output,
        "http://localhost/v1",
        "fake",
        max_attempts=2,
        transport=invalid,
    )
    harness.run(
        db,
        rows,
        output,
        "http://localhost/v1",
        "fake",
        max_attempts=2,
        transport=invalid,
    )
    assert len(calls) == 4
    assert agreement.labels_by_id(output) == {}
    assert all(
        "labels" not in json.loads(line) for line in output.read_text().splitlines()
    )
    rows[0]["text_id"] = "bad hash"
    with pytest.raises(ValueError, match="source_hash_mismatch"):
        harness.run(
            db,
            rows,
            tmp_path / "new.jsonl",
            "http://localhost/v1",
            "fake",
            transport=invalid,
        )
    db.close()


def test_agreement_known_confusion_and_undefined():
    gold = {str(i): labels(subject="boat") if i < 2 else labels() for i in range(4)}
    predictions = {
        "0": labels(subject="boat"),
        "1": labels(),
        "2": labels(subject="dog"),
        "3": labels(),
    }
    result = agreement.compare(gold, predictions)
    assert result["per_component"]["subject"] == {
        "tp": 1,
        "fp": 1,
        "fn": 1,
        "tn": 1,
        "n": 4,
        "precision": 0.5,
        "recall": 0.5,
        "accuracy": 0.5,
        "kappa": 0.0,
    }
    assert result["per_component"]["action"]["kappa"] is None
    assert agreement.compare(gold, {"0": predictions["0"]})["missing_or_failed"] == 3
    assert agreement.compare(gold, gold)["micro"]["kappa"] == 1


def test_crash_on_last_attempt_becomes_terminal_failure(tmp_path):
    db, rows = synthetic_db()
    output = tmp_path / "crash.jsonl"

    def interrupted(*_):
        raise KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        harness.run(
            db,
            rows[:1],
            output,
            "http://localhost/v1",
            "fake",
            max_attempts=1,
            transport=interrupted,
        )
    # Resuming must record the interrupted attempt as failure, without a new call.
    harness.run(
        db,
        rows[:1],
        output,
        "http://localhost/v1",
        "fake",
        max_attempts=1,
        transport=interrupted,
    )
    last = json.loads(output.read_text().splitlines()[-1])
    assert last["status"] == "failure"
    assert last["error_type"] == "Interrupted"
    db.close()


def test_completed_corruption_is_not_silently_discarded(tmp_path):
    output = tmp_path / "bad.jsonl"
    output.write_bytes(b"{invalid}\n")
    with output.open("a+b") as stream, pytest.raises(ValueError):
        harness.recover(stream)
    assert output.read_bytes() == b"{invalid}\n"


@pytest.mark.parametrize(
    "reply",
    [
        [],
        {"choices": []},
        {"model": "stub", "choices": [{"finish_reason": "length"}]},
        {
            "model": "stub",
            "choices": [
                {
                    "finish_reason": "stop",
                    "message": {"content": json.dumps(labels(subject="invented"))},
                }
            ],
        },
    ],
)
def test_bad_endpoint_replies_are_retained_as_failures(tmp_path, reply):
    db, rows = synthetic_db()
    output = tmp_path / "invalid.jsonl"
    harness.run(
        db,
        rows[:1],
        output,
        "http://localhost/v1",
        "stub",
        max_attempts=1,
        transport=lambda *_: reply,
    )
    record = json.loads(output.read_text().splitlines()[-1])
    assert record["status"] == "failure"
    assert "labels" not in record
    db.close()
