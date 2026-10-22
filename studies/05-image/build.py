"""Study 05: image bindings, literal controls and bounded construction evidence."""

import argparse
import csv
import hashlib
import importlib.util
import json
import re
from collections import Counter
from functools import cache
from pathlib import Path

import pandas as pd

from film_practice import connect

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NULL = r"\N"
ROUTES = [
    "fresh_candidate",
    "reference_guided",
    "multi_input",
    "local_edit",
    "reframe",
    "upscale",
    "unknown",
]
CONTROLS = [
    "is_inpaint",
    "width",
    "height",
    "output_width",
    "output_height",
    "aspect_ratio",
    "resolution",
    "rotate_degree",
    "move_forward_level",
    "vertical_angle",
    "is_all_angles_dump",
    "expand_top",
    "expand_bottom",
    "expand_left",
    "expand_right",
    "mode",
    "remove_bg",
    "sharpen",
    "denoise",
]
ALTERNATIVE = (
    "Public records omit external/private work; raw asset IDs may alias. "
    "Attachments do not verify media contents; prompt matches can be quoted, "
    "negated or miss other languages. No outcome or approval follows."
)
CONFIDENCE = (
    "Deterministic exported-record count under documented film-scoped rules; "
    "semantic completeness, independent agreement and causal benefit unmeasured."
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


def mechanisms(obj, prefix="$"):
    """Inventory exact mask/layer key paths, without treating text as controls."""
    found = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = prefix + "." + key
            if re.search(r"(?:^|_)(?:mask|masks|layer|layers)(?:$|_)", key):
                kind, raw = state(obj, key)
                active = (
                    value is not None
                    and value is not False
                    and value != 0
                    and value != ""
                    and value != []
                    and value != {}
                )
                found.append((path, kind, raw, active))
            found.extend(mechanisms(value, path))
    elif isinstance(obj, list):
        for value in obj:
            found.extend(mechanisms(value, prefix + "[*]"))
    return found


def classify(obj, image_inputs, other_inputs, model):
    """Conservative recorded route; requested intent remains an independent axis."""
    if obj is not None:
        if obj.get("is_inpaint") is True or any(x[3] for x in mechanisms(obj)):
            return "local_edit"

        def number(key):
            v = obj.get(key)
            return v if type(v) in (int, float) else 0

        enlarged = (
            number("output_width") > number("width") > 0
            or number("output_height") > number("height") > 0
        )
        if image_inputs and (
            model == "bytedance_image_upscale"
            or model in ("topaz_image", "topaz_image_generative")
            and enlarged
        ):
            return "upscale"
        if image_inputs and (
            (
                model == "qwen_camera_control"
                and any(
                    number(k) != 0
                    for k in ["rotate_degree", "move_forward_level", "vertical_angle"]
                )
            )
            or model == "flux_2_pro_outpaint"
            and any(
                number("expand_" + k) != 0 for k in ["top", "bottom", "left", "right"]
            )
        ):
            return "reframe"
    if image_inputs > 1:
        return "multi_input"
    if image_inputs == 1:
        return "reference_guided"
    media_keys = [
        "input_image",
        "medias",
        "reference_elements",
        "image_reference",
        "custom_reference",
        "paint_image",
    ]
    populated_media = obj is not None and any(
        obj.get(k) not in (None, "", [], {}) for k in media_keys
    )
    if (
        obj is not None
        and not other_inputs
        and not populated_media
        and obj.get("input_images") == []
    ):
        return "fresh_candidate"
    return "unknown"


def evidence(fid, entities, source, excerpt, denominator, label="observed"):
    return dict(
        study="05",
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


def ids(row):
    return list(
        dict.fromkeys(
            re.findall(
                re.escape(row["film_id"]) + r"/generation:([\w-]+)", row["entity_ids"]
            )
        )
    )


def panel_outputs(db, output):
    cases, contexts, edges = [], [], []
    for path in sorted((ROOT / "case-files").glob("*/codes.csv")):
        rows = [
            r for r in csv.DictReader(path.open()) if r["code_id"].startswith("05.")
        ]
        assert len(rows) == 5
        for row in rows:
            row["case_source"] = path.relative_to(ROOT).as_posix()
            cases.append(row)
        fid = rows[0]["film_id"]
        tasks = sorted({g for r in rows for g in ids(r)})
        # Each named source span must occur in at least one of that assignment's jobs.
        for row in rows:
            if row["status"] != "coded":
                continue
            texts = [
                db.execute(
                    "SELECT prompt FROM j WHERE film_id=? AND generation_id=?", [fid, g]
                ).fetchone()[0]
                or ""
                for g in ids(row)
            ]
            opening = row["excerpt"].split(" [excerpt boundary] ")[0]
            if not opening.startswith("["):
                assert any(opening in t for t in texts), row["evidence_id"]
        for gid in tasks:
            job = db.execute(
                "SELECT generation_type,model_identifier,prompt_source_path,"
                "parameters_json FROM j WHERE film_id=? AND generation_id=?",
                [fid, gid],
            ).fetchone()
            assert job
            inputs = db.execute(
                "SELECT asset_id,asset_role,parameter_path,reference_element_id,"
                "image_binding,producer,producer_type FROM attachments "
                "WHERE film_id=? AND generation_id=? ORDER BY ALL",
                [fid, gid],
            ).fetchall()
            bindings = [
                dict(
                    zip(
                        [
                            "asset_id",
                            "asset_role",
                            "parameter_path",
                            "reference_element_id",
                            "image_binding",
                            "producer",
                            "producer_type",
                        ],
                        x,
                        strict=True,
                    )
                )
                for x in inputs
            ]
            ps, obj = parse(job[3])
            contexts.append(
                dict(
                    film_id=fid,
                    generation_id=gid,
                    generation_type=job[0],
                    model_identifier=job[1],
                    prompt_source_path=job[2],
                    parameter_state=ps,
                    literal_controls={
                        k: dict(zip(["state", "raw_json"], state(obj, k), strict=True))
                        for k in CONTROLS
                    },
                    attachments=bindings,
                    evidence_ids=[r["evidence_id"] for r in rows if gid in ids(r)],
                    evidence_label="observed",
                    denominator="One named job; attachments are occurrence rows",
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
                                f"{fid}/generation:{gid}; {fid}/asset:{b['asset_id']}",
                                "assets.generation_id; "
                                "asset_usages.asset_role/parameter_path",
                                json.dumps(b, sort_keys=True),
                                "One explicit input edge occurrence; no alias collapse",
                            ),
                            producer=b["producer"],
                            consumer=gid,
                            asset_id=b["asset_id"],
                            asset_role=b["asset_role"],
                            parameter_path=b["parameter_path"],
                        )
                    )
    write_csv(pd.DataFrame(cases), output / "case_evidence.csv")
    write_json(output / "panel_contexts.json", contexts)
    recipes = []
    for row in cases:
        if row["code_id"] != "05.2":
            continue
        scoped = [c for c in contexts if row["evidence_id"] in c["evidence_ids"]]
        recipes.append(
            dict(
                evidence=row,
                construction_label="inferred",
                sequence="Resolved producer outputs then named consumer input; "
                "unresolved external sources retained without invented steps",
                jobs=scoped,
                layer_or_mask_claim="unsupported unless explicitly disclosed",
                applicability="Named construction task only; no outcome or benefit",
                tradeoff="More explicit dependencies to record and review",
                failure_mode="Mistaking conditioning or a request "
                "for achieved integration",
            )
        )
    write_json(output / "construction_recipes.json", recipes)
    write_csv(pd.DataFrame(edges).drop_duplicates(), output / "panel_edges.csv")
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
        (eligibility.study.astype(str).str.zfill(2) == "05")
        & (eligibility.population == "primary")
    ][["film_id", "cohort_group"]].sort_values("film_id")
    assert len(eligible) == 157
    study_eligibility = eligibility[
        (eligibility.study.astype(str).str.zfill(2) == "05")
        & (eligibility.population == "primary")
    ].sort_values("film_id")
    write_csv(study_eligibility, output / "eligibility.csv")
    spec = importlib.util.spec_from_file_location(
        "af3a", ROOT / "prompt-labels/build.py"
    )
    features = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(features)

    @cache
    def lexical(text):
        return tuple(
            int(bool(text and features.REGEX[k].search(text)))
            for k in ["edit", "preservation", "reference", "lens"]
        )

    with connect(data) as db:
        db.register("eligible", eligible)
        db.execute((HERE / "measures.sql").read_text())
        jobs = db.sql("SELECT * FROM image_jobs ORDER BY film_id,generation_id").df()
        jobs = jobs.astype(object).where(pd.notna(jobs), None)
        derived, mask_inventory = [], []
        controls = Counter()
        for row in jobs.to_dict("records"):
            ps, obj = parse(row["parameters_json"])
            route = classify(
                obj, row["image_inputs"], row["other_inputs"], row["model_identifier"]
            )
            values = dict(
                jobs=1,
                prompt_nonempty=int(row["prompt"] not in (None, "")),
                prompt_empty=int(row["prompt"] == ""),
                prompt_unavailable=int(row["prompt"] is None),
                input_jobs=int(row["image_inputs"] > 0),
                multi_input_jobs=int(row["image_inputs"] > 1),
                other_input_jobs=int(row["other_inputs"] > 0),
                staged_jobs=int(row["image_parents"] > 0),
                convergent_jobs=int(row["image_parents"] > 1),
                used_by_video=int(row["video_consumer"]),
            )
            values.update({"route_" + k: int(route == k) for k in ROUTES})
            values.update(
                {
                    "json_" + k: int(ps == k)
                    for k in ["object", "invalid", "unavailable", "empty", "nonobject"]
                }
            )
            values.update(
                {
                    k + "_jobs": v
                    for k, v in zip(
                        ["edit", "preservation", "reference", "lens"],
                        lexical(row["prompt"]),
                        strict=True,
                    )
                }
            )
            values["short_edit_jobs"] = int(
                bool(row["prompt"])
                and len(row["prompt"]) <= 300
                and values["edit_jobs"]
            )
            values["edit_with_input"] = values["edit_jobs"] * values["input_jobs"]
            values["edit_staged"] = values["edit_jobs"] * values["staged_jobs"]
            values["edit_without_parent"] = values["edit_jobs"] * (
                1 - values["staged_jobs"]
            )
            values["inpaint_false"] = int(
                obj is not None and obj.get("is_inpaint") is False
            )
            values["inpaint_true"] = int(
                obj is not None and obj.get("is_inpaint") is True
            )
            values["mask_layer_active"] = int(any(x[3] for x in mechanisms(obj)))
            derived.append(values)
            for k in CONTROLS:
                kind, raw = state(obj, k)
                controls[(row["film_id"], row["model_identifier"], k, kind, raw)] += 1
            for path, kind, raw, active in mechanisms(obj):
                mask_inventory.append(
                    dict(
                        film_id=row["film_id"],
                        generation_id=row["generation_id"],
                        parameter_path=path,
                        state=kind,
                        raw_json=raw,
                        active=active,
                    )
                )
        numeric = list(derived[0])
        jobs = pd.concat([jobs.reset_index(drop=True), pd.DataFrame(derived)], axis=1)
        film = jobs.groupby("film_id", sort=True)[numeric].sum().reset_index()
        film = eligible.merge(film, on="film_id", how="left")
        film[numeric] = film[numeric].fillna(0).astype(int)
        taxonomy = read_csv(upstream / "taxonomy.csv")
        film = film.merge(
            taxonomy[["film_id", "title", "record_orientation", "scale"]], on="film_id"
        )
        film["unusual_project"] = film.film_id.isin(
            read_csv(upstream / "unusual_projects.csv").film_id
        )
        baseline = read_csv(upstream / "film_metrics.csv")
        assert (
            film.merge(baseline[["film_id", "image_jobs"]], on="film_id").eval(
                "jobs==image_jobs"
            )
        ).all()
        assert film.jobs.sum() == 92058
        ratios = [
            (
                n,
                "prompt_nonempty"
                if n
                in [
                    "edit_jobs",
                    "preservation_jobs",
                    "reference_jobs",
                    "lens_jobs",
                    "short_edit_jobs",
                ]
                else "edit_jobs"
                if n in ["edit_with_input", "edit_staged", "edit_without_parent"]
                else "jobs",
            )
            for n in numeric
            if n != "jobs"
        ]
        film = film[film.jobs > 0].copy()
        assert len(film) == int(study_eligibility.production_eligible.sum()) == 155
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
            jobs["route"] = jobs.apply(
                lambda r: next(k for k in ROUTES if r["route_" + k]), axis=1
            )
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
        control_frame = pd.DataFrame(
            [
                dict(
                    zip(
                        [
                            "film_id",
                            "model_identifier",
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
        control_frame = (
            control_frame.groupby(
                ["film_id", "model_identifier", "parameter", "state", "raw_json"],
                dropna=False,
                sort=True,
            )
            .jobs.sum()
            .reset_index()
        )
        totals = (
            jobs.groupby(["film_id", "model_identifier"], sort=True)
            .size()
            .rename("image_job_denominator")
            .reset_index()
        )
        control_frame = control_frame.merge(totals, on=["film_id", "model_identifier"])
        for parameter in CONTROLS:
            write_csv(
                control_frame[control_frame.parameter == parameter],
                output / ("controls_" + parameter + ".csv"),
            )
        write_csv(
            pd.DataFrame(
                mask_inventory,
                columns=[
                    "film_id",
                    "generation_id",
                    "parameter_path",
                    "state",
                    "raw_json",
                    "active",
                ],
            ),
            output / "mask_layer_paths.csv",
        )
        ledger = []
        for row in film.to_dict("records"):
            ledger.append(
                evidence(
                    row["film_id"],
                    row["film_id"] + "/generation:* WHERE generation_type=image; "
                    "compound asset IDs from measures.sql",
                    "generations; assets; asset_usages; "
                    "studies/05-image/measures.sql; build.py",
                    json.dumps({k: int(row[k]) for k in numeric}, sort_keys=True),
                    f"{row['jobs']} image jobs; "
                    f"{row['prompt_nonempty']} nonempty primary texts; "
                    f"{row['edit_jobs']} edit-word fields; "
                    "per-metric denominator_name in summaries",
                )
            )
        write_csv(pd.DataFrame(ledger), output / "metric_evidence.csv")
        panel_outputs(db, output)
        instructions = []
        for reading in json.loads((HERE / "readings.json").read_text()):
            fid, gid = reading["film_id"], reading["generation_id"]
            text, source = db.execute(
                "SELECT prompt,prompt_source_path FROM j "
                "WHERE film_id=? AND generation_id=?",
                [fid, gid],
            ).fetchone()
            assert reading["span"] in text and reading["span"] != text
            instructions.append(
                dict(
                    **evidence(
                        fid,
                        fid + "/generation:" + gid,
                        "generations.prompt; " + source,
                        reading["span"],
                        "One named property span; six purposive spans in two tasks",
                        "inferred",
                    ),
                    property=reading["property"],
                    generation_id=gid,
                    instruction_observed=True,
                    media_outcome="unobservable",
                )
            )
        write_csv(pd.DataFrame(instructions), output / "integration_instructions.csv")
        # AF3a counts matches per exact text, whereas this study counts jobs
        # with any match. Check the original grain before reporting job shares.
        checks = []
        baseline_features = read_csv(
            ROOT / "prompt-labels/outputs/features_by_stratum.csv"
        )
        baseline_features = baseline_features[
            (baseline_features.population == "primary")
            & (baseline_features.generation_type == "image")
            & (baseline_features.text_role == "primary")
        ].set_index("film_id")
        for fid, group in jobs[jobs.prompt_nonempty == 1].groupby("film_id"):
            texts = group.prompt.drop_duplicates()
            values = dict(distinct_texts_denominator=len(texts))
            for feature in ["edit", "preservation", "reference", "lens"]:
                values[feature + "_matches_sum"] = sum(
                    len(features.REGEX[feature].findall(t)) for t in texts
                )
            values["short_edit_proxy_sum"] = sum(
                len(t) <= 300 and bool(features.REGEX["edit"].search(t)) for t in texts
            )
            for key, value in values.items():
                assert value == baseline_features.loc[fid, key], (fid, key)
            checks.append(dict(film_id=fid, **values, af3a_equal=True))
        assert len(checks) == 155
        write_csv(pd.DataFrame(checks), output / "structural_check.csv")
        audit = []
        panel = read_csv(upstream / "panel.csv")
        for fid in sorted(panel.film_id):
            group = jobs[jobs.film_id == fid]
            for name in ["edit", "preservation", "reference", "lens"]:
                for positive in [False, True]:
                    selected = group[
                        (group.prompt_nonempty == 1)
                        & (group[name + "_jobs"] == int(positive))
                    ]
                    if selected.empty:
                        continue
                    r = selected.iloc[0]
                    text = r.prompt
                    found = features.REGEX[name].search(text)
                    span = found.group() if found else None
                    if span == text:
                        span = None
                    audit.append(
                        dict(
                            **evidence(
                                fid,
                                fid + "/generation:" + r.generation_id,
                                "generations.prompt; " + r.prompt_source_path,
                                span,
                                f"{len(selected)} eligible fields in this panel film; "
                                "first sorted key",
                            ),
                            feature=name,
                            positive=positive,
                            text_sha256=hashlib.sha256(text.encode()).hexdigest(),
                            match_start=found.start() if found else None,
                            match_end=found.end() if found else None,
                        )
                    )
        write_csv(pd.DataFrame(audit), output / "structural_audit.csv")
    sources = [
        HERE / "build.py",
        HERE / "measures.sql",
        HERE / "taxonomy.json",
        HERE / "contracts.json",
        HERE / "readings.json",
        ROOT / "PROGRAMME.md",
        ROOT / "prompt-labels/build.py",
        ROOT / "prompt-labels/outputs/features_by_stratum.csv",
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
        for n in ["CODEBOOK.md", "DICTIONARY.md", "PROVENANCE.md"]
    ]
    sources += [
        ROOT / "studies" / n / "README.md"
        for n in ["02-planning", "03-elements", "10-organisation"]
    ]
    sources += [ROOT / "case-files/README.md", ROOT / "prompt-labels/README.md"]
    sources += sorted((ROOT / "case-files").glob("*/codes.csv")) + sorted(
        (ROOT / "case-files").glob("*/CASE.md")
    )
    write_json(
        output / "reproduction.json",
        dict(
            study="05",
            release="data-2026-10-20",
            source_manifest_sha256=digest(data / "SHA256SUMS"),
            inputs={p.relative_to(ROOT).as_posix(): digest(p) for p in sources},
            outputs={
                p.name: digest(p)
                for p in sorted(output.iterdir())
                if p.name != "reproduction.json"
            },
            primary_films=157,
            eligible_films=155,
            image_films=int((film.jobs > 0).sum()),
            image_jobs=int(film.jobs.sum()),
        ),
    )
    for path in output.iterdir():
        assert path.stat().st_size < 1_000_000, (path.name, path.stat().st_size)
    print(
        f"Built {len(list(output.iterdir()))} outputs; 155 eligible films; "
        f"{film.jobs.sum()} image jobs"
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
        expected = {p.name: p.read_bytes() for p in (HERE / "outputs").iterdir()}
        actual = {p.name: p.read_bytes() for p in args.output.iterdir()}
        assert actual == expected, "Reproduction differs from committed outputs"
        print("Every output reproduced byte for byte")


if __name__ == "__main__":
    main()
