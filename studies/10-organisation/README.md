# Study 10 — Organisation and production economics

## 1. Answer and limits

Public records make work **countable and traceable**, but do not measure effort or
production economics. Across **157 primary films / 130,704 jobs**, folders coexist
with dependencies that often cross their boundaries. Folder semantics come from
the 16 purposive case files; folder counts alone do not identify scenes or stages.

Recorded ownership, authorship and asset use are different facts: **24/157** films
have several author IDs and **21/157** have explicit cross-author producer/consumer
pairs. Neither establishes a team, employment, delegated responsibility or a human
handoff. Dates are event windows, never hours worked. Exact text repeats and reuse
are common in this export; neither is waste or evidence of benefit. Comparable
formats, actual labour, prices, spend and final-use decisions remain unavailable.

The operating-model response is **proposed**: keep identity and dependencies
independent of folders; record ownership, versions, review decisions and budget
transactions explicitly. These are hypotheses awaiting tests, not tested best
practices or reconstructed platform architecture. No agents, scheduler, internal
orchestration or autonomous workflow is inferred.

Only the selected cohort has detailed records: this study cannot establish what
separates top films from other films. No film, image or audio was opened; no story,
aesthetics, continuity or media quality was judged.

## 2. Population, coverage, units and denominators

The unchanged Study 01 [eligibility register](../01-corpus/outputs/eligibility.csv)
provides all **157 production-eligible Study 10 primary histories**. The 186-film
priority union loses 23 excluded non-open-source and six unavailable workspaces.
The supplemental Cosmic tracks pilot (195 jobs) contributes to no measure here.
The remaining catalogue is not an unmeasured zero-work comparison group.

All **130,704/130,704** primary jobs have author IDs, parseable timestamps and
folder placements. All **157/157** films have a positive catalogue-declared
duration and one explicit `is_owner=true` author ID in `films.authors_json`.
These are field-coverage facts, not complete production, sole labour or ownership
of every asset. The 49 films flagged in Study 01's unusual-project audit remain in
all 157-film summaries; none is removed or winsorized.

| Unit / coverage | Measured denominator and boundary |
| --- | --- |
| Film | 157 histories; 62 shortlist only, 55 most watched only, 40 both; 151 literal creator handles from Study 01, so films are not independent creators |
| Recorded job | 130,704 compound `(film_id,generation_id)` keys; every generation type retained |
| Primary text | 124,449 nonempty, 1,083 explicitly empty, 5,172 unavailable; sum 130,704; nested copies never add instructions |
| Generation placement | 136,076 rows over 130,704 jobs; 3,230 folder entities, 2,408 with generation placements |
| Asset placement | 142,254 rows over 136,795 placed raw asset IDs; these assets can include nonproduction catalogue items |
| Inputs | 337,692 distinct `(film_id,consumer,asset_id)` pairs over 29,906 raw input IDs in 156/157 films; role/path duplicates collapsed only for these measures |
| Resolved producer/consumer pair | 198,201 distinct `(film_id,producer,consumer)` pairs in 147/157 films; all have both authors and placed endpoints in this snapshot |
| Case semantics | 16/16 registered panel cases, all five Study 10 codes: 80 assignments; purposive and single-coder, never a prevalence sample |

Counts of rows, entities, pairs and films are different denominators. All input
roles are enumerated in [measures.sql](measures.sql). Unresolved producer inputs
remain inputs; they supply no reconstructed producer. The ten films without a
resolved pair have an undefined pair share, not a measured zero share.

## 3. Method, codebook and checks

[build.py](build.py) reads the checksum-verified `data-2026-10-20` snapshot with
`film_practice.connect`, registers Study 01 eligibility, executes the reusable SQL,
and writes sorted per-film outputs before aggregate comparisons. Source views
remain strings. Study 01's dictionary supplies the timestamp and duration types;
casts live only in temporary study tables. UTC dates are calendar dates with at
least one event. Span is `(last_event-first_event)/86400`, with no gap threshold,
work-session reconstruction or conversion to labour.

Codebook **1.0** is unchanged. Codes 10.1–10.5 are retained verbatim, with their
full compound keys, paths, excerpts, evidence labels, alternatives, denominators
and confidence in [case_evidence.csv](outputs/case_evidence.csv). Every case's
folder-label transcription and full-export repetition/multiple-placement counts
are checked against the new build. No corpus-wide folder-name semantic classifier
is introduced. Case semantics cannot be assigned to the other 141 films.

| Local operational definition | Evidence label / limit / dependency |
| --- | --- |
| Flat ≤2 folders, partitioned >2; small <200 jobs, medium 200–999, large 1,000–2,999, very large ≥3,000 | Study 01 inferred structural thresholds, retained; system/root folders included; semantic scene/task decomposition awaits Study 02 |
| Image-led ≥70% image jobs, film-led ≥70% video, otherwise mixed | Study 01 inferred history composition; not content/format or build order; task and model roles await Studies 05, 06 and 08 |
| Owner ID | Only a literal boolean `is_owner=true` with nonempty ID; compare exact `author_user_id`, never usernames; not employment or responsibility |
| Author specialisation proxy | Job counts by literal author × generation type × model within film, with author-job denominator; no semantic role or specialty label; waits on Study 08 (and operations in 05/06) |
| Cross-author relationship | Different nonempty IDs on an explicit resolved producer/asset/consumer link; count distinct job pairs, not role/path occurrences; semantic handoffs await Study 08 |
| Disjoint folder relationship | A resolved pair has placements on both ends and no shared exact folder ID; ancestor/child folders count as different; placement at capture, not a historical move or scene boundary; semantic interpretation awaits Study 02 |
| Reused input | Same raw compound asset ID consumed by at least two distinct jobs, including external inputs; self-output pairs excluded from resolved edges only; alias/version resolution awaits Studies 03/07 |
| Repeat excess | Nonempty primary-field count minus distinct exact strings within film; whitespace/case retained; within-task/model variants recompute in their own scope; revision families await Study 09 and semantic text interpretation Study 04 |
| Multiple placement | More than one distinct folder ID for a compound job/asset; entity and occurrence counts both retained; no extra jobs, revisions or waste inferred; family interpretation awaits Study 09 |
| Duration proxy | All recorded jobs ×60 / positive catalogue seconds, only as within-film capture context; no comparable-format contrast is available; planning/deliverable semantics await Study 02 and technical routes 05/06, but these cannot by themselves verify final screen time |

No missing upstream result or semantic model label is assumed. Structural prompt
features are optional here; exact equality answers the repetition question without
semantic labels. There is no model-label accuracy or independent-coder agreement
estimate. Source transcription/aggregate checks establish correspondence, not
semantic correctness. Nine released malformed parameter strings are never repaired;
none of the present SQL measures requires those JSON fields.

The provenance rule for **every numeric output** is its film ID joined to
[metric_evidence.csv](outputs/metric_evidence.csv), which names the whole compound-key
source scope and records the exact aggregate excerpt, denominators, label,
competing explanation and confidence. Case interpretations join `evidence_id` in
the case ledger and are **inferred**, separately from observed counts. Subgroup
rows retain exact film sets and join those ledgers; see section 9 for the measure
contract. Quartiles use pandas linear interpolation. They describe this frozen
cohort, not population uncertainty or independent draws. Coverage, raw-ID alias
ambiguity, unequal history capture, creator dependence and semantic ambiguity are
the material uncertainties; no significance tests or causal estimates are made.

## 4. Findings: all six programme steps

### Step 1 — Organisation, dependencies and scale

**Observed:** the structural threshold yields **26/157 flat** and **131/157
partitioned** histories. Median jobs are **215 over 26 flat films** and **646 over
131 partitioned films**; this is descriptive, with history capture and production
scale as alternatives to any organisational explanation.

Resolved dependencies have disjoint folder sets for **107,399/198,201 pairs**
(54.19% pooled); the mean film share is **46.69% over 147 films with pairs**,
median **53.07%**, IQR **1.73–81.49%**. This is placement topology, not a count of
scene handoffs. In the flat subset, **20/26** films have pairs and the mean disjoint
share is **1.62% over those 20**; in the partitioned subset **127/131** have pairs,
mean **53.79% over those 127**. Folder partitioning partly defines the opportunity
for this measure; there is no inferred benefit.

**Inferred from cases:** scene/entity organisation (The Staff), mixed
scene/entity/type/stage organisation (Ivy, KAGEROU), and flat exported organisation
(Fallen Leaves, SNAP) all coexist with explicitly different dependency structures.
The panel comparison in section 5 is the semantic comparison with scale. Its
sampling cannot support a corpus-wide semantic pattern frequency.

### Step 2 — Ownership, authors and recorded handoffs

**Observed:** **133/157** films have one author ID; **14/157** have two,
**6/157** three, **3/157** four and **1/157** five. Explicit owner IDs account for
**116,574/130,704 jobs (89.19% pooled)**; mean owner share is **93.98% over 157
films**. The other **14,130/130,704** jobs bear a different recorded ID, not a proven
contributor role. All one-author histories match their declared owner ID here.

Cross-author pairs occur in **21/157 films**, and in **21/24 multi-author films**;
there are **23,632/198,201 authored pairs (11.92% pooled)**. The equal-film mean is
**3.85% over 147 films with authored pairs**, median zero, IQR zero–zero. The pooled
value is influenced by large shared histories; pair counts are not independent
handoff decisions. The three multi-author histories without such a pair do not
establish absence of collaboration.

[author_operations.csv](outputs/author_operations.csv) exposes the measured author
× type × literal-model composition. For example, Prophecy's owner ID has
**568 image + 348 video = 916 jobs**, while the other ID has **138 image / 138 jobs**.
That is a visible composition difference, not proof of character-design versus
animation labour. Its case file explicitly keeps two recorded IDs apart from a
single-person creator account. Team structure, responsibility transfer, actual
specialisation, human headcount and labour division cannot be measured.

### Step 3 — Recorded activity windows

**Observed:** across **157 films**, event-span median is **24.330 calendar days**,
IQR **14.298–29.932**, range **0.000083–36.486 days**. Median distinct active UTC
dates is **16 per film**, IQR **10–24**, range **1–34**, with **2,613 film/date
occurrences** overall. Those dates cannot be added as person-days. Time zones,
batches, long gaps and activity outside the public history prevent any labour,
speed, latency or schedule-performance interpretation. The Titanic four-job
window lasts about 7.18 seconds; that is evidence of recorded event proximity,
not a film produced in that time.

### Step 4 — Reuse, exact repetition and placements

**Observed:** **155/157** films have exact repeat excess. The sum is
**63,042/124,449 nonempty primary fields (50.66% pooled)**; the mean film repeat
share is **38.45% over 157 films**, median **38.63%**, IQR **20.83–56.46%**.
This counts additional occurrences after the first exact text in each film,
not failed attempts or iteration families. Changed media inputs, batches,
operations and repeated boilerplate are competing explanations.

**20,869/29,906 raw input IDs (69.78% pooled)** are consumed by at least two jobs;
the mean film share is **69.53% over the 156 films with inputs**, median **70.25%**,
IQR **57.32–82.02%**. All 156 input-bearing films have at least one such raw ID.
This includes external inputs and does not identify canonical, approved or
visually equivalent assets. Cross-ID aliases remain unresolved.

**4,942/130,704 jobs (3.78% pooled)** have multiple folder placements, in **45/157
films**; equal-film mean **4.27% over 157**, median zero. There are **5,372 placement
rows beyond one per placed job**, not additional jobs. **5,029/136,795 placed asset
IDs** have multiple placements, in **46/157 films**. Asset placements exceed placed
assets by **5,459 rows**. Neither placement repetition nor reuse is classified as
waste, inefficiency or rejection.

### Step 5 — Resource proxies and comparable formats

The build records **157/157** within-film jobs-per-declared-minute ratios with
both numerator and declared seconds. They are capture descriptors, not estimates
of generations per actual finished minute, cost, productivity or speed. No ratio
ranking, pooled economics or cross-format comparison is reported: all **157/157**
catalogue categories are `[]`, and record orientation cannot stand in for format.
Thus **zero comparable-format contrasts are estimable from the available format
strata**. Brief statements can conflict with catalogue duration (The Staff,
Detour, Random Access Memories); they are not silently substituted. The missing
finished-duration/format and production-boundary evidence prevents the programme's
within-comparable-format resource comparison, even though arithmetic is possible.

### Step 6 — Operating needs and resource visibility

The audit below concerns **157 public histories**, not all resources actually used.
“Visible” means an exported field/relationship under its stated denominator;
“partial” includes creator accounts without independent measurement.

| Resource | Visibility and measured scope | What cannot follow |
| --- | --- | --- |
| Job/model/type records and source provenance | Visible: 130,704 jobs / 157 films; task is raw generation type | Full work inventory, semantic task roles or provider costs |
| Folders and placements | Visible: 3,230 folders, 136,076 generation placements / 157 films | Executed sequence, maturity, completion, scene intent outside the cases |
| Recorded owner and author IDs | Visible: 157 declared owner IDs / 157 films; all jobs authored | Real team size, roles, employment, permission history or labour division |
| Asset inputs and producer links | Partial: 156/157 films have inputs; 147/157 have resolved job pairs | Complete lineage, alias identity, external preparation or true responsibility transfer |
| Reusable entities and versions | Partial: 120/157 films disclose elements in Study 01; raw input reuse measured above | Canonical approval, semantic equivalence and project-wide version intent |
| Dates and calendar coverage | Visible: 130,704 dated jobs / 157 films | Hours worked, latency, elapsed production time, gaps as work sessions |
| Declared duration and format | Partial: positive catalogue seconds in 157/157; usable format strata absent in 157/157 | Actual finished duration or comparable-format economics |
| Brief accounts of external work, credits and staffing | Partial: 118/157 nonempty briefs in Study 01, substance uneven; no claim of 118 resource disclosures | A cost ledger, verified person-hours or complete external editing inventory; Lost's credit statement is not money |
| Billed spend, prices, subscriptions and compute | Unavailable as a film-attributed, reconciled ledger | Unit cost, savings, budget adherence or total production cost |
| Labour and team structure | Unavailable as measured assignments/time records | Person-hours, productivity, headcount or schedules |
| Checkpoints, approvals and final adoption | Unavailable as verified review events; folder names/creator statements are partial clues | Acceptance rates; reuse means further work only |
| Failures and discarded work | Unavailable denominator; all 130,704 exported jobs are marked completed in Study 01 | Failure/retry rates, waste, technical success or selection efficiency |
| Private prompts, agents and platform orchestration | Unavailable and outside retrieval scope | Autonomous-agent or internal architecture claims |

Ownership, versioning, search, budgets, checkpoints and provenance are addressed
as **proposed behaviours** in section 7, with validation tests rather than claims
of observed platform features or measured savings.

### Task, literal-model and cohort context

The task-level denominator available now is generation type; semantic operation
roles await later studies. Exact repetition is recomputed within each type/model,
so subtotals need not sum to whole-film excess when a text crosses scopes.

| Recorded type | Films with jobs / 157 | Jobs / 130,704 | Repeat excess / nonempty fields in type | Mean within-film type repeat share (measured films) |
| --- | ---: | ---: | ---: | ---: |
| Image | 155 | 92,058 | 53,284 / 87,238 | 47.03% (155) |
| Video | 156 | 38,508 | 9,679 / 37,079 | 19.28% (156) |
| Audio | 10 | 132 | 33 / 132 | 22.02% (10) |
| Text; image_3d; unavailable type | 1; 1; 2 | 1; 1; 4 | 0 / 0 in each | Undefined; small/descriptive only |

| Literal model (five largest job counts) | Films / 157 | Jobs / 130,704 | Mean film job share (all 157, absent=0) | Repeat excess / model nonempty fields |
| --- | ---: | ---: | ---: | ---: |
| seedance_2_5 | 145 | 31,082 | 31.14% | 8,093 / 31,082 |
| nano_banana_2 | 138 | 25,355 | 16.93% | 14,451 / 25,355 |
| seedream_v5_pro | 96 | 21,136 | 10.93% | 11,645 / 21,136 |
| gpt_image_2 | 120 | 14,397 | 9.47% | 6,027 / 14,397 |
| soul_cinematic | 65 | 7,696 | 5.23% | 5,474 / 6,919 |

Model labels are literal; no provider, speed, benefit, cost or workflow role is
assigned. Empty/unavailable text is excluded only from text denominators, never
from job counts. Every model, type and cohort combination, including small groups,
is retained in the `by_*` and `summary_*` outputs.

| Primary cohort | Films; jobs | Multi-author films / films; cross-author films / films | Median event span (film denominator) | Mean film repeat share; pooled repeat share |
| --- | --- | --- | --- | --- |
| Shortlist only | 62; 45,497 | 8/62; 6/62 | 22.997 days (62) | 39.30%; 46.21% |
| Most watched only | 55; 31,169 | 5/55; 5/55 | 18.739 days (55) | 32.14%; 42.13% |
| Both | 40; 54,038 | 11/40; 10/40 | 28.899 days (40) | 45.80%; 59.19% |

These are observed descriptive comparisons, not evidence that organisation causes
selection or that one group is more efficient. Duration, scale, creator overlap,
model/type composition and missing external work are competing explanations.
Exact prompt denominators, quartiles and film sets are in `summaries.csv`; no
uncertainty estimate treats jobs, pairs or repeated texts as independent films.

## 5. Traced examples and counterexamples

All IDs below are scoped to the named film. The complete five-code evidence,
folder compound keys and source excerpts are in `case_evidence.csv`, linked to
the unchanged case files; the new count excerpts and alternatives join
`metric_evidence.csv`. No example establishes production benefit.

1. **KAGEROU versus Random Access Memories, P4** —
   `51d2c0b2-d692-42b4-b66f-daf87cac1eb3` versus
   `e99b5ad2-8f58-4ef8-a13c-4441cfdd5205`.
   Codes `kagerou:10.1` and `random-access-memories:10.1` infer mixed organisation
   from labels including “pre-vis”, “cut”, “export” versus “Generated Refs”,
   “Notes, Script, Tools”, “Sound”. Their observed scale is **489 versus 482 jobs**,
   but **227 versus 24 folders**, with **693/755 versus 287/537** resolved pairs
   crossing disjoint folder sets. These are two registered shortlist-only cases,
   not a general association. Competing explanation: repeated labels, copied
   structure and different capture/placement habits, not organisational maturity.
   Confidence: exact full folder/count checks; semantic meaning remains inferred
   by one coder, with no executed-order evidence.

2. **Don't Poison Ivy: author identity versus handoff** —
   film `d305f6e5-b906-49a1-a0c6-75ef7f653ad8`, codes
   `dont-poison-ivy:10.1`/`:10.2`/`:10.4`. “Characters”, “Outfits”,
   “Video Generations” and “Act 4: The Break” support inferred mixed organisation.
   **411/553 jobs** match the owner ID; **142/553** bear two other IDs.
   **344/1,042 authored producer/consumer pairs** cross author IDs. One fully
   resolved edge in `cross_author_examples.csv` has producer/asset
   `093c9448-335b-47fb-a9c0-b865dd495c00` consumed by
   `0c102167-33f1-4e12-ac68-7539d7055bd1` under a different ID. Source:
   `assets.generation_id`, non-output `asset_usages`, both jobs'
   `author_user_id`; exact compound keys and author IDs are in that output.
   Denominator: one lexicographically first example among 344 cross-author pairs.
   Interpretation: a recorded account boundary, not proven ownership transfer or
   division of labour; published histories can omit external work and account use
   is not human headcount. Confidence: exact explicit joins, not inferred lineage.

3. **Lost: placement is not another generation** —
   film `e5ce8a79-9375-4e31-84a8-620bd4f07550`, `lost:10.1`/`:10.4`.
   Literal “Scenes”, “Characters”, “Locations”, “Assets” support inferred mixed
   organisation. Observed **275/350 jobs** occur in several folders,
   **817 placements / 350 jobs**, **248 repeat occurrences / 350 nonempty fields**.
   None of **1,023/1,023 resolved pairs** has disjoint folder sets despite the
   partitioned register. Shared placement can mask a finer organisation; it does
   not erase dependencies or indicate duplicate labour. Confidence: full exported
   placement and equality counts, checked against the case's exact aggregate.

4. **Counterexample: flat organisation with explicit reuse** — Fallen Leaves,
   film `6659c520-c88e-4ac7-a2c9-f28d8a40c954`, `fallen-leaves:10.1` and `:10.4`.
   “Watermarks; Fallen Leaves” is the full two-folder register, but the film has
   **10 disclosed elements**, **37 reused / 41 input asset IDs** and **701 resolved
   job pairs / 356 jobs**. Case edge asset/producer
   `1cba062c-b6c5-456d-929d-b958859ae105` → consumer
   `023fadcd-4fdd-46b9-98f4-1b940839b4c7` records explicit reuse under
   `gpt_image_2` → `seedance_2_5` (case codes 07.1/08.3). This counters “flat means
   no reuse”; it cannot establish continuity or effectiveness. Confidence: explicit
   edge and full register; private organisation and cross-ID aliases remain unknown.

5. **Counterexample to interpreting the duration ratio as productivity** —
   A Tales Before Titanic Tragedy, film `3f6e509b-f3da-4324-a746-b9d35f0b9845`,
   `a-tales-before-titanic-tragedy:10.3`–`:10.5`: **4 jobs / 313.25 declared
   seconds ×60 = 0.766161 jobs per declared minute**. The four events span
   **7.181655 seconds**, and **3/4 nonempty fields** are repeat excess. Complete
   export status does not establish a whole production. An external/unpublished
   build is a competing explanation; the ratio supplies no efficiency claim.
   Confidence: exact extrema/count arithmetic, no inference about work duration.

## 6. Organisation and operating-pattern catalogue

The catalogue separates **inferred case practices**, **observed structural
patterns** and **proposed operating responses**. A recurring case pattern is not
an estimated corpus prevalence or tested best practice.

| Problem / applicability | Method, inputs and sequence | Evidence | Tradeoffs and failure modes |
| --- | --- | --- | --- |
| Find work by scene/entity/type/stage in a partitioned project | Retain literal folder ID, parent and placements; inspect case semantics; view dependencies beside folders | Inferred: Ivy, KAGEROU, The Kiss 10.1; observed disjoint-pair measures | Several browsing routes, repeated labels and many empty folders; names cannot prove order or approval; applies when the register and edges are disclosed |
| Find dependencies in a flat workspace | Keep stable asset/job IDs; follow explicit producer→asset→consumer independently of folders | Observed: Fallen Leaves counterexample; SNAP 10.1/07.1 | Simpler folder register does not remove graph complexity; hidden inputs and aliases limit scope |
| A job appears in several useful places | Separate entity identity from placements; group by compound job ID before counting work | Observed: Lost 275/350 multiply placed jobs; 817 placements | Extra views need deduplication; never turn an occurrence into another generation or revision |
| Work crosses recorded author IDs | Preserve owner declaration, each event author and explicit asset edge; infer responsibility only from an added decision record | Observed: Ivy edge and 344/1,042 cross-author pairs; proposed responsibility ledger | Account sharing, multiple accounts and external work defeat team/headcount interpretations; no semantic role taxonomy yet |
| Review repeated requests and shared inputs | Count exact primary text and distinct consumers separately, then inspect case context | Observed: Titanic, APEIROPHOBIA 10.4; corpus equality/input denominators | Equality is transparent but misses semantic families and changed media; reuse is neither approval nor waste |
| Plan checkpoints and resource visibility | Proposed: link task, versions, source evidence and explicit review event; attach measured billing entries when available | Observed gaps in audit; case labels “FINAL”, “Used” only partial clues | Added recording effort; missing events remain unknown; no claimed savings, failure control or optimal budget |

Failure modes here are ways a measure or proposed workflow can mislead; they are
not observed technical-generation failures.

## 7. Studio implications — proposals awaiting validation

| Evidence → requirement or hypothesis | Proposed behaviour | Validation test |
| --- | --- | --- |
| Disjoint folder pairs; Fallen Leaves counterexample → navigation and dependencies need independent identities | Support folders plus search by scene/entity/model/author with compound IDs and visible lineage; semantic tags carry their source | Synthetic folder move/rename leaves dependency and job counts unchanged; human retrieval exercise checks correct record recovery, without claiming production benefit |
| KAGEROU's repeated labels; unresolved versions → version identity must be explicit | Store element/version IDs, source assets and declaration provenance; distinguish inferred derivatives from approved versions | Synthetic repeated names create no version link; explicit version event creates a scoped link; adjudicate with Studies 03/07 |
| 24 multi-author films; Ivy cross-author edge → authorship does not assign responsibility | Keep owner declaration, job author, responsible reviewer and responsibility-transfer event as separate fields | Synthetic two accounts produce an edge without a team/approval event; a human assignment changes responsibility only with recorded actor and scope |
| Repeated text and reuse; missing acceptance → checkpoints need their own events | Store candidate, further-work use, review, approval and rejection separately; link the reviewed asset version | Human review exercise and synthetic reused-but-unreviewed candidate must retain unknown acceptance; Study 09 refines states |
| No reconciled spending ledger → budget control is a product hypothesis | Propose task/project caps, user-entered estimates separately from actual billed amount, unit/currency, rate source/date and reservation/reconciliation events; missing prices stay unknown | Simulated priced/unpriced jobs, concurrent reservations, cancellation and reconciliation; enforce cap only under defined billing semantics; no conversion of archive counts into money |
| Event-window and capture limitations → provenance must travel with resource totals | Display job numerator, declared duration, source snapshot, scope, unavailable fields and each cost/time unit independently | Synthetic null/empty, malformed JSON, repeated placements and external inputs preserve their states; user cannot mistake event span for hours worked |

All behaviours are **proposed**; none was implemented as studio architecture in
this slice or observed as the platform's internals. There is no controlled benefit
evidence, experimentally supported recommendation or “best practice” claim.

## 8. Unresolved questions and downstream handoff

Study 02 must refine scene/shot/deliverable semantics and reconcile differing
brief/catalogue duration declarations without pretending to verify finished media.
Studies 03/07 must resolve element versions and raw/preview aliases before semantic
reuse/canonical measures. Study 04 and the pending model labels can distinguish
repeated instruction components from exact-string equality; their labels and
agreement do not yet exist. Studies 05/06 provide operation/route definitions;
Study 08 provides model and author-role/handoff interpretation; Study 09 provides
iteration families and review semantics. Every provisional definition and its
specific dependency is listed in section 3. These pending studies do not delay the
present structural measures or authorise assuming their answers.

The evidence does **not allow** comparable-format generations per finished minute,
labour/person-hours, headcount/team structure, semantic author specialisation or
responsibility transfers, rendering latency, production speed/productivity,
monetary cost/savings/budget adherence, generation failure/retry/rejection rates,
final acceptance or waste. Raw-ID reuse does not allow canonical-version counts
or semantic duplicate counts. No future study using only these public records
can manufacture missing ledgers, verified screen time or private work.

Study 12 receives operating requirements with explicit tests and evidence limits,
not an architecture decision or ranked implementation roadmap. Study 11 may use the
descriptive cohort measures after recording winners separately; no winner labels
or comparison with the uncollected catalogue are inferred here.

## 9. Reusable code, outputs and reproduction

Run from the repository root:

```bash
uv sync --locked
uv run python scripts/fetch_data.py
uv run python studies/10-organisation/build.py
uv run python scripts/fetch_data.py --output data/study10-fresh
uv run python studies/10-organisation/build.py --data data/study10-fresh --output data/study10-reproduced --check
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/check_repository.py
```

The build test runs the full reproduction when the fetched data is present;
CI without data explicitly skips that integration test and runs synthetic boundary
checks plus committed-output/input hash checks. No real record is copied into a
fixture. The fresh-fetch command verifies all 28 assets, then the study's `--check`
compares every output byte, including the reproduction manifest, against the
committed build. `--check` requires a separate output directory. Original data,
Study 01, case files and prompt-label tools are unchanged.

| Output | Measure / provenance contract |
| --- | --- |
| [film_metrics.csv](outputs/film_metrics.csv) | 157 per-film rows; all counts and their denominators; exact event extrema; jobs/declared-minute within-film only; source scopes in metric_evidence joined on film_id; inherited threshold fields are inferred |
| [metric_evidence.csv](outputs/metric_evidence.csv) | 157 full numeric excerpts; study/film/entity scope, source/query path, observed label, alternatives, denominators and confidence; aggregate entity scope means all compound keys in named tables, selectable by film ID using SQL |
| [summaries.csv](outputs/summaries.csv) | Per-film mean, median/IQR beside pooled numerator/denominator; explicit eligible film IDs; measured subset is exactly members with positive nonmissing metric denominator in film_metrics; non-share metrics use measured-film denominator; no aggregate duration-economics ranking |
| [by_generation_type.csv](outputs/by_generation_type.csv), [by_model_identifier.csv](outputs/by_model_identifier.csv) | Film × literal type/model; counts, within-stratum nonempty text and repeat excess, author counts and total film-job denominator; null type remains unavailable |
| [summary_generation_type.csv](outputs/summary_generation_type.csv), [summary_model_identifier.csv](outputs/summary_model_identifier.csv) | Every literal type/model × cohort plus all-primary; exact film sets with jobs; equal-film job share uses all eligible cohort films including absent=0, pooled share uses cohort jobs; text mean uses only positive nonempty denominators |
| [author_operations.csv](outputs/author_operations.csv) | Film × author ID × type × model counts; owner-match flag, film/authored denominators, author-job denominator and share; unavailable author/owner match stays unavailable |
| [panel_comparison.csv](outputs/panel_comparison.csv) | All 16 panel films and matched IDs with full-export measures and inferred code 10.1 value; join evidence_id to case_evidence; not semantic prevalence |
| [case_evidence.csv](outputs/case_evidence.csv) | All 80 unchanged 10.x assignments with exact provenance and case source paths; short excerpts only, no full prompts |
| [cross_author_examples.csv](outputs/cross_author_examples.csv) | One deterministic explicit asset edge per film with cross-author pairs (21 rows); compound film/producer/consumer/asset IDs and literal authors, pair totals, observed label, deterministic excerpt, alternatives and confidence |
| [reproduction.json](outputs/reproduction.json) | SHA-256 of snapshot manifest, build/SQL/programme/upstream registers and case ledgers, plus every generated CSV; no machine paths, times or usernames |

For type/model/author rows, the evidence label is **observed** counts; exact entity
scope is all jobs in that film satisfying the row's literal dimensions. Join to
`metric_evidence` for alternatives and confidence. Summary excerpts are the numeric
row itself; its source is the per-film rows and query/build paths, with explicit
film sets. No semantic meaning is assigned by those joins. Case source files and
traced examples supply the narrower substantive interpretations.

Every output is below **1 MB**, committed beside the code. No `study-10-v1` release
is needed; no large data, full prompt text or data-directory file is committed.
