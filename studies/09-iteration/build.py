"""Study 09: overlapping candidate families, comparison deltas and further-work use."""

import argparse
import csv
import hashlib
import importlib.util
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import pandas as pd

from film_practice import connect

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NULL = r"\N"
ALT = (
    "Shared context can serve different shots/tasks; chronology is comparison order, "
    "not revision intent. Omitted work, multilingual boilerplate, changed controls "
    "and unresolved cross-ID aliases compete. Use is not approval or benefit."
)
CONF = (
    "Deterministic compound-key counts over released records; checked inherited "
    "graph/structural counts. Case interpretation is single-coder and purposive; "
    "no semantic accuracy, independent agreement or media assessment."
)
BASES = ["shared_asset", "input_set", "batch", "lineage", "similarity_time"]
JOB_METRICS = [f"{b}_member" for b in BASES] + [
    "supported_member",
    "rerun_candidate",
    "adopted",
    "supported_adopted",
    "prompt_nonempty",
    "prompt_empty",
    "prompt_unavailable",
    "batch_nonempty",
    "edit_words",
    "preservation_words",
]
PAIR_METRICS = [
    "text_comparable",
    "text_equal",
    "text_changed",
    "token_addition",
    "token_deletion",
    "longer_text",
    "preservation_added",
    "preservation_removed",
    "inputs_changed",
    "input_added",
    "input_removed",
    "input_replacement_candidate",
    "model_comparable",
    "model_changed",
    "controls_comparable",
    "controls_changed",
    "role_bindings_changed",
    "same_type",
]


def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lineage = module("lineage09", "studies/07-lineage/build.py")
features = module("features09", "prompt-labels/build.py")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_hash(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def read(path):
    return pd.read_csv(path, keep_default_na=False, na_values=[NULL])


def write(frame, path):
    frame.to_csv(
        path, index=False, na_rep=NULL, float_format="%.9f", lineterminator="\n"
    )


def js(path, obj):
    path.write_text(
        json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
    )


def evidence(fid, ids, source, excerpt, denominator, label="observed"):
    return dict(
        study="09",
        film_id=fid,
        entity_ids=ids,
        source_path=source,
        excerpt=excerpt,
        evidence_label=label,
        competing_explanation=ALT,
        denominator=denominator,
        confidence_rationale=CONF,
    )


def summarize(frame, ratios, dimensions=()):
    rows = []
    groups = [("all", "primary", frame)]
    for dim in dimensions:
        groups.extend((dim, value, g) for value, g in frame.groupby(dim, dropna=False))
    for dim, value, group in groups:
        for n, d in ratios:
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
                )
            )
    return pd.DataFrame(rows)


def controls(raw):
    state, obj = lineage.parse(raw)
    if state != "object":
        return state, None
    # Only compare top-level non-text, non-media controls. Do not emit text/containers.
    excluded = {
        "prompt",
        "negative_prompt",
        "prompt_language",
        "enhanced_prompt",
        "source_prompt",
        "reference_elements",
        "medias",
        "input_images",
        "input_image",
        "input_video",
        "input_audio",
        "multi_prompt",
        "image_reference",
        "custom_reference",
        "paint_image",
        "end_input_image",
    }
    return state, {
        k: v
        for k, v in obj.items()
        if k not in excluded and not isinstance(v, (dict, list))
    }


def prepare(jobs, graph, usages):
    result = {}
    inputs, bindings = defaultdict(set), defaultdict(set)
    for aid, consumers in graph["media"].items():
        for gid in consumers:
            inputs[gid].add(aid)
    for u in usages:
        if lineage.binding_kind(u["asset_role"], u["parameter_path"]) == "media":
            bindings[u["generation_id"]].add(
                (
                    u["asset_id"],
                    u["asset_role"],
                    u["parameter_path"],
                    u["reference_element_id"],
                )
            )
    for j in jobs:
        gid, text = j["generation_id"], j["prompt"]
        result[gid] = dict(
            j,
            inputs=inputs[gid],
            bindings=bindings[gid],
            tokens=Counter(text.split()) if text else Counter(),
            text_hash=text_hash(text) if text is not None else None,
            timestamp=datetime.fromisoformat(j["created_at"].replace("Z", "+00:00"))
            if j["created_at"]
            else None,
            control=controls(j["parameters_json"]),
            preservation=bool(text and features.REGEX["preservation"].search(text)),
        )
    return result


def order(j):
    # Invalid/unknown dates cannot establish temporal similarity; IDs break ties only.
    return (
        j["timestamp"].timestamp() if j["timestamp"] is not None else float("-inf"),
        j["generation_id"],
    )


def families(context, graph):
    """Return separate evidence sets. No transitive union of shared-input jobs."""
    groups = {b: [] for b in BASES}
    for aid, members in sorted(graph["media"].items()):
        if len(members) >= 2:
            groups["shared_asset"].append((aid, sorted(members)))
    sets, batches = defaultdict(list), defaultdict(list)
    for gid, j in context.items():
        if j["inputs"] and j["generation_type"] not in (None, ""):
            sets[j["generation_type"], tuple(sorted(j["inputs"]))].append(gid)
        if j["generation_batch_id"] not in (None, ""):
            batches[j["generation_batch_id"]].append(gid)
    for key, members in sorted(sets.items()):
        if len(members) >= 2:
            groups["input_set"].append((text_hash(canonical(key)), sorted(members)))
    for key, members in sorted(batches.items()):
        if len(members) >= 2:
            groups["batch"].append((key, sorted(members)))
    pairs = sorted(
        (p, c)
        for c, ps in graph["parents"].items()
        for p in ps
        if p in context and c in context and p != c
    )
    groups["lineage"] = [(p + ":" + c, [p, c]) for p, c in pairs]
    buckets = defaultdict(list)
    for gid, j in context.items():
        if (
            j["timestamp"] is not None
            and j["prompt"] not in (None, "")
            and j["generation_type"] not in (None, "")
            and j["model_identifier"] not in (None, "")
        ):
            buckets[j["generation_type"], j["model_identifier"]].append(gid)
    for _, members in sorted(buckets.items()):
        members.sort(key=lambda g: (context[g]["timestamp"], g))
        for a, b in zip(members, members[1:], strict=False):
            ja, jb = context[a], context[b]
            ta, tb = set(ja["tokens"]), set(jb["tokens"])
            hours = (jb["timestamp"] - ja["timestamp"]).total_seconds() / 3600
            if (
                min(len(ta), len(tb)) >= 10
                and hours <= 24
                and len(ta & tb) / len(ta | tb) >= 0.8
            ):
                groups["similarity_time"].append((a + ":" + b, [a, b]))
    return groups


def delta(a, b):
    comparable = a["prompt"] not in (None, "") and b["prompt"] not in (None, "")
    models = a["model_identifier"] not in (None, "") and b["model_identifier"] not in (
        None,
        "",
    )
    cc = a["control"][0] == b["control"][0] == "object"
    return dict(
        pairs=1,
        text_comparable=int(comparable),
        text_equal=int(comparable and a["prompt"] == b["prompt"]),
        text_changed=int(comparable and a["prompt"] != b["prompt"]),
        token_addition=int(comparable and bool(b["tokens"] - a["tokens"])),
        token_deletion=int(comparable and bool(a["tokens"] - b["tokens"])),
        longer_text=int(comparable and len(b["prompt"]) > len(a["prompt"])),
        preservation_added=int(
            comparable and not a["preservation"] and b["preservation"]
        ),
        preservation_removed=int(
            comparable and a["preservation"] and not b["preservation"]
        ),
        inputs_changed=int(a["inputs"] != b["inputs"]),
        input_added=int(bool(b["inputs"] - a["inputs"])),
        input_removed=int(bool(a["inputs"] - b["inputs"])),
        input_replacement_candidate=int(
            bool(b["inputs"] - a["inputs"]) and bool(a["inputs"] - b["inputs"])
        ),
        model_comparable=int(models),
        model_changed=int(models and a["model_identifier"] != b["model_identifier"]),
        controls_comparable=int(cc),
        controls_changed=int(cc and a["control"][1] != b["control"][1]),
        role_bindings_changed=int(a["bindings"] != b["bindings"]),
        same_type=int(
            a["generation_type"] not in (None, "")
            and a["generation_type"] == b["generation_type"]
        ),
    )


def analyse(jobs, assets, usages, refs):
    graph = lineage.graph(jobs, assets, usages, refs)
    context = prepare(jobs, graph, usages)
    groups = families(context, graph)
    flags = {g: {k: 0 for k in JOB_METRICS} for g in context}
    for basis, rows in groups.items():
        for _, members in rows:
            for g in members:
                flags[g][basis + "_member"] = 1
    reruns = defaultdict(list)
    for g, j in context.items():
        if (
            j["prompt"] not in (None, "")
            and j["inputs"]
            and j["model_identifier"] not in (None, "")
            and j["generation_type"] not in (None, "")
        ):
            reruns[
                j["generation_type"],
                j["model_identifier"],
                j["text_hash"],
                tuple(sorted(j["inputs"])),
            ].append(g)
    for members in reruns.values():
        if len(members) >= 2:
            for g in members:
                flags[g]["rerun_candidate"] = 1
    for g, j in context.items():
        f = flags[g]
        f["supported_member"] = int(any(f[b + "_member"] for b in BASES[:-1]))
        f["adopted"] = int(bool(graph["adjacency"].get(g)))
        f["supported_adopted"] = f["supported_member"] * f["adopted"]
        f["prompt_nonempty"] = int(j["prompt"] not in (None, ""))
        f["prompt_empty"] = int(j["prompt"] == "")
        f["prompt_unavailable"] = int(j["prompt"] is None)
        f["batch_nonempty"] = int(j["generation_batch_id"] not in (None, ""))
        for k in ["edit", "preservation"]:
            f[k + "_words"] = int(
                bool(j["prompt"] and features.REGEX[k].search(j["prompt"]))
            )
    return context, graph, groups, flags


def comparison_pairs(basis, rows, context):
    # Shared-asset fans are context screens only; no arbitrary pairwise revision census.
    if basis == "shared_asset":
        return []
    pairs = set()
    for _, members in rows:
        if basis not in {"lineage", "similarity_time"}:
            members = sorted(members, key=lambda g: order(context[g]))
        pairs.update(zip(members, members[1:], strict=False))
    return sorted(pairs)


def panel(output, contexts, graphs):
    cases, histories, checks = [], [], []
    for path in sorted((ROOT / "case-files").glob("*/codes.csv")):
        rows = [
            dict(r, case_source=str(path.relative_to(ROOT)))
            for r in csv.DictReader(path.open(newline=""))
            if r["code_id"].startswith("09.")
        ]
        cases.extend(rows)
        fid = rows[0]["film_id"]
        ctx, graph = contexts[fid], graphs[fid]
        for r in rows:
            ids = list(
                dict.fromkeys(re.findall(r"/generation:([\w-]+)", r["entity_ids"]))
            )
            assert all(g in ctx for g in ids)
            if r["code_id"] == "09.2" and r["value"] == "local_correction_request":
                span = r["excerpt"].split(" [excerpt boundary] ")[0]
                assert span in ctx[ids[0]]["prompt"], r["evidence_id"]
            if r["code_id"] == "09.1" and r["status"] == "coded":
                shared = set.intersection(*(ctx[g]["inputs"] for g in ids))
                assert shared
                checks.append(
                    dict(
                        film_id=fid,
                        evidence_id=r["evidence_id"],
                        members=len(ids),
                        shared_material_assets=len(shared),
                        exact_text_equal=len({ctx[g]["prompt"] for g in ids}) == 1,
                        full_input_sets_equal=len(
                            {tuple(sorted(ctx[g]["inputs"])) for g in ids}
                        )
                        == 1,
                    )
                )
            if r["code_id"] in {"09.3", "09.4"} and r["status"] == "coded":
                assert len(ids) == 2
                a, b = ids
                linked = a in graph["parents"].get(b, set())
                if r["code_id"] == "09.4" or "producer/consumer" in r["denominator"]:
                    assert linked
                histories.append(
                    dict(
                        evidence_id=r["evidence_id"],
                        film_id=fid,
                        code_id=r["code_id"],
                        interpretation=r["value"],
                        interpretation_label="inferred"
                        if r["code_id"] == "09.3"
                        else "observed",
                        producer_consumer_edge=linked,
                        comparison_order="producer_to_consumer"
                        if linked
                        else "named_comparison_only",
                        members=[context_record(ctx[g]) for g in ids],
                        delta=delta(ctx[a], ctx[b]),
                        approval="unknown",
                    )
                )
    spans = json.loads((HERE / "readings.json").read_text())
    span_rows = []
    by_evidence = {r["evidence_id"]: r for r in cases}
    for entry in spans:
        row = by_evidence[entry["evidence_id"]]
        ids = list(
            dict.fromkeys(re.findall(r"/generation:([\w-]+)", row["entity_ids"]))
        )
        gid = ids[entry["member_index"]]
        assert entry["span"] in contexts[row["film_id"]][gid]["prompt"]
        assert len(entry["span"]) < len(contexts[row["film_id"]][gid]["prompt"])
        span_rows.append(
            dict(
                **evidence(
                    row["film_id"],
                    f"{row['film_id']}/generation:{gid}",
                    "generations.prompt",
                    entry["span"],
                    row["denominator"],
                ),
                evidence_id=entry["evidence_id"],
                member_index=entry["member_index"],
            )
        )
    write(pd.DataFrame(span_rows), output / "revision_spans.csv")
    assert len(cases) == 64
    write(pd.DataFrame(cases), output / "case_evidence.csv")
    assignments = (
        pd.DataFrame(cases)
        .groupby(["code_id", "status", "value"], sort=True)
        .size()
        .reset_index(name="assignments")
    )
    assignments["panel_films_denominator"] = 16
    write(assignments, output / "panel_assignments.csv")
    write(pd.DataFrame(checks), output / "panel_family_checks.csv")
    js(output / "revision_histories.json", histories)


def raw_selected_controls(raw):
    state, obj = lineage.parse(raw)
    keys = [
        "model",
        "mode",
        "model_version",
        "duration",
        "resolution",
        "aspect_ratio",
        "is_inpaint",
        "multi_shots",
        "generate_audio",
        "draft",
        "extension_mode",
        "width",
        "height",
        "output_width",
        "output_height",
        "seed",
    ]
    result = {}
    for k in keys:
        if state != "object":
            result[k] = {"state": state, "raw_value": None}
        elif k not in obj:
            result[k] = {"state": "absent", "raw_value": None}
        elif isinstance(obj[k], (list, dict)):
            result[k] = {"state": "container", "raw_value": None}
        else:
            result[k] = {
                "state": "null" if obj[k] is None else "scalar",
                "raw_value": obj[k],
            }
    return result


def context_record(j):
    return dict(
        generation_id=j["generation_id"],
        generation_type=j["generation_type"],
        model_identifier=j["model_identifier"],
        generation_batch_id=j["generation_batch_id"],
        prompt_state="unavailable"
        if j["prompt"] is None
        else "empty"
        if j["prompt"] == ""
        else "nonempty",
        prompt_sha256=j["text_hash"],
        bindings=sorted(j["bindings"], key=lambda x: canonical(x)),
        parameter_state=j["control"][0],
        # Full control semantics stay in source; hashes avoid text publication.
        nonmedia_scalar_controls_sha256=text_hash(canonical(j["control"][1])),
        raw_selected_controls=raw_selected_controls(j["parameters_json"]),
        source_path="generations.prompt/parameters_json; asset_usages",
    )


def build(data, output):
    output.mkdir(parents=True, exist_ok=True)
    upstream = ROOT / "studies/01-corpus/outputs"
    scope = read(upstream / "eligibility.csv")
    scope = scope[scope.study.astype(str).str.zfill(2) == "09"]
    write(scope, output / "eligibility.csv")
    eligible = scope[(scope.population == "primary") & scope.production_eligible][
        ["film_id", "cohort_group"]
    ].sort_values("film_id")
    assert len(eligible) == 157
    tax = read(upstream / "taxonomy.csv").set_index("film_id")
    unusual = set(read(upstream / "unusual_projects.csv").film_id)
    film_rows, job_rows, pair_rows, family_rows, examples, audits = (
        [],
        [],
        [],
        [],
        [],
        [],
    )
    contexts, graphs = {}, {}
    panel_ids = set(read(upstream / "panel.csv").film_id)
    with connect(data) as db:
        db.register("eligible", eligible)
        db.execute((HERE / "measures.sql").read_text())
        tables = {}
        for t in ["jobs", "bindings", "film_assets", "elements"]:
            frame = db.sql(f"SELECT * FROM {t} ORDER BY film_id").df()
            records = (
                frame.astype(object).where(pd.notna(frame), None).to_dict("records")
            )
            tables[t] = defaultdict(list)
            for r in records:
                tables[t][r["film_id"]].append(r)
        for fid in eligible.film_id:
            jobs = tables["jobs"][fid]
            ctx, graph, groups, flags = analyse(
                jobs,
                tables["film_assets"][fid],
                tables["bindings"][fid],
                tables["elements"][fid],
            )
            if fid in panel_ids:
                contexts[fid], graphs[fid] = ctx, graph
            totals = Counter()
            for g, j in ctx.items():
                v = dict(jobs=1, **flags[g])
                totals.update(v)
                job_rows.append(
                    dict(
                        film_id=fid,
                        generation_type=j["generation_type"],
                        model_identifier=j["model_identifier"],
                        **v,
                    )
                )
            f = dict(
                film_id=fid,
                cohort_group=tax.loc[fid, "cohort_group"],
                record_orientation=tax.loc[fid, "record_orientation"],
                scale=tax.loc[fid, "scale"],
                unusual=fid in unusual,
                **totals,
            )
            film_rows.append(f)
            for basis, rows in groups.items():
                members = {g for _, gs in rows for g in gs}
                family_rows.append(
                    dict(
                        film_id=fid,
                        basis=basis,
                        families=len(rows),
                        member_jobs=len(members),
                        jobs=len(jobs),
                        largest_family=max((len(gs) for _, gs in rows), default=0),
                        families_with_adoption=sum(
                            any(flags[g]["adopted"] for g in gs) for _, gs in rows
                        ),
                    )
                )
                pairs = comparison_pairs(basis, rows, ctx)
                by = defaultdict(Counter)
                for a, b in pairs:
                    values = delta(ctx[a], ctx[b])
                    by[ctx[b]["generation_type"], ctx[b]["model_identifier"]].update(
                        values
                    )
                for (typ, mod), values in sorted(by.items(), key=lambda x: str(x[0])):
                    pair_rows.append(
                        dict(
                            film_id=fid,
                            basis=basis,
                            generation_type=typ,
                            model_identifier=mod,
                            **values,
                        )
                    )
                if pairs and fid in panel_ids:
                    a, b = pairs[0]
                    examples.append(
                        dict(
                            **evidence(
                                fid,
                                f"{fid}/generation:{a};{fid}/generation:{b}",
                                "build.py:families/comparison_pairs/delta; "
                                "generations; asset_usages; assets",
                                canonical(delta(ctx[a], ctx[b])),
                                f"One example / {len(pairs)} {basis} pairs; "
                                f"{len(jobs)} film jobs",
                            ),
                            basis=basis,
                            members=[context_record(ctx[a]), context_record(ctx[b])],
                        )
                    )
            for typ in sorted({j["generation_type"] for j in jobs}, key=str):
                texts = {
                    j["prompt"]
                    for j in jobs
                    if j["generation_type"] == typ and j["prompt"] not in (None, "")
                }
                for k in ["edit", "preservation"]:
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
    film = pd.DataFrame(film_rows)
    baseline = read(upstream / "film_metrics.csv").set_index("film_id")
    assert (
        film.set_index("film_id").jobs == baseline.loc[film.film_id].generations
    ).all()
    previous = read(ROOT / "studies/07-lineage/outputs/film_metrics.csv").set_index(
        "film_id"
    )
    assert (
        film.set_index("film_id").shared_asset_member
        == previous.loc[film.film_id].shared_input_jobs
    ).all()
    write(film, output / "film_metrics.csv")
    ledgers = [
        evidence(
            r["film_id"],
            f"{r['film_id']}/generation:*;{r['film_id']}/asset:*;{r['film_id']}/reference:*",
            "measures.sql; build.py:analyse/families/delta; generations; "
            "assets; asset_usages; reference_elements",
            canonical(r),
            f"{r['jobs']} film jobs; text denominators and membership in excerpt; "
            "pair/family denominators in corresponding rows",
        )
        for r in film_rows
    ]
    write(pd.DataFrame(ledgers), output / "metric_evidence.csv")
    ratios = [
        (k, "jobs")
        for k in JOB_METRICS
        if k not in {"edit_words", "preservation_words", "supported_adopted"}
    ] + [
        ("edit_words", "prompt_nonempty"),
        ("preservation_words", "prompt_nonempty"),
        ("supported_adopted", "supported_member"),
    ]
    write(
        summarize(film, ratios, ["cohort_group", "record_orientation", "scale"]),
        output / "summaries.csv",
    )
    members = {"all:primary": sorted(film.film_id)}
    for dim in ["cohort_group", "record_orientation", "scale"]:
        for value, g in film.groupby(dim):
            members[f"{dim}:{value}"] = sorted(g.film_id)
    js(output / "summary_members.json", members)
    d = pd.DataFrame(job_rows)
    for dim in ["generation_type", "model_identifier"]:
        counts = (
            d.groupby(["film_id", dim], dropna=False, sort=True)[["jobs", *JOB_METRICS]]
            .sum()
            .reset_index()
            .merge(eligible, on="film_id")
        )
        write(counts, output / f"by_{dim}.csv")
        summaries = []
        for value, g in counts.groupby(dim, dropna=False):
            s = summarize(g, ratios, ["cohort_group"])
            s[dim] = value
            summaries.append(s)
        write(pd.concat(summaries, ignore_index=True), output / f"summary_{dim}.csv")
    fam = pd.DataFrame(family_rows).merge(eligible, on="film_id")
    write(fam, output / "families_by_film.csv")
    write(
        pd.concat(
            [
                summarize(
                    g,
                    [("member_jobs", "jobs"), ("families_with_adoption", "families")],
                    ["cohort_group"],
                ).assign(basis=b)
                for b, g in fam.groupby("basis")
            ],
            ignore_index=True,
        ),
        output / "summary_families.csv",
    )
    pairs = pd.DataFrame(pair_rows).merge(eligible, on="film_id")
    # Compact files below 1 MB; all comparisons regenerable from source.
    pair_ratios = [
        (
            k,
            "text_comparable"
            if k
            in {
                "text_equal",
                "text_changed",
                "token_addition",
                "token_deletion",
                "longer_text",
                "preservation_added",
                "preservation_removed",
            }
            else "model_comparable"
            if k == "model_changed"
            else "controls_comparable"
            if k == "controls_changed"
            else "pairs",
        )
        for k in PAIR_METRICS
    ]
    pair_films = (
        pairs.groupby(["film_id", "basis"], sort=True)[["pairs", *PAIR_METRICS]]
        .sum()
        .reset_index()
        .merge(eligible, on="film_id")
    )
    grid = pd.MultiIndex.from_product(
        [eligible.film_id, BASES[1:]], names=["film_id", "basis"]
    ).to_frame(index=False)
    pair_films = grid.merge(
        pair_films.drop(columns="cohort_group"), on=["film_id", "basis"], how="left"
    )
    pair_films[["pairs", *PAIR_METRICS]] = (
        pair_films[["pairs", *PAIR_METRICS]].fillna(0).astype(int)
    )
    pair_films = pair_films.merge(eligible, on="film_id")
    write(pair_films, output / "comparisons_by_film.csv")
    write(
        pd.concat(
            [
                summarize(g, pair_ratios, ["cohort_group"]).assign(basis=b)
                for b, g in pair_films.groupby("basis")
            ],
            ignore_index=True,
        ),
        output / "summary_comparisons.csv",
    )
    for dim in ["generation_type", "model_identifier"]:
        counts = (
            pairs.groupby(
                ["film_id", "basis", dim, "cohort_group"], dropna=False, sort=True
            )[["pairs", *PAIR_METRICS]]
            .sum()
            .reset_index()
        )
        for basis, group in counts.groupby("basis"):
            write(group, output / f"comparisons_{basis}_{dim}.csv")
    js(output / "comparison_examples.json", examples)
    panel(output, contexts, graphs)
    checks = pd.DataFrame(audits)
    af = read(ROOT / "prompt-labels/outputs/features_by_stratum.csv")
    af = af[(af.population == "primary") & (af.text_role == "primary")]
    checks["upstream_matches"] = [
        int(
            af[
                (af.film_id == r.film_id)
                & (af.generation_type.fillna(NULL) == (r.generation_type or NULL))
            ][r.feature + "_matches_sum"].sum()
        )
        for r in checks.itertuples()
    ]
    checks["upstream_texts"] = [
        int(
            af[
                (af.film_id == r.film_id)
                & (af.generation_type.fillna(NULL) == (r.generation_type or NULL))
            ].distinct_texts_denominator.sum()
        )
        for r in checks.itertuples()
    ]
    assert (checks.matches == checks.upstream_matches).all()
    assert (checks.distinct_texts_denominator == checks.upstream_texts).all()
    write(checks, output / "structural_check.csv")
    inputs = [
        HERE / n
        for n in [
            "build.py",
            "measures.sql",
            "taxonomy.json",
            "review_states.json",
            "readings.json",
            "catalogue.json",
        ]
    ]
    inputs += [
        ROOT / n
        for n in [
            "AGENTS.md",
            "PROGRAMME.md",
            "DATA.md",
            "case-files/README.md",
            "prompt-labels/README.md",
            "prompt-labels/build.py",
            "prompt-labels/outputs/features_by_stratum.csv",
            "studies/07-lineage/build.py",
            "studies/07-lineage/outputs/film_metrics.csv",
        ]
    ]
    for name in [
        "01-corpus",
        "02-planning",
        "03-elements",
        "05-image",
        "06-video",
        "07-lineage",
        "08-workflow",
        "10-organisation",
    ]:
        inputs.append(ROOT / f"studies/{name}/README.md")
    inputs += list(upstream.glob("*.csv"))
    inputs += [
        ROOT / f"studies/01-corpus/{n}.md"
        for n in ["CODEBOOK", "DICTIONARY", "PROVENANCE"]
    ]
    for path in sorted((ROOT / "case-files").glob("*/codes.csv")):
        inputs += [path, path.with_name("CASE.md")]
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
    for p in output.iterdir():
        if p.stat().st_size >= 1_000_000:
            raise ValueError(f"Release required: {p.name} ({p.stat().st_size} bytes)")
    print(
        f"Built {len(film)} films / {int(film.jobs.sum())} jobs; "
        f"{len(checks)} structural checks; {len(pairs)} comparison strata."
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
