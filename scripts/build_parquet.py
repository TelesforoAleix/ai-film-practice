#!/usr/bin/env python3
"""Build privacy-redacted release assets without changing the collected source files."""

import argparse
import csv
import gzip
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import phonenumbers
import pyarrow as pa
import pyarrow.parquet as pq

from film_practice import TABLES

# A letter-only final domain label avoids treating package versions as addresses.
EMAIL = re.compile(
    r"(?<![\w.+-])[\w.+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"
    r"(?![\w.-])"
)
REPLACEMENT = "[email removed]"
LOCAL_PATH = re.compile(
    r"(?:/(?:Users|home|mnt|private|tmp|var|Volumes)/|~/)[^\s<>\"'`\\]+"
)
PHONE_LABEL = re.compile(r"\b(?:phone|telephone|tel|whatsapp|mobile)\s*[:=]\s*", re.I)
NULL = r"\N"
DOCUMENTS = (
    "README.md",
    "RESEARCH_HANDOVER.md",
    "validation_report.md",
    "four_film_case_studies.md",
    "FILE_DOWNLOADS.md",
    "Studio_Research_Programme.md",
)


def phone_spans(value: str) -> list[tuple[int, int]]:
    """Valid international numbers and explicitly labelled US-format contacts.

    Do not interpret arbitrary digit sequences (IDs, seeds, dates) as phone numbers.
    """
    labels = list(PHONE_LABEL.finditer(value))
    if "+" not in value and not labels:
        return []
    spans = (
        {
            (match.start, match.end)
            for match in phonenumbers.PhoneNumberMatcher(value, None)
        }
        if "+" in value
        else set()
    )
    for label in labels:
        segment = value[label.end() : label.end() + 80]
        for match in phonenumbers.PhoneNumberMatcher(segment, "US"):
            spans.add((label.end() + match.start, label.end() + match.end))
    return sorted(spans)


def redact_with_counts(value: str) -> tuple[str, Counter]:
    counts = Counter()
    value, counts["email"] = EMAIL.subn(REPLACEMENT, value)
    value, counts["local_path"] = LOCAL_PATH.subn("[local path removed]", value)
    spans = phone_spans(value)
    counts["phone"] = len(spans)
    for start, end in reversed(spans):
        value = value[:start] + "[phone removed]" + value[end:]
    return value, counts


def redact(value: str) -> str:
    return redact_with_counts(value)[0]


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def hash_value(digest, value: str | None) -> None:
    """Length framing preserves order and distinguishes null from empty text."""
    if value is None:
        digest.update(b"N")
    else:
        encoded = value.encode("utf-8")
        digest.update(b"S" + len(encoded).to_bytes(8, "big") + encoded)


def redacted_csv_gzip(source: Path, destination: Path) -> tuple[str, Counter]:
    """Preserve UTF-8 bytes and all line endings except authorized replacements."""
    digest = hashlib.sha256()
    counts = Counter()
    with source.open(encoding="utf-8", newline="") as src:
        with destination.open("wb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as out:
                for line in src:
                    sanitized, occurrences = redact_with_counts(line)
                    encoded = sanitized.encode("utf-8")
                    digest.update(encoded)
                    out.write(encoded)
                    counts.update(occurrences)
    # Decompress separately to verify transformed bytes without CSV reserialization.
    actual = hashlib.sha256()
    with gzip.open(destination, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            actual.update(block)
    if actual.hexdigest() != digest.hexdigest():
        raise ValueError("Redacted CSV byte verification failed")
    return digest.hexdigest(), counts


def build_table(source: Path, destination: Path, batch_size: int = 1024) -> dict:
    csv.field_size_limit(sys.maxsize)
    nulls, empties = Counter(), Counter()
    redactions = {kind: Counter() for kind in ("email", "local_path", "phone")}
    source_prompt_hash = hashlib.sha256()
    generation_keys, generation_films, prompts = set(), set(), set()
    raw_prompts = set()
    nonempty = explicitly_empty = row_count = 0
    with source.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        columns = reader.fieldnames
        if not columns or len(set(columns)) != len(columns):
            raise ValueError("Missing or duplicate CSV columns")
        schema = pa.schema([(name, pa.string()) for name in columns])
        with pq.ParquetWriter(destination, schema, compression="zstd") as writer:
            batch = []
            for row in reader:
                if None in row or any(value is None for value in row.values()):
                    raise ValueError("Malformed CSV row")
                values = {}
                for name, value in row.items():
                    sanitized, counts = redact_with_counts(value)
                    for kind, count in counts.items():
                        redactions[kind][name] += count
                    nulls[name] += value == NULL
                    empties[name] += value == ""
                    values[name] = None if value == NULL else sanitized
                batch.append(values)
                row_count += 1
                if source.stem == "generations":
                    key = (row["film_id"], row["generation_id"])
                    if key in generation_keys:
                        raise ValueError("Duplicate compound generation key")
                    generation_keys.add(key)
                    generation_films.add(row["film_id"])
                    prompt = values["prompt"]
                    hash_value(source_prompt_hash, prompt)
                    if prompt not in (None, ""):
                        nonempty += 1
                        prompts.add(prompt)
                        raw_prompts.add(row["prompt"])
                    explicitly_empty += prompt == ""
                if len(batch) == batch_size:
                    writer.write_table(pa.Table.from_pylist(batch, schema=schema))
                    batch = []
            if batch:
                writer.write_table(pa.Table.from_pylist(batch, schema=schema))
    # Re-read every value and count nulls and empty strings separately.
    parquet_nulls, parquet_empties = Counter(), Counter()
    parquet_prompt_hash = hashlib.sha256()
    parquet_rows = 0
    with source.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        parquet = pq.ParquetFile(destination)
        if parquet.schema_arrow != schema:
            raise ValueError("Parquet schema differs from all-string source schema")
        for batch in parquet.iter_batches(batch_size=batch_size):
            for actual in batch.to_pylist():
                raw = next(reader)
                expected = {
                    name: None if value == NULL else redact(value)
                    for name, value in raw.items()
                }
                if actual != expected:
                    # Never include cell contents in errors or logs.
                    raise ValueError("CSV/Parquet value comparison failed")
                for name, value in actual.items():
                    parquet_nulls[name] += value is None
                    parquet_empties[name] += value == ""
                if source.stem == "generations":
                    hash_value(parquet_prompt_hash, actual["prompt"])
                parquet_rows += 1
        if next(reader, None) is not None:
            raise ValueError("Parquet has fewer rows than CSV")
    if (
        row_count != parquet_rows
        or nulls != parquet_nulls
        or empties != parquet_empties
    ):
        raise ValueError("CSV/Parquet counts differ")
    result = {
        "csv_rows": row_count,
        "parquet_rows": parquet_rows,
        "all_values_equal_after_redaction": True,
        "columns": {
            name: {
                "csv_null": nulls[name],
                "parquet_null": parquet_nulls[name],
                "csv_empty": empties[name],
                "parquet_empty": parquet_empties[name],
                "email_occurrences_redacted": redactions["email"][name],
                "local_path_occurrences_redacted": redactions["local_path"][name],
                "phone_occurrences_redacted": redactions["phone"][name],
            }
            for name in columns
        },
    }
    if source.stem == "generations":
        if source_prompt_hash.digest() != parquet_prompt_hash.digest():
            raise ValueError("Ordered prompt hashes differ")
        result["generations"] = {
            "distinct_compound_keys": len(generation_keys),
            "distinct_film_ids": len(generation_films),
            "nonempty_primary_prompts": nonempty,
            "distinct_nonempty_primary_prompts_source": len(raw_prompts),
            "distinct_nonempty_primary_prompts_published": len(prompts),
            "explicitly_empty_primary_prompts": explicitly_empty,
            "ordered_redacted_csv_prompt_sha256": source_prompt_hash.hexdigest(),
            "ordered_parquet_prompt_sha256": parquet_prompt_hash.hexdigest(),
        }
    return result


def build(source_dir: Path, output_dir: Path, enforce_snapshot: bool = True) -> dict:
    if output_dir.resolve().is_relative_to(source_dir.resolve()):
        raise ValueError("Output must be outside the read-only source")
    output_dir.mkdir(parents=True, exist_ok=True)
    report = {"snapshot": "data-2026-10-20", "tables": {}}
    for name in TABLES:
        source = source_dir / f"{name}.csv"
        parquet = output_dir / f"{name}.parquet"
        compressed = output_dir / f"{name}.csv.gz"
        result = build_table(source, parquet)
        digest, counts = redacted_csv_gzip(source, compressed)
        for kind in ("email", "local_path", "phone"):
            if counts[kind] != sum(
                c[f"{kind}_occurrences_redacted"] for c in result["columns"].values()
            ):
                raise ValueError("CSV byte and field redaction counts differ")
        result["redacted_csv_sha256"] = digest
        result["gzip_decompression_verified"] = True
        report["tables"][name] = result
        print(
            f"Verified {name}: {result['csv_rows']:,} rows; {dict(counts)} redactions",
            flush=True,
        )
    if enforce_snapshot:
        expected = {
            "films": 6224,
            "priority_films": 186,
            "folders": 3246,
            "generations": 130899,
            "assets": 163184,
            "asset_usages": 469242,
            "reference_elements": 5223,
        }
        for name, count in expected.items():
            if report["tables"][name]["csv_rows"] != count:
                raise ValueError(f"Snapshot row count does not reconcile: {name}")
        metrics = report["tables"]["generations"]["generations"]
        expected_metrics = {
            "distinct_compound_keys": 130899,
            "distinct_film_ids": 158,
            "nonempty_primary_prompts": 124642,
            "distinct_nonempty_primary_prompts_source": 61479,
            "explicitly_empty_primary_prompts": 1083,
        }
        for name, count in expected_metrics.items():
            if metrics[name] != count:
                raise ValueError(f"Snapshot metric does not reconcile: {name}")
    assets = [
        output_dir / f"{name}{suffix}"
        for name in TABLES
        for suffix in (".parquet", ".csv.gz")
    ]
    report["assets"] = {
        p.name: {"bytes": p.stat().st_size, "sha256": file_sha256(p)} for p in assets
    }
    (output_dir / "SHA256SUMS").write_text(
        "".join(f"{v['sha256']}  {name}\n" for name, v in report["assets"].items()),
        encoding="utf-8",
    )
    (output_dir / "build-report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_folder", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/build"))
    args = parser.parse_args()
    build(args.source_folder, args.output)


if __name__ == "__main__":
    main()
