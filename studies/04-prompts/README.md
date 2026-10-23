# Study 04 — Prompt design and context assembly

## 1. Answer and evidence limits

Creators specify changes, invariants, spatial roles and shot instructions in text
beside actual attached sources. The record supports **assembling context by
property and task scope**, preserving the provenance of each instruction and
binding. It cannot tell us which properties an unseen image supplies, what a
provider adds privately, or whether a request worked. The panel's plant placement,
logo edit and structured shot request demonstrate different context shapes;
there is no single demonstrated best prompt format.

Structural wording and provisional semantics are different evidence. Across 157
primary histories, preservation vocabulary has a 31.78% mean film share
(39,918/124,449 nonempty primary fields pooled). The 27B's provisional preservation
labels give a **63.13% mean film share after descriptive stratum weighting**,
conditional on 4,633 successful sampled texts and covered short-text strata.
These are different rules and denominators, not an estimated improvement or a
replacement census. Preservation has the largest 27B–Jev disagreement,
976/4,633 texts (component kappa 0.590); 27B–gold kappa is 0.875 on 276 paired
texts. The raw 5,000-text failure sensitivity interval is 59.72–67.06%; the
weighted all-length sensitivity envelope is 51.55–67.84% under the transport
assumptions in section 3. Long texts and missing semantic decisions remain
unknown. All fourteen components have the same qualifications beside their
measures below.

Possible conflicts require scope adjudication. Nine of sixteen panel 04.6
assignments retain a possible conflict and seven remain unknown; this is neither
a population conflict rate nor evidence of model confusion. Text length and
repetition cannot establish overload. None of the fourteen endpoints in seven
named revision comparisons is in the semantic sample; source-linked case
interpretations remain the available semantic evidence for those changes.

Only the selected cohort has detailed records; nothing establishes what separates
top films from other films. No media or source site was retrieved or watched.
Story, achieved aesthetics, quality, continuity, actual timing and final use are
unassessed. No agents, internal orchestration, labour, cost or production failure
rates are inferred. The [context contract](context_contract.json) is **proposed**,
not implemented infrastructure or an experimentally supported best practice.

## 2. Population, exclusions, coverage, units and denominators

The unchanged Study 01 [eligibility register](outputs/eligibility.csv) supplies
157 production-eligible primary films: 62 shortlist only, 55 most watched only,
40 both. Of the priority union of 186, 23 non-open-source listings were excluded
and six public workspaces unavailable. Cosmic tracks remains a separate
supplemental pilot and contributes to no measure. All 49 unusual projects are
retained; 151 creator handles across 157 films mean films are not independent
creators. No panel replacements occurred.

| Unit / gate | Denominator and limitation |
| --- | --- |
| Recorded primary job | 130,704 compound film/generation keys; not necessarily one shot or one semantic operation |
| Primary field | 124,449 nonempty + 1,083 explicitly empty + 5,172 unavailable; nested primary copies never add instructions |
| All-role field after crosswalk | 166,781 including empty/unavailable; 160,526 nonempty source-field occurrences |
| Nonempty roles | 124,449 primary; 36,056 other-text; 19 shot-prompt; 2 negative /160,526 fields |
| Exact text | 61,422 globally distinct all-role primary-population texts; 61,626 film/text pairs; repeated text is not independent evidence |
| Semantic sampling frame | 55,500 globally distinct texts ≤12,000 characters; 5,922/61,422 (9.64%) excluded long texts retain structure only |
| Published semantic sample | 5,000 globally unique assigned texts, all 157 films; 4,633 successes +367 final labelling failures (364 ValueError, 2 Interrupted, 1 HTTPError); no missing/pending |
| Weighting grain | Film × literal generation type × text role × distinct text; 55,753 eligible memberships in 481 occupied strata; overlaps across strata are intentional |
| Covered strata | 338/481 have sampled successes; 55,609/55,753 eligible memberships covered, 144 uncovered; full-length membership denominator 61,676 |
| Panel | 16 purposive films ×6 unchanged 04.x assignments =96; unequal inherited reading scopes, single coder, no prevalence extrapolation |
| Gold / cross-check | 276/300 successful paired 27B–gold texts; Jev–gold 300; 27B–Jev 4,633; no negative/shot-role gold examples |

[Field states](outputs/field_states.csv) retain role-specific empty/unavailable
counts. [Coverage](outputs/coverage.json) distinguishes global distinct texts,
film/text pairs and overlapping stratum memberships. A zero relevant denominator
has an unavailable rate. Missing input evidence never establishes text-only
production. No uncollected history becomes a zero-work comparison film.

## 3. Method, codebook and label checks

[build.py](build.py) loads only verified releases `data-2026-10-20`,
`prompt-labels-v1` and `prompt-labels-v2`, with `film_practice.connect` for source
views. [measures.sql](measures.sql) removes a nested field only when it is the
same compound generation and primary source path; the build first asserts exact
primary-copy equality. It checks all 160,526 nonempty field keys, roles and text
hashes against v1, and independently verifies every one of the 47,666 positive
semantic spans. All 35 full-field spans remain withheld; their hashes and lengths
are checked, and `present=true` is retained. Jev is never merged into the labels.
No source text is executed. Source columns stay strings; derived JSON parsing
preserves absent, unavailable, invalid, null, false, zero and empty states. The
nine malformed published parameter strings remain unrepaired.

Codebook **1.0**, codes 04.1–04.6, is unchanged. [Taxonomy](taxonomy.json)
separates source role, structure, semantic components, task context and information
channel. Structural features use the checksummed v1 release's unchanged rules:
English lexical matches, parsed whole-field JSON, XML-like syntax, section markers,
≤300-character edit-word proxy, ≥1,000-character description proxy, reference
and multi-shot markers, and duplicate stripped lines of at least 40 characters.
These are **observed** format/wording counts. They do not establish complete scene
description, edit mechanism, actual cuts or semantic absence in other languages.

Semantic interpretation uses the fourteen definitions published with v2: subject,
identity, action, environment, spatial relations, composition, lens/framing,
camera motion, lighting, material, aesthetic intent, timing, exclusions and
preservation. They mean explicit **requested** information in the labelled field.
No label says what a reference contains or an output achieved. `other_text`
includes language metadata and enhanced/source text; no explicit script source
path exists. Dialogue cannot automatically label every mentioned event as a
visual instruction. Short edits and multi-shot intent have no dedicated released
semantic component.

The reported model is `Qwen3.6-27B-Q4_K_M.gguf`, provisional inferred labels;
Jev reports `jev-1.14.0`, presence-only cross-check. Micro presence kappa is
0.779205 for 27B–gold (3,864 decisions /276 texts), 0.747471 for full-sample
Jev–gold (4,200/300), and 0.732228 for 27B–Jev (64,862/4,633). The separate Jev
gold run gives 0.743113. Gold is one agent coder, unadjudicated, with no independent
human validation or inter-coder reliability estimate; 24/300 gold texts lack a
successful 27B label. Exact spans establish correspondence, not correctness.
Environment is particularly uncertain: 27B–gold kappa 0.460, including 60/276
27B-only positives. No component or subgroup acquires a stronger validation claim
from the pooled micro statistic. [Agreement](outputs/agreement.csv) retains all
four comparisons' component contingency counts, denominators, accuracy and kappa.

For every semantic measure the primary estimand is a **descriptive, transported
short-text composition**, not unbiased population prevalence. For stratum s,
N_s is eligible distinct-text membership, n_s assigned sample texts, r_s successful
texts, and p_sc positive successes. Each success receives weight N_s/r_s.
Within each film, sum N_s·p_sc/r_s and divide by the mass of covered strata; then
report equal-film mean/median/IQR first and pooled weighted mass beside it.
[semantic_strata.csv](outputs/semantic_strata.csv) exposes every weight and zero
coverage stratum. Films have 1–33 successes each; all 157 have a measured rate.
The deterministic rotation and global deduplication do not give known inclusion
probabilities. Transport assumes assigned successes describe their covered
strata; task/model selection, shared texts and concentrated failures can violate
that assumption. Weighting cannot repair semantic label error.

Failure sensitivity instead weights every sampled text N_s/n_s, first making
failures all absent, then all present. Uncovered-stratum mass and excluded-long
mass receive 0/1 extremes in [semantic_bounds.csv](outputs/semantic_bounds.csv).
These are **conditional sensitivity envelopes**, not design-based confidence
intervals or logical bounds on the unknown corpus: unsampled texts within
covered strata are still transported from sampled texts. Without that assumption,
the evidence gives no useful population semantic prevalence estimate. Global
long exclusion is 5,922/61,422 texts; the corresponding overlapping stratum mass
is 5,923/61,676. Means by model condition on assigned sample models with the same
stratum weights; models are not sampling strata. Their transported composition
is especially tentative, never a model effect.

Every numeric row is its own aggregate excerpt. Structural rows join film_id to
[metric_evidence.csv](outputs/metric_evidence.csv); their source set is the film's
compound keys selected by SQL and the row's literal dimensions. Semantic rows join [semantic_evidence.csv](outputs/semantic_evidence.csv) and
select the assigned v2 source keys using film/type/role/model and component, then
join `agreement.csv`, `semantic_strata.csv` and `semantic_bounds.csv`; all spans
and disagreement IDs remain retrievable from v2. Their evidence label is
**inferred**, alternative ALT and confidence CONF in build.py. Aggregate film
membership is exactly the corresponding per-film output and dimension filter;
no significance test treats fields as independent. Case conclusions retain full
keys, source path, short excerpt, original label, denominator, alternative and
confidence in [case_evidence.csv](outputs/case_evidence.csv). Comparisons are
descriptive **associations**; studio behaviours **proposed**. No experiment ran.

## 4. Findings through the seven programme steps

### Step 1 — Distinct source fields and tasks

Primary, negative, shot-level and other text stay separate by source path.
The 36,056 other-text fields are chiefly language metadata, not another 36,056
independent generation instructions; enhanced/source fields remain separately
named. The 19 shot fields occur in two films and the two negative fields in two films.
Neither count estimates scripts, actual shots or all exclusion instructions.
Instructions embedded in primary prose remain primary; JSON text inside a primary
field does not become executed parameters. Task comparisons below use literal
image/video types; semantic purpose comes only from named case evidence.

### Step 2 — Fourteen provisional semantic components

Every row below is the **27B provisional label** on successful sampled fields,
with stratum weighting as defined above. Equal-film means use all 157 films;
weighted pooled shares divide by 55,609 covered memberships, not jobs or 61,422
global texts. Gold kappas use 276 texts; Jev kappas and disagreement counts use
4,633. Failure envelopes include all 5,000 assigned texts. All-length envelopes
add uncovered strata and excluded-long membership mass under the same transport
assumptions. Full per-film quartiles and task/model/role/cohort measures are in
`semantic_by_*.csv` and `semantic_summary*.csv`.

| Component | Positive /4,633 | Weighted mean film; pooled | Gold κ | Jev κ; disagreements /4,633 | Weighted failure envelope | All-length envelope |
| --- | ---: | --- | ---: | --- | --- | --- |
| subject | 4370 | 94.40%; 94.86% | 0.742 | 0.400; 538 | 87.95–95.11% | 79.30–95.59% |
| identity | 3399 | 72.45%; 70.54% | 0.649 | 0.598; 844 | 64.58–71.73% | 58.22–74.51% |
| action | 3381 | 71.35%; 69.18% | 0.633 | 0.812; 349 | 63.21–70.37% | 56.99–73.28% |
| environment | 3933 | 85.23%; 85.91% | 0.460 | 0.610; 610 | 79.42–86.58% | 71.61–87.90% |
| spatial | 3856 | 83.07%; 85.79% | 0.747 | 0.737; 306 | 79.32–86.48% | 71.52–87.81% |
| composition | 3568 | 77.69%; 80.01% | 0.757 | 0.644; 657 | 73.81–80.96% | 66.54–82.84% |
| lens_framing | 3235 | 70.11%; 71.40% | 0.781 | 0.748; 507 | 65.52–72.68% | 59.07–75.37% |
| camera_motion | 2293 | 46.50%; 43.86% | 0.873 | 0.892; 249 | 38.94–46.10% | 35.11–51.40% |
| lighting | 3473 | 75.39%; 77.69% | 0.919 | 0.884; 203 | 71.60–78.76% | 64.56–80.85% |
| material | 3311 | 72.38%; 75.04% | 0.728 | 0.674; 681 | 69.36–76.52% | 62.54–78.83% |
| aesthetic_intent | 3972 | 86.06%; 86.45% | 0.698 | 0.575; 681 | 79.92–87.08% | 72.06–88.35% |
| timing | 2160 | 42.29%; 38.46% | 0.824 | 0.885; 267 | 33.79–40.95% | 30.47–46.76% |
| exclusion | 3729 | 80.82%; 82.17% | 0.936 | 0.731; 466 | 75.84–83.00% | 68.38–84.67% |
| preservation | 2986 | 63.13%; 62.68% | 0.875 | 0.590; 976 | 57.17–64.33% | 51.55–67.84% |

Preservation, identity, material and aesthetic intent have the largest cross-check
disagreement counts (976, 844, 681, 681 /4,633 respectively); their corresponding
measures should remain especially tentative. Jev generally assigns fewer positives
for these four components; that is disagreement, not adjudication. Aesthetic
intent labels describe instructions, never an assessment of aesthetics.

### Steps 3–4 — Actual attachments and the information-location matrix

The build pairs every nonempty source field with that exact film/job's usages,
reference IDs and metadata-description availability. For primary text,
93,437/124,449 fields have a material-media binding under the enumerated role/path
rule (77.69% mean film share /157), 39,278/124,449 have a named reference binding
(34.89% mean), and 5,347/124,449 have at least one linked nonempty description
(5.84% mean). These different measures exclude camera/style presets from media;
metadata field presence does not establish any particular property in it.
Multiple role/path usages of one raw asset add no sources. Bound assets can have
unresolved producers; no name/date/token creates a lineage edge.

[The numeric matrix](outputs/information_matrix.csv) contains film × component
counts: positive successful texts, coexistence with media/reference/description
fields, successful-text and weighted-mass denominators. The provisional text
measure carries the component agreement and failure/long envelopes above; the
other columns are **observed channel availability**, not inferred image content.
[Panel contexts](outputs/panel_contexts.json) retain exact input IDs, raw roles,
parameter paths, reference metadata states and raw controls beside every named
04.x job. [Scoped locations](outputs/information_locations.json) retain all
sixteen original 04.4 assignments and their full evidence links.

| Property / information | Explicit text | Attached media | Reference metadata | Parameters / contradiction / unknown |
| --- | --- | --- | --- | --- |
| Subject and identity | Provisional component labels; Titanic subject/wardrobe tokens; Staff identity lock | Actual bindings observed; identity contents unobservable | Name/category may name an entity; not verified identity | No automatic same-entity or cross-ID equivalence |
| Action, timing and camera movement | Provisional action/timing/camera labels; Transmission timed hold | Input image/video/audio roles observed; motion/audio contents unknown | No corpus property-specific metadata coding | Literal duration/multi_shots/audio retained; possible scope mismatch is unadjudicated |
| Environment, spatial relations and composition | Provisional components; Ivy placement/scale; RAM foreground/perspective | Inputs observed; geometry/layout contents unknown | Kiss/Detour/Harmony explicitly code names/categories in their scoped 04.4 evidence | Broad preservation can coexist with permitted transformations; no layer/mask inferred |
| Lens/framing, lighting, material and aesthetic intent | Provisional components; original-language spans stay literal | Contents of all attached media remain unobservable | Description availability counted; property specificity and sufficiency not coded | Camera/resolution/control names do not verify appearance or defaults |
| Exclusion and preservation | Provisional components; Staff/Harmony locks and exclusions | Attachment cannot supply a verified invariant | No metadata-derived automatic authority | Nine panel possible conflicts; no population contradiction verdict or fulfilment rate |
| Any property absent from sampled text | Absent only under this model's field-level definition | Cannot conclude it was delegated to an image | Cannot conclude it exists elsewhere | Hidden system context, provider defaults and unsampled properties unknown |

Thus the programme's “carried by attached media” and “contradicted across channels”
columns cannot receive verified property-content counts. We retain **attached,
content unknown** and **possible conflict, unadjudicated**, with the reason for
each unobservable cell. Fifteen of sixteen panel 04.3 assignments establish
attachments; Dry Aged Dreams remains unknown for actual context, with zero
exported inputs. All sixteen 04.4 assignments establish explicit text; three also
explicit metadata at their named units. Those are scoped assignment counts, not
a semantic property census or evidence that all other metadata is absent.

### Step 5 — Short edits, descriptions, structure and reuse, by task/model

The following are **observed structural primary-field** measures. Each mean is
over films with a positive relevant primary-text denominator; film quartiles and
all literal models are retained. Long description means ≥1,000 characters only.
Numbered-shot/count wording includes quoted/negated wording and can match one
numbered shot. No row is a success or model-capability measure.

| Task/model | Films | Short-edit proxy /nonempty | Mean film share | Long-description proxy /nonempty | Mean film share |
| --- | ---: | --- | ---: | --- | ---: |
| image | 155 | 4116/87238 | 6.19% | 61005/87238 | 61.49% |
| video | 156 | 214/37079 | 0.64% | 33892/37079 | 87.56% |
| audio | 10 | 0/132 | 0.00% | 38/132 | 20.02% |
| nano_banana_2 | 138 | 1715/25355 | 8.27% | 15297/25355 | 59.30% |
| seedream_v5_pro | 96 | 876/21136 | 6.00% | 15772/21136 | 67.35% |
| gpt_image_2 | 120 | 545/14397 | 3.89% | 10448/14397 | 64.45% |
| seedance_2_5 | 145 | 166/31082 | 1.26% | 28982/31082 | 89.93% |

Across all 157 films and 124,449 nonempty primary fields:

| Feature | Positive fields /124,449 | Mean film share /157 |
| --- | ---: | ---: |
| section | 46766 | 35.45% |
| structured_json | 530 | 1.05% |
| xml_like | 0 | 0.00% |
| reference | 60227 | 51.38% |
| multi_shot | 9428 | 10.04% |
| repeated_lines | 2930 | 3.35% |
| repeat_excess | 63042 | 38.45% |
| long_text | 8742 | 7.58% |

Repeat excess is additional exact primary occurrences within a film, not within-field
repeated lines; neither is waste or revision intent. XML-like absence is under
one lexical rule, not proof of no structured prompts. Structured JSON remains
instruction text. The all-role `by_*` files separately include metadata and nested
fields; use `primary_by_*` and `primary_summary_*` for the primary comparisons above.

| Cohort | Films | Reference-token fields /nonempty primary | Mean film share | Short-edit fields /nonempty primary | Mean film share |
| --- | ---: | --- | ---: | --- | ---: |
| shortlist_only | 62 | 22012/42425 | 51.98% | 1530/42425 | 3.50% |
| most_watched_only | 55 | 16250/29970 | 50.51% | 1159/29970 | 4.64% |
| both | 40 | 21965/52054 | 51.66% | 1641/52054 | 3.89% |

The same-model comparisons describe requests given to the literal model, with
no provider normalisation. Model interface, operation mix, language, capture,
creator overlap, duration and production scale are competing explanations.
All cohorts, orientation and scale summaries preserve Study 01's thresholds;
no useful category split exists (primary catalogue categories are empty arrays).
Small groups stay descriptive. There is no causal or quality interpretation.

Within the **same 4,633 successful sample texts**, the preservation regex and
27B agree positively in 1,318; 99 are lexical-only, 1,668 semantic-only and
1,548 neither. Lens/framing has 822 semantic-only; camera vocabulary has 746
lexical-only. These are descriptive disagreement counts against provisional
labels, not regex precision/recall against ground truth. Per-film cells are in
[lexical_semantic.csv](outputs/lexical_semantic.csv). The component agreement,
367/5,000 failures and 5,922/61,422 long exclusions continue to apply; these
paired observed cells describe only the successful sample, with no transport
or population claim. They explain why earlier lexical definitions are retained
as structure and qualified rather than silently replaced.


These additional **27B provisional** comparisons condition on successful assigned
sample texts and use the same stratum weights. Component agreement is camera
0.873/0.892 (gold/Jev), timing 0.824/0.885, preservation 0.875/0.590;
preservation's 976/4,633 global cross-check disagreements remain material. There
is no independently validated subgroup agreement. Long counts below are actual
source stratum/text memberships in that subgroup, not assigned sample records.
Excluded-long component presence is unidentified, bounded only by 0–100% in
each subgroup; the global all-length envelopes above must not be applied as
model-specific bounds. Model weighting is descriptive and not calibrated to
population model counts.

| Task/model | Component | Successful /sampled texts | Measured films | Weighted film mean; pooled | Conditional failure envelope | Long /all-length memberships |
| --- | --- | --- | ---: | --- | --- | --- |
| image | camera_motion | 2257/2338 | 155 | 8.90%; 13.36% | 12.58–16.50% | 241/33954 |
| image | timing | 2257/2338 | 155 | 3.02%; 4.67% | 4.31–8.23% | 241/33954 |
| image | preservation | 2257/2338 | 155 | 47.21%; 49.31% | 47.16–51.08% | 241/33954 |
| video | camera_motion | 2337/2622 | 156 | 90.53%; 91.23% | 79.88–92.08% | 5682/27623 |
| video | timing | 2337/2622 | 156 | 89.41%; 90.62% | 79.27–91.47% | 5682/27623 |
| video | preservation | 2337/2622 | 156 | 82.69%; 83.64% | 72.92–85.11% | 5682/27623 |
| nano_banana_2 | preservation | 641/663 | 103 | 50.79%; 51.94% | 50.15–53.31% | 34/10448 |
| seedream_v5_pro | preservation | 484/503 | 68 | 49.87%; 49.64% | 47.98–51.29% | 120/9260 |
| gpt_image_2 | preservation | 483/500 | 81 | 52.24%; 59.88% | 56.49–61.88% | 83/8017 |
| seedance_2_5 | preservation | 1802/2026 | 140 | 84.16%; 86.20% | 75.48–87.35% | 5453/23119 |

Timing and camera instructions are more frequent in the sampled video task
contexts under these definitions; this is an **association**, not model behaviour,
output motion or proof that any context is better. The source populations, tasks,
languages, model interfaces and repeated text differ. Semantic cohort breakdowns
with successful/sample counts, film quartiles, failure envelopes, and local long
exclusions remain in the semantic summaries; their interpretation has the same
limits as these task/model rows.

### Step 6 — Conflicts, overload and changes along revision chains

Nine 04.6 cases retain **inferred possible conflicts /16 assignments**, seven
unknown. Birthdays' four views/three panels could combine views in one panel;
Fallen Leaves' stationary/drifting camera could express observational style;
KAGEROU's colour print/monochrome could distinguish print from capture; Staff's
no-speech/appended speech could concern separate drafts. Harmony, Ivy, Prophecy,
RAM and SNAP pair requested timing with differing literal duration. Content and
container scope, approximation and stale drafting are alternatives. No media
conflict or model response was observed. Exact paired spans, raw controls and
compound task keys are in the evidence/context ledgers; no duration unit or
provider behaviour is invented.

Long text occurs in 8,742/124,449 primary occurrences (7.58% mean film share /157)
and long distinct texts are excluded from semantics as above. Repeated-line
matches occur in 2,930/124,449 fields (3.35% mean). Neither threshold measures
overload, contradictory constraints, attention limits or performance degradation.
No matched outcome experiment, model token budget or hidden-context inventory
supports an overload rate. Long texts have more camera/exclusion matches in v2's
structural audit; that cannot identify their semantic prevalence or bias direction.

[revision_contexts.json](outputs/revision_contexts.json) checks all seven named
09.3 comparisons against current source keys/text hashes and retains their
literal models, lengths, controls, comparison order and sample status. Six are
explicit producer-to-consumer comparisons; Detour is comparison order only.
Kiss title position/size, Ivy paint, Lost continuous-shot constraint, Prophecy
machine properties, RAM wear, SNAP framing and Detour reference change remain
scoped **inferred** deltas backed by Study 09's named spans/edges. All fourteen
endpoints are `not_sampled`; there is no paired 27B component change denominator.
Zero labelled endpoint pairs is missing evidence, not zero semantic revisions.
Character growth is not specificity; complete input-set equality is not a common
shot; preparation edges are not automatically revisions. We consume the merged
Study 09 distinction rather than inventing semantic family membership.

### Step 7 — Context-assembly contract

[context_contract.json](context_contract.json) proposes seven layers: project
rules, entity context, scene state, shot/task, attached assets, constraints and
operation-specific instructions. Each claim retains source channel/path, scope,
version, evidence and unavailable state. An explicit property authority can govern
that property; layer order alone creates no precedence. A broad lock beside a
permitted relighting operation requires scope resolution, not automatic deletion
of either instruction. Unknown media contents cannot fill missing properties.

The proposed sequence is: preserve raw fields → resolve chosen compound bindings
and versions → select relevant scoped claims → retain instructions and literal
adapter controls → surface unresolved scope/bindings → record an immutable
assembled request → keep output/use/review/approval separate. Changed sources or
instructions create a new candidate request. Human decisions settle authority,
creative changes and readiness; code validates identities/states; planning models
may propose with evidence. Study 09 supplies the proposed human attempt-cap and
review boundaries. No numeric cap, execution topology or storage design is chosen.
Study 12 must adjudicate and test these behaviours before claiming benefit.

## 5. Fully traced examples and counterexamples

Full keys, paths, short excerpts, labels, competing explanations, denominators
and confidence join the named evidence IDs in `case_evidence.csv`; each job's
literal controls and every actual input occurrence are in `panel_contexts.json`.
The inherited cases supply the semantics, not new whole-film model assignments.
Confidence is high in exact released IDs/fields, provisional and single-coder in
property/context interpretation. No achieved result is asserted.

1. **Ivy — allowed changes beside invariants.** Film
   `d305f6e5-b906-49a1-a0c6-75ef7f653ad8`, `dont-poison-ivy:04.2`–`:04.5`.
   Task `5bc1268c-ccc1-419e-bd13-79344eadf228`, `seedream_v5_pro`, consumes
   room `4ebd698e-e1f7-479d-93b0-4043e5e61913` and plant
   `c16ce530-c7d1-461a-acc8-63b8d7de63b1` at the recorded image input paths.
   “FIRST, SCALE.”, “SECOND, POSITION.”, “THIRD, VIEWING ANGLE.” and
   “FOURTH, LIGHTING.” distinguish permitted transformations from source
   preservation. **Observed** wording/bindings; **inferred** property-scoped
   context. Denominator one named task within 553 inspected/exported jobs.
   Alternative: full resynthesis conditioned on sources rather than a layered
   transplant. False inpaint remains literal; attached object contents and
   preservation success remain unknown.

2. **Birthdays — a short request can need scope review.** Film
   `d51d6821-d191-40f7-949b-1086750a2e93`, `birthdays:04.2`–`:04.6`.
   Task `372eae81-9e4e-4264-adac-febf9565667e`, `seedream_v5_lite`, binds
   tablet `37f689e1-04da-473c-9778-97b61732ec90` at `params.medias[0].data`
   and logo `b38a38ab-607f-4228-93ee-f2d940fdb20f` at `[1].data`.
   “Embross the logo” and “Front, Side, 3/4 and back” coexist with “3 panels”.
   **Observed** text/inputs; **inferred possible conflict**, not an output defect.
   Denominator one task in 170 purposively inspected /1,003 exported jobs.
   Alternative: one panel may contain several views. The short-edit proxy
   cannot prove a complete or unambiguous specification.

3. **THE LAST TRANSMISSION — JSON prose plus an actual image.** Film
   `03f596b0-23da-4312-9e58-2e1cc4582348`,
   `the-last-transmission:04.2`–`:04.5`. Task
   `0a5dad36-f81f-4a32-a38a-bc7bcd103e7f`, `seedance_2_5`, includes
   `"shot_id":"TLT_S02_clock_v2"`, timing `"0-5s"` and `"5-9s"`,
   `"camera":"locked frame on the dial and hands"` and “no voice, no music”.
   Text's image ID `9264c44d-ad74-4ddc-91fc-4490b55a5b18` matches an actual
   input_image at `params.medias[0].data`. **Observed** parsed JSON, binding
   and raw duration=12 /multi_shots=false /generate_audio=true; component
   meanings **inferred**. Denominator one task within 66/66 inspected video
   jobs. Alternative: audio enabled for effects, timing specifies only part of
   a container. No executed controls, media contents, cuts or sound are inferred.

4. **Counterexample — Dry Aged Dreams, structure without disclosed attachments.**
   Film `3777eda4-c15e-4531-9f04-4c02a900f3c3`, `dry-aged-dreams:04.2`–`:04.5`.
   Image task `3e7791d1-6165-4a81-bbaa-575811c1edd8`, `nano_banana_2`, names
   “FOREGROUND:”, “MIDDLE GROUND:” and “BACKGROUND:”. All eleven exported
   usages are outputs; no input attachment is established. **Observed** sections
   and export counts; environment/composition **inferred**, actual context
   unknown. Denominator all 11 inspected/exported jobs. Alternative: omitted or
   external preparation. This counters treating every sectioned prompt as
   reference-bound or missing usages as proof of a text-only production.

5. **Counterexample to English proxies — KAGEROU.** Film
   `51d2c0b2-d692-42b4-b66f-daf87cac1eb3`, `kagerou:04.2`–`:04.4`; full task
   key and three actual image IDs in the ledgers. “人物達の位置は構図の３等分したうちの右側。”
   and “人物を小さく描写。” explicitly request placement/size in the inherited
   reading. **Observed** spans/attachments, component interpretation **inferred**.
   Denominator one task within 489/489 inspected jobs. Language coverage is an
   alternative to semantic absence from an English lexical match; no image
   geometry or model fulfilment is verified.

## 6. Pattern catalogue

These are scoped practices and proposed uses, not tested best practices. Failure
modes are interpretation/workflow risks, never measured generation failures.

| Problem / applicability | Method and inputs | Sequence | Evidence / label | Tradeoffs | Failure mode |
| --- | --- | --- | --- | --- | --- |
| Local change with retained context | Bind base and source; name changes and invariants | Sources → role bindings → scoped permissions → candidate | Ivy/Harmony 04.2–04.5; observed text/input, inferred interpretation | More scope decisions; needs explicit source identity | Broad locks silently overrule permitted changes; no verified pixel preservation |
| Short placement edit | Two sources plus explicit object/region/view instruction | Bind tablet/logo → placement → requested package → review ambiguity | Birthdays 04.2–04.6; observed inputs, inferred possible conflict | Compact text may omit hierarchy | Four views treated as necessarily four panels; output defect invented |
| Full scene/task description | Text sections plus input roles where disclosed | Section task → bind sources → separate invariants/changes | Kiss/Prophecy/Detour 04.2–04.5; inferred case pattern | More repeated context and authority management | Length mistaken for completeness, specificity or overload |
| Structured timed shot | JSON prose, shot ID, image, events, camera, exclusions | Parse text as text → retain raw controls → proposed task | Transmission 04.2–04.5; observed structure/binding | Easier explicit field recovery, still prose semantics | JSON keys promoted to executed controls or actual timing |
| Reference token binding | Preserve token and actual usage tuple | Resolve explicit input position/ID → retain unknowns | Titanic/Kiss/Harmony 04.3; observed | Direct media and named elements coexist | Token match invents an attachment or media property |
| Repeated passages and reruns | Exact text hashes, duplicate-line features, independent candidates | Count equality → inspect complete context → human family decision | Corpus structure; Titanic case; Study 09 families | Deduplication aids counting but loses candidate distinctions if misused | Repetition called waste, failure or identical task without controls/inputs |
| Possible conflicting scopes | Paired spans and literal controls | Preserve both → human adjudicates intended property/task scope | Staff/Birthdays/Fallen Leaves and timing cases 04.6; inferred | Requires judgement; often undecidable retrospectively | Coexisting instructions automatically labelled contradiction/model confusion |
| Source-linked revision | Actual edge or labelled comparison, named property delta | Preserve source → compare allowed change → new candidate → review | Seven Study 09 histories; inferred bounded deltas | Semantic sample has zero endpoint-pair coverage | Longer text/similarity treated as specificity, motive or benefit |

## 7. Studio-implication table

All requirements and behaviours are **proposed**, awaiting the validation tests.
They are information contracts, not a recovered platform architecture.

| Evidence | Requirement or hypothesis | Proposed behaviour | Validation test |
| --- | --- | --- | --- |
| Ivy plant and Harmony seat permissions | Context needs property-level scope | Store invariants, allowed changes, source authority and exclusions separately | Independent reviewers recover the same change/lock scopes; then an authorised controlled task tests fulfilment |
| Titanic/Transmission token-to-actual-input bindings | Source identity must survive assembly | Preserve film-scoped asset/version, raw role/path and unresolved tokens | Cross-film collision and duplicate-path synthetic import preserves identities and source counts |
| Unknown media in every panel case | Missing text cannot be filled from attachment presence | Keep content observability and property evidence per channel | Unseen image leaves identity/material/light content unknown despite an attachment |
| Staff no-speech/appended speech; timing mismatches | Conflict detection is a review aid | Show paired spans, scopes and literal controls; require explicit decision for dependent dispatch | Independent scope adjudication; container/content timing is retained without a fabricated correction |
| Language fields; JSON prose; false controls | Intent and adapter parameters are distinct | Preserve source roles, raw controls and parse diagnostics; no silent defaults | Null/empty/false/zero/invalid round-trip; JSON instruction creates no parameter activation |
| Lexical/27B disagreements and uncertain components | Automated semantic tags need evidence and limits | Expose provisional source/model, exact span or withholding, agreement and missingness | Independently code multilingual/long/rare-role examples, report adjudicated per-component agreement before expanding claims |
| Seven histories with no sampled endpoints | Revision analysis needs paired semantic evidence | Store immutable before/after requests and property deltas, family basis and human confirmation | Paired independent coding of known edges versus shared-input nonrevision controls; no length-only specificity |
| Recurring layered context needs, no outcome data | Scope-filtered assembly may help but is untested | Assemble relevant project/entity/scene/task claims and explicit chosen assets | Authorised fixed-task comparison with baseline, changed factor, repetitions, rubric, budget and independent review; no archive benefit claim |

## 8. Provisional definitions, unresolved measures and handoffs

Our local definitions remain explicit rather than assuming upstream results:

| Provisional definition in Study 04 | Dependency and boundary |
| --- | --- |
| Task = literal generation type for comparisons; semantic purpose only in named cases | Uses merged 05/06/08 routes/roles; Study 12 independently adjudicates purpose and adapters; no original-design census |
| Information location = explicit text/metadata plus actual bindings and unobservable media contents | Study 12 property-authority adjudication and contract tests; hidden/default context and media content cannot be recovered |
| Weighted semantics = N_s/r_s successful-text transport within covered film/type/role strata | Study 12 independent label review, long/rare-role coverage and sensitivity work; no known inclusion probabilities or semantic census |
| Short edit/long description/sections/reference/multi-shot/repeated lines = unchanged v1 structural rules | Study 12 multilingual intent and retrieval validation; no semantic overload or executed-shot claim |
| Conflict = same-property/scope candidate with alternative explanation, not a verdict | Study 12 independent scope adjudication; no model-confusion or outcome count |
| Revision = actual named source relation plus case-coded property change; Detour comparison unordered | Consumes merged Study 09; comparable-family and semantic delta rates remain provisional for Study 12; no missing paired labels invented |
| Seven-layer assembly, scoped authority, immutable requests, readiness and human review | Study 12 synthesis, implementation choices and controlled tests; uses Study 09 review/cap proposal, no persistence/execution architecture selected |

The following table resolves **every earlier provisional definition explicitly
waiting on Study 04** in the named reports' section 8 (Study 10 points back to its
section 3). Confirmed means supported at the original bounded instruction/record
scope, never validated outcomes. Changed means additional provisional sampled
semantics qualify the earlier lexical description; original values stay as
merged. Undecided means these labels cannot settle that dependency. Several
other dependencies in those studies wait on different studies and are untouched.
The machine-readable source is [dependencies.csv](dependencies.csv): 14 confirmed,
8 changed and 13 undecided /35 scoped dependencies.

| Study | Earlier provisional definition | Status | Assessment | Remaining dependency |
| --- | --- | --- | --- | --- |
| 02 | Eight-sentence placeholders and standard regions | undecided | Labels concern sampled generation fields not brief substance | 12 independent brief coding |
| 02 | Section/reference/multi-shot lexical proxies | changed | Retain structural census; semantic components add provisional sample interpretation not scene/shot counts | 12 multilingual and shot-intent adjudication |
| 02 | Seven brief categories and five property correspondences | undecided | No new documentary brief-task links or independently adjudicated property matches | 12 independent adjudication |
| 03 | Disclosed record as element and semantic kind | undecided | Component presence cannot establish persistent entity identity or complete libraries | 07 explicit linkage; 12 synthesis |
| 03 | Environment mapped to location and literal categories | undecided | Environment instruction is not persistent location equivalence or rights verification | 07 linkage; 12 adjudication |
| 03 | Identity/variant from retained and changed properties | confirmed | Scoped case wording supports property distinctions; identity labels remain provisional with high cross-check disagreement | 09 comparable family intent; 12 independent adjudication |
| 03 | Package request or attachment distinct from fulfilment | confirmed | Context joins preserve named inputs but no sheet form is verified | 05/06 operation context; 07 aliases; 12 tests |
| 03 | Property location prose/metadata plus unknown media | confirmed | Matrix separates text and recorded metadata from unseen attached contents | 12 property authority and validation |
| 03 | Reference and preservation regex meanings | changed | Lexical counts stay unchanged; 27B preservation is an additional sampled semantic measure with agreement and bounds | 12 multilingual/adjudicated semantic census |
| 05 | Edit/preservation/reference/lens and short-edit proxy | changed | Semantic preservation/lens estimates are conditional on successful weighted sample; edit intent not a released component | 12 operation-intent adjudication |
| 05 | Integration properties and sheet/plate/poster purpose in cases | confirmed | Spatial/composition/light components are instruction evidence; purpose and media fulfilment remain case-scoped | 12 property/purpose adjudication and controlled tests |
| 06 | AF3a camera/lens/preservation/exclusion/multi-shot/reference | changed | Camera/lens/preservation/exclusion gain provisional sampled semantic measures; multi-shot intent has no matching semantic label | 12 shot-intent validation |
| 06 | Subject/camera/environment/events/audio/invariants in named spans | confirmed | Action/camera/environment/timing/preservation components support instruction decomposition but omit dedicated audio or environment-motion labels | 12 independent task coding |
| 06 | Possible conflict as same-scope candidate | confirmed | Nine panel possible conflicts remain unadjudicated; timing text and controls may have different scope | 12 scope adjudication |
| 06 | Requested shots distinct from jobs and cuts | confirmed | Shot fields and structured prose remain source-path units; labels do not count executed shots | 09 comparable families; 12 validation |
| 07 | Raw compound input reuse or branch | undecided | Instruction labels cannot establish semantic cross-shot or identity equivalence | 09 family intent; 12 adjudication |
| 07 | Within-asset representations and zero cross-ID merges | undecided | No semantic label establishes asset alias equivalence | 09 derivative interpretation; 12 explicit alias evidence |
| 07 | Preservation/reference structural wording | changed | Provisional semantic preservation is available only on weighted successful texts with exclusions and agreement | 12 adjudicated semantic expansion |
| 07 | Inherited semantic strategy/identity case interpretation | confirmed | Text properties remain scoped to named instructions and attached contents unknown; no strategy effectiveness claim | 09 family intent; 12 synthesis/tests |
| 08 | Semantic request role and original design distinct from sheet edit | confirmed | Fourteen components do not identify original design or complete semantic purposes | 12 purpose adjudication |
| 08 | Closed adapter role and video candidate mapping | undecided | Text labels cannot validate adapter capabilities/defaults or implementation | 12 adapter validation |
| 08 | Conservative input route and direct candidate | confirmed | No recorded input never establishes text-only production; semantic labels add no hidden context | 09 family scope; 12 validation |
| 08 | Reference preparation/foundation distinct from verified sheet/keyframe | confirmed | Actual bindings and requested properties remain independent of fulfilment and timing | 09 use/approval; 12 validation |
| 08 | Branches/chains/convergence/cross-model from explicit parents | undecided | Component overlap cannot prove common shot/entity or revision motive | 09 comparable families; 12 adjudication |
| 08 | Within-ID raw/preview and unresolved origins | undecided | No media or new alias evidence introduced | 09 derivative meaning; 12 explicit evidence |
| 08 | Edit/preservation/reference/multi-shot lexical indicators | changed | Preservation gains bounded provisional semantic estimates; edit and multi-shot remain lexical/case scope | 12 intent adjudication |
| 09 | Separate structural family bases | undecided | Same semantic components do not establish same task or ordered revision family | 12 independent comparable-family validation |
| 09 | Adjacent Jaccard/time retrieval screen | undecided | Sample is not paired to validate retrieval recall/precision and cannot recover omitted relations | 12 retrieval adjudication |
| 09 | Equal request rerun candidate and unordered alternatives | undecided | Component labels establish neither motives nor concurrency | 12 human validation |
| 09 | Exact/token/length deltas and case-only specificity | confirmed | Named source-linked property changes remain distinct from character growth; sample cannot supply a semantic delta census | 12 paired semantic coding |
| 09 | Preservation/edit markers and appearance/disappearance | changed | 27B preservation can qualify successful sampled fields but sparse pairs cannot replace lexical delta census | 12 paired semantic validation |
| 09 | Raw input differences and replacement candidates | undecided | Unseen media and text components do not establish equivalent input replacements | 12 family/alias validation |
| 09 | Top-level scalar control subset | confirmed | Raw control states stay beside instruction text; hidden defaults and omitted nested semantics unknown | 12 adapter validation |
| 09 | Local correction/derivative/specificity scoped to cases | confirmed | Seven histories retain named property changes with sample availability explicit; no motive/defect/outcome | 12 independent adjudication |
| 10 | Exact-string repeat excess distinct from instruction components | changed | Repeated-line census and successful weighted component estimates add descriptions; semantic duplicate or waste rate remains unavailable | 09 family context; 12 paired semantic coding |

Studies 02, 03 and 05–10 remain byte-for-byte as merged. The table does not
retroactively assign sample labels to all their jobs or close missing semantic
family, alias, version, approval, purpose or media dependencies. Study 11 receives
descriptive cohort context, no winner labels or comparison to uncollected films.
Study 12 receives a traceable proposed assembly contract and validation backlog.

The evidence **does not allow**: a semantic corpus census or unbiased population
prevalence; property contents delegated to attached media; verified cross-channel
contradiction rates; hidden provider/system defaults; complete scripts or executed
shot counts; semantic edit/purpose/audio/environment-motion prevalence from these
fourteen components alone; overload or optimal prompt length; paired semantic
component deltas in the seven histories (0/7 covered pairs); complete equivalent
revision/alias/version families; semantic duplicate/waste rates; actual timing,
control effects, preservation, continuity, quality, final screen use or acceptance;
benefits of a format, model, assembly or revision strategy; generation failure,
retry/rejection, labour, cost, speed, productivity, agents or internal orchestration.
Long/failure extremes quantify sensitivity conditional on transport, not any of
these missing outcomes.

## 9. Reusable code, outputs and reproduction

From the repository root, choose new download directories:

```bash
uv sync --locked
uv run python scripts/fetch_data.py
gh release download prompt-labels-v1 --dir data/af11-labels-v1
gh release download prompt-labels-v2 --dir data/af11-labels-v2
uv run python prompt-labels/release.py --check data/af11-labels-v2
uv run python studies/04-prompts/build.py
uv run python scripts/fetch_data.py --output data/af11-fresh
gh release download prompt-labels-v1 --dir data/af11-fresh-v1
gh release download prompt-labels-v2 --dir data/af11-fresh-v2
uv run python studies/04-prompts/build.py --data data/af11-fresh \
  --v1 data/af11-fresh-v1 --v2 data/af11-fresh-v2 \
  --output data/af11-reproduced --check
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/check_repository.py
```

The build checks all source assets against their checksum manifest, v1 checksums,
and the complete offline v2 release check; no journals or other local working data
are read. `--check` requires a separate output directory and compares every byte,
including reproduction.json. The integration test runs when all three releases
are present; CI without them explicitly skips it, testing synthetic boundaries
and committed input/output hashes. Tests contain no actual source records.

| Output / code | Grain, denominator and provenance |
| --- | --- |
| taxonomy.json; context_contract.json; dependencies.csv | Prompt axes, proposed seven-layer assembly, complete 35-row dependency assessment |
| eligibility.csv; field_states.csv; coverage.json | Unchanged 187-row Study 01 Study 04 register; film/role/state field counts; global and overlapping membership denominators, source/span checks |
| film_metrics.csv; metric_evidence.csv; summaries.csv | Primary fields per film; source/compound-key scope and numeric excerpts; all/cohort/orientation/scale film means, quartiles and pooled counts |
| by_*.csv; summary_*.csv | All-role film × literal type/model/role counts and conditioned film summaries; language metadata remains in other_text |
| primary_by_*.csv; primary_summary_*.csv | Primary-only type/model pattern counts and summaries; nonempty field denominator, no metadata dilution |
| distinct_structural.csv | Film × all-role distinct exact texts and structural positives; film/text denominator, separate from source occurrences |
| semantic_evidence.csv | 157 inferred semantic provenance rows with numeric excerpts, exact assigned-source scope, denominators, alternatives and confidence |
| semantic_strata.csv | 481 candidate strata, assigned/success/failure counts and both weight definitions; zero coverage remains visible |
| semantic_by_*.csv; semantic_summary*.csv | Assigned 27B sample film/type/model/role positive counts and transported weighted masses; successful/sample/failure counts, subgroup long membership counts with unidentified component bounds 0–1; per-film first, weighted pooled alongside; agreement and long/failure-bound joins explicit |
| semantic_bounds.csv; agreement.csv | Fourteen conditional failure/uncovered/long sensitivity envelopes, raw failure extremes; four agreement comparisons' per-component contingency counts and paired-text denominators |
| information_matrix.csv; information_locations.json | Film/component explicit provisional text and observed channel coexistence with success/mass denominators; sixteen scoped original location assignments; all media property contents unknown |
| case_evidence.csv; panel_assignments.csv; panel_contexts.json | All 96 unchanged 04.x assignments, audit /16, exact named inputs/reference states and raw controls with full evidence metadata |
| lexical_semantic.csv | Film × four component confusion cells /successful texts; lexical versus provisional labels, not accuracy against ground truth |
| revision_contexts.json | Seven named 09.3 histories, exact current keys/hashes, model/control/length deltas and explicit missing semantic endpoint coverage; full spans/edges in unchanged Study 09 |
| reproduction.json | Three release checksum-manifest hashes, code/SQL/taxonomy/contract/dependencies/design/register/report/case hashes and every generated output hash |

No full prompt is committed; published bounded case excerpts are retained.
All outputs are below 1 MB each, so no `study-04-v1` release is needed. Original
data, programme, prompt-label tools/releases, Study 01, cases and other study
folders are unchanged. No data-directory file, machine-specific path or local
user name is committed. Validation results and the merged PR state are recorded
in the task handover.
