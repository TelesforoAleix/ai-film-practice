"""Resumable local OpenAI-compatible semantic labelling; no model is bundled."""

import argparse
import fcntl
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from film_practice import connect
from film_practice.prompt_labels import (
    SCHEMA,
    TEMPLATE,
    canonical,
    digest,
    load_text,
    validate,
)


def read_rows(path):
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if len({r["text_id"] for r in rows}) != len(rows):
        raise ValueError("duplicate_text_id")
    return rows


def recover(stream):
    """Recover only an unterminated tail. Completed malformed records are errors."""
    stream.seek(0)
    rows = []
    while True:
        offset = stream.tell()
        line = stream.readline()
        if not line:
            break
        if not line.endswith(b"\n"):
            stream.seek(offset)
            stream.truncate()
            break
        rows.append(json.loads(line))
    stream.seek(0, 2)
    return rows


def post(url, payload, timeout):
    request = urllib.request.Request(
        url,
        data=canonical(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as reply:
        return json.load(reply)


def run(
    db,
    sample,
    output,
    base_url,
    model,
    max_attempts=3,
    timeout=180,
    max_tokens=1400,
    transport=post,
):
    if max_attempts < 1 or timeout <= 0 or max_tokens < 1:
        raise ValueError("invalid_request_settings")
    settings = {"temperature": 0, "max_tokens": max_tokens, "stream": False}
    template_hash = digest(canonical({"system": TEMPLATE, "schema": SCHEMA}))
    metadata = {
        "requested_model": model,
        "base_url": base_url.rstrip("/"),
        "request_settings": settings,
        "template_sha256": template_hash,
        "max_attempts": max_attempts,
        "timeout_seconds": timeout,
        "codebook_version": "1.0",
        "labels_version": "AF3a-v1",
        "provisional": True,
        "study": "04",
        "code_id": "04.2",
        "evidence_label": "inferred",
        "denominator": "One exact text; fourteen component decisions.",
        "competing_explanation": "Wording and reference scope can be ambiguous; "
        "instructions do not establish achieved output.",
        "confidence_rationale": "Provisional model assignment with exact source spans; "
        "agreement with single-agent gold is pending a separate assessment.",
    }
    run_hash = digest(canonical(metadata))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a+b") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        history = recover(stream)
        latest = {}
        for record in history:
            if record["run_sha256"] != run_hash:
                raise ValueError("output_configuration_mismatch")
            latest[record["text_id"]] = record

        def append(record):
            stream.write((canonical(record) + "\n").encode())
            stream.flush()
            os.fsync(stream.fileno())
            latest[record["text_id"]] = record

        for row in sample:
            previous = latest.get(row["text_id"])
            if previous and previous["status"] == "started":
                previous = {
                    **previous,
                    "status": "failure",
                    "error_type": "Interrupted",
                }
                append(previous)
            if previous and (
                previous["status"] == "success" or previous["attempt"] >= max_attempts
            ):
                continue
            text = load_text(db, row)
            if len(text) > 12000:
                raise ValueError("sample_exceeds_documented_limit")
            start = previous["attempt"] if previous else 0
            for attempt in range(start + 1, max_attempts + 1):
                record = {
                    **row,
                    **metadata,
                    "run_sha256": run_hash,
                    "attempt": attempt,
                    "status": "started",
                    "reported_model": None,
                }
                # Reserve before sending; crashes cannot reset retry budgets.
                append(record)
                payload = {
                    "model": model,
                    **settings,
                    "messages": [
                        {"role": "system", "content": TEMPLATE},
                        {"role": "user", "content": text},
                    ],
                    "response_format": {
                        "type": "json_schema",
                        "json_schema": {
                            "name": "prompt_components",
                            "strict": True,
                            "schema": SCHEMA,
                        },
                    },
                }
                try:
                    reply = transport(
                        base_url.rstrip("/") + "/chat/completions", payload, timeout
                    )
                    if not isinstance(reply, dict):
                        raise ValueError("reply_object")
                    reported = reply.get("model")
                    if not isinstance(reported, str) or not reported:
                        raise ValueError("missing_reported_model")
                    record["reported_model"] = reported
                    choice = reply["choices"][0]
                    if choice.get("finish_reason") != "stop":
                        raise ValueError("incomplete_reply")
                    labels = validate(json.loads(choice["message"]["content"]), text)
                    record = {**record, "status": "success", "labels": labels}
                except (
                    ValueError,
                    KeyError,
                    IndexError,
                    TypeError,
                    OSError,
                    urllib.error.URLError,
                ) as error:
                    # Errors may echo source text: persist only the exception type.
                    record = {
                        **record,
                        "status": "failure",
                        "error_type": type(error).__name__,
                    }
                append(record)
                if record["status"] == "success":
                    break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", type=Path, required=True)
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument(
        "--base-url", required=True, help="OpenAI-compatible URL ending /v1"
    )
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--max-tokens", type=int, default=1400)
    args = parser.parse_args()
    with connect(args.data) as db:
        run(
            db,
            read_rows(args.sample),
            args.output,
            args.base_url,
            args.model,
            args.max_attempts,
            args.timeout,
            args.max_tokens,
        )
