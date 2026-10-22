"""Descriptive presence agreement between AF3a, Jev, and optional gold labels."""

import argparse
import json
from pathlib import Path

from film_practice.prompt_labels import COMPONENTS


def read_labels(path, kind):
    rows = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("status", "success") != "success":
            continue
        text_id = row["text_id"]
        labels = (
            row["presence"]
            if kind == "jev"
            else {name: value["present"] for name, value in row["labels"].items()}
        )
        rows[text_id] = {name: bool(labels[name]) for name in COMPONENTS}
    return rows


def compare(left, right):
    keys = left.keys() & right.keys()
    per_component = {}
    total = {
        name: 0
        for name in (
            "both_present",
            "both_absent",
            "left_only_present",
            "right_only_present",
        )
    }
    for component in COMPONENTS:
        per_component[component] = _component_metrics(left, right, keys, component)
        per_component[component]["left_lacks"] = sorted(right.keys() - left.keys())
        per_component[component]["right_lacks"] = sorted(left.keys() - right.keys())
        for name in total:
            total[name] += per_component[component][name]
    n = sum(total.values())
    observed = (total["both_present"] + total["both_absent"]) / n if n else None
    yes_left = total["both_present"] + total["left_only_present"]
    yes_right = total["both_present"] + total["right_only_present"]
    expected = (
        ((yes_left * yes_right) + ((n - yes_left) * (n - yes_right))) / n**2
        if n
        else None
    )
    return {
        "compared_texts": len(keys),
        "left_lacks": sorted(right.keys() - left.keys()),
        "right_lacks": sorted(left.keys() - right.keys()),
        "per_component": per_component,
        "micro": {
            **total,
            "n": n,
            "accuracy": observed,
            "kappa": (observed - expected) / (1 - expected)
            if n and expected != 1
            else None,
            "left_lacks": sorted(right.keys() - left.keys()),
            "right_lacks": sorted(left.keys() - right.keys()),
        },
        "disagreements": {
            component: sorted(
                key for key in keys if left[key][component] != right[key][component]
            )
            for component in COMPONENTS
        },
    }


def _component_metrics(left, right, keys, component):
    counts = {
        "both_present": 0,
        "both_absent": 0,
        "left_only_present": 0,
        "right_only_present": 0,
    }
    for key in keys:
        a, b = left[key][component], right[key][component]
        label = (
            "both_present"
            if a and b
            else "both_absent"
            if not a and not b
            else ("left_only_present" if a else "right_only_present")
        )
        counts[label] += 1
    n = sum(counts.values())
    accuracy = (counts["both_present"] + counts["both_absent"]) / n if n else None
    yes_left = counts["both_present"] + counts["left_only_present"]
    yes_right = counts["both_present"] + counts["right_only_present"]
    expected = (
        ((yes_left * yes_right) + ((n - yes_left) * (n - yes_right))) / n**2
        if n
        else None
    )
    return {
        **counts,
        "n": n,
        "accuracy": accuracy,
        "kappa": (accuracy - expected) / (1 - expected)
        if n and expected != 1
        else None,
    }


def run(harness_path, jev_path, output, gold_path=None):
    harness = read_labels(harness_path, "harness")
    jev = read_labels(jev_path, "jev")
    result = {"harness_vs_jev": compare(harness, jev)}
    if gold_path:
        gold = read_labels(gold_path, "harness")
        result["harness_vs_gold"] = compare(harness, gold)
        result["jev_vs_gold"] = compare(jev, gold)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--harness", type=Path, required=True)
    parser.add_argument("--jev", type=Path, required=True)
    parser.add_argument("--gold", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.harness, args.jev, args.output, args.gold)
