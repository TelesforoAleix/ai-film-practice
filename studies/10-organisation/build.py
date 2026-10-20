"""Reproduce Study 10 from the verified snapshot and frozen Study 01/case registers."""

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

import pandas as pd

from film_practice import connect

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NULL = r"\N"
ALTERNATIVE = (
    "Public histories can omit external, private or discarded work and include work "
    "outside this entry; authors are accounts, placements are occurrences; "
    "reuse is not approval."
)
CONFIDENCE = (
    "Deterministic aggregate over film-scoped released records; exact-string/raw-ID "
    "definitions only. No semantic accuracy, causal benefit or labour estimate."
)


def read_csv(path):
    return pd.read_csv(path, keep_default_na=False, na_values=[NULL])


def write_csv(frame, path):
    frame.to_csv(
        path, index=False, na_rep=NULL, float_format="%.9f", lineterminator="\n"
    )


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def owners(raw):
    """Only a literal boolean owner declaration establishes a recorded owner ID."""
    if raw is None or raw == "":
        return None
    try:
        value = json.loads(raw)
    except (ValueError, TypeError):
        return None
    if not isinstance(value, list):
        return None
    result = {
        x["id"]
        for x in value
        if isinstance(x, dict)
        and x.get("is_owner") is True
        and isinstance(x.get("id"), str)
        and x["id"]
    }
    return result or None


def ratio(numerator, denominator):
    return numerator / denominator if denominator > 0 else None


def summaries(frame):
    """Equal-film and pooled shares, with member sets and paired denominators."""
    measures = {
        "repeat_share": ("repeat_excess", "prompt_nonempty"),
        "multiple_placement_share": ("multiply_placed_jobs", "jobs"),
        "reused_input_share": ("reused_input_assets", "input_assets"),
        "cross_author_share": ("cross_author_pairs", "authored_job_pairs"),
        "disjoint_folder_share": ("disjoint_folder_pairs", "placed_job_pairs"),
        "owner_job_share": ("owner_jobs", "owner_comparable_jobs"),
    }
    rows = []
    groups = [("all", "primary", frame)]
    for dimension in [
        "cohort_group",
        "record_orientation",
        "scale",
        "organisation_proxy",
    ]:
        groups.extend(
            (dimension, str(value), group)
            for value, group in frame.groupby(dimension, sort=True)
        )
    for dimension, value, group in groups:
        common = dict(
            dimension=dimension,
            value=value,
            films=len(group),
            film_ids=json.dumps(sorted(group.film_id)),
            study="10",
            evidence_label="observed",
            source_path="measures.sql; film_metrics.csv",
            competing_explanation=ALTERNATIVE,
            confidence_rationale=CONFIDENCE,
        )
        for metric, (n, d) in measures.items():
            valid = group[group[d].notna() & (group[d] > 0)]
            shares = valid[n] / valid[d]
            rows.append(
                dict(
                    common,
                    metric=metric,
                    measured_films=len(valid),
                    numerator=int(valid[n].sum()),
                    denominator=int(valid[d].sum()),
                    equal_film_mean=shares.mean(),
                    median=shares.median(),
                    q25=shares.quantile(0.25),
                    q75=shares.quantile(0.75),
                    pooled_share=ratio(valid[n].sum(), valid[d].sum()),
                )
            )
        for metric in ["jobs", "folders", "event_span_days", "active_utc_dates"]:
            values = group[metric].dropna()
            rows.append(
                dict(
                    common,
                    metric=metric,
                    measured_films=len(values),
                    numerator=values.sum(),
                    denominator=len(values),
                    equal_film_mean=values.mean(),
                    median=values.median(),
                    q25=values.quantile(0.25),
                    q75=values.quantile(0.75),
                    pooled_share=None,
                )
            )
    return pd.DataFrame(rows)


def build(data, output):
    output.mkdir(parents=True, exist_ok=True)
    upstream = ROOT / "studies/01-corpus/outputs"
    eligibility = read_csv(upstream / "eligibility.csv")
    eligible = eligibility[
        (eligibility.study.astype(str) == "10")
        & (eligibility.population == "primary")
        & (eligibility.production_eligible.astype(str) == "True")
    ]
    eligible = eligible[["film_id", "cohort_group"]].sort_values("film_id")
    assert len(eligible) == 157 and eligible.film_id.is_unique
    taxonomy = read_csv(upstream / "taxonomy.csv")
    baseline = read_csv(upstream / "film_metrics.csv")
    case_rows = []
    for path in sorted((ROOT / "case-files").glob("*/codes.csv")):
        for row in csv.DictReader(path.open()):
            if row["code_id"].startswith("10."):
                row["case_source"] = path.relative_to(ROOT).as_posix()
                case_rows.append(row)
    cases = pd.DataFrame(case_rows)
    assert len(cases) == 80 and cases.film_id.nunique() == 16
    with connect(data) as db:
        db.execute("SET TimeZone='UTC'")
        db.register("eligible", eligible)
        db.execute((HERE / "measures.sql").read_text())
        film = db.sql(
            "SELECT * EXCLUDE(film_id_1) FROM film_measures ORDER BY film_id"
        ).df()
        owner_map = {
            fid: owners(raw)
            for fid, raw in db.sql(
                "SELECT film_id, authors_json FROM films JOIN eligible USING(film_id)"
            ).fetchall()
        }
        for row in cases[cases.code_id == "10.1"].to_dict("records"):
            names = db.execute(
                "SELECT folder_name FROM folders WHERE film_id=? ORDER BY folder_id",
                [row["film_id"]],
            ).fetchall()
            assert row["excerpt"] == "; ".join(n[0] for n in names)
        author = db.sql("""SELECT film_id, author_user_id, generation_type,
          model_identifier, count(*) AS jobs FROM j GROUP BY ALL
          ORDER BY film_id, author_user_id, generation_type, model_identifier""").df()
        author["recorded_owner"] = [
            None
            if owner_map[fid] is None or pd.isna(uid) or uid == ""
            else uid in owner_map[fid]
            for fid, uid in zip(author.film_id, author.author_user_id, strict=True)
        ]
        owner_jobs = author[author.recorded_owner == True].groupby("film_id").jobs.sum()  # noqa: E712
        film["owner_ids_disclosed"] = film.film_id.map(
            lambda fid: len(owner_map[fid]) if owner_map[fid] is not None else None
        )
        film["owner_jobs"] = film.film_id.map(owner_jobs).fillna(0).astype(int)
        film.loc[film.owner_ids_disclosed.isna(), "owner_jobs"] = None
        film["owner_comparable_jobs"] = film.authored.where(
            film.owner_ids_disclosed.notna()
        )
        film["nonowner_id_jobs"] = film.owner_comparable_jobs - film.owner_jobs
        # One cross-author asset edge per film; no semantic handoff label.
        traces = db.sql("""SELECT * FROM edges WHERE producer_author<>consumer_author
          AND nullif(producer_author,'') IS NOT NULL
          AND nullif(consumer_author,'') IS NOT NULL
          QUALIFY row_number() OVER(
            PARTITION BY film_id ORDER BY producer,consumer,asset_id)=1
          ORDER BY film_id""").df()
        for dimension in ["generation_type", "model_identifier"]:
            part = db.sql(f"""SELECT film_id, {dimension} AS value, count(*) AS jobs,
              count(*) FILTER(WHERE prompt<>'') AS prompt_nonempty,
              count(*) FILTER(WHERE prompt<>'')-count(DISTINCT prompt)
                FILTER(WHERE prompt<>'') AS repeat_excess,
              count(DISTINCT nullif(author_user_id,'')) AS authors
              FROM j GROUP BY ALL ORDER BY film_id,value""").df()
            part = part.merge(
                film[["film_id", "cohort_group", "jobs"]],
                on="film_id",
                suffixes=("", "_film_denominator"),
            )
            part["job_share"] = part.jobs / part.jobs_film_denominator
            write_csv(part, output / f"by_{dimension}.csv")
            comparisons = []
            for cohort, members in [("all", film), *film.groupby("cohort_group")]:
                selected = part[part.film_id.isin(members.film_id)]
                for value, group in selected.groupby("value", dropna=False, sort=True):
                    measured = group[group.prompt_nonempty > 0]
                    comparisons.append(
                        dict(
                            dimension=dimension,
                            value=value,
                            cohort_group=cohort,
                            films_with_jobs=len(group),
                            film_denominator=len(members),
                            jobs=int(group.jobs.sum()),
                            job_denominator=int(members.jobs.sum()),
                            equal_film_job_share=group.job_share.sum() / len(members),
                            pooled_job_share=group.jobs.sum() / members.jobs.sum(),
                            repeat_excess=int(group.repeat_excess.sum()),
                            nonempty_denominator=int(group.prompt_nonempty.sum()),
                            repeat_measured_films=len(measured),
                            equal_measured_film_repeat_share=(
                                measured.repeat_excess / measured.prompt_nonempty
                            ).mean(),
                            film_ids=json.dumps(sorted(group.film_id)),
                        )
                    )
            write_csv(pd.DataFrame(comparisons), output / f"summary_{dimension}.csv")
    film = film.merge(
        taxonomy[["film_id", "record_orientation", "scale", "organisation_proxy"]],
        on="film_id",
        validate="one_to_one",
    )
    film["jobs_per_declared_minute"] = (
        film.jobs * 60 / film.declared_seconds.where(film.declared_seconds > 0)
    )
    film["format_comparability"] = "unavailable; category=[] is not format"
    film["unusual_project"] = film.film_id.isin(
        read_csv(upstream / "unusual_projects.csv").film_id
    )
    for row in cases[cases.code_id == "10.4"].to_dict("records"):
        measured = film.set_index("film_id").loc[row["film_id"]]
        values = dict(re.findall(r"(\w+)=(\d+)", row["excerpt"]))
        for key, column in {
            "nonempty": "prompt_nonempty",
            "distinct_nonempty": "distinct_nonempty",
            "repeat_occurrences_beyond_first": "repeat_excess",
            "jobs_in_multiple_folders": "multiply_placed_jobs",
        }.items():
            assert int(values[key]) == measured[column]
    for name, baseline_name in [
        ("jobs", "generations"),
        ("authored", "authored"),
        ("folders", "folders"),
        ("dated", "dated"),
    ]:
        check = film.merge(
            baseline[["film_id", baseline_name]],
            on="film_id",
            suffixes=("", "_baseline"),
        )
        other = baseline_name + "_baseline" if baseline_name == name else baseline_name
        assert (check[name] == check[other]).all(), name
    author = author.merge(
        film[["film_id", "jobs", "authored"]],
        on="film_id",
        suffixes=("", "_film_denominator"),
    )
    author["jobs_author_denominator"] = author.groupby(
        ["film_id", "author_user_id"], dropna=False
    ).jobs.transform("sum")
    author["share_within_author"] = author.jobs / author.jobs_author_denominator
    write_csv(author, output / "author_operations.csv")
    write_csv(film, output / "film_metrics.csv")
    write_csv(cases, output / "case_evidence.csv")
    write_csv(summaries(film), output / "summaries.csv")
    panel = read_csv(upstream / "panel.csv")[["film_id", "pair", "matched_film_id"]]
    semantic = cases[cases.code_id == "10.1"][["film_id", "value", "evidence_id"]]
    write_csv(
        panel.merge(semantic, on="film_id").merge(film, on="film_id"),
        output / "panel_comparison.csv",
    )
    ledger = []
    for row in film.to_dict("records"):
        fid = row["film_id"]
        ledger.append(
            dict(
                study="10",
                film_id=fid,
                entity_ids=f"{fid}/film:{fid}; all compound keys in scope",
                source_path="measures.sql; generations; folders; generation_folders; "
                "asset_folders; asset_usages; assets.generation_id; "
                "films.duration/authors_json; Study 01 taxonomy",
                excerpt=json.dumps(row, default=str, sort_keys=True),
                evidence_label="observed",
                competing_explanation=ALTERNATIVE,
                denominator=f"{row['jobs']} jobs; "
                f"{row['prompt_nonempty']} nonempty primary fields; "
                f"{row['input_assets']} raw input IDs; "
                f"{row['authored_job_pairs']} authored pairs; "
                f"{row['placed_job_pairs']} placed pairs; "
                f"{row['declared_seconds']} declared seconds; "
                "other denominator columns in excerpt; taxonomy separately inferred",
                confidence_rationale=CONFIDENCE,
            )
        )
    write_csv(pd.DataFrame(ledger), output / "metric_evidence.csv")
    for column, value in [
        ("study", "10"),
        ("evidence_label", "observed"),
        (
            "source_path",
            "assets.generation_id; asset_usages; generations.author_user_id",
        ),
        ("competing_explanation", ALTERNATIVE),
        ("confidence_rationale", CONFIDENCE),
    ]:
        traces[column] = value
    traces = traces.merge(
        film[["film_id", "authored_job_pairs", "cross_author_pairs"]], on="film_id"
    )
    traces["denominator"] = (
        "One lexicographically first cross-author edge per film; pair totals beside it"
    )
    traces["excerpt"] = (
        "Explicit producer asset consumed under a different recorded author ID"
    )
    write_csv(traces, output / "cross_author_examples.csv")
    inputs = [HERE / "build.py", HERE / "measures.sql", ROOT / "PROGRAMME.md"]
    inputs += [
        upstream / f"{x}.csv"
        for x in [
            "eligibility",
            "taxonomy",
            "film_metrics",
            "unusual_projects",
            "panel",
        ]
    ]
    inputs += sorted((ROOT / "case-files").glob("*/codes.csv"))
    manifest = dict(
        release="data-2026-10-20",
        source_manifest_sha256=digest(Path(data) / "SHA256SUMS"),
        inputs={p.relative_to(ROOT).as_posix(): digest(p) for p in inputs},
        outputs={p.name: digest(p) for p in sorted(output.glob("*.csv"))},
    )
    (output / "reproduction.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    assert all(p.stat().st_size < 1_000_000 for p in output.iterdir())
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, default=HERE / "outputs")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare fresh build with committed outputs",
    )
    args = parser.parse_args()
    if args.check and args.output.resolve() == (HERE / "outputs").resolve():
        parser.error("--check requires a separate --output directory")
    manifest = build(args.data, args.output)
    if args.check:
        for name in [*manifest["outputs"], "reproduction.json"]:
            assert (args.output / name).read_bytes() == (
                HERE / "outputs" / name
            ).read_bytes(), name
    print(f"Study 10: 157 films; {len(manifest['outputs'])} outputs reproduced.")


if __name__ == "__main__":
    main()
