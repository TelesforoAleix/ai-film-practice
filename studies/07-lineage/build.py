"""Study 07: film-scoped disclosed dependency graphs and bounded review sets."""

import argparse
import csv
import gzip
import hashlib
import importlib.util
import io
import json
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

from film_practice import connect

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NULL = r"\N"
PRESETS = {
    "params.style",
    "params.camera_lens",
    "params.camera_model",
    "params.color_preset",
    "params.camera_aperture",
    "params.camera_focal_length",
    "params.pacing",
    "params.light",
    "params.genre_control",
    "params.era_control",
    "params.preset",
    "params.motion",
    "params.application",
}
ALT = (
    "Disclosed graph only; omitted external/private work and unresolved cross-ID "
    "aliases can change topology. Shared inputs need not represent the same shot "
    "or entity. Reuse does not establish approval, continuity or benefit."
)
CONF = (
    "Exact compound-key counts and deterministic traversal of released records; "
    "no media inspection, independent semantic agreement or causal inference."
)
NODE_COLUMNS = [
    "film_id",
    "node_kind",
    "node_id",
    "record_state",
    "generation_type",
    "model_identifier",
    "asset_type",
]
EDGE_COLUMNS = [
    "film_id",
    "source_kind",
    "source_id",
    "target_kind",
    "target_id",
    "edge_type",
    "asset_role",
    "parameter_path",
    "reference_element_id",
    "source_path",
]
RATIOS = [
    ("jobs_with_media", "jobs"),
    ("chained_jobs", "jobs"),
    ("shared_input_jobs", "jobs"),
    ("hybrid_jobs", "jobs"),
    ("convergent_jobs", "jobs"),
    ("cross_model_jobs", "jobs"),
    ("reused_media_assets", "media_input_assets"),
    ("resolved_media_bindings", "media_bindings"),
    ("preservation_words", "prompt_nonempty"),
    ("reference_words", "prompt_nonempty"),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path):
    return pd.read_csv(path, keep_default_na=False, na_values=[NULL])


def write_json(path, value):
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    )


def write_csv(frame, path):
    frame.to_csv(
        path, index=False, na_rep=NULL, float_format="%.9f", lineterminator="\n"
    )


def evidence(fid, entities, source, excerpt, denominator, label="observed"):
    return dict(
        study="07",
        film_id=fid,
        entity_ids=entities,
        source_path=source,
        excerpt=excerpt,
        evidence_label=label,
        competing_explanation=ALT,
        denominator=denominator,
        confidence_rationale=CONF,
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


def binding_kind(role, path):
    if role == "output":
        return "output"
    if role != "input_asset":
        return "media"
    if path in PRESETS or (
        path and path.startswith("params.multi_prompt[") and path.endswith("].preset")
    ):
        return "preset"
    if path and (
        path.startswith("params.input_images[")
        or path
        in {
            "params.input_image",
            "params.image_reference",
            "params.custom_reference",
            "params.paint_image",
            "params.end_input_image",
            "params.input_video",
            "params.input_audio",
        }
    ):
        return "media"
    return "unknown"


def reachable(adjacency, roots):
    """Cycle-safe, unique descendants, excluding the changed roots themselves."""
    seen = set(roots)
    todo = list(roots)
    while todo:
        for child in adjacency.get(todo.pop(), ()):
            if child not in seen:
                seen.add(child)
                todo.append(child)
    return seen - set(roots)


def components(nodes, edges):
    adj = defaultdict(set)
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    remaining = set(nodes)
    sizes = []
    isolated = []
    while remaining:
        root = min(remaining)
        part = reachable(adj, [root]) | {root}
        remaining -= part
        sizes.append(len(part))
        if len(part) == 1:
            isolated.append(root)
    return sorted(sizes, reverse=True), sorted(isolated)


def cyclic_nodes(adjacency, nodes):
    """Kahn residual is audited separately from strongly connected membership."""
    # Exact cycle membership using iterative Kosaraju, avoiding recursion limits.
    reverse = defaultdict(set)
    for a, children in adjacency.items():
        for b in children:
            reverse[b].add(a)
    visited, order = set(), []
    for root in sorted(nodes):
        if root in visited:
            continue
        stack = [(root, False)]
        while stack:
            a, done = stack.pop()
            if done:
                order.append(a)
            elif a not in visited:
                visited.add(a)
                stack.append((a, True))
                stack.extend(
                    (b, False)
                    for b in sorted(adjacency.get(a, ()), reverse=True)
                    if b not in visited
                )
    visited, cycles = set(), set()
    for root in reversed(order):
        if root in visited:
            continue
        group, todo = set(), [root]
        while todo:
            a = todo.pop()
            if a in visited:
                continue
            visited.add(a)
            group.add(a)
            todo.extend(reverse.get(a, ()))
        if len(group) > 1 or root in adjacency.get(root, ()):
            cycles |= group
    return cycles


def graph(jobs, assets, usages, references):
    """Build all nodes, including detached assets/elements and unresolved stubs."""
    nodes, edges = {}, set()
    producers = defaultdict(set)
    jid = {j["generation_id"] for j in jobs}
    aset = {a["asset_id"] for a in assets}
    rid = {r["reference_element_id"] for r in references}
    for j in jobs:
        nodes["generation", j["generation_id"]] = (
            "recorded",
            j["generation_type"],
            j["model_identifier"],
            None,
        )
    for a in assets:
        nodes["asset", a["asset_id"]] = ("recorded", None, None, a["asset_type"])
        if a["generation_id"] in jid:
            producers[a["asset_id"]].add(a["generation_id"])
            edges.add(
                (
                    "generation",
                    a["generation_id"],
                    "asset",
                    a["asset_id"],
                    "produces",
                    None,
                    None,
                    None,
                    "assets.generation_id",
                )
            )
    for r in references:
        nodes["reference", r["reference_element_id"]] = ("recorded", None, None, None)
        _, obj = parse(r["metadata_json"])
        for field in ["medias", "video_medias", "audio_medias"]:
            values = obj.get(field, []) if obj else []
            if not isinstance(values, list):
                continue
            for i, media in enumerate(values):
                aid = media.get("id") if isinstance(media, dict) else None
                if not isinstance(aid, str) or not aid:
                    continue
                nodes.setdefault(("asset", aid), ("metadata_only", None, None, None))
                edges.add(
                    (
                        "reference",
                        r["reference_element_id"],
                        "asset",
                        aid,
                        "groups_media",
                        None,
                        f"metadata_json.{field}[{i}]",
                        r["reference_element_id"],
                        "reference_elements.metadata_json",
                    )
                )
    for u in usages:
        aid, g, r = u["asset_id"], u["generation_id"], u["reference_element_id"]
        if aid is None or aid == "":
            raise ValueError("Missing asset identity cannot define an edge")
        nodes.setdefault(("asset", aid), ("usage_only", None, None, None))
        kind = binding_kind(u["asset_role"], u["parameter_path"])
        if kind == "output":
            producers[aid].add(g)
            edge = ("generation", g, "asset", aid, "produces")
        else:
            edge = ("asset", aid, "generation", g, kind + "_input")
        edges.add((*edge, u["asset_role"], u["parameter_path"], r, "asset_usages"))
        if r not in (None, ""):
            nodes.setdefault(("reference", r), ("usage_only", None, None, None))
            edges.add(
                (
                    "reference",
                    r,
                    "generation",
                    g,
                    "reference_binding",
                    u["asset_role"],
                    u["parameter_path"],
                    r,
                    "asset_usages",
                )
            )
    # Producers are accepted only when exactly one existing job is disclosed.
    # Self input and conflicting producer assignments stay explicitly unresolved.
    resolved = {a: next(iter(ps)) for a, ps in producers.items() if len(ps) == 1}
    raw, media, ref_users, parent = (
        defaultdict(set),
        defaultdict(set),
        defaultdict(set),
        defaultdict(set),
    )
    adjacency = defaultdict(set)
    kinds = Counter()
    missing_refs, missing_assets, self_inputs = set(), set(), set()
    for u in usages:
        k = binding_kind(u["asset_role"], u["parameter_path"])
        kinds[k] += 1
        if k == "output":
            continue
        a, g, r = u["asset_id"], u["generation_id"], u["reference_element_id"]
        raw[a].add(g)
        if a not in aset:
            missing_assets.add(a)
        if r not in (None, ""):
            ref_users[r].add(g)
            if r not in rid:
                missing_refs.add(r)
        if k != "media":
            continue
        media[a].add(g)
        p = resolved.get(a)
        if p == g:
            self_inputs.add((a, g))
        elif p is not None:
            adjacency[p].add(g)
            parent[g].add(p)
    return dict(
        nodes=nodes,
        edges=sorted(edges, key=lambda e: tuple("" if v is None else v for v in e)),
        producers=producers,
        resolved=resolved,
        raw=raw,
        media=media,
        refs=ref_users,
        parents=parent,
        adjacency=adjacency,
        kinds=kinds,
        missing_refs=missing_refs,
        missing_assets=missing_assets,
        self_inputs=self_inputs,
    )


def aggregate(frame, dimensions):
    rows = []
    groups = [("all", "primary", frame)]
    for dim in dimensions:
        groups += [
            (dim, str(v), g) for v, g in frame.groupby(dim, dropna=False, sort=True)
        ]
    for dim, value, group in groups:
        for n, d in RATIOS:
            if n not in group or d not in group:
                continue
            valid = group[group[d] > 0]
            shares = valid[n] / valid[d]
            den = int(valid[d].sum())
            rows.append(
                dict(
                    dimension=dim,
                    value=value,
                    metric=n,
                    denominator_name=d,
                    eligible_films=len(group),
                    measured_films=len(valid),
                    films_with_numerator=int((group[n] > 0).sum()),
                    numerator=int(valid[n].sum()),
                    denominator=den,
                    equal_film_mean=shares.mean(),
                    median=shares.median(),
                    q25=shares.quantile(0.25),
                    q75=shares.quantile(0.75),
                    pooled_share=int(valid[n].sum()) / den if den else None,
                    film_ids=";".join(sorted(group.film_id)),
                )
            )
    return pd.DataFrame(rows)


def compressed_csv(path, columns):
    handle = gzip.GzipFile(filename="", mode="wb", fileobj=path.open("wb"), mtime=0)
    stream = io.TextIOWrapper(handle, encoding="utf-8", newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(columns)
    return stream, writer


def build(data, output, large):
    output.mkdir(parents=True, exist_ok=True)
    large.mkdir(parents=True, exist_ok=True)
    upstream = ROOT / "studies/01-corpus/outputs"
    eligibility = read_csv(upstream / "eligibility.csv")
    eligibility = eligibility[eligibility.study.astype(str).str.zfill(2) == "07"]
    write_csv(eligibility, output / "eligibility.csv")
    eligible = eligibility[
        (eligibility.population == "primary") & eligibility.production_eligible
    ]
    assert len(eligible) == 157
    taxonomy = read_csv(upstream / "taxonomy.csv").set_index("film_id")
    panel = read_csv(upstream / "panel.csv").set_index("film_id")
    features_spec = importlib.util.spec_from_file_location(
        "lineage_features", ROOT / "prompt-labels/build.py"
    )
    features = importlib.util.module_from_spec(features_spec)
    features_spec.loader.exec_module(features)
    with connect(data) as db:
        db.register("eligible", eligible[["film_id"]])
        db.execute((HERE / "measures.sql").read_text())
        # One fetch per table; no other working files under data are read.
        tables = {}
        for t in ["jobs", "bindings", "film_assets", "elements"]:
            grouped = defaultdict(list)
            result = db.sql("SELECT * FROM " + t + " ORDER BY ALL")
            cols = [c[0] for c in result.description]
            for record in result.fetchall():
                row = dict(zip(cols, record, strict=True))
                grouped[row["film_id"]].append(row)
            tables[t] = grouped
    node_stream, node_writer = compressed_csv(large / "nodes.csv.gz", NODE_COLUMNS)
    edge_stream, edge_writer = compressed_csv(large / "edges.csv.gz", EDGE_COLUMNS)
    metrics, strata, ledgers, hubs, reviews, aliases, maps, checks = (
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    )
    review_summaries = []
    cases = []
    for p in sorted((ROOT / "case-files").glob("*/codes.csv")):
        with p.open(newline="") as f:
            for r in csv.DictReader(f):
                if r["code_id"].startswith("07.") or r["code_id"] == "03.6":
                    r["case_source"] = p.relative_to(ROOT).as_posix()
                    cases.append(r)
    for fid in sorted(eligible.film_id):
        jobs, usages, assets, refs = (
            tables[t][fid] for t in ["jobs", "bindings", "film_assets", "elements"]
        )
        g = graph(jobs, assets, usages, refs)
        jmap = {j["generation_id"]: j for j in jobs}
        for (kind, nid), values in sorted(g["nodes"].items()):
            node_writer.writerow(
                [fid, kind, nid, *[NULL if x is None else x for x in values]]
            )
        for edge in g["edges"]:
            edge_writer.writerow([fid, *[NULL if x is None else x for x in edge]])
        material_edges = [
            (("asset", a), ("generation", c))
            for a, cs in g["media"].items()
            for c in cs
        ]
        material_edges += [
            (("generation", p), ("asset", a))
            for a, ps in g["producers"].items()
            for p in ps
        ]
        sizes, isolated = components(g["nodes"], material_edges)
        all_sizes, _ = components(g["nodes"], [(e[:2], e[2:4]) for e in g["edges"]])
        cycles = cyclic_nodes(g["adjacency"], jmap)
        shared_jobs = (
            set().union(*(cs for cs in g["media"].values() if len(cs) >= 2))
            if g["media"]
            else set()
        )
        chain_jobs = set(g["parents"])
        cross = {
            c
            for c, ps in g["parents"].items()
            if any(
                jmap[p]["model_identifier"] is not None
                and jmap[c]["model_identifier"] is not None
                and jmap[p]["model_identifier"] != jmap[c]["model_identifier"]
                for p in ps
            )
        }
        resolved_bindings = sum(
            1
            for a, cs in g["media"].items()
            for c in cs
            if a in g["resolved"] and g["resolved"][a] != c
        )
        base = dict(
            film_id=fid,
            title=taxonomy.loc[fid, "title"],
            cohort_group=taxonomy.loc[fid, "cohort_group"],
            record_orientation=taxonomy.loc[fid, "record_orientation"],
            scale=taxonomy.loc[fid, "scale"],
        )
        job_rows = []
        for j in jobs:
            jid = j["generation_id"]
            text = j["prompt"]
            jr = dict(
                film_id=fid,
                generation_id=jid,
                cohort_group=base["cohort_group"],
                generation_type=j["generation_type"],
                model_identifier=j["model_identifier"],
                jobs=1,
                jobs_with_media=int(any(jid in cs for cs in g["media"].values())),
                chained_jobs=int(jid in chain_jobs),
                shared_input_jobs=int(jid in shared_jobs),
                hybrid_jobs=int(jid in shared_jobs & chain_jobs),
                convergent_jobs=int(len(g["parents"].get(jid, ())) >= 2),
                cross_model_jobs=int(jid in cross),
                prompt_nonempty=int(text not in (None, "")),
                preservation_words=int(
                    bool(text and features.REGEX["preservation"].search(text))
                ),
                reference_words=int(
                    bool(text and features.REGEX["reference"].search(text))
                ),
            )
            job_rows.append(jr)
        frame = pd.DataFrame(job_rows)
        m = {
            **base,
            **{
                c: int(frame[c].sum())
                for c in frame
                if c
                not in [
                    "film_id",
                    "generation_id",
                    "cohort_group",
                    "generation_type",
                    "model_identifier",
                ]
            },
            "asset_nodes": sum(k == "asset" for k, _ in g["nodes"]),
            "reference_nodes": sum(k == "reference" for k, _ in g["nodes"]),
            "recorded_assets": len(assets),
            "recorded_references": len(refs),
            "graph_nodes": len(g["nodes"]),
            "typed_edges": len(g["edges"]),
            "usage_occurrences": len(usages),
            "raw_input_assets": len(g["raw"]),
            "raw_reused_assets": sum(len(cs) >= 2 for cs in g["raw"].values()),
            "media_input_assets": len(g["media"]),
            "reused_media_assets": sum(len(cs) >= 2 for cs in g["media"].values()),
            "media_bindings": sum(map(len, g["media"].values())),
            "resolved_media_bindings": resolved_bindings,
            "preset_occurrences": g["kinds"]["preset"],
            "unknown_input_occurrences": g["kinds"]["unknown"],
            "missing_asset_records": len(g["missing_assets"]),
            "missing_reference_records": len(g["missing_refs"]),
            "conflicting_producer_assets": sum(
                len(ps) > 1 for ps in g["producers"].values()
            ),
            "self_input_bindings": len(g["self_inputs"]),
            "cyclic_generations": len(cycles),
            "material_components": len(sizes),
            "largest_material_component_nodes": sizes[0],
            "all_edge_components": len(all_sizes),
            "isolated_material_nodes": len(isolated),
            "max_media_consumers": max(map(len, g["media"].values()), default=0),
            "resolved_job_pairs": sum(map(len, g["adjacency"].values())),
        }
        metrics.append(m)
        ledgers.append(
            evidence(
                fid,
                fid + "/all generation,asset,reference keys in named tables",
                "generations; assets; asset_usages; reference_elements; "
                "studies/07-lineage/measures.sql; build.py",
                json.dumps(m, ensure_ascii=False, sort_keys=True),
                f"{len(jobs)} jobs; {len(assets)} asset records; "
                f"{len(refs)} reference records; {len(usages)} usage occurrences; "
                "individual ratios in README section 3",
            )
        )
        for dim in ["generation_type", "model_identifier"]:
            cols = [
                "jobs",
                "jobs_with_media",
                "chained_jobs",
                "shared_input_jobs",
                "hybrid_jobs",
                "convergent_jobs",
                "cross_model_jobs",
                "prompt_nonempty",
                "preservation_words",
                "reference_words",
            ]
            for value, sub in frame.groupby(dim, dropna=False, sort=True):
                strata.append(
                    dict(
                        film_id=fid,
                        cohort_group=base["cohort_group"],
                        dimension=dim,
                        value=None if pd.isna(value) else value,
                        **{c: int(sub[c].sum()) for c in cols},
                    )
                )
        # Full asset/reference fan-out and transitive review census goes in release.
        film_reviews = []
        for kind, users in [("asset", g["media"]), ("reference", g["refs"])]:
            for key, cs in sorted(users.items()):
                scope = cs | reachable(g["adjacency"], cs)
                row = dict(
                    film_id=fid,
                    node_kind=kind,
                    node_id=key,
                    direct_jobs=len(cs),
                    reachable_jobs=len(scope),
                    jobs_denominator=len(jobs),
                )
                film_reviews.append(row)
        reviews.extend(film_reviews)
        for kind in ["asset", "reference"]:
            rr = pd.DataFrame([r for r in film_reviews if r["node_kind"] == kind])
            values = rr.reachable_jobs if len(rr) else pd.Series(dtype=float)
            review_summaries.append(
                dict(
                    film_id=fid,
                    node_kind=kind,
                    input_nodes_denominator=len(values),
                    jobs_denominator=len(jobs),
                    mean_reachable_jobs=values.mean(),
                    median_reachable_jobs=values.median(),
                    q25=values.quantile(0.25),
                    q75=values.quantile(0.75),
                    max_reachable_jobs=values.max(),
                    max_reachable_job_share=values.max() / len(jobs),
                    evidence_label="observed",
                )
            )
        for kind, users in [("asset", g["media"]), ("reference", g["refs"])]:
            if not users:
                continue
            key = min(users, key=lambda k: (-len(users[k]), k))
            cs = users[key]
            hubs.append(
                {
                    **evidence(
                        fid,
                        f"{fid}/{kind}:{key}",
                        "asset_usages; assets.generation_id; build.py:graph/reachable",
                        f"distinct consumers={len(cs)}; "
                        f"total {kind} input nodes={len(users)}",
                        f"{len(jobs)} jobs; {len(users)} distinct input {kind} nodes",
                    ),
                    "node_kind": kind,
                    "node_id": key,
                    "consumers": len(cs),
                    "jobs": len(jobs),
                    "reachable_jobs": next(
                        r["reachable_jobs"]
                        for r in film_reviews
                        if r["node_kind"] == kind and r["node_id"] == key
                    ),
                }
            )
        ar = Counter()
        url_ids = defaultdict(set)
        for a in assets:
            state, obj = parse(a["metadata_json"])
            ar["metadata_" + state] += 1
            if obj:
                if isinstance(obj.get("raw"), dict) and isinstance(
                    obj.get("min"), dict
                ):
                    ar["grouped_raw_min"] += 1
                for name in ["raw", "min", "h264", "hls"]:
                    rep = obj.get(name)
                    if (
                        isinstance(rep, dict)
                        and isinstance(rep.get("url"), str)
                        and rep["url"]
                    ):
                        url_ids[rep["url"]].add(a["asset_id"])
            ar["explicit_source_id"] += int(a["source_asset_id"] not in (None, ""))
        aliases.append(
            dict(
                film_id=fid,
                assets_denominator=len(assets),
                **{
                    k: ar[k]
                    for k in [
                        "metadata_object",
                        "metadata_unavailable",
                        "metadata_empty",
                        "metadata_invalid",
                        "metadata_nonobject",
                        "grouped_raw_min",
                        "explicit_source_id",
                    ]
                },
                cross_id_representation_url_groups=sum(
                    len(ids) > 1 for ids in url_ids.values()
                ),
                cross_id_merges=0,
            )
        )
        # Recheck the unchanged structural regex at AF3a film-distinct primary grain.
        texts = {
            (j["generation_type"], j["prompt"])
            for j in jobs
            if j["prompt"] not in (None, "")
        }
        checks.append(
            dict(
                film_id=fid,
                distinct_type_primary_text_pairs=len(texts),
                preservation_matches_sum=sum(
                    len(features.REGEX["preservation"].findall(t)) for _, t in texts
                ),
                reference_matches_sum=sum(
                    len(features.REGEX["reference"].findall(t)) for _, t in texts
                ),
            )
        )
        if fid in panel.index:
            code_rows = [r for r in cases if r["film_id"] == fid]
            named = set()
            for r in code_rows:
                for item in r["entity_ids"].split("; "):
                    if "/" in item and ":" in item.split("/", 1)[1]:
                        k, i = item.split("/", 1)[1].split(":", 1)
                        if (k, i) in g["nodes"]:
                            named.add((k, i))
            map_edges = [e for e in g["edges"] if e[:2] in named and e[2:4] in named]
            root_case = next(r for r in code_rows if r["code_id"] == "07.5")
            review = None
            if root_case["status"] == "coded":
                root = root_case["excerpt"].split("[root generation] ")[1].split(";")[0]
                expected = set(
                    root_case["excerpt"]
                    .split("[reachable generation IDs] ")[1]
                    .split(",")
                )
                actual = reachable(g["adjacency"], [root])
                assert actual == expected, (fid, "case descendant mismatch")
                review = dict(
                    root=root,
                    generation_ids=sorted(actual),
                    evidence_id=root_case["evidence_id"],
                    evidence_label="proposed",
                    observed_basis="explicit graph reachability",
                )
            maps.append(
                dict(
                    film_id=fid,
                    title=base["title"],
                    whole_graph_metrics=m,
                    named_nodes=[dict(kind=k, id=i) for k, i in sorted(named)],
                    named_edges=[
                        dict(zip(EDGE_COLUMNS[1:], e, strict=True)) for e in map_edges
                    ],
                    case_evidence_ids=[r["evidence_id"] for r in code_rows],
                    review=review,
                    complete_graph=(
                        "study-07-v1 nodes.csv.gz + edges.csv.gz filtered "
                        "by film_id; includes disconnected nodes"
                    ),
                    material_component_sizes=sizes,
                    isolated_generation_ids=[
                        i for k, i in isolated if k == "generation"
                    ],
                    evidence_label="observed",
                    interpretation=(
                        "Named semantic strategies retain case evidence labels; "
                        "high degree implies no canonical authority."
                    ),
                )
            )
    node_stream.close()
    edge_stream.close()
    metric_frame = pd.DataFrame(metrics)
    write_csv(metric_frame, output / "film_metrics.csv")
    write_csv(pd.DataFrame(ledgers), output / "metric_evidence.csv")
    write_csv(
        aggregate(metric_frame, ["cohort_group", "record_orientation", "scale"]),
        output / "summaries.csv",
    )
    sf = pd.DataFrame(strata)
    write_csv(sf, output / "by_task_model.csv")
    sr = []
    members = {}
    for (dim, value), f in sf.groupby(["dimension", "value"], dropna=False, sort=True):
        for cohort in ["all", *sorted(f.cohort_group.unique())]:
            group = f if cohort == "all" else f[f.cohort_group == cohort]
            a = aggregate(group, [])
            member_key = f"{dim}:{value}:{cohort}"
            members[member_key] = sorted(group.film_id)
            a = a.drop(columns=["film_ids"])
            a["member_key"] = member_key
            a["stratum_dimension"] = dim
            a["stratum_value"] = value
            a["cohort_group"] = cohort
            sr.append(a)
    write_csv(pd.concat(sr, ignore_index=True), output / "summary_task_model.csv")
    write_json(output / "summary_members.json", members)
    write_csv(pd.DataFrame(hubs), output / "hubs.csv")
    write_csv(pd.DataFrame(aliases), output / "alias_audit.csv")
    write_csv(pd.DataFrame(review_summaries), output / "review_summary.csv")
    write_csv(pd.DataFrame(cases), output / "case_evidence.csv")
    write_json(output / "panel_maps.json", maps)
    # Compressed census is deterministic and contains keys/counts, never prompts.
    rs, rw = compressed_csv(large / "review_census.csv.gz", list(reviews[0]))
    for r in reviews:
        rw.writerow(r.values())
    rs.close()
    checks = pd.DataFrame(checks)
    baseline = read_csv(ROOT / "prompt-labels/outputs/features_by_film.csv").set_index(
        "film_id"
    )
    # AF3a by-film includes nested text; compare primary-only sum of by-stratum.
    bs = read_csv(ROOT / "prompt-labels/outputs/features_by_stratum.csv")
    bs = bs[(bs.population == "primary") & (bs.text_role == "primary")]
    bs = bs.groupby("film_id")[
        ["preservation_matches_sum", "reference_matches_sum"]
    ].sum()
    for _, r in checks.iterrows():
        for c in ["preservation_matches_sum", "reference_matches_sum"]:
            assert r[c] == bs.loc[r.film_id, c], (r.film_id, c)
        assert r.film_id in baseline.index
    checks["af3a_equal"] = True
    write_csv(checks, output / "structural_check.csv")
    sources = [
        HERE / "build.py",
        HERE / "measures.sql",
        HERE / "queries.sql",
        HERE / "invalidation_policy.json",
        HERE / "catalogue.json",
        ROOT / "PROGRAMME.md",
        ROOT / "AGENTS.md",
        ROOT / "prompt-labels/build.py",
    ]
    sources += [
        upstream / n
        for n in [
            "eligibility.csv",
            "taxonomy.csv",
            "film_metrics.csv",
            "unusual_projects.csv",
            "panel.csv",
        ]
    ]
    sources += [
        ROOT / "prompt-labels/outputs/features_by_stratum.csv",
        ROOT / "prompt-labels/outputs/features_by_film.csv",
    ]
    sources += sorted((ROOT / "case-files").glob("*/codes.csv"))
    sources += sorted((ROOT / "case-files").glob("*/CASE.md"))
    sources += [
        ROOT / f"studies/{s}/README.md"
        for s in [
            "01-corpus",
            "02-planning",
            "03-elements",
            "05-image",
            "06-video",
            "10-organisation",
        ]
    ]
    write_json(
        output / "release_manifest.json",
        dict(
            release="study-07-v1",
            assets={
                p.name: dict(sha256=digest(p), bytes=p.stat().st_size)
                for p in sorted(large.iterdir())
                if p.name != "SHA256SUMS"
            },
            node_columns=NODE_COLUMNS,
            edge_columns=EDGE_COLUMNS,
        ),
    )
    (large / "SHA256SUMS").write_text(
        "".join(
            f"{digest(p)}  {p.name}\n"
            for p in sorted(large.iterdir())
            if p.name != "SHA256SUMS"
        )
    )
    write_json(
        output / "reproduction.json",
        dict(
            release="data-2026-10-20",
            source_manifest_sha256=digest(data / "SHA256SUMS"),
            inputs={p.relative_to(ROOT).as_posix(): digest(p) for p in sources},
            outputs={
                p.name: digest(p)
                for p in sorted(output.iterdir())
                if p.name != "reproduction.json"
            },
            primary_films=157,
            jobs=130704,
        ),
    )
    for p in output.iterdir():
        assert p.stat().st_size < 1_000_000, (p.name, p.stat().st_size)
    print(
        f"Built {len(list(output.iterdir()))} small outputs; "
        "157 films / 130704 jobs; large graph assets hashed"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, default=HERE / "outputs")
    parser.add_argument(
        "--large-output", type=Path, default=Path("data/study07-release")
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check and args.output.resolve() == (HERE / "outputs").resolve():
        parser.error("--check needs separate output")
    build(args.data, args.output, args.large_output)
    if args.check:
        assert {p.name: p.read_bytes() for p in args.output.iterdir()} == {
            p.name: p.read_bytes() for p in (HERE / "outputs").iterdir()
        }, "Output reproduction differs"
        print("Every committed output and large-asset digest reproduced byte for byte")


if __name__ == "__main__":
    main()
