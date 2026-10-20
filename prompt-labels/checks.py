"""Validate source spans and sampling invariants; reproduce agreement smoke checks."""

import argparse
import copy
import json
from pathlib import Path

from agreement import compare, labels_by_id
from harness import read_rows

from film_practice import connect
from film_practice.prompt_labels import COMPONENTS, load_text, validate


def check(data, sample_path, output):
    sample = read_rows(sample_path)
    selected = read_rows(output / "gold_selection.jsonl")
    gold_rows = read_rows(output / "gold.jsonl")
    sample_by_id = {r["text_id"]: r for r in sample}
    assert len(sample) == 5000
    assert len(gold_rows) == len(selected) == 300
    assert len({r["film_id"] for r in sample}) == 157
    assert len({r["film_id"] for r in gold_rows}) == 157
    assert {r["text_id"] for r in gold_rows} == {r["text_id"] for r in selected}
    with connect(data) as db:
        # Avoid thousands of Parquet scans; source bytes and keys stay unchanged.
        db.execute(
            "CREATE TEMP TABLE af3a_primary AS "
            "SELECT film_id,generation_id,prompt FROM generations"
        )
        db.execute(
            "CREATE TEMP TABLE af3a_nested AS "
            "SELECT * FROM generation_prompts WHERE field_path<>'params.prompt'"
        )
        db.execute("CREATE OR REPLACE VIEW generations AS SELECT * FROM af3a_primary")
        db.execute(
            "CREATE OR REPLACE VIEW generation_prompts AS SELECT * FROM af3a_nested"
        )
        for row in sample:
            assert row["population"] == "primary"
            assert len(load_text(db, row)) <= 12000
        for row in gold_rows:
            text = load_text(db, row)
            validate(row["labels"], text)
            assert row["film_id"] == sample_by_id[row["text_id"]]["film_id"]
            assert all(v["span"] != text for v in row["labels"].values())
    gold = labels_by_id(output / "gold.jsonl")
    perturbed = copy.deepcopy(gold)
    for labels in perturbed.values():
        value = labels["subject"]
        value["present"] = not value["present"]
        value["span"] = "deliberately incorrect" if value["present"] else None
    self_result = compare(gold, gold)
    wrong_result = compare(gold, perturbed)
    assert self_result["micro"]["kappa"] == 1
    assert self_result["micro"]["n"] == len(COMPONENTS) * 300
    assert wrong_result["per_component"]["subject"]["tp"] == 0
    for name, result in [
        ("agreement_self.json", self_result),
        ("agreement_perturbed.json", wrong_result),
    ]:
        (output / name).write_text(json.dumps(result, indent=2) + "\n")
    print(
        "Verified 5000 sampled fields, 300 gold fields, 4200 gold decisions; "
        "self kappa=1; all 300 subject decisions deliberately inverted."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument(
        "--sample", type=Path, default=Path("data/prompt-labels-v1/sample.jsonl")
    )
    parser.add_argument("--output", type=Path, default=Path("prompt-labels/outputs"))
    args = parser.parse_args()
    check(args.data, args.sample, args.output)
