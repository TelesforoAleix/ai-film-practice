"Snapshot reconciliation and model weights, without retrieving source sites."

import json

import pandas as pd

from film_practice import TABLES

EXPECTED = [
    6224,
    186,
    3246,
    130899,
    161836,
    163184,
    469242,
    142513,
    136313,
    5223,
    456,
    1495,
    6224,
    0,
]


def checks(db, out):
    tables = {t: db.execute(f"SELECT count(*) FROM {t}").fetchone()[0] for t in TABLES}
    assert list(tables.values()) == EXPECTED
    prompts = db.execute(
        "SELECT count(*) FILTER(WHERE prompt<>''),count(DISTINCT "
        "prompt) FILTER(WHERE prompt<>''),count(*) FILTER(WHERE "
        "prompt=''),count(*) FILTER(WHERE prompt IS NULL) FROM "
        "generations"
    ).fetchone()
    assert prompts == (124642, 61479, 1083, 5174)
    result = {
        "release": "data-2026-10-20",
        "table_rows": tables,
        "primary_prompts_all_158": dict(
            zip(
                ["nonempty", "distinct_nonempty", "empty", "unavailable"],
                prompts,
                strict=True,
            )
        ),
        "generation_types_all_158": db.execute(
            "SELECT generation_type,count(*) AS jobs FROM generations "
            "GROUP BY 1 ORDER BY 1"
        )
        .fetchdf()
        .where(lambda x: x.notna(), None)
        .to_dict("records"),
        "generation_statuses_all_158": db.execute(
            "SELECT generation_status,count(*) AS jobs FROM generations "
            "GROUP BY 1 ORDER BY 1"
        )
        .fetchdf()
        .to_dict("records"),
    }
    (out / "snapshot_checks.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )
    counts = db.execute(
        "SELECT p.cohort_group,g.film_id,g.model_identifier,count(*) "
        "AS jobs FROM generations g JOIN population p USING(film_id) "
        "WHERE p.population='primary' GROUP BY ALL"
    ).fetchdf()
    metrics = db.execute(
        "SELECT film_id,cohort_group,generations FROM profile WHERE "
        "population='primary'"
    ).fetchdf()
    rows = []
    for group, base in [("primary", metrics), *list(metrics.groupby("cohort_group"))]:
        subset = counts[counts.film_id.isin(base.film_id)].merge(
            base[["film_id", "generations"]], on="film_id"
        )
        for model, sample in subset.groupby("model_identifier"):
            sample = sample.sort_values("film_id")
            rows.append(
                {
                    "cohort_group": group,
                    "model_identifier": model,
                    "jobs": int(sample.jobs.sum()),
                    "job_denominator": int(base.generations.sum()),
                    "films_with_model": len(sample),
                    "film_denominator": len(base),
                    "mean_per_film_share": (sample.jobs / sample.generations).sum()
                    / len(base),
                }
            )
    pd.DataFrame(rows).to_csv(out / "model_weights.csv", index=False)
