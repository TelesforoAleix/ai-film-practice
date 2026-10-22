"""Unweighted descriptive agreement on available gold texts; failures stay missing."""

import argparse
import json
from pathlib import Path

from film_practice.prompt_labels import COMPONENTS, validate


def labels_by_id(path):
    latest = {}
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            latest[row["text_id"]] = row
    result = {}
    for key, row in latest.items():
        if row.get("status", "success") == "success":
            result[key] = validate(row["labels"])
    return result


def metrics(tp, fp, fn, tn):
    n = tp + fp + fn + tn
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    observed = (tp + tn) / n if n else None
    expected = ((tp + fp) * (tp + fn) + (fn + tn) * (fp + tn)) / n**2 if n else None
    kappa = (observed - expected) / (1 - expected) if n and expected != 1 else None
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "n": n,
        "precision": precision,
        "recall": recall,
        "kappa": kappa,
        "accuracy": observed,
    }


def compare(gold, predictions):
    keys = gold.keys() & predictions.keys()
    per = {}
    total = [0, 0, 0, 0]
    for component in COMPONENTS:
        counts = [0, 0, 0, 0]
        for key in keys:
            actual = gold[key][component]["present"]
            predicted = predictions[key][component]["present"]
            index = (
                0 if actual and predicted else 1 if predicted else 2 if actual else 3
            )
            counts[index] += 1
        per[component] = metrics(*counts)
        total = [a + b for a, b in zip(total, counts, strict=True)]
    macro = {}
    for name in ("precision", "recall", "kappa", "accuracy"):
        defined = [v[name] for v in per.values() if v[name] is not None]
        macro[name] = sum(defined) / len(defined) if defined else None
        macro[name + "_defined_components"] = len(defined)
    return {
        "gold_texts": len(gold),
        "compared_texts": len(keys),
        "missing_or_failed": len(gold.keys() - keys),
        "prediction_texts_outside_gold": len(predictions.keys() - gold.keys()),
        "per_component": per,
        "micro": metrics(*total),
        "macro": macro,
        "scope": (
            "Presence only; spans checked for schema, not span agreemen"
            "t. Single-coder agent gold; provisional."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument("--labels", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(
            compare(labels_by_id(args.gold), labels_by_id(args.labels)), indent=2
        )
        + "\n"
    )
