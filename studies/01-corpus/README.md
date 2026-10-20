# Study 01 — Corpus, evidence map, panel and codebook

## 1. Answer and evidence limits

The frozen release supports descriptive comparisons of **157 complete primary
public workspace histories**, with Cosmic tracks kept as a separate pilot. It
supports technical questions about recorded jobs, prompts, disclosed inputs,
models and organisation. It does not establish how these films differ from the
rest of the catalogue, or reveal missing external/private work. No media was
watched; no story, aesthetics, continuity or output quality was judged.

Coverage depends on the question: 118/157 primary films have nonempty brief text,
120/157 expose reference elements, 156/157 have recorded inputs, 155/157 have image
jobs and 156/157 have video jobs. All 157 have some prompt, date, author, output and
folder evidence; this does not mean every generation has every field. A missing
input is not proof of text-only generation. Complete item collection does not
mean complete briefs or complete production. The [coverage matrix](outputs/coverage.csv)
and [field counts](outputs/film_metrics.csv) must travel together.

These observations lead to a 16-film purposive panel and a 49-code shared codebook,
calibrated on four films. They are infrastructure for the later studies, not
findings about which techniques work best. Metric provenance, excerpts, evidence
labels, alternatives, denominators and confidence rationales are recorded in
[metric_evidence.csv](outputs/metric_evidence.csv),
[aggregate_evidence.csv](outputs/aggregate_evidence.csv) and
[calibration_evidence.csv](outputs/calibration_evidence.csv). The shared
[measure contract](PROVENANCE.md) explains how to join these to each output.

## 2. Population, coverage, units and denominators

| Population / reconciliation | Count |
| --- | ---: |
| Catalogue publications | 6,224 |
| Shortlisted / first-page most watched / overlap | 126 / 100 / 40 |
| Priority union: 126 + 100 − 40 | 186 |
| Shortlist only / most watched only / both, before exclusions | 86 / 60 / 40 |
| Non-open-source exclusions, all shortlist only | 23 |
| Public priority: 186 − 23 | 163 |
| Unavailable public priority: shortlist only / most watched only | 1 / 5 |
| Complete primary: 163 − 6 | 157 |
| Complete primary: shortlist only / most watched only / both | 62 / 55 / 40 |
| Supplemental Cosmic tracks, outside the 186 | 1 |
| Other index-only publications: 6,224 − 186 − 1 | 6,037 |
| Films with generation records: 157 + 1 | 158 |
| Primary jobs + supplemental jobs | 130,704 + 195 = 130,899 |

All counts match DATA.md; there is no population discrepancy. `audience_choice`
in shortlist_status identifies the 126-list union; `top_50` is a nested shortlist
label, not another population. Editorial labels remain separate. Original
most_watched_rank_top100 presence identifies that cohort; current views do not
re-rank it. Winners are not in the snapshot.

All 14 table row counts match DATA.md. Primary prompt counts across the 158
histories reconcile exactly: 124,642 nonempty, 61,479 distinct nonempty, 1,083
explicitly empty and 5,174 unavailable, totalling 130,899. The 119 reported decoded
briefs reconcile to 118 primary plus one pilot in the extraction flags. The
released evidence is flattened visible text and embeddings; decoded source
responses themselves are unavailable. See [snapshot_checks.json](outputs/snapshot_checks.json)
and [populations.json](outputs/populations.json).

The matrix contains **one row for every priority film plus the pilot (187)** and
columns for briefs, prompt fields, dates, inputs, outputs, authors, references,
folders, nested text, brief embeddings and brief decoding. `available` means at
least one exported nonempty item/value; `empty` means explicitly empty text or
zero exported items in a collected collection; `unavailable` means undisclosed
values or inaccessible collection. A zero exported reference collection is not
proof that no references were used. The 23 excluded and six unavailable histories
never become measured zero-work projects. Brief decoding is unavailable unless
explicitly recorded complete; there is no false flag invented from null.

Comparison units are films first, then jobs within each film. Creator, generation,
batch, asset, reference element and placement are separate grains. There are 151
literal creator handles among the 157 primary films; films by the same creator,
repeated prompts and batches are not independent. Assets include catalogue covers
and final-film links, so the total 163,184 is not a production-asset denominator.
All joins retain film IDs, even when this snapshot's generation IDs happen to be
unique across films.

## 3. Method, typing, taxonomy and codebook

Run the scripts from the repository root. The only data source is the verified
`data-2026-10-20` release. [profile.sql](profile.sql) exposes the population and
per-film aggregate queries. [build.py](build.py) builds the dictionary, profiles,
coverage, panel and supporting ledgers. All 14 source views remain strings.
[DICTIONARY.md](DICTIONARY.md), [dictionary.csv](outputs/dictionary.csv),
[grains.json](outputs/grains.json) and [json_paths.csv](outputs/json_paths.csv)
cover every table/column, proposed derived types, null/empty handling, compound
keys and observed JSON paths. [typed.py](typed.py) is an optional additive set of
temporary typed views; `connect` behaviour stays unchanged.

Nine generation parameters_json strings in one film fail parsing in the published
release. Their IDs are in [invalid_json.csv](outputs/invalid_json.csv); no repair
or reconstruction is performed. All other proposed scalar/JSON parses pass. This
is a released-field limitation, not a claim about what happened during collection.
Source-record paths do not make the unavailable raw responses accessible.

[Taxonomy](outputs/taxonomy.csv) separates declared catalogue duration/category
from these **provisional record-derived definitions**, chosen for this slice:

| Dimension | Operational definition | Limit / downstream dependency |
| --- | --- | --- |
| Image-led / film-led / mixed | At least 70% image jobs / at least 70% video jobs / neither, using all recorded jobs | A history-composition proxy, not the film's content or actual production order; revise only with explicit documentation. |
| Production scale | Small <200 jobs; medium 200–999; large 1,000–2,999; very large ≥3,000 | Recorded workload proxy, not labour, cost or film quality. |
| Model breadth | Narrow 1–3; moderate 4–8; broad ≥9 literal model identifiers | Versions/nicknames remain separate; roles await Study 08. |
| Reference use | Disclosed element count >0 versus none exported | Not the number of all media inputs and not an authenticated library census; Study 03 owns semantic entity/version definitions. |
| Organisation | Flat proxy ≤2 folders; partitioned >2 | Counts include root/system folders; scene/entity/stage meaning awaits case coding and Study 10. |
| Substantive planning | Non-template technical section, manually assessed | Brief availability alone is insufficient; section-level coding in Study 02. |
| Iteration family | Shared batch/input or explicit lineage first; similarity/time only a candidate | Actual revision intent needs Study 09; shared inputs can support unrelated tasks. |
| Adoption / canonical | Explicit downstream use / explicit scoped creator declaration | Use is not approval; hubs are not canonical by frequency. Studies 03/07/09 refine these. |
| Operation / route | Explicit job type, usage roles, prompt intent and active parameter values | Empty/missing inputs stay unknown; an instruction is not an achieved result or an editing implementation. Studies 05/06 refine it. |
| Information location | Text/metadata explicit; attached media content unknown | No property is assigned to media by inspecting it; Study 04's semantic labels and gold subset are pending. |
| Resource proxy | Recorded jobs ÷ declared seconds ×60 | Only comparable formats; not effort, spend, speed or productivity. Study 10 interprets it. |

These definitions are the local provisional layer required when upstream study
results do not exist. Dates are event windows only. No provider is inferred from
a model nickname. Catalogue category is `[]` for all 157 primary films: it cannot
supply a genre/format stratification. The 70% proxy yields 56 image-led, 17 film-led
and 84 mixed histories, out of 157, under that threshold only.

The [codebook](CODEBOOK.md) gives the 49 codes, values, inclusion/exclusion rules,
units and evidence protocol for Studies 02–10. The
[calibration assignments](outputs/calibration.csv) cover each code on Don't Poison
Ivy, The Kiss, Fallen Leaves and supplemental Cosmic tracks (196 rows). The
calibration log records draft-to-v1.0 revisions and unknown codes. These are
single-coder, purposive calibration notes, not full case files or an agreement
estimate. Excerpt checks validate source correspondence, not semantic accuracy.
No model labels at scale were generated; that remains a later slice.

## 4. Distributions, task/model/cohort context and unusual projects

Recorded job counts range from **4 to 6,862**, median **609**, IQR **249–1,032**
across 157 primary films. Literal model breadth has median 9 (range 1–24); folder
count median 12 (range 2–293). Declared duration has median 435.932 seconds (range
180.001–1,939.125); these are catalogue values, not measured screen time. See
[distributions.csv](outputs/distributions.csv) for measured denominators and
quantile definitions, and [film_metrics.csv](outputs/film_metrics.csv) for each film.

| Complete primary group | Films | Jobs | Median jobs/film |
| --- | ---: | ---: | ---: |
| Shortlist only | 62 | 45,497 | 568 |
| Most watched only | 55 | 31,169 | 316 |
| Both | 40 | 54,038 | 716.5 |

These are descriptive differences within the selected cohort. Selection, duration,
creator and absent external work are competing explanations; this slice supplies
no causal or significance claim. The groups do not represent the uncollected
catalogue or future winners.

The task-level split available here is **generation type**, not a coded operation
ontology: 92,058 image, 38,508 video, 132 audio, one text, one image_3d and four
unavailable types in the 130,704 primary jobs. Image jobs are 70.43% when pooled,
but the mean film's image share is 59.89% (157 films, each equally weighted).
Prolific image histories therefore change the pooled description. Video shares
are 29.46% pooled and 39.96% film-weighted. The separate pilot has 158 image, 36
video and one audio job, totalling 195; it contributes to none of these primary
comparisons. All 130,899 exported jobs are marked completed, so they cannot
estimate failure rates.

Literal `seedance_2_5`, for example, appears in 145/157 primary histories with
31,082/130,704 jobs (23.78% pooled; 31.14% mean per-film share). This establishes
recorded breadth/use, not a provider, workflow role or benefit. Complete per-film
breakdowns by type, literal model and author are in the `by_*.csv` outputs;
[model_weights.csv](outputs/model_weights.csv) and
[generation_weights.csv](outputs/generation_weights.csv) supply pooled and equal
film weights by cohort. Per-film creator, duration and declared category profiles
are retained beside them. Operation semantics await case files and Studies 05–08.

[The unusual-project audit](outputs/unusual_projects.csv) flags 49/157 films:
the union of upper 5% job/model/folder/duration values, lower 5% job counts,
multiple recorded authors, and rare/unavailable job types. Every flagged history
reconciles with its exported source-reported generation count; all table candidate
keys are unique at their documented grains. No film was removed or winsorized.
This audits released counts, not the unavailable extraction responses or whether
the whole history was made for this festival entry.

APEIROPHOBIA (6,862 jobs) and Detour (6,162) are deliberately retained as large
contrast cases; KAGEROU's 227 folders and One - The Mercy Ledger's 293 are
organisation outliers, not evidence of maturity. A Tales Before Titanic Tragedy
has four jobs despite a complete workspace flag: completion is not proof that the
archive contains a whole film's technical build. Their exact film IDs, triggers,
coverage and competing explanations are in the audit and metric ledger.

## 5. Traced examples and counterexample

Each example's complete keys, short published excerpts, source paths, evidence
label, denominator and competing explanation are in
[calibration_evidence.csv](outputs/calibration_evidence.csv). Evidence IDs below
are scoped to their film; the rows also carry the full film UUID. No example
asserts an achieved visual result.

1. **Don't Poison Ivy** (`d305f6e5-b906-49a1-a0c6-75ef7f653ad8`):
   `Dont_Poison_Ivy:I`, generation `bec13f8c-2125-4ff5-8a5b-c7e21511721b`,
   asks to “remove the plant”. It has an explicit image input and output, with
   `is_inpaint=false`. Observed: a local-edit request and disclosed input. Unknown:
   the actual editing mechanism or success. The creator's separate brief statement
   about character sheets, scene plates and video stays creator-stated (`:B`).
2. **The Kiss** (`655325cc-46d9-4b0b-b03d-d177defa4b3f`): `The_Kiss:B`
   quotes “Schedule, locations, crew, and logistics.” as template content. The
   brief also has substantive context, so code 02.6 is mixed. Observed source
   `The_Kiss:E` joins asset/producer `0035469c-1e6e-4c3f-aad6-bb3ab0bb05ce`
   (`nano_banana_2`) to consumer `122382c3-e873-4845-8a14-89ff9dfa215e`
   (`seedance_2_5`) at `params.reference_elements[0].medias[0]`. This is one
   explicit cross-model reuse edge, not evidence of an agent or global build order.
3. **Cosmic tracks, supplemental** (`94181633-a40a-4143-ace0-7d6bc3699d59`):
   `Cosmic_tracks:V`, generation `6cb74c0d-1051-4a84-834a-872d10fe4c55`,
   declares the start image “authoritative over every other reference”. This is
   observed instruction text for that sequence, not project-wide canonical approval
   or demonstrated continuity. `Cosmic_tracks:B` separately states external editing,
   compositing and sound design; those operations are not reconstructed from the
   public job list. This film never counts toward the primary panel.
4. **Counterexample — Fallen Leaves** (`6659c520-c88e-4ac7-a2c9-f28d8a40c954`):
   the flat two-folder register (`Fallen_Leaves:F`) coexists with ten disclosed
   reference elements in its metric row. `Fallen_Leaves:E` traces asset/producer
   `1cba062c-b6c5-456d-929d-b958859ae105` (`gpt_image_2`) into consumer
   `023fadcd-4fdd-46b9-98f4-1b940839b4c7` (`seedance_2_5`) as a reference
   image. The flat-folder proxy therefore cannot stand for absence of explicit
   element reuse. The sample supports that narrow counterexample, not a claim
   about how effectively identity was preserved.

## 6. Pattern catalogue and panel register

| Problem | Method, inputs and sequence | Evidence / tradeoffs / applicability |
| --- | --- | --- |
| A large history dominates a pooled summary | Aggregate compound-key jobs per film, then compare film shares beside pooled counts | Observed weighting difference above. Applies to all primary summaries; loses some job-level detail but exposes prolific histories. Failure mode: treating repeated jobs as independent films. |
| A visible brief section looks like completed planning | Read section text, identify placeholders, retain substantive sections, code uncertainty | The Kiss:B; observed text, inferred section classification. Manual interpretation remains necessary; template matching alone can discard genuine plans. |
| Editing intent is confused with an implementation | Pair prompt span with actual usage rows and active controls; code request and mechanism separately | Ivy:I and Cosmic:I; observed false inpaint fields. Applicable to request classification; no result or mask inference. Missing controls remain unknown. |
| A sparse workspace looks like a sparse production | Retain collection status and generation counts, audit extremes, state external-work uncertainty | Four-job complete history in the audit. Count reconciliation is useful; festival-specific work boundaries remain unknown. |
| Folder hierarchy is used as a proxy for reuse | Count folders, then examine element disclosure and explicit asset edges separately | Fallen Leaves counterexample. Graph work costs further analysis; folders alone miss dependencies. |

The [panel register](outputs/panel.csv) contains 16 film IDs, titles, groups,
selection reasons, matched film IDs and replacement fields. The frozen source is
[panel.json](panel.json): eight purposive contrast pairs, with group/size matches
where available and confounds explicitly named. There are six shortlist-only,
four most-watched-only and six both films. All three primary prior cases are
included; the pilot is excluded. **No replacements have occurred.** If later
replacement is needed, retain the original ID, reason, new ID and effect on its
pair/batch; choose from the same primary eligibility/contrast stratum and record
any relaxed match. Do not silently erase a selected case.

Four batches use largest-first assignment to the least-loaded batch with space,
with four films each. Generation count is a workload proxy only; the two largest
histories make equal totals impossible under this panel. Pair members may be in
different sessions; compare them after both case files exist.

| Batch | Films | Recorded jobs |
| --- | --- | ---: |
| 1 | APEIROPHOBIA; The Staff; Dry Aged Dreams; A Tales Before Titanic Tragedy | 6,959 |
| 2 | Detour; Fallen Leaves; Lost; THE LAST TRANSMISSION | 6,934 |
| 3 | Harmony; Birthdays; KAGEROU; The Kiss | 3,426 |
| 4 | Prophecy in 2047; SNAP; Don't Poison Ivy; Random Access Memories | 3,123 |

The extremes are part of the study's evidence audit, not a representative sample
or a ranking. About 16 eligible films were available without changing the criteria;
157 primary histories form the selection pool.

## 7. Studio implications — proposals to test

| Evidence | Requirement or hypothesis | Proposed behaviour | Validation test |
| --- | --- | --- | --- |
| Brief/field coverage varies independently of crawl completeness | Preserve evidence state at field and collection level | Separate unavailable, explicitly empty and observed values in import/UI | Synthetic null/empty/inaccessible round-trip, plus coverage review on case files |
| Published parameter JSON has nine parse failures | Preserve raw source and parse diagnostics | Add typed views with explicit empty/invalid flags, never repair silently | Synthetic invalid JSON plus released-key audit; verify original views unchanged |
| Explicit producer/input edges and folder counterexample | Identity and dependency records should survive organisation changes | Join on compound keys; show lineage separately from folder placement | Trace one edge, move its placement in a synthetic workspace, verify edge identity |
| Instructions and active controls have distinct meanings | Store intent beside literal operation controls | Separate requested edit/shot behaviour from implementation and output state | Calibrate paired prompt/control examples and adjudicate ambiguous cases |
| Reuse is observable but acceptance is not | Review state should be explicit | Track reuse for further work separately from approval | Human review exercise with named candidate/approval events |

All rows are **proposed** design responses, not reverse-engineered platform
architecture or tested best practices. No autonomous agents, routing, labour,
spend, speed, failure rates or quality benefits are inferred.

## 8. Missing evidence and handoff to Studies 02–11

The completion test is met by the per-study/per-film
[eligibility register](outputs/eligibility.csv) and
[summary](outputs/eligibility_summary.csv). These are outer eligible populations;
every narrower claim must apply its evidence gate and state its own denominator.
The pilot may be reported separately, never added to the primary numbers.

| Study | Eligible primary films / narrower gate | Missing evidence / dependency |
| --- | --- | --- |
| 02 | 157 for record reconstruction; 118 for brief-text inspection | Substantive sections, explicit planning/task links and build-order coding need case files; no private/blocked briefs. |
| 03 | 157; 120 expose element metadata | Complete libraries, semantic entity/variant links and canonical declarations unavailable or uncoded. |
| 04 | 157 with some prompt text | Hidden/default context and media contents unavailable; structural features and stratified semantic labels/gold agreement are later work. Invalid JSON-only text may be unavailable. |
| 05 | 155 with image jobs | Actual output properties, masks/layers and operation meaning need disclosed evidence; absent inputs are not text-only. |
| 06 | 156 with video jobs | Clip quality/used portions unavailable; routes and raw control semantics require case coding. |
| 07 | 157 outer histories; 156 have exported inputs | Resolved producers/aliases, full graphs and versions not yet reconstructed; private/external edges remain missing. |
| 08 | 157 with literal models | Operation roles and edge-supported transitions need case files; agents/scheduler/external finishing unobservable. |
| 09 | 157 outer histories; family comparisons require actual batch/input/lineage membership | Families and deltas uncoded; discarded work, defects and final acceptance unavailable. |
| 10 | 157 with dates/authors/folders and declared duration | Organisation semantics/ownership handoffs need case files; labour, spend and team structure unavailable. Category offers no format stratification. |
| 11 | 186 for catalogue context, 157 for production comparisons | Winners absent; wait for their announcement and Studies 02–10 measures. Do not retrieve them in this slice. |

Unresolved: the origin of the nine JSON parse defects; whether history boundaries
match festival-specific work; reference alias equivalence; substantive planning
in every brief; semantic operation/role labels; family intent; scoped canonical
versions and explicit approvals. The next four sessions create full case files
for these panel batches, across all study dimensions in one pass. They should
use this codebook, retain unknowns and extend the calibration log when a definition
changes. No upstream result has been invented to fill these gaps.

## 9. Reproduction and reusable outputs

```bash
uv sync --locked
uv run python scripts/fetch_data.py
uv run python studies/01-corpus/build.py
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/check_repository.py
```

For independent reproduction, fetch to `data/af1-clean`, then run
`uv run python studies/01-corpus/build.py --data data/af1-clean --output data/af1-reproduced`.
Compare every filename/hash with [outputs/reproduction.json](outputs/reproduction.json);
that manifest covers CSV/JSON outputs and excludes itself. The build performs no
network retrieval. Queries, codebook definitions, manual calibration assignments
and excerpt assertions are beside this report. Synthetic tests check table-specific
JSON typing, malformed JSON, compound keys and unavailable/empty distinctions.

Local validation passed: Ruff lint and format checks, all 10 tests, and the
repository boundary/original-hash check. An independent clean download verified
all 28 source assets; all 27 derived outputs reproduced byte for byte (plus the
identical reproduction manifest). The largest derived output is 443,934 bytes.

The five deliverables are coverage.csv (evidence map), taxonomy.csv, panel.csv,
dictionary.csv plus JSON paths/grains, and codebook.csv plus calibration/log.
Supporting outputs include film metrics, distributions, unusual-project audit,
per-film dimension profiles, equal-film/pooled weights, population reconciliation,
eligibility and provenance ledgers. Every derived CSV/JSON is below 1 MB and has
no full prompt texts. No `study-01-v1` release is needed. The original release,
original documents, programme, existing loader and corpus-build scripts are unchanged.
