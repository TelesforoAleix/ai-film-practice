# Study 09 — Iteration

## 1. Answer and evidence limits

Creators explore **related candidates and source-conditioned changes**, but the
archive does not expose a complete review or retry history. Across 157 primary
films, the mean film has **57.56% of jobs in repeated complete material-input sets**
within a literal job type; pooled membership is **80,987/130,704 jobs**. This is a
candidate-family rule, not proof of the same shot or revision intention. Sharing
just one input gives the broader **70.89% mean; 91,752/130,704** screen.

Equal primary text, literal type/model and complete nonempty input set identify
**53,130/130,704 candidate-rerun jobs**, mean film share **31.05%**. Controls may
still differ. Named case histories support title-position/size, continuous-shot,
paint, wear, machine-property and framing changes; shared inputs or timing alone
do not establish those deltas. Instructions describe requests, never achieved
media, defects, successful correction or a change of creative direction.

Outputs of **15,781/130,704 jobs** have a recorded material consumer, mean film
share **14.74%**. This is **adoption for further work**, not final acceptance;
no exported use cannot imply rejection. Candidate, review, approval and bounded
retry are therefore specified as separate **proposed** records/events in
[review_states.json](review_states.json), awaiting validation.

Only the selected cohort has detailed records; nothing here establishes what
separates top films from other films. Published histories can omit discarded,
external or private work. Nothing was watched or retrieved from the source site;
story, aesthetics, media quality, continuity and actual screen use are unassessed.
No agents, internal orchestration, labour, cost, failure rate, causal benefit or
tested best practice is inferred. Numeric claims join the [metric ledger](outputs/metric_evidence.csv);
semantic claims join the [64-row case ledger](outputs/case_evidence.csv).

## 2. Population, coverage, units and denominators

Study 01's unchanged Study 09 eligibility register provides **157 primary histories**:
62 shortlist only, 55 most watched only, 40 both. The priority union is 186;
23 non-open-source listings are excluded and six public workspaces unavailable.
Cosmic tracks remains a separate supplemental pilot and contributes to no measure.
All 49 unusual histories remain; no outlier is removed or winsorized. The 151
creator handles, repeated requests and batches preclude independent-trial claims.

| Unit / gate | Denominator and boundary |
| --- | --- |
| Film / recorded job | 157 films; 130,704 compound film/generation keys, every type retained |
| Primary text | 124,449 nonempty, 1,083 explicitly empty, 5,172 unavailable /130,704; nested copies add no job or independent primary instruction |
| Material input | Study 07's 29,321 raw compound material IDs, 307,316 distinct material asset/consumer bindings in 156/157 films; presets excluded; unseen contents unknown |
| Batch | All 130,704 jobs have nonempty batch IDs; only actual multi-job membership supports a batch family |
| Structural family | Separate shared-asset, exact input-set, batch and explicit producer/consumer relations; these overlap, cannot be summed as independent families |
| Pair comparison | Adjacent members within input-set/batch groups; all explicit lineage pairs; separate adjacent similarity/time screen; pair denominators remain separate from jobs/families |
| Panel semantics | All 16 registered films × four unchanged 09.x assignments = 64; purposive, unequal reading scopes, single coder; no prevalence extrapolation |
| Source parameters | Nine released malformed strings remain invalid; independently exported text/usages remain usable, JSON-only control comparison unavailable |

The [eligibility copy](outputs/eligibility.csv) retains all 187 priority/pilot
rows and their missing-evidence notes. Unavailable histories never become zero-work
films. Empty text differs from unavailable text. A zero comparison/text/input
membership denominator produces an unavailable rate, never a semantic negative.

## 3. Method, taxonomy, codebook and automated checks

[build.py](build.py) uses `film_practice.connect` over the verified
`data-2026-10-20` release and [measures.sql](measures.sql). Source columns remain
strings. CSV and JSON are parsed properly. Compound film/entity keys constrain
every join. The unchanged Study 07 graph supplies material/preset classification,
actual bindings and unambiguous existing different producers from assets and
output usages. Raw/min representations within one asset remain one ID; no
cross-ID semantic alias is merged. Names, folders, text or chronology add no lineage.

Codebook **1.0**, codes 09.1–09.4, stays unchanged. [taxonomy.json](taxonomy.json)
defines the additional structural operational rules beside inherited scoped case
interpretations. There is no exclusive whole-film iteration strategy.

| Family evidence, strongest before similarity | Operational rule and boundary |
| --- | --- |
| Shared material input | At least two distinct consumers of one exact asset; broad contextual screen only, no all-pairs revision comparison or transitive closure |
| Complete input-set candidate | At least two jobs of the same nonempty literal type with equal complete nonempty material-asset-ID sets; model can differ; role/path/reference bindings compared separately |
| Shared batch | At least two jobs with one compound nonempty batch ID; does not establish simultaneous execution or human choice |
| Explicit lineage | One actual producer → material asset → different consumer; deduplicate producer/consumer pairs across assets/channels; preparation and handoffs can be unrelated to revision |
| Similarity/time candidate | Consecutive dated nonempty requests within film/type/model, ≥10 distinct whitespace tokens each, token-set Jaccard ≥0.8 and event gap ≤24h; weak retrieval screen, never a revision or lineage claim |

The exact-set rule is a deliberately narrower candidate screen than the case
files' common-input examples. Detour and Transmission show why common sources
need not mean equal complete sets. No minimum lexical similarity is imposed on
stronger evidence: that would lose short correction requests. Similarity does
not upgrade an otherwise unsupported pair into the eligible revision population.
The 0.8/24h/10-token thresholds are local retrieval choices, not validated task
equivalence or work-session thresholds. Distant/nonadjacent related work can be
missed; adjacent boilerplate can match unrelated requests.

Within an input-set/batch group, sort parsed event timestamps then generation IDs
and compare adjacent members, not every possible pair. All timestamps parse in
Study 01; IDs only break ties. Lineage comparisons retain producer→consumer order;
similarity uses timestamp adjacency within type/model. Deduplicate identical pairs
**within** each basis, never across bases. Sorting is a comparison convention,
not a recovered revision decision or production order. Shared-asset fans receive
membership measures but no arbitrary ordered-delta census. Full member/pair sets
are regenerated by `families` and `comparison_pairs`; examples do not replace
corpus enumeration.

A candidate rerun requires equal nonempty primary text, nonempty equal literal
type/model and complete nonempty material input sets. This is stricter than the
original case interpretations: SNAP's equal-text pair spans two models, and
Lost's shared subset has differing full input sets. Original case labels are
preserved, not silently recoded. Parallel alternatives, reruns, local correction,
direction change and model change are separate modes in the taxonomy: batch or
shared-input membership supports **candidate alternatives**; no execution
parallelism is inferred. Low similarity or a model difference cannot establish
changed creative direction.

Text comparison requires **two nonempty primary fields**. Equality retains exact
case/whitespace. Additions/deletions are presence of positive case-sensitive
whitespace-token **multiset** differences, not ordered edit scripts or semantic
components. Reordering can change text without a multiset delta. `longer_text`
is character growth, not specificity. Preservation added/removed means the
unchanged AF3a regex switches absent/present, not newly retained media properties.
Input deltas compare raw material-ID sets; addition plus removal is only a
replacement candidate, without property equivalence. On lineage, adding a producer's
output changes the input set by construction; it cannot by itself prove replacement.
Role/path/reference tuple changes are independent of asset-set changes.

Control comparison uses canonical top-level scalars after removing enumerated
text/media keys and all containers, and requires two valid parameter objects.
It omits nested controls and is not full request equality. Raw selected controls
(model, mode, version, duration, dimensions, aspect, resolution, seed and flags)
remain beside each traced context, preserving absent/null/false/zero/invalid states;
full raw parameters remain retrievable by compound key. There is no unit/default
translation or control-effect inference.

The build checks all 15 named shared-input families, all 13 named adoption edges
and six linked 09.3 deltas; Detour's seventh coded delta remains an unordered
comparison. It checks correction opening spans and [11 short revision spans](outputs/revision_spans.csv)
against the source. All 64 original evidence rows retain their excerpts, labels,
alternatives, denominators and confidence. Shared-asset membership reproduces
Study 07 for every primary film. The 650 AF3a checks recompute edit/preservation
match counts and text denominators at **film × literal type × distinct primary
text**, before job weighting. These are correspondence checks, not semantic
precision/recall, independent agreement or outcome validation. English vocabulary,
quotation, negation, multilingual text and boilerplate limit lexical meaning.
No pending model semantic labels were read or used; Study 04 is an explicit dependency.

Counts under the rules are **observed**; family/mode/revision meaning is
**inferred**; source creator accounts retain **creator-stated** labels; descriptive
cohort relationships are **associated**, never causal; review/studio behaviours
are **proposed**. No experimentally supported claim is made. Each numeric row
joins film_id to `metric_evidence.csv` for exact compound-key scope, numeric excerpt,
source/query path, alternatives, denominators and confidence; row dimensions
further restrict that scope. Quartiles use linear interpolation and describe this
frozen cohort, not sampling uncertainty or independent creator observations.

## 4. Findings through the five programme steps

### Step 1 — Identify families without inventing ordered versions

| Observed relation | Positive films /157 | Jobs /130,704 | Equal-film mean; median; IQR /157 | Groups or pairs, not independent trials |
| --- | ---: | ---: | --- | ---: |
| Shared one material asset | 156 | 91,752 | 70.89%; 75.60%; 59.46–84.58% | 20,383 asset fans |
| Equal complete nonempty input set within type | 156 | 80,987 | 57.56%; 58.93%; 45.72–71.04% | 16,310 sets |
| Actual multi-job batch | 111 | 50,526 | 25.07%; 13.91%; 0–44.41% | 17,546 batches |
| Either endpoint of explicit lineage | 147 | 78,788 | 58.78%; 65.28%; 41.47–82.11% | 198,201 producer/consumer pairs |
| Similarity/time candidate only | 156 | 85,507 | 54.42%; 55.36%; 35.40–75.41% | 62,165 adjacent candidate pairs |

The union of the four structural support relations is **116,783/130,704 jobs**
in 156/157 films, mean **88.15% /157 films**. This broad union includes references,
preparation and handoffs; it is not an iteration rate. The difference between
shared-one-asset and equal-full-set membership is **10,765/130,704 jobs** under
these rules, demonstrating sensitivity to evidence granularity. None of the five
relation counts estimates semantic families, shots or attempts after rejection.
All jobs having batch IDs does not mean all batches contain alternatives.

### Step 2 — Alternatives, reruns, local corrections, direction and model changes

The stricter rerun candidate has **53,130/130,704 jobs in 154/157 films**, mean
**31.05%**, median **26.83%**, IQR **13.87–43.99% /157**. This counts all members,
including first occurrences, not repeat excess and not failed attempts. By
contrast Study 10's unchanged exact-text repeat excess is 63,042/124,449 nonempty
fields. Those are different numerators and denominators and cannot be subtracted
as a count of genuine or wasteful iterations.

All **32,448/32,448 text-comparable adjacent batch pairs** have equal primary
text; all **32,980/32,980 batch comparison pairs** have equal material input sets
and literal model IDs. Scalar controls differ in **18/32,980** pairs, across
**5/111 films with batch comparisons**, mean per-film control-change share
**0.0528% /111**. These records support candidate alternatives with repeated
requests; they do not disclose actual concurrency, reasons or outcome differences.
The remaining 532/32,980 pairs lack two nonempty texts, never become text-equal
observations by treating null/empty as a prompt.

The panel's mode assignments are separately audited in `panel_assignments.csv`:
**6 rerun interpretations +9 local correction requests +1 unknown /16 cases**;
order and intent within the shared-input families remain unconfirmed. A correction request does not prove a prior defect. Model differences
are observed in **5,043/64,677 adjacent input-set pairs**, equal-film mean **7.46%
over 156 comparison-bearing films**; they support model alternatives, not a
preference, switch motive, improved result or changed creative direction.
No coded 09.2 direction-change assignment establishes that mode; corpus direction
change and semantic parallel/rerun/correction prevalence remain unmeasurable.

### Step 3 — Compare text, inputs and controls on named relations

| Basis | Comparison pairs | Two nonempty primary texts | Text changes /comparable; equal-film mean (measured films) | Model changes /model-comparable; mean |
| --- | ---: | ---: | --- | --- |
| Adjacent complete input-set members | 64,677 | 63,695 | 25,697/63,695; 54.31% (156) | 5,043/64,677; 7.46% (156) |
| Adjacent batch members | 32,980 | 32,448 | 0/32,448; 0% (111) | 0/32,980; 0% (111) |
| Explicit producer/consumer | 198,201 | 191,448 | 190,819/191,448; 99.78% (147) | 140,008/198,201; 72.44% (147) |
| Similarity/time screen | 62,165 | 62,165 | 10,196/62,165; 28.15% (156) | 0/62,165 by within-model rule |

Most lineage comparisons are preparation or operation handoffs. Their high text
and model differences cannot establish revision intensity. Input-set pairs have
zero asset-set change **by definition**, while lineage pairs have **198,201/198,201**
changed input sets here. Similarity/time candidates have **5,318/62,165** input-set
changes, mean **16.23% /156 films**; related wording does not imply equal context.
These denominator-conditioned facts prevent conflating the relation types.

Within the 63,695 text-comparable input-set pairs, token additions occur in
**25,088/63,695** (mean **53.02% /156 films**), deletions in **23,757/63,695**
(mean **50.51% /156**), and longer text in **16,372/63,695** (mean **33.30% /156**).
The measures overlap. Preservation-regex appearance is **1,384/63,695** (mean
**3.26% /156**). These are lexical comparison differences, not new specificity,
semantic deletion or successful preservation. `summary_comparisons.csv` retains
removal, input replacement candidates, role-binding and scalar-control differences
with their separate comparable denominators. Semantic specificity/preservation
are established only for named case spans; Study 04 must refine them.

The seven coded 09.3 assignments comprise six explicit producer/consumer deltas
(Kiss, Lost, Ivy, Prophecy, RAM, SNAP) and Detour's named reference replacement
comparison. Eight assignments remain unknown; Titanic's exhaustive four-member
text/input comparison is `not_observed_in_scope`. Those are **7 coded +8 unknown
+1 scoped non-observation /16 cases**, not seven representative films with all
revisions recovered. A plate-family comparison cannot inherit a separate poster
or prop derivative's semantics.

### Step 4 — Further-work adoption, not approval

**147/157 films** have at least one output with an actual material consumer.
The source-job count is **15,781/130,704**, equal-film mean **14.74%**, median
**12.60%**, IQR **6.93–21.41% /157**. The corresponding consumer-job count from
Study 07 is 72,863/130,704: one source can condition many candidates. These are
different sides of a dependency, not selection or acceptance rates.

All 15,781 adopted source jobs are in the structural support union because a
lineage edge itself puts both endpoints in that union. Its **15,781/116,783**
conditional share, mean **16.90% /156 support-bearing films**, is therefore
selection-conditioned, not evidence that candidate grouping improves adoption.
All 198,201 lineage pair-families have adoption by construction. Adoption among
batch/input-set groups remains descriptive in `families_by_film.csv`; overlapping
families and shared outputs are not independent human selections.

The case audit retains **13 reused-for-further-work /16 assignments**, three
unknown (Titanic, Dry Aged Dreams, Transmission), **zero explicit approval /16
assignments**. This is absence of established approval in these coded units,
not a corpus-wide claim that nobody approved anything. No-use cannot identify
rejection or omitted discarded work.

### Step 5 — Review states and bounded retry specification

[review_states.json](review_states.json) is a **proposed information and behaviour
specification**, not a persistence or execution implementation. It separates:

- Candidate identity, immutable source/input versions, literal model/raw controls,
  source field paths/hashes, intended changed properties and invariants.
- Family membership and its evidence, comparison order and human confirmation of
  comparable task scope; overlap does not create automatic version ancestry.
- Submission/reviewer/changes-requested/approved/rejected/superseded events, each
  carrying actor, candidate version, event, reason, evidence and property/task scope.
- Further-work use and dependency-review causes, independent of approval. Study 07's
  deduplicated descendant sets mark review candidates without automatic reruns,
  rejection or revoked approval. Scoped authority remains separate from library approval.

Imports start `recorded` with review unknown. A changed prompt/input/model/control
creates a new linked candidate, preserving the old candidate and decision. A human
must explicitly approve that version/scope; neither completed status nor reuse
can do so. Direction changes require a named human decision rather than inference.

A human chooses a positive **maximum total attempts per task version**; the
archive supplies no optimal cap. Reserve a unique attempt before dispatch, count
reruns and interrupted/unknown invocations within that cap, and stop on exhaustion,
cancellation, missing required input, unresolved scope or ambiguous dispatch.
Preserve results and history; continuation requires a reasoned cap-change event.
A planning model cannot increase its own cap or approve its own proposal. Any
transport retry policy must be separately bounded and handle uncertain duplicate
dispatch. These rules are hypotheses for Study 12's synthetic/concurrent-cap and
human-review tests, not observed creator infrastructure or measured failure control.

### Comparisons by task, literal model and cohort

Task means recorded generation type, not a semantic shot or workflow role. The
corpus membership indicators are computed before stratification. Model/type means
condition on films with that literal stratum; absent models are not users.

| Task | Input-set members /type jobs; mean film share (films) | Rerun candidates /type jobs; mean |
| --- | --- | --- |
| Image | 52,046/92,058; 48.83% (155) | 39,599/92,058; 31.10% (155) |
| Video | 28,901/38,508; 66.93% (156) | 13,526/38,508; 26.30% (156) |
| Audio | 40/132; 14.59% (10) | 5/132; 3.74% (10); small/descriptive |

The one text job, one image_3d job and four unavailable-type jobs remain in the
outputs (1, 1 and 2 films respectively); each has zero input-set/rerun membership
under these rules, not evidence of no actual iteration. Source adoption is
13,672/92,058 image jobs, mean **22.39% /155**, versus 2,108/38,508 video jobs,
mean **5.53% /156**. Final media consumption outside the archive is unobserved.

| Literal model | Input-set members /model jobs | Mean film share (films with model jobs) |
| --- | ---: | ---: |
| seedance_2_5 | 24,360/31,082 | 68.28% (145) |
| nano_banana_2 | 18,450/25,355 | 54.32% (138) |
| seedream_v5_pro | 14,436/21,136 | 60.71% (96) |
| gpt_image_2 | 9,725/14,397 | 58.97% (120) |
| soul_cinematic | 790/7,696 | 9.61% (65) |

| Cohort | Films; jobs | Input-set members /jobs; mean film share | Rerun candidates /jobs; mean |
| --- | --- | --- | --- |
| Shortlist only | 62; 45,497 | 26,411/45,497; 56.13% | 15,350/45,497; 28.98% |
| Most watched only | 55; 31,169 | 19,591/31,169; 56.83% | 11,373/31,169; 28.07% |
| Both | 40; 54,038 | 34,985/54,038; 60.80% | 26,407/54,038; 38.36% |

Every literal model/type and small subgroup remains descriptive in the per-film
outputs; comparison strata use the second member's type/model, retaining
producer→consumer order only on explicit lineage. Differences are **associations**.
Capture, task/model mix, duration, scale, input interfaces, language, repeated
creators/requests and omitted work are competing explanations. There is no causal,
quality, provider, capability or jury/audience-preference inference. Orientation
and scale retain Study 01's thresholds; catalogue category cannot supply a useful
format split (all primary categories are empty arrays).

## 5. Fully traced histories and counterexamples

All examples join full film/evidence keys in `case_evidence.csv`, named contexts
and actual bindings in [revision_histories.json](outputs/revision_histories.json),
and exact source spans in `revision_spans.csv`. Labels apply to the claim, not
a whole film. Confidence is high for compound-key edges/spans and bounded,
single-coder for interpretation; no media fulfilment is assessed.

1. **The Kiss — poster revision, separate from the plate family.** Film
   `655325cc-46d9-4b0b-b03d-d177defa4b3f`, `the-kiss:09.3`.
   Producer/asset `6672ee33-d850-4db4-b78f-667905814400` → consumer
   `19f73675-b69e-4314-b3a1-f74802df1da2`, both nano_banana_2, actual
   input_asset at `params.input_images[0]`. Producer requests “Add the words
   \"The Kiss\"”; consumer requests “Move the entire title \"The Kiss\" UP” and
   “Reduce the title's size slightly”. **Observed** edge/wording; **inferred**
   local title-position/size revision. Denominator: one pair; all film assets/usages
   searched; 391/391 job contexts in the inherited reading. Alternative: a new
   poster candidate without a visibility defect or approved replacement. The
   separately named three-member shared-input plate family cannot inherit this delta.

2. **Lost — continuous-shot preservation added along a video edge.** Film
   `e5ce8a79-9375-4e31-84a8-620bd4f07550`, `lost:09.2`/`:09.3`.
   Producer/asset `4e117e2d-14cf-46f3-8466-69d0306101ff` →
   `09925f84-295d-42ac-a3f2-d8dbf98a1740`, both seedance_2_5;
   input_video at `params.medias[0].data`. Producer says “make everything the
   same”; consumer adds “one continuous shot with no cuts”, while asking to fix
   sounds/color grading and retaining three named references. **Observed**
   edge/spans, **inferred** scoped preservation delta. Denominator: one pair,
   350/350 contexts and all assets/usages searched. Alternative: further candidate
   work rather than a failed predecessor or successful correction. Literal
   model=default remains beside the request; it does not erase correction intent.

3. **Random Access Memories — wear on a prepared object.** Film
   `e99b5ad2-8f58-4ef8-a13c-4441cfdd5205`, `random-access-memories:09.3`.
   Producer/asset `a5620e3d-120b-4dd5-ad46-ccb087640437` (gpt_image_2) →
   `d0efc423-f288-4e29-9665-e2bd10b23b29` (nano_banana_2), input_asset at
   `params.input_images[0]`. “make prop sheet of a Commodore 64 console” becomes
   a source for “overused, tape around it”. **Observed** edge/property request;
   **inferred** derivative and added specificity, not length-based specificity or
   explicit version approval. Denominator: one pair, 482/482 job contexts and all
   assets/usages searched. Alternative: a new conditioned candidate; no separately
   established preservation span or successful wear treatment is claimed.

4. **Detour — changed reference, unestablished direction.** Film
   `d90fe8bd-3329-40b3-963c-d9b33075aec1`, `detour:09.1`/`:09.3`.
   Named members `093e4529-6ad2-4ab4-9703-12dbd79de477` and
   `c430fa55-2065-4ca3-8114-7698cbcb36c3`, both seedance_2_5, share assets
   `56ce2d38-8485-47ec-9005-301d0a6d629e` and
   `f69abdbb-17f3-4cac-907f-af90f447bc13`. Reference bindings differ:
   `36137ad2-4960-44bc-9896-3c88a953afc8` versus
   `2e3a1baf-2838-48a0-9ea1-f76e695724c1`. **Observed** binding difference;
   **inferred** candidate replacement, comparison order only. Denominator: two
   named members /6,162 jobs; 219 purposively inspected contexts; all bindings
   available. Alternative: different shots/tasks using common context rather
   than ordered revision. Full input-set equality and semantic input replacement
   cannot be inferred from the shared subset.

5. **Counterexample — Titanic equal requests across distinct batches.** Film
   `3f6e509b-f3da-4324-a746-b9d35f0b9845`,
   `a-tales-before-titanic-tragedy:09.1`–`:09.4`. All four jobs use assets
   `612f580b-00fe-4730-a3eb-b2c49902c939` and
   `7a44e44c-7b45-4fc5-8c8b-303f25779194`, identical primary texts and literal
   nano_banana_2; each has a different batch ID. Full member IDs are in the case
   ledger and deterministic comparison example. **Observed** equality and inputs;
   **inferred** rerun candidates. Denominator: all 4/4 jobs; no text/input delta
   observed in that scope, no directional intent or adoption/approval established.
   Alternative: repeated candidates from external preparation. This counters both
   batch-ID presence as sufficient family evidence and repeated prompts as proof
   of directional revision, failure or acceptance.

6. **Counterexample — Dry Aged Dreams.** Film
   `3777eda4-c15e-4531-9f04-4c02a900f3c3`, `dry-aged-dreams:09.1`–`:09.4`.
   All **11/11 prompts are distinct**, batches singleton, all 11 usage rows outputs;
   no supported structural family or adoption edge is established. All four
   iteration assignments remain unknown. A lexical similarity candidate, if
   retrieved, cannot supply the missing family/intent evidence. Alternative:
   external or unpublished work. Exact released counts are high confidence;
   absence of actual exploration, rejection or iteration is not established.

Other traced histories retain Ivy's paint addition, Prophecy's machine age/power/
palette instruction (with broader structural-change ambiguity), SNAP's box-framing
change and all thirteen named uses. None transfers its intent to a different
shared-input family or becomes a corpus-wide revision-frequency estimate.

## 6. Pattern catalogue

[catalogue.json](catalogue.json) records each problem, method, inputs, sequence,
evidence/label, tradeoffs, failure modes and applicability. Failure modes below
concern interpretation or proposed use, not measured production failures.

| Problem / applicability | Inputs and sequence | Evidence | Tradeoffs and failure modes |
| --- | --- | --- | --- |
| Explore related alternatives | Shared source → compare full bindings/task intent → human confirms family | Detour/Transmission 09.1; observed bindings, inferred comparability | Broad screens mix shots; transitive shared-reference closure creates false versions |
| Identify repeated requests | Exact text/type/model/nonempty set → compare controls → retain candidates | Titanic/Staff 09.1/09.2; inferred rerun | Equality misses semantic reruns; repetition is neither waste nor failure |
| Request bounded correction | Source → changed property/region + invariants → candidate → review | Ape/Transmission 09.2; inferred intent | Scope needs interpretation; request cannot disclose mask, defect or preservation success |
| Make revision differences inspectable | Actual producer/input pair → changed paths/spans → intended delta | Kiss/Lost/RAM 09.3; observed links, inferred revision | Preparation also creates edges; length/similarity alone cannot measure specificity or direction |
| Compare model alternatives | Named shared inputs/text → literal model/control differences → human choice | Prophecy/SNAP 09.1; observed model differences | Different interfaces/context confound comparison; no provider or benefit ranking |
| Separate use and decision | Candidate → further-work edge; separate human version/scope decision | Thirteen 09.4 uses, three unknowns; proposed review response | Added recording; frequency cannot approve, no use cannot reject |

These are bounded patterns, not tested best practices. Shared practices require
independent projects; repeated jobs or several films by one creator are not such
independent replications. No strategy effectiveness comparison is supplied.

## 7. Studio-implication table

All behaviours are **proposed**, awaiting validation. They are information and
behaviour requirements, not a new execution/storage architecture.

| Evidence → requirement or hypothesis | Proposed behaviour | Validation test |
| --- | --- | --- |
| Shared subsets versus full sets; Detour input change → family membership needs explicit scope/evidence | Store basis and named members, preserve binding differences; require human comparable-task confirmation | Synthetic shared-reference fan with different shots never becomes one ordered version chain |
| Titanic/Staff equality and batch singleton boundary → retain candidate identity beyond prompt/batch equality | Distinct candidates with text/input/control provenance and separate family links | Four equal requests across four batches remain four candidates, one candidate input-set family, no approval |
| Kiss/Lost/RAM source-linked deltas → revision needs changed properties and invariants | Immutable source/candidate versions; record exact changed paths/spans and comparison-order kind | Human trace exercise distinguishes title/continuous-shot/wear delta from unrelated plate/shared-input family |
| Actual model alternatives and scalar changes → request identity includes model and raw controls | Retain literal IDs/version states and raw values beside interpreted modes; no invented defaults | Null/false/zero/absent/invalid round-trip and model change preserve both requests and old decisions |
| Thirteen uses with no approval events → adoption and review are independent | Explicit actor/event/version/scope-backed approval/rejection; preserve unknown import state | A reused unreviewed output stays approval-unknown; no-use candidate stays rejection-unknown |
| Study 07 reachability versus actual changes → dependency review needs causes | Deduplicate known descendants, mark needs_review, human chooses keep/rebind/new candidate | Synthetic diamond/cycle terminates; no automatic rerun, rejection or revocation from reachability |
| Missing failures/discarded-work denominator → bounded retry is a product hypothesis | Human total-attempt cap, unique reservation, uncertain-outcome stop, reasoned cap changes | Concurrent synthetic reservations cannot exceed cap; interruption preserves reservation; no autonomous cap increase |
| Unvalidated family semantics → test retrieval and reviewer decisions before claiming benefit | Independent comparable-task adjudication, then separately authorised controlled comparison | Predeclare tasks, baselines, changed factor, repetitions, rubric, budget and approval events; report agreement and exclusions |

## 8. Provisional definitions, unresolved measures and handoffs

Every provisional definition used here has an explicit dependency:

| Provisional definition | Later study / remaining boundary |
| --- | --- |
| Family = separate shared-asset, same-type full-input-set, actual batch or explicit lineage relation; union is a broad support screen | Study 04 task/context/component interpretation; Study 12 independent comparable-family validation; no semantic shot/entity equivalence |
| Similarity = adjacent same-type/model ≥10-token Jaccard ≥0.8 within 24h | Study 04 semantic context and Study 12 retrieval adjudication; missing nonadjacent/multilingual relations and boilerplate false candidates remain |
| Rerun candidate = equal primary text/type/model/nonempty material set; parallel alternatives are unordered candidates | Study 04 intent/context and Study 12 human validation; controls can differ, actual concurrency/motives remain unavailable |
| Text delta = exact equality, whitespace-token multiset changes, character growth; specificity only named case interpretation | Study 04 semantic components/agreement and sample exclusions; length never establishes specificity or direction |
| Preservation/edit = unchanged AF3a lexical markers, preservation delta = appearance/disappearance | Study 04 semantic labels/context matrix; no semantic census or achieved preservation |
| Input delta = raw material set difference, replacement candidate = both addition/removal; role/path/reference tuple differences separate | Study 04 property/context interpretation and Study 12 family validation; cross-ID semantic aliases and actual equivalent replacements remain unknown |
| Control delta = canonical top-level non-text/media scalar subset on valid objects; selected raw controls retained | Study 04 context and Study 12 adapter validation; omitted nested/container controls and hidden defaults remain unknown |
| Adoption = actual output material consumer, source-job denominator; support-conditioned use explicitly labelled | Study 12 review-contract validation; final use/acceptance cannot be recovered from archive edges |
| Local correction/derivative/revision specificity = inherited named case interpretation, no broadcast to films | Study 04 semantics and Study 12 independent adjudication; no motive, defect or outcome inferred |
| Task/type/model = literal generation type and ID; orientation ≥70% image/video; scale <200/200–999/1,000–2,999/≥3,000 jobs | Inherits Studies 01/05/06/08 structural context; Study 12 synthesis; no economic or actual shot meaning |
| Candidate/review/approval, canonical scope, immutable versions and human bounded total-attempt cap | Study 12 implementation decisions and controlled validation; proposal only, no optimal cap or reconstructed platform design |

**Resolve upstream dependencies at their supported scope, without rewriting them:**

- Studies 02/03 receive source-linked property deltas distinct from shared-input
  exploration, and explicit candidate/version/review requirements. Local
  preparation remains partial order; variants/identity and project-wide approval
  do not follow from derivatives or authoritative single-task instructions.
- Studies 05/06 receive named correction/revision histories and raw binding/control
  differences. These distinguish comparable named changes from broad shared-source
  groups. They establish neither matched-task benefit nor difficult-action motive,
  camera/keyframe rescue rates, masks, successful correction or final use.
- Study 07 receives narrower full-set candidates beside its unchanged broad branches,
  and review/adoption semantics. Its graph and within-ID representation rules remain
  unchanged; no semantic alias or automatic invalidation is invented.
- Study 08 receives separate alternatives/rerun candidates, named revision deltas
  and bounded review/retry requirements. Depth-two staging is still insufficient
  to call refinement, rescue or a retry, and model transitions do not reveal routing.
- Study 10 receives candidate membership versus exact repeat excess and source use
  versus approval. Folder placements do not create candidates/attempts. Repetition,
  reuse and budgets gain no waste, cost, labour or responsibility interpretation.

Study 04 is pending by owner's choice; the unavailable semantic sample was not
read or assumed. Its stratified labels will carry agreement/exclusion limits and
cannot retroactively label the entire corpus. Studies 11/12 receive descriptive
cohort measures and testable requirements, not winner labels or an implementation
ranking. No upstream report, codebook or case assignment is silently changed.

**Measures the evidence does not allow:** exhaustive semantic iteration/shot/
version families; original-to-final revision order; actual parallel-execution,
semantic rerun/local-correction/direction-change rates; corpus specificity or
semantic preservation/addition/deletion prevalence; complete alias-equivalent
input replacements; camera/keyframe rescue, difficulty or change motives; observed
review, approval, rejection, failure/retry/discard rates or optimal attempt cap;
final screen use, correction success, verified preservation, quality/continuity;
causal family/model/strategy benefit; labour, costs, savings, speed/productivity,
responsibility transfer, agents or internal orchestration. Absent decisions,
media and private work cannot be manufactured by later studies.

## 9. Code, outputs and reproduction

Run from the repository root:

```bash
uv sync --locked
uv run python scripts/fetch_data.py
uv run python studies/09-iteration/build.py
uv run python scripts/fetch_data.py --output data/study09-fresh
uv run python studies/09-iteration/build.py --data data/study09-fresh --output data/study09-reproduced --check
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/check_repository.py
```

The independent fresh fetch verifies all 28 source assets. `--check` requires a
separate output directory and compares every generated byte, including the
reproduction manifest. The integration test rebuilds when source data exists;
CI without it explicitly skips that integration and runs synthetic boundaries
and committed input/output hash checks. Fixtures contain no real source records.
Tests validate analysis and reproduction; review/cap scenarios remain proposed
studio validation, not implemented workflow software.

| Output | Grain / provenance and denominator contract |
| --- | --- |
| eligibility.csv | All 187 unchanged Study 01 Study 09 priority/pilot rows and missing-evidence notes |
| film_metrics.csv; metric_evidence.csv | 157 film rows; observed numeric excerpts, full compound-key/table/query scope, label, alternatives, denominator and confidence; taxonomy context remains inferred |
| summaries.csv; summary_members.json | All/cohort/orientation/scale ratios; explicit eligible film sets, positive denominator selects measured subset; equal-film mean/median/IQR before pooled numerator/denominator |
| by_generation_type.csv; by_model_identifier.csv; summary_*.csv | Film × literal type/model membership and use counts; job/nonempty/support denominators, every small stratum; corresponding summaries condition on users and cohort, member IDs recoverable from matching per-film rows |
| families_by_film.csv; summary_families.csv | Film × basis, group count, unique member jobs, largest family, groups with any adoption; denominators all film jobs or basis groups; overlapping groups are never summed as independent units |
| comparisons_by_film.csv; summary_comparisons.csv | All 157 films × four compared bases, including zero-pair films; pair/text/model/control comparable denominators; equal-film means only where the relevant denominator is positive |
| comparisons_*_generation_type.csv; comparisons_*_model_identifier.csv | Film × basis × second-member literal type/model; pair/delta counts with comparable denominators; producer→consumer direction only for lineage; source/case intent not assigned by stratum |
| case_evidence.csv; panel_assignments.csv; panel_family_checks.csv | All 64 unchanged case rows; assignment audits /16; 15 named common-input families with full-set equality separately checked; joins exact film/evidence IDs |
| revision_histories.json; revision_spans.csv | Seven named 09.3 comparisons and thirteen 09.4 adoption pairs with actual role/path/reference bindings, text hashes/states, selected raw control values/states, comparison order and lexical deltas; eleven exact checked spans; original ledger supplies full semantic provenance |
| comparison_examples.json | First sorted pair per available basis in each panel film; full compound keys, actual contexts, numeric excerpt, label, competing explanation, scoped denominator/confidence; examples are not the census |
| structural_check.csv | 650 exact AF3a original-grain match/denominator checks across 157 films; correspondence only |
| reproduction.json | Source release manifest hash; code/SQL/taxonomy/readings/catalogue/review specification, governance, upstream reports/registers/graph/features/case narrative and ledger hashes; all generated output hashes |

For numeric family/comparison rows, the row itself is the excerpt; film, basis
and literal dimensions select exact members/pairs through the hashed source code.
Join film metric evidence for alternatives/confidence, and summary member sets
for aggregate source scopes. Semantic interpretations join the original case
ledger, not numeric counts. `families`, `analyse` and `comparison_pairs` expose
reusable complete membership/pair enumeration; no large all-pairs text dump is
needed. Source texts remain retrievable only from the release by compound keys.

All committed CSV/JSON outputs are below **1 MB** each, contain no full prompts,
and live beside the study code. No `study-09-v1` release is needed. Original data,
programme, prior studies, prompt-label tools and case files remain unchanged.
No data-directory file, machine-specific path or local user name is introduced.
