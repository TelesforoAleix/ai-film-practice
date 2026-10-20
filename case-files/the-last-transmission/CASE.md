# THE LAST TRANSMISSION — technical case file

Film `03f596b0-23da-4312-9e58-2e1cc4582348`, primary, shortlist only.
Codebook **1.0**: 37 coded / 6 unknown / 6 other, 49 assignments.
[Full evidence ledger](codes.csv); [profile and reading register](profile.json);
[traced examples](traced-edges.json).

All film-scoped records in all 14 tables were profiled. Technical reading covered
66/66 job contexts: the complete job register, their controls and usage roles,
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

**Creator-stated:** Production gives “assets, then stress tests, then the film”
and Visuals specifies one motivated light source per frame (02.1, 02.5–02.6).
**Observed:** `0a5dad36` contains a named shot, plate and literal image ID that
matches its attachment (02.2–02.4). **Interpretation:** local task binding is
visible, but the creator's preparation sequence cannot be reconstructed from this
video-only history. **Proposed:** keep declarations and task bindings distinct.

## Study 03 — Elements

**Observed:** a named deck plate and JSON prose specify persistent context despite
zero exported reference elements. `2056af94` requests profile-to-frontal rotation
in a reference task; a separate screen edit preserves the surrounding person
(03.1–03.4). **Interpretation:** a requested video turn is a multi-angle package
instruction, not an observed still sheet. Element-version chains and canonical
approval remain unknown (03.5–03.6). **Proposed:** represent package medium and
purpose independently of reference-library disclosure.

## Study 04 — Context

**Observed:** primary fields crosswalk to params.prompt; language entries remain
metadata. The complete primary text of `0a5dad36` parses as JSON and contains
named plate binding, timed actions, camera instructions and audio exclusions;
its literal image ID matches the input usage (04.1–04.5).
**Interpretation:** JSON prose is still instruction text, and attached content
remains unknown. No sufficiently scoped conflict is established (04.6 unknown).
**Proposed:** preserve structured prose without treating it as executed controls.

## Study 05 — Image production boundary

**Observed:** all 66 exported jobs are video; there are zero image jobs.
**Interpretation:** the five image-operation codes are not applicable to this
exported job history (05.1–05.5), although the brief discusses sheets and assets.
This does not establish that no still preparation occurred elsewhere.
**Proposed:** retain the distinction between unsupported operations and inaccessible
preparation evidence.

## Study 06 — Video

**Observed:** `0a5dad36` specifies timed actions in a continuous take, no voice or
music, and enabled audio. `083272c6` requests replacing only the CRT screen while
preserving the person, movements, lighting and sound outside it, with
model=video_edit and an actual video input (06.1–06.7).
**Interpretation:** audio exclusions and an enabled audio flag can coexist because
effects remain allowed. A local-edit request does not disclose a mask or prove a
successful correction. **Proposed:** retain region scope, invariants and controls
as separate task properties.

## Study 07 — Lineage

**Observed:** inputs are typed but none resolves to an exported producer when all
106 assets and 155 usages are searched. `1338707f` and `feb2cb01` share two exact
image inputs while using different unresolved videos (07.1–07.4). Metadata groups
raw/min representations within one asset, without cross-ID alias merging.
**Interpretation:** shared-reference branching is supported; upstream generation
chains are not. A changed-producer descendant review set is unknown (07.5).
**Proposed:** show unresolved producer nodes instead of inventing lineage.

## Study 08 — Roles and models

**Observed:** all 66 jobs use literal `seedance_2_5`; timed action instructions
support an animation role and shared inputs support a bounded branch (08.1–08.4).
Cross-model transition is not applicable within this one-model export.
**Creator-stated:** scan lines were laid in post (08.5).
**Interpretation:** this post statement supplies neither an observed finishing
job nor a named tool. **Proposed:** record external process statements separately
from job graphs.

## Study 09 — Iteration

**Observed:** the named two-consumer pair shares image references and equal
primary text; `083272c6` separately requests a local screen correction
(09.1–09.2). **Interpretation:** different input videos can mean different shots;
no directional revision intent is established for that family (09.3 unknown).
No output resolves to a later recorded consumer, so adoption remains unknown
rather than rejection (09.4). Brief anecdotes about filters, failures and tests
are creator accounts; this case does not infer failure rates or experimentally
supported outcomes. **Proposed:** keep candidate grouping and review decisions
separate, preserving unknowns.

## Study 10 — Organisation and resources

**Observed:** the root/Watermarks register supports only a flat proxy. All jobs
have one recorded author and parseable events; exact repeats, placement counts
and the catalogue-duration proxy are given below (10.1–10.5).
**Interpretation:** the event window does not measure days worked; claims about
production effort in the brief are not converted into labour estimates.
**Proposed:** display recorded events, job counts and stated duration with their
original denominators.

## Complete-export measures and handoff

These observed aggregates have full evidence in codes 10.2–10.5, including their
query paths, denominators, competing explanations and confidence rationales.

| Code | Exact aggregate excerpt |
| --- | --- |
| 10.2 | 66/66 jobs with author ID; 1 distinct IDs |
| 10.3 | [66, "2026-08-16 21:05:16.584612+00", "2026-09-10 14:37:35.730842+00"] |
| 10.4 | nonempty=66; distinct_nonempty=56; repeat_occurrences_beyond_first=10; jobs_in_multiple_folders=0 |
| 10.5 | recorded_jobs=66; catalogue_duration_seconds=271.458333; jobs_per_declared_minute=14.587874 |

Unresolved assignments: 03.5, 03.6, 04.6, 07.5, 09.3, 09.4. Each is scoped uncertainty, not an absent
practice. No codebook revision or panel replacement was needed. Batches 3–4 should
retain codebook 1.0 and use these case files as named examples, not prevalence
estimates or validated best practices. Full alias resolution, approval states and
semantic labels at scale remain later work. Proposals await the validation tests
in the [shared index](../README.md). Public records may omit external, discarded
or private work; no cost, failure rate, internal orchestration or quality is inferred.
