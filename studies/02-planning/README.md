# Study 02 — Planning and production decomposition

## 1. Answer and limits

The public records support **local decomposition into persistent entities,
requested views and input-bound tasks**. They support much less about a master
plan or the order in which a whole film was built. Across 157 primary histories,
123 have at least one numbered-shot/count lexical marker in primary text; this
is a wording measure, not the prevalence of substantive planning. In the
purposive panel, 14/16 cases establish a local plan/task binding; the other two
remain unknown. [The evidence ledger](outputs/case_evidence.csv) and
[panel maps](outputs/panel_maps.json) retain the scope of each conclusion.

Briefs are declarations, not execution logs. Of 16 panel cases, ten establish
substantive technical brief intent, one mixes substantive Context with generic
technical placeholders, and five have unavailable briefs. Eight cases support
an **inferred local reference-preparation sequence** through explicit asset
edges; three more state preparation order in their briefs. Neither set recovers
complete project order. Scene-first, character-first and exploratory production
cannot be compared as executed project strategies from this evidence.

The proposed studio response is a planning workspace linking versioned brief
claims, scene states, requested shots and executable tasks, with evidence and
unknowns attached. It is a hypothesis awaiting validation, not a tested best
practice or a reconstruction of platform architecture. Only the selected cohort
has detailed records; these findings cannot establish what separates top films
from other films. No media was opened or judged for story, aesthetics, quality
or continuity. No agents, internal orchestration, labour, cost or failure rates
are inferred.

## 2. Population, coverage, units and denominators

Study 01's unchanged [eligibility register](../01-corpus/outputs/eligibility.csv)
provides 157 Study 02 production-eligible primary films. Of the 186-film priority
union, 23 non-open-source listings were excluded and six workspaces unavailable.
The supplemental Cosmic tracks pilot contributes to no measure here. All 49
unusual projects remain; no outlier is removed or winsorized. There are 151
literal creator handles among the 157 films, so film comparisons are not
independent creator comparisons.

| Scope | Denominator / limitation |
| --- | --- |
| Record reconstruction | 157 films, 130,704 compound film/job keys; 62 shortlist only, 55 most watched only, 40 both |
| Brief structural inspection | 118/157 nonempty briefs; 39 unavailable; no explicitly empty brief; availability does not establish substance |
| Primary text | 124,449 nonempty + 1,083 empty + 5,172 unavailable = 130,704 fields |
| All-role structural text | 160,526 nonempty field occurrences after primary/nested crosswalk; film-distinct text counts are retained per film, not independent jobs |
| Folder labels | 3,230 compound film/folder keys across 157 films, including root/system folders; placements are not scene membership |
| Semantic scope | All 16 registered case files and all 96 Study 02 assignments; eleven visible panel briefs, five unavailable; no panel replacements |
| Technical brief extraction | 16 × seven field categories = 112 scoped assignments; populated spans are not exhaustive entity/shot lists |
| Maps | One map for each of 16 panel films; observed attachments, inferred property correspondences, local preparation edges and unknown links distinguished |

The semantic cases are purposive and have unequal reading scopes, particularly
the largest histories. Their assignment counts audit the panel; they are never
corpus prevalence estimates. Corpus measures use every eligible record. Missing
text never becomes a negative semantic decision or proof of text-only work.

## 3. Method, codebook and automated checks

[build.py](build.py) uses `film_practice.connect`, Study 01's dictionary and
[measures.sql](measures.sql). Source views remain strings. JSON is parsed with
`json.loads`; false, null, absent, empty, invalid and unavailable states stay
separate. Nine released malformed parameter strings remain invalid and cannot
supply controls. All joins use compound film/entity keys. No source site,
external script, blocked brief or authenticated library is retrieved.

Codebook **1.0**, codes 02.1–02.6, is unchanged. The case ledger is copied with
its original excerpt, source path, evidence label, alternatives, denominator and
confidence. [readings.json](readings.json) adds short, manually chosen technical
brief spans in seven categories: objectives, constraints, visual intentions,
deliverables, characters, settings and shots. All positive spans are checked
against the source; unavailable/unestablished values remain null. Main Characters,
Eric's room and Final shot in Random Access Memories are retained as **labels**,
not specifications of completed planning. Narrative interpretation is excluded.

Automated brief inspection splits the seven standard section headings and a
preamble, retaining offsets, lengths and SHA-256, without copying full text.
Eight exact generic placeholder sentences are flagged, including generic
Production and Visuals text. A placeholder with additional prose is a mixed
candidate. Other prose remains **nonplaceholder/unclassified**, not automatically
substantive. Custom headings remain within those regions; this is not a complete
semantic section parser. The `empty_sections` metric counts empty parsed regions,
including preambles; filter `heading != preamble` for empty headed sections. Corpus substance cannot be estimated by subtracting
placeholder counts. Case files provide the semantic decisions; the other 107
nonempty briefs outside the eleven visible panel briefs are not newly assigned
substantive-plan labels.

Prompt features reuse the exact regular expressions from the merged
[prompt-label tools](../../prompt-labels/README.md). Primary-field job indicators
record section, reference-token and multi-shot lexical matches. The latter
recognises numbered shots, numeric shot counts and multi-shot wording; **one
numbered shot, negation or quotation can match**. It misses ordered framings,
spelled-out counts, languages and synonyms. Nested primary copies are removed
by compound generation plus field path, asserting exact text equality first.
The all-role film-distinct text denominator and multi-shot match count are
recomputed and checked against all 157 merged AF3a summary rows. Nested language
metadata stays `other_text`, never a new planned task. The 19 separately exported
shot-prompt fields remain a different unit from the primary-field indicators.

[structural_audit.csv](outputs/structural_audit.csv) preserves deterministic first
positive/negative primary-field keys where available in each panel film, with
short exact spans and full-match offsets/hashes. This checks lexical
correspondence, not semantic accuracy.
Fallen Leaves, Birthdays and THE LAST TRANSMISSION supply additional case-based
coverage counterexamples below. There is no model semantic label run, second
coder, semantic precision/recall estimate or inter-coder agreement. Structural
absence must not become absence of planning.

Every numeric row joins [metric_evidence.csv](outputs/metric_evidence.csv) on
film_id for study, full compound-key scope, query/source path, numeric excerpt,
alternatives, denominators and confidence. Aggregate members are explicit in
`summaries.csv`; type/model member sets are exactly the per-film rows satisfying
the literal dimension and cohort filters. Counts are **observed**; interpreting
wording as planning is **inferred**, brief accounts **creator-stated**, and schema
behaviour **proposed**. No experimentally supported claim is made. Equal-film
means, medians and linearly interpolated quartiles describe the frozen cohort;
pooled shares are beside them. No significance test assumes jobs are independent.

## 4. Findings across the five programme steps

### Step 1 — Technical brief intent and placeholders

Across 118/118 nonempty eligible briefs, the structural parser finds **594
regions**: 67 template-only, 32 mixed candidates, 16 empty and 479 other
unclassified regions. There are 99 distinct-placeholder-within-region matches
across 27/118 briefs. Region counts are parser output, not completed planning
sections or independent plans. A custom-heading region can contain several
conceptual sections. Unknown brief counts remain unavailable in the per-film
output, rather than zero planning.

In the 16 panel cases, code 02.1 is coded for 10/16 and unknown for 6/16; code
02.6 identifies ten substantive, one mixed and five unknown briefs. The extra
unknown in 02.1 is The Kiss: its Context prose does not turn its generic
Production placeholder into a technical plan.

The new extraction has objectives in 5/16, constraints in 6/16, visual intentions
in 9/16, deliverables in 8/16, character preparation/specification in 6/16,
settings in 8/16 and shot/view intentions in 3/16. Another three assignments,
one each for character/setting/shot in Random Access Memories, are label-only.
The remaining 64/112 field assignments are unknown, including 35/112 belonging
to five unavailable briefs. These are scoped positive extractions, not exhaustive
absence claims. Briefs supply technical intention and preparation accounts; they
cannot verify that the declared format or schedule was delivered.

### Step 2 — Scene/shot wording, instructions and organisation

| Observed primary-field feature | Films with a match / 157 | Matched fields / 124,449 nonempty | Mean film share / 157 | Median; IQR / 157 |
| --- | ---: | ---: | ---: | --- |
| Numbered-shot/count or multi-shot lexical marker | 123 | 9,428 (7.58%) | 10.04% | 4.69%; 0.33–11.16% |
| Section marker | 145 | 46,766 (37.58%) | 35.45% | 36.08%; 9.88–53.83% |
| Reference token | 147 | 60,227 (48.39%) | 51.38% | 57.50%; 34.63–70.36% |

All-role film-distinct text gives 7,004 matched / 61,626 film-text pairs. The
same exact text can occur in several films; this denominator is deliberately
not the global distinct-text count. The nested `shot_prompt` role has 19 fields
in 2/157 films; neither figure estimates requested or executed shots.

The folder lexical rule (scene/shot, numbered act, or `Snn:` labels) matches
**350/3,230 folders in 60/157 films**; the equal-film folder share is 9.48%
versus 10.84% pooled. These are navigation labels. Birthdays' numbered “1 The
Corkboard · 1970s” is understood through its case evidence even though that
wording does not match the scene-word rule. No jobs-per-scene or scene count is
derived from this proxy.

Literal `multi_shots=true` occurs in **170/130,704 jobs across 9/157 films**;
false in 36,744/130,704, key absent in 93,781/130,704 and invalid JSON in
9/130,704. The other parameter-document states are measured zero here, but are
supported separately by the parser. Of 9,428 lexical-positive primary fields,
8,981 have false controls (95.26% pooled; 93.83% equal-film mean over the 123
films with positive fields). This is coexisting wording/control scope, not proof
of conflict, achieved cuts or a model failure.

Task is provisionally the literal generation type; semantic operation roles are
pending. Type and literal model comparisons are descriptive:

| Type | Positive fields / nonempty type fields | Mean within-film share (measured films) |
| --- | ---: | ---: |
| Image | 368/87,238 | 0.36% (155) |
| Video | 9,060/37,079 | 25.01% (156) |
| Audio | 0/132 | 0% (10) |
| Text / image_3d / unavailable type | 0/0 in each | Undefined (zero nonempty fields) |

| Literal model, five largest nonempty denominators | Positive fields / nonempty model fields | Mean within-film share (measured films) |
| --- | ---: | ---: |
| seedance_2_5 | 8,162/31,082 | 25.14% (145) |
| nano_banana_2 | 107/25,355 | 0.17% (138) |
| seedream_v5_pro | 202/21,136 | 0.45% (96) |
| gpt_image_2 | 25/14,397 | 0.66% (120) |
| soul_cinematic | 0/6,919 | 0% (63 with nonempty text; 65 with jobs) |

Different tasks, model syntax, language, shared prompts and history capture are
alternatives to any model effect. No provider or model benefit is inferred.
Every literal type/model and cohort, including small subgroups, is retained in
the outputs.

| Cohort | Film denominator | Positive primary fields / nonempty fields | Equal-film mean |
| --- | ---: | ---: | ---: |
| Shortlist only | 62 | 4,060/42,425 | 11.51% |
| Most watched only | 55 | 1,955/29,970 | 5.56% |
| Both | 40 | 3,413/52,054 | 13.92% |

These are observed wording differences within the selected cohort. Duration,
scale, creator overlap, model/task composition, language and missing external
work prevent a causal or quality interpretation. `summaries.csv` carries the
film-level quartiles and exact member sets; no confidence interval implies a
representative sample of creators.

### Step 3 — Brief, entity and shot-to-task maps

[panel_maps.json](outputs/panel_maps.json) contains all **16/16 films**, joining
brief declaration/template evidence, planned entity and scene/shot evidence,
actual task attachments and the local preparation or stated-order evidence.
The 14/16 coded 02.4 entries establish local instruction/task bindings; Dry Aged
Dreams and Titanic remain unknown. A task attachment is observed; the semantic
role is bounded by the case's named instruction. Unresolved asset producers stay
null. No lineage is invented from similarly named objects.

Five paired technical-property spans support **inferred correspondences**:
Birthdays' period specification and 1970s lecture hall; Detour's continuity
objective and Ryu identity binding; Fallen Leaves' naturalistic lighting; THE
LAST TRANSMISSION's single-source lighting; and The Staff's staff texture.
[brief_task_correspondences.csv](outputs/brief_task_correspondences.csv) preserves
both spans and compound task keys. Confidence is moderate: the property recurs,
but independent instructions are a competing explanation. There is **no explicit
documentary brief-node → task-ID binding**, and no completeness/coverage rate for
all planned entities or shots can be measured. The other eleven maps keep that
brief/task correspondence unknown while retaining any observed local bindings.

### Step 4 — What can be said about build order

Of 16/16 case assignments for 02.5, eight infer local reference-first preparation
from named output/input edges (Birthdays, Harmony, KAGEROU, The Kiss, Ivy,
Prophecy, Random Access Memories and SNAP). Three are creator-stated accounts:
Detour, Lost and THE LAST TRANSMISSION; the latter also states entity-first.
Five remain unknown. These counts refer to coded examples, not mutually exclusive
whole-film strategies or representative frequencies.

Reference-first thus has local evidence in several projects, but
nothing establishes its benefit. Character preparation can be part of reference
preparation; the codebook's `entity_first` is broader than character-first. Lost's
“beginning and end” followed by a bridge to the middle is a useful stated order,
but not an executed scene-first sequence. Scene-first, character-first and
exploratory execution rates, relative outcomes and complete build-order shares
are **not allowed by the evidence**. Dates and folder order do not fill that gap.

### Step 5 — Draft schemas and a decomposition contract

[schemas.json](schemas.json) is a **proposed** JSON Schema for brief, scene, shot
and task records, with evidence-bearing claims and explicit state. It records
recurring information needs, not inferred platform tables:

| Record | Proposed minimum information | Traced need |
| --- | --- | --- |
| Brief | Film/brief/version IDs; objectives, constraints, visual intentions, deliverables, planned entities, section states and scene links | Ten substantive panel briefs; The Kiss mixed placeholders; five unavailable briefs |
| Scene | Stable film-scoped ID, declared/reconstructed label, setting/world state, entity bindings, invariants, shot membership and independently evidenced folder links | Birthdays/RAM labels; KAGEROU's missing brief; Ivy room preparation |
| Shot | Scene link, requested order, action, camera, timing, audio, invariants, attached-reference bindings and task links | Ivy six-shot request; Harmony four timed shots; Staff continuation |
| Task | Film/task/version IDs; plan claims, input versions, explicit dependencies, operation, literal model, source field paths, raw controls, candidate IDs and separate review state | Explicit 02.4/02.5 links; false controls beside shot text; unresolved producers |

A scene is an explicitly scoped planned grouping of setting/state and requested
shots. A shot is an explicitly delimited requested view or temporal segment;
ordered framing need not prove an executed cut. A task is an executable request:
one task can request several shots, and a shot may need several tasks. A folder
is a placement/navigation object until evidence supplies a semantic link.

The proposed contract preserves source channel, scope, version and evidence for
each claim. Unavailable/unknown values are null; explicit empty remains an empty
value with its own state. Template/label-only entries cannot become task-ready
specifications. Task dependencies require explicit asset/version links or a
labelled proposal; lexical matches cannot invent lineage. Timing is requested,
controls retain literal model semantics, and reuse cannot set approval. The
schema describes record shape; cross-record film-scope integrity, missing-input
readiness and human approval gates are proposed behavioural requirements, not
implemented workflow software. Studies 03–09 refine their pending semantics.

## 5. Fully traced examples and counterexamples

Every example below joins `case_evidence.csv` by film plus evidence ID. That
ledger carries the exact paths, short excerpts, alternatives, denominators and
confidence; `panel_maps.json` adds all scoped attachment IDs. These are technical
instructions, never assessments of outputs.

1. **Ivy: scene foundation and six-shot task.** Film
   `d305f6e5-b906-49a1-a0c6-75ef7f653ad8`; `dont-poison-ivy:02.1`–`:02.6`.
   The brief states “Stylized 3D animated. No dialogue.” Task
   `407acee9-0585-468c-a544-db7a19ef8003` asks for “6 shots. Total 30 seconds”
   and binds room asset `0020c74f-ff7e-4aa1-8622-521dda43ea41` through reference
   `8dd8b729-2d20-440a-b62a-034af11cf409`, alongside three other references.
   `assets.generation_id` and `asset_usages` also explicitly connect that room's
   producer to task `0df863b8-4eaf-4fb2-ae6b-4ee70071f00c`. Observed attachment,
   inferred local preparation, creator-stated format: three different claims.
   Scope: named records in 553 inspected/exported jobs; no whole-film order.
   Confidence is high for IDs, provisional for planning meaning; the source
   need not have originated in a master plan.

2. **Harmony: costume preparation before a local shot request.** Film
   `2fd725ab-2604-4220-8cca-d332e9de53a2`; `harmony:02.2`–`:02.5`.
   Costume producer/asset `52b4e96b-5ab6-406c-ab3e-54234dbf0961`
   (`nano_banana_2`) conditions
   `1674aeae-dc7c-4605-a504-c048f028d51e`
   (`cinematic_studio_video_4_0`) at
   `params.reference_elements[2].medias[0]`. The task requests four timed
   shots and carries named character/room/wardrobe bindings. Scope: named edge
   within 233 purposively inspected / 1,543 exported jobs. The edge is observed;
   reference-first is a local inference, not verified costume content or
   project order. Alternative: preparation for this task alone.

3. **THE LAST TRANSMISSION: a stated order with no recovered preparation chain.**
   Film `03f596b0-23da-4312-9e58-2e1cc4582348`;
   `the-last-transmission:02.1`–`:02.6`. Brief: “Order of work: assets, then
   stress tests, then the film”. Task
   `0a5dad36-f81f-4a32-a38a-bc7bcd103e7f` names shot
   `TLT_S02_clock_v2`, plate `tlt_deck` and attached asset
   `9264c44d-ad74-4ddc-91fc-4490b55a5b18`. Its “a single practical source”
   corresponds to the brief's “One motivated light source per frame”. Attachment
   is observed; correspondence inferred; order creator-stated. Scope: all 66
   inspected/exported video jobs. Producers remain unresolved, so a missing
   external build is an alternative. Confidence is high in wording/attachment,
   moderate in property correspondence, insufficient for reconstructed order.

4. **Counterexample to lexical absence meaning no shot plan — Fallen Leaves.**
   Film `6659c520-c88e-4ac7-a2c9-f28d8a40c954`;
   `fallen-leaves:02.3` names task
   `0b35d954-ca3d-426c-86c1-caf4c955d7dd`, with “FIRST — CLOSE-UP:” and
   “THEN — FAST WHIP TO A MEDIUM-WIDE:”. The primary lexical rule has
   0/356 matches in this film. This observed ordered framing is nevertheless
   coded a shot list, without claiming an executed cut. Scope: 356/356 job
   contexts; exact wording is strong evidence, its semantic granularity is
   single-coder. Spelled-out/order wording is a competing coverage explanation.

5. **Counterexamples to brief/folder proxies.** The Kiss
   (`655325cc-46d9-4b0b-b03d-d177defa4b3f`, `the-kiss:02.1`/`:02.6`) has the
   generic “Schedule, locations, crew, and logistics.” alongside substantive
   Context; its local reference-to-task bindings do not validate that placeholder
   as a plan. SNAP (`aed4098b-3278-4e5d-a347-24fad9cfb9ae`, `snap:02.1`–`:02.6`)
   has an unavailable brief and two folders, yet task
   `2199ecf1-0186-4958-a24c-024d8ce09c9c` explicitly requests six shots and
   binds actual inputs; sheet producer/asset
   `16536627-0f5a-4ac8-bdb8-b9d43902785a` feeds
   `0d9a690f-3ac3-4886-bb34-fa70159ca8dc`. Scope: 68 inspected / 1,034
   exported jobs. Confidence is high for these links, insufficient to recover a
   missing master plan. Private/external planning remains a competing explanation.

## 6. Planning-pattern catalogue

These are bounded shared practices or proposed responses, not tested best
practices. Failure modes describe evidence/workflow risks, not measured failures.

| Problem / applicability | Method, inputs and sequence | Evidence | Tradeoffs / failure modes |
| --- | --- | --- | --- |
| Establish persistent task context where inputs are disclosed | Request entity/location packages, then bind actual asset IDs to task instructions | Observed edges, inferred local preparation: Harmony, Ivy, SNAP 02.2–02.5 | Added preparation and version decisions; no proven benefit; requested package content/approval unknown |
| Divide a moving sequence within one request | Specify ordered views, boundaries, timing, action, invariants and actual inputs | Observed Ivy/Harmony/Staff/Detour 02.3–02.4 | A job is not one shot; controls can remain false; executed cuts and timing unknown |
| Carry project constraints into local tasks | Preserve both brief and task spans with a labelled same-property correspondence | Inferred five paired examples in brief_task_correspondences | Semantic correspondence is not documented derivation; independent instructions and scope changes can explain similarity |
| Navigate planned settings and stages | Keep scene label and folder ID separately, then require evidence of membership | Observed Birthdays/RAM 02.3; mixed organisation in Study 10 | Repeated labels, copied folders and several placements defeat folders-as-scenes; no executable order follows |
| Plan with missing or mixed brief evidence | Retain unknown/template state while reconstructing only explicit local bindings | SNAP, KAGEROU, The Kiss; observed coverage and case interpretations | Allows partial planning visibility; inventing a master plan or counting generic headings would overstate it |
| Compare preparation strategies | Separate creator-stated sequence, explicit dependency and unknown executed order | Creator-stated Lost/Detour/Transmission versus eight local edge cases | Reference and entity preparation overlap; no defensible ranking or scene-first/exploratory execution denominator |

## 7. Studio-implication table

Every behaviour is **proposed**, awaiting validation. No studio implementation,
architecture change, autonomous agent or measured production benefit is claimed.

| Evidence → requirement or hypothesis | Proposed behaviour | Validation test |
| --- | --- | --- |
| The Kiss template; five unavailable panel briefs → field-level readiness needs evidence | Display declared, reconstructed, unknown, empty, template and label-only states independently; create specifications only from explicit claims | Synthetic mixed brief retains placeholder flag and substantive constraint without marking all sections complete |
| Five technical-property correspondences → intent needs traceable task links | Link each task to a versioned brief/scene/shot claim, showing explicit versus inferred correspondence and scope | Independent reviewers trace paired spans, adjudicate alternate matches and retain unknown where no binding exists |
| Ivy/Harmony multi-shot tasks and false controls → shot and task identity must differ | Support many shots per task and several tasks per shot; retain requested timing and literal controls beside each other | Synthetic six-shot request with false control survives import; job count stays one; no executed-cut claim |
| Explicit preparation edges and unresolved Transmission producers → dependencies require versions and provenance | Bind input IDs/versions to plan roles; distinguish external/unresolved assets from missing tasks; human confirms readiness | Remove producer in a synthetic graph; preserve input and declaration, create no invented preparation task |
| Birthdays/RAM labels and SNAP flat register → scene identity needs independent scope | Store scene state/membership separately from folder placement; show label-only candidates for review | Move/rename folders without changing verified scene membership; a folder alone cannot supply jobs-per-scene |
| Missing order/approval and overlapping strategies → planning order is a proposal until evidenced | Keep stated order, dependency partial order, proposed sequence and explicit human approval separately | Synthetic reorder changes proposed schedule only; further-work reuse never approves a candidate or proves actual production order |

## 8. Unresolved questions and downstream handoff

All provisional definitions and their specific dependencies are explicit:

| Provisional definition here | Boundary / later result needed |
| --- | --- |
| Exact eight-sentence placeholders plus standard-heading regions | Structural flag only; substantive semantics outside the panel require further section coding; Study 04's semantic labels refine instruction interpretation, not unavailable briefs |
| Section, reference-token and multi-shot regular expressions from AF3a | English/format proxies; Study 04 and the pending semantic-label run/agreement refine meanings and misses; the sample alone cannot supply a new census |
| Seven-category brief extraction and five same-property correspondences | Single-coder, bounded technical spans; Studies 03/04 refine entity identity and context/property matching; independent adjudication still needed |
| Task = literal generation type for corpus comparisons | Recorded job type, not operation or model role; Studies 05/06/08 refine routes, operations and roles |
| Planned scene = explicit scoped setting/state grouping; shot = requested view/segment | Neither equals a folder, job or executed cut; Study 06 refines shot-control granularity, Study 07 dependency membership, Study 10 may consume the bounded semantics now |
| Scene-folder lexical proxy | Navigation wording only; Study 10 must join explicit case semantics/membership rather than interpret the proxy as scene counts; later semantic expansion needs source evidence |
| Local reference-first = named preparation output used as input | Partial dependency, not whole project strategy; Studies 03/07 resolve packages/versions/aliases, Study 08 workflow roles, Study 09 revision versus exploration |
| Task input versions, review state and proposed readiness contract | Proposed fields; Studies 03/07 refine identity/version linkage, 09 review/families, 12 synthesis and validation; no inferred approval |
| Brief and catalogue duration remain separate declarations | Study 10 retains catalogue seconds as its existing proxy denominator; Study 06 refines requested clip timing; neither verifies finished duration |

[scene_handoff.csv](outputs/scene_handoff.csv) passes all 16 scoped 02.3 records
and the scene/shot definitions to Study 10, with membership and jobs-per-scene
denominators explicitly unknown. Birthdays' folder key, RAM's folder label and
Transmission's JSON shot ID are different units, even though all were assigned
code value `scene` in their original cases. No code is silently changed or scene
inventory fabricated. Study 10's disjoint-folder pairs remain placement topology;
this study does not retroactively rename them scene handoffs.

Duration discrepancies also remain visible. Detour says seven minutes in its
brief versus 678.375 catalogue seconds; Lost says three minutes versus 202.199365;
Random Access Memories says five minutes versus 324.629333; The Staff declares
18 minutes versus 266.791667. Transmission's 4:31 declaration is close to
271.458333 catalogue seconds but still not independent verification. These
channel differences have no justified single corrected duration and cannot
support comparable-format economics or counts per finished scene/minute.

The evidence does not allow: corpus-wide substantive-plan prevalence; exhaustive
planned entity/scene/shot inventories; complete brief-to-task coverage or omission
rates; executed scene/shot counts; scene membership or jobs per scene; complete
build order or scene-first/character-first/exploratory execution rates; comparative
benefits of planning strategies; timing/continuity/quality assessments; final-use
or approval rates; labour, cost, failure rates, agents or internal orchestration.
The public completed-job history cannot manufacture the missing denominators.
Studies 11/12 receive descriptive measures and testable proposals, not winner
labels, causal claims or an implementation ranking.

## 9. Reusable code, outputs and reproduction

From the repository root:

```bash
uv sync --locked
uv run python scripts/fetch_data.py
uv run python studies/02-planning/build.py
uv run python scripts/fetch_data.py --output data/study02-fresh
uv run python studies/02-planning/build.py --data data/study02-fresh --output data/study02-reproduced --check
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/check_repository.py
```

The fresh downloader verifies all 28 assets. `--check` requires a separate output
directory and compares every generated CSV/JSON byte and the manifest with the
committed build. The reproduction test runs when the verified data is installed;
CI without data explicitly skips integration reproduction and checks synthetic
boundaries plus input/output hashes. Synthetic tests cover mixed/empty templates,
control states, compound joins, primary/nested crosswalk, missing labels and
film/pooled denominators. No real record is a fixture.

| Output | Grain and provenance contract |
| --- | --- |
| [film_metrics.csv](outputs/film_metrics.csv) | 157 film rows, counts/denominators, inherited inferred taxonomy and unusual-project flag; join metric_evidence on film_id |
| [metric_evidence.csv](outputs/metric_evidence.csv) | One full numeric excerpt and whole compound-key source scope per film; query paths, evidence, alternatives, confidence and denominators |
| [summaries.csv](outputs/summaries.csv) | All/cohort/orientation/scale: measured film sets, numerator/denominator, film mean/median/IQR and pooled shares; undefined ratios remain unavailable |
| [by_generation_type.csv](outputs/by_generation_type.csv), [by_model_identifier.csv](outputs/by_model_identifier.csv) | Film × literal dimension counts; source scope is all matching jobs; join film evidence; absent dimension combinations are not additional rows |
| [summary_generation_type.csv](outputs/summary_generation_type.csv), [summary_model_identifier.csv](outputs/summary_model_identifier.csv) | Dimension × cohort plus all: equal-film shares among films with positive text denominators for text measures, jobs for controls; exact members recoverable in corresponding per-film table; unavailable type stays null |
| [brief_sections.csv](outputs/brief_sections.csv) | Film/region index, source character offsets, hash, lengths, template spans and structural state; source films.project_brief; join film evidence; no content-only region is called substantive |
| [brief_fields.csv](outputs/brief_fields.csv) | All 112 panel field assignments, short source spans, states and full evidence metadata; unknown is not semantic absence |
| [case_evidence.csv](outputs/case_evidence.csv) | All 96 unchanged 02.x assignments with case source path and full provenance |
| [panel_maps.json](outputs/panel_maps.json) | All 16 maps, declaration/entity/shot evidence IDs, observed task attachments, inferred local preparation/property links, stated order and unknown links; every link labelled and confidence-scoped |
| [brief_task_correspondences.csv](outputs/brief_task_correspondences.csv) | Five paired brief/task property spans, inferred evidence label and moderate rationale; no documentary derivation claim |
| [scene_handoff.csv](outputs/scene_handoff.csv) | Sixteen original scene/shot code rows, proposed definitions and explicitly unknown membership/scene denominators for Study 10 |
| [structural_audit.csv](outputs/structural_audit.csv) | Deterministic panel positive/negative keys, literal spans and selection denominators; no semantic accuracy claim |
| [reproduction.json](outputs/reproduction.json) | Source manifest SHA-256, hashes of code/SQL/schemas/readings/programme, relevant Study 01 registers, AF3a feature source/summary, case narratives/ledgers/edges, and every generated output |

Every output is below 1 MB and committed beside the code. No `study-02-v1`
release is necessary. Original data, Study 01, case files, prompt-label tools and
Study 10 are unchanged; there is no data-directory exception, full prompt text,
machine-specific path or local user name in the committed outputs.
