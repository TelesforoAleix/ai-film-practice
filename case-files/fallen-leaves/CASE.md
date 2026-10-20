# Fallen Leaves — technical case file

Film `6659c520-c88e-4ac7-a2c9-f28d8a40c954`, primary, both.
Codebook **1.0**: 44 coded / 5 unknown / 0 other, 49 assignments.
[Full evidence ledger](codes.csv); [profile and reading register](profile.json);
[traced examples](traced-edges.json).

All film-scoped records in all 14 tables were profiled. Technical reading covered
356/356 job contexts: the complete job register, their controls and usage roles,
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

**Creator-stated:** Tone/Visual Style specifies naturalistic camera movement and
lighting in substantive prose (02.1, 02.6). **Observed:** `7188a902` requests a
persistent location across views; `0b35d954` names first-close-up and then-whip
framings; `62e05ad7` binds predecessor context to a task through input usages
(02.2–02.4). **Interpretation:** ordered local framing is not the complete build
order (02.5 unknown). This extends the calibration sample's unresolved planning
entry using newly inspected records. **Proposed:** store local plans without
inventing a project-wide execution sequence.

## Study 03 — Elements

**Observed:** the full ten-element register has character and environment
categories (03.1; location mapping inferred). `7188a902` requests an establishing
view plus two supporting angles (03.3–03.4). `aa8a5c34` requests regeneration with
no other changes (03.2). **Interpretation:** package requests and preservation
instructions do not establish element-version chains or canonical approval
(03.5–03.6 unknown). **Proposed:** keep requested packages and explicit version
approval separate.

## Study 04 — Context

**Observed:** primary fields crosswalk to nested params.prompt (04.1).
`330764cc` gives figure placement with actual image/reference inputs; their
contents remain unknown (04.2–04.5). `4e4c57a8` combines “Stationary film camera
shot.” with “The camera drifts slowly across the scene” (04.6).
**Interpretation:** this is a possible conflict; stationary may describe an
observational style or the drift may amend the earlier wording. No model confusion
is inferred. **Proposed:** retain paired spans for later scope adjudication.

## Study 05 — Images

**Observed:** `330764cc` receives three distinct inputs, including the recorded
output of `dc2e911c`; it requests named figure placement. `is_inpaint` is missing,
so the mechanism is unspecified (05.1–05.4). `7188a902` declares sheet purpose
(05.5). **Interpretation:** input convergence and a construction stage are
observable; masks, layers and achieved integration are not.
**Proposed:** keep the explicit producer/input links beside operation intent.

## Study 06 — Video

**Observed:** `62e05ad7` combines image/video/reference guidance and explicitly
asks for physical crane movement rather than pivoting. `0bc2480b` has timed
instructions. `aa8a5c34` consumes `023fadcd` and asks only for 1080p regeneration
under video_edit mode (06.1–06.7). Literal controls retain false and null.
**Interpretation:** a resolution request is not proof of improved output or a
technical failure. **Proposed:** scope preservation and resolution-change intent
independently of output assessment.

## Study 07 — Lineage

**Observed:** `1cba062c` (`gpt_image_2`) → `023fadcd` (`seedance_2_5`), then
`023fadcd` → `aa8a5c34`, are explicit producer/input links. The first asset is
attached through `params.reference_elements[0].medias[0]`; the second through
`params.medias[0].data` (07.1, 07.4). A named two-consumer pair shares exact inputs;
raw/min representations are grouped only within their asset entity (07.2–07.3).
**Interpretation:** flat folders do not imply missing reuse.
**Proposed:** use the fully enumerated exported descendants of `023fadcd` for
bounded review after change (07.5), without predicting visual impact.

## Study 08 — Models and roles

**Observed:** sheet/environment preparation is explicit in `gpt_image_2`;
the named reference-to-video edge supports a cross-model stage. The complete
profile retains `seedance_2_0` separately from `seedance_2_5` (08.1–08.4).
**Interpretation:** the brief's account of generated sound does not establish a
standalone audio job or named external finishing tool; 08.5 remains unknown.
**Proposed:** keep audio intent separate from audio-production visibility.

## Study 09 — Iteration

**Observed:** `023fadcd` and `45e66125` have equal primary text and shared inputs;
a separate explicit resolution-only correction consumes the former (09.1–09.2).
Further-work reuse is recorded, not acceptance (09.4). **Interpretation:** the
candidate family has no established directional text/input delta under 09.3;
its equal requests do not establish independent trials. The separate raw
resolution change remains documented under 06.7, without adding a codebook value.
**Proposed:** retain families, correction requests and raw parameter deltas separately.

## Study 10 — Organisation and resources

**Observed:** one populated root and Watermarks form the flat proxy; all jobs
have one recorded author. Event extrema, exact text repeats, placement counts and
the resource proxy use the complete export (10.1–10.5; table below).
**Interpretation:** this organisation coexists with ten disclosed elements and
resolved dependencies; it says nothing about private organisation, labour or
cost. **Proposed:** present folder and dependency views independently.

## Complete-export measures and handoff

These observed aggregates have full evidence in codes 10.2–10.5, including their
query paths, denominators, competing explanations and confidence rationales.

| Code | Exact aggregate excerpt |
| --- | --- |
| 10.2 | 356/356 jobs with author ID; 1 distinct IDs |
| 10.3 | [356, "2026-08-16 23:41:39.113613+00", "2026-09-11 18:02:11.276042+00"] |
| 10.4 | nonempty=356; distinct_nonempty=156; repeat_occurrences_beyond_first=200; jobs_in_multiple_folders=0 |
| 10.5 | recorded_jobs=356; catalogue_duration_seconds=339.336417; jobs_per_declared_minute=62.946383 |

Unresolved assignments: 02.5, 03.5, 03.6, 08.5, 09.3. Each is scoped uncertainty, not an absent
practice. No codebook revision or panel replacement was needed. Batches 3–4 should
retain codebook 1.0 and use these case files as named examples, not prevalence
estimates or validated best practices. Full alias resolution, approval states and
semantic labels at scale remain later work. Proposals await the validation tests
in the [shared index](../README.md). Public records may omit external, discarded
or private work; no cost, failure rate, internal orchestration or quality is inferred.
