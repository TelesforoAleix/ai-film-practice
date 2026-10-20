"Reproduce Study 01 metadata outputs from the frozen release; no network access."

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import pandas as pd
from calibration import calibrate
from codebook_source import CODES
from eligibility import eligibility
from evidence import aggregates
from quality import checks

from film_practice import TABLES, connect

HERE = Path(__file__).resolve().parent
INTEGER = set(
    (
        "most_watched_rank_top100 views likes comments "
        "audience_votes reported_generations item_count "
        "subfolders_count usage_count folders_found "
        "generations_found assets_found items_received"
    ).split()
)
FLOAT = {"duration", "usage_percentage"}
BOOLEAN = set(
    (
        "in_priority_scope is_open_source show_prompts prompt_hidden "
        "items_complete folders_complete generation_count_reconciles "
        "brief_complete leaf_recovery_complete"
    ).split()
)
DATES = {"submitted_at", "created_at", "extraction_timestamp"}
JSON_FIELDS = set(
    (
        "category shortlist_status model_usage_summary authors_json "
        "parameters_json metadata_json missing_fields errors "
        "leaf_recovery_errors"
    ).split()
)
KEYS = {
    "films": ["film_id"],
    "priority_films": ["film_id"],
    "folders": ["film_id", "folder_id"],
    "generations": ["film_id", "generation_id"],
    "generation_prompts": ["film_id", "generation_id", "field_path"],
    "assets": ["film_id", "asset_id"],
    "asset_usages": [
        "film_id",
        "generation_id",
        "asset_id",
        "asset_role",
        "parameter_path",
    ],
    "asset_folders": ["film_id", "asset_id", "folder_id"],
    "generation_folders": ["film_id", "generation_id", "folder_id"],
    "reference_elements": ["film_id", "reference_element_id"],
    "brief_assets": ["film_id", "embedding_id"],
    "model_usage": ["film_id", "model_identifier"],
    "extraction_log": ["film_id"],
    "other_items": ["film_id", "record_hash"],
}


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def state(nonempty, empty, total, accessible=True):
    "Availability describes exported evidence, never the creator's behaviour."
    if not accessible or total is None:
        return "unavailable"
    if nonempty:
        return "available"
    if empty or total == 0:
        return "empty"
    return "unavailable"


def walk(value, path="$"):
    kind = (
        "null"
        if value is None
        else "boolean"
        if isinstance(value, bool)
        else "object"
        if isinstance(value, dict)
        else "array"
        if isinstance(value, list)
        else "number"
        if isinstance(value, (int, float))
        else "string"
    )
    yield path, kind, value == "" if isinstance(value, str) else False
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, path + "." + key)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child, path + "[*]")


def dictionary(db, out):
    columns, paths, grains = [], [], []
    for table in TABLES:
        schema = db.execute(f"DESCRIBE {table}").fetchall()
        n = db.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        keys = KEYS[table]
        key_sql = ",".join('"' + k + '"' for k in keys)
        distinct = db.execute(
            f"SELECT count(*) FROM (SELECT DISTINCT {key_sql} FROM {table})"
        ).fetchone()[0]
        grains.append(
            {
                "table": table,
                "rows": n,
                "candidate_key": keys,
                "distinct_candidate_keys": distinct,
                "grain_note": "Occurrence grain; not an entity key"
                if table == "asset_usages"
                else "Snapshot candidate key; retain film scope",
            }
        )
        for name, *_ in schema:
            q = '"' + name + '"'
            null, empty = db.execute(
                f"SELECT count(*) FILTER(WHERE {q} IS NULL), "
                f"count(*) FILTER(WHERE {q}='') FROM {table}"
            ).fetchone()
            typ = (
                "JSON"
                if name in JSON_FIELDS
                and (name != "category" or table in ("films", "priority_films"))
                else "BIGINT"
                if name in INTEGER
                else "DOUBLE"
                if name in FLOAT
                else "BOOLEAN"
                if name in BOOLEAN
                else "TIMESTAMPTZ"
                if name in DATES
                else "VARCHAR"
            )
            invalid = 0
            if typ == "JSON":
                invalid = db.execute(
                    f"SELECT count(*) FROM {table} WHERE {q} IS NOT NULL "
                    f"AND {q}<>'' AND NOT json_valid({q})"
                ).fetchone()[0]
            if typ not in ("VARCHAR", "JSON"):
                invalid = db.execute(
                    f"SELECT count(*) FROM {table} WHERE {q} IS NOT NULL "
                    f"AND {q}<>'' AND try_cast({q} AS {typ}) IS NULL"
                ).fetchone()[0]
            columns.append(
                {
                    "table": table,
                    "column": name,
                    "derived_type": typ,
                    "rows": n,
                    "nulls_unavailable": null,
                    "empty_strings": empty,
                    "invalid_casts": invalid,
                    "handling": "Retain raw and empty text; NULL remains unavailable"
                    if typ == "VARCHAR"
                    else (
                        "Retain raw; derived empty=>NULL with explicit empty flag; "
                        "invalid=>NULL with invalid flag"
                    ),
                    "key_member": name in keys,
                }
            )
            if typ == "JSON":
                counts, documents = Counter(), Counter()
                empty_counts = Counter()
                cursor = db.execute(
                    f"SELECT {q} FROM {table} WHERE {q} IS NOT NULL AND {q}<>''"
                )
                while batch := cursor.fetchmany(500):
                    for (text,) in batch:
                        try:
                            obj = json.loads(text)
                        except json.JSONDecodeError:
                            # Invalid JSON stays raw and counted, never repaired.
                            continue
                        seen = set()
                        for path, kind, is_empty in walk(obj):
                            counts[path, kind] += 1
                            empty_counts[path, kind] += is_empty
                            seen.add((path, kind))
                        documents.update(seen)
                for (path, kind), count in sorted(counts.items()):
                    paths.append(
                        {
                            "table": table,
                            "column": name,
                            "path": path,
                            "json_type": kind,
                            "occurrences": count,
                            "documents": documents[path, kind],
                            "table_rows": n,
                            "empty_strings": empty_counts[path, kind],
                        }
                    )
    pd.DataFrame(columns).to_csv(out / "dictionary.csv", index=False)
    pd.DataFrame(paths).to_csv(out / "json_paths.csv", index=False)
    write_json(out / "grains.json", grains)


def profile(db, out):
    db.execute((HERE / "profile.sql").read_text())
    frame = db.execute("SELECT * FROM profile ORDER BY film_id").fetchdf()
    # Missing workspace collections remain unavailable, even though SQL count
    # over absent rows yields zero. Catalogue asset entities remain observable.
    inaccessible = ~frame.population.isin(("primary", "supplemental"))
    for col in (
        "folders",
        "reference_elements",
        "nested_text_fields",
        "brief_embeddings",
    ):
        frame[col] = frame[col].astype("Int64")
        frame.loc[inaccessible, col] = pd.NA
    frame.to_csv(out / "film_metrics.csv", index=False, na_rep="\\N")
    coverage = []
    for row in frame.to_dict("records"):
        fid = row["film_id"]
        accessible = row["population"] in ("primary", "supplemental")
        result = {k: row[k] for k in ("film_id", "title", "population", "cohort_group")}
        n = int(row["generations"]) if pd.notna(row["generations"]) else None
        result["briefs"] = state(
            row["brief_disclosed"] and not row["brief_explicitly_empty"],
            row["brief_explicitly_empty"] is True,
            1,
        )
        for label, count in [
            ("prompt_fields", "prompt_nonempty"),
            ("dates", "dated"),
            ("authors", "authored"),
            ("inputs", "jobs_with_inputs"),
            ("outputs", "jobs_with_outputs"),
        ]:
            value = row[count]
            total = n
            if label in ("inputs", "outputs") and accessible and pd.isna(value):
                value, total = 0, 0
            result[label] = state(
                0 if pd.isna(value) else value,
                row["prompt_empty"]
                if label == "prompt_fields"
                else (value == 0 if label in ("inputs", "outputs") else 0),
                total,
                accessible,
            )
        for label, col in [
            ("references", "reference_elements"),
            ("folders", "folders"),
            ("nested_text", "nested_text_fields"),
            ("brief_assets", "brief_embeddings"),
        ]:
            result[label] = state(row[col], 0, row[col], accessible)
        result["brief_decoding"] = (
            "available" if row["brief_complete"] == "True" else "unavailable"
        )
        coverage.append(result)
    pd.DataFrame(coverage).to_csv(out / "coverage.csv", index=False)
    taxonomy = frame[
        [
            "film_id",
            "title",
            "population",
            "cohort_group",
            "declared_duration_seconds",
            "declared_category_json",
            "generations",
            "models",
            "reference_elements",
            "folders",
        ]
    ].copy()
    taxonomy["record_orientation"] = frame.apply(
        lambda r: (
            "unavailable"
            if pd.isna(r.generations)
            else "image_led"
            if r.image_jobs / r.generations >= 0.7
            else "film_led"
            if r.video_jobs / r.generations >= 0.7
            else "mixed"
        ),
        axis=1,
    )
    taxonomy["scale"] = frame.generations.map(
        lambda n: (
            "unavailable"
            if pd.isna(n)
            else "small"
            if n < 200
            else "medium"
            if n < 1000
            else "large"
            if n < 3000
            else "very_large"
        )
    )
    taxonomy["model_breadth"] = frame.models.map(
        lambda n: (
            "unavailable"
            if pd.isna(n)
            else "narrow"
            if n <= 3
            else "moderate"
            if n <= 8
            else "broad"
        )
    )
    taxonomy["organisation_proxy"] = frame.apply(
        lambda r: (
            "unavailable"
            if r.population not in ("primary", "supplemental")
            else "flat"
            if r.folders <= 2
            else "partitioned"
        ),
        axis=1,
    )
    taxonomy["reference_proxy"] = frame.apply(
        lambda r: (
            "unavailable"
            if r.population not in ("primary", "supplemental")
            else "disclosed"
            if r.reference_elements
            else "none_exported"
        ),
        axis=1,
    )
    taxonomy["evidence_label"] = "inferred"
    taxonomy["source_path"] = "profile.sql; README.md section 3 thresholds"
    taxonomy["denominator"] = "One film; orientation divides by recorded jobs"
    taxonomy.to_csv(out / "taxonomy.csv", index=False, na_rep="\\N")
    counts = {
        "catalogue": db.execute("SELECT count(*) FROM films").fetchone()[0],
        "priority": db.execute("SELECT count(*) FROM priority_films").fetchone()[0],
        "shortlisted": db.execute(
            "SELECT count(*) FROM priority_films WHERE "
            "json_contains(shortlist_status, '\"audience_choice\"')"
        ).fetchone()[0],
        "most_watched": db.execute(
            "SELECT count(*) FROM priority_films WHERE "
            "most_watched_rank_top100 IS NOT NULL"
        ).fetchone()[0],
        "populations": frame.groupby("population").size().to_dict(),
        "cohorts_by_population": frame.groupby(["population", "cohort_group"])
        .size()
        .reset_index(name="films")
        .to_dict("records"),
        "generations_all": db.execute("SELECT count(*) FROM generations").fetchone()[0],
        "generation_films": db.execute(
            "SELECT count(DISTINCT film_id) FROM generations"
        ).fetchone()[0],
    }
    assert counts["catalogue"] == 6224 and len(frame) == 187
    assert counts["populations"] == {
        "excluded": 23,
        "primary": 157,
        "supplemental": 1,
        "unavailable": 6,
    }
    write_json(out / "populations.json", counts)
    primary = frame[frame.population == "primary"]
    dist = []
    for group, sample in [("primary", primary), *list(primary.groupby("cohort_group"))]:
        for col in [
            "generations",
            "models",
            "folders",
            "reference_elements",
            "declared_duration_seconds",
        ]:
            values = pd.to_numeric(sample[col], errors="coerce").dropna()
            dist.append(
                {
                    "group": group,
                    "measure": col,
                    "eligible_films": len(sample),
                    "measured_films": len(values),
                    "min": values.min(),
                    "p25": values.quantile(0.25),
                    "median": values.median(),
                    "p75": values.quantile(0.75),
                    "p95": values.quantile(0.95),
                    "max": values.max(),
                    "sum": values.sum(),
                }
            )
    pd.DataFrame(dist).to_csv(out / "distributions.csv", index=False)
    for dimension in ["generation_type", "model_identifier", "author_user_id"]:
        # Author IDs retained; no names or profile metadata required.
        db.execute(
            f"SELECT p.cohort_group,g.film_id,g.{dimension}, "
            "count(*) AS generations FROM generations g "
            "JOIN population p USING(film_id) WHERE p.population='primary' "
            "GROUP BY ALL ORDER BY 1,2,3"
        ).fetchdf().to_csv(out / f"by_{dimension}.csv", index=False, na_rep="\\N")
    for dimension in ["creator", "declared_duration_seconds", "declared_category_json"]:
        primary[["film_id", "cohort_group", dimension, "generations"]].to_csv(
            out / f"by_{dimension}.csv", index=False, na_rep="\\N"
        )
    rare = set(
        db.execute(
            "SELECT DISTINCT film_id FROM generations WHERE "
            "generation_type IS NULL OR generation_type IN "
            "('text','image_3d')"
        )
        .fetchdf()
        .film_id
    )
    audit = primary[
        (primary.film_id.isin(rare))
        | (primary.generations <= primary.generations.quantile(0.05))
        | (
            pd.to_numeric(primary.declared_duration_seconds)
            >= pd.to_numeric(primary.declared_duration_seconds).quantile(0.95)
        )
        | (primary.generations >= primary.generations.quantile(0.95))
        | (primary.models >= primary.models.quantile(0.95))
        | (primary.folders >= primary.folders.quantile(0.95))
        | (primary.authors > 1)
    ].copy()
    audit["audit_triggers"] = audit.apply(
        lambda r: "|".join(
            k
            for k, yes in {
                "jobs_p95": r.generations >= primary.generations.quantile(0.95),
                "jobs_p05": r.generations <= primary.generations.quantile(0.05),
                "models_p95": r.models >= primary.models.quantile(0.95),
                "folders_p95": r.folders >= primary.folders.quantile(0.95),
                "multiple_authors": r.authors > 1,
                "rare_or_missing_job_type": r.film_id in rare,
                "duration_p95": float(r.declared_duration_seconds)
                >= pd.to_numeric(primary.declared_duration_seconds).quantile(0.95),
            }.items()
            if yes
        ),
        axis=1,
    )
    audit["audit_result"] = (
        "Compound generation grain; source count reconciles="
        + audit.generation_count_reconciles.fillna("unavailable")
    )
    audit["alternative"] = (
        "Large shared/external history may exceed festival-specific "
        "work; breadth does not establish specialisation; authors do "
        "not establish team structure"
    )
    audit.to_csv(out / "unusual_projects.csv", index=False, na_rep="\\N")
    # Explicit denominator and evidence metadata for each per-film metric row.
    ledger = []
    for row in frame.to_dict("records"):
        ledger.append(
            {
                "study": "01",
                "film_id": row["film_id"],
                "entity_ids": "All compound keys in the named tables for this film",
                "source_path": (
                    "profile.sql: population/jobs/usage_counts/profile; "
                    "published Parquet views"
                ),
                "excerpt": "; ".join(
                    f"{k}={row[k]}"
                    for k in [
                        "population",
                        "cohort_group",
                        "generations",
                        "models",
                        "folders",
                        "reference_elements",
                    ]
                ),
                "evidence_label": "observed",
                "competing_explanation": (
                    "Export completeness is not completeness of the creative "
                    "production; catalogue assets and summary counts have "
                    "different grains"
                ),
                "denominator": (
                    "One film; job proportions use this film generations; "
                    "primary summaries use 157 films and 130704 jobs"
                ),
                "confidence_rationale": (
                    "Deterministic compound-key aggregates of a "
                    "checksum-verified snapshot; no raw responses available to "
                    "revalidate collection"
                ),
            }
        )
    pd.DataFrame(ledger).to_csv(out / "metric_evidence.csv", index=False)
    invalid = db.execute(
        "SELECT film_id,generation_id,prompt_source_path,source_recor"
        "d_file FROM generations WHERE parameters_json IS NOT NULL "
        "AND NOT json_valid(parameters_json) ORDER BY "
        "film_id,generation_id"
    ).fetchdf()
    invalid["source_path"] = "generations.parameters_json"
    invalid["handling"] = (
        "Raw retained; JSON-derived values unavailable; "
        "independently exported fields still usable"
    )
    invalid.to_csv(out / "invalid_json.csv", index=False)
    weights = []
    for kind in ["image", "video", "audio", "image_3d", "text", None]:
        predicate = (
            "g.generation_type IS NULL"
            if kind is None
            else "g.generation_type='" + kind + "'"
        )
        result = db.execute(
            "SELECT p.cohort_group,g.film_id,count(*) AS n "
            "FROM generations g JOIN population p USING(film_id) "
            f"WHERE p.population='primary' AND ({predicate}) GROUP BY ALL"
        ).fetchdf()
        for group, base in [
            ("primary", primary),
            *list(primary.groupby("cohort_group")),
        ]:
            subset = result[result.film_id.isin(base.film_id)]
            shares = (
                base[["film_id", "generations"]]
                .merge(subset[["film_id", "n"]], how="left")
                .fillna({"n": 0})
            )
            weights.append(
                {
                    "cohort_group": group,
                    "generation_type": kind or "unavailable",
                    "jobs": int(shares.n.sum()),
                    "job_denominator": int(base.generations.sum()),
                    "film_denominator": len(base),
                    "mean_per_film_share": (shares.n / shares.generations).mean(),
                }
            )
    pd.DataFrame(weights).to_csv(out / "generation_weights.csv", index=False)
    pairs = json.loads((HERE / "panel.json").read_text())
    panel = []
    for pair in pairs:
        for fid in pair["films"]:
            row = frame[frame.film_id == fid].iloc[0]
            assert row.population == "primary"
            panel.append(
                {
                    **{
                        k: row[k]
                        for k in [
                            "film_id",
                            "title",
                            "cohort_group",
                            "generations",
                            "models",
                            "folders",
                            "reference_elements",
                        ]
                    },
                    "pair": pair["pair"],
                    "matched_film_id": next(x for x in pair["films"] if x != fid),
                    "selection_reason": pair["match"] + "; " + pair["contrast"],
                    "replacement": "none",
                    "replacement_reason": (
                        "Initial register; no replacement has occurred"
                    ),
                }
            )
    assert len({r["film_id"] for r in panel}) == 16
    # Largest first; assign to the least loaded batch with space, deterministic ties.
    loads, sizes = [0] * 4, [0] * 4
    for row in sorted(panel, key=lambda r: (-r["generations"], r["film_id"])):
        batch = min((i for i in range(4) if sizes[i] < 4), key=lambda i: (loads[i], i))
        row["batch"] = batch + 1
        loads[batch] += int(row["generations"])
        sizes[batch] += 1
    pd.DataFrame(sorted(panel, key=lambda r: (r["batch"], r["film_id"]))).to_csv(
        out / "panel.csv", index=False
    )
    return frame, taxonomy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default="data")
    parser.add_argument("--output", type=Path, default=HERE / "outputs")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    with connect(args.data) as db:
        dictionary(db, args.output)
        frame, _ = profile(db, args.output)
        eligibility(frame, args.output)
        checks(db, args.output)
        aggregates(frame, args.output)
        calibrate(db, args.output)
        pd.DataFrame(
            CODES,
            columns=[
                "code_id",
                "study",
                "name",
                "values",
                "inclusion",
                "exclusion_ambiguity",
            ],
        ).to_csv(args.output / "codebook.csv", index=False)
    manifest = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(args.output.iterdir())
        if p.suffix in (".csv", ".json") and p.name != "reproduction.json"
    }
    write_json(args.output / "reproduction.json", manifest)
    print(f"Reproduced {len(manifest)} outputs.")


if __name__ == "__main__":
    main()
