# Lost — technical case file

Film `e5ce8a79-9375-4e31-84a8-620bd4f07550`, primary, shortlist only.
Codebook **1.0**: 46 coded / 3 unknown / 0 other, 49 assignments.
[Full evidence ledger](codes.csv); [profile and reading register](profile.json);
[traced examples](traced-edges.json).

All film-scoped records in all 14 tables were profiled. Technical reading covered
350/350 job contexts: the complete job register, their controls and usage roles,
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

**Creator-stated:** Resources describes taking reference photographs, making
assets, and building the beginning/end before bridging the middle. Status names
a three-minute final cut (02.1, 02.5–02.6). **Observed:** `02e53a47` maintains one
character in a sheet request; `08d2776c` contains seven shot labels with named
character/reference bindings (02.2–02.4). **Interpretation:** the creator's order
is not independently reconstructed from timestamps. **Proposed:** retain declared
sequence and local task bindings with distinct evidence labels.

## Study 03 — Elements

**Observed:** the complete 26-element register retains literal categories,
including auto categories, without treating them as verified identities (03.1).
`02e53a47` requests the same character in a changed presentation and specifies
background/eye properties in prose (03.2–03.4). **Interpretation:** a generic
sheet request is not a multi-angle package. Names such as v1 do not establish
version links or canonical approval (03.5–03.6 unknown).
**Proposed:** store identity constraints, package form and approval separately.

## Study 04 — Context

**Observed:** the primary field crosswalk avoids duplicate prompt counting.
`02e53a47` is a short edit with three actual input_asset rows, same-character
wording and explicit background/eye instructions (04.1–04.5).
**Interpretation:** media content is unknown; metadata labels cannot verify it.
No sufficiently scoped conflict is established (04.6 unknown).
**Proposed:** retain prompt spans and all attachment IDs without inferring unseen
properties or hidden context.

## Study 05 — Images

**Observed:** `044604ad` requests placing characters in a town with wide framing;
it has twelve input_asset rows plus a reference_image. Its inputs include the
recorded output of `02e53a47`. The separate sheet edit has no disclosed inpaint
boolean, mask or layers (05.1–05.5). **Interpretation:** this is conditioning and
an observed construction stage, not thirteen compositing layers or successful
integration. **Proposed:** represent actual input roles and editing mechanisms
independently.

## Study 06 — Video

**Observed:** `08d2776c` combines seven shot labels, ordered actions and image
inputs while `multi_shots=false`. `09925f84` asks to preserve the scene while
changing sound/grade and making one continuous shot; it consumes video even
though its raw model field is default (06.1–06.7).
**Interpretation:** request type is not determined by a model nickname; timed or
ordered text does not establish achieved cuts or corrected sound.
**Proposed:** store changed-shot intent beside literal controls and input roles.

## Study 07 — Lineage

**Observed:** `02e53a47` → `044604ad` is an image construction link;
`66411159` → `09925f84` crosses image to video; `4e117e2d` → `09925f84` is a
video input link. Named consumers `044604ad`/`0aa04ddc` share exact assets
(07.1–07.4). Raw/min grouping stays within one metadata asset.
**Interpretation:** placements never add independent assets or edges.
**Proposed:** use the enumerated descendants of `4e117e2d` as the exported review
boundary (07.5), keeping hidden/external dependencies unresolved.

## Study 08 — Models and roles

**Observed:** `seedream_v4_5` has sheet/local-edit requests; the named
`66411159` → `09925f84` edge supports transition to `seedance_2_5` (08.1–08.4).
The brief says “Edited using capcut.” (08.5, creator-stated).
**Interpretation:** this statement is separate from observed jobs, and provides
no recoverable editor timeline. `seedream_v5_lite` remains a separate literal
identifier in the full profile. **Proposed:** distinguish explicit transitions,
model co-occurrence and external-tool statements.

## Study 09 — Iteration

**Observed:** a named image pair shares inputs; `09925f84` consumes `4e117e2d`
and adds a continuous-shot preservation constraint to its text (09.1–09.3).
Output reuse supports further work only (09.4). **Interpretation:** neither a
correction request nor reuse establishes defect, success or acceptance. Shared
inputs alone can also condition unrelated tasks.
**Proposed:** require named membership and changed paths before displaying revisions.

## Study 10 — Organisation and resources

**Observed:** Scenes, Characters, Locations and Assets support an inferred mixed
organisation. All jobs have one recorded author; 275 jobs have multiple folder
placements among 817 placement rows. Exact repetition, UTC events and the
catalogue-duration proxy are recorded below (10.1–10.5).
**Interpretation:** duplicated placements are not additional jobs. The brief's
credit statement does not establish monetary cost and is not converted here.
**Proposed:** expose entity/occurrence denominators beside resource measures.

## Complete-export measures and handoff

These observed aggregates have full evidence in codes 10.2–10.5, including their
query paths, denominators, competing explanations and confidence rationales.

| Code | Exact aggregate excerpt |
| --- | --- |
| 10.2 | 350/350 jobs with author ID; 1 distinct IDs |
| 10.3 | [350, "2026-08-19 15:30:10.047746+00", "2026-09-12 23:25:09.624728+00"] |
| 10.4 | nonempty=350; distinct_nonempty=102; repeat_occurrences_beyond_first=248; jobs_in_multiple_folders=275 |
| 10.5 | recorded_jobs=350; catalogue_duration_seconds=202.199365; jobs_per_declared_minute=103.857893 |

Unresolved assignments: 03.5, 03.6, 04.6. Each is scoped uncertainty, not an absent
practice. No codebook revision or panel replacement was needed. Batches 3–4 should
retain codebook 1.0 and use these case files as named examples, not prevalence
estimates or validated best practices. Full alias resolution, approval states and
semantic labels at scale remain later work. Proposals await the validation tests
in the [shared index](../README.md). Public records may omit external, discarded
or private work; no cost, failure rate, internal orchestration or quality is inferred.
