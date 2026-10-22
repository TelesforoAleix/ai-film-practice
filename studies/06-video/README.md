# Study 06 — Video generation and shot control

## 1. Answer and evidence limits

The records show moving-shot requests built around **bound images, video sources,
written action/timing and property-specific constraints**. In 156 eligible primary
histories, 36,417/38,508 video jobs have image bindings; the equal-film mean is
93.40%. This is source conditioning, not proof that an image was a start frame or
that the requested movement appeared. Video bindings occur in 8,246/38,508 jobs,
including declared extensions, edits and finishing; these categories overlap with
image guidance. [Per-film measures](outputs/film_metrics.csv) precede pooled shares.

Creators can specify subject movement, camera movement, environmental motion,
events, speech/sound and invariants separately. The panel supplies scoped examples;
the corpus structural features cannot supply their semantic prevalence. Shot
wording and controls must remain separate: 8,981/9,060 fields matching the
numbered-shot/count rule coexist with `multi_shots=false`. This is neither a
contradiction verdict nor an achieved-cut or failure count.

Explicit lineage supports a local change from a continuous-take request to a
two-shot request in Ivy. It does not show why the action was split, whether it was
difficult, or whether splitting helped. Camera-change and revised-keyframe
strategies lack comparable, semantically established revision families here.
The proposed studio response is a video node retaining scoped intent, immutable
input bindings, literal controls, candidate provenance and human review separately.
It is a hypothesis awaiting tests, not a tested best practice.

Only the selected cohort has detailed records; this study cannot establish what
separates top films from other films. No media was watched or fetched; story,
aesthetics, media quality, continuity, screen timing and the proportion of a clip
used remain unobservable. No agents, internal orchestration, labour, cost, speed,
technical failure rate or causal benefit is inferred. Counts are **observed** under
**inferred** route definitions; case interpretations retain their labels and
studio behaviours are **proposed**. No experimentally supported claim is made.

## 2. Population, coverage, units and denominators

Study 01's unchanged [eligibility register](../01-corpus/outputs/eligibility.csv)
provides 156 Study 06 production-eligible films out of 157 complete primary public
histories. The remaining film has no exported video jobs. Of 186 priority films,
23 non-open-source listings were excluded and six public workspaces unavailable.
The supplemental Cosmic tracks pilot, including its 36 video jobs, contributes to
no measure here. No unusual project is removed or winsorized. Repeated texts,
batches and films by one creator are not independent observations; Study 01
records 151 creator handles across the outer 157 histories.

| Unit / coverage | Denominator and boundary |
| --- | --- |
| Video-bearing primary film | 156: 62 shortlist only, 54 most watched only, 40 both; outer primary population 157 |
| Video job | 38,508 compound film/generation keys: 13,876 shortlist only, 10,490 most watched only, 14,142 both |
| Primary video text | 37,079 nonempty + 290 explicitly empty + 1,139 unavailable = 38,508; nested copies do not add jobs |
| Parameter document | 38,499 valid objects + nine invalid released strings /38,508; no repair |
| Image-bound job | 36,417/38,508 in 155/156 films; raw IDs deduplicated within each consumer |
| Video-bound job | 8,246/38,508 in 131/156 films; includes generic input_asset at params.input_video |
| Audio-bound job | 2,550/38,508 in 38/156 films; does not establish generated dialogue or sound |
| Explicit frame roles | Start in 2,095/38,508 jobs, end in 190/38,508; not necessarily exclusive of video guidance |
| Resolved parent | Image producer in 29,769/38,508 jobs, video producer in 5,207/38,508; same-film, different existing job required |
| Case semantics | All 16 panel films × seven unchanged 06.x codes = 112 assignments; one case's seven are not applicable; unequal purposive reading scopes |
| Additional motion evidence | Eleven exact spans in four named jobs, across three panel films; purposive decomposition, not corpus semantic prevalence |

The [eligibility copy](outputs/eligibility.csv) retains all 157 primary rows and
Study 01's missing-evidence notes, including the video-zero film. An absence of input usages
cannot establish text-only generation. A zero relevant denominator yields
an unavailable rate. Per-film mean, median and linearly interpolated quartiles
come beside pooled job shares; these describe frozen-cohort variation, not
sampling uncertainty or independent-trial confidence intervals.

## 3. Method, taxonomy, codebook and checks

[build.py](build.py) uses `film_practice.connect` over the verified
`data-2026-10-20` release and executes [measures.sql](measures.sql). Source columns
stay strings. CSV is parsed, JSON uses `json.loads`, and every generation/asset/
reference join is film-scoped. Producers require `assets.generation_id` plus a
different, existing generation. Neither dates, names nor folder proximity supplies
an invented edge. Unresolved sources remain inputs with unknown producers.

The [shot-control taxonomy](taxonomy.json) has an exclusive **recorded input
route**, plus independent instruction, audio, timing, invariant and control axes.
Its precedence is extension → video-guided → start/end → image-guided → explicitly
declared text-to-video → text candidate → unknown. Extension needs an actual video
binding and literal `model=video_extension`. Any other video binding wins over
frame/image guidance, while independent input flags preserve their coexistence.
Start/end needs both explicit roles. Start-only and end-only remain image-guided;
ordinary reference images never become start/end frames. Text-to-video requires a
literal mode declaration plus nonempty text and no recorded or populated media;
text candidate needs explicit `medias=[]` under the same exclusion. Both are
export-conditioned, never proof of complete text-only production.

Typed image/video/audio usage roles and named generic media paths define bindings.
Camera/lens/light/pacing/style/genre/era/preset paths are excluded from media counts;
unexplained untyped paths would be retained as unknown inputs (zero qualifying
jobs here). Multi-shot wording, literal `multi_shots` and nonempty `multi_prompt`
arrays are independent indicators, not one exclusive route. Video-guided includes
editing and finishing; the raw video job type does not establish fresh synthesis.

Every literal control histogram keeps film, literal model identifier, explicit
`model_version` state and exact scalar JSON. Absent, JSON null, false, zero,
empty string/container, invalid document and unavailable document stay distinct.
Container states are retained without copying arbitrary text. Version absence
never becomes an assumed provider version; identifiers such as `seedance_2_5`
remain distinct. `model`, `mode`, camera and extension controls retain their own
literal values, without inferred defaults, units or cross-model equivalence.

Codebook **1.0**, codes 06.1–06.7, is unchanged. All 112 assignments, including
unknown/not-applicable states, retain source paths, compound entity IDs, short
excerpts, evidence labels, alternatives, denominators and confidence in
[case_evidence.csv](outputs/case_evidence.csv). Named opening prompt spans are
source-checked; non-prompt aggregate/edge openings are not treated as prompt text.
Panel attachments and producer edges are rebuilt. Eleven manually selected
component/split spans in [readings.json](readings.json) are all exact-substring
checked, with no full field copied. Their component interpretation is inferred.

The corpus uses the merged AF3a camera, lens, preservation, exclusion, multi-shot
and reference-token regexes unchanged. Each nonempty primary field counts once per
video job. Camera vocabulary includes a static camera or negated movement; the
multi-shot rule can match a single numbered shot, quotation or negation and misses
spelled-out counts and languages. **None is a semantic action/component label.**
The build recomputes counts at AF3a's film-distinct primary-video-text grain and
asserts equality for all 156 films in [structural_check.csv](outputs/structural_check.csv).
[structural_audit.csv](outputs/structural_audit.csv) keeps first sorted positive/
negative panel keys where available, exact offsets, bounded matches and hashes.
These check correspondence, not precision, recall or agreement. Harmony's
Portuguese four-plan instruction is a concrete coverage limit of English markers.
No pending model semantic labels, second coder or independent semantic validation
are used; Study 04 remains an explicit dependency under the owner's ordering choice.

Every numeric row joins [metric_evidence.csv](outputs/metric_evidence.csv) on film
ID for study, compound-key scope, source/query path, numeric excerpt, alternative,
denominator and confidence. A subgroup/control row adds its literal dimension/
state/value predicates to that scope. Aggregate member sets and predicates are
specified in section 9. Raw counts are observed; interpreting routes and component
spans is inferred. Selection, task mix, language, repeated requests, capture,
creator dependence and unresolved aliases are competing explanations throughout.

## 4. Findings through all five programme steps

### Step 1 — Route comparison

All rows use 156 films and 38,508 video jobs. Counts apply the inferred taxonomy;
routes sum to 38,508. [Route examples](outputs/route_examples.csv) retain actual
binding IDs/paths and model for one deterministic example per observed route,
preferring a panel film; no example is invented for a zero-count route.

| Recorded input route | Jobs /38,508 | Films with route /156 | Equal-film mean share /156 |
| --- | ---: | ---: | ---: |
| Declared extension with video input | 2,260 | 53 | 5.11% |
| Other video-guided | 5,986 | 130 | 15.40% |
| Start and end frame, without video binding | 122 | 23 | 0.42% |
| Other image-guided | 29,597 | 154 | 76.56% |
| Explicit text-to-video declaration under rule | 0 | 0 | 0% |
| Text candidate, explicit empty media | 530 | 82 | 2.47% |
| Unknown | 13 | 6 | 0.03% |

Input axes overlap: image-bound mean share is **93.40%**, median **96.77%**, IQR
**92.66–99.29%**, versus **94.57% pooled**; video-bound mean **20.51%**, median
**10.71%**, IQR **4.16–30.33%**, versus **21.41% pooled**, over 156 films.
These are disclosure-conditioned comparisons, not route effectiveness. Zero
qualifying explicit text-to-video jobs cannot mean nobody used text-to-video.
Dry Aged Dreams' no-input request remains a candidate, not proven text-only work.
SNAP's image inputs coexist with a declared extension and actual video input;
Fallen Leaves combines reference images with video guidance. Exclusive route
labels do not erase those bindings.

The independent start/end counts exceed the 122 exclusive start/end route jobs
because frame inputs can coexist with video guidance or occur singly. Study 05's
8,076 image-producing jobs consumed by video are reproduced exactly. The
[foundation-role table](outputs/foundation_roles.csv) refines that proxy into raw
reference/input/start/end role/path uses. Distinct producers are deduplicated
within each row; the same producer can occur in several roles/paths, so summing
those rows is **not** another unique-image total. A reference attachment never
establishes frame timing, verified keyframe contents or screen use.

### Step 2 — Motion prompt patterns and shot decomposition

| Instruction dimension | Scoped source example and evidence label | Limit |
| --- | --- | --- |
| Subject action | Prophecy 06.2: “Roopa hauls right to left”; observed wording, inferred component | No observed direction of motion |
| Camera action | Prophecy: “tracking with her, handheld tremor”; Staff 06.2 tilt; observed wording, inferred component | Camera vocabulary also includes static/negated instructions |
| Environment motion | Prophecy: “Heavy rain falls in every frame.”; observed wording, inferred component | Not verified weather or temporal consistency |
| Temporal events and boundaries | Prophecy: “4.0s HARD CUT”; Staff timed shot boundaries; observed request | Requested times/cuts, never measured output timing |
| Dialogue, voice and audio intent | RAM 06.4 voice-age lock, ducking and no music; APEIROPHOBIA 06.4 supplied audio/lip-sync request; observed text and attachment | No audible result, lip sync or mix verification |
| Invariants | Prophecy pod clearance; RAM appearance/layout; Staff prop dimensions; observed instructions | No preservation or continuity success rate |

The [eleven-span motion ledger](outputs/motion_patterns.csv) gives exact keys,
paths, excerpts, alternatives, denominators and confidence; code 06.4 and panel
contexts add full typed audio/source bindings. Instructions can hold a camera
fixed while a subject moves, sequence actions within one continuous take, or
request boundaries and invariants across shots. These are scoped procedural
patterns, not semantic prevalence estimates.

| Structural primary-video feature | Positive fields /37,079 nonempty | Films with match /156 | Equal-film mean /156 |
| --- | ---: | ---: | ---: |
| Camera vocabulary | 32,432 | 156 | 86.28% |
| Lens/framing vocabulary | 27,845 | 154 | 72.64% |
| Preservation wording | 13,163 | 144 | 36.95% |
| Exclusion wording | 33,762 | 156 | 90.87% |
| Numbered-shot/count marker | 9,060 | 122 | 25.01% |
| Reference token | 32,045 | 146 | 81.17% |

Literal `multi_shots=true` occurs in **170/38,508 jobs across 9/156 films**;
false in **36,744/38,508**. A nonempty `multi_prompt` array occurs in **7/38,508
jobs in 2/156 films**; its presence alone cannot establish multiple valid shot
instructions. Among lexical-positive fields, **8,981/9,060 (99.13% pooled)** have
false controls; the mean film share is **99.05% over 122 positive films**. This
extends Study 02's all-type comparison to video only. Enabled audio occurs in
**35,905/38,508 jobs**, mean film share **91.55% over 156**; exclusions such as no
music or no voice can coexist with enabled sound effects. No contradiction or
usable-sound rate follows.

### Step 3 — Literal duration, aspect, resolution and controls

The `controls_*.csv` outputs contain full per-film distributions; their
`summary_controls_*.csv` counterparts compare exact value/state frequencies within
literal model × explicit version state. Equal-film means include zero-share films
for each bucket among all users of that model/version; pooled counts are beside
them. No raw controls are translated into measured clip duration/pixels or an
interchangeable quality scale.

| Literal model / version-state group | Observed raw control values / group job denominator | Interpretation limit |
| --- | --- | --- |
| seedance_2_5 / model_version absent | duration=20 in 5,022/31,080; =30 in 4,188/31,080; =15 in 2,891/31,080; aspect 16:9 in 17,709/31,080, 21:9 in 13,022/31,080; resolution 720p in 16,246/31,080, 1080p in 10,848/31,080, 480p in 3,986/31,080 | Recorded scalar values, not screen seconds or output pixels; two additional jobs have invalid documents |
| cinematic_studio_video_4_0 / model_version absent | aspect 16:9 in 1,569/2,652, 21:9 in 1,065/2,652; resolution 1080p in 1,862/2,652, 720p in 402/2,652, 480p in 388/2,652 | Different interface/task mix; no cross-model resolution-benefit claim |
| kling3_0 / model_version absent | resolution key absent in 699/699; literal mode retained separately | Missing resolution is not zero resolution or a provider default |
| seedance_2_5 / model_version absent | draft=false in 31,080/31,080; extension_mode null in 28,820/31,080, forward in 2,047/31,080, backward in 213/31,080 | Null extension is not enabled extension; direction is literal |

The film-weighted control comparisons below use the exact same value buckets as
the raw table; all model/version users enter each bucket, with zero when the value
is not present. The two upscale-version user sets can overlap and are small.

| Literal model/version and value | Equal-film mean (film denominator) | Pooled jobs /model-version jobs |
| --- | --- | ---: |
| seedance_2_5 / absent, duration=20 | 16.46% (145) | 5,022/31,080 |
| seedance_2_5 / absent, duration=30 | 13.87% (145) | 4,188/31,080 |
| seedance_2_5 / absent, resolution=720p | 48.44% (145) | 16,246/31,080 |
| bytedance_video_upscale / standard, resolution=4k | 28.57% (7) | 44/53 |
| bytedance_video_upscale / pro, resolution=4k | 21.25% (8) | 4/19 |

These comparisons concern recorded settings; the weighting difference exposes
unequal job counts. It supplies no result, capability or benefit comparison.

Version fields are sparse; most groups have absent explicit versions and retain
their literal model ID. Explicit versions such as the video-upscale `standard`
value remain separate in the outputs; no hidden version is reconstructed.
Birthdays 06.6 pairs an 8K text request with literal resolution=720p; SNAP's
six-shot 15-second wording coexists with duration=18. These require retaining
requested and parameter channels, not inferring which was executed. False flags
and missing fields are not interchangeable. Literal video_edit occurs in
448/38,508 jobs across 46/156 films; it is not a census of edit intent (Lost's
changed-shot example has model=default).

### Step 4 — Splits, camera changes and keyframe revision

Code 06.7 has **12 coded /16 assignments**, three unknown (Dry Aged Dreams,
KAGEROU, Staff) and one not applicable (Titanic). [revision_requests.json](outputs/revision_requests.json)
preserves each named request and its source contexts, including unresolved video
producers. The panel does not estimate corpus revision or retry prevalence.

Ivy's explicit producer→video-input edge joins a continuous 15-second source
request to a two-shot 15-second request with one hard cut at 0:08. The edge and
text delta are observed; a local split-revision interpretation is inferred. The
evidence does **not** establish that difficult action caused the split, that an
actual clip was split, or that the new request worked better. Lost requests a
continuous take while changing sound/grade; this differs procedurally from Ivy's
split, without a matched causal comparison.

Fallen Leaves requests crane movement rather than pivoting; APEIROPHOBIA's belt
edit explicitly retains the camera angle. These show desired/retained camera
behaviour, **not a paired before/after camera-change history**. Study 05's traced
image derivatives and the 8,076 image→video foundations establish preparation/use,
not that a keyframe was revised to solve action. No comparable rate or benefit for
camera changes, revised-keyframe rescue, difficult-action splitting or one-shot
versus several-shot execution is estimable. Dates/shared inputs cannot supply
those missing semantic links. Studies 07/09 must refine lineage/families without
inventing motives, defects or outcomes.

### Step 5 — Shot inputs, constraints and revision routes

[video_node.json](video_node.json) is a **proposed specification**, not implemented
storage or orchestration. It requires film/scene/shot/task/version identity,
plan evidence, immutable asset/version bindings and scoped authority, the six
instruction dimensions, allowed changes, literal adapter/parameter states,
output IDs/provenance, and separate use/verification/review events. Scene/shot
links can be unknown; one task may request several shots. It consumes Study 02's
planned-shot/task distinction and Study 03's scoped source authority.

The six proposed revision routes are instruction change, revised keyframe,
video edit, extension, split request and bounded rerun. Each retains its source,
change scope and invariants, creates a separate candidate, and needs an explicit
human retry reason/cap or review decision. The archive provides no optimal retry
cap. The specification has readiness/round-trip/integrity rules and validation
tests; it chooses no execution architecture or platform scheduler.

### Task, literal-model and cohort comparisons

Task comparison uses the recorded input route, with independent instruction
indicators beside it in `by_route.csv` and `summary_route.csv`. It cannot compare
matched semantic task difficulty or success. Model means below condition on users
of that literal model with a positive relevant denominator; absent models are not
counted as users. Editor jobs with no nonempty primary text have an undefined
text rate, not zero shot intent.

| Literal model | Video-bound / model jobs | Equal-film mean (film denominator) | Shot-marker fields / nonempty fields | Equal-film mean (film denominator) |
| --- | ---: | --- | ---: | --- |
| seedance_2_5 | 6,340/31,082 | 20.16% (145) | 8,162/31,082 | 25.14% (145) |
| cinematic_studio_video_4_0 | 189/2,652 | 9.45% (52) | 511/2,652 | 21.94% (52) |
| seedance_2_0 | 184/1,297 | 5.77% (58) | 130/1,289 | 18.76% (58) |
| cinematic_video_editor | 785/785 | 100% (73) | 0/0 | Unavailable (0) |
| kling3_0 | 0/699 | 0% (28) | 91/696 | 2.13% (27) |

| Eligible cohort | Films | Video-bound / jobs | Mean film share | Shot-marker / nonempty fields | Mean film share |
| --- | ---: | ---: | ---: | ---: | ---: |
| Shortlist only | 62 | 2,741/13,876 | 19.81% | 4,018/13,461 | 30.04% |
| Most watched only | 54 | 2,113/10,490 | 18.66% | 1,902/9,990 | 17.24% |
| Both | 40 | 3,392/14,142 | 24.10% | 3,140/13,628 | 27.70% |

These are descriptive associations within the selected cohort. Model interfaces,
video finishing versus synthesis mix, repeated text, creator overlap, duration,
scale, language and missing external work compete as explanations. Full per-film
counts, orientation/scale strata, median/IQR and both weightings accompany every
measure. Small groups remain descriptive; no significance, provider, capability,
selection advantage or benefit is inferred.

## 5. Fully traced examples and counterexamples

Each example's full provenance is in the named 06.x case rows; contexts and edges
supply literal controls and attachment IDs. All keys below are scoped to the full
film UUID. Confidence is high in exported keys/exact spans, bounded and
single-coder for semantic interpretation; no media fulfilment is assessed.

1. **Ivy — linked split request.** Film
   `d305f6e5-b906-49a1-a0c6-75ef7f653ad8`, `dont-poison-ivy:06.7`.
   Producer/output `a9d85422-c95b-4e48-af27-093d2fbff0ca` explicitly feeds
   `070cf05b-2cd9-41fb-9c19-f232081d3e99` as input_video at
   `params.medias[0].data`; both literal models are seedance_2_5. Source text is
   “ONE CONTINUOUS SHOT — 15 seconds”; consumer text is “TWO SHOTS — 15 seconds
   total.” and “ONE HARD CUT at 0:08.” Observed edge/delta, inferred local
   split revision. Denominator: one named link in 553 inspected/exported jobs.
   Alternative: a new candidate/decomposition without a failure or accepted cut;
   no motive, benefit or project-wide splitting rate follows.
2. **Prophecy — independent actors of motion.** Film
   `9b38b885-bf92-484e-8f36-a890e4e10d61`, `prophecy-in-2047:06.1`–`:06.6`;
   job `014a8505-858b-4b9a-9777-b4461d5957e2`, seedance_2_5. Start-image asset
   `6b289173-c0e4-40ba-b2c1-f8aeca9c8992` binds at `params.medias[0].data`;
   character/prop/location reference bindings remain separately named in context.
   Hauling, tracking, rain, a timed cut and pod-clearance invariant have separate
   spans in the motion ledger. duration=15, 16:9, 1080p, audio=true and
   multi_shots=false remain literal controls. Denominator: one job within
   184 inspected/1,054 exported jobs. Alternative: a multi-shot request can be
   interpreted differently by an adapter; no action/cut success is observed.
3. **SNAP — extension with images and video.** Film
   `aed4098b-3278-4e5d-a347-24fad9cfb9ae`, `snap:06.1`–`:06.6`;
   job `2199ecf1-0186-4958-a24c-024d8ce09c9c`, seedance_2_5, model=video_extension.
   Video `c52bdac7-3338-48a3-8dcd-7971d8571461` attaches at
   `params.medias[3].data` beside three image inputs. “Every shot locked off”
   coexists with six written shots and source wardrobe/room constraints.
   Wording requests 15 seconds; raw duration is 18. Denominator: one job within
   68 inspected/1,034 exported jobs. Observed bindings/control, inferred extension
   route; the source producer/actual continuation cannot be invented. Alternative:
   continuation can retain or replace context; the records show no verified seam.
4. **Transmission — region-scoped video change.** Film
   `03f596b0-23da-4312-9e58-2e1cc4582348`, `the-last-transmission:06.5`/`:06.7`;
   job `083272c6-2303-4ddd-87e3-27dd2531ee0e`, seedance_2_5, model=video_edit,
   video asset `6640605c-455d-42cd-ab70-db0c327d7b20` at
   `params.medias[0].data`. “Edit: inside the CRT screen ONLY” and “EVERYTHING
   outside the screen glass stays exactly unchanged” scope change and invariants.
   Denominator: one job within 66/66 inspected/exported jobs. Observed request
   and input; inferred local-edit intent. Alternative: source-conditioned
   regeneration, without a disclosed mask or verified preserved surrounding media.
5. **Counterexample — Dry Aged Dreams.** Film
   `3777eda4-c15e-4531-9f04-4c02a900f3c3`, `dry-aged-dreams:06.1`/`:06.2`/`:06.4`/`:06.6`;
   job `c32600a6-0e04-4039-a577-2c8cdf2d60c2`, seedance_2_5. “slow push-in”
   and “SFX only.” coexist with duration=4, 480p, 21:9, audio=true,
   multi_shots=false, draft=false, extension_mode=null and no input usages.
   Denominator: one named task, ten video jobs/11 exported jobs, all inspected.
   Empty media supports only the inferred text candidate, not proof of text-only
   production. External inputs/capture omissions remain alternatives. This
   counters interpreting missing edges as a complete direct-generation workflow.
6. **Boundary counterexample — Titanic.** Film
   `3f6e509b-f3da-4324-a746-b9d35f0b9845`: all four exported jobs are images;
   all seven video codes are not applicable. A published film cannot be used to
   invent video records or infer the contents of an unobserved build.

## 6. Pattern catalogue

Failure modes below are ways requests or evidence can mislead, never measured
production failures. Recurrence of instructions is not a tested best practice.

| Problem / applicability | Method, inputs and sequence | Evidence | Tradeoffs and failure modes |
| --- | --- | --- | --- |
| Turn a prepared source into a moving-shot candidate | Bind images with their literal roles → specify subject/camera/environment motion → retain output and provenance | Prophecy, RAM 06.1–06.6; observed inputs, inferred procedure | More bindings/constraints; references may carry identity rather than frame timing; fulfilment unknown |
| Specify several events or cuts | Write order/time/boundaries and invariants → keep literal multi_shots separately → request candidate | Staff, Kiss, KAGEROU, Harmony 06.1/06.3/06.5 | Worded shots need not be provider multi-shot activation; timed events can remain one take; English regex misses meanings |
| Continue with image and video guidance | Bind source video plus supporting images → declare continuation/direction → keep a new candidate | SNAP 06.1; Staff explicit continuation edge in case files; inferred route | Source seam and direction semantics need review; no actual continuation or approval established |
| Separate sound intent from enablement | Attach audio if disclosed → specify speech/voice/ambience/exclusions → retain audio controls independently | APEIROPHOBIA/RAM/Transmission 06.4 | No-music does not mean silent; supplied audio is not generated audio; lip-sync and mix outcomes unknown |
| Split a continuous request | Trace explicit source video → change requested boundaries → retain source/invariants and new candidate | Ivy 06.7, observed edge/delta, inferred revision | No evidence of difficulty or benefit; changed decomposition needs a decision; not an executed editing operation |
| Change one property or region | Source video → named allowed changes and invariants → separately review output | Transmission screen; Prophecy lighting; RAM voice/character; Fallen Leaves resolution, 06.7 | More scope to adjudicate; requests disclose neither masks nor success; raw model=default can still accompany changed intent |
| Change a camera instruction or keyframe | Proposed: bind explicit predecessor/source version → name delta → request candidate → review | Camera directives and image-parent visibility; paired strategy evidence insufficient | No proven rescue strategy or prevalence; aliases and missing versions can create false revision families; Studies 07/09 needed |

## 7. Studio implications and video-node specification

All behaviours are **proposed**, awaiting validation; none reconstructs platform
internals or chooses an implementation architecture. The evidence anchors in
[video_node.json](video_node.json) link to the case ledger and the metric contract.

| Evidence | Requirement or hypothesis | Proposed behaviour | Validation test |
| --- | --- | --- | --- |
| Image/video/frame roles coexist; presets are not frames | Bind sources with typed role/path and film-scoped identity | Preserve immutable source/producer/version keys and unresolved state; keep reference and frame semantics distinct | Synthetic duplicate channels and cross-film ID collision preserve distinct consumers and prevent wrong producer links |
| Staff cuts with false control; SNAP requested/control duration difference | Keep request channels and literal adapter controls separate | Store boundaries, requested timing and raw typed values without silent rewriting | Round-trip false/null/absent/empty/invalid plus differing requested/control timing; human adjudication resolves task intent |
| Prophecy's six dimensions; RAM voice and exclusions | Shot intent needs independent scoped fields | Store motion actors, events, audio, invariants and changed properties with evidence | Independent coders recover allowed changes/invariants; review multilingual/negated/static-camera examples before semantic automation |
| Ivy linked split; unknown difficult-action motive | Revision needs source and reason, not chronology | New version for split/camera/keyframe/edit changes; retain original and ask a human to record intended change | Synthetic source/child relation retains both requests; controlled same-task continuous/split experiment with one changed factor, declared rubric/repetitions/budget |
| Transmission region constraint; unknown mechanism | Local edit intent must not invent a mask | Optional disclosed mask/region payload beside text, source and invariants; review candidate independently | Synthetic screen-only request creates no mask or success claim; separately authorised media experiment tests fulfilment |
| More use is not acceptance; missing failure denominator | Keep candidate, further-work use, verification and decision events separate | Require actor/version/scope-backed approval; bounded rerun policy has an explicit human cap/reason | Reused but unreviewed candidate stays approval-unknown; cap exhaustion stops without inferring archive failure rates |
| Raw model/version semantics and hidden defaults unknown | Adapters need explicit capabilities and provenance | Retain literal model/version/state, source hash, raw parameters and declared unit mappings | Unsupported/unknown control remains unresolved; no default or cross-model conversion is silently invented |

## 8. Unresolved questions and downstream handoff

Every provisional definition is listed here with the result it waits on. No later
study using only these records can manufacture omitted media, private work,
failures, decisions or timing.

| Provisional definition | Later study and current boundary |
| --- | --- |
| Recorded route = conservative input/control precedence; extension = video binding plus literal video_extension; unknown stays explicit | Study 08 model/adapter/workflow interpretation; Study 07 disclosed graph; no hidden implementation recovered |
| Text candidate = nonempty text + explicit empty medias + no other recorded/populated media; declared text-to-video additionally requires literal mode | Studies 07/08 can refine source linkage; complete text-only production remains unknowable |
| Image/video/audio binding = typed roles or enumerated generic parameter path; presets excluded; raw IDs deduplicated per consumer | Study 07 alias/representation and typed-graph resolution; several raw IDs need not mean several semantic sources |
| Start/end = explicit roles only; image output→video = candidate foundation, not automatically a keyframe | Study 07 version/graph scope and Study 08 workflow roles; screen timing/content remains unobservable |
| Corpus motion/invariant/shot features = unchanged AF3a lexical indicators on nonempty primary fields | Study 04 semantic labels, agreement and context matrix; no subject/environment/dialogue semantic census here |
| Semantic motion/timing/audio/invariants = scoped single-coder case/span interpretation | Study 04 context/component refinement; requested outcomes remain unverified |
| Linked split/revision = explicit source edge plus named changed intent; shared inputs/dates alone insufficient | Studies 07/09 refine lineage, comparable families, instruction/input deltas and revision intent; no difficult-action or failure motive inferred |
| Model/version group = literal model identifier plus explicit version state; raw model/mode retained separately | Study 08 adapter roles/semantics; absent version/defaults not reconstructed |
| Task comparison = recorded route; multi-shot request/control/container are independent axes | Study 04 planned boundaries/semantics, Study 08 roles and Study 09 comparable families; no matched-task benefit estimate |
| Inherited orientation ≥70% image/video, otherwise mixed; Study 01 scale thresholds unchanged | Study 08 workflow interpretation; Study 10's limits still exclude economic/labour meanings |
| Video-node inputs, human review states and six revision routes are proposals | Studies 09/12 review/family refinement, synthesis and controlled validation; no execution/persistence architecture chosen |

**Handoff to Studies 02/03/05/10:** video task context now distinguishes source
roles, start/end bindings, literal extension/edit controls and independent shot
wording. A package can be a video turn, as Study 03 noted; nothing makes it a
verified still sheet. Study 05's 8,076 candidate foundations reproduce, with
explicit role/path refinement but no automatic frame timing. Study 02's shot/task
contract can consume the six intent dimensions without treating one task as one
shot. Study 10 can stratify video records by these routes but gains no cost,
labour, responsibilities or comparable-format resource denominator. These earlier
reports remain unchanged. Study 04 was deliberately not assumed; its later
semantic results must carry sample exclusions and agreement limits.

**Measures the evidence does not allow:** proven text-only/fresh-generation rates;
corpus semantic action/environment-motion/dialogue/invariant or actual multi-shot
prevalence; complete/alias-resolved revision and keyframe version families;
difficult-action splitting rate or motive; camera-change/keyframe-rescue rates;
matched-task route/split/revision benefits; actual control effect/defaults;
clip quality, continuity, preservation, timing, usable audio or portion used;
final acceptance, failures, retry/rejection rates, labour, cost, speed, productivity,
agents or internal orchestration. No comparison with the uncollected catalogue,
provider ranking or winner labels is supplied. Study 12 receives testable
hypotheses, not a ranked roadmap or tested best practices.

## 9. Reusable code, outputs and reproduction

From the repository root:

```bash
uv sync --locked
uv run python scripts/fetch_data.py
uv run python studies/06-video/build.py
uv run python scripts/fetch_data.py --output data/study06-fresh
uv run python studies/06-video/build.py --data data/study06-fresh --output data/study06-reproduced --check
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/check_repository.py
```

`--check` requires a separate output directory and compares every output byte,
including the manifest. A fresh fetch verifies all 28 source assets. The integration
reproduction test runs when the snapshot is present; CI without source data skips
it explicitly and runs synthetic route/state/compound-key/weighting checks and
committed-artifact/input hashes. No actual source record is copied into a fixture.
The tests exercise analysis code; they do not implement/test the proposed studio.

| Output | Grain, denominator and provenance contract |
| --- | --- |
| eligibility.csv | All 157 primary Study 01 Study 06 rows, including video-zero exclusion |
| film_metrics.csv; metric_evidence.csv | 156 per-film numeric rows and full study/film/compound-key source/query scope, numeric excerpts, alternatives, denominators and confidence; inferred taxonomy context stays separate |
| summaries.csv; summary_members.json | All/cohort/orientation/scale ratios; exact eligible film sets; measured subset has positive denominator_name in per-film metrics; equal-film mean/median/IQR beside pooled counts |
| by_route.csv; by_model_identifier.csv; by_model_version.csv | Film × inferred recorded route or literal model/version with every numeric measure and within-stratum denominators; joins film metric provenance |
| summary_route.csv; summary_model_identifier.csv | Dimension × cohort/all; exact members recoverable from matching per-film rows and literal dimension/cohort predicate, then positive denominator; absent models are not users |
| controls_*.csv | Film × literal model/version × exact parameter/state/raw scalar JSON, bucket jobs and full model/version-video-job denominator; exact generation scope selected by those predicates |
| summary_controls_*.csv | Each model/version × exact control/state/value; members are all model/version users in corresponding controls file; bucket absence contributes zero share; full film/job denominators and both weightings; join member film evidence for alternatives/confidence |
| foundation_roles.csv | Film × image-bound role/path; distinct image producers, video consumers and pairs; film distinct-foundation denominator; same entity can recur across rows, which must not be summed as unique sources; exact SQL scope and observed label |
| route_examples.csv | One sorted example per observed route, preferring panel; compound task and attachment IDs/paths, inferred route, observed bindings as excerpt, alternatives, denominator and confidence |
| case_evidence.csv; panel_assignments.csv | All 112 unchanged 06.x assignments plus source path; code/state/value counts with panel denominator 16 |
| panel_contexts.json; panel_edges.csv | Named video jobs, literal controls, actual bindings and resolved producers; explicit edge occurrences with full evidence metadata; unknown producers/outputs remain unknown |
| motion_patterns.csv; revision_requests.json | Eleven checked component/split spans and twelve scoped revision assignments with source contexts; wording/edges observed, interpretation inferred, no outcome or exhaustive-family claim |
| structural_check.csv; structural_audit.csv | All 156 AF3a original-grain equality checks and deterministic panel positive/negative lexical source correspondence; not semantic accuracy |
| reproduction.json | Source manifest hash; code/SQL/taxonomy/node/readings, governance, upstream registers/reports/features and case narrative/ledger hashes; every generated output hash; no machine paths/times/usernames |

For aggregate/control/foundation numeric rows, the numeric row itself is the exact
excerpt and its source is the named per-film output/build/SQL scope. Film IDs and
raw dimensions select the original compound generation/asset/reference IDs;
metric_evidence supplies the shared alternative and confidence rationale. Route
semantics are inferred; original case labels remain intact. All files are below
1 MB and committed; no `study-06-v1` release is needed. Original data, programme,
Study 01, other studies, prompt-label tools and case files are unchanged. No full
prompt, tracked data-directory file, machine-specific path or local user name is
introduced.
