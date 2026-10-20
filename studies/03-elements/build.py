"""Study 03: disclosed elements, structural channels and scoped panel evidence."""

import argparse
import csv
import hashlib
import importlib.util
import json
import re
from functools import cache
from pathlib import Path

import pandas as pd

from film_practice import connect

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NULL = r"\N"
ALTERNATIVE = (
    "Disclosed metadata is not a complete library; raw IDs can alias and shared "
    "inputs can serve different entities/tasks. English lexical matches can be "
    "quoted, negated or miss other languages. External/private work is omitted; "
    "attachments and requests do not establish media content or approval."
)
CONFIDENCE = (
    "Exact deterministic count of compound-key exported records under stated "
    "scope; no semantic accuracy, independent-coder agreement or causal estimate."
)
RATIOS = [
    ("input_jobs", "jobs"),
    ("named_reference_jobs", "jobs"),
    ("multiple_reference_jobs", "jobs"),
    ("resolved_input_jobs", "input_jobs"),
    ("reference_token_jobs", "prompt_nonempty"),
    ("preservation_jobs", "prompt_nonempty"),
    ("preservation_with_input", "preservation_jobs"),
    ("token_with_named_reference", "reference_token_jobs"),
    ("used_elements", "elements"),
    ("reused_elements", "elements"),
    ("multi_asset_elements", "elements"),
    ("reused_input_assets", "input_asset_ids"),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path):
    return pd.read_csv(path, keep_default_na=False, na_values=[NULL])


def write_json(path, value):
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    )


def write_csv(frame, path):
    frame.to_csv(
        path, index=False, na_rep=NULL, float_format="%.9f", lineterminator="\n"
    )


def provenance(fid, entity, source, excerpt, denominator, label="observed"):
    return dict(
        study="03",
        film_id=fid,
        entity_ids=entity,
        source_path=source,
        excerpt=excerpt,
        evidence_label=label,
        competing_explanation=ALTERNATIVE,
        denominator=denominator,
        confidence_rationale=CONFIDENCE,
    )


def field_state(value):
    return "unavailable" if value is None else "empty" if value == "" else "nonempty"


def reference_state(raw):
    """Document/key/container states; values never imply attachment or activation."""
    if raw is None:
        return "unavailable"
    if raw == "":
        return "empty_document"
    try:
        obj = json.loads(raw)
    except (ValueError, TypeError):
        return "invalid_json"
    if not isinstance(obj, dict):
        return "other_document"
    if "reference_elements" not in obj:
        return "absent"
    value = obj["reference_elements"]
    if value is None:
        return "null"
    if isinstance(value, list):
        return "nonempty_array" if value else "empty_array"
    return "other_value"


def aggregate(frame, dimensions):
    rows = []
    groups = [("all", "primary", frame)]
    for dimension in dimensions:
        groups += [
            (dimension, None if pd.isna(v) else str(v), g)
            for v, g in frame.groupby(dimension, dropna=False, sort=True)
        ]
    for dimension, value, group in groups:
        for numerator, denominator in RATIOS:
            if numerator not in group or denominator not in group:
                continue
            valid = group[group[denominator] > 0]
            shares = valid[numerator] / valid[denominator]
            n, d = int(valid[numerator].sum()), int(valid[denominator].sum())
            rows.append(
                dict(
                    dimension=dimension,
                    value=value,
                    metric=numerator,
                    eligible_films=len(group),
                    measured_films=len(valid),
                    films_with_numerator=int((group[numerator] > 0).sum()),
                    film_ids=json.dumps(sorted(valid.film_id)),
                    numerator=n,
                    denominator=d,
                    equal_film_mean=shares.mean(),
                    median=shares.median(),
                    q25=shares.quantile(0.25),
                    q75=shares.quantile(0.75),
                    pooled_share=n / d if d else None,
                )
            )
    return pd.DataFrame(rows)


def entity_ids(row, kind):
    return list(
        dict.fromkeys(
            re.findall(
                re.escape(row["film_id"]) + "/" + kind + r":([\w-]+)", row["entity_ids"]
            )
        )
    )


def checked_edges(db, fid, producer, consumer):
    return db.execute(
        "SELECT DISTINCT asset_id,asset_role,parameter_path FROM attachments "
        "WHERE film_id=? AND producer=? AND generation_id=? ORDER BY ALL",
        [fid, producer, consumer],
    ).fetchall()


def panel_outputs(db, output):
    cases, packages, versions, authorities = [], [], [], []
    readings = json.loads((HERE / "readings.json").read_text())
    locations = []
    for path in sorted((ROOT / "case-files").glob("*/codes.csv")):
        with path.open() as stream:
            rows = [r for r in csv.DictReader(stream) if r["code_id"].startswith("03.")]
        assert len(rows) == 6
        for row in rows:
            row["case_source"] = path.relative_to(ROOT).as_posix()
            cases.append(row)
        by_code = {r["code_id"]: r for r in rows}
        package = by_code["03.3"]
        fid = package["film_id"]
        tasks = (
            entity_ids(package, "generation") if package["status"] == "coded" else []
        )
        contexts = []
        for gid in tasks:
            job = db.execute(
                "SELECT generation_type,model_identifier,prompt,prompt_source_path "
                "FROM j WHERE film_id=? AND generation_id=?",
                [fid, gid],
            ).fetchone()
            assert job
            # Check the opening package span; inherited ledgers are hashed too.
            first = package["excerpt"].split(" [excerpt boundary] ")[0]
            assert first in job[2], (path, gid)
            attachments = db.execute(
                "SELECT DISTINCT asset_id,reference_element_id,"
                "asset_role,parameter_path,producer FROM attachments "
                "WHERE film_id=? AND generation_id=? ORDER BY ALL",
                [fid, gid],
            ).fetchall()
            consumers = db.execute(
                "SELECT DISTINCT a.asset_id,a.generation_id,a.asset_role,"
                "a.parameter_path FROM attachments a WHERE a.film_id=? "
                "AND a.producer=? AND a.generation_id<>? ORDER BY ALL",
                [fid, gid, gid],
            ).fetchall()
            contexts.append(
                dict(
                    film_id=fid,
                    generation_id=gid,
                    generation_type=job[0],
                    model_identifier=job[1],
                    prompt_source_path=job[3],
                    attachments=[
                        dict(
                            zip(
                                [
                                    "asset_id",
                                    "reference_element_id",
                                    "asset_role",
                                    "parameter_path",
                                    "producer",
                                ],
                                a,
                                strict=True,
                            )
                        )
                        for a in attachments
                    ],
                    output_uses=[
                        dict(
                            zip(
                                [
                                    "asset_id",
                                    "consumer",
                                    "asset_role",
                                    "parameter_path",
                                ],
                                a,
                                strict=True,
                            )
                        )
                        for a in consumers
                    ],
                )
            )
        packages.append(
            dict(
                slug=path.parent.name,
                evidence=package,
                package_state="named_attachment"
                if package["value"] == "named_element"
                else "request"
                if tasks
                else "unknown",
                media_content_state="unobservable",
                fulfillment_state="unknown",
                contexts=contexts,
                denominator="One scoped 03.3 assignment / 16 panel films",
            )
        )
        version = by_code["03.5"]
        if version["status"] == "coded":
            gids = entity_ids(version, "generation")
            assert len(gids) == 2
            edges = checked_edges(db, fid, *gids)
            assert edges, (path, gids)
            spans = readings[path.parent.name]
            endpoints = []
            for gid in gids:
                kind, model, field, text = db.execute(
                    "SELECT generation_type,model_identifier,prompt_source_path,prompt "
                    "FROM j WHERE film_id=? AND generation_id=?",
                    [fid, gid],
                ).fetchone()
                endpoints.append(
                    dict(
                        film_id=fid,
                        generation_id=gid,
                        generation_type=kind,
                        model_identifier=model,
                        prompt_source_path=field,
                    )
                )
            for span in [*spans["changed_properties"], spans["identity_basis"]]:
                if span:
                    assert span in text and len(span) < len(text), (path, span)
            versions.append(
                dict(
                    evidence=version,
                    producer=gids[0],
                    consumer=gids[1],
                    relationship="inferred_derivative",
                    approval_state="unknown",
                    endpoints=endpoints,
                    requested_changes=spans["changed_properties"],
                    identity_basis=spans["identity_basis"],
                    identity_limit=(
                        "Source linkage and case interpretation; "
                        "no verified same-entity equivalence."
                    ),
                    edges=[
                        dict(
                            zip(
                                ["asset_id", "asset_role", "parameter_path"],
                                e,
                                strict=True,
                            )
                        )
                        for e in edges
                    ],
                )
            )
        locations.append(
            dict(
                evidence=by_code["03.4"],
                prose="explicit in named span",
                reference_metadata="explicit name/category"
                if "reference_metadata" in by_code["03.4"]["value"]
                else "not assigned by this code",
                attached_media_properties="unobservable",
                parameter_properties=(
                    "not assigned by this code; structural states in film_metrics"
                ),
                denominator="One scoped 03.4 assignment / 16 panel films",
            )
        )
        authorities.append(
            dict(
                evidence=by_code["03.6"],
                declaration_scope="named task/properties only"
                if by_code["03.6"]["status"] == "coded"
                else "unknown",
                project_approval_state="unknown",
            )
        )
    write_csv(pd.DataFrame(cases), output / "case_evidence.csv")
    write_json(output / "reference_packages.json", packages)
    write_json(output / "versions.json", versions)
    write_json(output / "authority.json", authorities)
    write_json(output / "property_locations.json", locations)
    counts = (
        pd.DataFrame(cases)
        .groupby(["code_id", "status", "value"], sort=True)
        .size()
        .reset_index(name="assignments")
    )
    counts["panel_denominator"] = 16
    write_csv(counts, output / "panel_assignments.csv")


def build(data, output):
    output.mkdir(parents=True, exist_ok=True)
    upstream = ROOT / "studies/01-corpus/outputs"
    eligibility = read_csv(upstream / "eligibility.csv")
    eligible = eligibility[
        (eligibility.study.astype(str).str.zfill(2) == "03")
        & (eligibility.population == "primary")
        & eligibility.production_eligible
    ][["film_id", "cohort_group"]].sort_values("film_id")
    assert len(eligible) == 157
    spec = importlib.util.spec_from_file_location(
        "af3a", ROOT / "prompt-labels/build.py"
    )
    features = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(features)

    @cache
    def lexical(text):
        return tuple(
            int(bool(text and features.REGEX[k].search(text)))
            for k in ["reference", "preservation"]
        )

    with connect(data) as db:
        db.register("eligible", eligible)
        db.execute((HERE / "measures.sql").read_text())
        jobs = db.sql("SELECT * FROM job_channels ORDER BY film_id,generation_id").df()
        jobs = jobs.astype(object).where(pd.notna(jobs), None)
        jobs["jobs"] = 1
        for state in ["nonempty", "empty", "unavailable"]:
            jobs["prompt_" + state] = jobs.prompt.map(
                lambda t, s=state: int(field_state(t) == s)
            )
        jobs["input_jobs"] = (jobs.input_assets > 0).astype(int)
        jobs["named_reference_jobs"] = (jobs.attached_references > 0).astype(int)
        jobs["multiple_reference_jobs"] = (jobs.attached_references > 1).astype(int)
        jobs["resolved_input_jobs"] = jobs.resolved_input.astype(int)
        jobs["reference_token_jobs"] = jobs.prompt.map(lambda t: lexical(t)[0])
        jobs["preservation_jobs"] = jobs.prompt.map(lambda t: lexical(t)[1])
        jobs["preservation_with_input"] = jobs.preservation_jobs * jobs.input_jobs
        jobs["token_with_named_reference"] = (
            jobs.reference_token_jobs * jobs.named_reference_jobs
        )
        states = [
            "unavailable",
            "empty_document",
            "invalid_json",
            "other_document",
            "absent",
            "null",
            "empty_array",
            "nonempty_array",
            "other_value",
        ]
        jobs["reference_state"] = jobs.parameters_json.map(reference_state)
        for state in states:
            jobs["parameter_" + state] = (jobs.reference_state == state).astype(int)
        numeric = [
            "jobs",
            "prompt_nonempty",
            "prompt_empty",
            "prompt_unavailable",
            "input_jobs",
            "named_reference_jobs",
            "multiple_reference_jobs",
            "resolved_input_jobs",
            "reference_token_jobs",
            "preservation_jobs",
            "preservation_with_input",
            "token_with_named_reference",
        ] + ["parameter_" + s for s in states]
        film = (
            jobs.groupby("film_id", sort=True)[numeric]
            .sum()
            .reset_index()
            .merge(eligible, on="film_id")
        )
        refs = db.sql("SELECT * FROM refs ORDER BY film_id,reference_element_id").df()
        refs = refs.astype(object).where(pd.notna(refs), None)
        refs["elements"] = 1
        refs["used_elements"] = (refs.consumers > 0).astype(int)
        refs["reused_elements"] = (refs.consumers > 1).astype(int)
        refs["multi_asset_elements"] = (refs.attached_asset_ids > 1).astype(int)
        ref_numeric = [
            "elements",
            "used_elements",
            "reused_elements",
            "multi_asset_elements",
        ]
        for field in ["name", "category", "description"]:
            for state in ["nonempty", "empty", "unavailable"]:
                col = field + "_" + state
                refs[col] = refs[field].map(lambda v, s=state: int(field_state(v) == s))
                ref_numeric.append(col)
        counts = refs.groupby("film_id", sort=True)[ref_numeric].sum().reset_index()
        film = film.merge(counts, on="film_id", how="left")
        film[ref_numeric] = film[ref_numeric].fillna(0).astype(int)
        reuse = db.sql(
            "SELECT film_id,count(*) AS input_asset_ids,count(*) FILTER(WHERE "
            "consumers>1) AS reused_input_assets FROM input_reuse GROUP BY film_id"
        ).df()
        film = film.merge(reuse, on="film_id", how="left")
        film[["input_asset_ids", "reused_input_assets"]] = (
            film[["input_asset_ids", "reused_input_assets"]].fillna(0).astype(int)
        )
        taxonomy = read_csv(upstream / "taxonomy.csv")
        film = film.merge(
            taxonomy[["film_id", "title", "record_orientation", "scale"]], on="film_id"
        )
        film["unusual_project"] = film.film_id.isin(
            read_csv(upstream / "unusual_projects.csv").film_id
        )
        baseline = read_csv(upstream / "film_metrics.csv")
        check = film.merge(
            baseline[["film_id", "generations", "reference_elements"]], on="film_id"
        )
        assert (check.jobs == check.generations).all() and (
            check.elements == check.reference_elements
        ).all()
        write_csv(film, output / "film_metrics.csv")
        write_csv(
            aggregate(film, ["cohort_group", "record_orientation", "scale"]),
            output / "summaries.csv",
        )
        categories = (
            refs.groupby(["film_id", "category"], dropna=False, sort=True)[ref_numeric]
            .sum()
            .reset_index()
            .merge(eligible, on="film_id")
        )
        write_csv(categories, output / "reference_categories.csv")
        for dim in ["generation_type", "model_identifier"]:
            part = (
                jobs.groupby(["film_id", dim], dropna=False, sort=True)[numeric]
                .sum()
                .reset_index()
                .merge(eligible, on="film_id")
            )
            write_csv(part, output / ("by_" + dim + ".csv"))
            summaries = []
            for cohort, group in [
                ("all", part),
                *part.groupby("cohort_group", sort=True),
            ]:
                summary = aggregate(group, [dim])
                summary = summary[summary.dimension == dim].drop(columns="film_ids")
                summary["cohort_group"] = cohort
                summaries.append(summary)
            write_csv(pd.concat(summaries), output / ("summary_" + dim + ".csv"))
        # Verify structural rules against AF3a on every film-distinct all-role text.
        fields = db.sql(
            "SELECT film_id,generation_id,prompt_source_path AS field_path,"
            "prompt AS text FROM j UNION ALL SELECT p.film_id,p.generation_id,"
            "p.field_path,p.text FROM generation_prompts p "
            "JOIN j ON p.film_id=j.film_id AND p.generation_id=j.generation_id "
            "WHERE p.field_path IS DISTINCT FROM j.prompt_source_path"
        ).df()
        # The omitted primary copies must be exactly equal, including null states.
        assert (
            db.sql(
                "SELECT count(*) FROM generation_prompts p JOIN j "
                "ON p.film_id=j.film_id AND p.generation_id=j.generation_id "
                "AND p.field_path=j.prompt_source_path "
                "WHERE p.text IS DISTINCT FROM j.prompt"
            ).fetchone()[0]
            == 0
        )
        fields = fields[fields.text.notna() & (fields.text != "")].drop_duplicates(
            ["film_id", "text"]
        )
        structural = []
        for fid, g in fields.groupby("film_id", sort=True):
            structural.append(
                dict(
                    film_id=fid,
                    distinct_texts_denominator=len(g),
                    reference_matches_sum=sum(
                        len(list(features.REGEX["reference"].finditer(t)))
                        for t in g.text
                    ),
                    preservation_matches_sum=sum(
                        len(list(features.REGEX["preservation"].finditer(t)))
                        for t in g.text
                    ),
                )
            )
        structural = pd.DataFrame(structural)
        expected = read_csv(ROOT / "prompt-labels/outputs/features_by_film.csv")
        joined = structural.merge(expected, on="film_id", suffixes=("", "_af3a"))
        assert len(joined) == 157
        for col in [
            "distinct_texts_denominator",
            "reference_matches_sum",
            "preservation_matches_sum",
        ]:
            assert (joined[col] == joined[col + "_af3a"]).all(), col
        write_csv(structural, output / "structural_check.csv")
        audits = []
        panel = read_csv(upstream / "panel.csv")
        assert set(panel.film_id) == {
            json.loads((p.parent / "profile.json").read_text())["film_id"]
            for p in (ROOT / "case-files").glob("*/codes.csv")
        }
        for fid in sorted(panel.film_id):
            for feature, column in [
                ("reference", "reference_token_jobs"),
                ("preservation", "preservation_jobs"),
            ]:
                for positive in [True, False]:
                    candidates = jobs[
                        (jobs.film_id == fid)
                        & (jobs.prompt_nonempty == 1)
                        & (jobs[column] == int(positive))
                    ]
                    if candidates.empty:
                        continue
                    row = candidates.iloc[0]
                    match = features.REGEX[feature].search(row.prompt)
                    span = match[0] if match else None
                    audits.append(
                        dict(
                            generation_id=row.generation_id,
                            feature=feature,
                            lexical_positive=positive,
                            match_start=match.start() if match else None,
                            match_end=match.end() if match else None,
                            match_sha256=hashlib.sha256(span.encode()).hexdigest()
                            if span
                            else None,
                            **provenance(
                                fid,
                                f"{fid}/generation:{row.generation_id}",
                                "generations.prompt; " + str(row.prompt_source_path),
                                span if span != row.prompt else None,
                                f"First sorted match={positive} / "
                                f"{len(candidates)} matching film fields",
                            ),
                        )
                    )
        write_csv(pd.DataFrame(audits), output / "lexical_audit.csv")
        panel_outputs(db, output)
    ledgers = []
    for r in film.to_dict("records"):
        fid = r["film_id"]
        ledgers.append(
            provenance(
                fid,
                f"{fid}/generation,asset,reference,field: all scoped compound keys",
                "measures.sql; build.py; generations.prompt/parameters_json; "
                "asset_usages; assets.generation_id; "
                "reference_elements.name/category/description; Study 01 taxonomy",
                json.dumps(r, sort_keys=True),
                f"{r['jobs']} jobs; {r['prompt_nonempty']} nonempty primary fields; "
                f"{r['elements']} disclosed elements; "
                f"{r['input_asset_ids']} raw input IDs; "
                "zero denominator ratios unavailable; taxonomy inferred",
            )
        )
    write_csv(pd.DataFrame(ledgers), output / "metric_evidence.csv")
    inputs = [
        HERE / n
        for n in [
            "build.py",
            "measures.sql",
            "schemas.json",
            "ontology.json",
            "readings.json",
        ]
    ]
    inputs += [
        ROOT / n
        for n in [
            "PROGRAMME.md",
            "prompt-labels/build.py",
            "prompt-labels/outputs/features_by_film.csv",
        ]
    ]
    inputs += [
        upstream / (n + ".csv")
        for n in [
            "eligibility",
            "taxonomy",
            "film_metrics",
            "unusual_projects",
            "panel",
            "codebook",
        ]
    ]
    inputs += [
        p
        for pattern in ["*/codes.csv", "*/CASE.md", "*/traced-edges.json"]
        for p in sorted((ROOT / "case-files").glob(pattern))
    ]
    manifest = dict(
        release="data-2026-10-20",
        source_manifest_sha256=digest(Path(data) / "SHA256SUMS"),
        inputs={p.relative_to(ROOT).as_posix(): digest(p) for p in inputs},
        outputs={
            p.name: digest(p)
            for p in sorted(output.iterdir())
            if p.suffix in {".json", ".csv"} and p.name != "reproduction.json"
        },
    )
    write_json(output / "reproduction.json", manifest)
    assert all(p.stat().st_size < 1_000_000 for p in output.iterdir())
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, default=HERE / "outputs")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check and args.output.resolve() == (HERE / "outputs").resolve():
        parser.error("--check requires a separate output directory")
    manifest = build(args.data, args.output)
    if args.check:
        for name in [*manifest["outputs"], "reproduction.json"]:
            assert (args.output / name).read_bytes() == (
                HERE / "outputs" / name
            ).read_bytes(), name
    print(
        f"Study 03: 157 films, 96 panel assignments, {len(manifest['outputs'])} outputs"
    )


if __name__ == "__main__":
    main()
