# Study 08 — Model roles and workflow

## 1. Answer and evidence limits

The records show **shared sources, chained outputs and cross-model asset handoffs**,
not a recovered scheduler or agent system. Across 157 primary histories the mean
film has 70.89% of jobs sharing an exact media input with another job, 52.71%
consuming a recorded output and 36.92% consuming an output from a different literal
model. Pooled counts are respectively 91,752, 72,863 and 48,631 /130,704 jobs.
These are overlapping dependency patterns, not whole-film strategies, comparable
iteration families or evidence of benefit.

Models serve several recorded operations and requested purposes. Image-conditioned
composition, sheet preparation and local-change requests are traced in the panel;
video-typed jobs also include editor, upscale and voice/transform adapters. A model
name, job type or lexical match alone cannot establish semantic character design,
actual animation, a successful edit or a final master. The [role matrix](outputs/role_matrix.csv)
therefore retains literal types, models, input routes and graph roles beside the
[scoped semantic matrix](outputs/panel_role_matrix.csv). Character design is defined
but its original creation/prevalence is unestablished by the scoped 08.1 assignments;
character-sheet editing is not silently promoted to original design.

Sound and final editing remain only partly visible. Recorded audio/voice adapters,
editor jobs and creator accounts are separate evidence channels. Proposed node
contracts preserve sources, literal controls, requested changes, candidate outputs
and human decisions; proposed planning assistance cannot invent dependencies or
approve its own references. No controlled test establishes a best practice.

Only the selected cohort has detailed records; these findings cannot establish
what separates top films from other films. No source site or media was retrieved
or watched. Story, aesthetics, media quality, continuity, actual screen use,
internal orchestration, agents, labour, cost and failure rates are unassessed.
Every numeric conclusion joins the [metric ledger](outputs/metric_evidence.csv);
case interpretations join the [case ledger](outputs/case_evidence.csv).

## 2. Population, exclusions, coverage, units and denominators

Study 01's unchanged Study 08 eligibility register supplies **157 complete primary
histories**, 62 shortlist only, 55 most watched only and 40 both. The 186-film
priority union also contains 23 excluded non-open-source listings and six unavailable
public workspaces. The supplemental Cosmic tracks pilot contributes to no measure.
The [eligibility copy](outputs/eligibility.csv) retains all 187 priority/pilot rows
and their missing-evidence notes; excluded/unavailable workspaces never become
zero-work projects. All 49 unusual projects remain; no outlier is removed. The
151 creator handles, repeated requests and batches preclude independent-trial claims.

| Unit / gate | Denominator and limitation |
| --- | --- |
| Film and job | 157 films /130,704 compound film/generation keys; every exported type retained |
| Recorded type | 92,058 image, 38,508 video, 132 audio, one text, one image_3d, four unavailable /130,704 jobs; unavailable differs from empty |
| Primary text | 124,449 nonempty, 1,083 empty and 5,172 unavailable /130,704; lexical rates use only nonempty primary fields, never nested copies |
| Material bindings | 307,316 distinct asset/consumer bindings; presets excluded under Study 07; 109,115 have unresolved origin, not proven external creation |
| Resolved job pairs | 198,201 distinct producer/consumer pairs; several assets or role/path occurrences do not add pairs |
| Panel semantics | 16 purposive films × five unchanged 08.x codes = 80 assignments; unequal reading scopes, single coder; not corpus prevalence |
| Raw models and controls | Literal identifier/name/type inventory; raw model, mode, model_version, is_inpaint and generate_audio states retained by film/model; nine invalid parameter strings remain invalid |

All source columns stay strings. CSV/JSON are parsed properly. Within one asset,
raw/preview representations remain one identity; there are no cross-ID semantic
merges. Missing input evidence cannot prove text-only production. Zero relevant
denominators yield unavailable rates, not zero. Film summaries precede pooled job
shares; counts of films, jobs, sources, pairs and occurrences are not interchangeable.

## 3. Method, codebook and checks

[build.py](build.py) uses `film_practice.connect` over checksum-verified
`data-2026-10-20` and [measures.sql](measures.sql). All joins retain film scope.
The build reuses the merged Study 05/06 route functions and SQL, and Study 07's
typed graph function, without modifying them. A producer must be unambiguous and
an existing different job. Both assets.generation_id and exported output usages
are retained by the graph. Self-inputs and conflicting/unresolved origins cannot
create handoffs. Dates, folders, names and prompt similarity add no lineage.

Codebook **1.0**, codes 08.1–08.5, is unchanged. All 80 case rows retain original
values, states, source paths, bounded excerpts, alternatives, denominators and
confidence. Their narratives and ledgers are hashed. All sixteen 08.1 opening
spans are checked against named source tasks; all twelve edge-supported 08.3
examples are rebuilt with literal producer/consumer models and actual material
bindings. Semantic request-role interpretations in the panel matrix are explicitly
**inferred**, even when the original case labels observed wording. They are not
broadcast to the rest of a film or its model's jobs.

The [catalogue](catalogue.json) defines the programme's eight semantic roles and a
closed, provisional mapping of declared adapter operations. It is an interpretation
of literal exported identifiers/names, never provider capabilities or hidden
mechanisms. Models outside that mapping remain unclassified. `video_candidate`
means video-typed jobs outside the listed transform/voice/finish adapters; it
cannot establish animation intent or fresh synthesis. The model inventory keeps
the original names and types beside these interpretations.

| Structural operational definition | Measure / denominator and limit |
| --- | --- |
| No recorded material input | Jobs with no media binding /all film jobs; only a direct-generation candidate, not proven fresh/text-only production |
| Shared-input branch | Jobs consuming an exact material asset with ≥2 distinct consumers /all film jobs; shared context need not be a revision family |
| Chained / convergent | Jobs with ≥1 /≥2 distinct explicit material producers /all jobs; sources need not be distinct semantic entities |
| Cross-model handoff | Different nonempty literal model IDs on an explicit producer/asset/consumer relation; job share /all jobs, pair share /all resolved pairs |
| Reference preparation proxy | Producer jobs whose output is actually consumed through a named reference-element binding /all jobs; misses direct-asset packages; verifies no sheet form |
| Candidate image foundation | Image-producing job consumed through an image-bound role/path by a video-typed job /all jobs and /image jobs; no automatic keyframe timing or screen use |
| Staged refinement proxy | Consumer with a producer that itself has a material producer /all jobs; path depth ≥2, not semantic revision or rescue |
| Finishing proxy | Closed literal editor/upscale/declared-finishing mapping /all jobs, including unavailable job type; no final timeline or acceptance |
| Voice adapter proxy | Closed voiceover/voice-change/lip-sync mapping /all jobs, independent of audio job type |
| Input routes | Exact merged Study 05/06 conservative precedence, prefixed by job type; unknown retained; request text never establishes a mask or an outcome |

Structural prompt features use the unchanged AF3a edit, preservation, reference
and multi-shot regexes. Job-level indicators divide by nonempty primary fields.
The 1,300 structural checks across all 157 films recompute match sums and
distinct-text denominators at the exact
film × literal type × distinct primary text grain against the merged AF3a output.
English vocabulary, quotation, negation and boilerplate limit meanings; no semantic
sample labels were read or assumed. Source-span/edge/count checks are correspondence
checks, not precision/recall, independent agreement or achieved-media validation.

Numeric rows are **observed** under documented rules; role/route interpretations
are **inferred**, creator accounts **creator-stated**, comparisons descriptive
**associations**, and node/studio behaviours **proposed**. No experimentally
supported claim is made. Each numeric output joins film_id to metric_evidence for
full source/query scope, numeric excerpt, competing explanation and confidence;
its literal dimensions select the exact compound entity set. Summary rows are
numeric excerpts from those members. Quartiles use linear interpolation and
describe frozen-cohort variation, not sampling uncertainty or causal effects.

## 4. Findings through the six programme steps

### Step 1 — Roles without invented semantics

All 16/16 scoped 08.1 assignments are coded: composition 9/16, local_edit 8/16,
reference_sheet 4/16, environment 3/16 and animation 1/16; these overlap. They
are a panel-code audit, not the proportions of each film's jobs serving those
roles. Character-reference preparation/editing is explicit in Staff/Lost/Titanic;
original character design is not separately established here. Voice and finishing
receive their own job/adapter audit below instead of inferred semantic prompt labels.

The semantic matrix shows `seedream_v5_pro` in composition/local-edit requests,
`nano_banana_2` in local edits, environmental plates and sheet preparation,
`gpt_image_2` in location-sheet/environment and seat-change requests, and
`seedance_2_5` in a timed animation request. These associations have named tasks
and source controls, not a capability ranking or claim of model specialisation.

### Step 2 — Role-by-model matrix and operation context

`role_matrix.csv` is film × literal type × model × merged route × declared adapter
role, with job and graph-role counts and the film-job denominator. Roles overlap:
a sheet preparation output can also be an image foundation and share sources.
`panel_role_matrix.csv` adds semantic purposes only for the sixteen named tasks.
`model_inventory.csv` independently retains literal model names and counts; names
are never normalised into supposed providers or model versions.

| Literal model | Films with jobs /157 | Chained jobs /model jobs | Mean film chaining share (films using model) |
| --- | ---: | ---: | ---: |
| seedance_2_5 | 145 | 25,732/31,082 | 73.29% (145) |
| nano_banana_2 | 138 | 15,707/25,355 | 45.64% (138) |
| seedream_v5_pro | 96 | 10,754/21,136 | 47.76% (96) |
| gpt_image_2 | 120 | 7,551/14,397 | 46.60% (120) |
| soul_cinematic | 65 | 651/7,696 | 6.09% (65) |

These largest-job models are descriptive examples; every literal model, including
rare and unavailable-type records, remains in the outputs. Means condition on
films using that model; they are not model adoption shares across absent films.
Input interfaces, task mix, repeated requests, history capture, scale, duration
and creator overlap compete as explanations. No comparative effectiveness follows.

### Step 3 — Model transitions versus co-occurrence

An explicit cross-model consumer is visible in **146/157 films**, with
**48,631/130,704 jobs**; mean film share **36.92%**, median **38.31%**, IQR
**20.77–52.24% /157 films**. There are **140,008/198,201 resolved job
pairs** across different literal model IDs; mean per-film pair share **72.44%**
over **147 films with resolved pairs**. Job and pair shares differ because a
consumer may bind several producing jobs. Of 154 multi-model histories, eight
have no explicit cross-model consumer; three other histories have one model.

The largest ordered transition by pair count is `seedream_v5_pro` →
`seedance_2_5`: **30,119/198,201 pairs**, present in **66/157 films**. This is
recorded reuse, not model capability or a preferred router. `cooccurrence.csv`
contains **1,472 distinct unordered model combinations**; only **353/1,472** have
any actual transition in either direction in any film. Across film/model-pair
occurrences, **1,816/7,549** co-occurrences have such an edge. An edge in one film
cannot be transferred to another film where those models merely co-occur.

`transitions.csv` counts distinct producer/consumer job pairs by film and ordered
literal model pair, with consumers, sources, film-pair and film-job denominators.
One consumer with several parents counts in several transition rows, so summing
row consumers is not a unique-job count. `cooccurrence.csv` separately lists
unordered model pairs present in a film and how many such films have an actual
transition in either direction. Co-occurrence cannot supply a missing edge.

### Step 4 — Workflow structures, per film first

| Structural motif | Positive films /157 | Jobs /130,704 | Equal-film mean; median; IQR /157 |
| --- | ---: | ---: | --- |
| No recorded media (direct candidate only) | 151 | 34,962 | 24.34%; 18.67%; 8.70%–35.50% |
| Shared-input branch | 156 | 91,752 | 70.89%; 75.60%; 59.46%–84.58% |
| Output chaining | 147 | 72,863 | 52.71%; 58.06%; 35.91%–75.84% |
| Convergence | 140 | 42,390 | 30.56%; 30.43%; 11.90%–48.07% |
| Depth-two stage (refinement proxy) | 140 | 53,175 | 36.10%; 36.00%; 13.29%–54.87% |
| Cross-model consumer | 146 | 48,631 | 36.92%; 38.31%; 20.77%–52.24% |
| Named-reference preparation source | 100 | 3,930 | 3.78%; 2.41%; 0.00%–5.58% |
| Image source used by video | 143 | 8,076 | 8.13%; 6.39%; 3.18%–11.08% |

These motifs overlap; they are not mutually exclusive film archetypes. The
reference-preparation measure requires a named element binding and misses direct
packages such as Titanic. Its branch is observed despite having no local producer.
A depth-two path establishes stages, not refinement intent, failure, benefit or
whole-film order. No-recorded-media jobs can include omitted sources and presets;
they cannot establish a complete direct workflow. The six qualitative workflow archetypes in
[catalogue.json](catalogue.json) and section 6 supply bounded semantics and explicit alternatives.

| Cohort | Films; jobs | Shared-input jobs /jobs; mean film share | Cross-model jobs /jobs; mean film share |
| --- | --- | --- | --- |
| Shortlist only | 62; 45,497 | 30,331/45,497; 68.15% | 18,096/45,497; 37.92% |
| Most watched only | 55; 31,169 | 23,201/31,169; 74.00% | 11,521/31,169; 33.50% |
| Both | 40; 54,038 | 38,220/54,038; 70.84% | 19,014/54,038; 40.07% |

These cohort differences are descriptive associations within the selected records.
Model/operation mix, capture, scale, duration, repeated creators and requests remain
competing explanations; no significance test treats jobs as independent films.
Orientation and scale splits in the outputs retain Study 01's thresholds, including
all outliers. They describe history composition and recorded workload only.

### Step 5 — Audio, voice and editing visibility

There are **132/130,704 audio-typed jobs in 10/157 films**: `seed_audio`
127 jobs in seven films and `text2speech_v2` five in three films. These literal
job records are observed; complete voice/sound production is not. There are also
53 video-typed `voice_change_merge` jobs in ten films, two `dubbing_lipsync`
jobs in two and one `sync_so` job in one. The closed voice-adapter proxy totals
**61/130,704 jobs in 14/157 films**, mean film share **0.08% /157**; it overlaps
with five audio jobs and must not be added to 132 as disjoint audio work.
The one `speech2text` record is text-typed, with transcription inferred from its
literal identifier/name; it is not counted as audio synthesis.

The finishing proxy totals **1,358/130,704 jobs in 80/157 films**, mean film
share **1.57% /157**. It includes 789 `cinematic_video_editor` jobs (785 video,
four unavailable type), 423 `topaz_video`, 74 `flux_video_upscale` and 72
`bytedance_video_upscale` jobs. Literal Topaz naming is retained as declared
finishing, without assumed scale factors. An editor job still counts when its
primary text or job type is unavailable. None establishes a final master.

The panel's 08.5 audit has ten assignments with `job_observed` /16 films (Detour also
has a creator-stated external account), two creator-stated-only assignments and
four unknowns. Lost states “Edited using capcut.”; Transmission states scan lines
were laid in post. Detour's Photoshop/Premiere/Suno account stays creator-stated.
Prophecy's separately reported voice/assembly tools do not replace literal job IDs.
Sound instructions in video prompts are not audio-job counts, and generated-audio
controls do not establish usable sound. Most of the final sound/edit process and
its handoffs remain unobservable; no complete external-process denominator exists.

`adapter_examples.csv` gives one sorted source job per mapped adapter with typed
bindings, exact literal controls, model/name/type excerpt, full film/job IDs,
alternative, denominator and confidence. It includes voiceover, audio generation,
voice change, lip-sync, transcription and editing/finishing, without copying scripts
or claiming that the chosen record represents a complete production.

### Step 6 — Node contracts and proposed orchestration

[node_contracts.json](node_contracts.json) specifies common identity, evidence,
versioned input bindings, context, literal adapter parameters, candidate outputs
and separate review records; five operation contracts cover reference preparation,
image construction/editing, video generation/transforms, voice/audio and finishing.
These are **proposed information and behaviour contracts**, not an implemented
execution/persistence architecture or a reconstruction of platform internals.

Code can deterministically validate compound keys and states, bind explicitly
chosen sources, record outputs and enumerate known downstream review candidates.
Humans choose identity/variants, reference authority, role/model suitability,
branch adoption, changes and approval. A planning model might propose decomposition,
role/model candidates and context gaps with evidence; human decisions and code
validation constrain those proposals. The archive supplies no evidence that a
planning model was used, no routing policy and no benefit estimate. Study 12 must
test this proposal; Study 09 refines comparable families and bounded review/retry.

## 5. Fully traced examples and counterexamples

Every example joins its evidence_id and full film key in `case_evidence.csv`;
`handoff_examples.csv` rebuilds the twelve named cross-model links, and
`panel_contexts.json` retains actual inputs and raw controls for the role/finish
jobs. Confidence is high in exported compound keys and exact spans, bounded and
single-coder for semantic interpretation. Instructions are never outcomes.

1. **Birthdays — composition/editing across still models.** Film
   `d51d6821-d191-40f7-949b-1086750a2e93`, `birthdays:08.1`/`:08.3`/`:08.4`.
   Producer/asset `37f689e1-04da-473c-9778-97b61732ec90` (`seedream_v4_5`)
   feeds `372eae81-9e4e-4264-adac-febf9565667e` (`seedream_v5_lite`),
   input_image at `params.medias[0].data`; separate logo asset
   `b38a38ab-607f-4228-93ee-f2d940fdb20f` binds at `params.medias[1].data`.
   “Embross the logo” is observed wording; composition/local editing is inferred.
   Denominator: one named task within 170 inspected /1,003 exported jobs.
   Alternative: new multi-conditioned candidate rather than a layered or approved
   revision; four requested views versus three panels remains unresolved.
2. **Fallen Leaves — preparation into a video reference.** Film
   `6659c520-c88e-4ac7-a2c9-f28d8a40c954`, `fallen-leaves:08.1`–`:08.4`.
   Asset/producer `1cba062c-b6c5-456d-929d-b958859ae105` (`gpt_image_2`)
   feeds `023fadcd-4fdd-46b9-98f4-1b940839b4c7` (`seedance_2_5`) as
   reference_image at `params.reference_elements[0].medias[0]`.
   The separately named role job requests “Location reference sheet”; this is
   environment/sheet intent, not a media observation. Denominator: one named
   producer/consumer link; all 356/356 job contexts inspected and all assets/usages
   searched. Alternative: reference context rather than a start frame; no global
   workflow order or successful animation is established.
3. **APEIROPHOBIA — synthesis to an editor.** Film
   `c3d8ee5e-b119-4654-99f9-c6545f650635`, `apeirophobia:08.3`–`:08.5`.
   Producer/asset `88160a68-3dd4-4662-be7e-4fb5852634c5` (`seedance_2_5`)
   feeds `b6e44e77-d4a0-4821-9663-55a452fffc01` (`cinematic_video_editor`)
   as input_video at `params.medias[1].data`; the editor also binds start image
   `b4a29f34-99b8-424c-b9bf-fe425c0e0b8c` and records duration=7.
   Denominator: one named edge within 63 purposively inspected /6,862 exported
   jobs; all assets/usages searched for the link. Edge/controls observed, finishing
   role inferred. Alternative: an intermediate candidate, not a final timeline,
   master, approved cut or internal routing policy.
4. **SNAP — finishing despite empty text.** Film
   `aed4098b-3278-4e5d-a347-24fad9cfb9ae`, `snap:08.5`; full task ID is in
   the ledger/context. Literal `bytedance_video_upscale` task records resolution
   `2k`, an explicitly empty primary field and asset
   `4be1fff0-9862-45e7-8725-d1eea18d983c` under two input_video paths,
   `params.medias[0].data` and `[1].data`. Denominator: one task within
   68 inspected /1,034 exported jobs; two usage occurrences mean one source.
   Observed operation/bindings, inferred finishing; no enlargement, output quality
   or final use was verified. This counters dropping empty-text jobs from roles.
5. **Counterexample — Dry Aged Dreams.** Film
   `3777eda4-c15e-4531-9f04-4c02a900f3c3`, `dry-aged-dreams:08.1`–`:08.5`.
   `nano_banana_2` has one image job, `seedance_2_5` ten video jobs /11;
   all 11 usage rows are outputs, with zero non-output bindings. The named image
   task's FOREGROUND/MIDDLE GROUND/BACKGROUND wording supports an inferred
   environment purpose. Co-occurrence is observed; workflow shape and finishing
   remain unknown. Alternative: omitted/external preparation. A complete crawl
   cannot supply a missing handoff or establish text-only production.
6. **Counterexample — The Staff.** Film
   `3b09c7c2-3f0c-48e3-8304-fad569bf50ce`, `the-staff:08.3`/`:08.4`.
   Three models co-occur /82 jobs, but the only resolved pair is
   `0e619b88-43ef-4a45-84c3-b7b86ac96fe4` →
   `1d963033-bc45-495d-9bfa-a05e4d0cf918`, both `seedance_2_5`, through
   input_video at `params.medias[1].data`. All 82 jobs, 121 assets and 462 usages
   were searched. One stage is observed; a cross-model handoff is not established.
   Alternative: undisclosed preparation, not absence of model division in reality.

## 6. Pattern catalogue

[catalogue.json](catalogue.json) supplies problem, method, inputs, sequence,
evidence/label, tradeoffs, failure modes and applicability for all six patterns.
Failure modes concern evidence interpretation or proposed use, not measured job
failures; recurring practice is not tested best practice.

| Problem / applicability | Inputs and sequence | Evidence / interpretation | Tradeoffs and failure modes |
| --- | --- | --- | --- |
| A direct request has no preparation edge | Text/raw controls → candidate; retain unknown sources | Dry Aged Dreams 08.3/08.4; inferred direct candidate only | Simple disclosed topology can hide substantial external work; do not claim text-only |
| Prepare a reusable source then generate | Produced source → typed reference/input → new task | Fallen Leaves/Kiss/Lost 08.3; observed links, inferred local preparation | More version/authority decisions; reference need not be a verified sheet or frame |
| Branch alternatives from common context | Exact source → ≥2 consumers → proposed human choice | Titanic/Transmission 08.4; observed branch | Shared context is not a comparable revision family; frequency does not approve candidates |
| Refine through stages | Producer → derivative → further task where disclosed | Birthdays/Detour 08.3 and Ape editor path; inferred procedural intent | Path depth does not establish motive, difficulty, benefit or accepted versions |
| Hand off across literal models | Producer model → asset → different consumer model | Ape/SNAP/Birthdays 08.3; observed transition | Requires explicit binding; model count/co-occurrence cannot imply routing or agents |
| Retain external finishing boundaries | Known jobs plus separately sourced creator account | Lost/Detour/Transmission 08.5; creator-stated external work | Cannot recover missing timeline, complete sound stack or final acceptance |

## 7. Studio implications — proposals to validate

All rows are **proposed**, awaiting validation. None is an observed platform
architecture, implemented studio workflow or demonstrated production benefit.

| Evidence → requirement or hypothesis | Proposed behaviour | Validation test |
| --- | --- | --- |
| Staff/Dry co-occurrence without a cross-model link → transitions need explicit provenance | Show model inventory separately from producer/asset/consumer bindings; preserve unresolved origins | Synthetic co-occurrence with no edge remains unresolved; adding one typed material edge creates exactly that handoff |
| One model has several purposes; video type includes transforms → task role and adapter capability need separate fields | Store requested role/evidence, recorded route, literal ID/version state and raw controls independently; unknown mappings stay unresolved | Round-trip a sheet edit, voice-change video and unavailable-type editor without changing raw types or inventing masks/defaults |
| Birthdays sources converge; SNAP duplicates a source → node inputs need compound/version identity and exact channel roles | Bind immutable source versions; deduplicate consumers for counts while retaining all role/path occurrences | Synthetic cross-film collisions and duplicate channels preserve distinct identities and exactly one source per raw ID |
| Ape editor and partial external audio statements → candidate and finishing records cannot imply final approval | Record outputs/use history beside separate actor/version/scope-backed review and external-process statements | A reused editor candidate remains approval-unknown; a tool mention creates no missing job or final timeline |
| Branched/staged motifs overlap → deterministic execution should follow explicit choices | Validate bindings and caps, record results, enumerate downstream review causes; humans choose continuation/revision | Synthetic branch/diamond preserves provenance and bounded review; no automatic invalidation or rerun from depth alone |
| Planning and context gaps recur → planning-model assistance is a product hypothesis | Model proposes decomposition/role/context with evidence; human approves, code validates IDs/control mappings | Compare assisted and human-only plans on fixed tasks with declared rubric, repetitions, budget and independent adjudication |

## 8. Provisional definitions, unresolved measures and downstream handoff

Every provisional definition used here and its specific dependency follows. A later
study cannot manufacture absent media, private work, prices, decisions or outcomes.

| Provisional definition | Later study / remaining limit |
| --- | --- |
| Semantic role = inherited named 08.1 request interpretation; character design distinct from sheet/edit reuse | Study 04 semantic components, sample exclusions/agreement and context matrix; original design and corpus purpose prevalence remain unknown |
| Adapter role = closed literal identifier/name mapping; video_candidate = video type outside mapped transforms/voice/finish | Study 04 context and Study 12 adapter validation; actual implementation/defaults/capabilities are not recoverable |
| Input route = unchanged Study 05/06 conservative rules; no-recorded-media = direct candidate only | Study 04 information location and Study 09 family context may refine intent; complete fresh/text-only histories remain unknowable |
| Reference preparation = produced output actually bound through a named element; image foundation = image output bound as image to video | Study 04 context/purpose and Study 09 use/approval; direct packages and reference-vs-frame timing remain distinct; no verified sheet/keyframe |
| Branch = ≥2 consumers of exact raw material input; chained/convergent/cross-model = explicit material parents | Study 04 identity/context and Study 09 comparable families/revision intent; no semantic cross-shot equivalence, motive or benefit |
| Staged refinement = parent with its own parent, depth ≥2 | Study 09 named instruction/input deltas and comparable families; structural staging alone is not refinement, rescue or retry |
| Raw/preview variants within one asset stay one ID; no cross-ID merges; unresolved origins retained | Studies 04/09 may refine property/derivative meaning, but absent alias evidence remains absent |
| Edit/preservation/reference/multi-shot wording = unchanged AF3a lexical indicators | Study 04 semantic labels with agreement and exclusions; English structural matches are not semantic census labels |
| Orientation ≥70% image/video else mixed; scale <200, 200–999, 1,000–2,999, ≥3,000 jobs | Study 01 inherited structural thresholds; Study 12 synthesis may consume context, never economic or quality meanings |
| Node fields, deterministic paths, human choices, planning assistance and explicit review/attempt caps | Study 09 family/review refinement and Study 12 synthesis/controlled tests; proposal only, no execution/storage design chosen |

**Resolve upstream dependencies without rewriting earlier reports:** Studies 02/03
receive bounded task roles and asset-backed preparation/handoff patterns; task,
shot and semantic character/element identity remain distinct. Studies 05/06 receive
literal adapter roles beside unchanged conservative routes: editor/voice/transform
jobs cannot be treated as fresh synthesis, a reference image remains a candidate
foundation and unsupported mechanisms/defaults stay unknown. All 8,076 candidate
image foundations reproduce. Study 07 receives roles on disclosed graph motifs,
not a new lineage graph, semantic alias merge or observed review effect. Its
shared/chained/convergent/cross-model job counts reproduce for every primary film.
Study 10 receives operation context and explicit model handoffs, but an author ID
on such an edge still cannot establish human responsibility transfer, semantic
specialisation, team structure or labour division. These dependencies are resolved
only at those scopes; no source or upstream result is silently changed.

Study 09 receives explicit stages and shared-input candidates, with revision intent,
comparable-family equivalence and approval unresolved. Study 04 remains pending by
owner choice; no unavailable model labels were used. Studies 11/12 receive descriptive
cohort counts and testable proposals, not winner labels or an implementation ranking.

**Measures the evidence does not allow:** corpus-wide semantic character-design,
reference-sheet, environment, composition, local-edit or animation prevalence;
complete executed pipelines/build order; proven fresh/text-only/direct workflow
rates; semantic cross-shot/version/alias families; complete audio/external-edit
inventories or final timelines; automatic keyframe timing or final screen use;
actual control effects/defaults, masks/layers from wording; role/model/route benefit,
quality, continuity, verified preservation or tested best practices; approval/final
acceptance, failure/retry/rejection rates; human responsibility transfers, labour,
cost, speed or productivity; hidden routing, scheduler architecture or agents.
No comparison with the uncollected catalogue is supported.

## 9. Code, outputs and reproduction

Run from the repository root:

```bash
uv sync --locked
uv run python scripts/fetch_data.py
uv run python studies/08-workflow/build.py
uv run python scripts/fetch_data.py --output data/study08-fresh
uv run python studies/08-workflow/build.py --data data/study08-fresh --output data/study08-reproduced --check
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/check_repository.py
```

`--check` requires a separate output directory and compares every generated byte,
including the reproduction manifest. The reproduction test runs when the snapshot
is present; CI without source data explicitly skips it and runs synthetic boundaries
and committed-artifact/input hashes. No actual source record is copied into fixtures.
Tests validate analysis code and artifact contracts, not the proposed studio.

| Output | Grain / measure and provenance contract |
| --- | --- |
| eligibility.csv | All Study 01 Study 08 priority/pilot rows and missing evidence; only 157 eligible primary films measured |
| film_metrics.csv; metric_evidence.csv | 157 per-film rows and numeric excerpts; study, full compound entity scope, source/query path, observed label, denominator, competing explanation and confidence; inherited taxonomy flags remain inferred |
| role_matrix.csv; model_inventory.csv | Film × literal model/type/route/adapter with job/graph-role counts; inventory retains literal display names; film-job denominator and metric-evidence scope; requested semantic roles remain separate |
| by_model_identifier.csv; by_generation_type.csv; by_route.csv | Film × literal dimension counts and within-stratum jobs/nonempty text denominators; route prefixed with type; joins film evidence |
| summaries.csv; summary_members.json; summary_*.csv | All/cohort/orientation/scale film mean/median/IQR beside pooled numerator/denominator; exact outer film sets in summary_members, measured members have positive denominator_name; model/type/route summaries condition on users recoverable from matching per-film rows and cohort filters |
| transitions.csv; summary_transitions.csv; cooccurrence.csv | Ordered edge-supported model transitions by film; model-pair summaries include zero contributions from other films with resolved pairs; eligible films include all cohort members, measured means require positive pair denominator. Unordered co-occurrence retains exact film sets and actual-edge film counts; no implied routing |
| controls_*.csv | Film × literal model × parameter/state/exact scalar JSON; jobs/model-job denominator; containers retained as states without text; raw semantics beside classification |
| case_evidence.csv; panel_assignments.csv; panel_role_matrix.csv | All 80 unchanged 08.x assignments; audit counts /16; inferred semantic matrix joins full evidence_id/film provenance |
| handoff_examples.csv; panel_contexts.json; adapter_examples.csv | Rebuilt named links and contexts plus one sorted record per mapped adapter; compound IDs, literal bindings/controls and full evidence metadata or case-evidence join; unknown media/final use preserved |
| structural_check.csv | Every film/type/feature match sum and distinct-primary-text denominator compared with original AF3a grain; lexical correspondence only |
| reproduction.json | Source manifest hash, code/SQL/catalogue/contracts/governance/upstream and case narrative/ledger hashes plus every generated output hash; no machine paths, times or usernames |

Numeric summary rows are their own excerpts; sources are the corresponding
per-film rows and hashed build/query. Literal dimensions or source IDs restrict the
film evidence scope to exact compound keys selectable in the original release.
For example, a transition row selects that film and its producer/consumer models
on the explicit material graph; controls select that film/model/key/state/value.
Every measure retains its denominator and does not count usages as independent jobs.

Local validation passed: Ruff lint and format checks, **158/158 tests**, the
repository boundary/original-hash check, and **all 29 outputs reproduced byte for
byte from an independent fresh fetch** of all 28 verified source assets. All
**1,300 structural checks** matched original-grain counts and text denominators;
the four merged graph indicators matched for every one of 157 films. The largest
output is **657,245 bytes**.

All outputs are under **1 MB** each, committed without full prompts; no
`study-08-v1` release is needed. Original data, programme, Study 01, case files,
prompt-label tools and other studies are unchanged. No data-directory file,
machine-specific path or local user name is introduced.
