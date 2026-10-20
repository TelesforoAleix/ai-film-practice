"""Validate every case file against the current shared codebook (no data needed)."""

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATES = {"coded", "unknown", "empty", "not_applicable", "not_observed_in_scope"}
LABELS = {
    "observed",
    "creator-stated",
    "inferred",
    "associated",
    "experimentally supported",
    "proposed",
}
EVIDENCE = (
    "study",
    "film_id",
    "entity_ids",
    "source_path",
    "excerpt",
    "evidence_label",
    "competing_explanation",
    "denominator",
    "confidence_rationale",
    "scope_note",
    "evidence_id",
)


def validate(rows, definitions, version):
    """Validate one film's assignments; arguments allow wholly synthetic tests."""
    expected = {r["code_id"]: r for r in definitions}
    counts = Counter(r["code_id"] for r in rows)
    if set(counts) != set(expected) or any(n != 1 for n in counts.values()):
        raise ValueError("Each current code must occur exactly once")
    if len({r["film_id"] for r in rows}) != 1:
        raise ValueError("One film per codes.csv")
    for row in rows:
        if row["status"] not in STATES:
            raise ValueError("Invalid state")
        if row["codebook_version"] != version:
            raise ValueError("Stale codebook version")
        definition = expected[row["code_id"]]
        if (
            row["study"] != definition["study"]
            or row["later_study"] != definition["study"]
        ):
            raise ValueError("Study/code mismatch")
        if row["evidence_label"] not in LABELS:
            raise ValueError("Invalid evidence label")
        if any(not row.get(k, "").strip() or row[k] == r"\N" for k in EVIDENCE):
            raise ValueError("Empty evidence field")
        if row["status"] == "coded":
            values = row["value"].split("|")
            if not set(values) <= set(definition["values"].split("|")) or len(
                set(values)
            ) != len(values):
                raise ValueError("Invalid coded value")
        elif row["value"] != r"\N":
            raise ValueError(
                "Non-coded assignment must retain unavailable value marker"
            )


def main():
    corpus = ROOT.parent / "studies/01-corpus"
    version = re.search(
        r"^# Shared codebook, version (\S+)", (corpus / "CODEBOOK.md").read_text()
    ).group(1)
    with (corpus / "outputs/codebook.csv").open() as stream:
        definitions = list(csv.DictReader(stream))
    with (corpus / "outputs/calibration.csv").open() as stream:
        columns = csv.DictReader(stream).fieldnames
    paths = sorted(ROOT.glob("*/codes.csv"))
    if not paths:
        raise ValueError("No case files")
    total = 0
    for path in paths:
        if path.stat().st_size >= 1_000_000:
            raise ValueError("Case file exceeds 1 MB")
        with path.open() as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != columns:
                raise ValueError("Calibration column contract changed")
            rows = list(reader)
        validate(rows, definitions, version)
        total += len(rows)
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in {".csv", ".json", ".md", ".py"}:
            if path.stat().st_size >= 1_000_000:
                raise ValueError("Case file exceeds 1 MB")
    print(
        f"Validated {len(paths)} case files, {total} assignments, codebook {version}."
    )


if __name__ == "__main__":
    main()
