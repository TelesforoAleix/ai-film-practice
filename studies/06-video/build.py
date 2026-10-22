"""Study 06: disclosed video routes, shot instructions and literal controls."""

import argparse
import csv
import hashlib
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

import pandas as pd

from film_practice import connect

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NULL = r"\N"
FEATURES = ["camera", "lens", "preservation", "exclusion", "multi_shot", "reference"]
ROUTES = [
    "extension",
    "video_guided",
    "start_end",
    "image_guided",
    "text_to_video",
    "text_candidate",
    "unknown",
]
CONTROLS = [
    "duration",
    "aspect_ratio",
    "resolution",
    "width",
    "height",
    "fps",
    "model",
    "mode",
    "model_version",
    "multi_shots",
    "multi_shot_mode",
    "generate_audio",
    "sound",
    "draft",
    "extension_mode",
    "start_seconds",
    "end_seconds",
    "motion",
    "camera_model",
    "camera_lens",
    "camera_aperture",
    "camera_focal_length",
]
ALTERNATIVE = (
    "Published histories omit external/private work; raw asset IDs may alias. "
    "Wording can be quoted, negated or miss other languages. Attachments and "
    "controls do not verify media, execution, acceptance or benefit."
)
CONFIDENCE = (
    "Deterministic film-scoped record counts under documented rules; semantic "
    "completeness, independent agreement and causal effects unmeasured."
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path):
    return pd.read_csv(path, keep_default_na=False, na_values=[NULL])


def write_json(path, value):
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )


def write_csv(frame, path):
    frame.to_csv(
        path, index=False, na_rep=NULL, float_format="%.9f", lineterminator="\n"
    )


def parse(raw):
    if raw is None:
        return "unavailable", None
    if raw == "":
        return "empty", None
    try:
        obj = json.loads(raw)
    except (ValueError, TypeError):
        return "invalid", None
    return ("object", obj) if isinstance(obj, dict) else ("nonobject", None)


def state(obj, key):
    if obj is None:
        return "unavailable", None
    if key not in obj:
        return "absent", None
    value = obj[key]
    if value is None:
        return "null", None
    if value == "" and isinstance(value, str):
        return "empty_string", '""'
    if isinstance(value, (dict, list)):
        return ("nonempty_" if value else "empty_") + type(value).__name__, None
    return type(value).__name__, json.dumps(value, ensure_ascii=False, sort_keys=True)


def evidence(fid, entities, source, excerpt, denominator, label="observed"):
    return dict(
        study="06",
        film_id=fid,
        entity_ids=entities,
        source_path=source,
        excerpt=excerpt,
        evidence_label=label,
        competing_explanation=ALTERNATIVE,
        denominator=denominator,
        confidence_rationale=CONFIDENCE,
    )


def aggregate(frame, metrics, dimensions):
    rows = []
    groups = [("all", "primary", frame)]
    for dim in dimensions:
        groups += [
            (dim, str(v), g) for v, g in frame.groupby(dim, dropna=False, sort=True)
        ]
    for dim, value, group in groups:
        for n, d in metrics:
            valid = group[group[d] > 0]
            shares = valid[n] / valid[d]
            numerator, denominator = int(valid[n].sum()), int(valid[d].sum())
            rows.append(
                dict(
                    dimension=dim,
                    value=value,
                    metric=n,
                    denominator_name=d,
                    eligible_films=len(group),
                    measured_films=len(valid),
                    films_with_numerator=int((group[n] > 0).sum()),
                    numerator=numerator,
                    denominator=denominator,
                    equal_film_mean=shares.mean(),
                    median=shares.median(),
                    q25=shares.quantile(0.25),
                    q75=shares.quantile(0.75),
                    pooled_share=numerator / denominator if denominator else None,
                )
            )
    return pd.DataFrame(rows)


def control_state(obj, key, document_state):
    """A malformed document is distinct from an unavailable document/key."""
    if document_state != "object":
        return document_state + "_document", None
    return state(obj, key)


def classify(obj, images, videos, audio, start, end, unknown, text):
    """Input route is exclusive; multi-shot intent/control are independent axes."""
    if videos:
        if obj is not None and obj.get("model") == "video_extension":
            return "extension"
        return "video_guided"
    if start and end:
        return "start_end"
    if images:
        return "image_guided"
    if obj is None or audio or unknown or not text:
        return "unknown"
    # A mode declaration supports an export-level route, not proven absence of
    # undisclosed inputs. Merely missing usage rows never supports text-only.
    media = [
        "medias",
        "reference_elements",
        "input_image",
        "input_images",
        "input_video",
        "input_audio",
        "end_input_image",
        "reference_input_images",
        "style_input_image",
        "draw_input_image",
    ]
    if any(obj.get(k) not in (None, "", [], {}) for k in media):
        return "unknown"
    if obj.get("mode") == "text-to-video":
        return "text_to_video"
    if obj.get("medias") == []:
        return "text_candidate"
    return "unknown"


def generation_ids(row):
    return list(
        dict.fromkeys(
            re.findall(
                re.escape(row["film_id"]) + r"/generation:([\w-]+)", row["entity_ids"]
            )
        )
    )


def panel_outputs(db, output, jobs):
    cases, contexts, edges = [], [], []
    for path in sorted((ROOT / "case-files").glob("*/codes.csv")):
        rows = [
            r for r in csv.DictReader(path.open()) if r["code_id"].startswith("06.")
        ]
        assert len(rows) == 7
        for row in rows:
            row["case_source"] = path.relative_to(ROOT).as_posix()
            cases.append(row)
        fid = rows[0]["film_id"]
        for gid in sorted({g for r in rows for g in generation_ids(r)}):
            job = jobs[(jobs.film_id == fid) & (jobs.generation_id == gid)]
            assert len(job) == 1
            r = job.iloc[0]
            ps, obj = parse(r.parameters_json)
            bindings = (
                db.execute(
                    "SELECT asset_id,asset_role,parameter_path,reference_element_id,"
                    "producer,producer_type,image_binding,video_binding,audio_binding "
                    "FROM attachments WHERE film_id=? AND generation_id=? ORDER BY ALL",
                    [fid, gid],
                )
                .df()
                .astype(object)
            )
            bindings = bindings.where(pd.notna(bindings), None).to_dict("records")
            assigned = [x["evidence_id"] for x in rows if gid in generation_ids(x)]
            contexts.append(
                dict(
                    film_id=fid,
                    generation_id=gid,
                    model_identifier=r.model_identifier,
                    model_version=r.model_version,
                    parameter_state=ps,
                    route=r.route,
                    route_label="inferred",
                    literal_controls={
                        k: dict(
                            zip(
                                ["state", "raw_json"],
                                control_state(obj, k, ps),
                                strict=True,
                            )
                        )
                        for k in CONTROLS
                    },
                    attachments=bindings,
                    evidence_ids=assigned,
                    source_path=r.prompt_source_path,
                    denominator=(
                        "One named video job; attachments are "
                        "deduplicated occurrence channels"
                    ),
                    evidence_label="observed",
                    media_outcome="unobservable",
                )
            )
            for b in bindings:
                if b["producer"]:
                    edges.append(
                        dict(
                            **evidence(
                                fid,
                                f"{fid}/generation:{b['producer']}; "
                                f"{fid}/asset:{b['asset_id']}; {fid}/generation:{gid}",
                                "assets.generation_id; "
                                "asset_usages.asset_role/parameter_path",
                                json.dumps(b, sort_keys=True),
                                "One explicit input-edge occurrence",
                            ),
                            consumer=gid,
                            **b,
                        )
                    )
        for row in rows:
            if row["status"] != "coded":
                continue
            opening = row["excerpt"].split(" [excerpt boundary] ")[0]
            if opening.startswith("["):
                continue
            texts = [
                db.execute(
                    "SELECT prompt FROM j WHERE film_id=? AND generation_id=?", [fid, g]
                ).fetchone()[0]
                or ""
                for g in generation_ids(row)
            ]
            assert any(opening in t for t in texts), row["evidence_id"]
    write_csv(pd.DataFrame(cases), output / "case_evidence.csv")
    write_json(output / "panel_contexts.json", contexts)
    write_csv(pd.DataFrame(edges).drop_duplicates(), output / "panel_edges.csv")
    counts = (
        pd.DataFrame(cases)
        .groupby(["code_id", "status", "value"], sort=True)
        .size()
        .reset_index(name="assignments")
    )
    counts["panel_denominator"] = 16
    write_csv(counts, output / "panel_assignments.csv")
    # Source-check additional component spans and the linked split request.
    readings = []
    for item in json.loads((HERE / "readings.json").read_text()):
        text, source = db.execute(
            "SELECT prompt,prompt_source_path FROM j "
            "WHERE film_id=? AND generation_id=?",
            [item["film_id"], item["generation_id"]],
        ).fetchone()
        assert item["span"] in text and item["span"] != text
        readings.append(
            dict(
                **evidence(
                    item["film_id"],
                    item["film_id"] + "/generation:" + item["generation_id"],
                    "generations.prompt; " + source,
                    item["span"],
                    "One purposive component span; not corpus semantic prevalence",
                    "inferred",
                ),
                **{k: v for k, v in item.items() if k != "film_id"},
            )
        )
    write_csv(pd.DataFrame(readings), output / "motion_patterns.csv")
    revisions = []
    for row in cases:
        if row["code_id"] != "06.7" or row["status"] != "coded":
            continue
        scoped = [c for c in contexts if row["evidence_id"] in c["evidence_ids"]]
        revisions.append(
            dict(
                evidence=row,
                jobs=scoped,
                interpretation_label="inferred",
                revision=(
                    "Named changed-shot request; "
                    "no defect, success or acceptance inferred"
                ),
                lineage=(
                    "Only resolved producer inputs in contexts are explicit edges; "
                    "unresolved sources remain unknown"
                ),
                comparison_limit=(
                    "Not an exhaustive revision-family inventory or retry denominator"
                ),
            )
        )
    write_json(output / "revision_requests.json", revisions)


def build(data, output):
    output.mkdir(parents=True, exist_ok=True)
    upstream = ROOT / "studies/01-corpus/outputs"
    eligibility = read_csv(upstream / "eligibility.csv")
    scope = eligibility[
        (eligibility.study.astype(str).str.zfill(2) == "06")
        & (eligibility.population == "primary")
    ].sort_values("film_id")
    assert len(scope) == 157 and int(scope.production_eligible.sum()) == 156
    eligible = scope[["film_id", "cohort_group"]]
    write_csv(scope, output / "eligibility.csv")
    spec = importlib.util.spec_from_file_location(
        "af3a", ROOT / "prompt-labels/build.py"
    )
    features = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(features)
    with connect(data) as db:
        db.register("eligible", eligible)
        db.execute((HERE / "measures.sql").read_text())
        jobs = db.sql("SELECT * FROM video_jobs ORDER BY film_id,generation_id").df()
        jobs = jobs.astype(object).where(pd.notna(jobs), None)
        derived = []
        controls = Counter()
        versions = []
        routes = []
        for row in jobs.to_dict("records"):
            ps, obj = parse(row["parameters_json"])
            route = classify(
                obj,
                row["image_inputs"],
                row["video_inputs"],
                row["audio_inputs"],
                row["has_start"],
                row["has_end"],
                row["unknown_inputs"],
                row["prompt"],
            )
            routes.append(route)
            version = json.dumps(
                control_state(obj, "model_version", ps), ensure_ascii=False
            )
            versions.append(version)
            v = dict(
                jobs=1,
                prompt_nonempty=int(row["prompt"] not in (None, "")),
                prompt_empty=int(row["prompt"] == ""),
                prompt_unavailable=int(row["prompt"] is None),
                image_bound=int(row["image_inputs"] > 0),
                video_bound=int(row["video_inputs"] > 0),
                audio_bound=int(row["audio_inputs"] > 0),
                start_bound=int(row["has_start"]),
                end_bound=int(row["has_end"]),
                image_parent=int(row["image_parents"] > 0),
                video_parent=int(row["video_parents"] > 0),
                unknown_input=int(row["unknown_inputs"] > 0),
            )
            v.update({"route_" + k: int(route == k) for k in ROUTES})
            v.update(
                {
                    "json_" + k: int(ps == k)
                    for k in ["object", "invalid", "unavailable", "empty", "nonobject"]
                }
            )
            v.update(
                {
                    k + "_words": int(
                        bool(row["prompt"] and features.REGEX[k].search(row["prompt"]))
                    )
                    for k in FEATURES
                }
            )
            v["multi_true"] = int(obj is not None and obj.get("multi_shots") is True)
            v["multi_false"] = int(obj is not None and obj.get("multi_shots") is False)
            v["audio_true"] = int(obj is not None and obj.get("generate_audio") is True)
            v["edit_mode"] = int(obj is not None and obj.get("model") == "video_edit")
            v["multi_words_false"] = v["multi_shot_words"] * v["multi_false"]
            v["multi_prompt_nonempty"] = int(
                obj is not None
                and isinstance(obj.get("multi_prompt"), list)
                and bool(obj["multi_prompt"])
            )
            derived.append(v)
            for key in CONTROLS:
                kind, raw = control_state(obj, key, ps)
                controls[
                    (row["film_id"], row["model_identifier"], version, key, kind, raw)
                ] += 1
        numeric = list(derived[0])
        jobs = pd.concat([jobs.reset_index(drop=True), pd.DataFrame(derived)], axis=1)
        jobs["route"] = routes
        jobs["model_version"] = versions
        film = (
            jobs.groupby("film_id", sort=True)[numeric]
            .sum()
            .reset_index()
            .merge(eligible, on="film_id")
        )
        assert len(film) == 156 and film.jobs.sum() == 38508
        baseline = read_csv(upstream / "film_metrics.csv")
        assert (
            film.merge(baseline[["film_id", "video_jobs"]], on="film_id")
            .eval("jobs==video_jobs")
            .all()
        )
        taxonomy = read_csv(upstream / "taxonomy.csv")
        film = film.merge(
            taxonomy[["film_id", "title", "record_orientation", "scale"]], on="film_id"
        )
        film["unusual_project"] = film.film_id.isin(
            read_csv(upstream / "unusual_projects.csv").film_id
        )
        ratios = [
            (
                n,
                "multi_shot_words"
                if n == "multi_words_false"
                else "prompt_nonempty"
                if n.endswith("_words")
                else "jobs",
            )
            for n in numeric
            if n != "jobs"
        ]
        write_csv(film, output / "film_metrics.csv")
        write_csv(
            aggregate(film, ratios, ["cohort_group", "record_orientation", "scale"]),
            output / "summaries.csv",
        )
        members = {
            dim: {str(v): sorted(g.film_id) for v, g in film.groupby(dim, sort=True)}
            for dim in ["cohort_group", "record_orientation", "scale"]
        }
        members["all"] = {"primary": sorted(film.film_id)}
        write_json(output / "summary_members.json", members)
        for dim in ["model_identifier", "route"]:
            part = (
                jobs.groupby(["film_id", dim], dropna=False, sort=True)[numeric]
                .sum()
                .reset_index()
                .merge(eligible, on="film_id")
            )
            write_csv(part, output / ("by_" + dim + ".csv"))
            summaries = []
            for cohort, g in [("all", part), *part.groupby("cohort_group", sort=True)]:
                s = aggregate(g, ratios, [dim])
                s = s[s.dimension == dim]
                s["cohort_group"] = cohort
                summaries.append(s)
            write_csv(pd.concat(summaries), output / ("summary_" + dim + ".csv"))
        part = (
            jobs.groupby(["film_id", "model_identifier", "model_version"], sort=True)[
                numeric
            ]
            .sum()
            .reset_index()
            .merge(eligible, on="film_id")
        )
        write_csv(part, output / "by_model_version.csv")
        cf = pd.DataFrame(
            [
                dict(
                    zip(
                        [
                            "film_id",
                            "model_identifier",
                            "model_version",
                            "parameter",
                            "state",
                            "raw_json",
                        ],
                        key,
                        strict=True,
                    ),
                    jobs=n,
                )
                for key, n in controls.items()
            ]
        )
        cf = cf.sort_values(
            [
                "film_id",
                "model_identifier",
                "model_version",
                "parameter",
                "state",
                "raw_json",
            ],
            na_position="first",
        )
        totals = (
            jobs.groupby(["film_id", "model_identifier", "model_version"], sort=True)
            .size()
            .rename("video_job_denominator")
            .reset_index()
        )
        cf = cf.merge(totals, on=["film_id", "model_identifier", "model_version"])
        for key in CONTROLS:
            write_csv(cf[cf.parameter == key], output / ("controls_" + key + ".csv"))
        # Compare exact value/state frequencies within literal model/version.
        # Include zero-share films for each bucket within that model/version.
        for key in CONTROLS:
            rows = []
            for (model, version), group in cf[cf.parameter == key].groupby(
                ["model_identifier", "model_version"], sort=True
            ):
                denoms = group.groupby("film_id").video_job_denominator.first()
                for (kind, raw), bucket in group.groupby(
                    ["state", "raw_json"], dropna=False, sort=True
                ):
                    counts = bucket.groupby("film_id").jobs.sum()
                    shares = counts.reindex(denoms.index, fill_value=0) / denoms
                    rows.append(
                        dict(
                            model_identifier=model,
                            model_version=version,
                            parameter=key,
                            state=kind,
                            raw_json=raw,
                            films_with_value=len(counts),
                            film_denominator=len(denoms),
                            jobs=int(counts.sum()),
                            video_job_denominator=int(denoms.sum()),
                            equal_film_mean=shares.mean(),
                            median=shares.median(),
                            q25=shares.quantile(0.25),
                            q75=shares.quantile(0.75),
                            pooled_share=counts.sum() / denoms.sum(),
                        )
                    )
            write_csv(pd.DataFrame(rows), output / ("summary_controls_" + key + ".csv"))
        ledger = [
            evidence(
                r["film_id"],
                r["film_id"] + "/generation:* WHERE generation_type=video; "
                "compound input asset IDs selected by measures.sql",
                "generations; assets; asset_usages; "
                "studies/06-video/measures.sql; build.py",
                json.dumps({k: int(r[k]) for k in numeric}, sort_keys=True),
                f"{r['jobs']} video jobs; "
                f"{r['prompt_nonempty']} nonempty primary fields; "
                "per-metric denominator_name in summaries",
            )
            for r in film.to_dict("records")
        ]
        write_csv(pd.DataFrame(ledger), output / "metric_evidence.csv")
        examples = []
        panel_ids = set(read_csv(upstream / "panel.csv").film_id)
        for route, group in jobs.groupby("route", sort=True):
            panel_group = group[group.film_id.isin(panel_ids)]
            chosen = panel_group if len(panel_group) else group
            r = chosen.iloc[0]
            bindings = db.execute(
                "SELECT asset_id,asset_role,parameter_path,reference_element_id "
                "FROM attachments WHERE film_id=? AND generation_id=? ORDER BY ALL",
                [r.film_id, r.generation_id],
            ).fetchall()
            examples.append(
                dict(
                    **evidence(
                        r.film_id,
                        r.film_id + "/generation:" + r.generation_id,
                        "generations.parameters_json; asset_usages; "
                        + r.prompt_source_path,
                        json.dumps(
                            dict(bindings=bindings, route=route), sort_keys=True
                        ),
                        f"One first sorted {'panel' if len(panel_group) else 'corpus'} "
                        f"example among {len(group)} jobs in this recorded route",
                        "inferred",
                    ),
                    route=route,
                    generation_id=r.generation_id,
                    model_identifier=r.model_identifier,
                    in_panel=r.film_id in panel_ids,
                )
            )
        write_csv(pd.DataFrame(examples), output / "route_examples.csv")
        panel_outputs(db, output, jobs)
        structural_outputs(jobs, features, upstream, output)
        # Refine Study 05's foundation proxy without promoting references to frames.
        foundations = db.sql("""SELECT a.film_id,a.asset_role,a.parameter_path,
          count(DISTINCT a.producer) AS image_producers,
          count(DISTINCT a.generation_id) AS video_consumers,
          count(DISTINCT (a.producer,a.generation_id)) AS producer_consumer_pairs
          FROM attachments a JOIN video_jobs v USING(film_id,generation_id)
          WHERE a.image_binding AND a.producer_type='image'
 GROUP BY ALL ORDER BY ALL""").df()
        foundation_totals = db.sql("""SELECT a.film_id,
 count(DISTINCT a.producer) AS image_producers
          FROM attachments a JOIN video_jobs v USING(film_id,generation_id)
          WHERE a.image_binding AND a.producer_type='image' GROUP BY ALL""").df()
        assert int(foundation_totals.image_producers.sum()) == 8076
        foundations = foundations.merge(
            foundation_totals.rename(
                columns={"image_producers": "film_foundation_denominator"}
            ),
            on="film_id",
        )
        write_csv(foundations, output / "foundation_roles.csv")
    sources = [
        HERE / n
        for n in [
            "build.py",
            "measures.sql",
            "taxonomy.json",
            "video_node.json",
            "readings.json",
        ]
    ]
    sources += [
        ROOT / n
        for n in [
            "PROGRAMME.md",
            "AGENTS.md",
            "DATA.md",
            "prompt-labels/build.py",
            "prompt-labels/README.md",
            "prompt-labels/outputs/features_by_stratum.csv",
            "case-files/README.md",
        ]
    ]
    sources += [
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
    sources += [
        ROOT / "studies/01-corpus" / n
        for n in ["README.md", "CODEBOOK.md", "DICTIONARY.md", "PROVENANCE.md"]
    ]
    sources += [
        ROOT / "studies" / n / "README.md"
        for n in ["02-planning", "03-elements", "05-image", "10-organisation"]
    ]
    sources += sorted((ROOT / "case-files").glob("*/codes.csv")) + sorted(
        (ROOT / "case-files").glob("*/CASE.md")
    )
    write_json(
        output / "reproduction.json",
        dict(
            study="06",
            release="data-2026-10-20",
            source_manifest_sha256=digest(data / "SHA256SUMS"),
            inputs={p.relative_to(ROOT).as_posix(): digest(p) for p in sources},
            outputs={
                p.name: digest(p)
                for p in sorted(output.iterdir())
                if p.name != "reproduction.json"
            },
            primary_films=157,
            eligible_films=156,
            video_jobs=38508,
        ),
    )
    for p in output.iterdir():
        assert p.stat().st_size < 1_000_000, (p.name, p.stat().st_size)
    print(
        f"Built {len(list(output.iterdir()))} outputs; "
        "156 eligible films; 38508 video jobs"
    )


def structural_outputs(jobs, features, upstream, output):
    baseline = read_csv(ROOT / "prompt-labels/outputs/features_by_stratum.csv")
    baseline = baseline[
        (baseline.population == "primary")
        & (baseline.generation_type == "video")
        & (baseline.text_role == "primary")
    ].set_index("film_id")
    checks = []
    for fid, g in jobs[jobs.prompt_nonempty == 1].groupby("film_id", sort=True):
        texts = g.prompt.drop_duplicates()
        values = dict(distinct_texts_denominator=len(texts))
        for name in FEATURES:
            values[name + "_matches_sum"] = sum(
                len(features.REGEX[name].findall(t)) for t in texts
            )
        for k, v in values.items():
            assert v == baseline.loc[fid, k], (fid, k)
        checks.append(dict(film_id=fid, **values, af3a_equal=True))
    assert len(checks) == 156
    write_csv(pd.DataFrame(checks), output / "structural_check.csv")
    audit = []
    for fid in sorted(read_csv(upstream / "panel.csv").film_id):
        group = jobs[(jobs.film_id == fid) & (jobs.prompt_nonempty == 1)]
        for name in FEATURES:
            for positive in [False, True]:
                selected = group[group[name + "_words"] == int(positive)]
                if selected.empty:
                    continue
                r = selected.iloc[0]
                found = features.REGEX[name].search(r.prompt)
                span = found.group() if found and found.group() != r.prompt else None
                audit.append(
                    dict(
                        **evidence(
                            fid,
                            fid + "/generation:" + r.generation_id,
                            "generations.prompt; " + r.prompt_source_path,
                            span,
                            f"First sorted key among {len(selected)} "
                            "matching-state nonempty panel fields",
                        ),
                        feature=name,
                        positive=positive,
                        text_sha256=hashlib.sha256(r.prompt.encode()).hexdigest(),
                        match_start=found.start() if found else None,
                        match_end=found.end() if found else None,
                    )
                )
    write_csv(pd.DataFrame(audit), output / "structural_audit.csv")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, default=HERE / "outputs")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check and args.output.resolve() == (HERE / "outputs").resolve():
        parser.error("--check requires a separate output directory")
    build(args.data, args.output)
    if args.check:
        assert {p.name: p.read_bytes() for p in args.output.iterdir()} == {
            p.name: p.read_bytes() for p in (HERE / "outputs").iterdir()
        }, "Reproduction differs from committed outputs"
        print("Every output reproduced byte for byte")


if __name__ == "__main__":
    main()
