"""Materialise single-coder agent readings; assignments contain short spans only.

Hashes bind readings to the deterministic gold_selection.jsonl. No model or heuristic
assigns semantics here: absent components were judged absent on the read text.
"""

import argparse
import json
from collections import Counter
from pathlib import Path

from film_practice import connect
from film_practice.prompt_labels import COMPONENTS, load_text, validate

# Each mapping was assigned by reading its complete sampled field.
READINGS = json.loads(Path(__file__).with_name("readings.json").read_text())


def build(data, output):
    with (output / "gold_selection.jsonl").open(encoding="utf-8") as stream:
        selection = [json.loads(line) for line in stream]
    if set(READINGS) != {row["text_id"] for row in selection}:
        raise ValueError("readings_incomplete")
    rows = []
    counts = Counter()
    with connect(data) as db:
        for source in selection:
            text = load_text(db, source)
            spans = READINGS[source["text_id"]]
            labels = {
                name: {"present": name in spans, "span": spans.get(name)}
                for name in COMPONENTS
            }
            validate(labels, text)
            counts.update(spans.keys())
            rows.append(
                {
                    **source,
                    "labels": labels,
                    "study": "04",
                    "code_id": "04.2",
                    "codebook_version": "1.0",
                    "labels_version": "AF3a-v1",
                    "provisional": True,
                    "coder": "single agent coder",
                    "adjudication": False,
                    "evidence_label": "inferred",
                    "competing_explanation": (
                        "Instruction wording and reference scope may admit "
                        "another interpretation; "
                        "no achieved output is observed."
                    ),
                    "denominator": "One exact text; fourteen component decisions.",
                    "confidence_rationale": (
                        "Complete field read against inclusion/exclusion rules "
                        "by one agent coder; "
                        "exact spans verified, no independent coder or adjudication."
                    ),
                }
            )
    (output / "gold.jsonl").write_text(
        "".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows
        )
    )
    (output / "gold_counts.json").write_text(
        json.dumps({name: counts[name] for name in COMPONENTS}, indent=2) + "\n"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, default=Path("prompt-labels/outputs"))
    args = parser.parse_args()
    build(args.data, args.output)
