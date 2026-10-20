"""Study 02: deterministic structural measures and evidence-scoped panel maps."""

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
    "Published histories omit external/private work and may include unrelated work; "
    "lexical matches can be quoted, negated, boilerplate or multilingual misses. "
    "Instructions, attachments and labels do not establish execution or approval."
)
CONFIDENCE = (
    "Exact compound-key count under a deterministic structural rule; no semantic "
    "accuracy estimate, independent-coder agreement or causal interpretation."
)
TEMPLATES = (
    "Short project description goes here.",
    "Why this project exists.",
    "Story, message, and audience.",
    "References, mood, color palette, and creative direction.",
    "Schedule, locations, crew, and logistics.",
    "Current progress, blockers, and next steps.",
    "Script, moodboard, storyboard, schedule, and assets.",
    "Key decisions, updates, and project history.",
)
HEADINGS = re.compile(
    r"(?m)(?:^[ \t]*[✨🎭🎨🎬🚀🔗📝]?[ \t]*(?:#{1,6}\s*)?"
    r"(Context|Narrative|Visuals|Production|Status|Resources|Notes)\b[: \t]*|"
    r"[✨🎭🎨🎬🚀🔗📝][ \t]*"
    r"(Context|Narrative|Visuals|Production|Status|Resources|Notes)[: \t]*)",
    re.I,
)
FOLDER_SCENE = re.compile(r"(?i)\b(?:(?:scenes?|shots?|act\s*\d+)\b|s\d{2}\s*:)")
FIELDS = (
    "objective",
    "constraint",
    "visual_intention",
    "deliverable",
    "character",
    "setting",
    "shot",
)
# Same-property correspondences, not proof that a prompt was derived from a brief.
CORRESPONDENCES = {
    "birthdays": ("constraint", "1970s university lecture hall"),
    "detour": ("objective", "controls Ryu’s exact identity, face, body proportions"),
    "fallen-leaves": ("visual_intention", "Naturalistic available light"),
    "the-last-transmission": ("constraint", "a single practical source"),
    "the-staff": ("constraint", "near-black grain, dull copper collars"),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_feature_module():
    spec = importlib.util.spec_from_file_location(
        "af3a_features", ROOT / "prompt-labels/build.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_csv(path):
    return pd.read_csv(path, keep_default_na=False, na_values=[NULL])


def write_csv(frame, path):
    frame.to_csv(
        path, index=False, na_rep=NULL, float_format="%.9f", lineterminator="\n"
    )


def write_json(path, obj):
    path.write_text(
        json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    )


def brief_sections(text):
    """Detect literal placeholders; leave other prose unclassified."""
    if text is None:
        return []
    headings = list(HEADINGS.finditer(text))
    regions = [("preamble", 0, headings[0].start() if headings else len(text))]
    regions += [
        (
            (m[1] or m[2]).lower(),
            m.end(),
            headings[i + 1].start() if i + 1 < len(headings) else len(text),
        )
        for i, m in enumerate(headings)
    ]
    result = []
    for index, (heading, start, end) in enumerate(regions):
        content = text[start:end]
        hits = [t for t in TEMPLATES if t in content]
        remainder = content
        for t in hits:
            remainder = remainder.replace(t, "")
        remainder = remainder.strip()
        state = (
            "empty"
            if not content.strip()
            else "template_only"
            if hits and not remainder
            else "mixed_candidate"
            if hits
            else "nonplaceholder_unclassified"
        )
        result.append(
            dict(
                section_index=index,
                heading=heading,
                start=start,
                end=end,
                characters=len(content),
                sha256=hashlib.sha256(content.encode()).hexdigest(),
                state=state,
                template_matches=len(hits),
                excerpt=" | ".join(hits) or None,
            )
        )
    return result


def controls(raw):
    if raw is None:
        return "unavailable"
    if raw == "":
        return "empty_document"
    try:
        obj = json.loads(raw)
    except (ValueError, TypeError):
        return "invalid_json"
    if not isinstance(obj, dict) or "multi_shots" not in obj:
        return "absent"
    value = obj["multi_shots"]
    if value is True:
        return "true"
    if value is False:
        return "false"
    return "null" if value is None else "other_value"


def provenance(
    fid, entity, source, excerpt, denominator, label="observed", confidence=CONFIDENCE
):
    return dict(
        study="02",
        film_id=fid,
        entity_ids=entity,
        source_path=source,
        excerpt=excerpt,
        evidence_label=label,
        competing_explanation=ALTERNATIVE,
        denominator=denominator,
        confidence_rationale=confidence,
    )


def aggregate(frame, dimensions):
    rows = []
    groups = [("all", "primary", frame)]
    for d in dimensions:
        groups.extend(
            (d, None if pd.isna(v) else str(v), g)
            for v, g in frame.groupby(d, dropna=False, sort=True)
        )
    for dimension, value, group in groups:
        for n, d in [
            ("multi_shot_jobs", "prompt_nonempty"),
            ("sectioned_jobs", "prompt_nonempty"),
            ("reference_token_jobs", "prompt_nonempty"),
            ("multi_true", "jobs"),
            ("multi_false_with_text", "multi_shot_jobs"),
            ("scene_label_folders", "folders"),
        ]:
            if d not in group:
                continue
            valid = group[group[d] > 0]
            shares = valid[n] / valid[d]
            numerator, denominator = int(valid[n].sum()), int(valid[d].sum())
            rows.append(
                dict(
                    dimension=dimension,
                    value=value,
                    metric=n,
                    eligible_films=len(group),
                    measured_films=len(valid),
                    film_ids=json.dumps(sorted(valid.film_id)),
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


def panel_outputs(db, panel, cases, briefs, output):
    readings = json.loads((HERE / "readings.json").read_text())
    fields, maps, correspondences = [], [], []
    for path in sorted((ROOT / "case-files").glob("*/codes.csv")):
        slug = path.parent.name
        rows = cases[cases.case_source == path.relative_to(ROOT).as_posix()]
        fid = rows.iloc[0].film_id
        b = briefs[fid]
        by_code = {r["code_id"]: r for r in rows.to_dict("records")}
        for field in FIELDS:
            span = readings.get(slug, {}).get(field)
            # These are document labels, not completed entity/shot specifications.
            label_only = slug == "random-access-memories" and field in {
                "character",
                "setting",
                "shot",
            }
            if span:
                assert span in b and len(span) < len(b), (slug, field)
            state = "label_only" if label_only else "extracted" if span else "unknown"
            fields.append(
                dict(
                    slug=slug,
                    field=field,
                    state=state,
                    **provenance(
                        fid,
                        f"{fid}/brief:project_brief",
                        "films.project_brief",
                        span,
                        "One field category / one panel brief; 16 panel films",
                        "creator-stated" if span else "observed",
                        "Single-coder technical-prose extraction, source span checked; "
                        "unknown means not established, never semantic absence. "
                        "Narrative synopsis and unvisited links excluded.",
                    ),
                )
            )
        task_code = by_code["02.4"]
        task_ids = re.findall(r"/generation:([^; ]+)", task_code["entity_ids"])
        links = []
        for gid in task_ids:
            job = db.execute(
                "SELECT "
                "prompt,prompt_source_path,model_identifier,generation_type"
                " FROM jobs WHERE film_id=? AND generation_id=?",
                [fid, gid],
            ).fetchone()
            assert job is not None
            uses = db.execute(
                "SELECT asset_id,producer,asset_role,parameter_path,referen"
                "ce_element_id FROM usage_edges WHERE film_id=? AND "
                "consumer=? ORDER BY asset_id,asset_role,parameter_path",
                [fid, gid],
            ).fetchall()
            for aid, producer, role, parameter_path, ref in uses:
                links.append(
                    dict(
                        relation="task_attachment",
                        generation_id=gid,
                        asset_id=aid,
                        producer_generation_id=producer,
                        reference_element_id=ref,
                        parameter_path=parameter_path,
                        asset_role=role,
                        model_identifier=job[2],
                        generation_type=job[3],
                        evidence_id=task_code["evidence_id"],
                        **provenance(
                            fid,
                            f"{fid}/generation:{gid}; {fid}/asset:{aid}",
                            "asset_usages; assets.generation_id; "
                            + task_code["case_source"],
                            f"{role} at {parameter_path}",
                            task_code["denominator"],
                            confidence=(
                                "High for exact attachment; role is limited to "
                                "the case instruction; unresolved producer "
                                "stays null."
                            ),
                        ),
                    )
                )
            if slug in CORRESPONDENCES:
                field, span = CORRESPONDENCES[slug]
                assert span in job[0] and len(span) < len(job[0])
                record = dict(
                    relation="brief_task_correspondence",
                    generation_id=gid,
                    brief_field=field,
                    brief_excerpt=readings[slug][field],
                    **provenance(
                        fid,
                        f"{fid}/brief:project_brief; {fid}/generation:{gid}",
                        "films.project_brief; generations.prompt; "
                        "prompt_source_path=" + job[1],
                        span,
                        "One selected correspondence / one panel film; not a "
                        "coverage rate",
                        "inferred",
                        "Moderate: same technical property in both spans; not proof"
                        " of derivation or implementation. Independent instructions"
                        " are an alternative.",
                    ),
                )
                correspondences.append(record)
                links.append(record)
        order = by_code["02.5"]
        # Preserve the exact explicitly traced dependency supporting local preparation.
        if order["status"] == "coded" and order["evidence_label"] == "inferred":
            edges = json.loads((path.parent / "traced-edges.json").read_text())["edges"]
            entities = set(
                re.findall(r"/(?:generation|asset):([^; ]+)", order["entity_ids"])
            )
            selected = [
                e
                for e in edges
                if e["producer"] in entities and e["consumer"] in entities
            ]
            assert selected, slug
            for e in selected:
                for u in e["usages"]:
                    assert (
                        db.execute(
                            "SELECT count(*) FROM usage_edges WHERE film_id=? AND "
                            "consumer=? AND producer=? AND asset_id=? AND asset_role=? "
                            "AND parameter_path=?",
                            [
                                fid,
                                e["consumer"],
                                e["producer"],
                                u["asset_id"],
                                u["asset_role"],
                                u["parameter_path"],
                            ],
                        ).fetchone()[0]
                        == 1
                    )
                links.append(
                    dict(
                        relation="local_preparation",
                        producer=e["producer"],
                        consumer=e["consumer"],
                        usages=e["usages"],
                        **{
                            k: order[k]
                            for k in [
                                "study",
                                "film_id",
                                "entity_ids",
                                "source_path",
                                "excerpt",
                                "evidence_label",
                                "competing_explanation",
                                "denominator",
                                "confidence_rationale",
                            ]
                        },
                    )
                )
        maps.append(
            dict(
                film_id=fid,
                slug=slug,
                title=by_code["02.1"]["title"],
                pair=panel.set_index("film_id").loc[fid, "pair"],
                brief_state="unavailable"
                if b is None
                else "empty"
                if b == ""
                else "available",
                declaration_evidence=by_code["02.1"]["evidence_id"],
                template_evidence=by_code["02.6"]["evidence_id"],
                planned_entities_evidence=by_code["02.2"]["evidence_id"],
                shot_plan_evidence=by_code["02.3"]["evidence_id"],
                task_binding_status=task_code["status"],
                task_binding_evidence=task_code["evidence_id"],
                brief_task_status="inferred_correspondence"
                if slug in CORRESPONDENCES
                else "unknown",
                brief_task_limit=(
                    "No documentary brief-node to task ID binding; local "
                    "plan/task and technical-property correspondences only. No "
                    "complete coverage or achieved result inferred."
                ),
                order_value=order["value"] if order["status"] == "coded" else None,
                order_label=order["evidence_label"],
                order_status=order["status"],
                order_evidence=order["evidence_id"],
                links=links,
            )
        )
    assert len(maps) == 16 and len(fields) == 112
    write_csv(pd.DataFrame(fields), output / "brief_fields.csv")
    write_csv(pd.DataFrame(correspondences), output / "brief_task_correspondences.csv")
    write_json(output / "panel_maps.json", maps)


def build(data, output):
    output.mkdir(parents=True, exist_ok=True)
    upstream = ROOT / "studies/01-corpus/outputs"
    eligibility = read_csv(upstream / "eligibility.csv")
    eligible = eligibility[
        (eligibility.study.astype(str).str.zfill(2) == "02")
        & (eligibility.population == "primary")
        & (eligibility.production_eligible.astype(str) == "True")
    ][["film_id", "cohort_group"]]
    assert len(eligible) == 157 and eligible.film_id.is_unique
    panel = read_csv(upstream / "panel.csv")
    taxonomy = read_csv(upstream / "taxonomy.csv")
    case_rows = []
    for path in sorted((ROOT / "case-files").glob("*/codes.csv")):
        for r in csv.DictReader(path.open()):
            if r["code_id"].startswith("02."):
                r["case_source"] = path.relative_to(ROOT).as_posix()
                case_rows.append(r)
    cases = pd.DataFrame(case_rows)
    assert len(cases) == 96 and set(cases.film_id) == set(panel.film_id)
    feature_module = load_feature_module()

    @cache
    def features(text):
        return {
            key + "_matches": sum(1 for _ in feature_module.REGEX[key].finditer(text))
            for key in ["multi_shot", "section", "reference"]
        }

    with connect(data) as db:
        db.register("eligible", eligible)
        db.execute((HERE / "measures.sql").read_text())
        assert (
            db.sql(
                "SELECT count(*) FROM generation_prompts p JOIN jobs j "
                "USING(film_id,generation_id) WHERE "
                "p.field_path=j.prompt_source_path AND p.text IS DISTINCT "
                "FROM j.prompt"
            ).fetchone()[0]
            == 0
        )
        jobs = (
            db.sql("SELECT * FROM jobs ORDER BY film_id,generation_id")
            .df()
            .astype(object)
            .where(lambda x: x.notna(), None)
        )
        jobs["prompt_nonempty"] = jobs.prompt.map(
            lambda t: t is not None and t != ""
        ).astype(int)
        jobs["prompt_empty"] = jobs.prompt.map(lambda t: t == "").astype(int)
        jobs["prompt_unavailable"] = jobs.prompt.isna().astype(int)
        for column, feature in [
            ("multi_shot_jobs", "multi_shot_matches"),
            ("sectioned_jobs", "section_matches"),
            ("reference_token_jobs", "reference_matches"),
        ]:
            jobs[column] = jobs.prompt.map(
                lambda t, f=feature: int(bool(t) and features(t)[f] > 0)
            )
        jobs["control_state"] = jobs.parameters_json.map(controls)
        for state in [
            "true",
            "false",
            "invalid_json",
            "absent",
            "unavailable",
            "empty_document",
            "null",
            "other_value",
        ]:
            jobs["multi_" + state] = (jobs.control_state == state).astype(int)
        jobs["multi_false_with_text"] = (
            (jobs.multi_shot_jobs == 1) & (jobs.multi_false == 1)
        ).astype(int)
        jobs["jobs"] = 1
        numeric = [
            "jobs",
            "prompt_nonempty",
            "prompt_empty",
            "prompt_unavailable",
            "multi_shot_jobs",
            "sectioned_jobs",
            "reference_token_jobs",
            "multi_false_with_text",
        ] + [
            "multi_" + s
            for s in [
                "true",
                "false",
                "invalid_json",
                "absent",
                "unavailable",
                "empty_document",
                "null",
                "other_value",
            ]
        ]
        film = (
            jobs.groupby("film_id", sort=True)[numeric]
            .sum()
            .reset_index()
            .merge(eligible, on="film_id")
        )
        film = film.merge(
            taxonomy[
                [
                    "film_id",
                    "record_orientation",
                    "scale",
                    "organisation_proxy",
                    "declared_duration_seconds",
                ]
            ],
            on="film_id",
        )
        briefs = dict(
            db.sql(
                "SELECT film_id,project_brief FROM films JOIN eligible USING(film_id)"
            ).fetchall()
        )
        section_rows, folder_rows = [], []
        for fid, text in sorted(briefs.items()):
            for r in brief_sections(text):
                section_rows.append(dict(film_id=fid, **r))
        sections = pd.DataFrame(section_rows)
        for fid, folder_id, name in db.sql(
            "SELECT film_id,folder_id,folder_name FROM folders JOIN "
            "eligible USING(film_id) ORDER BY film_id,folder_id"
        ).fetchall():
            folder_rows.append(
                dict(
                    film_id=fid,
                    folder_id=folder_id,
                    scene_label_match=int(bool(name and FOLDER_SCENE.search(name))),
                )
            )
        folders = pd.DataFrame(folder_rows)
        film["folders"] = film.film_id.map(folders.groupby("film_id").size())
        film["scene_label_folders"] = film.film_id.map(
            folders.groupby("film_id").scene_label_match.sum()
        )
        film["brief_state"] = film.film_id.map(
            lambda f: (
                "unavailable"
                if briefs[f] is None
                else "empty"
                if briefs[f] == ""
                else "nonempty"
            )
        )
        film["brief_template_matches"] = (
            film.film_id.map(sections.groupby("film_id").template_matches.sum())
            .fillna(0)
            .astype(int)
        )
        film.loc[film.brief_state == "unavailable", "brief_template_matches"] = None
        film["brief_sections"] = film.film_id.map(sections.groupby("film_id").size())
        film["empty_sections"] = film.film_id.map(
            sections[sections.state == "empty"].groupby("film_id").size()
        ).fillna(0)
        film.loc[film.brief_state == "unavailable", "empty_sections"] = None
        film["unusual_project"] = film.film_id.isin(
            read_csv(upstream / "unusual_projects.csv").film_id
        )
        # Full all-role structural re-count, checked against the merged AF3a output.
        fields = db.sql(
            "SELECT * FROM fields WHERE text IS NOT NULL AND text<>'' "
            "ORDER BY film_id,generation_id,field_path"
        ).df()
        structural = []
        for fid, group in fields.groupby("film_id", sort=True):
            distinct = list(dict.fromkeys(group.text))
            structural.append(
                dict(
                    film_id=fid,
                    distinct_texts_denominator=len(distinct),
                    multi_shot_matches_sum=sum(
                        features(t)["multi_shot_matches"] for t in distinct
                    ),
                    matched_texts=sum(
                        features(t)["multi_shot_matches"] > 0 for t in distinct
                    ),
                    shot_prompt_fields=int((group.text_role == "shot_prompt").sum()),
                )
            )
        structural = pd.DataFrame(structural)
        expected = read_csv(ROOT / "prompt-labels/outputs/features_by_film.csv")
        checked = structural.merge(expected, on="film_id", suffixes=("", "_af3a"))
        assert len(checked) == 157
        for c in ["distinct_texts_denominator", "multi_shot_matches_sum"]:
            assert (checked[c] == checked[c + "_af3a"]).all(), c
        film = film.merge(structural, on="film_id")
        panel_outputs(db, panel, cases, briefs, output)
        # A deterministic lexical audit: one positive and one negative per panel film.
        audits = []
        for fid in sorted(panel.film_id):
            for positive in [True, False]:
                part = jobs[
                    (jobs.film_id == fid)
                    & (jobs.prompt_nonempty == 1)
                    & (jobs.multi_shot_jobs == int(positive))
                ]
                if part.empty:
                    continue
                row = part.iloc[0]
                text = row.prompt
                match = feature_module.REGEX["multi_shot"].search(text)
                # Select a shorter exact span when a lexical match crosses CRLF.
                excerpt = match[0].splitlines()[0].rstrip() if match else None
                audits.append(
                    dict(
                        generation_id=row.generation_id,
                        lexical_positive=positive,
                        match_start=match.start() if match else None,
                        match_end=match.end() if match else None,
                        match_sha256=(
                            hashlib.sha256(match[0].encode()).hexdigest()
                            if match
                            else None
                        ),
                        **provenance(
                            fid,
                            f"{fid}/generation:{row.generation_id}",
                            "generations.prompt; prompt_source_path="
                            + (row.prompt_source_path or "unavailable"),
                            excerpt if excerpt != text else None,
                            f"First sorted polarity={positive} primary field / "
                            f"{len(part)} candidates in film",
                        ),
                    )
                )
        write_csv(pd.DataFrame(audits), output / "structural_audit.csv")
        for dimension in ["generation_type", "model_identifier"]:
            part = (
                jobs.groupby(["film_id", dimension], dropna=False, sort=True)[numeric]
                .sum()
                .reset_index()
                .merge(eligible, on="film_id")
            )
            write_csv(part, output / f"by_{dimension}.csv")
            groups = []
            for cohort, members in [
                ("all", part),
                *part.groupby("cohort_group", sort=True),
            ]:
                result = aggregate(members, [dimension])
                result = result[result.dimension == dimension]
                result["cohort_group"] = cohort
                groups.append(result)
            # Member sets are recoverable from the per-film dimension output.
            summary = pd.concat(groups).drop(columns="film_ids")
            write_csv(summary, output / f"summary_{dimension}.csv")
    baseline = read_csv(upstream / "film_metrics.csv")
    check = film.merge(baseline[["film_id", "generations"]], on="film_id")
    assert (check.jobs == check.generations).all() and (
        film.brief_state == "nonempty"
    ).sum() == 118
    write_csv(film, output / "film_metrics.csv")
    write_csv(
        aggregate(film, ["cohort_group", "record_orientation", "scale"]),
        output / "summaries.csv",
    )
    write_csv(sections, output / "brief_sections.csv")
    write_csv(cases, output / "case_evidence.csv")
    scene_handoff = cases[cases.code_id == "02.3"].copy()
    scene_handoff["scene_definition"] = (
        "An explicitly scoped planned setting/state grouping; a folder or scene "
        "word is only a label until its scope and membership are evidenced."
    )
    scene_handoff["shot_definition"] = (
        "An explicitly delimited requested view or temporal segment; one job can "
        "request several shots; no executed cut or final shot count inferred."
    )
    scene_handoff["membership_status"] = "unknown"
    scene_handoff["jobs_per_scene_denominator"] = None
    write_csv(scene_handoff, output / "scene_handoff.csv")
    ledgers = []
    for row in film.to_dict("records"):
        fid = row["film_id"]
        ledgers.append(
            provenance(
                fid,
                f"{fid}/generation,field,folder: all compound keys in named scopes",
                "build.py; measures.sql; generations; generation_prompts; "
                "folders; films.project_brief; Study 01 taxonomy",
                json.dumps(
                    {k: None if pd.isna(v) else v for k, v in row.items()},
                    sort_keys=True,
                    default=str,
                    allow_nan=False,
                ),
                f"{row['jobs']} jobs; "
                f"{row['prompt_nonempty']} nonempty primary fields; "
                f"{row['folders']} folders; "
                f"{row['distinct_texts_denominator']} film-distinct all-role texts; "
                "missing brief counts unavailable",
            )
        )
    write_csv(pd.DataFrame(ledgers), output / "metric_evidence.csv")
    inputs = [
        HERE / x for x in ["build.py", "measures.sql", "readings.json", "schemas.json"]
    ]
    inputs += [
        ROOT / "PROGRAMME.md",
        ROOT / "prompt-labels/build.py",
        ROOT / "prompt-labels/outputs/features_by_film.csv",
    ]
    inputs += [
        upstream / f"{x}.csv"
        for x in [
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
            if p.suffix in {".csv", ".json"} and p.name != "reproduction.json"
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
        parser.error("--check needs a separate output directory")
    manifest = build(args.data, args.output)
    if args.check:
        for name in [*manifest["outputs"], "reproduction.json"]:
            assert (args.output / name).read_bytes() == (
                HERE / "outputs" / name
            ).read_bytes(), name
    print(f"Study 02: 157 films, 16 panel maps, {len(manifest['outputs'])} outputs.")


if __name__ == "__main__":
    main()
