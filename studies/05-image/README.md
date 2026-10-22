# Study 05 — Image construction and editing

## 1. Answer and evidence limits

Creators combine stills through **reference conditioning, prepared-output inputs
and explicit change/preservation instructions**. Across 155 eligible primary
histories, multiple image inputs occur in 28,200/92,058 image jobs; the mean
film share is 28.94%. An image-producing parent is recorded for 41,779/92,058
jobs; the mean film share is 40.89%. These are observed bindings and local
preparation edges, not verified composites, complete construction histories or
evidence that staging improves results.

Local correction is visible as intent: the panel asks for a tattoo replacement,
a logo on a tablet, a plant transplant and a chair replacement. Multiple inputs
and these requests do not disclose layers or masks. All 25,332 exported image-job
`is_inpaint` values are literally false; the remaining 66,726/92,058 image jobs
have the key absent. No active mask/layer key is found under the documented
key rule. This describes disclosure, never the absence of editing elsewhere.

Requested reference sheets, location plates and posters have different purposes;
8,076/92,058 image jobs have a recorded output attached as an image input to a
video job. This is a candidate shot foundation and further-work use, not proof of
keyframe timing, final use or acceptance. The proposed studio response is to
retain source bindings, allowed changes, invariants, raw controls, dependency
edges and explicit review decisions independently, then test the contracts.

Only the selected cohort has detailed records: this study cannot establish what
separates top films from other films. Nothing was watched or retrieved from the
source site. Story, aesthetics, media quality and continuity are unassessed.
No agents, internal orchestration, labour, cost, technical failure rates or
causal benefits are inferred. Numeric claims join the [metric ledger](outputs/metric_evidence.csv);
scoped interpretations join the [case ledger](outputs/case_evidence.csv).

## 2. Population, coverage, units and denominators

Study 01's unchanged eligibility register supplies **155 Study 05 eligible films**
out of 157 complete primary public histories. The other two have zero exported
image jobs; their histories are not missing image-operation observations coded
as negative findings. The [eligibility output](outputs/eligibility.csv) preserves
all 157 primary rows, rules and missing-evidence notes. The priority union also
contains 23 excluded non-open-source listings and six unavailable workspaces.
The supplemental Cosmic tracks pilot contributes to no measure here.

| Unit / coverage | Denominator and boundary |
| --- | --- |
| Image-bearing primary film | 155: 61 shortlist only, 54 most watched only, 40 both; outer primary population 157 |
| Image job | 92,058 compound film/generation keys; 31,503 shortlist-only, 20,667 most-watched-only, 39,888 both |
| Primary image text | 87,238 nonempty + 793 explicitly empty + 4,027 unavailable = 92,058; nested copies do not add instructions |
| Parameters | 92,058/92,058 image jobs have valid object JSON; Study 01's nine malformed published strings are outside the image-job subset and remain unrepaired |
| Image-bound input | 57,717/92,058 jobs in 153/155 films; role/path duplicates collapse by raw compound asset ID within the consumer |
| Multiple image inputs | 28,200/92,058 jobs in 150/155 films; raw IDs may alias, so this is not a semantic entity count |
| Recorded image parent | 41,779/92,058 jobs in 140/155 films; existing different image producer required in the same film |
| Two or more image parents | 17,668/92,058 jobs in 128/155 films; distinct producers, not occurrence rows or necessarily different characters |
| Panel | All 16 registered films × five unchanged 05.x codes = 80 assignments; one film's five assignments are not applicable to its video-only export |
| Additional integration reading | Six purposive property spans in two named image tasks; no prevalence or accuracy denominator |

All Study 01 unusual projects remain eligible where they have image jobs; none is
removed or winsorized. The 151 literal creator handles among the outer 157 films,
repeated prompts and batches prevent interpreting job counts as independent
trials. Small subgroups remain descriptive. A zero text/operation denominator
produces an unavailable rate, not zero. Per-film results come before pooled job
shares; quartiles describe variation in this frozen cohort, not sampling error.

## 3. Method, taxonomy and checks

[build.py](build.py) uses `film_practice.connect` over the verified
`data-2026-10-20` release and executes [measures.sql](measures.sql). Source columns
remain strings; parsing is derived only. All generation, asset and reference
keys retain their film scope. Producers require `assets.generation_id` and an
existing, different job in the same film. No filename, date or folder supplies
an inferred producer. Unresolved sources remain inputs without invented origins.

An image binding uses a typed image role (`input_image`, `reference_image`,
`input_start_image`, `input_end_image`) or generic `input_asset` at
`params.input_images[*]`, `input_image`, `image_reference`, `custom_reference`
or `paint_image`. Generic style, camera, lens, aperture, focal-length and colour
presets are excluded. Four image jobs have unexplained other input IDs, recorded
separately. No input-media property is inferred by inspecting its contents.
`paint_image` is a media binding, never automatically a mask.

[The operation taxonomy](taxonomy.json) uses this explicit precedence for an
exclusive **inferred recorded route**. Independent intent, construction,
mechanism and purpose axes preserve the overlapping codebook 1.0 assignments.

| Route | Rule | Evidence limit |
| --- | --- | --- |
| Local edit mechanism candidate | Literal boolean `is_inpaint=true` or nonempty mask/layer key | Not local-edit wording; no qualifying image jobs here |
| Upscale | Actual image binding plus literal `bytedance_image_upscale`; alternatively a Topaz image identifier with output dimensions exceeding positive recorded width/height | Model-scoped interpretation, not measured output pixels or quality; the recorded fields may not be source dimensions |
| Reframe | Image binding plus nonzero Qwen angle/move control or nonzero signed Flux outpaint control | Negative expansion stays negative; direction/units and actual reframing are not recovered |
| Multi-input composition candidate | At least two distinct image-bound raw asset IDs | Several conditioning images, not disclosed layers or successful composition |
| Reference-guided | Exactly one image-bound raw asset ID after preceding routes | Does not verify media content or instruction fulfilment |
| Fresh candidate | No image or unexplained other input, explicit `input_images=[]`, no populated other media parameter | Export-conditioned candidate only; never established text-only generation |
| Unknown | No supported route above | No inputs alone cannot establish fresh generation |

Every control output retains exact scalar JSON beside its type/state, literal
model and film. Absent, null, false, zero, empty, invalid/unavailable document and
nonempty container states differ. Topaz's equal `width`/`output_width` and
`height`/`output_height` fields do not identify the input pixels or disprove
upscaling; they simply fail this conservative enlargement rule. Keys containing
underscore-delimited `mask(s)` or `layer(s)` are inventoried recursively through
objects/arrays; null, false, zero and empty values are not active. This is a
published-parameter key audit, not reconstruction of hidden editing machinery.

The corpus prompt measures reuse AF3a's unchanged edit, preservation, reference
and lens regular expressions and its ≤300-character short-edit proxy. Each
nonempty primary field counts once per image job. These are **observed lexical
features**, not semantic local-correction, perspective, integration or purpose
labels. Quoting, negation, long descriptions and non-English text limit meaning.
[structural_check.csv](outputs/structural_check.csv) independently recomputes
match sums and short-edit counts at AF3a's film-distinct primary-image-text grain
and asserts equality on all 155 image-bearing films before job weighting.
[structural_audit.csv](outputs/structural_audit.csv) stores deterministic first
positive/negative panel keys, exact offsets, bounded matches and source hashes.
Neither is semantic accuracy, precision/recall or independent-coder agreement.

All 80 existing case assignments and unknowns are retained, with source paths,
short excerpts, labels, alternatives, denominators and confidence. Named opening
spans are checked against their source tasks; input contexts and producer edges
are rebuilt from the release. Six additional exact spans in [readings.json](readings.json)
are checked and linked in [integration_instructions.csv](outputs/integration_instructions.csv).
Their wording is observed; property interpretation is inferred, single-coder
and purposive. Semantic model labels are unavailable to this slice; none is used.

## 4. Findings through the six programme steps

### Step 1 — Image operations

Counts below are observed applications of the **inferred** route rules, with a
common denominator of 92,058 jobs and 155 films. Raw control semantics remain
beside the classification in `controls_*.csv`. Routes sum to the job denominator.

| Recorded route | Jobs / 92,058 | Equal-film mean share / 155 |
| --- | ---: | ---: |
| Fresh candidate | 5,893 | 7.41% |
| Reference-guided | 29,490 | 34.49% |
| Multi-input | 28,200 | 28.94% |
| Local edit mechanism candidate | 0 | 0% |
| Reframe | 22 | 0.03% |
| Upscale | 5 | 0.01% |
| Unknown | 28,448 | 29.11% |

The 22 reframe candidates comprise 21 `qwen_camera_control` jobs and one
`flux_2_pro_outpaint` job. Its four expansion values are −36, −111, −492 and −507;
these are signed recorded controls, not an asserted canvas expansion. The five
upscale-route jobs use `bytedance_image_upscale`; 50/50 Topaz image jobs have
equal pairs of recorded dimension fields and are retained as reference-guided
under this rule. These rare routes cannot support model-benefit comparisons.

### Step 2 — Image dependency chains and convergence

Observed local staging occurs in **41,779/92,058** jobs: film median **42.45%**,
IQR **19.31–60.70%**, mean **40.89%**, pooled **45.38%** over 155 films.
Two or more distinct image producers converge in **17,668/92,058** jobs:
film median **11.33%**, IQR **3.40–21.53%**, mean **15.29%**, pooled **19.19%**.
These counts require explicit image bindings and producer IDs; there is no
inferred lineage added to the corpus graph. They do not distinguish semantic
characters from plates/props/styles at scale or resolve cross-ID raw/preview aliases.

The panel supplies that bounded interpretation: Ivy's room and plant, Birthdays'
tablet and logo, RAM's foreground/background, and Kiss's blockout plus prop/world
inputs converge in named tasks. Nine of 16 scoped 05.2 assignments contain
`staged_construction`; thirteen contain `multiple_inputs`, two remain unknown,
one is not applicable. Those are assignment audits, never corpus prevalence.

### Step 3 — Integration and preservation instructions

The six additional property examples are placement, uniform scale, viewing-angle
adaptation, relighting and camera/composition preservation in Ivy's plant task,
and keeping the foreground coffee table uncovered in Harmony's seat task.
These are **inferred property codes on observed instructions**, not achieved
physical integration. The source ledger gives full keys and exact spans.
All six programme properties therefore have a traced instruction example.

At corpus scale, preservation wording occurs in **26,750/87,238 nonempty image
fields** (30.66% pooled; **28.70%** mean film share, median **22.64%**, IQR
**10.09–42.91%**, over 155 films). Edit vocabulary occurs in **23,074/87,238**
(26.45% pooled; **25.06%** mean). Short-edit wording occurs in **4,116/87,238**
(4.72% pooled; **6.19%** mean). These cannot supply semantic prevalence of local
correction, spatial integration or preservation success. KAGEROU's Japanese
placement/scale instructions are a concrete limit of English lexical coverage.

### Step 4 — Conditioning versus editing mechanism

The 28,200 multiple-input jobs do not establish that any layers were disclosed.
No mask/layer key qualifies in the 92,058 valid image parameter objects under
the key rule; [mask_layer_paths.csv](outputs/mask_layer_paths.csv) is therefore
header-only. Literal `is_inpaint=false` occurs in 25,332/92,058 jobs and true in
0/92,058; the key is absent in 66,726/92,058. The parameter ledger preserves these
states by film and literal model.

Five of 16 panel 05.4 assignments retain `inpaint_false`, ten are `unspecified`
and one is not applicable. APEIROPHOBIA's false control belongs to its separate
cover job, not its tattoo task. No film-level copying of that mechanism is allowed.
Ivy's plant task directly pairs local-edit wording with false inpaint; a mask
cannot be inferred from its request. These are disclosure limits, not failure rates.

### Step 5 — One-pass, staging, correction and regeneration

Of **23,074 edit-word fields**, **19,569** have an actual image input (84.81%
pooled; **84.74%** mean over 146 films with such wording). **13,586/23,074** have
an image-producing parent (58.88% pooled; **58.61%** mean over those 146 films).
The complementary 9,488/23,074 lack a resolved image parent. They are not
established one-pass jobs or full regenerations: sources can be external and edit
words can occur in long descriptions. The measures expose attachment/staging
alongside wording without turning it into semantic local-correction prevalence.

The panel allows procedural comparisons for similar requested purposes: Titanic
asks for a sheet with subject and wardrobe sources in one disclosed task;
Birthdays asks for a tablet package after a prepared tablet output, adding a logo
and changing the requested panels. Staff requests expression change while
retaining identity/style; Ivy requests a replaced object while holding the room
fixed. These are scoped differences in task decomposition and change surface,
not matched experiments. Identity, model, task complexity, external preparation
and capture scope compete as explanations. The records provide no controlled
same-task one-pass/staged or local-correction/full-regeneration comparison,
benefit estimate, successful correction denominator or retry/failure rate.

### Step 6 — Routes to still purposes and shot foundations

| Purpose | Traced route and denominator | What remains unknown |
| --- | --- | --- |
| Plate | Harmony empty-location request; Kiss blockout/prop/world-conditioned plate; 2/16 scoped 05.5 assignments | No verified empty plate, correct layout or final use |
| Reference sheet | Titanic subject/wardrobe task; Staff expression task; Birthdays studio views; 11/16 scoped 05.5 assignments | Requested form and reuse intent, not actual sheet contents/completeness |
| Poster | APEIROPHOBIA festival key-art request, 1/16 scoped 05.5 assignments; SNAP 05.2 separately links prepared room to poster | No complete poster inventory or final publication/approval |
| Candidate keyframe/foundation | 8,076/92,058 image jobs feed a video through an explicit image binding, in 143/155 films; equal-film mean 14.91%, median 11.92%, IQR 4.78–21.57%, pooled 8.77% | Reference image may be identity/style context rather than a start frame; exact role/timing waits on Study 06 |
| Final still | No final-acceptance event established by these assignments | Complete final-still denominator unavailable; output/reuse is not acceptance |

Dry Aged Dreams' purpose remains unknown (1/16 assignments); Transmission is
not applicable (1/16). These scoped purpose counts are not exhaustive film
inventories. No corpus-wide poster/plate/sheet prevalence is inferred from words.

### Comparisons by task, literal model and cohort

[by_route.csv](outputs/by_route.csv) reports each film's jobs within each recorded
route, keeping route counts separate from independent edit/preservation intent.
[by_model_identifier.csv](outputs/by_model_identifier.csv) keeps every literal
model with all measures. Model summaries below condition on films using that
model; cohort comparisons condition on all eligible image-bearing films in the group.

| Literal model | Films with image jobs | Multi-input jobs / model jobs | Equal-film mean multi-input share |
| --- | ---: | ---: | ---: |
| nano_banana_2 | 138 | 10,845/25,355 (42.77%) | 34.15% |
| seedream_v5_pro | 96 | 7,744/21,136 (36.64%) | 35.88% |
| gpt_image_2 | 120 | 5,512/14,397 (38.29%) | 34.58% |
| soul_cinematic | 65 | 4/7,696 (0.05%) | 1.79% |

These are descriptive associations with recorded task/input selection, not model
capability, routing policy, preference or benefit. Parameter interfaces, missing
external preparation and prolific histories are alternative explanations.

| Eligible cohort | Films | Multi-input / image jobs | Equal-film mean | Image-parent / image jobs | Equal-film mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| Shortlist only | 61 | 8,560/31,503 (27.17%) | 26.63% | 14,407/31,503 (45.73%) | 42.84% |
| Most watched only | 54 | 6,547/20,667 (31.68%) | 33.51% | 10,108/20,667 (48.91%) | 40.31% |
| Both | 40 | 13,093/39,888 (32.82%) | 26.32% | 17,264/39,888 (43.28%) | 38.70% |

Per-film counts, medians/IQR, orientation/scale strata and both weightings are
available for all measures. The cohort contrast changes with weighting; no causal
or significance claim follows. Category is unavailable as a useful format split
(the primary catalogue categories are empty lists). Selection, duration, repeated
creators, job mix and history capture remain unresolved confounds.

## 5. Fully traced examples and counterexamples

Full film UUIDs, generation/asset/reference IDs, literal models, role/path
bindings, original excerpts, labels, denominators, alternatives and confidence
are in [case_evidence.csv](outputs/case_evidence.csv),
[panel_contexts.json](outputs/panel_contexts.json),
[panel_edges.csv](outputs/panel_edges.csv) and
[construction_recipes.json](outputs/construction_recipes.json). Prefix IDs below
resolve only within the named film; producer and consumer are never joined by
prefix in code. Each recipe is one named construction, not the whole film.

1. **Don't Poison Ivy**, `d305f6e5-b906-49a1-a0c6-75ef7f653ad8`:
   room output `4ebd698e-e1f7-479d-93b0-4043e5e61913` and plant output
   `c16ce530-c7d1-461a-acc8-63b8d7de63b1` feed
   `5bc1268c-ccc1-419e-bd13-79344eadf228`, literal `seedream_v5_pro`.
   Observed: two producer inputs and false inpaint. Inferred recipe: prepare
   room/object → bind both → request uniform scaling, placement, viewing-angle
   change and relighting while preserving the room. Codes 05.1–05.4 and six-span
   ledger; one task within 553 inspected/exported jobs. Alternative: full-image
   resynthesis conditioned on sources rather than a layered transplant. No
   successful integration is established.
2. **Birthdays**, `d51d6821-d191-40f7-949b-1086750a2e93`:
   tablet output/producer `37f689e1-04da-473c-9778-97b61732ec90`
   (`seedream_v4_5`) and logo asset `b38a38ab-607f-4228-93ee-f2d940fdb20f`
   feed `372eae81-9e4e-4264-adac-febf9565667e` (`seedream_v5_lite`).
   Observed: actual source/consumer edge and two inputs. Inferred recipe:
   prepare tablet → bind tablet/logo → request logo placement and a view package.
   Codes 05.1–05.2; one task within 170 inspected/1,003 exported jobs. Four named
   views versus three panels remain ambiguous; the logo producer is not invented.
   No layers, successful embossing or approved derivative is established.
3. **Random Access Memories**, `e99b5ad2-8f58-4ef8-a13c-4441cfdd5205`:
   `49ff032e-996b-4900-ba33-abf6fc402e93` and
   `c22d3af3-53cf-41ce-be21-876ebcba6360` (both `nano_banana_2`)
   feed `d3a5b0ea-495f-4b9c-89c1-4fe217609f8b` (`nano_banana_2`). Observed: two recorded source edges and
   “use foreground of image 1”, “keep perspective consistent”. Inferred recipe:
   prepare sources → bind foreground/background → request perspective matching.
   Codes 05.1–05.4; one task within 482 inspected/exported jobs. Alternative:
   multi-source conditioning can redraw the scene rather than preserve layers.
   Mechanism and correct perspective remain unknown.
4. **Counterexample — Dry Aged Dreams**, `3777eda4-c15e-4531-9f04-4c02a900f3c3`:
   `3e7791d1-6165-4a81-bbaa-575811c1edd8` is the sole image job and a fresh
   candidate, with `input_images=[]` and `input_image=null`. Codes 05.1/05.4/05.5;
   all 11 jobs inspected. Empty exported inputs support neither proven text-only
   production nor a known final-still purpose. This counters using no resolved
   parent as proof of one-pass construction.
5. **Boundary counterexample — THE LAST TRANSMISSION**,
   `03f596b0-23da-4312-9e58-2e1cc4582348`: all 66/66 jobs are video, so all
   five image codes are not applicable. Creator-stated preparation and a video
   turn request cannot be silently counted as observed still-sheet production.

## 6. Pattern catalogue

These patterns describe bounded procedures; none is a tested best practice.
Failure modes below concern proposed use or overclaiming evidence, not measured
technical failures. Each evidence ID resolves the full provenance contract above.

| Problem | Method / inputs / sequence | Evidence | Tradeoffs, failure modes and applicability |
| --- | --- | --- | --- |
| Place a prepared object while retaining a room | Separate room/object sources → bind → name change permissions and invariants | Ivy 05.1–05.4, observed edges/inferred recipe | More bindings and constraints to manage; unsupported claims of exact preservation are a failure mode; applies to named source-conditioned placement |
| Attach a mark while retaining an object package | Prepared tablet + logo → placement request → requested view package | Birthdays 05.1–05.2, observed inputs/inferred derivative intent | Panel/view ambiguity needs human resolution; does not disclose embossing or layers; applies to property-local derivatives |
| Combine spatial regions from sources | Two source outputs → foreground/background roles → perspective constraint | RAM 05.1–05.4, observed edges/inferred recipe | Spatial relation must be explicit; role assignment does not guarantee preserved pixels or geometry; applies to multi-source composition intent |
| Correct one seat without covering another object | Base + named references → single change → size/placement/occlusion constraints | Harmony 05.1–05.4; inferred integration coding on observed text | Long invariant lists can be ambiguous; actual preservation is unobservable; applies to bounded correction requests |
| Construct a location from a layout and props | Blockout + prop/world inputs → ordered location-plate request | Kiss 05.1–05.5, observed inputs/inferred layout recipe | Layout authority and prop bindings need independent scopes; a supplied blockout is not verified geometry |
| Prepare a sheet without an observed local producer | Subject + wardrobe inputs → requested views | Titanic 05.1/05.2/05.5 | External preparation unknown; one disclosed task is not proven one-pass production; applies to reference-package requests |
| Finish or reframe an existing still | Bound source → literal model-specific controls → candidate output | Model/control ledgers and taxonomy, inferred route | Preserve signed values and dimension-field ambiguity; a model name cannot establish enlargement, outcome or acceptance |

## 7. Studio implications and operation contracts

[contracts.json](contracts.json) proposes six operation contracts: fresh,
reference-guided, multi-input composition, local correction, reframe and
upscale/finish. They require film/task IDs, role/property-scoped source bindings,
request evidence, literal model/raw parameters and states, changed properties,
invariants, output IDs, producer links and explicit review state. Unknown
versions/approval stay unknown. This is a design artifact, not implemented
persistence, orchestration or a change to existing repository contracts.

| Evidence | Requirement or hypothesis | Proposed behaviour | Validation test |
| --- | --- | --- | --- |
| Ivy/RAM producer convergence; 41,779/92,058 staged jobs | Preserve construction dependencies independently of folders | Store immutable source bindings and unresolved producers; expose local recipes | Synthetic cross-film ID collision and duplicate role/path uses retain only correct film-scoped dependencies |
| Camera/style preset audit | Input count needs typed roles and parameter paths | Retain raw usage plus classified media/preset/unknown state | Adding a lens/style preset must not create another composition image |
| Ivy false inpaint beside local-edit request | Requested correction and implementation need separate fields | Keep intent, optional masks/layers and literal control states independent | False-inpaint edit request creates no mask, outcome or approval event |
| Ivy integration permissions; Harmony coffee-table visibility | Changes and invariants need property/task scope | Bind source, placement, scale, perspective, occlusion, relighting and preservation independently | Human coders recover the same allowed-change/invariant set from a task contract; then test fulfilment in a separately authorised experiment |
| Birthdays' panel/view ambiguity | Conflicting scopes need an explicit human decision | Preserve both source spans and mark unresolved requirements | Adjudication exercise chooses a package spec without silently rewriting the source |
| Signed outpaint and equal Topaz dimension pairs | Raw adapter semantics must survive route classification | Store literal values/units and declared meaning separately | Negative controls round-trip; equal recorded dimensions do not create an enlargement claim |
| 8,076/92,058 outputs used by video; no final acceptance | Further-work use and approval differ | Link still/video inputs while requiring actor/event-backed approval | A video input edge alone never promotes a candidate to final/approved |
| No controlled construction comparison | Staging/correction benefit is an experimental hypothesis | Compare same sources/task/model with one changed factor and explicit review rubric | Predeclare repetitions, budget, invariant/change rubric and acceptance events; compare one-pass/staged or correction/regeneration separately |

All behaviours are **proposed** and unvalidated. The experiment specification in
the contracts does not claim an experiment was conducted. No architecture or
model-selection ranking is derived from corpus frequency.

## 8. Unresolved questions and downstream handoff

| Provisional definition | Later study / unresolved dependency |
| --- | --- |
| Image operation = conservative input/control route with documented precedence; raw values retained | Study 08 adapter/model-role interpretation; Study 06 moving-shot routes; no hidden implementation recovered |
| Fresh candidate = explicit empty input array plus no populated media parameter or recorded image/unexplained input | Studies 07/08 can refine source linkage/workflow interpretation; external history remains unknowable |
| Multi-input = distinct raw image-bound IDs, excluding named preset paths | Study 07 alias resolution and typed graph; several IDs need not mean several semantic objects |
| Staged = at least one explicit image producer, convergent = at least two distinct image producers | Study 07 complete disclosed lineage/aliases, Study 08 workflow roles; never full build order |
| Edit, preservation, reference and lens wording; ≤300-character edit proxy | Study 04 semantic labels/agreement and context matrix; cannot substitute lexical matches for checked semantic components |
| Integration properties and sheet/plate/poster purposes only in named case requests/spans | Study 04 semantic interpretation and information location; requested media properties remain unverified |
| Same recorded task purpose used for procedural comparison only | Study 09 comparable revision families/changed instruction deltas; no causal same-task comparison supplied |
| Image output consumed by video = candidate foundation | Study 06 start/end/reference roles and timing; Study 07 downstream dependency scope; never actual screen use |
| Scoped derivative and authority stay separate from approved versions | Studies 07/09 identity, canonical versions and review semantics; consumes Study 03's bounded distinctions |
| Study 01 image-led/film-led/mixed and scale thresholds retained | Study 08 role/workflow synthesis; Study 10's limits still exclude economic interpretations |
| Proposed contracts/review events and construction experiments | Study 12 synthesis and validation; no execution/storage architecture chosen here |

**Handoff to Studies 02/03/10:** the corpus now has image input/control route
measures beside literal job type and model. Study 02's task bindings and Study
03's package requests can use these operation contexts; they still do not prove
sheet contents or a complete build order. Study 10 can group image jobs by these
recorded routes but gains no labour, prices, responsibility, productivity or
format-comparable resource denominator. No prior study or provisional definition
was silently rewritten. Study 04 remains pending by the owner's ordering choice;
its semantic labels were not available or assumed. Studies 11/12 receive
associations and testable proposals, not winners or a ranking of practices.

The evidence **does not allow** corpus-wide semantic local-edit, placement,
scale, perspective, occlusion, relighting, plate/poster/sheet or final-still
prevalence; complete/alias-resolved construction chains; proven fresh/text-only
or one-pass rates; comparable same-task staging/regeneration benefits; actual
mask/layer implementation outside disclosed controls; verified source/output
pixels, preservation, integration, quality or continuity; keyframe timing or
screen use; acceptance, failure, retry, cost, labour or speed rates; internal
orchestration or agents. Later studies cannot manufacture omitted private work,
media observations or absent review events from these records.

## 9. Reusable code, outputs and reproduction

Run from the repository root:

```bash
uv sync --locked
uv run python scripts/fetch_data.py
uv run python studies/05-image/build.py
uv run python scripts/fetch_data.py --output data/study05-fresh
uv run python studies/05-image/build.py --data data/study05-fresh --output data/study05-reproduced --check
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/check_repository.py
```

The output directory for `--check` must differ from committed outputs. The
reproduction test runs the complete build when the fetched snapshot exists;
CI without it explicitly skips integration and runs synthetic boundary tests
and source/output hash checks. No real records are copied into fixtures.

| Output | Grain and provenance contract |
| --- | --- |
| eligibility.csv | All 157 primary Study 01 Study 05 rows, including two ineligible image-zero histories |
| film_metrics.csv | 155 per-film rows, every count and denominator; join metric_evidence on film ID |
| metric_evidence.csv | Full numeric excerpts, study/film/compound-key scope, source/code path, observed count label, alternatives, denominator and confidence |
| summaries.csv; summary_members.json | Equal-film means, medians/IQR beside pooled counts; exact eligible film sets by all/cohort/orientation/scale; measured subset has positive denominator |
| by_route.csv; by_model_identifier.csv | Film × recorded route/literal model counts; same numeric denominator columns and film metric provenance; route interpretation is inferred |
| summary_route.csv; summary_model_identifier.csv | Within each route/model and cohort/all, equal-film rates over films with positive denominator beside pooled counts; member films recoverable from the matching per-film rows; absent models are not counted as users |
| controls_*.csv | Film × literal model × parameter × state × exact scalar JSON, job counts and model-image-job denominator; containers retain state; join metric ledger for alternatives/confidence; exact generation scope selected by these predicates |
| mask_layer_paths.csv | Exact compound job/key inventory; header-only here means no matching keys in the 92,058 valid image objects, not no private masks |
| case_evidence.csv; panel_assignments.csv | All 80 unchanged scoped 05.x assignments and their state/value counts with denominator 16 |
| panel_contexts.json; panel_edges.csv | Named task controls, raw input bindings, resolved producer edges and evidence IDs; no guessed producers or media contents |
| construction_recipes.json | All 16 scoped convergence assignments with source contexts, observed edges, inferred recipe interpretation, applicability/tradeoffs/failure limits and original evidence metadata |
| integration_instructions.csv | Six source-checked short property spans, exact keys/paths, inferred interpretation and full provenance |
| structural_check.csv; structural_audit.csv | All 155 AF3a grain-equivalence checks and deterministic panel positive/negative match correspondence checks, not semantic accuracy |
| reproduction.json | Source release manifest hash, code/SQL/taxonomy/contracts/readings, binding design/upstream registers/reports/features/case narrative/ledger hashes, plus every output hash |

For subgroup/control rows, the exact filter is the row's literal dimensions within
the ledger's film-scoped image-job set. Numeric excerpts are those rows themselves;
aggregate source paths are the per-film outputs and build/SQL. Route semantics are
**inferred**; raw counts and fields **observed**; scoped source declarations retain
their original labels; requirements **proposed**. No experimentally supported
claim is made. Original data, the programme, prior studies and case files are
unchanged. Every generated CSV/JSON is below 1 MB; no `study-05-v1` release is
needed. No full prompts, data-directory files, machine-specific paths or local
user names are committed.
