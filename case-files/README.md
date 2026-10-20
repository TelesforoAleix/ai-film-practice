# Panel case files — batch 1

These are case-level evidence files for Studies 02–10, not corpus-wide findings.
All four registered batch-one films support a technical case file; none was
replaced. Nothing was watched. The release is `data-2026-10-20`, freshly fetched
and verified against all 28 asset checksums. Only this release was opened; no
source site, media link or authenticated library was retrieved.

Only the selected cohort has detailed production records. These cases cannot
establish what separates top films from other films, estimate prevalence, or
establish a tested best practice. The 157 priority histories remain separate
from the supplemental pilot; every film here is primary. Batches 2–4 and semantic
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
films retain their original assignments. They are not additional batch-one cases.

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

`build.py` profiles batch 1 and transcribes the fixed manual assignments, asserting
all quoted spans against source fields and checking the named input/producer
relationships. It does not infer labels automatically. `reproduction.json` hashes
all generated CSV/JSON case artifacts (excluding itself); CASE.md files are human
reports. Full local reading packets stay in ignored `data/af2a/`. No full prompt
text is committed, and every case artifact is below 1 MB, so no release asset is
needed for this slice. The original data, loader and Study 01 outputs are unchanged.

`check.py` validates every `*/codes.csv`, complete current-code coverage, one row
per code, current version, study mapping, five states, allowed coded values and
all evidence fields. CI invokes it through an artifact-contract test; its unit
fixtures are synthetic and never copy released records. Future batches are
included automatically by the glob.

Batches 2–4 should retain version 1.0 and the panel as registered unless their own
reading requires a documented revision or replacement. Unknowns are scoped
uncertainties, not missing rows to fill by assumption. If the codebook changes,
reapply it to all completed cases and all four calibration films, including the
supplemental pilot, and reproduce Study 01's outputs. Matched comparisons await
the other member's case file. Corpus-wide rates, complete semantic prompt labels,
full lineage/alias resolution, versions, actual build order and independent
adjudication remain later work. No policy, architecture or programme change was
needed here.
