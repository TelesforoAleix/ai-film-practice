"""Batch-three manual assignments on published technical records.

Values are fixed reading decisions, never keyword classifications. Shared Case
methods assert excerpts and edges on the frozen release during reproduction.
"""

from batch2 import assign_many, family, traced


def combine(*evidence):
    """Keep each named source, compound key and denominator in a combined row."""
    return {
        key: " [evidence boundary] ".join(e[key] for e in evidence)
        for key in ("entity_ids", "source_path", "excerpt", "denominator")
    }


def references(c, values):
    refs = sorted(
        c.tables["reference_elements"], key=lambda r: r["reference_element_id"]
    )
    c.assign(
        "03.1",
        values,
        c.aggregate(
            "reference_elements.name/category",
            "; ".join(f"{r['name']}: {r['category']}" for r in refs),
            f"All {len(refs)} disclosed reference records / one film",
            "; ".join(c.key("reference", r["reference_element_id"]) for r in refs),
        ),
        "Literal categories retained; environment mapped to location, auto labels "
        "are weak evidence. Names alone do not establish identities or versions.",
        label="inferred",
    )


def reference_first(c, producer, consumer):
    c.assign(
        "02.5",
        "reference_first",
        c.edge(producer, consumer),
        "Named reference preparation output conditions a later task. This is a "
        "local dependency sequence, not a reconstruction of project build order.",
        label="inferred",
    )


def finish(c, prefix):
    c.assign(
        "08.5",
        "job_observed",
        c.job(prefix, controls=("duration",), inputs=True),
        "Recorded cinematic_video_editor operation with typed inputs; unavailable "
        "primary text is not empty. No final timeline, acceptance or achieved "
        "finishing quality inferred.",
    )


def harmony(c):
    c.common("scene|entity|stage|mixed")
    references(c, "character|location|prop")
    brief = c.brief("All voices, guitar and score are AI-generated.")
    c.assign(
        "02.1",
        "constraint",
        c.brief("Henri wears a watch always on his left wrist, and only there."),
        "Creator's declared identity/wardrobe constraint; no result verified.",
        label="creator-stated",
    )
    c.assign(
        "02.6",
        "substantive",
        brief,
        "Sound and identity sections contain specific technical declarations, "
        "rather than generic planning placeholders.",
        label="creator-stated",
    )
    image = c.job(
        "0205320f",
        "Use the attached 1 image as the only source of truth.",
        "Single change only, everything else pixel identical.",
        "with his pose, face, expression, glasses",
        "the armchair is the SAME WIDTH as the wooden armchair visible at frame-left",
        "The coffee table stays fully visible in front of it, never covered, "
        "never touched, never resized.",
        controls=("is_inpaint",),
        inputs=True,
    )
    assign_many(
        c,
        image,
        [
            (
                "03.2",
                "identity_constraint",
                "Preserve named figure and room while changing one seat.",
            ),
            (
                "03.4",
                "prose",
                "Seat size/placement are specified in prose; media properties unknown.",
            ),
            (
                "03.6",
                "creator_declared",
                "Source-of-truth declaration is scoped to this edit, not the library.",
            ),
            (
                "04.2",
                "preservation|spatial|composition",
                "Literal preservation, relative size and occlusion instructions.",
            ),
            (
                "04.3",
                "media_input|reference_element",
                "One input_image and three reference_image usages with IDs.",
            ),
            (
                "04.4",
                "text_explicit|metadata_explicit|media_attached_content_unknown",
                (
                    "Size is text-explicit, element names are metadata; attachment "
                    "content unknown."
                ),
            ),
            (
                "04.5",
                "sectioned|reference_tokens",
                "Single-change, dimension and placement sections with bound tokens.",
            ),
            (
                "05.1",
                "local_edit_request|reference_guided|multi_input",
                "Seat replacement request conditioned on actual inputs.",
            ),
            (
                "05.2",
                "multiple_inputs",
                "Four exact input assets; not four compositing layers.",
            ),
            (
                "05.3",
                "scale|placement|occlusion|preservation",
                "Named size, placement and coffee-table visibility requirements.",
            ),
            (
                "05.4",
                "unspecified",
                "No disclosed inpaint boolean, mask or layers in this named edit.",
            ),
            (
                "08.1",
                "local_edit|composition",
                "gpt_image_2 used for a seat replacement/composition instruction.",
            ),
        ],
    )
    c.assign(
        "03.3",
        "single_image",
        c.job(
            "128d88c2",
            "A reference photograph of one person seen from directly behind",
            inputs=True,
        ),
        "Requested single-view studio reference, not verified media content.",
    )
    c.assign(
        "05.5",
        "plate",
        c.job(
            "5fa376fc",
            "EMPTY LOCATION PLATE, no people, no characters, nobody in frame.",
        ),
        "Explicit empty-location plate request; no output judgement.",
    )
    video = c.job(
        "1674aeae",
        "modo DINÂMICO com 4 planos e cortes limpos entre eles.",
        "PLANO 1, ELE SE AJOELHA (0.0s-5.0s)",
        "PLANO 2, A CAIXINHA ABRE (5.0s-9.0s)",
        "Nenhum objeto, janela, porta, móvel, quadro, luminária ou parede novos "
        "podem ser inventados.",
        controls=(
            "duration",
            "aspect_ratio",
            "resolution",
            "multi_shots",
            "generate_audio",
            "draft",
        ),
        inputs=True,
    )
    assign_many(
        c,
        video,
        [
            (
                "02.2",
                "character|setting|prop",
                "Named Henri/Jade, room, costume and ring-box bindings in task.",
            ),
            (
                "02.3",
                "multi_shot_instruction|shot_list",
                "Four explicitly ordered shot sections, not inferred folder order.",
            ),
            (
                "02.4",
                "explicit_link",
                (
                    "ACTIVE REFERENCES contains IDs and scoped "
                    "character/wardrobe/room roles."
                ),
            ),
            (
                "06.1",
                "image_guided|multi_shot_request",
                "Actual image input and four-shot text; multi_shots=false retained.",
            ),
            (
                "06.2",
                "subject_action",
                "Named kneeling and box-opening actions; no achieved motion claim.",
            ),
            (
                "06.3",
                "shot_boundary|timed_event",
                "Two named time ranges within a four-shot request.",
            ),
            (
                "06.4",
                "generate_audio_true",
                "Literal enabled control, not proof of usable sound.",
            ),
            (
                "06.5",
                "layout",
                "No new scene objects, doors, windows or walls requested.",
            ),
            (
                "06.6",
                "duration|aspect_ratio|resolution|draft",
                "Literal model controls; false is retained, not absence.",
            ),
        ],
    )
    edit = c.job(
        "0a5cf741",
        "retire qualquer lágrima do rosto",
        inputs=True,
        controls=("model", "duration"),
    )
    c.assign(
        "06.7",
        "video_edit_request",
        edit,
        (
            "Explicit tear-removal request and video input; no defect or "
            "success assessment."
        ),
    )
    c.assign(
        "09.2",
        "local_correction_request",
        edit,
        "Requested local correction only; not a measured failure or retry.",
    )
    conflict = c.job(
        "16ffcdb7", "FORMAT: ~10 seconds", "6.5s-10.0s:", controls=("duration",)
    )
    c.assign(
        "04.6",
        "possible_conflict",
        conflict,
        "Text runs to 10 seconds while raw duration is 9. Approximation or "
        "scope mismatch may explain it; no model-confusion claim.",
        label="inferred",
    )
    reference_first(c, "52b4e96b", "1674aeae")
    traced(c, "001321d4", "eb1e92f8")
    finish(c, "eb1e92f8")
    family(c, ["03ca3f2b", "d9ce60c2"])
    c.descendants("16ffcdb7")


def birthdays(c):
    c.common("scene|entity|asset_type|mixed")
    references(c, "character|location|prop")
    brief = c.brief(
        "character aging appearance, wardrobe, production design, "
        "and technology kept period-accurate to each era"
    )
    c.assign(
        "02.1",
        "constraint",
        brief,
        "Declared period/age consistency objective; results unobservable.",
        label="creator-stated",
    )
    c.assign(
        "02.6",
        "substantive",
        brief,
        "Visuals and Production contain specific constraints and named tools.",
        label="creator-stated",
    )
    sheet = c.job(
        "071dab16", "front, side and back in 3 panels", "grey background.", inputs=True
    )
    assign_many(
        c,
        sheet,
        [
            (
                "03.3",
                "multi_angle",
                "Three-view package requested; output not inspected.",
            ),
            (
                "05.5",
                "reference_sheet",
                (
                    "Front/side/back studio package requested for reuse, not final "
                    "approval."
                ),
            ),
        ],
    )
    identity = c.job(
        "03fbd60d",
        "Generate a 60 years old version of this man.",
        "Slightly thinner hair, same facial hair, same iris color, "
        "same outfit, same background, same lighting.",
        inputs=True,
    )
    c.assign(
        "03.2",
        "identity_constraint|variant_instruction",
        identity,
        "Age/hair variation requested with explicit identity/property preservation.",
    )
    image = c.job(
        "372eae81",
        "Embross the logo from <<<image_2>>>",
        "on to the back of the electronic pad in <<<image_1>>>",
        "Front, Side, 3/4 and back for the pad on grey background in 3 panels",
        inputs=True,
    )
    assign_many(
        c,
        image,
        [
            (
                "03.4",
                "prose",
                "Logo placement and panel layout in prose; media contents unknown.",
            ),
            (
                "04.2",
                "action|spatial|composition",
                "Explicit embossing, placement and panel instructions.",
            ),
            (
                "04.3",
                "media_input",
                "Two actual input_image usages match the two numbered prompt inputs.",
            ),
            (
                "04.4",
                "text_explicit|media_attached_content_unknown",
                "Requested placement is text-explicit; logo image content unknown.",
            ),
            (
                "04.5",
                "short_edit|reference_tokens",
                "Short edit with explicit numbered tokens.",
            ),
            (
                "05.1",
                "local_edit_request|multi_input|reference_guided",
                "Linked tablet and logo inputs; no layer claim.",
            ),
            (
                "05.2",
                "multiple_inputs|staged_construction",
                (
                    "Tablet output 37f689e1 feeds this two-input edit; edge "
                    "recorded separately."
                ),
            ),
            (
                "05.4",
                "unspecified",
                "No literal inpaint, mask or layer mechanism disclosed in this edit.",
            ),
            (
                "08.1",
                "local_edit|composition",
                "seedream_v5_lite receives the tablet/logo placement instruction.",
            ),
        ],
    )
    c.assign(
        "05.3",
        "preservation",
        identity,
        (
            "Same outfit, background and lighting explicitly preserved in "
            "linked image request."
        ),
    )
    c.assign(
        "04.6",
        "possible_conflict",
        image,
        "Four named views versus three panels: a panel might combine views. "
        "Single-coder scope ambiguity, not an output defect.",
        label="inferred",
    )
    c.assign(
        "05.2",
        "multiple_inputs|staged_construction",
        combine(image, c.edge("37f689e1", "372eae81")),
        "Two actual inputs; one explicitly resolved tablet producer. "
        "Conditioning and staging, not compositing layers.",
    )
    e = combine(c.edge("37f689e1", "372eae81"), image)
    c.assign(
        "03.5",
        "inferred_version",
        e,
        "Exact tablet producer/input link and named logo/panel changes support "
        "a derivative reference version; not explicit version metadata or approval.",
        label="inferred",
    )
    video = c.job(
        "0014cfd5",
        "0:00-0:06",
        "0:10-0:15",
        "She moves down the aisle",
        "Continuity: Characters, props, environment identical across every cut.",
        "Audio: Environmental SFX only. No music. No subtitles.",
        controls=(
            "duration",
            "aspect_ratio",
            "resolution",
            "multi_shots",
            "generate_audio",
        ),
        inputs=True,
    )
    assign_many(
        c,
        video,
        [
            (
                "02.2",
                "character|setting",
                "Explicit character/wardrobe/location IDs in a task.",
            ),
            (
                "02.4",
                "explicit_link",
                "Planned characters and hall are bound to disclosed reference IDs.",
            ),
            (
                "06.1",
                "image_guided",
                "Typed reference_image usages, without inventing start/end roles.",
            ),
            (
                "06.2",
                "subject_action",
                "Walking and seating actions requested in timed sections.",
            ),
            (
                "06.3",
                "timed_event|ordered_event",
                "Three ordered time ranges; does not by itself require cuts.",
            ),
            (
                "06.4",
                "ambience|audio_exclusion|generate_audio_true",
                "Environmental SFX and no music coexist with enabled audio control.",
            ),
            (
                "06.5",
                "identity|appearance|layout",
                "Across-cut preservation of characters, props and environment.",
            ),
            (
                "06.6",
                "duration|aspect_ratio|resolution",
                "Raw controls retained separately from 8K text intent.",
            ),
        ],
    )
    folders = [r for r in c.tables["folders"] if r["folder_id"].startswith("5fdce85d")]
    f = folders[0]
    c.assign(
        "02.3",
        "scene",
        c.aggregate(
            "folders.folder_name",
            f["folder_name"],
            "One scene label / all 60 inspected folders",
            c.key("folder", f["folder_id"]),
        ),
        "Numbered scene folder label, not executed order.",
    )
    edit = c.job(
        "08590362",
        "Add a pin on each polaroid top edge",
        inputs=True,
        controls=("model", "duration"),
    )
    c.assign(
        "06.7",
        "video_edit_request",
        edit,
        (
            "Typed video input and pin-addition request; producer "
            "unresolved in reading sample."
        ),
    )
    c.assign(
        "09.2",
        "local_correction_request",
        edit,
        "Explicit correction intent; no measured defect or successful fix inferred.",
    )
    reference_first(c, "071dab16", "42dc451c")
    traced(c, "37f689e1", "372eae81")
    finish(c, "a58dc32f")
    family(c, ["1a664c20", "558a0737"])
    c.descendants("37f689e1")


def kagerou(c):
    c.common("scene|entity|asset_type|stage|mixed")
    references(c, "character")
    sheet = c.job(
        "0ca091f2",
        "Three views of the same character are arranged side by side.",
        "exactly one head and one face appear in the entire image",
        "His black hair is cut short",
        inputs=True,
    )
    assign_many(
        c,
        sheet,
        [
            (
                "03.2",
                "identity_constraint",
                "Explicit same character and constrained head/body layout.",
            ),
            (
                "03.3",
                "multi_angle",
                "Requested rear/front body and face package; media not inspected.",
            ),
            (
                "03.4",
                "prose",
                (
                    "Identity and layout properties in prose; style input is not "
                    "property verification."
                ),
            ),
            ("04.5", "sectioned", "Left/middle/right and layout-lock sections."),
            (
                "05.5",
                "reference_sheet",
                "Explicit character-reference package request.",
            ),
        ],
    )
    image = c.job(
        "4e1ed78a",
        "人物達の位置は構図の３等分したうちの右側。",
        "人物を小さく描写。人物達は背景の質感に合わせる。",
        inputs=True,
        controls=("is_inpaint",),
    )
    assign_many(
        c,
        image,
        [
            (
                "04.2",
                "spatial|composition",
                (
                    "Japanese instructions place figures in right third and match "
                    "background texture."
                ),
            ),
            ("04.3", "media_input", "Three actual input images; content not viewed."),
            (
                "04.4",
                "text_explicit|media_attached_content_unknown",
                "Placement/size in text; attached content unknown.",
            ),
            (
                "05.1",
                "multi_input|reference_guided",
                "Three-image conditioning with explicit figure-placement instruction.",
            ),
            (
                "05.2",
                "multiple_inputs|staged_construction",
                "21cdd520 and 23c75ad3 outputs are input images; no layers inferred.",
            ),
            (
                "05.3",
                "placement|scale",
                "Right-third location and small figure size requested.",
            ),
            (
                "05.4",
                "inpaint_false",
                "Explicit false preserved independently of edit intent.",
            ),
            (
                "08.1",
                "composition",
                "nano_banana_flash receives a figure-placement/scale task.",
            ),
        ],
    )
    stage = combine(
        image, c.edge("21cdd520", "4e1ed78a"), c.edge("23c75ad3", "4e1ed78a")
    )
    c.assign(
        "05.2",
        "multiple_inputs|staged_construction",
        stage,
        "Three inputs; two explicitly resolved output producers. Conditioning "
        "and staging, not compositing layers.",
    )
    video = c.job(
        "5b173d7d",
        "A twelve-second sequence consisting of exactly two shots",
        "At exactly six seconds, make one direct hard cut.",
        (
            "Preserve his referenced face, physique, hairstyle, clothing, "
            "colors, and patterns exactly."
        ),
        "No dialogue, music, exaggerated chewing, or dramatic sound effects.",
        controls=(
            "duration",
            "aspect_ratio",
            "resolution",
            "multi_shots",
            "generate_audio",
        ),
        inputs=True,
    )
    assign_many(
        c,
        video,
        [
            (
                "02.2",
                "character|setting|prop",
                "Explicit character, room and meal instructions with IDs.",
            ),
            (
                "02.3",
                "shot_list|multi_shot_instruction",
                "Two shots and one named six-second boundary.",
            ),
            (
                "02.4",
                "explicit_link",
                "Iguchi and Yakuza 5 are bound to their disclosed element IDs.",
            ),
            (
                "06.1",
                "image_guided|multi_shot_request",
                "Image/reference usages; two-shot text beside multi_shots=false.",
            ),
            (
                "06.2",
                "subject_action",
                "Eating and cut-boundary instructions; achieved motion unknown.",
            ),
            (
                "06.3",
                "timed_event|shot_boundary",
                "Explicit six-second cut within twelve-second request.",
            ),
            (
                "06.4",
                "audio_exclusion|generate_audio_true",
                "Audio exclusions and enabled control kept distinct.",
            ),
            (
                "06.5",
                "identity|appearance",
                "Explicit face, physique, hair, clothing and pattern preservation.",
            ),
            (
                "06.6",
                "duration|aspect_ratio|resolution",
                "Literal controls scoped to seedance_2_5.",
            ),
        ],
    )
    conflict = c.job("13273df7", "1990s Japanese color photo print", "monochrome")
    c.assign(
        "04.6",
        "possible_conflict",
        conflict,
        "Color print and trailing monochrome can refer to print versus capture; "
        "possible conflict requires adjudication, not model-confusion inference.",
        label="inferred",
    )
    reference_first(c, "0ca091f2", "06c9bb73")
    traced(c, "05607388", "4f438e33")
    finish(c, "4f438e33")
    family(c, ["009b4a27", "2be4a351"], equal=True)
    c.descendants("05607388")


def kiss(c):
    c.common("scene|entity|stage|mixed")
    references(c, "character|location|prop")
    c.assign(
        "02.6",
        "mixed",
        c.brief("Schedule, locations, crew, and logistics."),
        "Substantive Context alongside generic Narrative/Visuals/Production "
        "placeholders. Does not establish completed technical planning.",
        label="creator-stated",
    )
    image = c.job(
        "03055fdc",
        "Using the provided 3D layout blockout as the exact spatial reference",
        "generate a cinematic wide LOCATION plate",
        "Lay out the course left-to-right exactly as in the blockout",
        inputs=True,
        controls=("is_inpaint",),
    )
    assign_many(
        c,
        image,
        [
            (
                "03.4",
                "prose",
                (
                    "Spatial ordering and intended plate form in prose; blockout "
                    "content unobservable."
                ),
            ),
            (
                "04.2",
                "spatial|composition|preservation",
                "Explicit ordering and reference matching; no result assessment.",
            ),
            (
                "04.3",
                "media_input|reference_element",
                "Actual input asset and five reference_image usages with IDs.",
            ),
            (
                "04.4",
                "text_explicit|metadata_explicit|media_attached_content_unknown",
                (
                    "Ordering is text-explicit; names/categories are metadata; "
                    "media unknown."
                ),
            ),
            (
                "04.5",
                "sectioned|reference_tokens",
                "Ordered construction sections and numbered/element tokens.",
            ),
            (
                "05.1",
                "reference_guided|multi_input",
                (
                    "Input blockout and named prop/world references condition an "
                    "image request."
                ),
            ),
            (
                "05.2",
                "multiple_inputs|staged_construction",
                "Named prop outputs feed plate: 1430c7a7 edge asserted separately.",
            ),
            (
                "05.3",
                "placement|preservation",
                "Requested left-to-right obstacle placement and world matching.",
            ),
            (
                "05.4",
                "unspecified",
                (
                    "No explicit inpaint/mask/layer mechanism disclosed for this "
                    "plate request."
                ),
            ),
            (
                "05.5",
                "plate",
                "Explicit location-plate request, not verified output purpose/quality.",
            ),
            (
                "08.1",
                "composition|environment",
                (
                    "nano_banana_2 receives a spatially referenced environment "
                    "construction task."
                ),
            ),
        ],
    )
    c.assign(
        "05.2",
        "multiple_inputs|staged_construction",
        combine(image, c.edge("1430c7a7", "03055fdc")),
        "Six inputs include an explicitly produced prop; conditioning and "
        "staging, not compositing layers.",
    )
    sheet = c.job(
        "0509f83a",
        "Three studio photographs of the same 9-year-old American boy",
        inputs=True,
    )
    c.assign(
        "03.2",
        "identity_constraint",
        sheet,
        (
            "Same-character package instruction; names or appearance do "
            "not merge identities."
        ),
    )
    c.assign(
        "03.3",
        "multi_angle",
        c.job(
            "0509f83a",
            "full-body front photo on the left",
            "full-body back photo in the middle",
        ),
        "Explicit requested front/back character sheet; output not watched.",
    )
    c.assign(
        "03.6",
        "creator_declared",
        c.job("23904984", "as the strict spatial and visual reference.", inputs=True),
        (
            "Authority scoped to the supplied room for this camera change, "
            "not a global approved library."
        ),
    )
    video = c.job(
        "64c88da0",
        "SCENE CONTEXT",
        "HARD CUT TO BLACK",
        "Controlled multi-shot sequence with FIVE HARD CUTS",
        "A slow gentle push in",
        "The background does not change, shift or rebuild between shots.",
        "No other children, no other adults.",
        controls=(
            "duration",
            "aspect_ratio",
            "resolution",
            "multi_shots",
            "generate_audio",
        ),
        inputs=True,
    )
    assign_many(
        c,
        video,
        [
            (
                "02.2",
                "character|setting",
                "Named character and living-room element bindings in a task.",
            ),
            (
                "02.3",
                "multi_shot_instruction",
                "Explicit hard-cut boundary; full technical sections inspected.",
            ),
            (
                "02.4",
                "explicit_link",
                (
                    "Jack/Noah/mother/room instructions have explicit "
                    "reference-element bindings."
                ),
            ),
            (
                "06.1",
                "image_guided|multi_shot_request",
                (
                    "Reference images and multi-shot instructions; "
                    "multi_shots=false retained."
                ),
            ),
            (
                "06.2",
                "camera_action",
                (
                    "Named camera sections instruct framing transitions; output "
                    "motion not assessed."
                ),
            ),
            (
                "06.3",
                "shot_boundary",
                "Explicit hard cut to black; no screen timing measurement.",
            ),
            (
                "06.4",
                "generate_audio_true",
                "Enabled literal audio control; sound not evaluated.",
            ),
            (
                "06.5",
                "layout",
                "Background preservation across shots, scoped to this request.",
            ),
            (
                "06.6",
                "duration|aspect_ratio|resolution",
                "Raw parameters, not assumed equivalent across models.",
            ),
        ],
    )
    edit = c.job("14948b7d", "Remove the braces", inputs=True, controls=("model",))
    c.assign(
        "06.7",
        "video_edit_request",
        edit,
        "Explicit video input and braces-removal request, no defect/success judgement.",
    )
    c.assign(
        "09.2",
        "local_correction_request",
        edit,
        "Correction request does not establish previous failure or final acceptance.",
    )
    reference_first(c, "0035469c", "122382c3")
    traced(c, "0035469c", "122382c3")
    c.edge("2807fc31", "14948b7d")
    finish(c, "0557d4f0")
    family(c, ["03055fdc", "2c296b9d", "f1e77134"])
    delta = c.edge("6672ee33", "19f73675")
    before = c.job("6672ee33", 'Add the words "The Kiss"')
    after = c.job(
        "19f73675",
        'Move the entire title "The Kiss" UP',
        "Reduce the title's size slightly",
    )
    delta["source_path"] += "; generations.prompt"
    delta["excerpt"] += (
        " [producer text] " + before["excerpt"] + " [consumer text] " + after["excerpt"]
    )
    c.assign(
        "09.3",
        "text_addition|specificity",
        delta,
        "Explicit poster producer/input link; consumer adds title position and size "
        "specificity relative to producer's add-title request. No "
        "visibility defect verified.",
    )
    c.descendants("2807fc31")


def finalise(c):
    for row in c.rows.values():
        if row["status"] == "unknown":
            row["evidence_label"] = "inferred"
    if c.rows["09.3"]["status"] == "unknown":
        c.assign(
            "09.3",
            r"\N",
            combine(c.rows["09.1"]),
            "No directional revision delta established for this named candidate "
            "family. Shared inputs and text equality do not establish order or "
            "revision intent; no film-wide absence claim.",
            status="unknown",
            label="inferred",
        )
    if c.slug == "the-kiss":
        c.assign(
            "02.1",
            r"\N",
            c.brief("Schedule, locations, crew, and logistics."),
            "Production is generic placeholder prose; substantive Context "
            "describes the story, not an explicit technical production objective.",
            status="unknown",
            label="inferred",
        )
    # Harmony's nested negative field is independently exported; no reconstruction.
    if c.slug == "harmony":
        text = next(
            r
            for r in c.tables["generation_prompts"]
            if r["field_path"] == "params.negative_prompt"
        )
        span = text["text"].strip()[:65]
        assert span and span in text["text"] and span != text["text"]
        e = c.job(text["generation_id"])
        assert text["prompt_role"] == "negative"
        e["source_path"] += "; generation_prompts[params.negative_prompt].text"
        e["excerpt"] += " [field path] params.negative_prompt [role] negative " + span
        e["denominator"] = (
            "One negative field / all 2,125 exported text fields; primary "
            "crosswalk separate"
        )
        c.assign(
            "04.1",
            "primary|negative",
            combine(c.rows["04.1"], e),
            "Primary crosswalk retained in common(); one separate exported negative "
            "field, not negative phrases duplicated from primary text.",
        )
