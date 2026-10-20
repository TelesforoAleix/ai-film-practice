"""Final batch: manual, scoped coding decisions with executable source assertions.

No semantic classifier; helpers only transcribe the named reading decisions.
"""

from batch2 import assign_many, family, traced
from batch3 import combine, finish, reference_first, references


def brief(c, span, value):
    e = c.brief(span)
    c.assign(
        "02.1",
        value,
        e,
        "Project-specific technical declaration, not verified delivery.",
        label="creator-stated",
    )
    c.assign(
        "02.6",
        "substantive",
        e,
        (
            "Specific technical prose in the inspected brief section; linked "
            "scripts/media remain unobserved."
        ),
        label="creator-stated",
    )


def package(c, prefix, *spans):
    e = c.job(prefix, *spans, inputs=True)
    assign_many(
        c,
        e,
        [
            (
                "03.2",
                "identity_constraint",
                "Explicit same-identity/package constraints; output not inspected.",
            ),
            (
                "03.3",
                "multi_angle",
                "Requested multiple views, not verified fulfilment.",
            ),
            (
                "03.4",
                "prose",
                (
                    "Named identity/layout properties in text; media content remains "
                    "unknown."
                ),
            ),
            (
                "05.5",
                "reference_sheet",
                "Explicit reference-sheet request; not final acceptance.",
            ),
        ],
    )


def image(c, prefix, spans, values, mechanism):
    e = c.job(prefix, *spans, controls=("is_inpaint",), inputs=True)
    assign_many(
        c,
        e,
        [
            (
                "04.2",
                "spatial|composition|preservation",
                "Explicit spatial or framing and preservation instructions.",
            ),
            (
                "04.3",
                "media_input",
                "Actual typed input usages; no media content inferred.",
            ),
            (
                "04.4",
                "text_explicit|media_attached_content_unknown",
                "Named properties explicit in text; attached content unobservable.",
            ),
            (
                "04.5",
                "sectioned",
                "Named source/edit or reference/composition sections.",
            ),
            (
                "05.1",
                values,
                (
                    "Instruction and actual inputs establish requested operation; no "
                    "successful correction inferred."
                ),
            ),
            ("05.3", "preservation", "Preservation scoped to this named image task."),
            (
                "05.4",
                mechanism,
                "Literal mechanism state; request language is not a mask or layers.",
            ),
            (
                "08.1",
                "composition|local_edit",
                (
                    "Explicit construction/edit request assigned to the literal "
                    "recorded model."
                ),
            ),
        ],
    )
    return e


def video(c, prefix, spans, route, motion, invariant):
    e = c.job(
        prefix,
        *spans,
        controls=(
            "duration",
            "aspect_ratio",
            "resolution",
            "multi_shots",
            "generate_audio",
            "model",
        ),
        inputs=True,
    )
    assign_many(
        c,
        e,
        [
            (
                "02.2",
                "character|setting|prop",
                (
                    "Named persistent characters, location and props in the inspected "
                    "task; not a narrative reconstruction."
                ),
            ),
            (
                "02.4",
                "explicit_link",
                (
                    "Task explicitly binds named entities/properties to the supplied "
                    "IDs; not a complete brief-to-task map."
                ),
            ),
            (
                "06.1",
                route,
                (
                    "Typed usage roles and written route intent; false multi_shots "
                    "stays separate from shot wording."
                ),
            ),
            ("06.2", motion, "Explicit actors of motion; no achieved motion assessed."),
            (
                "06.3",
                "timed_event|shot_boundary"
                if "multi_shot_request" in route
                else "timed_event|ordered_event",
                "Written timing/order; raw duration is a separate control.",
            ),
            (
                "06.4",
                "generate_audio_true",
                (
                    "Literal enabled audio control; no usable sound or standalone "
                    "audio job inferred."
                ),
            ),
            (
                "06.5",
                invariant,
                (
                    "Explicit invariants scoped to this request; survival through "
                    "generation unobserved."
                ),
            ),
            (
                "06.6",
                "duration|aspect_ratio|resolution",
                (
                    "Literal controls retained within this model/version, without "
                    "cross-model equivalence."
                ),
            ),
        ],
    )
    return e


def derivative(c, producer, consumer, span, before):
    e = combine(
        c.edge(producer, consumer),
        c.job(producer, before),
        c.job(consumer, span, inputs=True),
    )
    c.assign(
        "03.5",
        "inferred_version",
        e,
        (
            "Named reference producer/input link plus changed property "
            "supports a derivative interpretation; no explicit version ID or "
            "approval."
        ),
        label="inferred",
    )
    c.assign(
        "09.3",
        "specificity",
        e,
        (
            "Consumer adds an explicit changed-property instruction to the "
            "named input; a scoped delta, not evidence of a defect or "
            "successful repair."
        ),
    )


def conflict(c, prefix, span, note):
    c.assign(
        "04.6",
        "possible_conflict",
        c.job(prefix, span, controls=("duration",)),
        note,
        label="inferred",
        alternative=(
            "Written timing may describe intended usable content while "
            "duration describes the requested container, or the text may be "
            "stale drafting material. No model confusion or achieved timing is"
            " inferred."
        ),
    )


def prophecy(c):
    c.common("scene|entity|stage|mixed")
    references(c, "character|location|prop")
    brief(c, "Output 21:9, 4K.", "deliverable")
    package(
        c, "7ef74efa", "Three views", "DO NOT REDESIGN IT. The shapes are unchanged."
    )
    e = image(
        c,
        "02e8e2a1",
        [
            "ACTIVE REFERENCES",
            "The billboard screen displays EXACTLY the image",
            "FOREGROUND:",
        ],
        "reference_guided|multi_input",
        "unspecified",
    )
    c.assign(
        "08.1",
        "composition",
        e,
        (
            "Explicit scene composition assigned to gpt_image_2_unlimited; no "
            "local-edit intent inferred from conditioning alone."
        ),
    )
    c.assign(
        "05.3",
        "placement|scale|perspective|preservation",
        e,
        (
            "Explicit foreground layout and camera distance/angle; exact "
            "billboard/reference preservation requested."
        ),
    )
    c.assign(
        "05.2",
        "multiple_inputs|staged_construction",
        combine(e, c.edge("0ffdcb42", "02e8e2a1")),
        (
            "Four typed input occurrences including a prepared cargo "
            "reference; conditioning, not layers."
        ),
    )
    v = video(
        c,
        "014a8505",
        [
            "Six separate shots joined by five hard cuts",
            "4.0s HARD CUT",
            "tracking with her, handheld tremor",
            "The pod stays clear of the ground at all times",
            "Roopa hauls right to left",
            "Heavy rain falls in every frame.",
        ],
        "image_guided|multi_shot_request",
        "subject_action|camera_action|environment_motion",
        "appearance|motion",
    )
    c.assign(
        "02.3",
        "shot_list|multi_shot_instruction",
        v,
        "Explicit six-shot timed list; no executed cut list inferred.",
    )
    c.assign(
        "03.6",
        "creator_declared",
        c.job("014a8505", "is the FIRST FRAME of this shot", inputs=True),
        (
            "First-frame authority scoped to this shot, not project-wide "
            "canonical approval."
        ),
    )
    conflict(
        c,
        "9ba4db45",
        "One continuous take, eight seconds",
        "Eight-second text versus duration=5; scopes may differ.",
    )
    edit = c.job(
        "17d142bf",
        "change only the lighting and the grade",
        inputs=True,
        controls=("model", "duration"),
    )
    c.assign(
        "06.7",
        "video_edit_request",
        edit,
        (
            "Explicit video_edit control and input_video; lighting/grade "
            "change request, not successful revision."
        ),
    )
    c.assign(
        "09.2",
        "local_correction_request",
        edit,
        "Correction intent does not establish a prior failure.",
    )
    derivative(
        c,
        "4aa39556",
        "7ef74efa",
        "Only its age, its power state and its palette",
        "Identical repeating segments",
    )
    reference_first(c, "0ffdcb42", "014a8505")
    traced(c, "18ae4caf", "a8868745")
    finish(c, "a8868745")
    family(c, ["0233bd03", "20cb7776", "2c09f05d"])
    c.descendants("18ae4caf")


def snap(c):
    c.common("flat_proxy")
    package(
        c,
        "16536627",
        "Character reference sheet of the SAME person",
        "One FRONT view",
        "one BACK view",
    )
    c.assign(
        "03.1",
        "character",
        c.job("16536627", "Character reference sheet of the SAME person", inputs=True),
        (
            "Character-reference creation request establishes this category "
            "despite zero disclosed element records; no authenticated library "
            "inferred."
        ),
    )
    e = image(
        c,
        "0139b8bd",
        [
            "It is the ground truth.",
            "only the box with the ball in it",
            "Same sheet layout",
        ],
        "reference_guided|local_edit_request",
        "unspecified",
    )
    c.assign(
        "03.6",
        "creator_declared",
        e,
        (
            "Ground-truth declaration scoped to the supplied source for this "
            "edit; not global approval."
        ),
    )
    poster = c.job("0c0903da", "Movie Poster style", inputs=True)
    c.assign(
        "05.2",
        "multiple_inputs|staged_construction",
        combine(poster, c.edge("784a8b5f", "0c0903da")),
        (
            "Three distinct inputs in the poster job; a prepared room output "
            "is linked explicitly, without compositing-layer inference."
        ),
    )
    v = video(
        c,
        "2199ecf1",
        [
            "Timed multishot, 15 seconds, six shots.",
            "1.9s HARD CUT",
            "Every shot locked off",
            "Same 4000K key from frame-left, same wardrobe, same room",
        ],
        "image_guided|video_guided|extension|multi_shot_request",
        "subject_action",
        "layout|appearance",
    )
    c.assign(
        "02.3",
        "shot_list|multi_shot_instruction",
        v,
        "Six-shot list with explicit cut boundaries, separate from multi_shots=false.",
    )
    conflict(
        c,
        "2199ecf1",
        "Timed multishot, 15 seconds, six shots.",
        ("15-second text versus duration=18; only the timing pair is coded here."),
    )
    edit = c.job(
        "795abb74",
        "Change character outfit",
        inputs=True,
        controls=("duration", "generate_audio"),
    )
    c.assign(
        "06.7",
        "video_edit_request",
        edit,
        (
            "Typed input_video and outfit-match request; "
            "hf_mult_replace_object is retained literally."
        ),
    )
    c.assign(
        "09.2",
        "local_correction_request",
        edit,
        "Explicit outfit correction intent, no defect/success inferred.",
    )
    derivative(
        c,
        "0139b8bd",
        "b1e57fe3",
        "make the full photo the box",
        "only the box with the ball in it",
    )
    reference_first(c, "16536627", "0d9a690f")
    traced(c, "3894fc5f", "795abb74")
    c.assign(
        "08.5",
        "job_observed",
        c.job("610971db", controls=("resolution",), inputs=True),
        (
            "Literal bytedance_video_upscale job with video input and "
            "explicitly empty primary prompt. Finishing intent text and final "
            "use unavailable; duplicate input occurrence paths do not create "
            "two source clips."
        ),
    )
    family(c, ["3759b66b", "77d4d4e8"], equal=True)
    c.descendants("3894fc5f")


def ivy(c):
    c.common("scene|entity|asset_type|stage|mixed")
    references(c, "character|location|prop")
    brief(c, "Stylized 3D animated. No dialogue.", "constraint")
    package(
        c,
        "028ae653",
        "A three-panel prop reference sheet",
        "CENTER PANEL",
        "the same single pair of shoes",
    )
    e = image(
        c,
        "5bc1268c",
        [
            "TRANSPLANT THE PLANT FROM IMAGE 2 ONTO THE SHELF.",
            "FIRST, SCALE.",
            "SECOND, POSITION.",
            "THIRD, VIEWING ANGLE.",
            "FOURTH, LIGHTING.",
        ],
        "reference_guided|local_edit_request|multi_input",
        "inpaint_false",
    )
    c.assign(
        "05.2",
        "multiple_inputs|staged_construction",
        combine(e, c.edge("4ebd698e", "5bc1268c"), c.edge("c16ce530", "5bc1268c")),
        (
            "Two exact producer inputs converge in the placement task, not two"
            " disclosed layers."
        ),
    )
    c.assign(
        "05.3",
        "placement|scale|perspective|lighting|preservation",
        e,
        (
            "Explicit placement, uniform scaling, low viewing angle, "
            "relighting and preservation in a linked image task."
        ),
    )
    c.assign(
        "03.6",
        "creator_declared",
        c.job(
            "5bc1268c", "it is the exact object to be placed into image 1", inputs=True
        ),
        (
            "Object authority is scoped to this transplant request, not a "
            "canonical library approval."
        ),
    )
    v = video(
        c,
        "407acee9",
        [
            "6 shots. Total 30 seconds",
            "SHOT 1 IS ONE CONTINUOUS UNBROKEN MOVE",
            "Diegetic sound and room tone only.",
            "no slow motion",
        ],
        "image_guided|multi_shot_request",
        "camera_action",
        "motion",
    )
    c.assign(
        "02.3",
        "shot_list|multi_shot_instruction",
        v,
        (
            "Written six-shot plan and five hard cuts; false multi_shots is "
            "separately retained."
        ),
    )
    c.assign(
        "06.4",
        "ambience|audio_exclusion|generate_audio_true",
        v,
        "No music and diegetic/room-tone intent coexist with enabled audio control.",
    )
    split = combine(
        c.edge("a9d85422", "070cf05b"),
        c.job("a9d85422", "ONE CONTINUOUS SHOT — 15 seconds"),
        c.job(
            "070cf05b",
            "TWO SHOTS — 15 seconds total.",
            "ONE HARD CUT at 0:08.",
            inputs=True,
        ),
    )
    c.assign(
        "06.7",
        "split_request",
        split,
        (
            "Linked continuous-shot source to two-shot consumer request; "
            "observed request change, not achieved cut or project order."
        ),
    )
    c.assign(
        "09.2",
        "local_correction_request",
        c.job("bec13f8c", "remove the plant", inputs=True),
        "Removal request; no prior failure or successful repair inferred.",
    )
    derivative(
        c,
        "c16ce530",
        "d720b7d2",
        "This is a paint addition to a single object, not a redesign.",
        "bare clay with no decoration, no painting",
    )
    conflict(
        c,
        "c0b9fa1b",
        "ONE CONTINUOUS SHOT — 6 seconds.",
        (
            "Six-second written take versus duration=12, kept as a possible "
            "scope conflict."
        ),
    )
    reference_first(c, "0020c74f", "0df863b8")
    traced(c, "dc7c91e0", "fbf502ce")
    finish(c, "fbf502ce")
    family(c, ["0df863b8", "bf12116e", "ff964502"], equal=True)
    c.descendants("dc7c91e0")


def ram(c):
    c.common("scene|entity|asset_type|stage|mixed", primary_prefix="0143044b")
    references(c, "character|location|prop")
    brief(c, "Duration: 5 min.", "deliverable")
    package(
        c,
        "1224c12b",
        "character sheet of Adrian",
        "front view, side view",
        "different expressions",
    )
    e = image(
        c,
        "d3a5b0ea",
        ["use foreground of image 1", "keep perspective consistent"],
        "reference_guided|multi_input",
        "unspecified",
    )
    c.assign(
        "04.2",
        "spatial|composition",
        e,
        "Explicit foreground/background roles and perspective matching.",
    )
    c.assign(
        "08.1",
        "composition",
        e,
        (
            "Explicit foreground/background construction; no mask, layer or "
            "local-correction intent inferred."
        ),
    )
    # This short request is an unsectioned instruction, not sectioned by length.
    c.assign(
        "04.5",
        "short_edit",
        e,
        "Short construction instruction; no full prompt reproduced.",
    )
    c.assign(
        "05.3",
        "perspective",
        e,
        "Perspective matching requested for foreground/background conditioning.",
    )
    c.assign(
        "05.2",
        "multiple_inputs|staged_construction",
        combine(e, c.edge("49ff032e", "d3a5b0ea"), c.edge("c22d3af3", "d3a5b0ea")),
        (
            "Two explicitly resolved producer inputs condition "
            "foreground/background construction; no layers disclosed."
        ),
    )
    video(
        c,
        "3123d068",
        [
            "Single continuous take, one camera position, exactly 20 seconds.",
            "Simon enters walking screen-left to screen-right",
            "No subtitles, no captions, no on-screen text, no music.",
            "The frame never changes for the entire 20 seconds",
            "100% matches the reference.",
            "18.0s to 20.0s:",
        ],
        "image_guided",
        "subject_action",
        "layout|appearance",
    )
    # Bind the observed folder entity from its literal name, never a name-based
    # lineage join.
    folder = next(
        r for r in c.tables["folders"] if r["folder_name"] == "S07: Breakfast"
    )
    c.assign(
        "02.3",
        "scene",
        c.aggregate(
            "folders.folder_name",
            folder["folder_name"],
            "One scene label / all 24 inspected folders",
            c.key("folder", folder["folder_id"]),
        ),
        "Literal scene label; executed ordering remains unknown.",
    )
    c.assign(
        "03.6",
        "creator_declared",
        c.job(
            "3123d068",
            (
                "controls the table shape, wood, wear and the breakfast dressing "
                "on it only"
            ),
            inputs=True,
        ),
        (
            "Reference authority explicitly limited to named table properties,"
            " excluding framing/light; not project canonical approval."
        ),
    )
    c.assign(
        "06.4",
        "dialogue|voice|audio_exclusion|generate_audio_true",
        c.job(
            "3123d068",
            "VOICE AGE LOCK",
            "Ambient sound ducks under every spoken line.",
            "No music of any kind.",
            controls=("generate_audio",),
        ),
        (
            "Dialogue/voice direction and exclusions retained as intent, "
            "separate from the control."
        ),
    )
    edit = c.job(
        "08339c56",
        "Swap character",
        "including voice",
        inputs=True,
        controls=("model", "duration"),
    )
    c.assign(
        "06.7",
        "video_edit_request",
        edit,
        (
            "Explicit character/voice replacement with input_video; no "
            "achieved result inferred."
        ),
    )
    c.assign(
        "09.2",
        "local_correction_request",
        edit,
        "Character correction request does not prove a prior defect.",
    )
    derivative(
        c,
        "a5620e3d",
        "d0efc423",
        "overused, tape around it",
        "make prop sheet of a Commodore 64 console",
    )
    conflict(
        c,
        "21115193",
        "Instrumental score cue only. Twelve seconds.",
        (
            "Twelve-second written score versus duration=16. Job remains typed"
            " video; the score request is not an audio-type job."
        ),
    )
    reference_first(c, "1224c12b", "34dacec2")
    traced(c, "ca1978b3", "fed8571b")
    finish(c, "fed8571b")
    family(c, ["1a0f7dbf", "1eec64ae"], equal=True)
    c.descendants("ca1978b3")


def finalise(c):
    for row in c.rows.values():
        if row["status"] == "unknown":
            row["evidence_label"] = "inferred"
