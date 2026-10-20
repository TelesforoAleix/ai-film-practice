"""Four-film manual calibration assignments with executable excerpt checks.

Assignments were made by reading selected published records. Reproduction checks
evidence; it does not relabel text semantically or produce full case files.
"""

import json

import pandas as pd
from codebook_source import CODES

CASES = [
    {
        "film_id": "d305f6e5-b906-49a1-a0c6-75ef7f653ad8",
        "title": "Don't Poison Ivy",
        "brief_needle": "Character sheets are built in Nano Banana Pro.",
        "samples": [
            ("I", "bec13f8c-2125-4ff5-8a5b-c7e21511721b", "remove the plant"),
            ("V", "407acee9-0585-468c-a544-db7a19ef8003", "6 shots. Total 30 seconds"),
            ("X", "e9f6ff29-3cd8-405e-bf85-9a037ed891d4", "2 shots. Total 6.0 seconds"),
        ],
    },
    {
        "film_id": "655325cc-46d9-4b0b-b03d-d177defa4b3f",
        "title": "The Kiss",
        "brief_needle": "Schedule, locations, crew, and logistics.",
        "samples": [
            ("I", "597c7874-1596-41cf-ab54-2e305bd057bc", "Remove the"),
            ("V", "64c88da0-2a24-49bc-bdc7-8ece091c1dff", "SCENE CONTEXT"),
            ("X", "14948b7d-5d8f-4783-987d-b87f68bc0a3d", "Remove the braces"),
        ],
    },
    {
        "film_id": "6659c520-c88e-4ac7-a2c9-f28d8a40c954",
        "title": "Fallen Leaves",
        "brief_needle": "naturalistic hand movement and lighting.",
        "samples": [
            (
                "I",
                "7188a902-290f-4b44-9d53-b3b34f1ee492",
                "Location reference sheet, color, on a neutral background.",
            ),
            (
                "V",
                "62e05ad7-79d3-4424-860c-feaa9673f2d9",
                "NOT merely tilting or pivoting in place.",
            ),
            ("X", "aa8a5c34-415f-4371-aca9-777f976cfed5", "regenerating in 1080p"),
        ],
    },
    {
        "film_id": "94181633-a40a-4143-ace0-7d6bc3699d59",
        "title": "Cosmic tracks",
        "brief_needle": "external editing, compositing, and sound design in post",
        "samples": [
            (
                "I",
                "ca2f3df7-3e74-45c4-8f03-e9ab929e6ac7",
                "do not change anything else",
            ),
            (
                "V",
                "6cb74c0d-1051-4a84-834a-872d10fe4c55",
                "the exact first frame and is authoritative over every other reference",
            ),
            (
                "X",
                "537b6c88-6c46-4f1f-a012-62826257e04c",
                "Character reference sheet, three views (front, 3/4, profile)",
            ),
            (
                "Y",
                "f4d75507-12be-4602-9349-1d0bdeecd460",
                "Controls geometry, materials, layout and practical lights only.",
            ),
        ],
    },
]

# Every film receives every code. Unestablished values are explicitly unknown
# within this calibration sample, never absent from the film.
COMMON = {
    "02.1": ("visual_intention", "B"),
    "02.2": ("character|setting", "V"),
    "02.3": ("multi_shot_instruction", "V"),
    "03.1": ("disclosed_category", "R"),
    "03.4": ("prose|parameter|reference_metadata", "V"),
    "04.1": ("primary", "I"),
    "04.2": ("exclusion|preservation", "I"),
    "04.3": ("media_input|reference_element", "I"),
    "04.4": ("text_explicit|media_attached_content_unknown", "I"),
    "04.5": ("short_edit", "I"),
    "05.1": ("local_edit_request", "I"),
    "05.3": ("preservation", "I"),
    "06.2": ("camera_action", "V"),
    "06.4": ("generate_audio_true", "V"),
    "06.5": ("appearance", "V"),
    "06.6": ("duration|aspect_ratio|resolution", "V"),
    "07.1": ("generation_input|producer_output", "I"),
    "08.1": ("local_edit", "I"),
    "08.2": ("literal_identifier", "I"),
    "09.1": ("shared_inputs", "G"),
    "09.2": ("local_correction_request", "I"),
    "07.4": ("previous_output_chaining", "E"),
    "08.3": ("edge_supported", "E"),
    "08.4": ("cross_model", "E"),
    "09.4": ("reused_for_further_work", "E"),
    "10.1": ("mixed", "F"),
    "10.2": ("single_recorded_author", "M"),
    "10.3": ("recorded_event_window", "M"),
    "10.5": ("jobs_per_declared_minute", "M"),
}
OVERRIDES = {
    "Don't Poison Ivy": {
        "02.1": ("deliverable", "B"),
        "03.1": ("character|prop", "R"),
        "02.6": ("substantive", "B"),
        "03.3": ("generic_reference_sheet", "B"),
        "03.2": ("unknown", "R"),
        "04.2": ("action|exclusion", "I"),
        "04.3": ("media_input", "I"),
        "05.3": ("unknown", "I"),
        "05.4": ("inpaint_false", "I"),
        "06.1": ("multi_shot_request", "X"),
        "06.3": ("timed_event|shot_boundary", "X"),
        "06.5": ("motion", "X"),
        "08.1": ("reference_sheet|environment|animation", "B"),
        "10.2": ("multiple_recorded_authors", "M"),
    },
    "The Kiss": {
        "03.1": ("character|prop|location", "R"),
        "02.1": ("unknown_template_section", "B"),
        "02.6": ("mixed", "B"),
        "04.2": ("action", "I"),
        "04.3": ("media_input", "I"),
        "05.3": ("unknown", "I"),
        "05.4": ("unspecified", "I"),
        "06.1": ("video_guided", "X"),
        "06.5": ("unknown", "V"),
        "06.7": ("video_edit_request", "X"),
        "08.5": ("folder_label_only", "F"),
    },
    "Fallen Leaves": {
        "03.1": ("character", "R"),
        "02.3": ("unknown", "F"),
        "02.6": ("substantive", "B"),
        "03.3": ("multi_angle", "I"),
        "04.2": ("composition|environment", "I"),
        "04.3": ("unknown_no_inputs_exported_for_this_job", "I"),
        "04.4": ("text_explicit", "I"),
        "04.5": ("full_description", "I"),
        "05.1": ("fresh_candidate", "I"),
        "05.3": ("placement", "I"),
        "05.4": ("unspecified", "I"),
        "05.5": ("reference_sheet", "I"),
        "06.1": ("video_guided", "X"),
        "06.5": ("appearance", "X"),
        "06.7": ("video_edit_request", "X"),
        "07.1": ("generation_input|producer_output", "X"),
        "08.1": ("reference_sheet", "I"),
        "10.1": ("flat_proxy", "F"),
    },
    "Cosmic tracks": {
        "03.1": ("prop|character", "R"),
        "02.1": ("unknown_external_tool_statement", "B"),
        "02.3": ("multi_shot_instruction", "V"),
        "02.6": ("substantive", "B"),
        "03.2": ("identity_constraint", "I"),
        "03.3": ("multi_angle", "X"),
        "03.6": ("creator_declared", "V"),
        "04.2": ("preservation", "I"),
        "04.3": ("reference_element", "I"),
        "04.5": ("short_edit|reference_tokens", "I"),
        "05.2": ("multiple_inputs", "I"),
        "05.4": ("inpaint_false", "I"),
        "05.5": ("reference_sheet", "X"),
        "06.1": ("multi_shot_request", "V"),
        "06.5": ("layout|appearance", "V"),
        "08.5": ("creator_stated_external", "B"),
    },
}


def calibrate(db, out):
    rows, evidence = [], []
    for case in CASES:
        fid, title = case["film_id"], case["title"]
        scope = "supplemental" if title == "Cosmic tracks" else "primary"
        prefix = title.replace(" ", "_").replace("'", "")
        base = {
            "study": "01",
            "film_id": fid,
            "population": scope,
            "competing_explanation": (
                "Instructions and metadata show intended operations; "
                "achieved results and omitted work are unobservable"
            ),
            "denominator": (
                "One film; selected calibration records only, not exhaustive "
                "case-file coding"
            ),
            "confidence_rationale": (
                "Direct published field excerpt checked byte-for-byte; "
                "semantic interpretation is single-coder and provisional"
            ),
        }
        brief = db.execute(
            "SELECT project_brief FROM films WHERE film_id=?", [fid]
        ).fetchone()[0]
        assert case["brief_needle"] in brief
        evidence.append(
            {
                **base,
                "evidence_id": prefix + ":B",
                "entity_ids": fid,
                "source_path": "films.project_brief",
                "excerpt": case["brief_needle"],
                "evidence_label": "creator-stated",
            }
        )
        folders = db.execute(
            (
                "SELECT folder_id,folder_name FROM folders WHERE film_id=? "
                "ORDER BY folder_path"
            ),
            [fid],
        ).fetchall()
        evidence.append(
            {
                **base,
                "evidence_id": prefix + ":F",
                "entity_ids": "|".join(r[0] for r in folders),
                "source_path": "folders.folder_name",
                "excerpt": "; ".join(r[1] for r in folders),
                "evidence_label": "observed",
            }
        )
        refs = db.execute(
            (
                "SELECT reference_element_id,name,category FROM "
                "reference_elements WHERE film_id=? ORDER BY "
                "reference_element_id LIMIT 3"
            ),
            [fid],
        ).fetchall()
        evidence.append(
            {
                **base,
                "evidence_id": prefix + ":R",
                "entity_ids": "|".join(r[0] for r in refs),
                "source_path": "reference_elements.name/category",
                "excerpt": "; ".join(f"{r[1]}: {r[2]}" for r in refs),
                "evidence_label": "observed",
            }
        )
        metric = db.execute(
            (
                "SELECT generations,models,authors,cast(first_event AS "
                "VARCHAR),cast(last_event AS "
                "VARCHAR),declared_duration_seconds FROM profile WHERE "
                "film_id=?"
            ),
            [fid],
        ).fetchone()
        evidence.append(
            {
                **base,
                "evidence_id": prefix + ":M",
                "entity_ids": "All compound generation keys for film",
                "source_path": "profile.sql: jobs/profile",
                "excerpt": str(metric),
                "evidence_label": "observed",
                "denominator": f"One film; {metric[0]} recorded jobs; "
                f"{metric[5]} declared seconds",
            }
        )
        for key, gid, excerpt in case["samples"]:
            prompt, model, params, source = db.execute(
                (
                    "SELECT prompt,model_identifier,parameters_json,source_record"
                    "_file FROM generations WHERE film_id=? AND generation_id=?"
                ),
                [fid, gid],
            ).fetchone()
            assert excerpt in prompt and excerpt != prompt
            obj = json.loads(params)
            controls = {
                k: obj[k]
                for k in [
                    "duration",
                    "aspect_ratio",
                    "resolution",
                    "multi_shots",
                    "generate_audio",
                    "is_inpaint",
                    "model",
                ]
                if k in obj
            }
            usages = db.execute(
                (
                    "SELECT asset_id,asset_role,parameter_path,reference_element_"
                    "id FROM asset_usages WHERE film_id=? AND generation_id=? "
                    "ORDER BY asset_role,asset_id,parameter_path"
                ),
                [fid, gid],
            ).fetchall()
            evidence.append(
                {
                    **base,
                    "evidence_id": prefix + ":" + key,
                    "entity_ids": gid
                    + "; "
                    + "; ".join("|".join(str(v) for v in r) for r in usages),
                    "source_path": (
                        "generations.prompt/parameters_json/model_identifier; "
                        "asset_usages.parameter_path; "
                    )
                    + source,
                    "excerpt": excerpt
                    + (
                        " [additional reviewed spans] "
                        + prompt[:550]
                        + " [...] "
                        + prompt[-220:]
                        if len(prompt) > 800
                        else ""
                    )
                    + " [controls] "
                    + json.dumps(controls, ensure_ascii=False, sort_keys=True)
                    + " [literal model] "
                    + model,
                    "evidence_label": "observed",
                }
            )
        shared_asset, members = db.execute(
            (
                "SELECT asset_id,list(DISTINCT generation_id ORDER BY "
                "generation_id) FROM asset_usages WHERE film_id=? AND "
                "asset_role<>'output' GROUP BY 1 HAVING count(DISTINCT "
                "generation_id)>1 ORDER BY 1 LIMIT 1"
            ),
            [fid],
        ).fetchone()
        evidence.append(
            {
                **base,
                "evidence_id": prefix + ":G",
                "entity_ids": shared_asset + "; " + "|".join(members),
                "source_path": (
                    "asset_usages.asset_id/generation_id, excluding output roles"
                ),
                "excerpt": "Shared input asset; distinct consumer count="
                + str(len(members)),
                "denominator": f"{len(members)} consumers of one recorded input; "
                "iteration-family candidate, "
                "not established semantic equivalence",
                "evidence_label": "observed",
            }
        )
        edge = db.execute(
            (
                "SELECT a.asset_id,producer.generation_id,producer.model_iden"
                "tifier,\n consumer.generation_id,consumer.model_identifier,u."
                "asset_role,u.parameter_path\n FROM asset_usages u JOIN "
                "assets a ON u.film_id=a.film_id AND u.asset_id=a.asset_id\n "
                "JOIN generations producer ON a.film_id=producer.film_id AND "
                "a.generation_id=producer.generation_id\n JOIN generations "
                "consumer ON u.film_id=consumer.film_id AND "
                "u.generation_id=consumer.generation_id\n WHERE u.film_id=? "
                "AND u.asset_role<>'output'\n AND "
                "producer.model_identifier<>consumer.model_identifier\n ORDER "
                "BY a.asset_id,consumer.generation_id,u.parameter_path LIMIT "
                "1"
            ),
            [fid],
        ).fetchone()
        assert edge is not None
        evidence.append(
            {
                **base,
                "evidence_id": prefix + ":E",
                "entity_ids": "|".join(str(v) for v in edge),
                "source_path": (
                    "assets.generation_id -> generations; "
                    "asset_usages.asset_id/parameter_path -> generations"
                ),
                "excerpt": f"Explicit producer {edge[2]} -> consumer {edge[4]}, "
                f"role {edge[5]}, path {edge[6]}",
                "denominator": (
                    "One explicit same-film producer/consumer edge; "
                    "variants not collapsed"
                ),
                "evidence_label": "observed",
            }
        )
        assignments = COMMON | OVERRIDES[title]
        for code, study, *_ in CODES:
            value, key = assignments.get(code, ("unknown_in_calibration_sample", "M"))
            unknown = value.startswith("unknown")
            rows.append(
                {
                    "film_id": fid,
                    "title": title,
                    "population": scope,
                    "code_id": code,
                    "later_study": study,
                    "value": value,
                    "status": "unknown" if unknown else "coded",
                    "evidence_id": prefix + ":" + key,
                    "scope_note": (
                        "Not established in inspected sample; "
                        "do not infer film-wide absence"
                    )
                    if unknown
                    else (
                        "Manual sample coding; requested versus "
                        "observed output kept separate"
                    ),
                    "codebook_version": "1.0",
                }
            )
    indexed = {r["evidence_id"]: r for r in evidence}
    for row in rows:
        source = indexed[row["evidence_id"]]
        row.update(
            {
                k: source[k]
                for k in [
                    "study",
                    "entity_ids",
                    "source_path",
                    "excerpt",
                    "evidence_label",
                    "competing_explanation",
                    "denominator",
                    "confidence_rationale",
                ]
            }
        )
        if row["status"] == "unknown":
            row["evidence_label"] = "inferred"
    pd.DataFrame(rows).to_csv(out / "calibration.csv", index=False)
    pd.DataFrame(evidence).to_csv(out / "calibration_evidence.csv", index=False)
