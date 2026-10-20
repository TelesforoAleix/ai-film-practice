# How top AI creators build films: research programme (version 2)

Version 2, 20 October 2026. It revises version 1 (kept in `original/`, unchanged but for one
sentence about an unrelated attachment) after one decision: **the programme studies the
technical build, not the creative result.** Every step that needed watching a film or judging
its quality is removed.

## Purpose

Turn the Higgsfield Global Film Festival corpus into an evidence-based account of how the
festival's strongest creators technically build their images and films: how they structure a
project, which tools and models they use for what, the steps and processes they follow, how assets
connect, how many they make and reuse, and how they describe them. Then translate that account into
requirements for an image and video studio and its harness.

**Why no quality assessment.** The detailed cohort is already selected by quality: the jury's
shortlist and the audience's 100 most-watched films. Their publication validates them well enough
for this purpose. Story, aesthetics and emotional effect are subjective and would be judged
differently by every reviewer; they are out of scope. So is anything that needs the media itself
(the archive holds links, not films): shot timing, pacing, sound, visual continuity, output quality.

**What follows from that, and is said plainly in every study.** Only the priority cohort has full
production records. The findings describe *what top creators do*, not *what separates top films
from the rest*. Where the cohort itself can be split (jury shortlist, audience-popular, both; and,
once announced, the festival's winners), a study may compare the groups, descriptively.

The analyses keep three layers apart:
1. **Observed creator practice:** what the archived records show.
2. **Interpretation:** a plausible explanation of the practice, with alternatives and limits.
3. **Studio design proposal:** a capability we could build in response, then test.

Creator workflows do not show that creators used autonomous agents. The public records do not
reveal Higgsfield's internal orchestration, infrastructure, private prompts or execution
architecture. A proposed harness is labelled as our design, never as a reverse-engineered fact.

## Evidence

| Evidence | Scope | Use and limitation |
| --- | --- | --- |
| Catalogue | 6,224 unique films | Landscape and selection context (views, likes, votes, editorial and shortlist status, duration, category); no production records for most films. |
| Priority cohort | 186 films: 126 shortlisted ∪ top 100 most-watched, 40 in both | Selected, not representative of all creators. |
| Complete public histories | 157 priority workspaces; Cosmic tracks as a separate pilot | Use the 157 for cohort analyses; report the pilot separately. 6 unavailable; 23 non-open-source listings excluded. |
| Generations | 130,899 records | Prompts, model IDs, parameters, batch IDs, authors, dates, outputs where exposed. Published histories may omit work done elsewhere. |
| Text | 124,642 nonempty primary prompts (61,479 distinct); 161,836 nested text fields | Includes scripts and other text, not only interchangeable prompts. Median distinct prompt about 2,700 characters; the longest 59,522. |
| Dependencies | 469,242 asset-usage rows; 5,223 reference elements | Explicit inputs and outputs support lineage. Rows are occurrences, not distinct assets or independent observations. |
| Organisation | 3,246 folders and their placements | Folder names are clues, not proof of scene order, production order or maturity. |
| Briefs | 119 decoded, visibility-sanitized documents | Uneven coverage; generic template text is excluded from substantive claims. |

The generations are 92,216 image jobs, 38,544 video jobs, 133 audio jobs, one text, one image_3d
and four of unavailable type. Every exported generation is dated and marked completed, so the
snapshot cannot estimate technical failure rates. Parameter objects carry fields for reference
elements, media inputs, image editing, camera and lens settings, audio, multi-shot instructions,
drafts and extensions; a key's presence does not establish a value, an enabled feature or its use.
Usage records distinguish input image, video, audio, start-image and end-image roles. Only two text
rows carry the exported negative role, so negative constraints are also coded inside ordinary
prompt text.

Do not retrieve private workspaces, hidden prompts, blocked brief snapshots or authenticated
libraries. The sanitized archive is the evidence.

## Shared method

### Units and joins

- Keep film, creator, generation, batch, asset, reference element and folder placement distinct.
- Join generations on (film_id, generation_id), assets on (film_id, asset_id), folders on their
  compound film and folder keys. Source IDs can recur across films.
- Keep original prompt text and parameter paths beside any derived tag. Parse CSV and JSON
  properly; prompts span lines and exceed spreadsheet limits.
- Keep unavailable values (`\N`) apart from empty strings. A missing reference record is not proof
  that a generation was text-only.
- Prefer explicit input and output relationships to chronology, filenames or folder proximity.
  Label inferred relationships and give a confidence.
- Dates are recorded events: they do not measure labour time, rendering latency or when a decision
  was made.

### Corpus-wide analysis, the panel, and labels

- **Corpus-wide measures** come from scripts over the whole cohort, with a denominator for every
  measure. Per-film summaries are the primary comparison, so prolific projects do not dominate;
  generation-weighted results are shown beside them where useful. Repeated prompts, batches and
  several films by one creator are not independent observations.
- **The panel:** about 16 films, chosen in Study 01 from the records (production scale, model
  diversity, reference use, visible organisation, image-led or film-led, cohort group), including
  the four case-study films where suitable. Each panel film is read in depth once and coded across
  every study's dimensions in one pass (a *case file*), after the codebook is calibrated on four
  films.
- **Prompt labels at scale:** structural features (length, sections, structured formats, reference
  tokens, camera and lens vocabulary, preservation and exclusion phrases) are computed by script
  over every prompt. Semantic components are labelled by a model on a stratified sample (balanced
  by film and operation), checked against a hand-labelled gold subset, and reported with their
  agreement. Model labels are provisional; source excerpts are kept with them.

### Evidence labels

- **Observed:** directly supported by a source record.
- **Creator-stated:** reported in a brief or description; not independently shown.
- **Inferred:** an interpretation supported by named evidence, with alternatives.
- **Associated:** a measured relationship, not a cause.
- **Experimentally supported:** a controlled test supports it under stated conditions.
- **Proposed:** a studio or harness recommendation awaiting validation.

A *shared practice* recurs across independent projects. A *tested best practice* needs a defined
task and evidence of benefit under stated conditions. No ranking follows from popularity, prompt
length, model count or folder depth.

## Programme

| Study | Subject | Main studio decision |
| --- | --- | --- |
| 01 | Corpus, evidence map, panel and codebook | Which use cases and comparisons can the studio rely on? |
| 02 | Planning and production decomposition | How should intent become scenes, shots and executable tasks? |
| 03 | Reusable elements | What needs a persistent identity, and in what form? |
| 04 | Prompt design and context assembly | What should each generation receive, and from where? |
| 05 | Image construction and editing | How should stills be composed and corrected? |
| 06 | Video generation and shot control | How should a planned shot become a controllable clip? |
| 07 | Lineage and cross-shot reuse | How should identity and dependencies persist across outputs? |
| 08 | Model roles and workflow | How should operations, models and handoffs connect? |
| 09 | Iteration | How should alternatives and revisions be organised? |
| 10 | Organisation and production economics | How should the studio manage work, ownership and budgets? |
| 11 | The jury and the audience | Do the selected groups build differently? (after the winners are announced) |
| 12 | Synthesis: the technical playbook and studio requirements | What should we build first, and how do we validate it? |

## 01 — Corpus, evidence map, panel and codebook

**Question:** What kinds of productions are represented, and which questions can be answered
reliably for each?

1. Freeze the snapshot. Define primary, supplemental, excluded and unavailable populations, and the
   cohort groups (shortlist only, most-watched only, both).
2. Build a per-film coverage matrix: briefs, prompt fields, dates, inputs, outputs, authors,
   references, folders.
3. A production taxonomy from records and catalogue fields: image-led versus film-led, duration,
   category, production scale, model breadth, reference use, organisation. Catalogue-declared
   attributes stay apart from coded ones.
4. Profile distributions by film, generation type, duration, creator and model. Audit very large or
   unusual projects before treating them as typical.
5. Select the panel and its matched contrasts; document replacements.
6. Draft the shared codebook for Studies 02–10 and calibrate it on four films.

**Deliverables:** evidence map, taxonomy, panel register, data dictionary, codebook.
**Completion test:** every later study can state its eligible population and its missing evidence.

## 02 — Planning and production decomposition

**Question:** How is a project broken down into a world, scenes, shots and generation tasks, as far
as the records show?

1. Extract from substantive brief content: objectives, constraints, visual intentions,
   deliverables, planned characters, settings and shots. Flag template headings and empty sections.
2. Identify explicit scene and shot planning, shot lists and multi-shot instructions, in briefs,
   prompts and folder structure. Creator-stated plans stay apart from reconstruction.
3. Map planned entities and shots to assets and generation tasks with evidence links and
   confidence.
4. Compare scene-first, character-first, reference-first and exploratory build orders where the
   records support them; folder names or dates alone do not.
5. Draft brief, scene and shot schemas from the recurring information needs.

**Deliverables:** planning-pattern catalogue, brief-to-task maps for the panel, schemas.
**Studio translation:** a planning workspace and a task decomposition contract.

## 03 — Reusable elements

**Question:** What do creators design once and reuse, and how do they represent it?

1. Classify reusable entities: characters, outfits, poses, locations, layouts, props, materials,
   palettes, lighting, style references, voice references where disclosed.
2. Separate identity from variation (the same character in another outfit; the same room at
   another time of day), as prompts, references and names show it.
3. Classify reference packages from records: single images, multi-angle sheets, expression sheets,
   location boards, blockouts, style sheets, named elements.
4. Record where each property is specified: prose, image, reference metadata, parameter, or a mix.
5. Trace creation and reuse of element versions; declared canonical assets versus merely frequent
   ones.
6. Define the minimum information and versioning a studio element needs.

**Deliverables:** element ontology, reference-package examples, element and version schema.
**Studio translation:** persistent libraries with source media, descriptions, variants, approval
status and use history.

## 04 — Prompt design and context assembly

**Question:** What do creators write, what do they leave to references, and how does that change
by task and model?

1. Separate primary prompts, negative prompts, shot-level prompts, scripts and other nested text by
   source path and task, without double-counting.
2. Code semantic components: subject, identity, action, environment, spatial relations,
   composition, lens and framing, camera motion, lighting, material, aesthetic, timing, exclusions,
   preservation instructions.
3. Pair each prompt with the inputs actually attached and any linked elements.
4. Build the information-location matrix: each property explicit in text, carried by attached
   media, stored in reference metadata, contradicted across channels, or unobservable.
5. Examine short edits, full scene descriptions, structured prompts, multi-shot instructions,
   reference tokens and repeated passages separately, within task and literal model.
6. Analyse conflicts, overload and changes along revision chains.
7. Propose a context-assembly specification: project rules, entity context, scene state, shot
   task, attached assets, constraints, operation-specific instructions.

**Deliverables:** prompt taxonomy, information-location matrix, prompt patterns by task and model,
context-assembly contract.
**Boundary:** provider defaults and hidden system instructions cannot be recovered.

## 05 — Image construction and editing

**Question:** How are characters, environments, objects and styles combined into usable stills and
shot foundations?

1. Classify operations from inputs and parameters: fresh generation, reference-guided generation,
   local edit, multi-input composition, reframe, upscale; unknown where unsupported.
2. Reconstruct image dependency chains: where characters, plates, props, layouts and styles
   converge.
3. Code instructions for placement, scale, perspective, occlusion, lighting integration and
   preservation.
4. Separate conditioning on several images from disclosed layers, masks or editing operations.
5. Compare one-pass and staged construction, local correction and full regeneration, for similar
   tasks.
6. Catalogue the routes to plates, keyframes, posters, reference sheets and final stills.

**Deliverables:** image-operation taxonomy, construction recipes from traced cases, operation
contracts.

## 06 — Video generation and shot control

**Question:** How does a still or a plan become a moving shot, as the records show?

1. Classify routes: text-to-video, image-to-video, video-guided, start and end frame, multi-shot,
   extensions; unknown where inputs are not recorded.
2. Decompose shot instructions: subject action, camera action, environment motion, temporal
   events, dialogue and audio intent, invariants.
3. Compare duration, aspect ratio, resolution and controls within model and version groups,
   keeping raw parameter semantics.
4. Find how creators split difficult action into several shots, change camera movement or revise
   keyframes, where lineage shows it.
5. Draft shot-level inputs, constraints and retry or revision routes.

**Deliverables:** shot-control taxonomy, motion prompt patterns, route comparison, video-node
specification.
**Boundary:** clip quality and how much of a clip was used are not observable.

## 07 — Lineage and cross-shot reuse

**Question:** How do identity, world rules and dependencies persist through a production's graph?

1. Build a typed dependency graph of generations, assets and reference elements, including external
   inputs and disconnected parts.
2. Find reference hubs, branches, shared ancestors, cross-model reuse and convergence; resolve raw
   and preview variants before counting reuse where possible.
3. Compare shared canonical references with chaining (using a previous output as the next
   reference).
4. Estimate what would need review downstream if a reference changed.
5. Define lineage, canonical-version and change-propagation requirements.

**Deliverables:** continuity-strategy catalogue, lineage maps for the panel, invalidation policy.
**Boundary:** a high-degree asset is not necessarily a good one; visual continuity is not assessed.

## 08 — Model roles and workflow

**Question:** How are capabilities divided across models and operations, and which workflow
structures recur?

1. Define roles: character design, reference sheet, environment, composition, local edit,
   animation, voice and audio, editing and finishing, as evidenced.
2. Build a role-by-model matrix from jobs and input-output edges, with literal model IDs.
3. Identify model-to-model transitions supported by asset edges, apart from merely co-occurring
   models.
4. Compare workflow structures: direct generation, reference preparation then generation, branching
   variants, staged refinement, cross-model handoffs.
5. Include what the records show of audio and editing (voiceover and audio jobs, editor models);
   most sound and final editing happen elsewhere and are unobservable.
6. Define node contracts and propose orchestration patterns: deterministic paths, human choices,
   and where a planning model might help.

**Deliverables:** role matrix, workflow archetypes, handoff examples, node contracts.
**Boundary:** the archive shows chosen workflows, not the platform's scheduler, routing or agents.

## 09 — Iteration

**Question:** How do creators explore alternatives and revise, as the records show?

1. Establish what identifies an iteration family: shared inputs, batches, lineage, then prompt
   similarity and timing.
2. Separate parallel alternatives, reruns, local corrections, changed direction and model changes.
3. Compare prompt and input changes across families: additions, deletions, specificity,
   preservation, input replacement.
4. Treat downstream reuse as adoption for further work, not final acceptance.
5. Propose candidate, review and approval states and bounded retry rules.

**Deliverables:** iteration taxonomy, revision case histories, review-state specification.
**Boundary:** published histories may omit discarded work; defects are not assessed.

## 10 — Organisation and production economics

**Question:** How is work organised, and what effort can be measured?

1. Classify organisation by scenes, entities, asset types, stages or mixes; compare with actual
   dependencies and scale.
2. Owner and contributor differences, author specialisation, cross-author handoffs; several
   authors do not prove a team structure.
3. Recorded activity windows, without converting gaps into hours worked.
4. Reuse, repeated prompts and duplicated placements, without calling them waste.
5. Resource proxies such as generations per finished minute, within comparable formats.
6. Needs for ownership, versioning, search, budgets, checkpoints and provenance.

**Deliverables:** organisation patterns, resource-visibility audit, operating-model
recommendations. No productivity, cost or speed claims without evidence.

## 11 — The jury and the audience

**Question:** Do the jury's selections, the audience's favourites and (once announced, in the last
week of October 2026) the festival's winners build differently?

1. Record the winners from the public festival page when announced, with the date.
2. Compare the groups on the measures of Studies 02–10, per film, descriptively; the groups are
   small and overlapping.
3. Report differences as associations, with the alternatives (category, duration, creator).

**Deliverables:** a group comparison table and its limits.

## 12 — Synthesis: the technical playbook and studio requirements

**Question:** Given the evidence, what should a studio orchestrate, what stays a human decision,
and what comes first?

1. Consolidate the recurring production problems; map every proposed capability to evidence or an
   explicit product hypothesis.
2. A shared domain model: project, brief, element and version, scene, shot, task, generation
   candidate, asset, reference, review decision.
3. Component responsibilities and contracts: storage, planning, context assembly, model adapters,
   workflow execution, job and provenance ledger, review.
4. Responsibilities: code owns identifiers, dependencies, versions, budgets and state; planning
   models propose; humans approve references and creative changes.
5. Experiments to design before calling anything a best practice: reference sheet versus textual
   identity; staged versus one-pass composition; local edit versus regeneration; continuity
   strategies. Each with task, baseline, changed factor, repetitions, rubric and budget.
6. A technical playbook for creators: the shared practices, each with when to use it,
   prerequisites, sequence, inputs, evidence strength and limits.

**Deliverables:** the playbook, a traceable studio architecture, contracts, the experiment backlog,
an MVP specification. A suggested first vertical slice, to validate: brief → approved references →
composed still or keyframe → short video candidate → review and targeted revision.

## Order

Study 01 first: population, panel, codebook. Then the panel's case files, a few films per session,
each film coded across every study at once. Then the prompt labels on the stratified sample. Then
Studies 02 to 10, corpus-wide, using the case files and labels: 02 and 03 first, then 04, then 05
and 06, then 07, then 08 and 09; 10 may run any time after 01. Study 11 when the winners are
announced. Study 12 last.

If an upstream output is missing, use a documented provisional definition and record the
dependency, rather than assuming the result.

## Output contract for each study

1. A plain-language answer, with its evidence limits beside each conclusion.
2. The eligible population, exclusions, coverage, units and denominators.
3. The method and codebook, and how automated labels were checked.
4. Findings by task, model and cohort group, per film, with uncertainty; small subgroups stay
   descriptive.
5. At least three fully traced examples and one counterexample, where evidence permits.
6. A pattern catalogue: problem, method, inputs, sequence, evidence, tradeoffs, failure modes,
   applicability.
7. A studio-implication table: evidence → requirement or hypothesis → proposed behaviour →
   validation test.
8. Unresolved questions and the handoff later studies need.
9. Reusable queries, code and data outputs; the original data unchanged.

Every substantive finding records its study, film ID, generation, asset or reference IDs, source
path, excerpt, evidence label, competing explanation, denominator and confidence rationale.
