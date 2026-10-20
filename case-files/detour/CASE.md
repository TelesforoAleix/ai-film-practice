# Detour — technical case file

Film `d90fe8bd-3329-40b3-963c-d9b33075aec1`, primary, both.
Codebook **1.0**: 48 coded / 1 unknown / 0 other, 49 assignments.
[Full evidence ledger](codes.csv); [profile and reading register](profile.json);
[traced examples](traced-edges.json).

All film-scoped records in all 14 tables were profiled. Technical reading covered
219/6162 job contexts: a purposive coverage set, their controls and usage roles,
bounded technical text windows, plus fuller instruction sections for named examples.
The visible brief and complete folder/reference metadata registers were inspected.
Exact text repeats were cross-referenced with each job’s context; long instructions
were not exhaustively annotated word by word. No media was watched. This case
cannot establish what separates selected films from other films.

Every claim below points to code IDs in the ledger, which supplies compound entity
keys, source paths, exact short excerpts, alternatives, denominators and confidence.
Prefix IDs in this narrative resolve to the full compound IDs there. Single-coder
semantic assignments are provisional; no independent agreement estimate exists.

## Study 02 — Planning

**Creator-stated:** Production describes continuity across geography, scale and
fast-moving action as a constraint and says character/location sheets established
the rules (02.1, 02.5–02.6). **Observed:** the costume-sheet request names a
persistent figure; `057fd821` specifies three connected two-second shots and binds
Ryu's reference to the task (02.2–02.4). **Interpretation:** a declared preparation
sequence and local bindings are visible; neither establishes the whole build order.
**Proposed:** retain declared plans separately from observed dependencies.

## Study 03 — Elements

**Observed:** the complete disclosed register includes character, prop and
literal environment categories; mapping environment to location is inferred
(03.1). `006dcc36` requests front, reverse and headshot views. Its output is an
input to `011fbb97`, which requests a ketchup mark while preserving the sheet
(03.2–03.5). **Interpretation:** this supports an inferred derivative version with
a named property change, not approved version metadata. `05637129` declares a
master composition and a separate colour reference, but the master-source token
is missing in the prose (03.6). Authority is task-scoped and that binding remains
unresolved. **Proposed:** record both property authority and unresolved bindings.

## Study 04 — Context

**Observed:** `00406410` combines an image and reference element with composition,
orientation and scale instructions (04.2–04.5). Primary fields are crosswalked;
three nested enhanced/source fields are retained separately, while language fields
are metadata (04.1). **Interpretation:** field names do not identify who rewrote
text. Attached content stays unobservable. A sufficiently scoped conflicting pair
is not established in this reading (04.6 unknown, not sample absence).
**Proposed:** keep each text path and property binding beside its attachment IDs.

## Study 05 — Images

**Observed:** `00406410` requests adding chevrons with placement/scale instructions
and a composition lock; its literal `is_inpaint=false` accompanies two input IDs
(05.1–05.4). The costume request explicitly names reference-sheet purpose (05.5).
**Interpretation:** multi-input conditioning and local-edit intent do not establish
layers, masks or successful integration. **Proposed:** separate requested edits,
conditioning inputs and disclosed mechanisms.

## Study 06 — Video

**Observed:** `057fd821` requests three timed shots with reference images while
`multi_shots=false`; duration, aspect, resolution, draft, extension and audio
controls remain literal (06.1, 06.3–06.6). `093e4529` specifies tracking-camera
motion. `0106d708` redirects a source video's performance to a named face under
`model=video_edit` (06.2, 06.7). **Interpretation:** neither textual timing nor a
correction request verifies output motion, identity or a previous failure.
**Proposed:** preserve shot intent, controls and correction scope independently.

## Study 07 — Lineage

**Observed:** `006dcc36` → `011fbb97` is a resolved sheet-to-edit input edge.
`093e4529` and `c430fa55` share exact reference assets (07.1–07.4). Raw/min
representations grouped by metadata stay under one asset ID; no cross-ID aliases
are merged. **Interpretation:** these are bounded motifs, not a global hub rank.
**Proposed:** the exported descendant set from `6354dd61` defines a review candidate
set (07.5); every reachable ID and traced edge is retained. It excludes hidden
edges and does not predict which images would visually change.

## Study 08 — Roles and models

**Observed:** named jobs establish sheet preparation, composition/editing and
animation roles across literal models. The sheet-to-edit edge connects
`seedream_v5_pro` to `gpt_image_2` (08.1–08.4). `c4625d5e` is a
`cinematic_video_editor` job with video/start-image inputs; its primary prompt is
unavailable. The brief separately names external refinement, editing and music
tools (08.5: job observed, external tools creator-stated). **Interpretation:**
co-occurrence and creator accounts cannot reconstruct all handoffs or internal
orchestration. **Proposed:** retain job and external-tool provenance separately.

## Study 09 — Iteration

**Observed:** the named `093e4529`/`c430fa55` shared-input candidate pair changes
its kart reference binding (09.1, 09.3). The sheet edit requests a local correction,
and an explicit later input establishes further-work use (09.2, 09.4).
**Interpretation:** comparison direction is not an established revision order;
reuse is not final approval. **Proposed:** show candidate membership, property
changes and approval as separate records.

## Study 10 — Organisation and resources

**Observed:** scene, entity, testing and final-labelled folders coexist; their
organisation meaning is inferred (10.1). Four author IDs occur across all jobs;
no labour division is inferred (10.2). The exact UTC event window, primary-text
repetition, two jobs with multiple folder placements and resource denominator are
in the measure table below (10.3–10.5). **Interpretation:** folder names such as
approved/FINAL do not supply approval events. The brief's seven-minute production
statement differs from the catalogue's duration used in the proxy.
**Proposed:** preserve both declarations and never convert the proxy or dates to
cost, labour or productivity.

## Complete-export measures and handoff

These observed aggregates have full evidence in codes 10.2–10.5, including their
query paths, denominators, competing explanations and confidence rationales.

| Code | Exact aggregate excerpt |
| --- | --- |
| 10.2 | 6162/6162 jobs with author ID; 4 distinct IDs |
| 10.3 | [6162, "2026-08-11 06:30:25.852481+00", "2026-09-11 09:58:50.692631+00"] |
| 10.4 | nonempty=6157; distinct_nonempty=2070; repeat_occurrences_beyond_first=4087; jobs_in_multiple_folders=2 |
| 10.5 | recorded_jobs=6162; catalogue_duration_seconds=678.375; jobs_per_declared_minute=545.008292 |

Unresolved assignments: 04.6. Each is scoped uncertainty, not an absent
practice. No codebook revision or panel replacement was needed. Batches 3–4 should
retain codebook 1.0 and use these case files as named examples, not prevalence
estimates or validated best practices. Full alias resolution, approval states and
semantic labels at scale remain later work. Proposals await the validation tests
in the [shared index](../README.md). Public records may omit external, discarded
or private work; no cost, failure rate, internal orchestration or quality is inferred.
