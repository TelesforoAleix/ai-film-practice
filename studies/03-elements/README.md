# Study 03 — Reusable elements

## 1. Answer and limits

Creators represent persistent subjects, places and objects through **named
reference metadata, direct asset packages and explicit prose constraints**. In
this export, 120/157 primary films disclose 5,200 element records; all have a
recorded attachment and 4,577/5,200 recur across distinct jobs. This measures
parameter disclosure and further-work use, **not a complete library, semantic
identity census, canonical approval or evidence that reuse improves results**.

Identity and variation are separable in instructions: an age, mark, logo, wear
state or framing can change while other properties are explicitly retained.
Six of the 16 panel assignments support an **inferred derivative** through an
actual producer/input link plus a named change. Nine establish task-scoped
reference authority. Neither establishes project-wide approved versions. Names
containing v2, frequent use and distinct outputs supply none of those decisions.

A requested sheet is not an attached, verified sheet. The panel includes single
views, multi-angle requests, expressions, locations, a described blockout and a
named element; one multi-angle request is a video turn. Media contents remain
unobservable. The studio response is **proposed**: persistent identity, source
media, descriptions, variant axes, version relationships, scoped authority,
explicit approval and use history stored separately, then tested.

Only the selected cohort has detailed records; these findings cannot establish
what separates top films from other films. No media was retrieved or watched;
no story, aesthetics, quality or continuity was judged. No agents, internal
orchestration, labour, cost, failure rate or causal benefit is inferred.

## 2. Population, coverage, units and denominators

The unchanged Study 01 [eligibility](../01-corpus/outputs/eligibility.csv), filtered
to Study 03, primary and production-eligible, supplies **157 films / 130,704 jobs**.
Of the 186 priority films, 23 non-open-source listings were excluded and six
public workspaces unavailable. Cosmic tracks, the supplemental pilot with 23
additional element records, contributes to no measure here. None of the 49
unusual projects is removed or winsorized. The 151 literal creator handles in
Study 01 mean films are not independent creators.

| Unit or gate | Denominator / evidence boundary |
| --- | --- |
| Primary film | 157; 62 shortlist only, 55 most watched only, 40 both |
| Disclosed element record | 5,200 compound `(film_id,reference_element_id)` keys in 120/157 films; zero disclosure in 37 is not absence of an element strategy |
| Recorded job | 130,704 compound film/generation keys; named-reference shares include every job, including missing text |
| Primary text | 124,449 nonempty, 1,083 explicitly empty, 5,172 unavailable; lexical shares divide by nonempty fields only |
| All-role structural check | 61,626 film-distinct exact-text pairs across 157 films after primary/nested crosswalk; a text shared between films is counted once in each |
| Direct inputs | 29,906 raw compound asset IDs; 337,692 distinct film/consumer/asset pairs in 156/157 films; role/path duplication does not add consumers |
| Panel meaning | 16 purposive films × six unchanged 03.x codes = 96 scoped assignments; unequal reading scopes, single coder, no prevalence extrapolation |
| Element recurrence | At least two distinct attached jobs per compound reference ID; not repeat occurrences in one job |
| Input recurrence | At least two distinct consuming jobs per raw compound asset ID, including external/unresolved inputs; cross-ID aliases remain unresolved |

Every summary reports eligible and measured films. A ratio with no denominator
is unavailable, never zero. A film with no disclosed elements remains in
job-based comparisons, but has no measured element-recurrence share. The
120-film element denominator and 157-film job denominator must not be interchanged.

## 3. Method, codebook and automated checks

[build.py](build.py) loads the verified `data-2026-10-20` release with
`film_practice.connect`, registers eligibility and executes [measures.sql](measures.sql).
Source views remain strings; derived parsing does not repair the original data.
All joins are film-scoped. Input roles are enumerated in SQL, including generic
`input_asset`; these can be presets and are not automatically media frames.
Producers require `assets.generation_id` plus an existing job in the same film;
self-consumption supplies no creation edge.

The unit of an element is initially a **disclosed metadata record**, not a
resolved semantic entity. Name/category/description states and literal category
counts are retained. An attached element requires an exported non-output usage
with its reference ID. Multi-asset element means more than one distinct attached
raw asset ID across its disclosed uses; it does not mean a multi-angle sheet or
multiple versions. The export is disclosure-conditioned, so all records being
attached cannot imply complete-library utilisation.

Codebook **1.0**, codes 03.1–03.6, stays unchanged. All 96 case assignments,
including unknowns, are preserved in [case_evidence.csv](outputs/case_evidence.csv).
They retain exact keys, source paths, excerpts, evidence labels, alternatives,
denominators and confidence. Their source ledgers and narratives are hashed.
Package opening spans, named package jobs, derivative endpoints, actual input
edges and the additional short change/identity spans in [readings.json](readings.json)
are checked against the release. No second coder or semantic model labels exist.
Counts of coded examples are audits of these assignments, not corpus prevalence.

Corpus lexical measures reuse AF3a's exact **reference-token and preservation
regular expressions**, without a new semantic classifier. Primary fields count
once per job. A separate all-role check deduplicates exact text within film and
asserts equality with AF3a on all 157 films for text denominators and both match
counts. Nested primary copies must equal their primary source before removal;
language metadata in the all-role check is not a new instruction. The
[lexical audit](outputs/lexical_audit.csv) gives first sorted positive/negative
panel keys where available, exact match offsets/hashes and bounded spans.
These are correspondence checks, not semantic precision, recall or agreement.
English wording, negation, quoting and boilerplate limit interpretation.

`reference_elements` in parameter JSON has separately counted unavailable,
empty-document, invalid, non-object, absent, null, empty-array, nonempty-array
and other-value states. Array presence does not itself establish an attachment,
an enabled feature or media content. The independent usage table is authoritative
for attachment measures. Nine malformed released strings remain invalid; they
supply no JSON-derived controls, while independent usages remain usable.

Every numeric row joins [metric_evidence.csv](outputs/metric_evidence.csv) on
film ID for study, whole compound-key scope, query/source paths, numeric excerpt,
alternatives, denominators and confidence. Literal type/model/category rows add
their exact filter to that scope. Aggregate film sets are recorded in
`summaries.csv`; type/model member sets are recoverable from their per-film
rows, literal dimension and cohort. Counts are **observed**; semantic mappings
and derivatives are **inferred**; brief accounts retain **creator-stated**;
schemas and requirements are **proposed**. No experimentally supported claim
is made. Quartiles use linear interpolation; they describe variation in this
frozen cohort, not sampling uncertainty. No independence-based significance
or population-confidence interval is claimed.

## 4. Findings through the six programme steps

### Step 1 — Classify reusable entities

The [element ontology](ontology.json) covers the programme's eleven classes,
with evidence anchors and boundaries. They can be independently reusable
records **or properties attached to an entity/task**; an adjective does not
create a persistent element automatically.

| Kind | Scoped evidence / interpretation | Boundary |
| --- | --- | --- |
| Character | Birthdays 03.2: same man, age change with retained facial identifiers | An age state need not be a new identity |
| Outfit | Titanic 03.1: separate subject and wardrobe image bindings | A garment reference is not a second character |
| Pose / expression | Staff 03.3: poses and expressions with identity retention | State differs from identity; fulfilment unknown |
| Location | Fallen Leaves 03.1/03.3: environment metadata and location angles | Mapping environment to location is inferred |
| Layout | Kiss 03.4: supplied input described as a 3D layout blockout | Media geometry unobservable |
| Prop | Birthdays 03.5: electronic pad with logo/panel changes | Explicit source link, inferred derivative |
| Material / wear | RAM 03.5 and narrative: worn, taped Commodore request | No verified surface content |
| Palette | Detour 03.6: separate colour-reference role | Authority is property/task scoped |
| Lighting | Detour 03.6: separate lighting-reference role | Time of day alone cannot supply illumination |
| Style reference | Staff 03.2: preserve original art style | A style constraint need not be an independent style asset |
| Voice reference | No established scoped 03.x panel example | Unknown, never inferred from audio-job counts |

Observed literal categories across **5,200/5,200 disclosed records** are:
character 1,383; auto:character 779; character_ip_verified 13; environment 1,008;
auto:environment 547; environment_ip_verified 108; prop 855; auto:prop 492;
auto 11; other 4. These are metadata labels, including literal `ip_verified`
suffixes, **not our verification of identity, rights or media**. They cannot
supply an eleven-class semantic inventory. Per-film literal counts are in
[reference_categories.csv](outputs/reference_categories.csv).

Per film, element-count median is **21**, IQR **1–51**, range **0–177**, over
157 films. The case assignment 03.1 is coded in 15/16 films and unknown in Dry
Aged Dreams. It demonstrates reusable-entity evidence outside the metadata
register, especially SNAP/Titanic/Transmission; it is not a count of all entities
in those films. Corpus-wide semantic entity and variant totals are unmeasurable
without uncoded links and the unavailable complete libraries.

### Step 2 — Separate identity and variation

The unchanged 03.2 assignments contain identity constraints in **14/16 cases**;
Birthdays and Detour additionally carry `variant_instruction` (**2/16**).
Titanic and Dry Aged Dreams remain unknown for this particular code. These
are bounded assignments, not exhaustive variation prevalence. The ontology
keeps persistent subject/object identity, variant state and representation
revision separate; matching names or appearance never merges source keys.

Across **151/157 films**, preservation wording matches **39,918/124,449 nonempty
primary fields (32.08% pooled)**; equal-film mean **31.78%**, median **27.37%**,
IQR **13.46–46.75%**, measured over 157 films. Of positive fields,
**36,908/39,918** have an actual input (92.46% pooled; **93.46%** mean over the
151 films with positive fields). This is coexisting wording and attachment,
not measured preservation or a same-identity success rate. Missing input rows
cannot prove reference-free work. Semantic labels and Study 04 must refine
what is retained and changed; Study 09 must refine revision-family intent.

### Step 3 — Classify reference packages

Code 03.3 establishes **15/16 scoped examples**, with Dry Aged Dreams unknown:
11 multi-angle assignments (one also location_board), one expression_sheet,
one single_image, one generic_reference_sheet, one named_element. These labels
overlap in the location case and describe named requests/attachments, not verified
media. **Transmission's multi-angle request is video**, not a still sheet.
Kiss 03.4 separately describes an attached blockout input. No standalone
style-sheet example is established by these scoped 03.x assignments; style
constraints/roles do not establish a sheet. No style-sheet or voice-package
prevalence can be estimated.

[reference_packages.json](outputs/reference_packages.json) contains all 16 scoped
assignments with literal model/type, actual input bindings and output-use rows
for each named package task. The output-use rows are observed attachment
occurrences, not independent consumers or verified package content; multiple
role/path representations can refer to the same use. Empty use lists mean no
exported resolved use for that named output, not no later use anywhere.

Across 120 element-bearing films, **218/5,200 element records** have more than
one attached raw asset ID: 4.19% pooled; **4.41% equal-film mean**, median zero,
IQR **0–6.68%**, with such records in **49/157 films**. Those can be substitutions,
raw/preview representations or several media; this count cannot classify sheet
form, package completeness, semantic equivalence or version transitions.

### Step 4 — Locate each property's specification

All **16/16 scoped 03.4 assignments** establish properties in prose; one
(APEIROPHOBIA) also codes reference metadata explicitly. This does not imply
that the other films lack metadata: the assignments attach to different named
units. [property_locations.json](outputs/property_locations.json) preserves
each original assignment beside explicit unknown media/parameter semantics.

| Channel | Observed coverage and property examples | What remains unknown |
| --- | --- | --- |
| Prose | 124,449 nonempty primary fields / 130,704 jobs; panel spans specify identity, wardrobe, layout, dimensions, changes and invariants | Unlabelled corpus property frequencies; fulfilled properties |
| Reference metadata | Name and category nonempty in 5,200/5,200 records; descriptions nonempty 548, explicitly empty 484, unavailable 4,168 / 5,200 | Whether descriptions fully specify identity; media properties; complete-library metadata |
| Attached assets | Inputs in 112,516/130,704 jobs (86.08% pooled; 86.86% equal-film mean /157); distinct source IDs and roles preserved | No appearance, material, palette, lighting or voice property is assigned from media contents |
| Parameters | Reference key absent 42,890; empty array 48,524; nonempty array 39,281; invalid JSON 9 /130,704; all other document/key states measured zero | Container presence is not identity semantics or activation; independent controls retain literal model meaning |
| Mix | Panel identity/prose plus input bindings; APEIROPHOBIA includes explicit reference metadata too | Cross-channel contradiction and which channel actually conditioned a result |

Reference tokens occur in **60,227/124,449 nonempty primary fields**, across
147/157 films. Only **39,278/60,227 token-positive jobs** have a named element
attachment (65.22% pooled; 63.69% mean across the 147 positive films). Tokens can
bind direct inputs, remain unresolved, or be lexical noise. They are not a
reference-library count. This extends Study 02's token measure with actual
attachments; Study 04 still owns the semantic information-location matrix.

### Step 5 — Trace creation, reuse and authority

All **5,200/5,200 disclosed elements** have at least one exported use; the
register arises from disclosed parameters, so this is **not 100% library adoption**.
**4,577/5,200** have at least two distinct consumer jobs (88.02% pooled;
**85.90%** equal-film mean across 120 element-bearing films; median **92.40%**,
IQR **83.13–96.56%**). Use is for further work, not final acceptance.

Raw-ID input reuse independently reproduces Study 10: **20,869/29,906 raw input
IDs** have at least two consumers (69.78% pooled; 69.53% equal-film mean across
156 input-bearing films). These assets need not be named elements. Cross-ID
raw/preview equivalence is unresolved; representations within one asset ID
never add another identity. No semantic duplicate or alias-collapsed count follows.

Of **112,516 input-bearing jobs**, **72,863** resolve at least one input to a
different recorded producer job (64.76% pooled; 61.25% mean over 156 input-bearing
films). This is creation/use visibility, not a rate of version creation. Unresolved
external inputs remain present without an invented producer.

[versions.json](outputs/versions.json) traces all **six coded 03.5 assignments /
16 cases**, with exact endpoints, models, role/path edges and source-checked
changed-property spans. Ten assignments remain unknown. The six are inferred
derivatives, not explicit version IDs or approval events. The machine example
also requests a structural/base change alongside “shapes are unchanged”; a
single summary such as palette-only variation would hide that ambiguity.

[authority.json](outputs/authority.json) preserves **nine coded 03.6 assignments /
16 cases**, with seven unknown. Each positive is bounded to its named task or
properties. Detour's master-source binding remains unresolved because its token
is missing. These examples supply no project-wide canonical declarations or
canonical-versus-frequent prevalence denominator. Frequency is never promoted
to a declaration; a task declaration never approves a whole library.

### Step 6 — Minimum studio information and versioning

[schemas.json](schemas.json) is a **proposed** JSON Schema, not implemented
storage or a change to existing contracts. Its minimum records are:

| Record | Required information | Evidence need |
| --- | --- | --- |
| Element | Film-scoped identity; interpreted kind and literal source category; name, description state/evidence; identity claims; variant axes; version and external-reference keys | Duplicate/auto/version-like names do not decide equivalence; prose-only and direct-asset elements exist |
| Version | Own key and element key; source assets/producer provenance; property claims with channel/state/scope; package form and request/attachment/review state; parent relationships | Six inferred derivatives; requested sheets and linked outputs are different facts |
| Relationship | Parent version; explicit revision versus inferred derivative versus proposed variant; changed-property claims; identity basis and evidence | Explicit edge plus named change, without invented approval |
| Authority | Named properties, task/scope, source binding resolved or unresolved, source asset and declaration evidence | RAM's table-only authority; Detour's unresolved master token |
| Review | Explicit status, actor, decision event, scope and evidence; unknown is allowed | Reuse and local authority cannot approve a version |
| Use history | Consumer, source asset/version context, reference ID, literal role/path, evidence; meaning is further work | Direct and named inputs coexist; occurrence rows must be deduplicated for consumer counts |

Every property claim carries an evidence state and source channel. Unknown and
unavailable values require null; explicit empty retains its own state/value.
Proposed behaviour requires same-film integrity, acyclic version relations,
valid parent/source IDs, immutable version provenance and actor/event-backed
approval. Shape validation alone cannot enforce cross-record integrity, prove
media verification or implement approval. A human must resolve ambiguous identity
and property scope. Studies 07/09/12 refine and validate these requirements.

### Task, literal model and cohort comparisons

Task is provisionally **literal generation type**, not operation intent. All
per-film type/model rows precede aggregation. A model/type mean includes films
with that model/type and a positive relevant denominator; absent model rows are
not silently treated as measured model use.

| Type | Named-reference jobs / type jobs | Mean within-film share (film denominator) |
| --- | ---: | ---: |
| Image | 15,043/92,058 | 16.46% (155) |
| Video | 24,238/38,508 | 56.96% (156) |
| Audio | 0/132 | 0% (10) |
| Text; image_3d; unavailable type | 0/1; 0/1; 0/4 | 0% (1; 1; 2), descriptive only |

| Literal model, five largest job denominators | Named-reference jobs / model jobs | Mean within-film share (films with jobs) |
| --- | ---: | ---: |
| seedance_2_5 | 21,733/31,082 | 61.29% (145) |
| nano_banana_2 | 4,582/25,355 | 14.25% (138) |
| seedream_v5_pro | 5,536/21,136 | 22.81% (96) |
| gpt_image_2 | 3,249/14,397 | 22.84% (120) |
| soul_cinematic | 0/7,696 | 0% (65) |

| Cohort | Element-bearing films / films; disclosed records | Named-reference jobs / jobs | Mean per-film job share |
| --- | --- | ---: | ---: |
| Shortlist only | 50/62; 2,080 | 16,038/45,497 | 36.40% (62) |
| Most watched only | 40/55; 1,562 | 9,839/31,169 | 28.83% (55) |
| Both | 30/40; 1,558 | 13,404/54,038 | 32.18% (40) |

Across all 157 films the named-reference job share has mean **32.67%**, median
**34.61%**, IQR **0.09–55.72%**, versus **39,281/130,704 = 30.05% pooled**.
The full outputs retain every literal model/type/cohort, quartiles and measured
film denominators, including tiny subgroups and undefined text shares. Different
model input interfaces, type mix, capture, repeated requests, creators, duration
and scale are competing explanations. These are descriptive associations within
the selected cohort, not model effects, effectiveness rankings or evidence of
jury/audience preferences for a method. No provider is inferred from a nickname.

## 5. Fully traced examples and counterexamples

Each example joins the named 03.x entries in `case_evidence.csv`; that ledger
supplies full source paths, excerpts, evidence labels, competing explanations,
denominators and confidence. `reference_packages.json` and `versions.json`
add actual attachments/endpoints. Prefixes in other tables are never global keys.

1. **Detour: package creation and marked derivative.** Film
   `d90fe8bd-3329-40b3-963c-d9b33075aec1`, `detour:03.2`–`:03.6`.
   Producer/asset `006dcc36-ec37-490f-9890-9524e3ed0ddd` requests three views
   of the same figure; consumer `011fbb97-732a-416b-825f-a9635b313b86`
   (`seedream_v5_pro` → `gpt_image_2`) takes that exact asset at
   `params.medias[0].data`. It requests “a small mark of tomato ketchup” while
   retaining face, clothing and sheet layout. Edge/request **observed**;
   derivative **inferred**, approval unknown. Scope: named edge within
   219 inspected / 6,162 exported jobs. High confidence in IDs and exact spans;
   moderate in version interpretation. Alternative: a local candidate edit,
   without a persistent version decision. The separate master-source statement
   cannot bind an asset when the source token is missing.

2. **Birthdays: identity variation differs from prop revision.** Film
   `d51d6821-d191-40f7-949b-1086750a2e93`, `birthdays:03.2`–`:03.5`.
   Age task `03fbd60d` retains facial hair, iris, outfit, background and lighting;
   its full key is in the ledger. Independently, tablet producer/asset
   `37f689e1-04da-473c-9778-97b61732ec90` feeds
   `372eae81-9e4e-4264-adac-febf9565667e` at `params.medias[0].data`
   (`seedream_v4_5` → `seedream_v5_lite`), alongside a separate logo input
   `b38a38ab-607f-4228-93ee-f2d940fdb20f`. Logo placement and panel changes
   are observed requests; the tablet derivative is inferred. Scope: 170
   inspected / 1,003 exported jobs. Confidence: exact attachment and change
   spans, single-coder identity interpretation. Alternative: independent
   requested candidates; no approved age/prop version lineage is disclosed.
   Four named views versus three panels remains an unresolved scope issue.

3. **RAM: a worn object and property-scoped authority.** Film
   `e99b5ad2-8f58-4ef8-a13c-4441cfdd5205`, `random-access-memories:03.5`/`:03.6`.
   Commodore package producer/asset `a5620e3d-120b-4dd5-ad46-ccb087640437`
   conditions `d0efc423-f288-4e29-9665-e2bd10b23b29` at
   `params.input_images[0]` (`gpt_image_2` → `nano_banana_2`); the consumer
   requests wear, tape, scratches and dents. A separate table instruction
   `3123d068` limits reference authority to shape, wood, wear and dressing,
   excluding framing/light (full keys in authority ledger). Scope: 482/482
   job contexts. Link and wording observed, derivative inferred; no independent
   identity-preservation span is assigned to the short wear request. Alternative:
   a new candidate from an input rather than an approved replacement. Confidence
   is high in the edge, bounded for identity/version meaning, with no media check.

4. **Counterexample: SNAP has no disclosed element register but a package route.**
   Film `aed4098b-3278-4e5d-a347-24fad9cfb9ae`, `snap:03.1`–`:03.3`.
   Package producer/asset `16536627-0f5a-4ac8-bdb8-b9d43902785a` asks for
   front/back/portrait views of the same person; consumer
   `0d9a690f-3ac3-4886-bb34-fa70159ca8dc` actually consumes that output at
   `params.medias[0].data`. Both are image jobs in the exported records;
   the route is local preparation, not a complete build order. Scope:
   68 inspected / 1,034 exported jobs. The direct input/request is observed;
   sheet fulfilment and library completeness unknown. External work is an
   alternative; confidence in compound keys is high. Zero named elements
   cannot stand for zero reference preparation. Titanic's two direct bindings
   and Transmission's video turn supply additional package/disclosure contrasts.

5. **Counterexample to names-as-versions: KAGEROU.** Film
   `51d2c0b2-d692-42b4-b66f-daf87cac1eb3`, `kagerou:03.1`/`:03.5`/`:03.6`.
   The complete 20-record metadata register includes version-like names, but
   version and canonical codes remain unknown despite 489/489 job contexts
   inspected. A name may denote an alternative or navigation convention;
   it supplies neither changed-property lineage nor an approval event.
   Confidence is high in literal names, insufficient for semantic equivalence.

## 6. Pattern catalogue

These are scoped observed requests/edges, inferred practices and proposed
responses. Failure modes below concern evidence/workflow risk, not measured
technical failures. Recurrence across films is no tested-best-practice claim.

| Problem / applicability | Method, inputs and sequence | Evidence | Tradeoffs and failure modes |
| --- | --- | --- | --- |
| Keep an identity while changing a property | Bind source, name invariants and changed axes, produce a separate candidate | Detour/Birthdays/Ivy 03.2/03.5; observed requests, inferred derivatives | More explicit decisions; contradictory broad locks and structural deltas need review; no proven preservation |
| Prepare reusable views | Request single/multi-angle/expression/location form, retain output ID, attach it to later task | Harmony/Birthdays/Staff/Fallen Leaves 03.3 and package contexts | Preparation adds candidates and decisions; request/use cannot verify contents or completeness |
| Reuse with a sparse or absent named library | Bind direct source assets and explicit identity prose; retain unresolved producers | SNAP/Titanic/Transmission 03.1–03.4 | Supports partial evidence; disclosure count misses direct packages; external origins remain unknown |
| Combine layout with other properties | Give the described blockout spatial scope and separate appearance/reference roles | Kiss 03.4, Detour 03.6; observed instruction and attachments | Independent controls may conflict; description of blockout does not verify geometry or layers |
| Decide which source governs a property | Record scoped declaration, named properties and resolved/unresolved source binding | RAM/Detour/Harmony 03.6 | Prevents global approval by implication; missing tokens and overlapping scopes need human adjudication |
| Distinguish reuse from version approval | Count distinct consumers, trace explicit source/change pairs, keep review state separate | Six 03.5 derivatives; nine task declarations; corpus recurrence | Aliases, repeated requests and candidate edits complicate identity; frequency cannot select a canonical asset |

## 7. Studio-implication table

All behaviours are **proposed**, awaiting validation. These are information and
workflow hypotheses, not observed platform architecture or implemented features.

| Evidence → requirement or hypothesis | Proposed behaviour | Validation test |
| --- | --- | --- |
| SNAP/Titanic direct packages; 37 zero-disclosure films → library and asset paths both matter | Allow persistent elements backed by direct source media/prose as well as external reference IDs; show coverage independently | Synthetic zero-element import retains a package request and its direct input without inventing a library |
| Birthdays/Detour/Ivy deltas → identity and variant/version decisions must differ | Retain stable element ID, named state axes, immutable source-bearing versions and labelled derivative relationships | Human trace exercise: same person/new outfit, new person/same outfit, unchanged rerun and linked prop edit remain distinct |
| Requested sheets and video turn → package form and verification need separate fields | Store requested form, medium, attached source IDs and reviewed fulfilment independently | Synthetic multi-angle video request cannot become a verified still sheet; downstream use cannot auto-verify |
| Sparse descriptions and explicit prose → property provenance must survive context assembly | Store descriptions/constraints by channel, source path, scope and unavailable/empty state | Round-trip unavailable, empty and nonempty descriptions; an unseen image cannot generate a lighting/material claim |
| RAM property authority; Detour unresolved token → authority needs explicit scope/binding | Bind declarations to task/properties; surface unresolved bindings for human review | A table-shape declaration cannot override framing/light or approve unrelated elements; missing source stays unresolved |
| Repeated element use, six inferred derivatives, no approval events → review is an independent action | Show use history beside candidate/review/approved status, actor, event and scope | A frequently used unreviewed source remains approval-unknown; explicit approval applies only to its version/scope |
| Multi-asset records and unresolved cross-ID aliases → provenance must precede deduplication | Keep literal IDs and evidence-bearing representation/alias links; show unknown equivalence | Synthetic raw/preview values within one asset add no identity; two similar URLs/names create no merge; Study 07 adjudicates aliases |

## 8. Unresolved questions and handoff

Every provisional definition and its specific dependency is listed below. None
assumes a missing upstream result, and no pending study can manufacture private
libraries, media observations or absent approval events.

| Provisional definition here | Later result needed / current boundary |
| --- | --- |
| Element = disclosed compound reference record for corpus counts; semantic kinds only in scoped cases | Study 04 plus pending semantic-label run/agreement can refine instructed properties; Study 07 identity/alias linkage and Study 12 synthesis; complete libraries remain unavailable |
| Environment → location; auto/ip_verified labels retained literally | Study 04 context semantics and Study 07 entity linkage; no automatic identity or rights verification |
| Identity/variant = explicit retained properties and named changes, without merging IDs | Studies 04/07 refine property and identity links; Study 09 revision-family intent; case interpretations remain single-coder |
| Package = scoped request or named attachment; multi-asset = several raw attached IDs across uses | Studies 04/05 refine context and image operations; Study 06 refines video turn/shot routes; Study 07 aliases; media fulfilment remains unobservable |
| Property location = explicit prose/metadata plus unknown attached-media contents; JSON array states structural only | Study 04's information-location matrix and semantic labels/agreement; Studies 05/06 literal control interpretation |
| Reference-token and preservation wording = the unchanged AF3a regular expressions | Study 04 and the pending semantic-label run/agreement refine meanings and misses; the stratified sample cannot establish a semantic census |
| Reuse = at least two distinct consumers of the same raw compound element/asset ID | Study 07 resolves raw/preview aliases and semantic graph links; Study 09 distinguishes family/revision intent; never automatic approval |
| Inferred derivative = actual producer/input edge plus named property delta and bounded case interpretation | Studies 07/09 refine version/family lineage and ambiguous identity; RAM lacks an explicit preservation span, Prophecy also changes structure |
| Authority = explicit declaration scoped to what it names; frequent use stays separate | Studies 07/09 refine canonical-version/review requirements; project-wide canonical declarations remain unavailable or uncoded |
| Task = literal generation type; model identifier literal; no role inference | Studies 05/06 operations/routes and Study 08 model/workflow roles |
| Inherited orientation: image-led at ≥70% image jobs, film-led at ≥70% video, otherwise mixed; scale: <200, 200–999, 1,000–2,999, ≥3,000 jobs | Study 01 structural groupings only; Studies 05/06/08 refine operation/workflow interpretation; Study 10's visibility limits preclude labour/economic interpretations |
| Proposed schema and explicit approval/readiness states | Studies 07/09 validate dependencies/review, Study 12 synthesises and tests studio contracts; no persistence implementation here |

**Handoff to Study 02:** use these bounded element/package/version definitions
for its input bindings and local reference-preparation examples. A generation's
output used later is observed preparation; its sheet form remains requested and
its version/identity relationship needs its own evidence. Brief/task same-property
correspondences remain inferred; no complete brief-entity coverage is supplied.

**Handoff to Study 10:** raw input reuse still uses the same raw compound-ID
rule and reproduces its 20,869/29,906 count. This study supplies six labelled
panel derivatives and scoped authority, **not** corpus-wide semantic version or
alias resolution. Its pending 03/07 dependency therefore remains open for the
07 part and for uncoded project-wide identity. No prior study is rewritten.

The evidence does **not allow** complete entity/variant/library inventories;
corpus-wide semantic package or identity-preservation prevalence; verified sheet
forms/contents/completeness; voice-package prevalence; complete or alias-collapsed
semantic version chains; explicit project-canonical versus frequent-asset rates;
approval/final-adoption rates; cross-channel outcome/conflict rates; benefits of
reuse or one packaging strategy versus another; labour, cost, failure rates,
agents or internal orchestration. No media quality, continuity or identity success
measure is attempted. Studies 11/12 receive descriptive measures and testable
proposals, not winner labels or an implementation ranking.

## 9. Code, outputs and reproduction

From the repository root:

```bash
uv sync --locked
uv run python scripts/fetch_data.py
uv run python studies/03-elements/build.py
uv run python scripts/fetch_data.py --output data/study03-fresh
uv run python studies/03-elements/build.py --data data/study03-fresh --output data/study03-reproduced --check
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/check_repository.py
```

The fresh downloader verifies all 28 source assets. `--check` requires a separate
output directory and compares every generated CSV/JSON byte plus the manifest.
The reproduction test runs when the verified data is installed; CI without data
explicitly skips source integration reproduction and checks synthetic boundaries
and artifact hashes. Synthetic fixtures cover compound-key joins, repeated usage
channels, unresolved producers, JSON/null/empty states, unequal film weighting
and undefined zero-denominator shares. Schema reference/approval constraints and
scoped artifact states are checked; no studio workflow is implemented or tested.

| Output | Grain and provenance contract |
| --- | --- |
| [film_metrics.csv](outputs/film_metrics.csv) | 157 film rows; jobs/text/attachment/element/input-ID denominators, metadata and parameter states, inherited inferred orientation/scale and unusual flag; joins metric evidence |
| [metric_evidence.csv](outputs/metric_evidence.csv) | Film-scoped numeric excerpts and compound-key/query scopes with full evidence metadata; original taxonomy inference remains separate |
| [summaries.csv](outputs/summaries.csv) | All/cohort/orientation/scale ratios, explicit film sets, eligible/measured/positive films, numerator/denominator, equal-film mean, median/IQR and pooled share |
| [reference_categories.csv](outputs/reference_categories.csv) | Film × literal category counts/states and element recurrence; exact source filter joins film evidence; no semantic merge |
| `by_generation_type.csv`, `by_model_identifier.csv` | Film × literal dimension counts, including unavailable type; within-dimension denominator retained |
| `summary_generation_type.csv`, `summary_model_identifier.csv` | Dimension × cohort/all summaries; exact film membership recoverable from corresponding per-film rows and filters; only positive relevant denominators measured |
| [case_evidence.csv](outputs/case_evidence.csv), [panel_assignments.csv](outputs/panel_assignments.csv) | All 96 unchanged 03.x evidence rows; grouped state/value counts with panel denominator 16 |
| [reference_packages.json](outputs/reference_packages.json) | Sixteen scoped assignments; requests/named attachment/unknown separated, task contexts, input bindings, observed output-use occurrences, content and fulfilment unknown |
| [property_locations.json](outputs/property_locations.json) | Sixteen original 03.4 evidence rows with channels and unknown media/parameter semantics |
| [versions.json](outputs/versions.json), [authority.json](outputs/authority.json) | Six source-checked inferred derivatives and all 16 scoped declaration assignments, including unknown/unresolved states; no invented approval |
| [structural_check.csv](outputs/structural_check.csv), [lexical_audit.csv](outputs/lexical_audit.csv) | All-film AF3a cross-check counts; deterministic panel lexical keys/spans/offsets/hashes with denominators |
| [reproduction.json](outputs/reproduction.json) | Source manifest SHA-256; code/SQL/schema/ontology/readings/programme, Study 01 register, AF3a source/summary and case narrative/ledger/edge hashes; all generated output hashes |

Every generated file is below 1 MB and committed; no `study-03-v1` release is
needed. The ontology, schema and manual readings live beside the build. Source
texts remain in the original release, retrievable by compound key, with only
bounded evidence excerpts here. Original data, Study 01, case files, prompt-label
tools and Studies 02/10 are unchanged. No data-directory exception, full prompt
field, machine-specific path or local user name is introduced.
