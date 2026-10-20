"""Validate every case file against the current shared codebook (no data needed)."""

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
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


def validate_profile(profile, rows, edges):
    """Check scope and partition invariants without opening the source snapshot."""
    fid = rows[0]["film_id"]
    if profile["film_id"] != fid or edges["film_id"] != fid:
        raise ValueError("Profile/edge film mismatch")
    counts = profile["row_counts"]
    n = counts["generations"]
    register = profile["reading_register"]
    ids = [r["generation_id"] for r in register]
    if not ids or len(set(ids)) != len(ids) or len(ids) > n:
        raise ValueError("Invalid reading register")
    if any(not r["reasons"] for r in register):
        raise ValueError("Reading selection needs reasons")
    for table, fields in profile["field_states"].items():
        for states in fields.values():
            if (
                set(states) != {"unavailable", "empty", "nonempty"}
                or any(v < 0 for v in states.values())
                or sum(states.values()) != counts[table]
            ):
                raise ValueError("Field states must partition table rows")
    for values in profile["generations"].values():
        if sum(v["count"] for v in values) != n:
            raise ValueError("Generation distribution denominator mismatch")
    if "prompt_states" in profile:
        states = profile["prompt_states"]
        exported = profile["field_states"]["generations"]["prompt"]
        if any(states[k] != exported[k] for k in exported) or not (
            0 <= states["distinct_nonempty"] <= states["nonempty"]
        ):
            raise ValueError("Prompt state denominator mismatch")
    for field, table in [
        ("text_roles", "generation_prompts"),
        ("usage_roles", "asset_usages"),
    ]:
        if field in profile and (
            any(v["count"] < 0 for v in profile[field])
            or sum(v["count"] for v in profile[field]) != counts[table]
        ):
            raise ValueError("Role distribution denominator mismatch")
    if "parameter_controls" in profile and not profile["invalid_parameters"]:
        models = {
            r["value"]: r["count"] for r in profile["generations"]["model_identifier"]
        }
        controls = defaultdict(int)
        for value in profile["parameter_controls"]:
            if value["count"] < 0:
                raise ValueError("Negative control count")
            controls[value["model"], value["path"]] += value["count"]
        if any(count != models.get(model) for (model, _), count in controls.items()):
            raise ValueError("Control distribution denominator mismatch")
    for row in rows:
        scopes = re.findall(
            r"([^; ]+)/(?:generation|asset|reference|folder|author|film):",
            row["entity_ids"],
        )
        if any(scope != fid for scope in scopes):
            raise ValueError("Evidence compound key crosses film scope")
        for generation in re.findall(r"/generation:([^; ]+)", row["entity_ids"]):
            # Descendant enumeration deliberately searches the complete graph.
            if row["code_id"] != "07.5" and generation not in ids:
                raise ValueError("Named evidence job outside reading register")
    for edge in edges["edges"]:
        if not edge["usages"]:
            raise ValueError("Traced edge needs usage provenance")


def validate_registration(rows, profile, registered):
    """Preserve literal panel titles, including significant whitespace."""
    if any(r["title"] != registered["title"] for r in rows):
        raise ValueError("Literal registered title mismatch")
    if profile["title"] != registered["title"]:
        raise ValueError("Literal profile title mismatch")
    for table, field in [
        ("generations", "generations"),
        ("folders", "folders"),
        ("reference_elements", "reference_elements"),
    ]:
        if profile["row_counts"][table] != int(registered[field]):
            raise ValueError("Registered entity count mismatch")


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
    with (corpus / "outputs/panel.csv").open() as stream:
        panel = {r["film_id"]: r for r in csv.DictReader(stream)}
    expected = {fid for fid, r in panel.items() if r["batch"] in {"1", "2", "3"}}
    actual = set()
    manifest = json.loads((ROOT / "reproduction.json").read_text())
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
        profile = json.loads((path.parent / "profile.json").read_text())
        edges = json.loads((path.parent / "traced-edges.json").read_text())
        validate_profile(profile, rows, edges)
        fid = rows[0]["film_id"]
        if fid in actual or fid not in panel:
            raise ValueError("Duplicate or unregistered panel film")
        actual.add(fid)
        validate_registration(rows, profile, panel[fid])
        if not (path.parent / "CASE.md").is_file():
            raise ValueError("Missing narrative")
        total += len(rows)
    if actual != expected:
        raise ValueError("Completed batches must match panel membership exactly")
    artifacts = {
        str(p.relative_to(ROOT))
        for p in ROOT.glob("*/*")
        if p.suffix in {".csv", ".json"}
    }
    if set(manifest) != artifacts:
        raise ValueError("Reproduction manifest coverage mismatch")
    for name, digest in manifest.items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest:
            raise ValueError("Reproduction hash mismatch")
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in {".csv", ".json", ".md", ".py"}:
            if path.stat().st_size >= 1_000_000:
                raise ValueError("Case file exceeds 1 MB")
    print(
        f"Validated {len(paths)} case files, {total} assignments, codebook {version}."
    )


if __name__ == "__main__":
    main()
