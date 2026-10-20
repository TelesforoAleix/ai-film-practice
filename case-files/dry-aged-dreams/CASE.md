# Dry Aged Dreams — technical case file

Film `3777eda4-c15e-4531-9f04-4c02a900f3c3`, primary, most-watched only.
Codebook 1.0: **19 coded, 29 unknown, one not_observed_in_scope**, 49 assignments.
[Full evidence ledger](codes.csv); [full-record profile and reading IDs](profile.json).
All 11 jobs were inspected with their primary text, raw controls and usages;
all film-scoped rows in all 14 tables were profiled. The brief is unavailable.
This tiny exported history supports a case, not a reconstruction of the whole
finished film. Only the selected cohort has detailed records, so this cannot
explain what separates top films from other films.

## Study 02 — Planning

**Observed:** the brief is unavailable (02.1, 02.6); no explicit plan-to-task
binding is established (02.4 unknown). **Interpretation:** these records cannot
settle production decomposition; a catalogue synopsis is not a technical plan.
**Proposed:** retain an unavailable-plan state rather than invent scene objects.

## Study 03 — Reusable elements

**Observed:** zero reference-element rows in the complete exported collection;
the environmental image request places spatial properties in prose (03.4).
Package, identity/version and canonical codes remain unknown (03.1–03.3,
03.5–03.6). **Interpretation:** the export does not establish an element library;
zero disclosed elements cannot disprove reference work elsewhere.
**Proposed:** store provenance for prose properties without inventing identities.

## Study 04 — Prompt and context

**Observed:** image job `3e7791d1-6165-4a81-bbaa-575811c1edd8` explicitly separates
“FOREGROUND:”, “MIDDLE GROUND:” and “BACKGROUND:” (04.2, 04.4–04.5). Its primary
path crosswalk is retained separately from the duplicated nested field (04.1).
Attached context remains unknown (04.3). **Interpretation:** this is a sectioned
request, not evidence that the output obeyed the structure. **Proposed:** preserve
text sections and attachment availability as different fields.

## Study 05 — Image construction

**Observed:** the one image job has empty `input_images` and null `input_image`;
05.1 is `fresh_candidate`, and 05.4 is `unspecified`. No nonempty mask or layer is
established. **Interpretation:** no exported input does not prove a text-only
pipeline. The image's eventual purpose remains unknown (05.5).
**Proposed:** keep operation confidence and mechanism disclosure separate.

## Study 06 — Video control

**Observed:** ten video jobs use literal `seedance_2_5`. In
`c32600a6-0e04-4039-a577-2c8cdf2d60c2`, “slow push-in” and “SFX only.” accompany
`duration=4`, `resolution=480p`, `aspect_ratio=21:9`, `generate_audio=true`,
`multi_shots=false`, `draft=false`, `extension_mode=null` (06.1–06.2, 06.4, 06.6).
**Interpretation:** these are requested camera/audio behaviour and raw controls;
neither achieved movement nor usable sound is observable. **Proposed:** keep
shot intent beside literal controls without translating models into common units.

## Study 07 — Lineage

**Observed:** all 11 usage occurrences are outputs; searching all 17 asset
entities and all usages exposes no input dependency (07.1 unknown).
07.3 retains one explicitly grouped raw/min representation; no cross-ID aliases
are collapsed. **Interpretation:** reconstructable chaining is unavailable,
not disproved. A downstream review set is unknown (07.5).
**Proposed:** show unresolved lineage rather than a proven disconnected graph.

## Study 08 — Models and roles

**Observed:** `nano_banana_2` has one job; `seedance_2_5` has ten. The named image
request supports an environment role, while the models only co-occur (08.1–08.3).
**Interpretation:** co-occurrence does not establish a model handoff. Workflow
shape and audio/finishing visibility remain unknown (08.4–08.5).
**Proposed:** require a producer/input edge before showing a transition.

## Study 09 — Iteration

**Observed:** all 11 primary prompts are distinct (10.4); 09.1–09.4 remain unknown
because no supported multi-member family, scoped revision or adoption edge is
established. **Interpretation:** this cannot show absence of iteration or rejection
of outputs; external or unpublished work may be omitted.
**Proposed:** distinguish unobserved candidate histories from rejected candidates.

## Study 10 — Organisation and resources

**Observed:** two folders support `flat_proxy` (10.1, inferred meaning of literal
labels). All 11 jobs have one recorded author and parseable event timestamps;
extrema are 2026-09-11 11:05:01.269389 to 11:10:14.008280 UTC (10.2–10.3).
No repeated primary text or multiple generation placements occurs within the
11-job export (10.4, exhaustive scoped negative). The proxy is 11 jobs /
(532.928 declared seconds / 60) = **1.238441 jobs per declared minute** (10.5).
**Interpretation:** the event window is not labour time and the ratio is not
productivity, spend or a count of all work. **Proposed:** present its numerator,
denominator and missing-work boundary together.

The central counterexample is two models without a reconstructable handoff.
Later studies should retain the unknown plan, reference, iteration and lineage
fields; the broader cohort cannot be inferred from this case. All proposals
await the validation tests in the [case-file index](../README.md).
