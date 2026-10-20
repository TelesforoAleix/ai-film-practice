# Panel case files — batches 1–3

These are case-level evidence files for Studies 02–10, not corpus-wide findings.
All twelve registered films in batches 1–3 support technical case files; none was
replaced. Nothing was watched. The release is `data-2026-10-20`, freshly fetched
and verified against all 28 asset checksums. Only this release was opened; no
source site, media link or authenticated library was retrieved.

Only the selected cohort has detailed production records. These cases cannot
establish what separates top films from other films, estimate prevalence, or
establish a tested best practice. The 157 priority histories remain separate
from the supplemental pilot; every film here is primary. Batch 4 and semantic
prompt labels at scale remain outside this slice.

## Index and inspected scope

IDs and cohort groups come from the unchanged
[panel register](../studies/01-corpus/outputs/panel.csv). Counts below are **code
assignment states**, not counts of independent findings or measures of film quality.
Each linked ledger contains 49 rows in the calibration's exact column order.

| Film / ID / cohort | Code states: coded / unknown / other | Scripted profile | Technical reading |
| --- | --- | --- | --- |
| [APEIROPHOBIA](apeirophobia/CASE.md) · `c3d8ee5e-b119-4654-99f9-c6545f650635` · both | 43 / 6 / 0 | All 6,862 jobs and all film-scoped records in all 14 tables | 63/6,862 jobs, purposive; complete folder and one-element metadata registers; no sample-negative labels |
| [The Staff](the-staff/CASE.md) · `3b09c7c2-3f0c-48e3-8304-fad569bf50ce` · shortlist only | 43 / 6 / 0 | All 82 jobs and all film-scoped records in all 14 tables | 82/82 job contexts, technical prompt sections and controls/usages; visible brief, 28 folders, 23 reference records |
| [Dry Aged Dreams](dry-aged-dreams/CASE.md) · `3777eda4-c15e-4531-9f04-4c02a900f3c3` · most watched only | 19 / 29 / 1 | All 11 jobs and all film-scoped records in all 14 tables | 11/11 jobs, all primary text/controls/usages; two-folder register; unavailable brief |
| [A Tales Before Titanic Tragedy](a-tales-before-titanic-tragedy/CASE.md) · `3f6e509b-f3da-4324-a746-b9d35f0b9845` · most watched only | 27 / 13 / 9 | All four jobs and all film-scoped records in all 14 tables | 4/4 jobs, all primary text/controls/usages; exact repeated text read once with each job's context inspected; unavailable brief |
| [Detour](detour/CASE.md) · `d90fe8bd-3329-40b3-963c-d9b33075aec1` · both | 48 / 1 / 0 | All 6,162 jobs and all film-scoped records in all 14 tables | 219/6,162 jobs, purposive; complete 114-folder and 132-element registers; three nested enhanced/source text fields |
| [Fallen Leaves](fallen-leaves/CASE.md) · `6659c520-c88e-4ac7-a2c9-f28d8a40c954` · both | 44 / 5 / 0 | All 356 jobs and all film-scoped records in all 14 tables | 356/356 job contexts, technical text windows, controls/usages; visible brief, two folders, ten elements |
| [Lost](lost/CASE.md) · `e5ce8a79-9375-4e31-84a8-620bd4f07550` · shortlist only | 46 / 3 / 0 | All 350 jobs and all film-scoped records in all 14 tables | 350/350 job contexts, technical text windows, controls/usages; visible brief, six folders, 26 elements |
| [THE LAST TRANSMISSION](the-last-transmission/CASE.md) · `03f596b0-23da-4312-9e58-2e1cc4582348` · shortlist only | 37 / 6 / 6 | All 66 jobs and all film-scoped records in all 14 tables | 66/66 job contexts, technical text windows, controls/usages; visible brief, two folders, zero disclosed elements |
| [Harmony](harmony/CASE.md) · `2fd725ab-2604-4220-8cca-d332e9de53a2` · both | 47 / 2 / 0 | All 1,543 jobs and all film-scoped records in all 14 tables | 233/1,543 jobs, purposive; visible brief, all 11 folders and 51 reference metadata records; separate negative field |
| [Birthdays](birthdays/CASE.md) · `d51d6821-d191-40f7-949b-1086750a2e93` · shortlist only | 47 / 2 / 0 | All 1,003 jobs and all film-scoped records in all 14 tables | 170/1,003 jobs, purposive; visible brief, all 60 folders and 177 reference metadata records |
| [KAGEROU](kagerou/CASE.md) · `51d2c0b2-d692-42b4-b66f-daf87cac1eb3` · shortlist only | 43 / 6 / 0 | All 489 jobs and all film-scoped records in all 14 tables | 489/489 job contexts, technical text windows, controls/usages; unavailable brief, all 227 folders and 20 reference records |
| [The Kiss](the-kiss/CASE.md) · `655325cc-46d9-4b0b-b03d-d177defa4b3f` · both | 46 / 3 / 0 | All 391 jobs and all film-scoped records in all 14 tables | 391/391 job contexts, technical text windows, controls/usages; mixed brief, all 13 folders and 26 reference records |

Dry Aged Dreams' other state is one `not_observed_in_scope` for exact repetition
and multiple placements in the full exported history (10.4). Titanic's other
states are eight `not_applicable` (seven video codes and cross-model handoff)
and one `not_observed_in_scope` (09.3: no text/input delta among all four named
requests). No assignment uses `empty`: unavailable briefs are not empty briefs,
and equal nonempty requests are not empty exported fields. The five protocol
states remain supported by the validator.

## Method and units

[CODEBOOK.md](../studies/01-corpus/CODEBOOK.md) version **1.0**, all 49 codes,
is unchanged. No definition proved inapplicable in a way requiring revision;
there are no new codes, calibration changes or replacements. The four calibration
films retain their original assignments. Fallen Leaves and The Kiss also have separate
full case files; their calibration rows have not been silently replaced.

The reading covers technical instructions, not the narrative or aesthetic merit
of those instructions. For long prompts, sections, reference bindings, shot
boundaries, controls and attached usages were inspected; this is not a claim of
exhaustive semantic annotation of every word. Exact repeats were identified by
string equality and inspected with each job's own context. All semantic
assignments are manual, single-coder and provisional. There is no second-coder
agreement estimate, semantic model labeling or corpus-scale classifier here.

A row assigns a code to its **named unit**: a brief section, prompt span, job,
reference record, folder register, explicit edge, named candidate family or
whole-film aggregate. It does not label every job in the film. `study` and
`later_study` both identify the target study, unlike the Study 01 calibration's
study-of-calibration column. Evidence IDs are `<slug>:<code_id>`; entity IDs are
compound `<film_id>/<kind>:<entity_id>` keys. A whole-film aggregate explicitly
names the film and the source/query scope. Each row includes its field path,
short source excerpt or marked deterministic aggregate, denominator, evidence
label, alternative and confidence rationale. `<unavailable>` in a control
transcription means that key is missing; JSON null, false and empty containers
are retained separately. `[unavailable/null]` represents a raw unavailable field,
not quoted source text. Non-coded values use the CSV unavailable marker `\N`.

Observations, interpretations and studio proposals are separate in each CASE.md.
The narrative's code IDs link to its full ledger; they are not extra unsupported
findings. A request is not proof of the achieved result. Reference media contents
remain unknown. Public histories may omit external, discarded or private work.
Unknown semantic assignments remain unknown even after a full record profile;
scripted field coverage does not settle semantic absence.

Each `profile.json` contains row counts, field null/empty/nonempty counts, literal
model/type/author/status distributions, primary-text equality counts, text roles,
raw controls by model, folder placement counts, reference metadata, explicit
edge counts and the complete job reading register with selection reasons.
`measure_provenance` gives the film-scoped evidence contract and table-row
denominator for these descriptive profiles. Field distributions partition their
table's rows; control distributions partition jobs within their literal model
and path (a missing key is explicit). Prompt-state counts partition jobs; distinct
nonempty text uses only nonempty primary fields. No primary/nested duplication is
counted as two instructions.

Graph joins use film/asset and film/generation keys. Producer edges come from
`assets.generation_id` and non-output usages. Explicit edge counts are distinct
producer/consumer/asset/role/path tuples, not a degree or semantic reuse count.
Raw/min representations explicitly grouped in one asset metadata object are
retained under that asset ID. Cross-ID aliases are not merged by URL similarity.
The coded branch motifs deduplicate exact input IDs per consumer and name only
the compared members; none claims a global hub rank. Producer-unresolved inputs
remain unresolved. `traced-edges.json` records the named producer/consumer
examples, not a purported complete graph. 07.5 searches all exported edges and
names the reachable generation set; the proposed review scope excludes hidden
edges and does not predict visual impact.

## Why APEIROPHOBIA's 63 records

[profile.py](profile.py) deterministically selects jobs in generation-ID order;
[profile.json](apeirophobia/profile.json) preserves every selected ID and all
reasons. The union has 63 unique jobs, including both endpoints of selected
resolved producer/consumer pairs. It deliberately covers:

- All seven literal models and every observed model/type combination.
- All 20 folders with generation placements, out of 27 folder entities. The
  other seven have no generation placements; their labels were still inspected.
- Every observed job-type/input-role-set combination, including no exported
  input, multiple images, start/end frames, audio and video input roles.
- Each literal model/control/value combination for `model`, `is_inpaint`,
  `multi_shots` and `generate_audio`, and an attached use of the one disclosed
  reference element.
- Each resolved producer-model/consumer-model/input-role combination, retaining
  an explicit consumer and a supporting producer; shortest nonempty and longest
  primary prompts provide boundary examples.

This covers disclosed operations and topology for purposive technical reading;
it is not a probability sample, saturation claim or complete inventory of
semantic practice. Rare instructions elsewhere may be missed. A code's own
named evidence and denominator take precedence over the sampling register.
Sample absence is always `unknown`, never `not_observed_in_scope`.

## Traced examples and counterexample

These illustrate evidence handling, not an ordering of creators. All IDs in a
row are scoped to that film. Full paths, excerpts, alternatives and denominators
are in the cited assignment rows.

| Case and problem | Method / inputs / sequence | Evidence and limits |
| --- | --- | --- |
| APEIROPHOBIA: edit-to-editor handoff | `88160a68-3dd4-4662-be7e-4fb5852634c5` output → `b6e44e77-d4a0-4821-9663-55a452fffc01` → `311a3f4c-be35-4c70-8d8e-2b882804d9cd` | [07.5, 08.3–08.5](apeirophobia/codes.csv): explicit input_video edges; two downstream generations from one root, searching the whole exported graph. A proposed review set, not visual invalidation or final finishing approval. |
| The Staff: reference-assisted continuation | `0e619b88-43ef-4a45-84c3-b7b86ac96fe4` output → `1d963033-bc45-495d-9bfa-a05e4d0cf918`; consumer says “frame 1 same last frame from here” | [02.4, 07.1, 07.4, 09.4](the-staff/codes.csv): one resolved input_video edge among 82 jobs; both models are seedance_2_5. Reuse for further work, not approval. |
| Titanic: repeated package requests | Inputs `7a44e44c-7b45-4fc5-8c8b-303f25779194` and `612f580b-00fe-4730-a3eb-b2c49902c939` → all four sheet requests, including `416eb299-5a02-4dd1-99c1-8a11d9de0b04` | [03.3, 05.2, 07.2, 09.1–09.3](a-tales-before-titanic-tragedy/codes.csv): four consumers, two exact input IDs, one distinct primary text. Candidate reruns, not four independent tests or verified versions. |
| Counterexample: Dry Aged Dreams | All 11 usage rows are outputs; no exported input edge links the image and ten videos | [07.1, 08.3](dry-aged-dreams/codes.csv): two models co-occur without a reconstructable handoff. Missing inputs cannot prove text-only production, a complete direct workflow or absence of external work. |

## Proposals for later study design

Each row is **proposed**, awaiting validation; it is not a shared or tested best
practice. Tradeoffs concern evidence visibility, not judged production failures.

| Study / evidence | Requirement or hypothesis | Proposed behaviour | Validation test |
| --- | --- | --- | --- |
| 02: Staff 02.1 versus 02.4; missing briefs elsewhere | Keep declared plans separate from local task links | Store plan source and task binding independently | Resolve a named binding, then remove its plan source in a synthetic project; retain uncertainty |
| 03: Titanic 03.3; Ape 03.6 | Package intent and authority need scope | Store requested package and per-task authority separately | Ensure a sheet request cannot mark media verified or a library globally approved |
| 04: Staff 04.6 | Conflicts need paired spans and uncertain scope | Show the conflicting instructions for human review | Have independent coders adjudicate silent-clip/appended-speech scope |
| 05: Staff 05.4; Ape 05.1 | Intent must not determine editing mechanism | Preserve edit text beside literal controls | Round-trip false, missing and enabled inpaint in synthetic requests |
| 06: Ape 06.1; Staff 06.1 | Shot wording and controls need separate fields | Keep planned boundaries beside raw model controls | Preserve two-shot wording alongside multi_shots=false without rewriting either |
| 07: Staff and Ape 07.5 | Review reachability needs explicit boundaries | Enumerate downstream candidates from known edges | Check reachable sets on a synthetic branched graph with unresolved producers |
| 08: Dry 08.3 versus Ape 08.3 | Co-occurrence cannot stand in for transitions | Require a producer/input edge for handoffs | Remove the edge in a synthetic example; transition must become unresolved |
| 09: Titanic 09.1–09.3 | Equal requests are not approved versions | Separate candidate families, deltas, reuse and approval | Four equal requests must not create revision deltas or acceptance events |
| 10: all 10.3–10.5 | Resource visibility must preserve denominators | Show recorded jobs, declared seconds and timestamp coverage | Changing catalogue duration must change the proxy, never estimated labour or spend |

## Reproduce, validate and continue

From the repository root, with the verified source snapshot installed:

```bash
uv sync --locked
uv run python scripts/fetch_data.py
uv run python case-files/build.py
uv run python case-files/check.py
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/check_repository.py
```

`build.py` profiles completed batches 1–3 and transcribes the fixed manual assignments, asserting
all quoted spans against source fields and checking the named input/producer
relationships. It does not infer labels automatically. `reproduction.json` hashes
all generated CSV/JSON case artifacts (excluding itself); CASE.md files are human
reports. Full local reading packets stay in ignored `data/af2a/`, `data/af2b/` and
`data/af2c/`. No full prompt
text is committed, and every case artifact is below 1 MB, so no release asset is
needed for this slice. The original data, loader and Study 01 outputs are unchanged.

`check.py` validates every `*/codes.csv`, complete current-code coverage, one row
per code, current version, study mapping, five states, allowed coded values and
all evidence fields. CI invokes it through an artifact-contract test; its unit
fixtures are synthetic and never copy released records. Artifacts are discovered by glob; later slices must also extend the explicit
completed-batch set in build.py, profile.py and check.py.

Batch 4 should retain version 1.0 and the panel as registered unless their own
reading requires a documented revision or replacement. Unknowns are scoped
uncertainties, not missing rows to fill by assumption. If the codebook changes,
reapply it to all completed cases and all four calibration films, including the
supplemental pilot, and reproduce Study 01's outputs. Matched comparisons await
the other member's case file. Corpus-wide rates, complete semantic prompt labels,
full lineage/alias resolution, versions, actual build order and independent
adjudication remain later work. No policy, architecture or programme change was
needed here.


## Batch 2 reading scope and decisions

Batch 2 adds **196 assignments: 175 coded, 15 unknown and six not applicable**.
THE LAST TRANSMISSION's other states are the five image-operation codes (05.1–05.5:
all 66 exported jobs are video) and cross-model transition (08.3: one literal
model). No batch-two assignment uses empty or not_observed_in_scope. Reading
absence is unknown, including in Detour's purposive set. No film was replaced;
codebook **1.0** needed no revision, so no calibration reapplication was required.

The three smaller films were inspected through their complete job registers,
per-job literal controls and usage-role contexts, bounded technical text windows,
and fuller source sections for named coding examples. This is not exhaustive
word-by-word annotation of long prompts. Exact repeated text was cross-referenced
while inspecting each job's context. All visible briefs, folder labels and
disclosed reference metadata registers were inspected. Language metadata in
nested text is not an additional instruction. Detour's two enhanced_prompt fields
and one source_prompt field are retained by path; no authoring or internal
orchestration process is inferred from those names. Full fields remain local.

Detour uses the same deterministic generation-ID ordering and coverage strata as
APEIROPHOBIA, plus the three non-primary/non-language text fields. The union is
**219/6,162 jobs**; profile.json records every full ID and all selection reasons:

- All 16 literal models and observed model/type combinations, across image and video.
- Every one of the 102 folders with generation placements among 114 folder entities;
  all labels of the other 12 were still inspected.
- Every observed job-type/input-role-set combination, including video input,
  start-image input and no exported inputs.
- Every literal model/control/value combination for model, is_inpaint,
  multi_shots and generate_audio; attached examples for every disclosed reference
  element occurring in usages. The complete 132-element metadata register was read.
- Each resolved producer-model/consumer-model/input-role combination, with selected
  producer and consumer endpoints; shortest nonempty and longest primary text;
  every enhanced/source text field's job, including the additional `31b2de1a` job.

This is purposive operational/topological coverage, not random sampling, semantic
saturation or proof of all practices. Each code's own named unit and denominator
take precedence. Profile partitions and their provenance cover every film-scoped
row in every source table. No job's output media was retrieved or judged.

The batch-two decisions apply existing definitions, rather than changing them:
Detour's input-linked sheet with a named changed property is an **inferred_version**,
not approved version metadata; an unbound master-source token leaves that binding
unresolved despite its authority wording. Fallen Leaves' full reading adds a
local ordered-framing plan beyond the calibration sample. THE LAST TRANSMISSION's
multi-angle turn request is a video reference package, not a recorded still-sheet
job. Shared image inputs can support a bounded branch even when their producers
are unresolved. Possible context conflict in Fallen Leaves is single-coder and
needs adjudication, not a claim of model confusion.

## Batch 2 traced examples and counterexample

Each row joins its case ledger for complete film/entity keys, source excerpts,
paths, denominators, alternatives and confidence. Prefix IDs are local to the named
film. These are case examples, not independent tests or cross-film prevalence.

| Case / problem | Method, inputs and sequence | Evidence, limits and proposed test |
| --- | --- | --- |
| Detour: a sheet derivative | `006dcc36` output → `011fbb97`, seedream_v5_pro → gpt_image_2; one ketchup-mark request preserves the remaining sheet | [03.5, 07.1, 08.3](detour/codes.csv). Explicit input and changed property support an inferred version, not approval. Proposed: require version intent/approval metadata in a synthetic derivative test. |
| Fallen Leaves: reference to video to regeneration | `1cba062c` → `023fadcd` at reference_elements[0].medias[0], then → `aa8a5c34` at medias[0].data | [06.7, 07.1, 09.2](fallen-leaves/codes.csv). Exact asset links; final request says regenerate in 1080p. No quality or failure judgement. Proposed: round-trip raw resolution change beside preservation text. |
| Lost: multi-input construction | Twelve input_asset occurrences plus one reference_image condition `044604ad`, including `02e53a47` output | [05.2, 07.1](lost/codes.csv). Conditioning and one stage, not thirteen layers. Proposed: synthetic import must retain input roles without manufacturing layers. |
| Counterexample: THE LAST TRANSMISSION | All 66 jobs are video; image/video usages exist but no input resolves to a recorded producer across all 106 assets and 155 usages | [05.1–05.5, 07.1, 08.3](the-last-transmission/codes.csv). Preparation is creator-stated; actual preparation chain is unresolved. Proposed: remove a producer in a synthetic project and retain an unresolved input, never invent a job. |

## Batch 2 proposals and continuation

All requirements here are **proposed**, awaiting tests. They neither describe the
platform's architecture nor establish a tested best practice.

| Study / evidence | Requirement or hypothesis | Proposed behaviour | Validation test |
| --- | --- | --- | --- |
| 02: Transmission 02.5; Fallen 02.3 | Distinguish declared sequence from local plans | Store declaration and observed task binding independently | Remove producer evidence; retain creator statement with its label |
| 03: Detour 03.5–03.6 | Property changes need version and authority scope | Preserve inferred derivative and unresolved master binding | A missing token must not silently bind a canonical asset |
| 04: Detour 04.1; Fallen 04.6 | Field paths and scope ambiguity must survive import | Retain enhanced/source paths and conflicting spans | Independent coder review of the stationary/drift pair; synthetic path round-trip |
| 05: Lost 05.2–05.4 | Conditioning is distinct from mechanism | Preserve all input IDs and literal mechanism state | Multi-input fixture must not acquire mask/layer claims |
| 06: Fallen 06.7 | A resolution retry needs explicit invariants | Retain requested preservation and raw mode/resolution | Round-trip request without marking output improved |
| 07: Transmission 07.1; Detour 07.5 | Review sets require graph boundaries | Enumerate known descendants and unresolved producers | Synthetic branch plus missing producer; no hidden edge invented |
| 08: Lost 08.5; Detour 08.5 | External statements and observed editor jobs differ | Show evidence label/source with each process node | Remove observed editor job while preserving creator's external-tool statement |
| 09: Lost 09.3; Detour 09.3 | Deltas need supported membership | Keep linked correction distinct from unordered comparison | No timestamps-only revision order or inferred approval |
| 10: Lost 10.4; Detour 10.5 | Occurrences and declared durations need provenance | Display placements separately; retain brief and catalogue duration | Duplicated placements cannot change job count; denominator change stays explicit |

Batches 3–4 should retain codebook 1.0 and the registered panel. Fallen Leaves'
calibration remains a separate sample ledger; its five case-file unknowns are not
instructions to rewrite calibration. Detour's brief says seven minutes while its
catalogue duration is 678.375 seconds; the resource proxy explicitly uses the
latter. THE LAST TRANSMISSION's brief includes anecdotes about filters, tests and
failures, but the completed-job export cannot estimate their rates or independently
establish experimental support. Lost's creator credit statement is not monetary
cost. Keep these boundaries in later corpus-wide studies. No programme or
architecture change was needed, and batches 3–4 remain uncoded.

The extended check now requires exact completed-batch panel membership, profile
film consistency, reading-register uniqueness/reasons, complete field-state and
model/type distribution denominators, named evidence jobs within reading scope
(except whole-graph descendant enumeration), narrative presence, artifact hashes
and the 1 MB file limit. Synthetic fixtures exercise the scope/partition failures.


## Batch 3 reading scope and decisions

Batch 3 adds **196 assignments: 183 coded, 13 unknown, zero other states**.
Each film receives all 49 codes. No assignment uses empty, not applicable or
not observed in scope. Unknowns remain scoped uncertainty after the technical
reading; no sampled absence becomes a film-wide negative. No replacement or
codebook revision was needed: **1.0** and Study 01's calibration remain unchanged.
The source title `"Harmony "` has one trailing space. Its ledger and profile retain
that literal title; only the heading, link label and directory use the display name.
A synthetic test rejects accidental title stripping.

KAGEROU and The Kiss were read through all job contexts: per-job input roles,
literal controls and bounded technical text windows, with fuller sections for
named coding examples. Exact repeats were cross-referenced while each job retained
its own context. This is not exhaustive word-by-word semantic annotation of long
prompts. The visible briefs and complete folder/reference metadata registers were
inspected for all four films. No hidden brief, private library or media was retrieved.

Harmony and Birthdays use the existing deterministic generation-ID-ordered selection
method. Their complete job-ID/reason registers are in their profile.json files:

| Coverage stratum | Harmony | Birthdays |
| --- | --- | --- |
| Union selected / exported jobs | 233 / 1,543 | 170 / 1,003 |
| Literal models and every model/type combination | All 24 models | All 12 models |
| Folders with generation placements / folder entities | All 8 / 11 | All 53 / 60 |
| Complete disclosed reference metadata register | 51 entities | 177 entities |
| Additional non-primary/non-language text | One exported negative field | None exported |

For each film, the union also covers every observed job-type/input-role-set
combination; every literal model/control/value combination for model, is_inpaint,
multi_shots and generate_audio; attached uses for each reference element occurring
in usages; each resolved producer-model/consumer-model/input-role combination,
including both endpoints; and shortest nonempty/longest primary text. Empty
folders' labels were still read. Source field states and literal-control
partitions profile all records, not only selected jobs. Preset input_asset usages
can represent camera/lens/lighting controls: they are not automatically media
frames. These are operational/topological coverage strata, not probability
samples, saturation claims or complete semantic inventories. Rare instructions
outside the selected set can be missed; each code's named unit and denominator
remain authoritative.

The local decisions apply existing definitions:

- Harmony's source-of-truth statement and The Kiss's strict room reference are
  task-scoped authority, not approval of a project-wide canonical library.
- Birthdays' tablet producer/input link plus logo/panel changes support an
  inferred derivative version (03.5); no version ID or approval is invented.
- Four named views versus three panels in Birthdays, ten-second text versus a
  nine-second control in Harmony, and color-print/monochrome wording in KAGEROU
  remain possible conflicts with explicit alternatives, not model confusion.
- KAGEROU's unavailable brief stays unknown. Many scene folders do not establish
  a substantive plan or the actual build order. Version-like reference names
  cannot establish version edges.
- The Kiss's full record adds observed editor jobs and a named poster revision
  beyond its calibration scope. Calibration rows remain a separate historical
  sample, not silently expanded or overwritten.

## Batch 3 traced patterns and counterexample

Each row joins its case ledger for full compound keys, source paths, short
excerpts, evidence labels, denominators, alternatives and confidence. Prefix IDs
resolve only within the named film. These are case examples, not independent
trials, prevalence estimates or tested best practices. Requests do not establish
achieved output or technical failure.

| Case / technical problem | Method, inputs and sequence | Evidence, applicability and limits |
| --- | --- | --- |
| Harmony: reference preparation to shot request | Costume output `52b4e96b` → `1674aeae`, a four-shot task with character/room/wardrobe bindings and actual image inputs | [02.2–02.5, 06.1–06.6](harmony/codes.csv). Explicit reference input; useful as a local preparation pattern. multi_shots=false remains separate from four-shot text. Not the complete build order or executed shot list. |
| Birthdays: a tablet derivative | `37f689e1` → `372eae81`, seedream_v4_5 → seedream_v5_lite; producer tablet plus a second logo input, with a requested placement and panel change | [03.5, 05.2, 08.3](birthdays/codes.csv). Exact input edge and named changed property support an inferred version. Applicable to linked reference derivatives; no layer, version approval or successful embossing is disclosed. |
| KAGEROU: video to editor branch | `05607388` → `4f438e33`, `63b6c53f`, `b36d8b13`; seedance_2_5 output consumed by three cinematic_video_editor jobs | [07.1, 07.5, 08.3–08.5](kagerou/codes.csv). All exported edges searched; three descendants form a proposed review set. Editor text is unavailable, so this cannot recover edits or a final timeline. |
| The Kiss: scoped poster revision | Add-title output `6672ee33` → `19f73675`, whose request moves the title up and reduces its size | [09.3](the-kiss/codes.csv). Exact producer/input link plus changed text; applicable to traceable correction requests. Visibility defects, achieved correction and final approval remain unobservable. |
| Counterexample to treating shared inputs as ordered versions | KAGEROU `009b4a27` / `2be4a351` have equal primary text and exact shared inputs | [09.1–09.3](kagerou/codes.csv). Candidate reruns, with unconfirmed intention/order and no established directional revision delta. Family membership cannot supply missing approval or revision events. |

Tradeoffs and failure modes here concern evidence: missing producers, ambiguous
scope, aliases and unverified requests can lead to overstatement. They are not
observed generation failures or judgments about the films.

## Batch 3 implications and continuation

All behaviours below are **proposed**, awaiting validation rather than presented
as observed creator systems or tested best practice.

| Evidence | Requirement or hypothesis | Proposed behaviour | Validation test |
| --- | --- | --- | --- |
| Harmony 02.5; KAGEROU 02.1/02.6 | Local dependencies and brief coverage need independent states | Store preparation edges while preserving unavailable planning prose | Synthetic project with reference → task edge and null brief must retain both facts |
| Birthdays 03.5; KAGEROU 03.5 | Version intent needs more than a name | Keep inferred derivatives distinct from explicit versions and approval | Version-like name alone creates no edge; a named changed-property/input link creates only an inferred derivative |
| Harmony/Birthdays/KAGEROU 04.6 | Scope ambiguity needs paired source evidence | Show exact spans, literal controls and competing interpretations | Independent coders adjudicate view/panel, duration and print/capture examples before claiming conflict |
| The Kiss 06.1 versus 06.7 | Prompt continuation and typed video inputs are distinct | Derive recorded route from roles alongside textual requests | Synthetic reference-image job remains image-guided; adding input_video records a video-guided route |
| KAGEROU 07.5; The Kiss 09.3 | Reachability and revision deltas answer different questions | Store review candidates separately from changed instructions and acceptance | A downstream editor without text is reviewable but cannot generate a semantic delta or approval |
| All 10.1–10.5 | Labels, entity counts and occurrence counts need separate denominators | Preserve literal titles/folder IDs and show measured coverage | Synthetic trailing-space title, duplicated placement and unavailable brief survive round-trip without extra jobs or invented planning |

Batch 4 should extend the explicit completed-batch sets and retain **1.0** unless
its reading needs a documented revision. No revision occurred in batch 3, so none
requires reapplication. If a future revision is made, reapply it to all twelve
completed cases and all four calibration films, including the separate pilot,
and reproduce Study 01. Do not infer semantic absence from these purposive sets.
Harmony/Prophecy, Birthdays/SNAP and KAGEROU/Random Access Memories matched
comparisons await batch 4; this slice does not code their partners. The Kiss and
Fallen Leaves now each have a complete case file, but corpus-wide findings and
semantic labels at scale remain later slices. Full alias/version resolution,
actual build order, independent adjudication and approval states remain unresolved.

The batch-three build asserts every named excerpt and explicit edge. Checks also
validate literal registered titles and entity counts, film scope of compound keys,
prompt-state/role/control denominators, current-code coverage and the reproduction
manifest. Synthetic tests exercise those invariants without copying source records.
Batches 1 and 2 reproduce byte for byte; no prior case file was rewritten. Each
case artifact remains below 1 MB, so no derived release asset is required.
