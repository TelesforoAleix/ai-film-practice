"""Batch-two single-coder assignments; assertions live in shared Case methods.

These are manual decisions on named units, not an automatic prompt classifier.
"""

import json


def assign_many(c, evidence, assignments):
    for code, value, note in assignments:
        c.assign(code, value, evidence, note)


def reference_kinds(c):
    refs = sorted(
        c.tables["reference_elements"], key=lambda r: r["reference_element_id"]
    )
    c.assign(
        "03.1",
        "character|location" + ("|prop" if c.slug == "detour" else ""),
        c.aggregate(
            "reference_elements.name/category",
            "; ".join(f"{r['name']}: {r['category']}" for r in refs),
            f"All {len(refs)} disclosed reference entities / one film; "
            "categories are metadata",
            "; ".join(c.key("reference", r["reference_element_id"]) for r in refs),
        ),
        "Character and environment metadata; location is an inferred mapping of "
        "environment. "
        "Names such as v1 or final do not establish version edges or approval.",
        label="inferred",
    )


def traced(c, producer, consumer):
    e = c.edge(producer, consumer)
    for code, value, note in [
        (
            "07.1",
            "producer_output|generation_input",
            "One explicit producer/input edge; exact asset ID.",
        ),
        (
            "07.4",
            "previous_output_chaining",
            "Observed downstream use; no continuity assessment.",
        ),
        (
            "08.3",
            "edge_supported",
            "Named pair has different literal models; edge supports a transition.",
        ),
        (
            "08.4",
            "staged|cross_model",
            "One supported stage; no global routing or build-order inference.",
        ),
        (
            "09.4",
            "reused_for_further_work",
            "Further-work use only, not final acceptance.",
        ),
    ]:
        c.assign(code, value, e, note)


def family(c, members, equal=False):
    e = c.family(members)
    c.assign(
        "09.1",
        "shared_inputs",
        e,
        "Named candidate family; common exact input IDs, no semantic-equivalence "
        "claim.",
    )
    c.assign(
        "07.2",
        "branch|shared_ancestor",
        e,
        "Scoped shared-input motif; deduplicate input IDs per consumer, retain "
        "raw/min under one entity; no hub ranking.",
    )
    if equal:
        c.assign(
            "09.2",
            "rerun",
            e,
            "Equal primary requests and shared inputs support a candidate rerun "
            "interpretation; order and intention unconfirmed.",
            label="inferred",
        )
    return e


def detour(c):
    c.common("scene|entity|stage|mixed")
    reference_kinds(c)
    brief = c.brief("Character and location sheets established the visual rules")
    c.assign(
        "02.1",
        "constraint",
        c.brief(
            "Production on this seven-minute race focused on maintaining continuity"
            " across geography, scale and fast-moving action."
        ),
        "Production section describes reference preparation to maintain technical "
        "consistency; creator account only.",
        label="creator-stated",
    )
    c.assign(
        "02.5",
        "reference_first",
        brief,
        "Creator-stated preparation order; not independently reconstructed for the "
        "whole production.",
        label="creator-stated",
    )
    c.assign(
        "02.6",
        "substantive",
        brief,
        "Production section contains specific sheets, frame reuse and tools, not "
        "template-only prose.",
        label="creator-stated",
    )
    sheet = c.job(
        "006dcc36",
        "Costume reference plate, three views of the same figure",
        "first the full length front view,",
        "second the full length reverse view, third a tight head shot",
        controls=("is_inpaint",),
        inputs=True,
    )
    assign_many(
        c,
        sheet,
        [
            (
                "02.2",
                "character",
                "Explicit same-figure identity across a requested costume sheet.",
            ),
            (
                "03.3",
                "multi_angle",
                "Requested front/reverse/headshot package; output not inspected.",
            ),
            (
                "05.5",
                "reference_sheet",
                "Declared costume-reference purpose, not verified package fulfilment.",
            ),
        ],
    )
    image = c.job(
        "00406410",
        "Keep the composition of <<<image_1>>> exactly as it is",
        "each block is 10–12 metres tall",
        "All chevrons point LEFT.",
        controls=("is_inpaint",),
        inputs=True,
    )
    assign_many(
        c,
        image,
        [
            (
                "03.4",
                "prose",
                "Composition and scale specified in prose; attached media contents "
                "unknown.",
            ),
            (
                "04.2",
                "composition|spatial|preservation",
                "Named composition lock, scale and orientation spans.",
            ),
            (
                "04.3",
                "media_input|reference_element",
                "Actual input image and disclosed reference-element usage.",
            ),
            (
                "04.4",
                "text_explicit|metadata_explicit|media_attached_content_unknown",
                "Text carries scale/orientation; metadata carries reference "
                "name/category; media not viewed.",
            ),
            (
                "04.5",
                "sectioned|reference_tokens",
                "Sectioned edit with explicit reference bindings.",
            ),
            (
                "05.1",
                "reference_guided|local_edit_request|multi_input",
                "Add chevrons while preserving composition; two actual input IDs.",
            ),
            (
                "05.2",
                "multiple_inputs",
                "One image and one reference asset condition the request; no layers"
                " inferred.",
            ),
            (
                "05.3",
                "placement|scale|preservation",
                "Explicit placement/scale request and composition lock, attached to"
                " inputs.",
            ),
            (
                "05.4",
                "inpaint_false",
                "Literal false retained; edit language is not a mask.",
            ),
            (
                "08.1",
                "composition|local_edit",
                "seedream_v5_pro has an explicit reference-guided composition edit "
                "request.",
            ),
        ],
    )
    edit = c.job(
        "011fbb97",
        "The only change is a small mark of tomato ketchup on one side of his face",
        "EVERYTHING ELSE STAYS UNTOUCHED",
        inputs=True,
    )
    c.assign(
        "03.2",
        "identity_constraint|variant_instruction",
        edit,
        "Same sheet and identity requested with one named changed property.",
    )
    edge = c.edge("006dcc36", "011fbb97")
    edge["excerpt"] += (
        " [changed property excerpt] The only change is a small mark of tomato "
        "ketchup on one side of his face"
    )
    edge["source_path"] += "; generations.prompt"
    c.assign(
        "03.5",
        "inferred_version",
        edge,
        "Explicit input derivative plus named property delta supports an inferred "
        "sheet version; no version ID or approval event.",
        label="inferred",
    )
    canonical = c.job(
        "05637129",
        "is the MASTER SOURCE IMAGE and strict composition lock.",
        "<<<image_2>>> is a COLOR, LIGHTING, TEXTURE, AND CINEMATIC MOOD REFERENCE "
        "ONLY.",
        inputs=True,
    )
    c.assign(
        "03.6",
        "creator_declared",
        canonical,
        "Task-scoped authority statement. Master-source token is missing in the "
        "text, so its asset binding is unresolved; no global canonical claim.",
    )
    video = c.job(
        "057fd821",
        "three connected 2-second shots",
        "controls Ryu’s exact identity, face, body proportions",
        "Both match their references exactly.",
        "0:00–0:02",
        controls=(
            "duration",
            "aspect_ratio",
            "resolution",
            "multi_shots",
            "generate_audio",
            "draft",
            "extension_mode",
        ),
        inputs=True,
    )
    assign_many(
        c,
        video,
        [
            (
                "02.3",
                "shot_list|multi_shot_instruction",
                "Three timed shot instructions in one prompt, independent of "
                "multi_shots=false.",
            ),
            (
                "02.4",
                "explicit_link",
                "Named Ryu identity token is explicitly bound to the task and an "
                "exported reference usage.",
            ),
            (
                "06.1",
                "image_guided|multi_shot_request",
                "Reference-image usages plus explicit three-shot text; false "
                "control retained.",
            ),
            (
                "06.3",
                "timed_event|shot_boundary",
                "Three requested two-second segments, not observed timing.",
            ),
            (
                "06.4",
                "generate_audio_true",
                "Enabled control, not proof of usable sound.",
            ),
            (
                "06.5",
                "identity|appearance",
                "Explicit exact-match identity and wardrobe invariants scoped to "
                "the task.",
            ),
            (
                "06.6",
                "duration|aspect_ratio|resolution|draft|extension",
                "Literal model controls, including false and null, not normalized "
                "across models.",
            ),
        ],
    )
    c.assign(
        "06.2",
        "camera_action",
        c.job(
            "093e4529",
            "A low wide tracking camera travels ahead and slightly front-left",
        ),
        "Explicit camera-motion instruction, not achieved motion.",
    )
    c.assign(
        "06.7",
        "video_edit_request",
        c.job(
            "0106d708",
            "女性身份与面部外观的唯一权威参考",
            controls=("model",),
            inputs=True,
        ),
        "Video-edit control and explicit face-identity correction constraint; "
        "actual correction unverified.",
    )
    traced(c, "006dcc36", "011fbb97")
    e = family(c, ["093e4529", "c430fa55"])
    c.assign(
        "09.2",
        "local_correction_request",
        edit,
        "One explicit local-change request; no failed prior output inferred.",
    )
    # The shared-input candidate pair differs in a named reference binding.
    a, b = c.find("093e4529"), c.find("c430fa55")
    old, new = (
        "36137ad2-4960-44bc-9896-3c88a953afc8",
        "2e3a1baf-2838-48a0-9ea1-f76e695724c1",
    )
    assert old in a["prompt"] and new in b["prompt"]
    for g, ref in [(a, old), (b, new)]:
        assert any(
            u["generation_id"] == g["generation_id"]
            and u["reference_element_id"] == ref
            for u in c.tables["asset_usages"]
        )
    e["excerpt"] += f" [reference binding comparison] {old} versus {new}"
    e["source_path"] += "; asset_usages.reference_element_id"
    e["entity_ids"] += "; " + "; ".join(c.key("reference", r) for r in [old, new])
    c.assign(
        "09.3",
        "input_replacement",
        e,
        "Named shared-input candidate pair changes kart reference binding; "
        "comparison direction only, no established revision order.",
    )
    c.descendants("6354dd61")
    c.assign(
        "08.5",
        "job_observed|creator_stated_external",
        c.job("c4625d5e", controls=("chain_preset_id",), inputs=True),
        "Observed cinematic_video_editor job; external finishing is separately "
        "creator-stated in Production, not reconstructed.",
    )
    # Retain the external statement in the same evidence record.
    b = c.brief(
        "Photoshop for quick refinement, Premiere for editing, and Suno for music."
    )
    c.rows["08.5"]["excerpt"] += " [creator-stated Production excerpt] " + b["excerpt"]
    c.rows["08.5"]["source_path"] += "; films.project_brief"
    c.rows["08.5"]["denominator"] += "; one Production brief section"
    c.rows["08.5"]["scope_note"] += (
        " Mixed evidence: job observed; named tools creator-stated."
    )


def fallen(c):
    c.common("flat_proxy")
    reference_kinds(c)
    brief = c.brief("naturalistic hand movement and lighting.")
    c.assign(
        "02.1",
        "visual_intention",
        brief,
        "Creator-stated technical intention; no achieved-media assessment.",
        label="creator-stated",
    )
    c.assign(
        "02.6",
        "substantive",
        brief,
        "Specific Tone/Visual Style and Production prose; no template-only section "
        "used as a plan.",
        label="creator-stated",
    )
    sheet = c.job(
        "7188a902",
        "Location reference sheet, color, on a neutral background.",
        "plus two supporting angles of the same location",
        inputs=True,
    )
    assign_many(
        c,
        sheet,
        [
            ("02.2", "setting", "Persistent location requested across several views."),
            (
                "03.3",
                "multi_angle|location_board",
                "Requested location package, not a verified output.",
            ),
            ("03.4", "prose", "Package and geography consistency specified in prose."),
            (
                "04.5",
                "full_description",
                "Long-form descriptive reference-sheet request.",
            ),
            ("05.5", "reference_sheet", "Explicit reference-sheet purpose."),
            (
                "08.1",
                "reference_sheet|environment",
                "gpt_image_2 carries an explicit location-sheet request.",
            ),
        ],
    )
    image = c.job(
        "330764cc",
        "kneels low directly in the snow",
        controls=("is_inpaint",),
        inputs=True,
    )
    assign_many(
        c,
        image,
        [
            (
                "04.2",
                "spatial|composition",
                "Explicit figure placement in one still request.",
            ),
            (
                "04.3",
                "media_input|reference_element",
                "Actual image and two reference usages; media not viewed.",
            ),
            (
                "04.4",
                "text_explicit|media_attached_content_unknown",
                "Placement in prose; contents of inputs unknown.",
            ),
            (
                "05.1",
                "reference_guided|multi_input",
                "Image job conditioned on three exact input IDs.",
            ),
            (
                "05.2",
                "multiple_inputs|staged_construction",
                "Actual conditioning; dc2e911c producer output is an image input to"
                " this job.",
            ),
            ("05.3", "placement", "Named figure placement, no result assessment."),
            (
                "05.4",
                "unspecified",
                "is_inpaint unavailable; no disclosed mask/layer mechanism "
                "established for this image request.",
            ),
        ],
    )
    c.edge("dc2e911c", "330764cc")
    video = c.job(
        "62e05ad7",
        "NOT merely tilting or pivoting in place.",
        "CONTINUITY REFERENCE",
        controls=(
            "duration",
            "aspect_ratio",
            "resolution",
            "generate_audio",
            "multi_shots",
            "draft",
            "extension_mode",
        ),
        inputs=True,
    )
    assign_many(
        c,
        video,
        [
            (
                "02.4",
                "explicit_link",
                "Continuity-reference token and input video bind predecessor "
                "context to this task.",
            ),
            (
                "06.1",
                "image_guided|video_guided",
                "Actual image/video/reference inputs; no media-derived route assumed.",
            ),
            (
                "06.2",
                "camera_action",
                "Physical crane movement requested, distinguished from a tilt.",
            ),
            (
                "06.4",
                "generate_audio_true",
                "Literal true control, not a standalone audio job.",
            ),
            (
                "06.6",
                "duration|aspect_ratio|resolution|draft|extension",
                "Literal control values including false and null.",
            ),
        ],
    )
    c.assign(
        "02.3",
        "shot_list",
        c.job(
            "0b35d954",
            "FIRST — CLOSE-UP:",
            "THEN — FAST WHIP TO A MEDIUM-WIDE:",
            inputs=True,
        ),
        "Ordered framing plan in one request; a whip links the views. "
        "No executed cut or active multi-shot control inferred.",
    )
    timed = c.job("0bc2480b", "0–3s:", inputs=True)
    c.assign(
        "06.3",
        "timed_event",
        timed,
        "Written timing within a requested continuous take; not measured clip timing.",
    )
    revise = c.job(
        "aa8a5c34",
        "regenerating in 1080p",
        "no changes",
        controls=("model", "resolution"),
        inputs=True,
    )
    assign_many(
        c,
        revise,
        [
            (
                "03.2",
                "identity_constraint",
                "No-changes instruction on linked video, scoped to regeneration.",
            ),
            (
                "06.5",
                "appearance|other",
                "Everything except requested resolution held invariant.",
            ),
            (
                "06.7",
                "video_edit_request",
                "Explicit regeneration request and video_edit mode, not proof of "
                "better output.",
            ),
            (
                "09.2",
                "local_correction_request",
                "Resolution-only request, no failure inference.",
            ),
        ],
    )
    conflict = c.job(
        "4e4c57a8",
        "Stationary film camera shot.",
        "The camera drifts slowly across the scene",
    )
    c.assign(
        "04.6",
        "possible_conflict",
        conflict,
        "Stationary and drift instructions coexist; stationary may describe an "
        "observational style rather than zero motion.",
        label="inferred",
        alternative=(
            "Stationary may describe observational style, or the drift "
            "clause may be a local amendment; intended scope unresolved."
        ),
    )
    traced(c, "1cba062c", "023fadcd")
    c.edge("023fadcd", "aa8a5c34")
    family(c, ["023fadcd", "45e66125"], equal=True)
    # Keep the linked resolution revision beside the shared-input family.
    c.assign(
        "09.2",
        "local_correction_request",
        revise,
        "Explicit resolution-only regeneration; shared-input family itself does not"
        " establish iteration intent.",
    )
    c.descendants("023fadcd")


def lost(c):
    c.common("scene|entity|asset_type|mixed")
    reference_kinds(c)
    brief = c.brief(
        "Crafts at home, took pics for reference, made assets, built out beginning "
        "and end and bridged to middle."
    )
    c.assign(
        "02.5",
        "reference_first",
        brief,
        "Creator-stated reference/asset preparation order, not event-derived build "
        "order.",
        label="creator-stated",
    )
    c.assign(
        "02.6",
        "substantive",
        brief,
        "Resources and Production have specific technical prose, not generic "
        "placeholders.",
        label="creator-stated",
    )
    c.assign(
        "02.1",
        "deliverable",
        c.brief("3 minutes Final Cut complete"),
        "Creator-stated format and status; catalogue duration remains a separate "
        "denominator.",
        label="creator-stated",
    )
    image = c.job(
        "02e53a47",
        "make the character sheet for this character exactly the same",
        "gray neutral tone background",
        "black beaty eyes",
        controls=("is_inpaint",),
        inputs=True,
    )
    assign_many(
        c,
        image,
        [
            (
                "02.2",
                "character",
                "Same character explicitly maintained across a reference sheet.",
            ),
            (
                "03.2",
                "identity_constraint",
                "Explicit same-character instruction, not verified preservation.",
            ),
            (
                "03.3",
                "generic_reference_sheet",
                "Generic sheet request does not specify multiple angles.",
            ),
            (
                "03.4",
                "prose",
                "Background/eye properties in prose; attached content unknown.",
            ),
            (
                "04.2",
                "identity|preservation",
                "Same-character wording; no semantic labeling at scale.",
            ),
            (
                "04.3",
                "media_input",
                "Three actual input_asset rows; no reference-element usage in this "
                "one job.",
            ),
            (
                "04.4",
                "text_explicit|media_attached_content_unknown",
                "Text properties visible, media uninspected.",
            ),
            ("04.5", "short_edit", "Short reference-guided sheet alteration request."),
            (
                "05.1",
                "reference_guided|local_edit_request|multi_input",
                "Three attached inputs and an explicit same-character style change "
                "request.",
            ),
            (
                "05.3",
                "preservation",
                "Explicit identity preservation on attached inputs.",
            ),
            (
                "05.4",
                "unspecified",
                "No nonempty mask/layer or inpaint boolean disclosed for this request.",
            ),
            ("05.5", "reference_sheet", "Requested purpose only."),
            (
                "08.1",
                "reference_sheet|local_edit",
                "seedream_v4_5 carries a sheet transformation request.",
            ),
        ],
    )
    converge = c.job(
        "044604ad",
        "put all of these characters in the town",
        "zoomed out wide angle",
        inputs=True,
    )
    c.assign(
        "05.2",
        "multiple_inputs|staged_construction",
        converge,
        "Twelve input assets and one reference input condition one image; explicit "
        "02e53a47 producer edge, not layer compositing.",
    )
    c.edge("02e53a47", "044604ad")
    video = c.job(
        "08d2776c",
        "ACT 8:",
        "Shot 1 :",
        "Shot 2:",
        "shouting and waving his arms",
        controls=(
            "duration",
            "aspect_ratio",
            "resolution",
            "multi_shots",
            "generate_audio",
            "draft",
            "extension_mode",
        ),
        inputs=True,
    )
    assign_many(
        c,
        video,
        [
            (
                "02.3",
                "shot_list|multi_shot_instruction",
                "Seven requested shot labels while multi_shots=false.",
            ),
            (
                "02.4",
                "explicit_link",
                "Curtis/Nally named in shot instructions with ID tokens and "
                "reference usage rows.",
            ),
            (
                "06.1",
                "image_guided|multi_shot_request",
                "Actual images/reference inputs plus shot-list wording.",
            ),
            ("06.2", "subject_action", "Explicit subject-action instruction."),
            (
                "06.3",
                "ordered_event|shot_boundary",
                "Ordered shots, not measured cuts.",
            ),
            (
                "06.4",
                "generate_audio_true",
                "Literal enabled flag, no verified audio result.",
            ),
            (
                "06.6",
                "duration|aspect_ratio|resolution|draft|extension",
                "Raw controls retained, false/null distinct from missing.",
            ),
        ],
    )
    revise = c.job(
        "09925f84",
        "make everything the same but fix the sounds and color grading",
        "one continuous shot with no cuts",
        inputs=True,
    )
    assign_many(
        c,
        revise,
        [
            (
                "06.5",
                "other",
                "Keep-everything instruction with explicit sound/grade/shot "
                "exceptions.",
            ),
            (
                "06.7",
                "video_edit_request",
                "Video-guided changed-shot request despite raw model=default; "
                "intent and mechanism separate.",
            ),
            (
                "09.2",
                "local_correction_request",
                "Observed correction request, not assessed defect or successful "
                "correction.",
            ),
        ],
    )
    traced(c, "66411159", "09925f84")
    delta = c.edge("4e117e2d", "09925f84")
    for prefix, span in [
        ("4e117e2d", "make everything the same"),
        ("09925f84", "one continuous shot with no cuts"),
    ]:
        e = c.job(prefix, span)
        delta["excerpt"] += " [named member excerpt] " + prefix + ": " + e["excerpt"]
    delta["source_path"] += "; generations.prompt"
    c.assign(
        "09.3",
        "text_addition|preservation",
        delta,
        "Linked producer/consumer requests add an explicit continuous-shot "
        "constraint. Edge supports derivation, not successful correction.",
    )
    family(c, ["044604ad", "0aa04ddc"])
    c.assign(
        "08.5",
        "creator_stated_external",
        c.brief("Edited using capcut."),
        "External editor named by creator; no corresponding observed editor job "
        "asserted.",
        label="creator-stated",
    )
    c.descendants("4e117e2d")


def transmission(c):
    c.common("flat_proxy")
    brief = c.brief("Order of work: assets, then stress tests, then the film")
    c.assign(
        "02.5",
        "entity_first|reference_first",
        brief,
        "Creator-stated order only; exported video history does not independently "
        "reconstruct those assets.",
        label="creator-stated",
    )
    c.assign(
        "02.6",
        "substantive",
        brief,
        "Production gives a specific preparation/testing sequence, not "
        "template-only text.",
        label="creator-stated",
    )
    c.assign(
        "02.1",
        "constraint",
        c.brief("One motivated light source per frame"),
        "Technical lighting constraint as creator-stated intention; no output "
        "judgement.",
        label="creator-stated",
    )
    plan = c.job(
        "0a5dad36",
        '"shot_id":"TLT_S02_clock_v2"',
        '"reference_plates":["tlt_deck"]',
        '"reference_image_ids":["9264c44d-ad74-4ddc-91fc-4490b55a5b18"]',
        inputs=True,
    )
    assign_many(
        c,
        plan,
        [
            (
                "02.2",
                "setting",
                "Persistent named deck plate in explicit instructions.",
            ),
            (
                "02.3",
                "scene",
                "Explicit shot identifier and scene/world specification in JSON prose.",
            ),
            (
                "02.4",
                "explicit_link",
                "Named plate plus literal reference_image_ids binds shot task to an"
                " attached asset; producer unresolved.",
            ),
            (
                "03.1",
                "location",
                "Named deck plate in prose, despite zero disclosed reference elements.",
            ),
            (
                "03.4",
                "prose",
                "JSON-shaped primary prose stores plate/shot properties; not "
                "equivalent to reference-library metadata.",
            ),
            ("04.3", "media_input", "Actual input image matches ID in primary text."),
            (
                "04.4",
                "text_explicit|media_attached_content_unknown",
                "Textual plate binding visible, attached properties unobservable.",
            ),
            ("06.1", "image_guided", "Actual input_image role on this video task."),
        ],
    )
    g = c.find("0a5dad36")
    assert isinstance(json.loads(g["prompt"]), dict)
    temporal = c.job(
        "0a5dad36",
        '"time":"0-5s"',
        '"time":"5-9s"',
        "turn it once, twice, slower",
        "The fingers slow and stop mid-turn.",
        '"camera":"locked frame on the dial and hands"',
        "no voice, no music",
        controls=(
            "duration",
            "aspect_ratio",
            "resolution",
            "multi_shots",
            "generate_audio",
            "draft",
            "extension_mode",
        ),
        inputs=True,
    )
    assign_many(
        c,
        temporal,
        [
            (
                "04.2",
                "timing|camera_motion|exclusion",
                "Explicit timed camera-hold/audio exclusions in JSON text.",
            ),
            (
                "04.5",
                "structured_json",
                "Whole primary prompt parses as a JSON object; it remains "
                "instruction text.",
            ),
            (
                "06.2",
                "subject_action",
                "Timed knob-turn and stop actions; not achieved movement.",
            ),
            (
                "06.3",
                "timed_event|ordered_event",
                "Timed stages within a requested continuous take, not multiple cuts.",
            ),
            (
                "06.4",
                "audio_exclusion|generate_audio_true",
                "No voice/music and enabled audio flag coexist; effects may still "
                "be generated.",
            ),
            (
                "06.6",
                "duration|aspect_ratio|resolution|draft|extension",
                "Literal controls including false and null retained.",
            ),
            (
                "08.1",
                "animation",
                "seedance_2_5 video job with timed action instructions.",
            ),
        ],
    )
    edit = c.job(
        "083272c6",
        "Edit: inside the CRT screen ONLY",
        "EVERYTHING outside the screen glass stays exactly unchanged",
        controls=("model",),
        inputs=True,
    )
    assign_many(
        c,
        edit,
        [
            (
                "03.2",
                "identity_constraint",
                "Explicit preservation of person outside the edited screen region; "
                "no measured preservation.",
            ),
            (
                "06.5",
                "appearance|motion",
                "Preserve person, movements and surrounding scene outside screen.",
            ),
            (
                "06.7",
                "video_edit_request",
                "Explicit local screen-replacement request plus video_edit mode; no"
                " mask inferred.",
            ),
            (
                "09.2",
                "local_correction_request",
                "One requested correction does not establish a previous failure.",
            ),
        ],
    )
    package = c.job(
        "2056af94",
        '"shot_id":"CHAR_TLT_orlov"',
        "Full profile facing frame-left",
        "The turn completes to full frontal",
    )
    c.assign(
        "03.3",
        "multi_angle",
        package,
        "Multi-angle turn requested as a video reference task; not a still sheet or"
        " verified package.",
    )
    for code in ["05.1", "05.2", "05.3", "05.4", "05.5"]:
        c.assign(
            code,
            r"\N",
            c.aggregate(
                "generations.generation_type",
                "[exact distribution] video=66; image=0",
                "All 66 exported jobs; zero image jobs",
            ),
            "Image-operation code not applicable to the exported video-only job "
            "history; creator-stated sheets do not supply observed image jobs.",
            status="not_applicable",
        )
    c.assign(
        "07.1",
        "generation_input|external_or_unresolved",
        edit,
        "Typed video input is observed; searching all film assets/usages finds no "
        "recorded producer job.",
    )
    graph = c.reading["graph"]
    assert graph["explicit_distinct_producer_consumer_asset_role_path_edges"] == 0
    c.rows["07.1"]["source_path"] += "; assets.generation_id; profile.py:profile"
    c.rows["07.1"]["excerpt"] += " [whole-export producer join] resolved edges=0"
    c.rows["07.1"]["denominator"] += (
        "; all 106 film assets and 155 usages searched for producer resolution"
    )
    shared = family(c, ["1338707f", "feb2cb01"])
    c.assign(
        "07.4",
        "shared_reference",
        shared,
        "Two exact image inputs shared by named consumers; "
        "unresolved producers remain unresolved.",
    )
    c.assign(
        "08.4",
        "branching",
        shared,
        "Bounded input-to-two-consumer branch; "
        "does not reconstruct upstream preparation or a scheduler.",
    )
    c.assign(
        "08.3",
        r"\N",
        c.aggregate(
            "generations.model_identifier",
            "[distinct literal models] seedance_2_5",
            "All 66 jobs, one literal model",
        ),
        "Cross-model transition not applicable within this one-model export; "
        "external tools remain unobserved.",
        status="not_applicable",
    )
    c.assign(
        "08.5",
        "creator_stated_external",
        c.brief("The scan lines on the transmission picture are laid in post"),
        "Creator reports post work; no named tool or observed finishing job inferred.",
        label="creator-stated",
    )


def finalise(c):
    """Make batch-two uncertainty explicit without altering prior batch artifacts."""
    for row in c.rows.values():
        if row["status"] == "unknown":
            row["evidence_label"] = "inferred"
    if c.slug == "detour":
        texts = [
            r
            for r in c.tables["generation_prompts"]
            if r["field_path"] in {"params.enhanced_prompt", "params.source_prompt"}
        ]
        assert len(texts) == 3
        r = next(r for r in texts if r["field_path"] == "params.enhanced_prompt")
        assert "Video edit." in r["text"]
        e = c.job(r["generation_id"])
        e["source_path"] += "; generation_prompts.field_path/text"
        e["excerpt"] += " [nested field] params.enhanced_prompt [excerpt] Video edit."
        e["denominator"] = (
            "Three nested enhanced/source text fields across all 7,871 exported "
            "text rows; primary fields crosswalked separately"
        )
        c.assign(
            "04.1",
            "primary|other_text",
            e,
            "Primary is crosswalked in common(); enhanced/source text retained as "
            "other_text by path. prompt_language fields are metadata, not "
            "independent instructions. Field name does not establish who rewrote "
            "it.",
        )
