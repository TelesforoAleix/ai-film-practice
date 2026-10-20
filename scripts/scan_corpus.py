#!/usr/bin/env python3
"""Read-only publication scan; report counts/locations, never matched content."""

import argparse
import csv
import ipaddress
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

from film_practice import TABLES
from scripts.build_parquet import DOCUMENTS, EMAIL, phone_spans

SECRET = re.compile(
    r"\b(?:AKIA[A-Z0-9]{16}|gh[pousr]_[A-Za-z0-9]{20,}|"
    r"github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|"
    r"xox[baprs]-[A-Za-z0-9-]{10,}|"
    r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})\b|"
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
)
URL = re.compile(r"https?://[^\s<>\"'`]+")
POSIX_PATH = re.compile(r"(?:/(?:Users|home|mnt|private|tmp|var|Volumes)/|~/)")
WINDOWS_PATH = re.compile(r"\b[A-Za-z]:\\[^\s\\]+")
AUTH_QUERY = re.compile(
    r"^(?:token|access_token|api_key|key|signature|sig|auth|"
    r"x-amz-(?:signature|credential|security-token)|x-goog-signature)$",
    re.I,
)


def scan(source: Path) -> dict:
    csv.field_size_limit(sys.maxsize)
    counts = Counter()
    locations = {}
    files = {}

    def record(file, column, category, occurrences, row):
        if not occurrences:
            return
        counts[category] += occurrences
        key = (file, column, category)
        if key not in locations:
            locations[key] = {"occurrences": 0, "cells": 0, "example_data_rows": []}
        item = locations[key]
        item["occurrences"] += occurrences
        item["cells"] += 1
        if len(item["example_data_rows"]) < 3:
            item["example_data_rows"].append(row)

    def inspect(file, column, value, row):
        record(file, column, "email", len(EMAIL.findall(value)), row)
        record(file, column, "phone", len(phone_spans(value)), row)
        record(file, column, "secret_pattern", len(SECRET.findall(value)), row)
        record(file, column, "local_posix_path", len(POSIX_PATH.findall(value)), row)
        # JSON escape sequences are text serialization, not Windows filesystem paths.
        decoded = re.sub(r"\\[nrtbf]", "\n", value)
        decoded = decoded.replace('\\"', '"').replace("\\\\", "\\")
        record(
            file, column, "local_windows_path", len(WINDOWS_PATH.findall(decoded)), row
        )
        for url in URL.findall(value.replace("\\/", "/")):
            try:
                parts = urlsplit(url)
                suspicious = parts.username is not None or any(
                    AUTH_QUERY.fullmatch(key) for key, _ in parse_qsl(parts.query)
                )
                host = parts.hostname or ""
                if host == "localhost" or host.endswith(".local"):
                    suspicious = True
                try:
                    suspicious |= not ipaddress.ip_address(host).is_global
                except ValueError:
                    pass
                record(
                    file, column, "private_or_authenticated_url", int(suspicious), row
                )
            except ValueError:
                record(file, column, "unparseable_url", 1, row)

    for table in TABLES:
        name = table + ".csv"
        rows = 0
        with (source / name).open(encoding="utf-8", newline="") as stream:
            for rows, row in enumerate(csv.DictReader(stream), 1):
                for column, value in row.items():
                    if value:
                        inspect(name, column, value, rows)
        files[name] = {"rows_scanned": rows}
        print(f"Scanned {name}", flush=True)
    for name in DOCUMENTS:
        raw = (source / name).read_bytes()
        inspect(name, "document", raw.decode("utf-8"), 1)
        files[name] = {"bytes_scanned": len(raw)}
        print(f"Scanned {name}", flush=True)
    return {
        "method": "Full CSV-aware pattern and URL scan; no matched content retained.",
        "limits": "Pattern scanning is not proof of absence of every kind of secret.",
        "files": files,
        "category_occurrences": dict(counts),
        "locations": [
            {
                "file": file,
                "column": column,
                "category": category,
                **details,
                "example": "[email removed]"
                if category == "email"
                else "[redacted candidate]",
            }
            for (file, column, category), details in sorted(locations.items())
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_folder", type=Path)
    parser.add_argument("--report", type=Path, default=Path("data/scan-report.json"))
    args = parser.parse_args()
    report = scan(args.source_folder)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["category_occurrences"], sort_keys=True))


if __name__ == "__main__":
    main()
