"""Build or verify prompt-labels-v2 locally; never upload or publish anything."""

import argparse
import gzip
import hashlib
import io
import json
import re
from pathlib import Path

import jev as jev_client
import phonenumbers
import report

from film_practice.prompt_labels import COMPONENTS, canonical

ASSETS = {
    "labels.jsonl.gz",
    "jev-presence.jsonl.gz",
    "jev-gold-presence.jsonl.gz",
    "report.json",
    "manifest.json",
}
PRIMARY_FIELDS = (
    *report.SOURCE_KEYS,
    *report.RUN_KEYS,
    "status",
    "attempt",
    "reported_model",
    "error_type",
    "labels",
    "resolved_spans",
    "joined_spans",
)
JEV_FIELDS = (
    *report.SOURCE_KEYS,
    "status",
    "attempt",
    "configuration_sha256",
    "reported_model",
    "presence",
    "p_present",
    "confidence",
)


def filename(value):
    if value is None:
        return None
    if not isinstance(value, str) or not value or value.endswith(("/", "\\")):
        raise ValueError("invalid_model_name")
    return value.replace("\\", "/").rsplit("/", 1)[-1]


def privacy_check(value):
    """Refuse candidates without echoing their contents. No silent redaction."""
    if isinstance(value, dict):
        for item in value.values():
            privacy_check(item)
    elif isinstance(value, list):
        for item in value:
            privacy_check(item)
    elif isinstance(value, str):
        email = re.search(r"[A-Za-z0-9._%+-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}", value)
        local = re.search(
            r"(?:/(?:Users|home|mnt|private|tmp|var|Volumes)/|~/|[A-Za-z]:\\)", value
        )
        phone = any(phonenumbers.PhoneNumberMatcher(value, None))
        if email or local or phone:
            raise ValueError("private_content_candidate_requires_owner_review")


def clean(row, kind="primary"):
    allowed = PRIMARY_FIELDS if kind == "primary" else JEV_FIELDS
    result = {name: row[name] for name in allowed if name in row}
    if row["status"] == "failure":
        for name in ("labels", "joined_spans", "resolved_spans"):
            result.pop(name, None)
    for name in ("reported_model", "requested_model"):
        if name in result:
            result[name] = filename(result[name])
    if kind == "jev":
        result.update(
            {
                "study": "04",
                "code_id": "04.2",
                "provisional": True,
                "evidence_label": "inferred",
                "role": "independent presence-only cross-check",
                "labels_version": jev_client.LABELS_VERSION,
                "denominator": "One exact text; fourteen presence decisions.",
                "competing_explanation": (
                    "Wording and reference scope may be ambiguous."
                ),
                "confidence_rationale": (
                    "Independent model presence assignment; no evidence spans "
                    "or independent human adjudication. Scores are model-reported."
                ),
            }
        )
    privacy_check(result)
    return result


def withhold_full_field_spans(rows, sample, db):
    """No full field is released even if the model quoted it as a span.

    All spans have already passed source validation. Withheld positives keep a
    hash and length; they are explicitly distinguishable from absent components.
    """
    result = []
    for key, row in sorted(rows.items()):
        safe = clean(row)
        if row["status"] == "success":
            text = report.load_text(db, sample[key])
            safe["labels"] = {}
            for name, value in row["labels"].items():
                span = value["span"]
                safe["labels"][name] = (
                    {
                        "present": True,
                        "span": None,
                        "span_withheld": "full_source_field",
                        "span_sha256": hashlib.sha256(span.encode()).hexdigest(),
                        "span_characters": len(span),
                    }
                    if span == text
                    else value.copy()
                )
        result.append(safe)
    return result


def write_jsonl(path, rows):
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8", newline="\n") as stream:
                for row in rows:
                    stream.write(canonical(row) + "\n")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(args):
    sample, final, jev, jev_gold, data, sources = report.prepare(args)
    # Validate and clean in memory before creating an uploadable directory.
    with report.connect(args.data) as db:
        report.materialise_sources(db)
        primary = withhold_full_field_spans(final, sample, db)
    jev_rows = [clean(row, "jev") for _, row in sorted(jev.items())]
    jev_gold_rows = [clean(row, "jev") for _, row in sorted(jev_gold.items())]
    privacy_check(data)
    settings = [
        {name: row[name] for name in report.RUN_KEYS if name in row}
        for row in primary[:1]
    ]
    manifest = {
        "release": "prompt-labels-v2",
        "format_version": 1,
        "partial": bool(
            len(final) != len(sample) or sources["primary_journals"]["pending_attempts"]
        ),
        "primary_settings": settings,
        "reported_models": sorted(
            {r["reported_model"] for r in primary if r.get("reported_model")}
        ),
        "jev": {
            "role": "presence-only cross-check; never merged with primary labels",
            "reported_models": sorted(
                {
                    r["reported_model"]
                    for r in jev_rows + jev_gold_rows
                    if r.get("reported_model")
                }
            ),
            "labels_version": jev_client.LABELS_VERSION,
            "question_set_sha256": jev_client.QUESTION_SET_SHA256,
            "client_default_requested_model": jev_client.MODEL,
            "configuration_sha256": sorted(
                {r["configuration_sha256"] for r in jev_rows + jev_gold_rows}
            ),
            "limit": (
                "Journals retain the configuration hash and reported model, not "
                "plaintext original request settings. Client defaults describe "
                "the checked-in client, not independently attested execution "
                "settings."
            ),
        },
        "sources": sources,
        "counts": {
            "sample_texts": len(sample),
            "primary_final_records": len(primary),
            "jev_texts": len(jev_rows),
            "jev_gold_texts": len(jev_gold_rows),
        },
        "full_field_spans_withheld": sum(
            value.get("span_withheld") == "full_source_field"
            for row in primary
            for value in row.get("labels", {}).values()
        ),
        "cleaning": (
            "Allowlisted fields only; model identifiers reduced to file "
            "names; base_url omitted. No full text fields. Full-field spans "
            "withheld with hash and length. Run hashes bind original private "
            "configuration, not the sanitised metadata."
        ),
        "limits": (
            "Provisional inferred labels, single-agent unadjudicated gold, "
            "balanced non-proportional sample, long texts structural-only. "
            "Existing third-party rights remain unchanged."
        ),
        "shared_definitions_sha256": sha256(
            Path(report.__file__).parent.parent / "src/film_practice/prompt_labels.py"
        ),
        "tool_sha256": {
            path.name: sha256(path)
            for path in sorted(Path(__file__).parent.glob("*.py"))
        },
    }
    privacy_check(manifest)
    args.output.mkdir(parents=True, exist_ok=False)
    write_jsonl(args.output / "labels.jsonl.gz", primary)
    write_jsonl(args.output / "jev-presence.jsonl.gz", jev_rows)
    write_jsonl(args.output / "jev-gold-presence.jsonl.gz", jev_gold_rows)
    report.write_json(args.output / "report.json", data)
    manifest["assets"] = {
        name: {
            "sha256": sha256(args.output / name),
            "bytes": (args.output / name).stat().st_size,
        }
        for name in sorted(ASSETS - {"manifest.json"})
    }
    report.write_json(args.output / "manifest.json", manifest)
    (args.output / "SHA256SUMS").write_text(
        "".join(f"{sha256(args.output / name)}  {name}\n" for name in sorted(ASSETS)),
        encoding="utf-8",
    )
    check(args.output)


def check(directory):
    """Offline integrity, schema, linkage and privacy checks; no journals needed."""
    if {p.name for p in directory.iterdir()} != ASSETS | {"SHA256SUMS"}:
        raise ValueError("unexpected_release_files")
    if any(p.is_symlink() or not p.is_file() for p in directory.iterdir()):
        raise ValueError("unsafe_release_file")
    lines = (directory / "SHA256SUMS").read_text().splitlines()
    expected = [f"{sha256(directory / name)}  {name}" for name in sorted(ASSETS)]
    if lines != expected:
        raise ValueError("release_checksum_mismatch")
    manifest = json.loads((directory / "manifest.json").read_text())
    data = json.loads((directory / "report.json").read_text())
    if manifest["release"] != "prompt-labels-v2" or manifest["format_version"] != 1:
        raise ValueError("release_format")
    for name in ASSETS - {"manifest.json"}:
        if manifest["assets"].get(name) != {
            "sha256": sha256(directory / name),
            "bytes": (directory / name).stat().st_size,
        }:
            raise ValueError("manifest_asset_mismatch")
    sets = {}
    for name, kind in (
        ("labels.jsonl.gz", "primary"),
        ("jev-presence.jsonl.gz", "jev"),
        ("jev-gold-presence.jsonl.gz", "jev"),
    ):
        rows = report.read_rows(directory / name)
        sets[name] = rows
        for row in rows.values():
            privacy_check(row)
            allowed = (
                set(PRIMARY_FIELDS)
                if kind == "primary"
                else set(JEV_FIELDS)
                | {
                    "study",
                    "code_id",
                    "provisional",
                    "evidence_label",
                    "role",
                    "labels_version",
                    "denominator",
                    "competing_explanation",
                    "confidence_rationale",
                }
            )
            if set(row) - allowed or any(key not in row for key in report.SOURCE_KEYS):
                raise ValueError("release_record_schema")
            if row["status"] not in ("success", "failure"):
                raise ValueError("release_status")
            if any(
                row.get(key) != filename(row.get(key))
                for key in ("reported_model", "requested_model")
            ):
                raise ValueError("unclean_model_name")
            if kind == "jev":
                report.presence({row["text_id"]: row}, "jev")
            elif row["status"] == "success":
                labels = row["labels"]
                if set(labels) != set(COMPONENTS):
                    raise ValueError("release_component_keys")
                for value in labels.values():
                    if "span_withheld" in value:
                        if (
                            set(value)
                            != {
                                "present",
                                "span",
                                "span_withheld",
                                "span_sha256",
                                "span_characters",
                            }
                            or value["present"] is not True
                            or value["span"] is not None
                            or value["span_withheld"] != "full_source_field"
                            or not re.fullmatch(r"[0-9a-f]{64}", value["span_sha256"])
                            or type(value["span_characters"]) is not int
                            or value["span_characters"] < 1
                        ):
                            raise ValueError("invalid_withheld_span")
                    else:
                        # Reuse the exact shared schema without fabricating spans.
                        report.validate({name: value for name in COMPONENTS})
    primary = sets["labels.jsonl.gz"]
    jev = sets["jev-presence.jsonl.gz"]
    gold_jev = sets["jev-gold-presence.jsonl.gz"]
    for rows in (primary, gold_jev):
        for row in rows.values():
            report.check_source(row, jev)
    counts = {
        "sample_texts": len(jev),
        "primary_final_records": len(primary),
        "jev_texts": len(jev),
        "jev_gold_texts": len(gold_jev),
    }
    if manifest["counts"] != counts:
        raise ValueError("release_count_mismatch")
    success = sum(row["status"] == "success" for row in primary.values())
    if data["coverage"]["successes"] != success or data["coverage"][
        "terminal_texts"
    ] != len(primary):
        raise ValueError("release_report_mismatch")
    if not manifest["partial"] and len(primary) != len(jev):
        raise ValueError("incomplete_release")
    privacy_check(manifest)
    privacy_check(data)
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, metavar="BUILT_DIRECTORY")
    known, _ = parser.parse_known_args()
    if known.check:
        parser.parse_args()
        print(json.dumps(check(known.check), sort_keys=True))
    else:
        report.arguments(parser)
        parser.add_argument("--output", type=Path, required=True)
        args = parser.parse_args()
        build(args)
