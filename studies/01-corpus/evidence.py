"""Attach explicit film sets and evidence fields to report-level summaries."""

import pandas as pd


def aggregates(frame, out):
    primary = frame[frame.population == "primary"]
    rows = []
    for filename, group_column in [
        ("distributions.csv", "group"),
        ("generation_weights.csv", "cohort_group"),
        ("model_weights.csv", "cohort_group"),
    ]:
        summary = pd.read_csv(out / filename, keep_default_na=False)
        if filename == "model_weights.csv":
            summary = summary[summary.cohort_group == "primary"].nlargest(8, "jobs")
        for _, row in summary.iterrows():
            group = row[group_column]
            selected = (
                primary
                if group == "primary"
                else primary[primary.cohort_group == group]
            )
            rows.append(
                {
                    "study": "01",
                    "film_id": "|".join(sorted(selected.film_id)),
                    "entity_ids": (
                        "All compound generation/related entity keys "
                        "for the listed films"
                    ),
                    "source_path": filename
                    + ("; profile.sql and quality.py; published string views"),
                    "excerpt": row.to_json(force_ascii=False),
                    "evidence_label": "observed",
                    "competing_explanation": (
                        "Selection, format, duration, creator and incomplete external "
                        "histories may explain group differences; job shares "
                        "overweight prolific histories"
                    ),
                    "denominator": (
                        f"{len(selected)} films; "
                        f"{int(selected.generations.sum())} recorded jobs; "
                        "measured coverage and weights in excerpt"
                    ),
                    "confidence_rationale": (
                        "Exact reproducible snapshot aggregates; subgroup "
                        "comparisons descriptive; repeated creators, batches and "
                        "prompts not independent"
                    ),
                }
            )
    pd.DataFrame(rows).to_csv(out / "aggregate_evidence.csv", index=False)
