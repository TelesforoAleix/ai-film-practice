"""Batch-one exhaustive profiles and deterministic purposive reading register.

Run from the repository root. No network calls or semantic labels; source views
stay strings. Local reading packets (full fields) stay under ignored data/.
"""

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from film_practice import TABLES, connect

ROOT = Path(__file__).resolve().parent
SLUGS = {
    "Dry Aged Dreams": "dry-aged-dreams",
    "The Staff": "the-staff",
    "A Tales Before Titanic Tragedy": "a-tales-before-titanic-tragedy",
    "APEIROPHOBIA": "apeirophobia",
}


def records(db, table, fid):
    result = db.execute(f"SELECT * FROM {table} WHERE film_id=?", [fid])
    names = [c[0] for c in result.description]
    return [dict(zip(names, r, strict=True)) for r in result.fetchall()]


def distribution(rows, field):
    counts = Counter(r[field] for r in rows)
    return [
        {"value": k, "count": v}
        for k, v in sorted(
            counts.items(), key=lambda item: (item[0] is not None, str(item[0]))
        )
    ]


def profile(db, panel):
    fid = panel["film_id"]
    tables = {t: records(db, t, fid) for t in TABLES}
    jobs = sorted(tables["generations"], key=lambda r: r["generation_id"])
    byid = {r["generation_id"]: r for r in jobs}
    usages = defaultdict(list)
    for u in tables["asset_usages"]:
        usages[u["generation_id"]].append(u)
    placements = defaultdict(list)
    for p in tables["generation_folders"]:
        placements[p["generation_id"]].append(p["folder_id"])
    assets = {a["asset_id"]: a for a in tables["assets"]}
    edges = sorted(
        {
            (
                a["generation_id"],
                u["generation_id"],
                u["asset_id"],
                u["asset_role"],
                u["parameter_path"],
            )
            for u in tables["asset_usages"]
            if u["asset_role"] != "output"
            if (a := assets.get(u["asset_id"])) and a["generation_id"] in byid
        }
    )
    selected = defaultdict(set)

    def choose(rows, reason):
        if rows:
            selected[rows[0]["generation_id"]].add(reason)

    def strata(groups, prefix):
        for key, group in sorted(groups.items(), key=lambda x: str(x[0])):
            choose(group, f"{prefix}:{key}")

    if len(jobs) < 100:
        for g in jobs:
            selected[g["generation_id"]].add("exhaustive_small_history")
    else:
        groups = defaultdict(list)
        for g in jobs:
            groups[(g["generation_type"], g["model_identifier"])].append(g)
        strata(groups, "type_model")
        groups = defaultdict(list)
        for g in jobs:
            for folder in placements[g["generation_id"]]:
                groups[folder].append(g)
        strata(groups, "folder")
        groups = defaultdict(list)
        for g in jobs:
            inputs = [
                u for u in usages[g["generation_id"]] if u["asset_role"] != "output"
            ]
            roles = tuple(sorted({u["asset_role"] for u in inputs}))
            groups[(g["generation_type"], roles)].append(g)
        strata(groups, "input_role_set")
        groups = defaultdict(list)
        for g in jobs:
            try:
                obj = json.loads(g["parameters_json"])
            except (TypeError, ValueError):
                selected[g["generation_id"]].add("invalid_parameters")
                continue
            for key in ["model", "is_inpaint", "multi_shots", "generate_audio"]:
                if key in obj:
                    groups[(g["model_identifier"], key, str(obj[key]))].append(g)
            # Every disclosed reference element gets an attached-use example.
            for u in usages[g["generation_id"]]:
                if u["reference_element_id"]:
                    groups[("reference", u["reference_element_id"])].append(g)
        strata(groups, "control_or_reference")
        groups = defaultdict(list)
        for producer, consumer, _, role, _ in edges:
            groups[
                (
                    byid[producer]["model_identifier"],
                    byid[consumer]["model_identifier"],
                    role,
                )
            ].append(byid[consumer])
        for key, group in sorted(groups.items()):
            choose(group, f"edge_consumer:{key}")
            consumer = group[0]["generation_id"]
            producer = next(
                e[0]
                for e in edges
                if e[1] == consumer
                and byid[e[0]]["model_identifier"] == key[0]
                and e[3] == key[2]
            )
            selected[producer].add(f"edge_producer:{key}")
        texts = [g for g in jobs if g["prompt"]]
        choose(
            sorted(texts, key=lambda g: (len(g["prompt"]), g["generation_id"])),
            "shortest_nonempty_prompt",
        )
        choose(
            sorted(texts, key=lambda g: (-len(g["prompt"]), g["generation_id"])),
            "longest_prompt",
        )
    invalid = []
    params = Counter()
    for g in jobs:
        try:
            obj = json.loads(g["parameters_json"])
        except (TypeError, ValueError):
            invalid.append(g["generation_id"])
            continue
        for key in [
            "model",
            "is_inpaint",
            "multi_shots",
            "generate_audio",
            "duration",
            "resolution",
            "aspect_ratio",
        ]:
            params[
                (
                    g["model_identifier"],
                    key,
                    json.dumps(obj[key], ensure_ascii=False)
                    if key in obj
                    else "<unavailable>",
                )
            ] += 1
    summary = {
        "release": "data-2026-10-20",
        "film_id": fid,
        "title": panel["title"],
        "cohort_group": panel["cohort_group"],
        "row_counts": {t: len(rows) for t, rows in tables.items()},
        "measure_provenance": {
            t: {
                "study": "02-10 case-file preparation",
                "film_id": fid,
                "entity_ids": f"{fid}/{t}: all film-scoped source rows",
                "source_path": f"{t}.*; case-files/profile.py:profile",
                "excerpt": f"exported rows={len(rows)}",
                "evidence_label": "observed",
                "competing_explanation": (
                    "Public export can omit external/private work; these are "
                    "record counts, not the whole production."
                ),
                "denominator": (
                    f"{len(rows)} exported {t} rows for this one film; "
                    "field states and distributions partition those rows"
                ),
                "confidence_rationale": (
                    "Exact film-key filter; all columns profiled; raw null and "
                    "empty text separate. Grains follow Study 01. Graph count "
                    "uses explicit asset producers and distinct usage tuples, "
                    "not visual aliases. No semantic labels computed."
                ),
            }
            for t, rows in tables.items()
        },
        "field_states": {
            t: {
                column: {
                    "unavailable": sum(r[column] is None for r in rows),
                    "empty": sum(r[column] == "" for r in rows),
                    "nonempty": sum(r[column] not in (None, "") for r in rows),
                }
                for column in (rows[0] if rows else [])
            }
            for t, rows in tables.items()
        },
        "generations": {
            k: distribution(jobs, k)
            for k in [
                "generation_type",
                "model_identifier",
                "model_name",
                "author_user_id",
                "generation_status",
            ]
        },
        "prompt_states": {
            "unavailable": sum(g["prompt"] is None for g in jobs),
            "empty": sum(g["prompt"] == "" for g in jobs),
            "nonempty": sum(bool(g["prompt"]) for g in jobs),
            "distinct_nonempty": len({g["prompt"] for g in jobs if g["prompt"]}),
        },
        "text_roles": distribution(tables["generation_prompts"], "prompt_role"),
        "usage_roles": distribution(tables["asset_usages"], "asset_role"),
        "parameter_controls": [
            dict(model=m, path=k, value=v, count=n)
            for (m, k, v), n in sorted(params.items())
        ],
        "invalid_parameters": invalid,
        "folders": [
            {k: r[k] for k in ["folder_id", "folder_name", "parent_folder_id"]}
            | {
                "generation_placements": sum(
                    p["folder_id"] == r["folder_id"]
                    for p in tables["generation_folders"]
                )
            }
            for r in sorted(tables["folders"], key=lambda r: r["folder_id"])
        ],
        "references": [
            {k: r[k] for k in ["reference_element_id", "name", "category"]}
            for r in sorted(
                tables["reference_elements"], key=lambda r: r["reference_element_id"]
            )
        ],
        "graph": {
            "explicit_distinct_producer_consumer_asset_role_path_edges": len(edges),
            "distinct_input_assets": len(
                {
                    u["asset_id"]
                    for u in tables["asset_usages"]
                    if u["asset_role"] != "output"
                }
            ),
            "alias_policy": "Exact asset IDs only; no URL or visual alias merging",
        },
        "reading_register": [
            {"generation_id": gid, "reasons": sorted(reasons)}
            for gid, reasons in sorted(selected.items())
        ],
    }
    dest = ROOT / SLUGS[panel["title"]]
    dest.mkdir(exist_ok=True)
    (dest / "profile.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    )
    packet = {
        "film": tables["films"],
        "folders": tables["folders"],
        "references": tables["reference_elements"],
        "brief_assets": tables["brief_assets"],
        "jobs": [byid[gid] | {"usages": usages[gid]} for gid in sorted(selected)],
        "edges": edges,
    }
    local = Path("data/af2a")
    local.mkdir(exist_ok=True)
    (local / (SLUGS[panel["title"]] + ".json")).write_text(
        json.dumps(packet, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        panel["title"],
        len(jobs),
        "jobs;",
        len(selected),
        "selected;",
        len(edges),
        "explicit edges",
    )


def main():
    with (ROOT.parent / "studies/01-corpus/outputs/panel.csv").open() as stream:
        panel = [r for r in csv.DictReader(stream) if r["batch"] == "1"]
    with connect("data") as db:
        for film in panel:
            profile(db, film)


if __name__ == "__main__":
    main()
