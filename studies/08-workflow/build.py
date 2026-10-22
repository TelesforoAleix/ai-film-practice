"""Study 08: recorded operations, literal models and explicit workflow motifs."""

import argparse
import csv
import hashlib
import importlib.util
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

from film_practice import connect

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NULL = r"\N"
ALT = (
    "Published histories can omit external/private work; repeated requests and raw "
    "asset aliases change apparent workflow. A binding is not approval, a semantic "
    "role, a human responsibility transfer or evidence of benefit."
)
CONF = (
    "Deterministic compound-key released-record counts; source correspondence checked. "
    "Single-coder case semantics; no independent agreement or media assessment."
)
ADAPTERS = json.loads((HERE / "catalogue.json").read_text())["adapter_roles"]
FINISH = {
    k for k, v in ADAPTERS.items() if v in {"editing", "upscale", "finishing_declared"}
}
METRICS = [
    "media_bound",
    "no_recorded_media",
    "shared_input",
    "chained",
    "cross_model",
    "convergent",
    "staged_refinement",
    "reference_preparation",
    "image_foundation",
    "audio_job",
    "finishing_job",
    "video_candidate",
    "image_job",
    "voice_adapter",
]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


lineage = module("lineage08", "studies/07-lineage/build.py")
image = module("image08", "studies/05-image/build.py")
video = module("video08", "studies/06-video/build.py")
features = module("features08", "prompt-labels/build.py")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return pd.read_csv(path, keep_default_na=False, na_values=[NULL])


def write(frame, path):
    frame.to_csv(
        path, index=False, na_rep=NULL, float_format="%.9f", lineterminator="\n"
    )


def js(path, value):
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )


def evidence(fid, ids, source, excerpt, denominator, label="observed"):
    return dict(
        study="08",
        film_id=fid,
        entity_ids=ids,
        source_path=source,
        excerpt=excerpt,
        evidence_label=label,
        competing_explanation=ALT,
        denominator=denominator,
        confidence_rationale=CONF,
    )


def summarize(frame, metrics, dimensions=()):
    rows = []
    groups = [("all", "primary", frame)]
    for dim in dimensions:
        groups.extend((dim, value, g) for value, g in frame.groupby(dim, dropna=False))
    for dim, value, group in groups:
        for n, d in metrics:
            valid = group[group[d] > 0]
            shares = valid[n] / valid[d]
            num, den = int(valid[n].sum()), int(valid[d].sum())
            rows.append(
                dict(
                    dimension=dim,
                    value=value,
                    metric=n,
                    denominator_name=d,
                    eligible_films=len(group),
                    measured_films=len(valid),
                    positive_films=int((valid[n] > 0).sum()),
                    numerator=num,
                    denominator=den,
                    equal_film_mean=shares.mean(),
                    median=shares.median(),
                    q25=shares.quantile(0.25),
                    q75=shares.quantile(0.75),
                    pooled_share=num / den if den else None,
                    film_ids=";".join(sorted(group.film_id)),
                )
            )
    return pd.DataFrame(rows)


def motifs(jobs, assets, usages, refs):
    """One film only; explicit graph, no chronology or semantic identity edges."""
    graph = lineage.graph(jobs, assets, usages, refs)
    byid = {j["generation_id"]: j for j in jobs}
    media_jobs, branches = set(), set()
    for consumers in graph["media"].values():
        media_jobs |= consumers
        if len(consumers) >= 2:
            branches |= consumers
    foundation, prep = set(), set()
    pairs, triples = set(), set()
    for a, consumers in graph["media"].items():
        p = graph["resolved"].get(a)
        if p not in byid:
            continue
        for c in consumers - {p}:
            pairs.add((p, c))
            triples.add((p, a, c))
    for u in usages:
        p = graph["resolved"].get(u["asset_id"])
        c = u["generation_id"]
        is_image = u["asset_role"] in {
            "input_image",
            "reference_image",
            "input_start_image",
            "input_end_image",
        } or (
            u["asset_role"] == "input_asset"
            and (
                (u["parameter_path"] or "").startswith("params.input_images[")
                or u["parameter_path"]
                in {
                    "params.input_image",
                    "params.image_reference",
                    "params.custom_reference",
                    "params.paint_image",
                    "params.end_input_image",
                }
            )
        )
        if (
            p in byid
            and p != c
            and is_image
            and (
                byid[p]["generation_type"] == "image"
                and byid[c]["generation_type"] == "video"
            )
        ):
            foundation.add(p)
        if (
            u["reference_element_id"] not in (None, "")
            and lineage.binding_kind(u["asset_role"], u["parameter_path"]) == "media"
        ):
            p = graph["resolved"].get(u["asset_id"])
            if p in byid and p != u["generation_id"]:
                prep.add(p)
    flags = {}
    for key, job in byid.items():
        parents = graph["parents"].get(key, set())
        flags[key] = dict(
            media_bound=int(key in media_jobs),
            no_recorded_media=int(key not in media_jobs),
            shared_input=int(key in branches),
            chained=int(bool(parents)),
            cross_model=int(
                any(
                    byid[p]["model_identifier"] not in (None, "")
                    and job["model_identifier"] not in (None, "")
                    and byid[p]["model_identifier"] != job["model_identifier"]
                    for p in parents
                )
            ),
            convergent=int(len(parents) >= 2),
            staged_refinement=int(any(graph["parents"].get(p) for p in parents)),
            reference_preparation=int(key in prep),
            image_foundation=int(key in foundation),
            audio_job=int(job["generation_type"] == "audio"),
            finishing_job=int(job["model_identifier"] in FINISH),
            video_candidate=int(
                job["generation_type"] == "video"
                and job["model_identifier"] not in ADAPTERS
            ),
            image_job=int(job["generation_type"] == "image"),
            voice_adapter=int(
                ADAPTERS.get(job["model_identifier"])
                in {"voiceover", "voice_change", "lipsync"}
            ),
        )
    return flags, pairs, triples, graph


def records(db, table):
    frame = db.sql(f"SELECT * FROM {table} ORDER BY film_id").df()
    return frame.astype(object).where(pd.notna(frame), None).to_dict("records")


def routes(db):
    """Reuse merged route definitions and literal controls, without changing them."""
    result = {}
    for name, mod in [("05-image", image), ("06-video", video)]:
        db.execute((ROOT / f"studies/{name}/measures.sql").read_text())
        table = "image_jobs" if name == "05-image" else "video_jobs"
        for row in records(db, table):
            _, obj = mod.parse(row["parameters_json"])
            if name == "05-image":
                route = mod.classify(
                    obj,
                    row["image_inputs"],
                    row["other_inputs"],
                    row["model_identifier"],
                )
            else:
                route = mod.classify(
                    obj,
                    row["image_inputs"],
                    row["video_inputs"],
                    row["audio_inputs"],
                    row["has_start"],
                    row["has_end"],
                    row["unknown_inputs"],
                    row["prompt"],
                )
            result[row["film_id"], row["generation_id"]] = (
                row["generation_type"] + ":" + route
            )
        db.execute(f"DROP TABLE {table}")
        db.execute("DROP TABLE attachments")
        db.execute("DROP TABLE j")
    return result


def panel(db, output, job_lookup, flags):
    cases = []
    for path in sorted((ROOT / "case-files").glob("*/codes.csv")):
        with path.open(newline="") as stream:
            for row in csv.DictReader(stream):
                if row["code_id"].startswith("08."):
                    row["case_source"] = str(path.relative_to(ROOT))
                    cases.append(row)
    assert len(cases) == 80
    write(pd.DataFrame(cases), output / "case_evidence.csv")
    role_rows, contexts, handoffs = [], [], []
    for row in cases:
        fid = row["film_id"]
        ids = re.findall(r"/generation:([\w-]+)", row["entity_ids"])
        if row["code_id"] == "08.1" and row["status"] == "coded":
            # Existing human assignments are scoped, never broadcast to a film.
            assert (
                row["excerpt"].split(" [excerpt boundary] ")[0]
                in job_lookup[fid, ids[0]]["prompt"]
            )
            for role in row["value"].split("|"):
                for gid in ids:
                    j = job_lookup[fid, gid]
                    role_rows.append(
                        dict(
                            film_id=fid,
                            generation_id=gid,
                            model_identifier=j["model_identifier"],
                            requested_role=role,
                            evidence_id=row["evidence_id"],
                            evidence_label="inferred",
                            denominator="One named task; 16 purposive panel films",
                        )
                    )
        if row["code_id"] in {"08.1", "08.5"}:
            for gid in ids:
                j = job_lookup[fid, gid]
                state, obj = video.parse(j["parameters_json"])
                controls = {
                    k: video.control_state(obj, k, state)
                    for k in video.CONTROLS + ["is_inpaint"]
                }
                usages = db.execute(
                    "SELECT asset_id,asset_role,parameter_path,reference_element_id "
                    "FROM bindings "
                    "WHERE film_id=? AND generation_id=? ORDER BY ALL",
                    [fid, gid],
                ).fetchall()
                contexts.append(
                    dict(
                        film_id=fid,
                        generation_id=gid,
                        model_identifier=j["model_identifier"],
                        generation_type=j["generation_type"],
                        evidence_id=row["evidence_id"],
                        prompt_state="unavailable"
                        if j["prompt"] is None
                        else "empty"
                        if j["prompt"] == ""
                        else "nonempty",
                        controls=controls,
                        bindings=usages,
                        metrics=flags[fid, gid],
                        evidence_label="observed",
                        media_contents="unknown",
                        final_use="unknown",
                    )
                )
        if row["code_id"] == "08.3" and row["value"] == "edge_supported":
            assert len(ids) == 2
            p, c = ids
            usages = db.execute(
                "SELECT u.asset_id,u.asset_role,u.parameter_path,"
                "u.reference_element_id "
                "FROM bindings u JOIN film_assets a USING(film_id,asset_id) "
                "WHERE u.film_id=? AND u.generation_id=? AND a.generation_id=? "
                "AND u.asset_role<>'output' ORDER BY ALL",
                [fid, c, p],
            ).fetchall()
            assert usages
            for aid, role, path, ref in usages:
                assert lineage.binding_kind(role, path) == "media"
                handoffs.append(
                    dict(
                        **evidence(
                            fid,
                            row["entity_ids"],
                            row["source_path"],
                            row["excerpt"],
                            row["denominator"],
                        ),
                        producer=p,
                        consumer=c,
                        asset_id=aid,
                        asset_role=role,
                        parameter_path=path,
                        reference_element_id=ref,
                        producer_model=job_lookup[fid, p]["model_identifier"],
                        consumer_model=job_lookup[fid, c]["model_identifier"],
                        evidence_id=row["evidence_id"],
                    )
                )
    write(pd.DataFrame(role_rows), output / "panel_role_matrix.csv")
    write(pd.DataFrame(handoffs), output / "handoff_examples.csv")
    js(output / "panel_contexts.json", contexts)
    assignments = (
        pd.DataFrame(cases)
        .groupby(["code_id", "status", "value"], sort=True)
        .size()
        .reset_index(name="assignments")
    )
    assignments["panel_films_denominator"] = 16
    write(assignments, output / "panel_assignments.csv")


def adapter_examples(db, output, lookup):
    """One deterministic record per declared adapter, no prompt text copied."""
    rows = []
    for model, role in sorted(ADAPTERS.items()):
        jobs = sorted(
            (j for j in lookup.values() if j["model_identifier"] == model),
            key=lambda j: (j["film_id"], j["generation_id"]),
        )
        if not jobs:
            continue
        j = jobs[0]
        fid, gid = j["film_id"], j["generation_id"]
        bindings = db.execute(
            "SELECT asset_id,asset_role,parameter_path,reference_element_id "
            "FROM bindings WHERE film_id=? AND generation_id=? ORDER BY ALL",
            [fid, gid],
        ).fetchall()
        state, obj = video.parse(j["parameters_json"])
        controls = {
            k: video.control_state(obj, k, state)
            for k in [
                "model",
                "mode",
                "model_version",
                "duration",
                "resolution",
                "generate_audio",
            ]
        }
        excerpt = json.dumps(
            dict(
                model_identifier=model,
                model_name=j["model_name"],
                generation_type=j["generation_type"],
                bindings=bindings,
                controls=controls,
            ),
            ensure_ascii=False,
            sort_keys=True,
        )
        rows.append(
            dict(
                **evidence(
                    fid,
                    f"{fid}/generation:{gid}",
                    "generations.model_identifier/model_name/generation_type/"
                    "parameters_json; asset_usages",
                    excerpt,
                    f"One sorted example / {len(jobs)} jobs with literal model; "
                    f"{len({x['film_id'] for x in jobs})}/157 films",
                ),
                generation_id=gid,
                literal_model=model,
                adapter_role=role,
                role_evidence_label="inferred",
            )
        )
    write(pd.DataFrame(rows), output / "adapter_examples.csv")


def build(data, output):
    output.mkdir(parents=True, exist_ok=True)
    upstream = ROOT / "studies/01-corpus/outputs"
    eligibility = read(upstream / "eligibility.csv")
    scope = eligibility[eligibility.study.astype(str).str.zfill(2) == "08"]
    write(scope, output / "eligibility.csv")
    eligible = scope[(scope.population == "primary") & scope.production_eligible][
        ["film_id", "cohort_group"]
    ].sort_values("film_id")
    assert len(eligible) == 157
    taxonomy = read(upstream / "taxonomy.csv").set_index("film_id")
    unusual = set(read(upstream / "unusual_projects.csv").film_id)
    with connect(data) as db:
        db.register("eligible", eligible)
        db.execute((HERE / "measures.sql").read_text())
        co = db.sql("SELECT * FROM cooccurrence ORDER BY ALL").df()
        co_counts = co.groupby("film_id").size().to_dict()
        route_map = routes(db)
        tables = {
            t: records(db, t) for t in ["jobs", "film_assets", "bindings", "elements"]
        }
        groups = {}
        for t, rows in tables.items():
            groups[t] = defaultdict(list)
            for row in rows:
                groups[t][row["film_id"]].append(row)
        lookup = {(j["film_id"], j["generation_id"]): j for j in tables["jobs"]}
        flags, film_rows, numeric_evidence, transition_rows, audits = {}, [], [], [], []
        derived, control_counts = [], Counter()
        for fid in eligible.film_id:
            jobs = groups["jobs"][fid]
            ff, pairs, triples, graph = motifs(
                jobs,
                groups["film_assets"][fid],
                groups["bindings"][fid],
                groups["elements"][fid],
            )
            flags.update({(fid, gid): v for gid, v in ff.items()})
            jl = {j["generation_id"]: j for j in jobs}
            transitions = defaultdict(set)
            assets_by_pair = defaultdict(set)
            for p, a, c in triples:
                pm, cm = jl[p]["model_identifier"], jl[c]["model_identifier"]
                transitions[pm, cm].add((p, c))
                assets_by_pair[pm, cm].add(a)
            for (pm, cm), members in sorted(
                transitions.items(), key=lambda x: str(x[0])
            ):
                transition_rows.append(
                    dict(
                        film_id=fid,
                        producer_model=pm,
                        consumer_model=cm,
                        cross_model=pm is not None and cm is not None and pm != cm,
                        pairs=len(members),
                        consumers=len({c for _, c in members}),
                        assets=len(assets_by_pair[pm, cm]),
                        film_pairs_denominator=len(pairs),
                        film_jobs_denominator=len(jobs),
                    )
                )
            totals = Counter()
            for j in jobs:
                gid, text = j["generation_id"], j["prompt"]
                v = dict(
                    ff[gid],
                    jobs=1,
                    prompt_nonempty=int(text not in (None, "")),
                    prompt_empty=int(text == ""),
                    prompt_unavailable=int(text is None),
                )
                for k in ["edit", "preservation", "reference", "multi_shot"]:
                    v[k + "_words"] = int(bool(text and features.REGEX[k].search(text)))
                ps, obj = video.parse(j["parameters_json"])
                v["invalid_parameters"] = int(ps == "invalid")
                totals.update(v)
                derived.append(
                    dict(
                        film_id=fid,
                        generation_type=j["generation_type"],
                        model_identifier=j["model_identifier"],
                        adapter_role=ADAPTERS.get(
                            j["model_identifier"], "unclassified"
                        ),
                        route=route_map.get((fid, gid), "not_image_or_video"),
                        **v,
                    )
                )
                for k in [
                    "model",
                    "mode",
                    "model_version",
                    "is_inpaint",
                    "generate_audio",
                ]:
                    state, value = video.control_state(obj, k, ps)
                    control_counts[fid, j["model_identifier"], k, state, value] += 1
            for typ in sorted(
                {j["generation_type"] for j in jobs}, key=lambda v: v or ""
            ):
                texts = {
                    j["prompt"]
                    for j in jobs
                    if j["generation_type"] == typ and j["prompt"] not in (None, "")
                }
                for k in ["edit", "preservation", "reference", "multi_shot"]:
                    audits.append(
                        dict(
                            film_id=fid,
                            generation_type=typ,
                            feature=k,
                            matches=sum(
                                len(features.REGEX[k].findall(t)) for t in texts
                            ),
                            distinct_texts_denominator=len(texts),
                        )
                    )
            f = dict(
                film_id=fid,
                cohort_group=taxonomy.loc[fid, "cohort_group"],
                record_orientation=taxonomy.loc[fid, "record_orientation"],
                scale=taxonomy.loc[fid, "scale"],
                unusual=fid in unusual,
                **totals,
                pairs=len(pairs),
                cooccurring_model_pairs=co_counts.get(fid, 0),
                transition_model_pairs=len(transitions),
                literal_models=len(
                    {
                        j["model_identifier"]
                        for j in jobs
                        if j["model_identifier"] is not None
                    }
                ),
                material_bindings=sum(map(len, graph["media"].values())),
                unresolved_bindings=sum(
                    len(cs - {graph["resolved"].get(a)})
                    for a, cs in graph["media"].items()
                    if graph["resolved"].get(a) not in jl
                ),
            )
            film_rows.append(f)
            numeric_evidence.append(
                evidence(
                    fid,
                    f"{fid}/generation:*; {fid}/asset:*; {fid}/reference:*",
                    "studies/08-workflow/measures.sql; build.py motifs/routes; "
                    "generations; assets; asset_usages; reference_elements",
                    json.dumps(f, sort_keys=True),
                    f"{len(jobs)} film jobs; {len(pairs)} distinct resolved "
                    f"producer/consumer pairs; lexical rates use "
                    f"{totals['prompt_nonempty']} nonempty primary fields",
                )
            )
        panel(db, output, lookup, flags)
        adapter_examples(db, output, lookup)
        inventory = db.sql(
            "SELECT film_id,generation_type,model_identifier,model_name,"
            "count(*) AS jobs FROM jobs GROUP BY ALL ORDER BY ALL"
        ).df()
    film = pd.DataFrame(film_rows)
    baseline = read(upstream / "film_metrics.csv").set_index("film_id")
    assert (
        film.set_index("film_id").jobs == baseline.loc[film.film_id].generations
    ).all()
    previous = read(ROOT / "studies/07-lineage/outputs/film_metrics.csv").set_index(
        "film_id"
    )
    for current, old in [
        ("chained", "chained_jobs"),
        ("cross_model", "cross_model_jobs"),
        ("shared_input", "shared_input_jobs"),
        ("convergent", "convergent_jobs"),
    ]:
        assert (
            film.set_index("film_id")[current] == previous.loc[film.film_id, old]
        ).all()
    write(film, output / "film_metrics.csv")
    write(pd.DataFrame(numeric_evidence), output / "metric_evidence.csv")
    metrics = [(k, "jobs") for k in METRICS] + [
        (k + "_words", "prompt_nonempty")
        for k in ["edit", "preservation", "reference", "multi_shot"]
    ]
    metrics.append(("image_foundation", "image_job"))
    summary = summarize(film, metrics, ["cohort_group", "record_orientation", "scale"])
    # Member sets live separately to keep each committed artifact below 1 MB.
    members = {
        f"{r.dimension}:{r.value}": r.film_ids.split(";") for r in summary.itertuples()
    }
    js(output / "summary_members.json", members)
    write(summary.drop(columns="film_ids"), output / "summaries.csv")
    d = pd.DataFrame(derived)
    role_matrix = (
        d.groupby(
            ["film_id", "generation_type", "model_identifier", "route", "adapter_role"],
            dropna=False,
            sort=True,
        )[["jobs", *METRICS]]
        .sum()
        .reset_index()
    )
    role_matrix = role_matrix.merge(
        film[["film_id", "jobs"]].rename(columns={"jobs": "film_jobs_denominator"}),
        on="film_id",
    )
    role_matrix["evidence_label"] = "observed"
    role_matrix["role_evidence_label"] = "inferred"
    write(role_matrix, output / "role_matrix.csv")
    write(
        inventory.merge(
            film[["film_id", "jobs"]].rename(columns={"jobs": "film_jobs_denominator"}),
            on="film_id",
        ),
        output / "model_inventory.csv",
    )
    for dim in ["model_identifier", "generation_type", "route"]:
        counts = (
            d.groupby(["film_id", dim], dropna=False, sort=True)[
                [
                    "jobs",
                    *METRICS,
                    "prompt_nonempty",
                    "edit_words",
                    "preservation_words",
                    "reference_words",
                    "multi_shot_words",
                ]
            ]
            .sum()
            .reset_index()
        )
        counts = counts.merge(eligible, on="film_id")
        write(counts, output / f"by_{dim}.csv")
        summaries = []
        for value, group in counts.groupby(dim, dropna=False, sort=True):
            s = summarize(group, metrics, ["cohort_group"])
            s[dim] = value
            summaries.append(s.drop(columns="film_ids"))
        write(pd.concat(summaries, ignore_index=True), output / f"summary_{dim}.csv")
    transitions = pd.DataFrame(transition_rows).merge(eligible, on="film_id")
    write(transitions, output / "transitions.csv")
    co_rows = []
    for (p, c), g in co.groupby(["producer_model", "consumer_model"], sort=True):
        t = transitions[
            ((transitions.producer_model == p) & (transitions.consumer_model == c))
            | ((transitions.producer_model == c) & (transitions.consumer_model == p))
        ]
        co_rows.append(
            dict(
                model_a=p,
                model_b=c,
                cooccurring_films=len(g),
                transition_films=t.film_id.nunique(),
                film_denominator=157,
                film_ids=";".join(sorted(g.film_id)),
            )
        )
    write(pd.DataFrame(co_rows), output / "cooccurrence.csv")
    ts = []
    for (p, c), g in transitions.groupby(
        ["producer_model", "consumer_model"], dropna=False, sort=True
    ):
        # All eligible films, including zero pair counts, define prevalence/share.
        merged = (
            film[["film_id", "cohort_group", "pairs"]]
            .merge(
                g[["film_id", "pairs"]].rename(columns={"pairs": "transition_pairs"}),
                on="film_id",
                how="left",
            )
            .fillna({"transition_pairs": 0})
        )
        s = summarize(merged, [("transition_pairs", "pairs")], ["cohort_group"]).drop(
            columns="film_ids"
        )
        s["producer_model"], s["consumer_model"] = p, c
        ts.append(s)
    write(pd.concat(ts, ignore_index=True), output / "summary_transitions.csv")
    controls = pd.DataFrame(
        [
            dict(film_id=f, model_identifier=m, control=k, state=s, raw_value=v, jobs=n)
            for (f, m, k, s, v), n in sorted(
                control_counts.items(), key=lambda x: str(x[0])
            )
        ]
    )
    controls = controls.merge(
        d.groupby(["film_id", "model_identifier"], dropna=False)
        .size()
        .reset_index(name="model_jobs_denominator"),
        on=["film_id", "model_identifier"],
    )
    for key, group in controls.groupby("control"):
        write(group, output / f"controls_{key}.csv")
    checks = pd.DataFrame(audits)
    upstream_features = read(ROOT / "prompt-labels/outputs/features_by_stratum.csv")
    upstream_features = upstream_features[
        (upstream_features.population == "primary")
        & (upstream_features.text_role == "primary")
    ]
    checks["upstream_matches"] = [
        int(
            upstream_features[
                (upstream_features.film_id == r.film_id)
                & (
                    upstream_features.generation_type.fillna(NULL)
                    == (r.generation_type if r.generation_type is not None else NULL)
                )
            ][r.feature + "_matches_sum"].sum()
        )
        for r in checks.itertuples()
    ]
    checks["upstream_texts"] = [
        int(
            upstream_features[
                (upstream_features.film_id == r.film_id)
                & (
                    upstream_features.generation_type.fillna(NULL)
                    == (r.generation_type or NULL)
                )
            ].distinct_texts_denominator.sum()
        )
        for r in checks.itertuples()
    ]
    assert (checks.matches == checks.upstream_matches).all()
    assert (checks.distinct_texts_denominator == checks.upstream_texts).all()
    write(checks, output / "structural_check.csv")
    inputs = [
        HERE / "build.py",
        HERE / "measures.sql",
        HERE / "node_contracts.json",
        HERE / "catalogue.json",
        ROOT / "PROGRAMME.md",
        ROOT / "AGENTS.md",
        ROOT / "DATA.md",
        ROOT / "case-files/README.md",
        ROOT / "prompt-labels/README.md",
        ROOT / "prompt-labels/build.py",
        ROOT / "prompt-labels/outputs/features_by_stratum.csv",
    ]
    for name in [
        "01-corpus",
        "02-planning",
        "03-elements",
        "05-image",
        "06-video",
        "07-lineage",
        "10-organisation",
    ]:
        inputs += [ROOT / f"studies/{name}/README.md"]
    inputs += list(upstream.glob("*.csv"))
    inputs += [
        ROOT / f"studies/{n}/build.py" for n in ["05-image", "06-video", "07-lineage"]
    ]
    inputs += [ROOT / f"studies/{n}/measures.sql" for n in ["05-image", "06-video"]]
    inputs += [ROOT / "studies/07-lineage/outputs/film_metrics.csv"]
    for p in sorted((ROOT / "case-files").glob("*/codes.csv")):
        inputs += [p, p.with_name("CASE.md")]
    js(
        output / "reproduction.json",
        dict(
            source_release="data-2026-10-20",
            source_manifest_sha256=digest(data / "SHA256SUMS"),
            inputs={str(p.relative_to(ROOT)): digest(p) for p in sorted(set(inputs))},
            outputs={
                p.name: digest(p)
                for p in sorted(output.iterdir())
                if p.name != "reproduction.json"
            },
        ),
    )
    assert all(p.stat().st_size < 1_000_000 for p in output.iterdir())
    print(
        f"Built {len(film)} films, {int(film.jobs.sum())} jobs, "
        f"{len(transitions)} film/model transitions."
    )


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
        expected = {p.name: digest(p) for p in (HERE / "outputs").iterdir()}
        actual = {p.name: digest(p) for p in args.output.iterdir()}
        assert actual == expected, "Reproduction mismatch"
        print(f"Reproduced all {len(expected)} outputs byte for byte.")


if __name__ == "__main__":
    main()
