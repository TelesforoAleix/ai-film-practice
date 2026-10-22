# Study 07 — Lineage and cross-shot reuse

## 1. Answer and evidence limits

Creators reuse shared sources and chain generated outputs, often together.
Across 157 eligible primary histories, the average film has **70.89% of jobs
sharing a media input with another job**, **52.71% consuming a recorded output**,
and **50.60% doing both**. The corresponding pooled counts are
91,752, 72,863 and 70,660 / 130,704 jobs. These are disclosed dependencies across
jobs, **not counts of shots, semantic identities or successful continuity**.

Raw/preview representations can be resolved **within an asset record**:
118,429/150,835 asset records explicitly group raw/min objects. The release
supplies no cross-ID source links or equal representation-URL groups under the
specified audit. Cross-ID semantic equivalence remains unknown. High-degree
sources are observable; project-wide canonical approval is not. Nine of sixteen
panel authority assignments establish only task/property-scoped declarations.

A changed source has a bounded, computable review surface. All thirteen previously
enumerated panel descendant sets reproduce exactly; the other three cases lack
a producer-root set. Reachability identifies candidates for review, never which
outputs would visibly change, require regeneration or lose approval. The proposed
response is immutable input/version provenance, scoped canonical declarations
and explicit human change review, specified in [invalidation_policy.json](invalidation_policy.json).

Only the selected cohort has detailed histories; these findings cannot establish
what separates top films from other films. No media or source site was retrieved
or watched. Story, aesthetics, media quality, visual continuity, final screen use,
agents, internal orchestration, labour, cost and failure rates are unassessed.
No controlled benefit or experimentally supported best practice is claimed.

## 2. Population, exclusions, coverage, units and denominators

Study 01's unchanged eligibility register gives **157 primary Study 07 films**:
62 shortlist only, 55 most watched only, 40 both. The 186 priority union also
contains 23 excluded non-open-source listings and six unavailable workspaces.
The supplemental Cosmic tracks pilot contributes to no measure. All 49 unusual
projects are retained. The 151 creator handles, repeated requests and batches
mean films/jobs are not independent trials.

| Unit or coverage | Denominator and boundary |
| --- | --- |
| Recorded jobs | 130,704 compound film/generation keys; all types retained |
| Recorded assets | 150,835 compound film/asset keys in those films; includes covers, finals, thumbnails and unused records, not solely production inputs |
| Recorded reference elements | 5,200 compound film/reference keys in 120/157 films; no authenticated library census |
| Usage occurrences | 468,778; output, media, preset and unknown roles kept separately |
| Raw non-output asset IDs | 29,906; 20,869 recur across consumers, reproducing Studies 03/10 |
| Material input IDs | 29,321 in 156/157 films after preset exclusion; 20,383 have at least two consumers |
| Distinct material asset/consumer bindings | 307,316; 198,201 resolve a different existing producer; 109,115 have unresolved producer origin |
| Primary text | 124,449 nonempty, 1,083 empty, 5,172 unavailable /130,704 jobs; lexical rates use nonempty only |
| Panel semantics | All 16 films × five 07.x assignments = 80; plus all sixteen 03.6 authority assignments; single coder, unequal purposive reading scopes |
| Full graph | 286,739 nodes and 737,400 typed provenance-edge rows; every node retained, including disconnected records |

All source columns remain strings. Missing origins are not proof of external
creation or text-only generation. No unavailable workspace is a zero-work film.
Zero eligible text/input denominators produce unavailable rates (`\N`), not zero.
The [eligibility copy](outputs/eligibility.csv) retains the primary, supplemental,
excluded and unavailable registers and their missing-evidence notes.

## 3. Method, codebook and checks

[build.py](build.py) loads only the verified `data-2026-10-20` release through
`film_practice.connect`, using [measures.sql](measures.sql). All joins are
compound film/entity joins. Codebook **1.0**, codes 07.1–07.5, is unchanged.
Existing case labels/unknowns/excerpts are preserved with their original study,
full IDs, paths, competing explanation, denominator and confidence. Scope and
authority claims remain distinct from the observed graph.

**Graph construction.** Generation, asset and reference are distinct node kinds.
Produced-asset edges come from `assets.generation_id` and output usages, with
source channels retained separately. An unambiguous existing producer is needed
for traversal; conflicts and self-inputs are counted and excluded from the
projected generation graph. There are **0 conflicting producer assets /150,835
asset records**, **0 self-inputs /307,316 material bindings**, and **0 cyclic
jobs /130,704** here. The implementation nevertheless handles all three.
Dates, names, filenames, prompts and folders add no inferred lineage.

Non-output roles other than generic `input_asset` are material inputs. Generic
inputs are material only at enumerated image/video/audio paths, following the
merged image/video studies. Camera/style/lens/light/pacing/genre/era/preset paths,
including nested multi-prompt presets, are retained as **preset_input** edges.
The other generic paths remain **unknown_input**. Raw role and parameter path
always accompany the classification; no control value is translated or inferred.
This excludes 30,377 preset occurrences /468,778 usages in 100/157 films;
unknown-input occurrences are 0/468,778. Distinct consumers, parents and binding
sets deduplicate repeated role/path channels, independently of occurrence counts.

Reference metadata `medias`, `video_medias` and `audio_medias` ID entries create
**groups_media** edges; actual usage reference IDs create **reference_binding**
edges. Grouping is descriptive, not an executed dependency. Material propagation
uses only producer → asset → actual media consumer. A changed reference uses its
actual reference-bound consumers followed by the same generation traversal.
No membership-only edge invents a consumer. All recorded nodes remain even when
unused; metadata/usage-only stubs are supported. In this snapshot missing asset
records are **0/29,906 raw input IDs**, missing reference records **0/5,200 used
reference IDs**. Every external-or-unresolved input remains a node without an
invented upstream generation.

**Representations.** JSON is parsed properly; unavailable, empty, invalid,
non-object and object states remain distinct. All 150,835 asset metadata fields
are valid objects. An asset's explicit raw/min/h264/hls objects are representations
of that single exported asset, never extra identities. The audit counts nonempty
`source_asset_id` links and exact equality of nonempty representation `url` fields
across different asset IDs within a film; both are zero under this rule. It does
not inspect generic URL fields, infer aliases from filenames, strip suffixes or
compare media. Zero matches cannot prove distinct semantic identities. No
cross-ID merges are performed. The nine malformed generation parameter strings
identified by Study 01 remain unrepaired; independent usage records still count.

**Operational measures and denominators.** These are transparent structural
rules, not inferred production outcomes:

| Measure | Numerator / denominator |
| --- | --- |
| Shared-input branch / shared ancestor | Jobs using an exact material asset with ≥2 distinct consumers / all film jobs; common asset ancestry does not require a known producer |
| Output chaining | Jobs with ≥1 different, unambiguous recorded material-input producer / all film jobs |
| Hybrid | Jobs satisfying shared-input and chaining rules / all film jobs; film strategies are not exclusive |
| Convergence | Jobs with ≥2 distinct material-input producers / all film jobs; not number of semantic objects or layers |
| Cross-model reuse | Jobs with ≥1 explicit producer of a different non-null literal model ID / all film jobs; unavailable model never establishes a difference |
| Asset recurrence | Material asset IDs with ≥2 distinct consumers / distinct material input IDs; measured in 156 input-bearing films |
| Producer resolution | Distinct material asset/consumer bindings with a different resolved producer / all such bindings; measured in 156 films |
| Reference hub | Maximum distinct actual reference consumers within a film; ties use sorted ID; denominator all used reference IDs and film jobs |
| Material hub | Maximum distinct media consumers of an asset, including unresolved origins; denominator all material input IDs and film jobs |
| Review surface | Unique direct consumer jobs plus transitive generation descendants / all film jobs; changed generation root itself excluded |
| Disconnected parts | Weak components over all nodes: material edges only versus all typed edges; isolated nodes and component sizes retained |
| Preservation/reference wording | Primary fields matching unchanged AF3a regex / nonempty primary fields; instruction vocabulary only |

Structural checks recompute the unchanged AF3a regex match sums at the exact
**film × literal type × distinct primary text** grain, asserting equality for
all 157 films before job weighting. A text shared across types contributes once
in each type for that check. These are correspondence checks, not semantic
accuracy or independent agreement. Quoting, negation, language and boilerplate
limit meanings. No model semantic labels are available or used; Study 04 owns
that refinement. The inherited cases supply semantics a script cannot decide.

Every numeric row joins [metric_evidence.csv](outputs/metric_evidence.csv) on
film ID for study, exact whole-table compound-key scope, query/code path,
numeric excerpt, alternatives, denominators and confidence. Additional rows
restrict that scope by their literal dimension or node ID. Counts are **observed**;
semantic strategy/identity interpretations **inferred**; source declarations
retain their original labels; policy and studio behaviours **proposed**. Aggregate
excerpts are the numeric rows themselves, sourced to their member per-film rows.
Equal-film means, medians and linearly interpolated quartiles precede pooled
rates. Variation describes this frozen cohort; no sampling interval or causal
comparison treats jobs as independent observations.

## 4. Findings through the five programme steps

### Step 1 — Typed graph and disconnected disclosure

The full graph preserves **130,704 generation +150,835 asset +5,200 reference
nodes**, with all typed edges in the public release. There are **46,499 weak
material components /286,739 nodes** and **24,774 all-edge components /286,739
nodes** across 157 film graphs; per-film medians are respectively **170 and 85
components /157 films**. The material projection intentionally leaves reference
nodes isolated; its **11,796 isolated nodes /286,739** include these descriptive
records. Component counts are disclosure topology, never a count of scenes,
independent workflows or production teams. Covers/finals and undisclosed work
also explain disconnected records.

### Step 2 — Hubs, branches, common ancestry, convergence and model boundaries

| Structural measure | Positive films /157 | Pooled numerator /denominator | Equal-film mean; median; IQR |
| --- | ---: | ---: | --- |
| Media-bound jobs | 156 | 95,742/130,704 | 75.66%; 81.33%; 64.50–91.30% (157 films) |
| Shared-input jobs | 156 | 91,752/130,704 | 70.89%; 75.60%; 59.46–84.58% (157) |
| Chained jobs | 147 | 72,863/130,704 | 52.71%; 58.06%; 35.90–75.84% (157) |
| Convergent jobs | 140 | 42,390/130,704 | 30.56%; 30.43%; 11.90–48.07% (157) |
| Cross-model jobs | 146 | 48,631/130,704 | 36.92%; 38.31%; 20.77–52.24% (157) |
| Reused material input IDs | 156 | 20,383/29,321 | 69.08%; 70.25%; 56.97–81.89% (156 input-bearing films) |
| Resolved material bindings | 147 | 198,201/307,316 | 59.24%; 67.08%; 31.35–90.57% (156) |

A common asset can be external/unresolved, or produced within the film. These
shared-ancestor counts include both. They do not identify common characters,
world rules or semantic sameness. The alias audit above resolves representations
only where explicit; the counts remain compound raw-asset counts.

[hubs.csv](outputs/hubs.csv) records a deterministic maximum-degree material
asset and reference per film, with full keys and provenance. For example,
APEIROPHOBIA asset `36b6dccd-9a13-4ecc-81ab-835e6333e15d` has **1,602 direct
consumers /6,862 jobs** and **2,803 reachable consumers /6,862**. Detour's
`006dcc36-ec37-490f-9890-9524e3ed0ddd` has **1,127/6,162 direct** and
**1,310/6,162 reachable**. These are observed hubs, not rankings of source quality
or canonical authority. Repeated candidates, broad shared contexts and capture
scope are competing explanations. Every lower-degree source remains in the
release census; no inference is made from popularity.

### Step 3 — Shared sources versus chaining and scoped authority

The structural strategies overlap: **70,660/130,704 jobs** are hybrid, equal-film
mean **50.60%**, median **56.63%**, IQR **35.31–71.19% /157 films**.
Shared-input-only is **21,092/130,704**, chaining-only **2,203/130,704**, neither
**36,749/130,704**. The last group includes presets and unknown disclosure;
it cannot be labelled reference-free or text-only. These differences are
arithmetic on the overlapping per-film indicators, not exclusive film archetypes.

All 16 case files retain raw/min grouping; 15/16 have a named branch example;
13/16 code previous-output chaining and 2/16 shared reference in their scoped
07.4 assignment; Dry Aged Dreams is unknown. Those are case-code audits, not
representative prevalence. Nine coded /16 authority assignments (03.6) declare
property/task authority, seven remain unknown. No project-wide canonical-version
register or canonical-versus-chaining effectiveness denominator is established.
Frequency cannot supply that missing decision. The continuity-strategy catalogue
therefore compares **observed bindings**, **inferred continuity intent** where
text supports it, and **proposed canonical management**, separately.

### Step 4 — Estimate downstream review after change

[review_summary.csv](outputs/review_summary.csv) describes each film first;
`review_census.csv.gz` enumerates every material-input asset and every used
reference with direct and reachable job counts. Among 156 input-bearing films,
the median of per-film median asset review surfaces is **4 jobs /156 film
medians**. The median maximum asset review surface is **167 jobs /156 film
maxima**; maximums must not be summed as independent affected outputs. Among
120 reference-bearing films, the corresponding medians are **12 and 138 jobs
/120 film summaries**. Every census row supplies its own film-job denominator.
These are hypothetical changes at each root, not observed change events or
expected regeneration workload.

The largest disclosed asset review set is **3,650/6,862 jobs** in APEIROPHOBIA
(film `c3d8ee5e-b119-4654-99f9-c6545f650635`, asset
`bf99f0cf-cccc-45cd-8f4c-da629cd9e1f1`). The largest reference set is
**1,264/2,511 jobs** (film `44f19dce-585e-43e0-a66b-69fe7daab910`, reference
`976a85ed-08e8-4686-9aae-0469dd926261`). Exact root and traversal scopes
are in the census. A candidate reachable through several sources
counts once in each root's set; summing sets double-counts. The thirteen original
panel generation-root closures reproduce exactly (1–23 reachable jobs per named
root, with all IDs retained). Titanic can now enumerate review from its two
unresolved input assets even though its old generation-root code remains unknown:
each has four direct/total known consumers /four jobs. No original code is edited.
Dry Aged Dreams has no disclosed material input root; zero known input closure
is not zero production impact. Transmission has known asset consumers but no
resolved generation origin. Hidden dependencies can enlarge any set, and actual
change effects can be smaller than the structural candidate set.

### Step 5 — Lineage, canonical versions and change propagation

[invalidation_policy.json](invalidation_policy.json) is a **proposed information
and behaviour contract**, not implemented studio architecture. It requires film-
scoped node/version IDs, typed edges, literal role/path, immutable source-version
bindings and evidence. Unknown versions stay null. Canonical authority needs
an actor/declaration, version, property and task/scene/project scope; a hub or a
single task's authority cannot promote an entire library.

A representation refresh under the same immutable asset is distinct from content
or version replacement. On a content/reference change, enumerate direct material
or actual reference consumers, traverse known generation dependencies, deduplicate
and mark review candidates with causes. Preserve old candidates, bindings and
decisions. Humans choose whether to keep, rebind, regenerate or approve a replacement.
The policy does not automatically rerun, reject or revoke approval. Preset and
unknown-edge meanings need adapter review before material propagation. Inferred
links remain a labelled overlay, never part of observed closure without evidence.

### Comparisons by task, literal model and cohort

Task here means recorded generation type; it is not one shot or semantic workflow
role. The full per-film and summary outputs retain every type/model, including
small subgroups and undefined rates. Models stay literal, with no provider or
capability inference. Means condition on films using the named type/model.

| Task or literal model | Chained jobs /jobs in stratum | Equal-film mean (films with stratum jobs) |
| --- | ---: | ---: |
| Image | 41,779/92,058 | 40.89% (155) |
| Video | 31,075/38,508 | 73.29% (156) |
| seedance_2_5 | 25,732/31,082 | 73.29% (145) |
| nano_banana_2 | 15,707/25,355 | 45.64% (138) |
| seedream_v5_pro | 10,754/21,136 | 47.76% (96) |
| gpt_image_2 | 7,551/14,397 | 46.60% (120) |
| soul_cinematic | 651/7,696 | 6.09% (65) |

Here chaining accepts any material-producing parent. Study 05's image-parent
count happens to reproduce at 41,779; the video number is a union across material
roles, not the sum of Study 06's separate image/video-parent indicators.

| Cohort | Films; jobs | Shared-input jobs /jobs; mean film share | Chained jobs /jobs; mean film share |
| --- | --- | --- | --- |
| Shortlist only | 62; 45,497 | 30,331/45,497; 68.15% | 25,847/45,497; 54.28% |
| Most watched only | 55; 31,169 | 23,201/31,169; 74.00% | 17,731/31,169; 49.61% |
| Both | 40; 54,038 | 38,220/54,038; 70.84% | 29,285/54,038; 54.56% |

These are descriptive associations. Capture, operation/model mix, scale, duration,
creator overlap and repeated requests compete as explanations; none shows a
method causes selection, quality or continuity. Orientation/scale splits retain
Study 01's inferred thresholds and all outliers. No useful catalogue-category
format split exists: all primary categories are empty arrays.

## 5. Fully traced examples and counterexamples

The [case ledger](outputs/case_evidence.csv) and [sixteen panel maps](outputs/panel_maps.json)
retain full evidence IDs, source paths, short excerpts, labels, alternatives,
denominators and confidence. Each map includes the named typed subgraph, whole-
graph metrics and complete-graph release locator. Full node/edge tables filtered
by film ID provide the **complete** maps, including disconnected components;
the named subgraphs alone are not claimed complete. No inferred edge is added.

1. **The Staff — output continuation despite sparse resolved origin.** Film
   `3b09c7c2-3f0c-48e3-8304-fad569bf50ce`, codes `the-staff:07.1`, `:07.4`,
   `:07.5`. Producer/output `0e619b88-43ef-4a45-84c3-b7b86ac96fe4` →
   consumer `1d963033-bc45-495d-9bfa-a05e4d0cf918`, both `seedance_2_5`,
   role `input_video`, path `params.medias[1].data`. The case instruction says
   “frame 1 same last frame from here”. Observed edge, inferred continuation
   intent, proposed one-descendant review set /82 jobs. Only **one resolved
   pair /82 jobs** is exposed despite 23 reference records. Alternative: most
   preparation happened elsewhere or lacks producer IDs. Confidence is high in
   exact keys; no verified seam, reference contents or project order follows.

2. **Fallen Leaves — cross-model preparation, then further reuse.** Film
   `6659c520-c88e-4ac7-a2c9-f28d8a40c954`, `fallen-leaves:07.1`–`:07.5`.
   Asset/producer `1cba062c-b6c5-456d-929d-b958859ae105` (`gpt_image_2`) →
   `023fadcd-4fdd-46b9-98f4-1b940839b4c7` (`seedance_2_5`) via
   `params.reference_elements[0].medias[0]`, role `reference_image`.
   That output also feeds `aa8a5c34-415f-4371-aca9-777f976cfed5` via
   `params.medias[0].data`. Observed links; proposed review closure from
   `023fadcd` is **23 unique jobs /356**, all IDs rebuilt exactly. The full
   graph has **37 recurrent /41 material input assets**, despite two folders.
   Alternative: further-work candidates rather than approved versions; flat
   placement says nothing about continuity. Confidence: explicit joins and
   complete released-graph traversal, without media verification.

3. **Titanic — shared sources without a known local producer.** Film
   `3f6e509b-f3da-4324-a746-b9d35f0b9845`, `a-tales-before-titanic-tragedy:07.1`–`:07.4`.
   Assets `7a44e44c-7b45-4fc5-8c8b-303f25779194` (subject,
   `params.input_images[0]`) and `612f580b-00fe-4730-a3eb-b2c49902c939`
   (wardrobe, `params.input_images[1]`) feed all **4/4 jobs**. Named consumer
   `416eb299-5a02-4dd1-99c1-8a11d9de0b04` asks “make a character sheet.”
   All four primary texts are equal. Observed shared branch, inferred package
   intent, **0/4 chained jobs**. Each source's observed review surface is four
   jobs; their union remains four. Alternative: reruns from external sources,
   not four independent trials or canonical versions. Exact keys/text equality
   support the binding claim; fulfilment, origins and approval remain unknown.

4. **APEIROPHOBIA — authority is scoped, review is structural.** Film
   `c3d8ee5e-b119-4654-99f9-c6545f650635`, `apeirophobia:03.6`, `:07.5`.
   Task `4896743a-85d5-44df-8539-e08e0c8f7fdb` says “This single reference
   image is authoritative for the entire shot.” Start asset
   `288c7412-7e51-4301-af39-c1c460395c5c` binds at `params.medias[0].data`;
   audio `50f6882c-093c-4c1f-9020-4715e5483f4e` separately binds at
   `params.medias[1].data`. Observed instruction and bindings, not project-wide
   approval. Independently, producer `88160a68-3dd4-4662-be7e-4fb5852634c5`
   → `b6e44e77-d4a0-4821-9663-55a452fffc01` →
   `311a3f4c-be35-4c70-8d8e-2b882804d9cd` yields **two descendants /6,862 jobs**.
   Scope: named records in 63 purposively inspected /6,862 exported jobs, but
   traversal searches all exported edges. Alternative: local conditioning and
   editor candidates, not proven identity preservation or accepted finishing.
   Confidence is high in exact links/closure, bounded for intended authority.

5. **Counterexample — Dry Aged Dreams.** Film
   `3777eda4-c15e-4531-9f04-4c02a900f3c3`, `dry-aged-dreams:07.1`, `:07.4`,
   `:07.5`. All **11/11 usage rows are outputs**, across 11 jobs and 17 assets;
   the two literal models co-occur without an input handoff. The graph retains
   all 28 nodes in 17 material components; no material source root is disclosed.
   One asset's grouped raw/min objects establish representations, not a missing
   input chain. Alternative: external/omitted preparation. Confidence is high
   in the export census, insufficient for actual production connectivity.
   Missing inputs cannot establish text-only production or zero impact.

The case assignments are single-coder and purposive. Their counts are never
extrapolated to corpus semantic strategy prevalence or tested benefit.

## 6. Continuity-strategy and pattern catalogue

[catalogue.json](catalogue.json) preserves each pattern's problem, method, inputs,
sequence, evidence IDs/labels, tradeoffs, failure modes and applicability.
Failure modes below concern interpretation or proposed behaviour, not measured
technical failures.

| Problem / applicability | Inputs and sequence | Evidence / interpretation | Tradeoffs and failure modes |
| --- | --- | --- | --- |
| Carry shared identity/world context across tasks | Same exact source → bind independently to several consumers | Titanic/Transmission 07.2/07.4, observed shared inputs; continuity intent only where text establishes it | Central source widens review surface; shared source is not canon or a proven shared shot |
| Continue or change an existing output | Recorded producer → asset → continuation/change request | Staff/APEIROPHOBIA 07.1/07.4, observed chaining, inferred procedural intent | Downstream review grows; use does not prove approval or preserved pixels |
| Combine shared context with local derivation | Shared source + generated parent → new candidate with both bindings | Corpus hybrid indicator; Fallen Leaves/Lost named edges | Preserve both provenance channels; forcing one exclusive film strategy loses information |
| Converge prepared sources | At least two producers → bound assets → dependent candidate | Corpus convergence, Lost's separate image/video inputs | Several change causes; producer counts do not reveal layers or semantic objects |
| Navigate incomplete provenance | All nodes + known links + explicit unresolved origins | Dry Aged Dreams/Transmission counterexamples | Graph looks incomplete because evidence is incomplete; guessing origins produces false chains |
| Manage authority and changes | Explicit scoped declaration + immutable version → enumerate review → human decision | Nine panel 03.6 declarations; thirteen 07.5 closures; policy proposed | More decision recording; frequency cannot approve versions, reachability cannot force regeneration |

## 7. Studio-implication table

All behaviours are **proposed**, awaiting tests; none reconstructs internal
platform architecture or implements persistence/execution in this slice.

| Evidence → requirement or hypothesis | Proposed behaviour | Validation test |
| --- | --- | --- |
| Within-asset raw/min grouping; unresolved cross-ID identity → representations and versions need separate relations | One immutable asset/version with explicit representations; aliases carry evidence, never URL heuristics | Synthetic grouped raw/min changes no consumer degree; similar URLs and repeated names create no merge |
| 30,377 preset occurrences; mixed input roles → typed provenance must preserve raw semantics | Store literal role/path beside media/preset/unknown tag and source channel | Adding a style/lens preset never adds a material parent; unknown generic paths stay visible |
| Hubs, hybrid chains and convergence → dependencies need stable identities independent of organisation | Retain compound node/edge/version bindings, including disconnected nodes and unresolved origins | Cross-film ID collision, duplicate channel, folder move and diamond preserve exact material reachability |
| Staff/Titanic versus scoped authority → canonical versions need declarations | Record element/version, property and task/scene/project scope, actor/source/event; retain unknown approval | A high-degree source and an authoritative single-shot instruction cannot approve a project library |
| Thirteen bounded case closures → changes need review surfaces and causes | Enumerate unique candidates and supporting paths; mark needs_review, preserve prior bindings and decisions | Diamond/cycle terminates, descendants deduplicate, unrelated component stays intact; human reviews keep/rebind/regenerate choices |
| No observed quality/continuity outcomes → strategy benefit remains a hypothesis | Compare shared canonical reference, chaining and hybrid on a defined task in a separately authorised experiment | Predeclare sources, model/version, changed factor, repetitions, rubric, review and budget; no archive benefit claim |

## 8. Unresolved questions, provisional definitions and handoffs

Every provisional definition and its downstream dependency is explicit:

| Provisional definition | Later study / remaining boundary |
| --- | --- |
| Reuse/branch = ≥2 distinct consumer jobs for a raw compound material asset; reference recurrence analogous | Study 04 context/identity semantics and Study 09 comparable iteration families; job reuse is not necessarily cross-shot reuse |
| Chaining/convergence/shared ancestry = explicit material graph, with unambiguous existing producers for generation edges | Study 08 workflow roles and Study 09 revision intent; complete histories and semantic lineage remain unavailable |
| Raw/min/h264/hls within one asset = grouped representations; zero cross-ID merges | Studies 04/09 can refine property/derivative interpretation; absent explicit alias evidence cannot be manufactured by a later study |
| Canonical authority = explicit scoped declaration; approval requires a separate actor/version/event | Studies 09/12 review-state refinement and validated studio contract; no project-wide canonical census supplied |
| Review surface = known material/reference consumers plus transitive generation descendants | Studies 08/09 refine dependency meaning and revision families; Study 12 validates policy; visual impact is unobservable |
| Preservation/reference wording = unchanged AF3a structural regex on nonempty primary text | Study 04 semantic labels, sample exclusions, agreement and information-location matrix; no semantic census assumed |
| Task = literal generation type; model ID literal; orientation ≥70% image/video and existing scale bins | Study 08 roles/workflow interpretation; inherits Study 01 thresholds, no economic meaning |
| Semantic strategy/identity = inherited scoped single-coder case assignment; policy/catalogue response proposed | Study 04 context semantics, Study 09 family/review interpretation, Study 12 synthesis and controlled validation |

**Resolve what this study can:** Studies 02/03 now receive explicit typed graph
membership and representation handling; local reference-first edges remain
partial order, not scene/task or approved-version membership. Study 03's raw-ID
recurrence and Study 10's 20,869/29,906 baseline reproduce exactly; excluding
presets gives the separate 20,383/29,321 material count. These measures must not
replace one another silently. The cross-ID semantic alias/version dependency
remains unresolved, with the exact audit boundary recorded. Study 05's staging
and multi-input measures gain downstream coverage and raw/preview handling;
Study 06's bindings gain complete disclosed reachability. Neither gains semantic
source equivalence, actual keyframe timing or achieved preservation. Study 10
receives review-surface counts, without labour, ownership, spend or regeneration
cost. Earlier reports and case assignments are unchanged.

Study 04 remains deliberately pending by owner choice: no semantic sample labels
were read or assumed. Studies 08/09 receive typed edges and structural families,
not claims about model roles, internal agents or revision motives. Studies 11/12
receive descriptive measures and testable proposals, without winner labels,
comparison to uncollected films or an implementation ranking.

**Measures the evidence does not allow:** semantic cross-shot/identity/world-rule
persistence rates; complete cross-ID alias/semantic-version counts; project-wide
canonical-versus-frequent or approved-version prevalence; matched canonical/
chained strategy benefit; actual visual continuity, preserved pixels, shot count
or final screen use; actual changes/regenerations caused by a reference update;
approval/final acceptance, failure/retry/rejection rates; labour, cost, speed or
productivity; private work, hidden orchestration or agents. No later analysis of
these records can manufacture absent outcomes or decisions.

## 9. Reusable code, outputs and reproduction

Run from the repository root:

```bash
uv sync --locked
uv run python scripts/fetch_data.py
uv run python studies/07-lineage/build.py
uv run python scripts/fetch_data.py --output data/study07-fresh
uv run python studies/07-lineage/build.py --data data/study07-fresh \
  --output data/study07-reproduced --large-output data/study07-large-reproduced --check
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/check_repository.py
```

The fresh fetch verifies all 28 source assets. `--check` requires a separate
small-output directory and compares every committed output byte, including the
manifest and all large-asset hashes. Deterministic gzip headers contain neither
clock time nor machine filename. The integration test rebuilds when data exists;
CI without the snapshot explicitly skips integration and checks synthetic graph,
compound-key, undefined-rate, cycle, representation and artifact/hash boundaries.
No real records are copied into synthetic fixtures. Tests exercise analysis;
policy validation scenarios remain proposals, not a tested studio implementation.

| Output | Grain / provenance and denominator contract |
| --- | --- |
| eligibility.csv | Study 01 Study 07 register: 187 primary/supplemental/excluded/unavailable rows |
| film_metrics.csv; metric_evidence.csv | 157 film rows, counts and denominators; full numeric excerpts, source/query scope, alternatives and confidence; taxonomy fields remain inherited inferred context |
| summaries.csv | All/cohort/orientation/scale; explicit film IDs, measured subset has positive denominator_name; mean/median/IQR beside pooled counts |
| by_task_model.csv; summary_task_model.csv; summary_members.json | Film × literal type/model; within-stratum counts and job/nonempty denominators; summary member keys name exact eligible films, positive denominators select measured subset; model absence is not model use |
| hubs.csv | One deterministic maximum-consumer asset and reference per film where available; exact keys, source/count excerpt, denominator, alternative and confidence |
| alias_audit.csv | All film assets; JSON states, raw/min grouping, explicit source IDs and exact representation-URL collision groups, no URLs or media contents emitted; source scope assets.metadata_json/source_asset_id |
| review_summary.csv | Film × asset/reference input-root set; root denominator, film jobs, within-film closure mean/median/IQR/max, observed counts; joins film evidence |
| case_evidence.csv | All 80 unchanged 07.x and sixteen 03.6 rows, original labels and exact case paths; excerpts only |
| panel_maps.json | All sixteen panel maps: named typed edges/nodes, original evidence IDs, complete-graph locator, component sizes, isolated jobs and thirteen exactly checked producer-root review sets |
| structural_check.csv | 157 AF3a grain-equivalence checks, not semantic accuracy |
| release_manifest.json; reproduction.json | Large-asset hashes/sizes/schema; source release checksum-manifest hash, code/queries/specs/governance/upstream reports/registers/features/cases and every small-output hash |

The full graphs exceed 1 MB. They are published as three compressed CSV assets
plus **SHA256SUMS** at [study-07-v1](https://github.com/TelesforoAleix/ai-film-practice/releases/tag/study-07-v1):
`nodes.csv.gz`, `edges.csv.gz`, `review_census.csv.gz`. The latter travels with the
large graph despite being smaller than 1 MB compressed. Exact sizes/checksums
are committed in [release_manifest.json](outputs/release_manifest.json).
Nodes/edges include **all 157 graphs**; filtering by the unchanged panel register
provides all sixteen complete lineage maps. [queries.sql](queries.sql) loads the
local release build and gives panel, reuse and explicit handoff queries.

For graph rows, the typed edge/node tuple is its observed excerpt and exact
entity key; source_path names the released table/column. For review census rows,
the node key plus build.py:reachable selects exact consumers/descendants from
those edges; counts are observed reachability and only their use as invalidation
is proposed. Join film metric evidence for study, alternatives and confidence.
Group membership edges are never silently interpreted as execution.

All committed CSV/JSON outputs are below 1 MB. No data-directory file, full prompt,
machine path or local user name is committed. Original data, published snapshot,
programme, upstream studies, case files and prompt-label tools remain unchanged.
