# Image and Video Studio — Research Programme

Prepared for Aleix · 20 October 2026

## Purpose

Turn the Higgsfield festival corpus into an evidence-based understanding of how creators build images and films, then translate that understanding into requirements for an image and video studio and its AI harness.

This is a plan for twelve separate deep analyses, not a claim that their hypotheses have already been established. The goal is to understand creative decisions, reusable elements, context assembly, generation, compositing, animation, continuity, revision, editing, pacing, and coordination as one production system.

The analyses must preserve three layers:

1. **Observed creator practice:** what the archived records and inspected media demonstrate.
2. **Interpretation:** a plausible explanation of the practice, with alternatives and limits.
3. **Studio design proposal:** a capability or architecture we could build in response, then test.

Creator workflows do not establish that creators used autonomous agents. The public records do not reveal Higgsfield's internal orchestration, infrastructure, private prompts, or execution architecture. A proposed harness must be labelled as our design rather than a reverse-engineered fact.

## Evidence reviewed and available

Reviewed foundations: research handover, README, data-model validation, validation report, four manually inspected film case studies, and the schemas of all fourteen exported CSV tables. [One sentence about an unrelated attachment was removed.]

| Evidence | Available scope | Use and limitation |
| --- | --- | --- |
| Catalog | 6,224 unique films | Descriptive landscape and selection context; detailed production records are unavailable for most films. |
| Priority cohort | 186 films: 126 shortlisted union top 100 watched, with 40 overlapping | A deliberately selected cohort, not a representative sample of all creators. |
| Completed public histories | 157 priority workspaces plus Cosmic tracks as a separate pilot | Use 157 for primary cohort analyses; report the additional pilot separately. Six public priority workspaces are unavailable and 23 non-open-source listings are excluded. |
| Generations | 130,899 records across the collected corpus | Prompts, model IDs, parameters, batch IDs, authors, dates, and outputs where exposed. Published histories may omit outside work. |
| Text | 124,642 nonempty primary prompts; 161,836 nested prompt/text fields | Includes scripts and other text, not just interchangeable generation prompts. |
| Dependencies | 469,242 asset-usage occurrences; 5,223 disclosed reference elements | Explicit attached inputs and outputs support lineage analysis. Occurrences are not distinct assets or independent observations. |
| Organisation | 3,246 folders plus generation/asset placements | Folder names are clues, not proof of scene order, production order, or workflow maturity. |
| Briefs | 119 retained decoded, visibility-sanitized documents | Planning evidence with uneven coverage; generic template text must be excluded from substantive claims. |
| Media | Final-film and asset URLs, but no media binaries | Visual quality, motion, sound, final shot order, and pacing require an additional inspection pass. URL availability is not guaranteed. |

Use data/films.csv, priority_films.csv, folders.csv, generations.csv, assets.csv, asset_usages.csv, asset_folders.csv, generation_folders.csv, generation_prompts.csv, reference_elements.csv, brief_assets.csv, model_usage.csv, extraction_log.csv, and other_items.csv. Use raw/project records to resolve preserved fields rather than assuming every value has a dedicated CSV column.

A full structural scan performed for this plan found 92,216 image jobs, 38,544 video jobs, 133 audio jobs, one text job, one image_3d job, and four jobs with unavailable type. Every exported generation has a date and is marked completed. Consequently, this snapshot cannot estimate technical generation-failure rates; observed artefacts and explicit creator rejection are separate questions. The audio-job count is sparse relative to the video corpus and cannot represent the full sound-production process.

Parameter objects contain fields for reference elements, media inputs, image editing, camera/lens settings, audio generation, multi-shot instructions, drafts, and extensions. Key presence does not establish a nonempty value, an enabled feature, or actual use; each study must inspect values and applicable model semantics. Usage records explicitly distinguish input image, video, audio, start-image, and end-image roles. Only two nested text rows carry the exported negative role, so negative constraints must also be coded inside ordinary prompt text rather than measured only from that role label. These checks establish analysis feasibility, not creative effectiveness.

Do not retrieve private workspaces, hidden prompts, blocked brief snapshots, or authenticated reference libraries. Existing sanitized evidence is the starting point.

## Shared method for every analysis

### Units and joins

- Keep film, creator, generation, batch, asset, reference element, folder placement, shot, and final-film time interval distinct.
- Join generations on (film_id, generation_id), assets on (film_id, asset_id), and folders on their compound film/folder keys. Shared source IDs can recur across films.
- Keep original prompt text and parameter paths alongside any derived tags. Parse JSON and CSV correctly; prompts can span lines and exceed spreadsheet cell limits.
- Preserve unavailable values (\\N) separately from explicit empty strings. A missing reference record is not proof that a generation was text-only.
- Use explicit input/output relationships before chronology, filenames, folder proximity, or visual similarity. Label inferred relationships and attach a confidence level.
- Dates describe recorded events; they do not reveal continuous labour time, rendering latency, or the date a final editorial decision was made.

### Sampling and analysis

Compute applicable metadata measures across the completed cohort, with a denominator for every measure. Use per-film summaries as the primary comparison so prolific projects do not dominate. Also show generation-weighted results where useful. Account for repeated prompts, batches, and multiple films by one creator rather than treating them as independent observations.

Build a shared panel of approximately 16 deeply inspected projects, stratified across visual style, duration, narrative demands, model diversity, reference use, visible organisation, and cohort membership. Include the existing four cases where suitable; Cosmic tracks remains a supplemental pilot. Seek contrasting production approaches within similar tasks. Make access failures explicit and document replacements.

Calibrate the coding scheme on four projects, then extend it. Use a second independent review for ambiguous categories and a subset of coded material when available. LLM labels are provisional: retain source excerpts, validate samples, and report uncertainty. A single style of prompting or a single creator must not define the codebook.

Final films need timed viewing and selected intermediate-media inspection. Automatic shot-boundary detection, transcription, embeddings, or similarity tools may assist later analyses, but their outputs need verification. No method or model is selected by this plan.

### Required evidence labels

- **Observed:** directly supported by a source record or inspected media.
- **Creator-stated:** reported in a brief or description; not independently demonstrated.
- **Inferred:** an interpretation supported by named evidence, with alternatives.
- **Associated:** a measured relationship, not a causal conclusion.
- **Experimentally supported:** a controlled test supports the claim under specified conditions.
- **Proposed:** a studio/harness design recommendation awaiting implementation or validation.

A shared practice requires recurrence across independent projects. A promising practice also needs a credible relationship to assessed outcomes. A tested best practice needs a defined task and evidence of benefit under stated conditions. No universal ranking follows from popularity, prompt length, model count, or folder depth.

## Programme overview

| Study | Subject | Main studio decision |
| --- | --- | --- |
| 01 | Corpus, creative formats, and evidence map | Which use cases and comparisons should the studio support? |
| 02 | Brief, narrative, and production decomposition | How should intent become scenes, shots, and executable tasks? |
| 03 | Visual development and reusable elements | What entities and reference packages need persistent identity? |
| 04 | Prompt design and context assembly | What information should each generation receive, and from where? |
| 05 | Image construction, editing, and composition | How should elements be combined and corrected in still images? |
| 06 | Video generation, motion, and shot control | How should a planned shot become a controllable moving clip? |
| 07 | Continuity, lineage, and cross-shot reuse | How should identity, state, and dependencies persist across outputs? |
| 08 | Model roles and workflow architecture | How should operations, model capabilities, and handoffs connect? |
| 09 | Iteration, evaluation, and human decisions | How should alternatives be reviewed, revised, and approved? |
| 10 | Editing, pacing, sound, and final assembly | How should generated material become a coherent viewing experience? |
| 11 | Organisation, collaboration, and production economics | How should the studio manage work, ownership, budgets, and recovery? |
| 12 | Harness design, experiments, and implementation roadmap | Which components should we build and how will we validate them? |

## 01 — Corpus, creative formats, and evidence map

**Research question:** What kinds of productions are represented, and which questions can we answer reliably for each?

**Inputs:** films, priority_films, extraction_log, model_usage, validation reports; metadata summaries of other tables; a sample of final films.

**Steps**

1. Freeze the snapshot and define primary, supplemental, excluded, and unavailable populations. Record overlaps in shortlist/popularity membership.
2. Build a per-film coverage matrix for briefs, prompt fields, dates, generation status, inputs, outputs, authors, references, and accessible media.
3. Develop a creative taxonomy: image-led versus film-led production; narrative/montage/music-led/experimental format; realism/stylisation; dialogue; recurring characters; location and action complexity.
4. Separate catalog-declared attributes from analyst-coded attributes. Treat terms such as cinematic quality as something to assess, not a universal property of the cohort.
5. Profile distributions by project, generation type, duration, creator, and model identifiers. Audit very large or unusual projects before accepting them as typical.
6. Select and document the shared case panel and matched contrasts. Establish the annotation and quality rubrics for subsequent studies.

**Measures:** feature coverage by film and task; creative-category counts; generations per film; model diversity; reference coverage; complete-case versus broader-cohort differences.

**Deliverables:** corpus/evidence map, creative taxonomy, case-panel register, shared data dictionary and annotation rubric.

**Studio translation:** a use-case map and a list of evidence-backed requirements versus unresolved product assumptions.

**Completion test:** every downstream study can state its eligible population and unavailable evidence. This study does not attempt to explain workflow effectiveness.

## 02 — Brief, narrative, and production decomposition

**Research question:** How does an idea become a world, a story, scenes, shots, and generation tasks?

**Inputs:** substantive brief content, descriptions, generation_prompts, folders/placements, selected final films. Use Study 01 categories.

**Steps**

1. Extract actual objectives, intended audience/effect, story premise, constraints, visual intentions, and deliverables. Flag copied template headings and empty planning sections.
2. Code narrative structure: setup, change, stakes, escalation, resolution; recurring motifs and scene purposes where supported.
3. Identify explicit scene/shot planning, boards, shot lists, and multi-shot instructions. Keep creator-stated plans separate from analyst reconstruction of the finished film.
4. Map brief concepts to named characters, environments, props, planned actions, and generation tasks using evidence links and confidence.
5. Compare scene-first, character-first, reference-first, exploratory, and edit-led approaches. Do not infer these solely from folder names or creation dates.
6. Compare intended story with delivered story in the case panel. Identify where decomposition is explicit, implicit, or unobservable.
7. Draft a structured brief and scene/shot specification from the recurring information needs; identify where a human must clarify ambiguity.

**Measures:** substantive planning coverage; observed links from plans to assets/shots; narrative and scene complexity; planning changes only where versions or records demonstrate them.

**Deliverables:** planning-pattern catalogue; annotated brief-to-shot maps; brief, scene, and shot schemas with evidence requirements.

**Studio translation:** a planning workspace and task decomposition contract. Candidate fields include scene purpose, subject state, setting, action, duration intent, references, constraints, and acceptance criteria.

**Boundary:** narrative intent belongs here; actual shot timing, pacing, and sound belong in Study 10. Earliest visible generation is not necessarily the beginning of production.

## 03 — Visual development and reusable elements

**Research question:** What must be designed once, represented consistently, and made reusable before or during production?

**Inputs:** reference_elements, assets, brief_assets, relevant prompts, folders and asset placements; inspected reference media.

**Steps**

1. Classify reusable entities: characters, outfits, poses, locations, layouts, props, materials, palettes, lighting, style references, voice/sound references where disclosed.
2. Distinguish an entity's identity from its variations: the same character in another outfit or emotional state; the same room from another angle or time of day.
3. Inspect reference packages: single images, multi-angle sheets, expression sheets, location boards, spatial blockouts, style sheets, and named elements.
4. Record where each property is specified: prose, image, structured reference metadata, generation parameter, or a combination.
5. Trace observable creation and reuse of entity versions. Distinguish declared canonical assets from merely frequently reused assets.
6. Compare reference richness against production demands within similar projects. Do not equate more references with better results.
7. Define minimum information and versioning needs for a reusable studio element.

**Measures:** reference-package types; assets per element; cross-scene reuse coverage where scenes are verified; version proliferation; explicit identity/state separation.

**Deliverables:** element ontology, annotated reference-package examples, candidate visual-bible structure, element/version schema.

**Studio translation:** persistent character/location/prop/style libraries with source media, descriptions, variants, approval status, and use history.

**Boundary:** this study defines the reusable building blocks. Cross-shot continuity performance is assessed in Study 07. Without media inspection, visual-bible completeness remains a documentation measure.

## 04 — Prompt design and context assembly

**Research question:** What do creators describe, what do they leave to references or other context, and how does that change by task?

**Inputs:** generations, generation_prompts, parameters_json, attached-input records, reference_elements, brief_assets; output inspection for selected cases.

**Steps**

1. Separate primary prompts, negative prompts, shot-level prompts, scripts, creative directions, and other nested text by source path and task. Avoid double-counting the same text in two exports.
2. Code semantic components: subject, identity, action, environment, spatial relations, composition, lens/framing, camera motion, lighting, material, aesthetic, timing, exclusions, and preservation instructions.
3. Pair each prompt with the inputs actually attached to that generation and any explicitly linked reusable elements.
4. Build an information-location matrix: each relevant property may be explicit in text, visible in attached media, stored in reference metadata, contradicted across channels, or unobservable. Text-only absence does not establish the full conditioning supplied to a model.
5. Examine short edits, complete scene descriptions, structured prompts, multi-shot instructions, reference tokens, and repeated reusable passages separately.
6. Inspect a sample of outputs to determine which unspecified details were realised. Classify omissions as potentially reference-supplied, delegated, irrelevant, or unknown; intent is unknown unless the creator states it.
7. Analyse conflicts, overload, ambiguous references, and changes across revision chains. Compare within task and literal model/version, with per-film results.
8. Propose a context-assembly specification: global project rules, entity context, scene state, shot task, attached assets, negative constraints, and operation-specific instructions. Mark all proposed automatic inheritance as a design choice.

**Measures:** semantic component presence; text/reference overlap and contradiction; prompt length distributions by operation; repeated-text concentration; local versus full-rewrite revisions; manual label agreement.

**Deliverables:** prompt taxonomy, information-location matrix, annotated prompt/input/output cases, task-specific prompt patterns, context-assembly contract.

**Studio translation:** a context builder that selects relevant approved information, resolves reference labels, records the exact submitted payload, and exposes conflicts before execution.

**Boundary:** prompt patterns are not automatically best practices. Provider defaults and hidden system instructions cannot be recovered from this corpus.

## 05 — Image construction, editing, and composition

**Research question:** How are characters, environments, objects, and styles combined into usable still images and shot foundations?

**Inputs:** image-generation/edit records, parameters, asset_usages, reference elements, output media; concepts defined in Studies 03–04.

**Steps**

1. Classify operations from explicit inputs and parameters: fresh generation, reference-guided generation, local edit, multi-input composition, reframe, upscale, and other operations only where supported. Record unknown cases.
2. Reconstruct image dependency chains. Identify where characters, scene plates, props, layouts, and style references converge.
3. Compare instructions for placement, scale, perspective, occlusion, lighting integration, matching materials, and preserving existing regions.
4. Inspect input/output pairs to assess what actually changed and what drifted. A request to preserve an identity is not proof that it was preserved.
5. Distinguish semantic conditioning on several images from literal compositing, layers, masks, or editing operations. Claim masks/layers only when disclosed.
6. Examine one-pass versus staged construction and local correction versus complete regeneration for similar tasks.
7. Catalogue routes to scene plates, keyframes, posters, reference sheets, and final stills, with tradeoffs and exceptions.

**Measures:** number/type of explicit inputs; lineage depth; local-edit share; composition patterns; human-rated spatial/lighting integration and preservation in sampled pairs.

**Deliverables:** image-operation taxonomy, construction recipes supported by cases, input/output comparisons, proposed operation contracts.

**Studio translation:** image workflow nodes with explicit input roles, preservation constraints, editable regions where supported, variants, and review points.

**Boundary:** a folder called Editing does not prove a specific editing tool. Missing operations may have occurred outside the platform.

## 06 — Video generation, motion, and shot control

**Research question:** How does a still concept or scene plan become a controllable moving shot?

**Inputs:** video-generation parameters and text, image/video input roles, outputs, reference elements, inspected clips and corresponding final-film passages where identifiable.

**Steps**

1. Classify explicit routes: text-to-video, image-to-video, video-guided generation, start/end-frame conditioning, and multi-shot generation where the parameters establish them. Unknown input coverage remains unknown.
2. Decompose shot instructions into subject action, camera action, environment motion, temporal events, dialogue/audio intent, and invariants.
3. Compare shot duration, aspect ratio, resolution, and controls within supported model/version groups. Preserve raw parameter semantics instead of forcing unlike controls into one scale.
4. Examine how creators reduce difficult action into separate shots, change camera movement, use cutaways, or revise keyframes where observable.
5. Inspect clips for motion coherence, camera/action conflicts, identity drift, geometry changes, start/end behaviour, and temporal artefacts.
6. Link generated clips to final passages only with documented evidence and confidence. Compare generated length with used length for verified matches.
7. Draft shot-level inputs, constraints, validation checks, and routes for retrying, revising references, or changing the shot plan.

**Measures:** route frequencies among classifiable records; control coverage; clip-duration distributions; sampled motion defects; preservation ratings; verified used/generated duration ratio.

**Deliverables:** shot-control taxonomy, motion prompt patterns, route comparison, video-node specification and failure catalogue.

**Studio translation:** a shot executor that accepts temporal intent and invariants, supplies the correct conditioning media, and returns reviewable clips with provenance.

**Boundary:** generation timestamps do not measure rendering speed. Video quality and action completion need actual clip inspection.

## 07 — Continuity, lineage, and cross-shot reuse

**Research question:** How do identity, world rules, spatial relationships, and narrative state persist across a production?

**Inputs:** explicit asset lineage, reference reuse, prompts, element versions, verified scene/shot maps, inspected sequences.

**Steps**

1. Define continuity dimensions: face/body, outfit/props, style, lighting, location layout, screen direction, action state, and narrative state.
2. Construct a typed dependency graph connecting generators, assets, reference elements, and verified shots/scenes. Include external inputs and disconnected components.
3. Identify stable reference hubs, independent branches, shared ancestors, cross-model reuse, and convergence. Resolve raw/preview variants before counting reuse where evidence permits.
4. Compare shared canonical references with using preceding outputs as new references. Inspect whether chaining accumulates drift; do not assume it does.
5. Compare adjacent final shots and repeated appearances. Assess continuity with a consistent rubric and distinguish intentional variation from errors.
6. Examine changes to an entity or scene state and their downstream consequences. Estimate which outputs would need review after a reference changes.
7. Define lineage, canonical-version, scene-state, and downstream-review requirements for the studio.

**Measures:** explicit reuse reach; lineage depth/branching; disconnected share; continuity scores on inspected sequences; observed version changes; downstream dependency counts.

**Deliverables:** continuity-strategy catalogue, project lineage maps, annotated continuity cases, entity-state and invalidation policies.

**Studio translation:** persistent identities, explicit state overrides, version-pinned references, lineage inspection, and a review queue for affected descendants.

**Boundary:** a high-degree asset is not necessarily a successful asset. Similarity can suggest a link but cannot replace explicit provenance.

## 08 — Model roles and workflow architecture

**Research question:** How are capabilities divided across models and operations, and which workflow structures recur?

**Inputs:** direct generation records, explicit input/output graph, model_usage summaries as cross-checks, operation labels from Studies 05–07, substantive creator statements.

**Steps**

1. Define roles such as character design, reference sheet, environment, composition, local edit, animation, voice, and finishing where evidenced.
2. Build a role-by-model matrix using actual jobs and input/output relationships, keeping literal model IDs and labels. Do not infer undisclosed providers.
3. Identify model-to-model transitions supported by asset edges; distinguish these from unrelated use of two models in one project.
4. Compare recurring workflow structures: direct generation, reference preparation followed by generation, branching variants, staged refinement, and recurrent cross-model handoffs.
5. Compare specialist and narrow-stack projects within similar creative demands. Analyse creator-stated selection reasons separately from inferred reasons.
6. Define workflow-node contracts: inputs, outputs, prerequisites, references, parameter compatibility, validation, and unknowns.
7. Translate recurring structures into proposed orchestration patterns and identify which paths could be deterministic, require human choices, or might justify planning agents.

**Measures:** role concentration; models per role/project; explicit transition frequencies; workflow-pattern prevalence by film; cross-model handoff points; unknown-role share.

**Deliverables:** capability/role matrix, evidence-backed workflow archetypes, annotated handoff examples, candidate node contracts and routing rules.

**Studio translation:** a model-adapter layer and workflow executor driven by task capabilities and constraints. Current API availability and pricing require separate official-source verification at implementation time.

**Boundary:** the archive reveals chosen workflows, not the platform's scheduler, queue, agents, caching, retry engine, or hidden routing policy. Those remain proposed architecture.

## 09 — Iteration, evaluation, and human decisions

**Research question:** How do creators explore, diagnose, correct, and decide when to continue?

**Inputs:** batch IDs, lineage, dates, status fields, prompt deltas, local-edit chains, author records, inspected alternatives and outputs.

**Steps**

1. Establish which evidence can identify an iteration family. Use shared inputs/batches and explicit lineage before prompt similarity and timing.
2. Separate parallel alternatives, reruns, local corrections, changed creative direction, model changes, and likely unrelated jobs. Label uncertainty.
3. Compare prompt/input changes across families: additions, deletions, specificity changes, preservation instructions, and input replacement.
4. Separate technical execution failure, visible creative defects, creator-stated rejection, and absence from the final film. These are different outcomes.
5. Examine what changes after observed defects and whether revisions resolve them in inspected pairs.
6. Identify explicit selection/approval evidence where present. Treat downstream reuse as adoption for further work, not final acceptance.
7. Propose an evaluation rubric, candidate comparison interface, escalation rules, stop conditions, and human approval points.

**Measures:** variants per classifiable family; number/type of revisions; prompt/input change patterns; technical statuses with known denominators; sampled defect resolution. Do not invent acceptance rates or time saved.

**Deliverables:** iteration taxonomy, revision case histories, quality rubric, candidate-review specification, proposed human/automation responsibility map.

**Studio translation:** explicit draft/candidate/review/approved states, recorded decision reasons, targeted repair routes, bounded retries, and human control over creative direction.

**Boundary:** adoption, approval, and publication are distinct. A published snapshot may omit discarded material, failed work, or earlier decisions.

## 10 — Editing, pacing, sound, and final assembly

**Research question:** How do generated assets become a coherent film with rhythm, meaning, and emotional progression?

**Inputs:** accessible final films, timed shot annotations, substantive briefs/scripts, audio-related records, generation clips for verified matches. Media inspection is mandatory.

**Steps**

1. Build a final-film shot/scene timeline: timestamps, shot scale, subject/action, camera motion, transition, dialogue, music, ambience, and sound effects.
2. Define narrative beats and emotional changes from the film itself, with analyst/creator attribution where relevant.
3. Measure shot-length distributions and local pacing curves; compare introduction, escalation, climax, and resolution where those structures apply. Avoid reducing pacing to average shot length.
4. Analyse visual information density, action speed, pauses, reaction shots, cutaways, transitions, contrast, and shot-to-shot relationships.
5. Examine sound-image relationships: voiceover-led versus image-led storytelling, music accents, silence, continuity bridges, dialogue timing, and sound effects.
6. Match final passages to source generations where evidence supports it. Record crops, trims, speed changes, text overlays, grading, or other transformations only when demonstrable. Treat edit software and external production steps as unknown unless disclosed.
7. Assess whether editing compensates for generation limitations, while separating an observable cut from an inferred reason for making it.
8. Translate recurring patterns into timeline metadata, editorial checks, and optional creative suggestions; avoid universal rules for optimal shot length.

**Measures:** shot-duration distributions and variability; cuts per minute in local windows; scene/beat lengths; transition and audio-event frequencies; continuity breaks; verified clip utilisation; inter-reviewer agreement for interpretive labels.

**Deliverables:** annotated timelines, pacing curves, sound/editing pattern catalogue, generation-to-final evidence map, timeline/assembly requirements.

**Studio translation:** a timeline aware of scene purpose, shot order, clip trims, audio layers, and continuity, with human editorial control.

**Boundary:** source generation order and folder order are not final edit order. Without film access, this analysis must report an evidence gap rather than invent a pacing assessment. Sound workflow details may be externally produced and unobservable.

## 11 — Organisation, collaboration, and production economics

**Research question:** How is work organised and coordinated, and what production effort can we actually measure?

**Inputs:** folders/placements, authors, recorded dates, explicit lineage, project metadata, disclosed credits or other usage fields only where present and interpretable.

**Steps**

1. Classify organisation by scenes, entities, asset types, production stages, or mixed structures. Compare with actual dependencies and project scale.
2. Identify owner/contributor differences and observable author specialisation. Multiple authors do not by themselves prove a team structure or role hierarchy.
3. Map recorded activity windows and cross-author asset handoffs. Do not convert gaps between timestamps into hours worked.
4. Audit reusable assets, repeated prompts, duplicated placements, and repeated generation families without counting these as proven waste.
5. Verify whether cost/credit fields have clear meaning and scope. Report historical disclosed values separately from estimates; do not reconstruct bills from current prices.
6. Compare resource proxies such as generations per finished minute within comparable creative formats. More generations can reflect complexity, experimentation, or incomplete visibility.
7. Derive proposed needs for ownership, permissions, versioning, search, budgets, checkpoints, resumability, and provenance; distinguish observed needs from engineering safeguards.

**Measures:** organisation categories; author counts; cross-author reuse; recorded activity spans; generations per minute with caveats; reference reuse; verified disclosed usage totals where feasible.

**Deliverables:** organisation/collaboration patterns, resource-visibility audit, operating-model recommendations, explicit unknowns around cost and productivity.

**Studio translation:** a shared project store, asset search, ownership and review responsibilities, job ledger, budget controls, resumable runs, and audit history.

**Boundary:** no labour-productivity, dollar-cost, speed, or return-on-investment claims without the required evidence. Existing histories are not a complete accounting ledger.

## 12 — Harness design, validation experiments, and implementation roadmap

**Research question:** Given the evidence, what should our studio orchestrate, what should remain a human decision, and what should we build first?

**Inputs:** the eleven studies, evidence ledger, candidate patterns, unresolved questions, and Aleix's eventual product constraints. The current material is insufficient to assume a particular target customer, deployment model, or budget.

**Steps**

1. Consolidate recurring production problems and map every proposed capability to evidence or an explicit product hypothesis. Avoid building a feature solely because it appears in one impressive film.
2. Specify a shared domain model: project, brief, entity/version, scene, shot, task, generation candidate, asset, reference, review decision, and timeline placement. Keep recorded source facts separate from analyst annotations and generated plans.
3. Define component responsibilities: project/asset storage; brief and shot planning; context assembly; operation/model adapters; workflow execution; job/provenance ledger; evaluation and human review; timeline/export.
4. Define contracts and state transitions, version pinning, missing-input handling, change propagation, bounded retries, cancellation, duplicate-job prevention, and recovery. These are proposed engineering decisions, not recovered platform internals.
5. Assign responsibilities. Deterministic code should own identifiers, dependencies, versions, budgets, and state. Planning models may propose decompositions or repairs. Humans should approve identity/style references, ambiguous creative changes, and final editorial choices unless a product test supports another policy.
6. Design controlled experiments before calling a pattern best practice: reference sheet versus textual identity description; staged composition versus one-pass generation; local edit versus full regeneration; fixed versus varying motion instructions; different continuity strategies. Test only supported capabilities and choose comparisons that isolate a meaningful variable.
7. For each test, predefine task, baseline, changed factor, outputs, independent repetitions, quality rubric, reviewer blinding where possible, resource budget, and acceptance criteria. Keep intended improvements separate from non-inferiority checks for preserved properties. Keep evaluation examples separate from prompt-tuning examples.
8. Prioritise by evidence strength, user value, implementation effort, and failure impact. Identify the smallest end-to-end workflow that tests the main product assumption.
9. Create a phased roadmap with measurable gates, open assumptions, and explicit deferred capabilities. Verify current vendor documentation, APIs, constraints, and prices using official sources when choosing the implementation.

**Suggested initial vertical slice, to validate:** brief → approved character/location references → composed still or shot keyframe → short video candidate → human review and targeted revision → simple timeline/export. It should also support stopping at a finished still image. This is a design proposal, not a dataset finding.

**Deliverables:** traceable studio architecture, schema/node contracts, human/automation responsibility matrix, experiment backlog, MVP specification, and phased implementation roadmap.

**Completion test:** every high-priority capability has a user problem, supporting evidence or labelled hypothesis, an owner/component, acceptance criteria, and a feasible test. Full autonomy is not assumed to be a prerequisite.

## Execution order and dependencies

Complete Study 01 first to freeze the population, sample, vocabulary, evidence labels, and media-access plan.

Then run Studies 02 and 03. They establish planning and entity concepts. Study 04 uses these definitions; Studies 05 and 06 use the prompt/context coding while retaining separate image/video operation schemes. Study 07 connects the resulting evidence across shots. Studies 08 and 09 synthesise dependencies and revision families into workflow and review patterns.

Start final-film annotation for Study 10 soon after Study 01; it need not wait for generation-history analysis. Reconcile its shot maps with Studies 02, 06, and 07 later. Study 11 can also begin after Study 01, then incorporate lineage and iteration findings. Complete Study 12 after the findings and gaps from the other studies are available.

If studies are conducted in separate chats, give each the frozen corpus, this plan, the common protocol, its own brief, and the latest relevant upstream outputs. If an upstream output is missing, use a documented provisional definition and record the dependency rather than quietly assuming the result.

## Standard output contract for each deep analysis

Each study must produce:

1. A plain-language answer to its main question, with evidence limits stated alongside conclusions.
2. Its eligible population, exclusions, coverage, units, and denominators.
3. An explicit method and codebook, including how automated labels were checked.
4. Findings by relevant creative/task/model groups, with per-film summaries and uncertainty; exploratory small subgroups should remain descriptive.
5. At least three fully traced examples and one counterexample or boundary case where evidence permits. If there are too few cases, say so instead of manufacturing a pattern.
6. A pattern catalogue: problem, observed method, required inputs, sequence, evidence, tradeoffs, failure modes, and applicability.
7. A studio-implication table: evidence → requirement/hypothesis → proposed behaviour → validation test.
8. Unresolved questions, missing evidence, and the exact handoff needed by later studies.
9. Reusable annotations, query/code definitions, and data outputs as appropriate. Keep original data unchanged.

For every substantive finding, record study ID, film ID, generation/asset/reference IDs or final-film timestamps, source path, excerpt/observation, evidence label, competing explanation, eligible denominator, and confidence rationale. Report confidence based on evidence, not unsupported numeric certainty.

For every proposed practice, record: when to use it; prerequisites; sequence; what the model receives as text and media; what remains human-controlled; desired output; quality criteria; resource tradeoffs; exceptions; evidence strength; and proposed experiment.

## Reusable instruction for launching one study

Copy this instruction with the selected numbered brief. Attach the relevant data, this programme, and available upstream outputs. A filename or a prior summary is not a substitute for access to the underlying evidence.

> Conduct Study [NUMBER — TITLE] from the Image and Video Studio Research Programme. Work from the supplied archived corpus and the shared protocol. Complete this study's steps and standard output contract. Analyse the eligible corpus where feasible, then deeply inspect the shared case panel and the task-specific examples needed to answer the question. Keep creator-stated claims, directly observed records/media, inferences, associations, experimentally supported results, and proposed studio design separate. Give traceable IDs/source paths and timecodes for film observations. Do not infer attached inputs, final selection, edit order, cost, human intent, autonomy, or internal platform architecture from missing evidence. Use the permitted public/sanitized materials; do not retrieve hidden or private content. If media or upstream evidence is unavailable, complete the supported analysis and identify the exact gap. Translate the findings into concrete studio capabilities with tradeoffs and validation tests. Do not broaden into the other studies except to document dependencies. Do not claim an experiment was run unless it actually was; no paid generation experiments are required by this analysis brief. The target is a defensible production-practice analysis and an actionable product-design handoff, not a list of impressive prompts.

## Evidence sources in the delivered archive

- RESEARCH_HANDOVER.md — scope, table definitions, provenance, initial observations, and limitations.
- README.md — archive use, encoding, reproduction, and extraction details.
- reports/validation_report.md — completed cohort, validation checks, missing briefs, exclusions, and reconciliation.
- reports/data_model_validation.md — observed interface fields, relationships, raw parameters, and interpretation limits.
- reports/four_film_case_studies.md — Cosmic tracks, The Kiss, Fallen Leaves, and Don't Poison Ivy.
- data/*.csv and retained sanitized raw/project records — source evidence for the planned studies.

This programme creates the research structure. It does not yet establish cross-corpus creative best practices, inspect every film, measure pacing, or validate a harness implementation.
