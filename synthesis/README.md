<!-- Generated from README.template.md and points.json by synthesis/build.py; edit those, not this file. -->

# Findings synthesis of Studies 01–10

This document gathers what Studies 01–10 found into small, self-contained points. It
covers the 157 primary workspace histories only; the supplemental Cosmic tracks
pilot is excluded. It is a synthesis, not the Study 12 deliverables: there is no
playbook, architecture, contract, experiment backlog or MVP here.

## The short version, for creators

These films' production records show how people worked on the platform. They do not
show what worked, because nothing here was watched or judged.

1. **Video starts from a picture.** In almost every film, clips were generated from an
   image or frame rather than from words alone: 93.40% of the average film's video
   jobs had an image attached. Creators make stills first, then animate them.
2. **One video model, several image models.** Most films made nearly all of their video
   with one model, seedance_2_5, the main video model in 125 of the 156 films
   with video. For images, a typical film used about 5 different models, led by
   three that take an uploaded image and change it.
3. **Video prompts are written out in full.** The typical film's video prompt runs to
   about 5,104 characters, several paragraphs covering the camera, the action, the
   setting, the timing and what to leave out. Shots and cuts are written into the
   prompt; the multi-shot switch stays off.
4. **Say what changes and what stays.** Edit requests usually name the change and
   then what must stay exactly as it is. Creators also prepare reference sheets, with
   several views of a character, and attach them to later jobs.
5. **Work is reused and handed on.** Most jobs reuse an image or clip that other jobs
   also use, outputs pass from one model to another, and batches rerun one identical
   request to get options.
6. **What this cannot tell you.** These are records of what was asked for. Only these
   films have records, so nothing here says what makes a film stand out, which
   technique works best, or how much time or money any of it took.

## How to read the points

Points are grouped by kind and ranked within each group by how interesting and how
well supported they are. Each gives the finding, how often it occurs, where in
production it shows up, its evidence label and strength, the status Study 04 gave the
definitions it uses, a traced example, its denominator, a competing explanation and
the studies it rests on.

- **How often** gives the equal-weight mean over films first: each film's share,
  averaged so that a film with many jobs counts the same as a film with few. The
  pooled share over all jobs follows where it differs. Counts carry their
  denominators.
- **Evidence labels** follow PROGRAMME.md: observed, creator-stated, inferred,
  associated, experimentally supported, proposed. Instructions are not outcomes. A
  binding or reuse is not approval.
- **Provisional labels.** Anything about instruction components comes from
  prompt-labels-v2, a local Qwen 3.6 27B model's provisional labels on a weighted
  sample (see L07). These points are labelled inferred, or the provisional part is
  named.
- **Study 04 status.** Where Study 04 confirmed, changed or left undecided a definition
  that another study used, the point uses Study 04's assessment and says so.
- **Checked numbers.** Every number in the points and in the short version is filled
  from [`citations.csv`](outputs/citations.csv) when this document is built. Each
  citation is a committed study output, or a synthesis output reproduced by
  [`build.py`](build.py), and the build fails if a cited value disagrees with its
  source. Study numbers, model names, control values and code IDs are labels, not
  measures.

This synthesis has 40 points: 12 main patterns, 7 model preferences, 11 techniques and 10 limits.

## Main patterns

### P01. Video is made from images, not from text alone

Nearly every recorded video job is bound to an image or frame; a declared text-to-video route never appears, and explicit empty-media video requests are a small residue.

- **How often:** Image-bound video jobs: 93.40% of the mean film's video jobs (pooled 94.57%, 36,417/38,508 jobs, 156 films). Empty-media candidates: 530 jobs in 82 films. Declared text-to-video: 0 jobs.
- **Where:** Video generation; image-to-video and reference-guided video. Literal models: `seedance_2_5`, `cinematic_studio_video_4_0`.
- **Evidence:** observed. Counts of recorded media bindings on video jobs.
- **Strength:** strong: whole primary population, deterministic record counts.
- **Study 04 status:** Study 08 conservative input route and direct candidate: confirmed. A job with no recorded input never establishes text-only production.
- **Example:** film 655325cc-46d9-4b0b-b03d-d177defa4b3f; 655325cc-46d9-4b0b-b03d-d177defa4b3f/generation:0035469c-1e6e-4c3f-aad6-bb3ab0bb05ce; 655325cc-46d9-4b0b-b03d-d177defa4b3f/generation:122382c3-e873-4845-8a14-89ff9dfa215e; 655325cc-46d9-4b0b-b03d-d177defa4b3f/asset:0035469c-1e6e-4c3f-aad6-bb3ab0bb05ce; source `studies/08-workflow/outputs/handoff_examples.csv (the-kiss:08.3)`; excerpt: [producer model] nano_banana_2 [consumer model] seedance_2_5 [explicit usage] asset_role reference_image
- **Denominator:** 38,508 primary video jobs in 156 video-bearing films.
- **Competing explanation:** The interface may encourage image upload first; unpublished text-only trials and history capture can shape routes; a bound image need not be the shot's start frame.
- **Confidence:** Deterministic compound-key counts of released usage rows; attached contents are not inspected.
- **Rests on:** [`studies/06-video/README.md`](../studies/06-video/README.md), [`studies/06-video/outputs/summaries.csv`](../studies/06-video/outputs/summaries.csv), [`synthesis/outputs/model_stages.csv`](outputs/model_stages.csv); checked numbers `p01a`, `p01b`, `p01c`, `p01d`, `p01e`, `p01f`, `p01g`, `p01h` in [`citations.csv`](outputs/citations.csv).

### P02. Shots share sources and build on earlier outputs

Most jobs use a source that another job also uses, and about half take an earlier job's output, so a film's history is a web of reuse rather than one-off requests. Single sources can feed very many jobs.

- **How often:** Mean film: shared-input jobs 70.89% (pooled 70.20%); chained jobs 52.71% (pooled 55.75%); both 50.60%. Material input assets used more than once: 69.08% per film (20,383/29,321 assets). The largest hub, one APEIROPHOBIA asset, has 1,602 distinct consumers.
- **Where:** Across image and video work; inputs, references and chaining. Literal models: none named.
- **Evidence:** observed. Structure of the disclosed lineage graph. What a shared source means (same shot, same character) is not observed.
- **Strength:** strong for structure; meaning undecided.
- **Study 04 status:** Study 07 raw compound input reuse or branch, and Study 08 branches, chains and convergence: undecided. Text labels cannot show that shared inputs serve the same shot or entity.
- **Example:** film c3d8ee5e-b119-4654-99f9-c6545f650635; c3d8ee5e-b119-4654-99f9-c6545f650635/asset:36b6dccd-9a13-4ecc-81ab-835e6333e15d; source `studies/07-lineage/outputs/hubs.csv`; excerpt: distinct consumers=1602; total asset input nodes=669
- **Denominator:** 130,704 primary jobs in 157 films; 29,321 material input assets in 156 films.
- **Competing explanation:** Omitted external or private work and unresolved cross-ID aliases change the topology; a shared input need not represent the same shot or entity; reuse is not approval.
- **Confidence:** Exact compound-key counts and deterministic traversal of released records; no media inspection.
- **Rests on:** [`studies/07-lineage/README.md`](../studies/07-lineage/README.md), [`studies/07-lineage/outputs/summaries.csv`](../studies/07-lineage/outputs/summaries.csv), [`studies/07-lineage/outputs/hubs.csv`](../studies/07-lineage/outputs/hubs.csv); checked numbers `p02a`, `p02b`, `p02c`, `p02d`, `p02e`, `p02f`, `p02g`, `p02h`, `p02i`, `p02j` in [`citations.csv`](outputs/citations.csv).

### P03. Work passes between models

A large share of jobs consume something a different model made, so films are assembled across several models rather than inside one. Handoffs are specific: most model pairs that appear in the same film never pass anything to each other.

- **How often:** Mean film: 36.92% of jobs take an input made by a different literal model (146 of 157 films). Resolved producer-consumer pairs crossing models: 140,008/198,201. Largest route: seedream_v5_pro to seedance_2_5, 30,119 pairs in 66 films. Co-occurring model pairs with any actual handoff: 353/1,472.
- **Where:** Between image generation, video generation and finishing. Literal models: `seedream_v5_pro`, `seedance_2_5`.
- **Evidence:** observed. Explicit producer-consumer bindings; co-occurrence alone is not a handoff.
- **Strength:** strong for the bindings; motive undecided.
- **Study 04 status:** Study 08 branches, chains, convergence and cross-model from explicit parents: undecided. Component overlap cannot prove a common shot or revision motive.
- **Example:** film d90fe8bd-3329-40b3-963c-d9b33075aec1; d90fe8bd-3329-40b3-963c-d9b33075aec1/generation:006dcc36-ec37-490f-9890-9524e3ed0ddd; d90fe8bd-3329-40b3-963c-d9b33075aec1/generation:011fbb97-732a-416b-825f-a9635b313b86; d90fe8bd-3329-40b3-963c-d9b33075aec1/asset:006dcc36-ec37-490f-9890-9524e3ed0ddd; source `studies/08-workflow/outputs/handoff_examples.csv (detour:08.3)`; excerpt: [producer model] seedream_v5_pro [consumer model] gpt_image_2 [explicit usage] asset_role input_image
- **Denominator:** 130,704 primary jobs in 157 films; 198,201 resolved producer-consumer job pairs in 147 films; 1,472 unordered co-occurring model pairs.
- **Competing explanation:** Platform features may route outputs between models automatically; repeated requests and raw asset aliases change apparent handoffs; a binding is not approval.
- **Confidence:** Deterministic released-record counts; one consumer with several parents counts in several pairs.
- **Rests on:** [`studies/08-workflow/README.md`](../studies/08-workflow/README.md), [`studies/08-workflow/outputs/summaries.csv`](../studies/08-workflow/outputs/summaries.csv), [`studies/08-workflow/outputs/summary_transitions.csv`](../studies/08-workflow/outputs/summary_transitions.csv), [`studies/08-workflow/outputs/transitions.csv`](../studies/08-workflow/outputs/transitions.csv), [`studies/08-workflow/outputs/cooccurrence.csv`](../studies/08-workflow/outputs/cooccurrence.csv); checked numbers `p03a`, `p03b`, `p03c`, `p03d`, `p03e`, `p03f`, `p03g`, `p03h`, `p03i` in [`citations.csv`](outputs/citations.csv).

### P04. Video requests are long and written out in full

Video prompts are several times longer than image prompts and usually carry an attached input, a long description, camera wording and exclusion wording together. Provisional labels find most of the fourteen instruction components in a typical video text.

- **How often:** Median of per-film median prompt length: video 5,104 characters, image 1,549. All four traits together: 77.87% of the mean film's video prompts (pooled 81.48%; present in 150 of 156 films). Provisional components per text, mean film: video 12.5 of 14, image 8.2.
- **Where:** Video generation prompts; image prompts for comparison. Literal models: `seedance_2_5`.
- **Evidence:** observed. Lengths and the four-trait bundle are structural counts; the component counts are inferred from provisional 27B labels on a weighted sample.
- **Strength:** strong for length and bundle; moderate for component counts.
- **Study 04 status:** Study 06 lexical camera, lens, preservation and exclusion proxies: changed. The structural census stays; semantic components are a sampled, provisional addition.
- **Example:** film 9b38b885-bf92-484e-8f36-a890e4e10d61; 9b38b885-bf92-484e-8f36-a890e4e10d61/generation:014a8505-858b-4b9a-9777-b4461d5957e2; 9b38b885-bf92-484e-8f36-a890e4e10d61/asset:65374a8b-bdfc-4f94-860d-9246879c82ee; source `studies/06-video/outputs/case_evidence.csv (prophecy-in-2047:06.1)`; excerpt: Six separate shots joined by five hard cuts ... tracking with her, handheld tremor ... Heavy rain falls in every frame.
- **Denominator:** 37,079 nonempty primary video prompts in 156 films; 87,238 nonempty primary image prompts in 155 films; component counts over successfully labelled sampled primary texts.
- **Competing explanation:** Templates, copied boilerplate and repeated batch text lengthen prompts without adding intent; the model or interface may reward long prompts; length is not quality.
- **Confidence:** The census reproduces Study 04's per-film counts exactly; component counts carry the provisional label agreement in L07.
- **Rests on:** [`studies/04-prompts/README.md`](../studies/04-prompts/README.md), [`synthesis/outputs/summaries.csv`](outputs/summaries.csv), [`synthesis/outputs/technique_by_film.csv`](outputs/technique_by_film.csv), [`synthesis/outputs/semantic_breadth.csv`](outputs/semantic_breadth.csv); checked numbers `p04a`, `p04b`, `p04c`, `p04d`, `p04e`, `p04f`, `p04g`, `p04h`, `p04i` in [`citations.csv`](outputs/citations.csv).

### P05. Stills are made as foundations for video

Some image jobs exist to be handed to video: their output is taken as an input by a video job. Separately, some jobs make images that are later attached as named references.

- **How often:** Image jobs whose output a video job takes: 14.91% of the mean film's image jobs (pooled 8.77%; 8,076/92,058 jobs; 143 of 155 films). Jobs whose output becomes a named reference: 3,930 jobs in 100 of 157 films.
- **Where:** Image generation feeding video generation; reference preparation. Literal models: `nano_banana_2`, `seedream_v5_pro`, `gpt_image_2`.
- **Evidence:** observed. Recorded bindings from image outputs into video jobs.
- **Strength:** strong.
- **Study 04 status:** Study 08 reference preparation and foundation distinct from verified sheet or keyframe: confirmed. A foundation is a recorded binding, not a verified keyframe.
- **Example:** film 6659c520-c88e-4ac7-a2c9-f28d8a40c954; 6659c520-c88e-4ac7-a2c9-f28d8a40c954/generation:1cba062c-b6c5-456d-929d-b958859ae105; 6659c520-c88e-4ac7-a2c9-f28d8a40c954/generation:023fadcd-4fdd-46b9-98f4-1b940839b4c7; 6659c520-c88e-4ac7-a2c9-f28d8a40c954/asset:1cba062c-b6c5-456d-929d-b958859ae105; source `studies/08-workflow/outputs/handoff_examples.csv (fallen-leaves:08.3)`; excerpt: [producer model] gpt_image_2 [consumer model] seedance_2_5 [explicit usage] asset_role reference_image
- **Denominator:** 92,058 primary image jobs in 155 image-bearing films; 130,704 jobs in 157 films for reference preparation.
- **Competing explanation:** A video job may take an image as a loose reference rather than a frame; images used in video outside the platform are not recorded.
- **Confidence:** Deterministic binding counts; the role of the image inside the video is not inspected.
- **Rests on:** [`studies/05-image/README.md`](../studies/05-image/README.md), [`studies/05-image/outputs/summaries.csv`](../studies/05-image/outputs/summaries.csv), [`studies/08-workflow/outputs/summaries.csv`](../studies/08-workflow/outputs/summaries.csv); checked numbers `p05a`, `p05b`, `p05c`, `p05d`, `p05e`, `p05f`, `p05g`, `p05h` in [`citations.csv`](outputs/citations.csv).

### P06. Few outputs are taken further, and video outputs least

Only a minority of jobs have an output that any later job uses, and image outputs are taken further several times as often as video outputs.

- **How often:** Jobs whose output a later job uses: 14.74% of the mean film's jobs (pooled 12.07%; 15,781/130,704). Image 22.39% versus video 5.53% per film.
- **Where:** All generation; recorded further use. Literal models: none named.
- **Evidence:** observed. Further use is a recorded binding, not approval or selection.
- **Strength:** strong for the count; meaning limited.
- **Study 04 status:** Study 09 adoption is a recorded use measure; Study 04 leaves rerun-candidate motives undecided.
- **Example:** film 655325cc-46d9-4b0b-b03d-d177defa4b3f; 655325cc-46d9-4b0b-b03d-d177defa4b3f/generation:6672ee33-d850-4db4-b78f-667905814400; 655325cc-46d9-4b0b-b03d-d177defa4b3f/generation:19f73675-b69e-4314-b3a1-f74802df1da2; 655325cc-46d9-4b0b-b03d-d177defa4b3f/asset:6672ee33-d850-4db4-b78f-667905814400; source `studies/09-iteration/outputs/case_evidence.csv (The Kiss 09.3)`; excerpt: [consumer text] Move the entire title "The Kiss" UP
- **Denominator:** 130,704 primary jobs in 157 films; 92,058 image and 38,508 video jobs.
- **Competing explanation:** Video may be assembled outside the platform, so unused video outputs may still be in the film; final edits and sound can happen elsewhere; batches inflate denominators; unpublished work is missing.
- **Confidence:** Deterministic counts over released bindings; no link from jobs to the final cut exists.
- **Rests on:** [`studies/09-iteration/README.md`](../studies/09-iteration/README.md), [`studies/09-iteration/outputs/summaries.csv`](../studies/09-iteration/outputs/summaries.csv), [`studies/09-iteration/outputs/summary_generation_type.csv`](../studies/09-iteration/outputs/summary_generation_type.csv); checked numbers `p06a`, `p06b`, `p06c`, `p06d`, `p06e` in [`citations.csv`](outputs/citations.csv).

### P07. Batches repeat one request exactly

Jobs launched together as a batch are the same request run several times: same text, same inputs, same model, and almost always the same controls. Variation comes from sampling, not from rewording.

- **How often:** Comparable batch pairs with identical text: 32,448/32,448. Pairs with changed inputs: 0; with changed controls: 18/32,980. Batch members: 25.07% of the mean film's jobs (pooled 38.66%). Exact repeat excess, the nonempty primary prompts beyond the first copy of each exact string: 38.45% per film.
- **Where:** Image and video generation; candidate sampling. Literal models: `soul_cinematic`, `seedream_v5_pro`.
- **Evidence:** observed. Exact text, input, model and control comparisons within recorded batches.
- **Strength:** strong.
- **Study 04 status:** Study 10 exact-string repeat excess: changed. A semantic duplicate or waste rate remains unavailable. Study 09 rerun-candidate motives: undecided.
- **Example:** film 2fd725ab-2604-4220-8cca-d332e9de53a2; 2fd725ab-2604-4220-8cca-d332e9de53a2/generation:02650faf-bbfe-4b48-9b3c-3fade6421cd5; 2fd725ab-2604-4220-8cca-d332e9de53a2/generation:b1c1f22c-6350-408b-9501-d972afb3909e; source `studies/09-iteration/outputs/comparison_examples.json (basis batch)`; excerpt: "controls_changed":0, "inputs_changed":0, "model_changed":0, "text_equal":1
- **Denominator:** 32,980 batch pairs in 111 films; 130,704 jobs and 124,449 nonempty primary prompts in 157 films.
- **Competing explanation:** The interface may create batches by default; a repeat may be a deliberate seed search, a retry after failure, or an accident; motives are not recorded.
- **Confidence:** Deterministic pair comparisons of released fields; hidden seeds and defaults are unknown.
- **Rests on:** [`studies/09-iteration/README.md`](../studies/09-iteration/README.md), [`studies/09-iteration/outputs/summary_comparisons.csv`](../studies/09-iteration/outputs/summary_comparisons.csv), [`studies/09-iteration/outputs/summaries.csv`](../studies/09-iteration/outputs/summaries.csv), [`studies/10-organisation/outputs/summaries.csv`](../studies/10-organisation/outputs/summaries.csv); checked numbers `p07a`, `p07b`, `p07c`, `p07d`, `p07e`, `p07f`, `p07g`, `p07h`, `p07i`, `p07j` in [`citations.csv`](outputs/citations.csv).

### P08. Saying what must stay the same is far more common than keywords show

Keyword counts of preservation wording miss most of it: provisional semantic labels find a request to keep something unchanged in about twice as many prompts. The gap is largest in video prompts.

- **How often:** Mean film: lexical preservation wording 31.78% of primary prompts; provisional semantic preservation 63.13%. Video: semantic 82.69% versus lexical 36.95%. Image: semantic 47.21% versus lexical 28.70%.
- **Where:** Image edits and video generation prompts. Literal models: none named.
- **Evidence:** inferred. Semantic shares come from provisional 27B labels on a weighted sample; lexical shares are observed counts.
- **Strength:** moderate: preservation agreement with the single-coder gold is high, but the sample excludes long texts.
- **Study 04 status:** Preservation and reference regex meanings in Studies 03, 05, 06, 07, 08 and 09: changed. Lexical counts stay; 27B preservation is an additional sampled measure with agreement and missingness bounds.
- **Example:** film d90fe8bd-3329-40b3-963c-d9b33075aec1; d90fe8bd-3329-40b3-963c-d9b33075aec1/generation:011fbb97-732a-416b-825f-a9635b313b86; d90fe8bd-3329-40b3-963c-d9b33075aec1/asset:006dcc36-ec37-490f-9890-9524e3ed0ddd; source `studies/03-elements/outputs/case_evidence.csv (Detour 03.2)`; excerpt: The only change is a small mark of tomato ketchup on one side of his face ... EVERYTHING ELSE STAYS UNTOUCHED
- **Denominator:** 124,449 nonempty primary prompts in 157 films (lexical); weighted successful sample with covered stratum mass 55,609 (semantic).
- **Competing explanation:** The labeller may read boilerplate continuity lines as preservation; the keyword list is English and narrow; long texts excluded from labelling may differ.
- **Confidence:** Study 04 weighting reproduced exactly here; semantic values carry failure bounds in Study 04's tables.
- **Rests on:** [`studies/04-prompts/README.md`](../studies/04-prompts/README.md), [`studies/04-prompts/outputs/semantic_summary.csv`](../studies/04-prompts/outputs/semantic_summary.csv), [`studies/04-prompts/outputs/semantic_summary_generation_type.csv`](../studies/04-prompts/outputs/semantic_summary_generation_type.csv), [`studies/07-lineage/outputs/summaries.csv`](../studies/07-lineage/outputs/summaries.csv), [`synthesis/outputs/summaries.csv`](outputs/summaries.csv); checked numbers `p08a`, `p08b`, `p08c`, `p08d`, `p08e`, `p08f`, `p08g` in [`citations.csv`](outputs/citations.csv).

### P09. Several shots are asked for in words, not with the shot control

When a video prompt describes several shots, the multi-shot control is almost always off; the shots are written into the prompt instead. The control itself is used in only a handful of films.

- **How often:** Video jobs with multi-shot wording and the control off: 8,981/9,060 (99.05% per film, 122 films). Control on: 170 jobs in 9 films.
- **Where:** Video generation; shot structure. Literal models: `seedance_2_5`.
- **Evidence:** observed. Literal control values beside lexical shot wording.
- **Strength:** strong for the control state; shot intent of the wording is lexical.
- **Study 04 status:** Study 06 requested shots distinct from jobs and cuts: confirmed. Multi-shot lexical proxy: changed; no semantic label matches shot intent.
- **Example:** film c3d8ee5e-b119-4654-99f9-c6545f650635; c3d8ee5e-b119-4654-99f9-c6545f650635/generation:230fc3df-a3e7-4645-8116-561d321a70c5; c3d8ee5e-b119-4654-99f9-c6545f650635/asset:1ffe82b6-9d5e-41c0-a4e9-2e219a07a75e; source `studies/06-video/outputs/case_evidence.csv (apeirophobia:06.1)`; excerpt: EXACTLY TWO SHOTS ONLY — ONE SINGLE CUT. [literal controls] "multi_shots": false
- **Denominator:** 9,060 video jobs with multi-shot wording in 122 films; 38,508 video jobs in 156 films.
- **Competing explanation:** The control may be unavailable for some models or versions, or defaults may hide its state; wording can describe one shot's internal moves.
- **Confidence:** Literal control states and deterministic lexical matches; executed shots are not counted.
- **Rests on:** [`studies/06-video/README.md`](../studies/06-video/README.md), [`studies/06-video/outputs/summaries.csv`](../studies/06-video/outputs/summaries.csv); checked numbers `p09a`, `p09b`, `p09c`, `p09d`, `p09e`, `p09f` in [`citations.csv`](outputs/citations.csv).

### P10. Sound is asked of the video model; separate audio and finishing jobs are rare

Video jobs nearly always have sound generation switched on, while dedicated audio and voice jobs are rare. About half the films show finishing jobs such as editing or upscaling on the platform.

- **How often:** generate_audio on: 91.55% of the mean film's video jobs (35,905/38,508). Audio jobs: 132 in 10 films. Voice adapters: 61 jobs in 14 films. Finishing jobs: 1,358 in 80 of 157 films.
- **Where:** Video generation controls; audio, voice and finishing. Literal models: `seedance_2_5`, `cinematic_video_editor`, `voice_change_merge`.
- **Evidence:** observed. Literal control values and job roles.
- **Strength:** strong for what is recorded; external sound and editing are invisible.
- **Study 04 status:** Study 06 subject, camera, environment, events, audio and invariants in named spans: confirmed, without a dedicated audio label. Study 08 adapter mapping: undecided.
- **Example:** film d51d6821-d191-40f7-949b-1086750a2e93; d51d6821-d191-40f7-949b-1086750a2e93/generation:0014cfd5-e8f9-4b5a-8ab3-f2f5b93d2452; d51d6821-d191-40f7-949b-1086750a2e93/asset:45285c82-bc05-4548-87a4-b7e865f697ae; source `studies/06-video/outputs/case_evidence.csv (Birthdays 06.1)`; excerpt: Audio: Environmental SFX only. No music. No subtitles. [literal controls] "generate_audio": true
- **Denominator:** 38,508 video jobs in 156 films; 130,704 jobs in 157 films.
- **Competing explanation:** generate_audio may default to on; creators may discard generated sound and score externally; finishing done off-platform is not recorded.
- **Confidence:** Literal control states and deterministic role counts; sound is not heard.
- **Rests on:** [`studies/06-video/outputs/summaries.csv`](../studies/06-video/outputs/summaries.csv), [`studies/08-workflow/README.md`](../studies/08-workflow/README.md), [`studies/08-workflow/outputs/summaries.csv`](../studies/08-workflow/outputs/summaries.csv); checked numbers `p10a`, `p10b`, `p10c`, `p10d`, `p10e`, `p10f`, `p10g`, `p10h` in [`citations.csv`](outputs/citations.csv).

### P11. Saved elements are reused

Most films use saved reference elements, and most elements, once used, are used again.

- **How often:** Films using saved elements: 120 of 157. Used elements reused: 85.90% per film (pooled 88.02%; 4,577/5,200).
- **Where:** Reference elements attached to image and video jobs. Literal models: none named.
- **Evidence:** observed. Recorded element attachments.
- **Strength:** strong for reuse counts; element identity undecided.
- **Study 04 status:** Study 03 disclosed record as element and semantic kind: undecided. Component presence cannot establish persistent identity or complete libraries.
- **Example:** film all element-using primary films; per-film reference:* counts; source `studies/03-elements/outputs/film_metrics.csv`; excerpt: per-film used_elements and reused_elements
- **Denominator:** 5,200 used elements in 120 films.
- **Competing explanation:** Elements may be auto-attached by templates; the same character may live in several elements; libraries outside the workspace are not visible.
- **Confidence:** Deterministic counts of released attachments.
- **Rests on:** [`studies/03-elements/README.md`](../studies/03-elements/README.md), [`studies/03-elements/outputs/summaries.csv`](../studies/03-elements/outputs/summaries.csv); checked numbers `p11a`, `p11b`, `p11c`, `p11d`, `p11e` in [`citations.csv`](outputs/citations.csv).

### P12. Folders do not follow what feeds what

Nearly half of the recorded input bindings link jobs that sit in different, non-overlapping workspace folders, so folders are not a reliable map of a film's lineage.

- **How often:** Resolved input bindings across disjoint folders: 46.69% per film (pooled 54.19%; 147 films measured).
- **Where:** Workspace organisation. Literal models: none named.
- **Evidence:** observed. Folder placement compared across recorded bindings.
- **Strength:** moderate: folder meaning is creator-specific.
- **Study 04 status:** No Study 04 dependency.
- **Example:** film all primary films with resolved bindings; per-film generation:* folder placements; source `studies/10-organisation/outputs/film_metrics.csv`; excerpt: per-film disjoint-folder binding counts
- **Denominator:** 198,201 resolved bindings in 147 films.
- **Competing explanation:** Folders may group by scene, date or deliverable rather than lineage; moves after generation are not recorded.
- **Confidence:** Deterministic counts of released placements.
- **Rests on:** [`studies/10-organisation/README.md`](../studies/10-organisation/README.md), [`studies/10-organisation/outputs/summaries.csv`](../studies/10-organisation/outputs/summaries.csv); checked numbers `p12a`, `p12b`, `p12c`, `p12d` in [`citations.csv`](outputs/citations.csv).

## Model preferences

"Preference" here means recorded use of a literal model identifier. Why creators
chose a model is not recorded (L06).

### M01. One video model carries most video work: seedance_2_5

seedance_2_5 is the main video model in most films and usually makes nearly all of a film's video. It made every declared extension and most image-to-video jobs.

- **How often:** Top video model in 125 of 156 video-bearing films. Share of a film's video jobs: median 94.33%, mean 75.75%, pooled 80.72%; at least 90% in 90 films. Extensions: 2,260 jobs, all seedance_2_5 (100.00%). Image-to-video: 77.41% of the mean film's image-to-video jobs.
- **Where:** Video generation, extension and video-to-video. Literal models: `seedance_2_5`, `cinematic_studio_video_4_0`.
- **Evidence:** observed. Literal model identifiers on recorded jobs. A preference is not observed.
- **Strength:** strong for the share; the reason is unknown (see L06).
- **Study 04 status:** No Study 04 dependency for literal model counts.
- **Example:** film all video-bearing primary films; per-film generation:* model counts; source `synthesis/outputs/model_concentration.csv`; excerpt: per-film video jobs, models, top_model and seedance_2_5_jobs
- **Denominator:** 38,508 video jobs in 156 films.
- **Competing explanation:** Availability, defaults, price, release timing and contest rules can concentrate use without any judgement of quality.
- **Confidence:** Deterministic counts over Study 08's model inventory.
- **Rests on:** [`synthesis/outputs/summaries.csv`](outputs/summaries.csv), [`synthesis/outputs/model_concentration.csv`](outputs/model_concentration.csv), [`synthesis/outputs/model_stages.csv`](outputs/model_stages.csv), [`studies/08-workflow/outputs/model_inventory.csv`](../studies/08-workflow/outputs/model_inventory.csv); checked numbers `m01a`, `m01b`, `m01c`, `m01d`, `m01e`, `m01f`, `m01g`, `m01h` in [`citations.csv`](outputs/citations.csv).

### M02. Image work is spread over several models, led by three

Films use several image models, and no single one dominates image work the way seedance_2_5 dominates video. For image jobs with an input, three models lead: nano_banana_2, seedream_v5_pro and gpt_image_2.

- **How often:** Image models per film: median 5 (IQR 3-8). Top image model's share of a film's image jobs: median 60.61%. Image jobs with an input, mean film share and films where top: nano_banana_2 33.28% (49), seedream_v5_pro 22.24% (44), gpt_image_2 20.96% (30).
- **Where:** Image generation and editing. Literal models: `nano_banana_2`, `seedream_v5_pro`, `gpt_image_2`.
- **Evidence:** observed. Literal model identifiers on recorded image jobs.
- **Strength:** strong.
- **Study 04 status:** No Study 04 dependency for literal model counts.
- **Example:** film all image-bearing primary films; per-film generation:* model counts; source `synthesis/outputs/model_concentration.csv`; excerpt: per-film image jobs, models and top_model
- **Denominator:** 92,058 image jobs in 155 films; 57,717 image jobs with an input in 153 films.
- **Competing explanation:** Model releases during the contest window, price and interface defaults shape the mix; films may switch models for reasons unrelated to the task.
- **Confidence:** Deterministic counts over Study 08's role matrix.
- **Rests on:** [`synthesis/outputs/summaries.csv`](outputs/summaries.csv), [`synthesis/outputs/model_stages.csv`](outputs/model_stages.csv), [`studies/08-workflow/outputs/role_matrix.csv`](../studies/08-workflow/outputs/role_matrix.csv); checked numbers `m02a`, `m02b`, `m02c`, `m02d`, `m02e`, `m02f`, `m02g`, `m02h`, `m02i`, `m02j`, `m02k`, `m02l` in [`citations.csv`](outputs/citations.csv).

### M03. Two roles for image models: start from nothing, or work from what you give

Two soul models, soul_cinematic and text2image_soul_v2, are almost always run without a recorded input and in batches, while nano_banana_2, seedream_v5_pro and gpt_image_2 usually receive an attached image and often combine several.

- **How often:** Per film using each model, no recorded input: soul_cinematic 88.87%, text2image_soul_v2 88.33%; batch members: 69.84% and 62.76%. Attached input: nano_banana_2 77.01%, seedream_v5_pro 75.51%, gpt_image_2 75.87%; two or more inputs: 34.15%, 35.88%, 34.58%.
- **Where:** Image generation: first looks versus edits and composites. Literal models: `soul_cinematic`, `text2image_soul_v2`, `nano_banana_2`, `seedream_v5_pro`, `gpt_image_2`.
- **Evidence:** observed. Recorded input bindings and batch membership per literal model.
- **Strength:** strong.
- **Study 04 status:** Study 08 conservative input route: confirmed. No recorded input never establishes text-only production.
- **Example:** film all primary films using each model; per-film, per-model generation:* counts; source `synthesis/outputs/model_profiles.csv`; excerpt: metric, model_identifier, films_using_model, equal_film_mean
- **Denominator:** Jobs of each model in films using it: soul_cinematic 7,696 in 65 films; text2image_soul_v2 5,809 in 56; nano_banana_2 25,355 in 138; seedream_v5_pro 21,136 in 96; gpt_image_2 14,397 in 120.
- **Competing explanation:** Interfaces differ: a model may not accept inputs, or may batch by default; the role is an affordance as much as a choice.
- **Confidence:** Deterministic counts per literal model; model versions and hidden defaults are not resolved.
- **Rests on:** [`synthesis/outputs/model_profiles.csv`](outputs/model_profiles.csv), [`studies/08-workflow/outputs/role_matrix.csv`](../studies/08-workflow/outputs/role_matrix.csv), [`studies/09-iteration/outputs/by_model_identifier.csv`](../studies/09-iteration/outputs/by_model_identifier.csv); checked numbers `m03a`, `m03b`, `m03c`, `m03d`, `m03e`, `m03f`, `m03g`, `m03h`, `m03i`, `m03j`, `m03k`, `m03l`, `m03m`, `m03n`, `m03o`, `m03p`, `m03q`, `m03r`, `m03s`, `m03t` in [`citations.csv`](outputs/citations.csv).

### M04. Video foundations come from the three input-taking image models

When an image is handed to video generation, seedance_2_5 almost always receives it, and the image was usually made by nano_banana_2, gpt_image_2 or seedream_v5_pro. The text-first soul_cinematic rarely makes foundations.

- **How often:** Image-to-video handoffs (111,297 pairs, 143 films), mean film share: consumer seedance_2_5 79.30%; producers nano_banana_2 27.41%, gpt_image_2 24.73%, seedream_v5_pro 21.64% (pooled 29.40%). soul_cinematic's share of image foundations: 3.53% per film.
- **Where:** Image-to-video handoff. Literal models: `seedance_2_5`, `nano_banana_2`, `gpt_image_2`, `seedream_v5_pro`, `soul_cinematic`.
- **Evidence:** observed. Explicit producer-consumer bindings by literal model.
- **Strength:** strong.
- **Study 04 status:** Study 08 foundation distinct from verified keyframe: confirmed.
- **Example:** film 655325cc-46d9-4b0b-b03d-d177defa4b3f; 655325cc-46d9-4b0b-b03d-d177defa4b3f/generation:0035469c-1e6e-4c3f-aad6-bb3ab0bb05ce; 655325cc-46d9-4b0b-b03d-d177defa4b3f/generation:122382c3-e873-4845-8a14-89ff9dfa215e; source `studies/08-workflow/outputs/handoff_examples.csv (the-kiss:08.3)`; excerpt: [producer model] nano_banana_2 [consumer model] seedance_2_5
- **Denominator:** 111,297 image-to-video producer-consumer pairs in 143 films; 8,076 foundation image jobs in 143 films.
- **Competing explanation:** Producers reflect which models a film used for images at all; a foundation may be one of many candidate images.
- **Confidence:** Deterministic counts of Study 08's transitions by model type.
- **Rests on:** [`synthesis/outputs/model_handoffs.csv`](outputs/model_handoffs.csv), [`synthesis/outputs/model_stages.csv`](outputs/model_stages.csv), [`studies/08-workflow/outputs/transitions.csv`](../studies/08-workflow/outputs/transitions.csv); checked numbers `m04a`, `m04b`, `m04c`, `m04d`, `m04e`, `m04f`, `m04g`, `m04h` in [`citations.csv`](outputs/citations.csv).

### M05. On-platform finishing runs through cinematic_video_editor

Where finishing jobs exist, cinematic_video_editor is the usual tool, mostly fed by seedance_2_5 clips; topaz_video appears in fewer films but handles large volumes where used.

- **How often:** Of 80 films with finishing jobs, cinematic_video_editor is used in 73 and is the top finishing model in 66 (80.09% mean film share). topaz_video: 17 films, 31.15% of pooled finishing jobs. seedance_2_5 produces 60.96% of the mean film's into-finishing pairs.
- **Where:** Finishing: editing and upscaling. Literal models: `cinematic_video_editor`, `topaz_video`, `seedance_2_5`.
- **Evidence:** observed. Literal model identifiers on finishing jobs and their recorded inputs.
- **Strength:** moderate: about half the films show no on-platform finishing.
- **Study 04 status:** Study 08 closed adapter role mapping: undecided. What the editor does is not validated.
- **Example:** film c3d8ee5e-b119-4654-99f9-c6545f650635; c3d8ee5e-b119-4654-99f9-c6545f650635/generation:88160a68-3dd4-4662-be7e-4fb5852634c5; c3d8ee5e-b119-4654-99f9-c6545f650635/generation:b6e44e77-d4a0-4821-9663-55a452fffc01; source `studies/08-workflow/outputs/handoff_examples.csv (apeirophobia:08.3)`; excerpt: [producer model] seedance_2_5 [consumer model] cinematic_video_editor [explicit usage] asset_role input_video
- **Denominator:** 1,358 finishing jobs in 80 films; 1,367 into-finishing pairs in 77 films.
- **Competing explanation:** Most editing is said to happen in external editors, so on-platform finishing is a partial view.
- **Confidence:** Deterministic counts; finishing content is not inspected.
- **Rests on:** [`synthesis/outputs/model_stages.csv`](outputs/model_stages.csv), [`synthesis/outputs/model_handoffs.csv`](outputs/model_handoffs.csv), [`studies/08-workflow/outputs/handoff_examples.csv`](../studies/08-workflow/outputs/handoff_examples.csv); checked numbers `m05a`, `m05b`, `m05c`, `m05d`, `m05e`, `m05f`, `m05g`, `m05h`, `m05i` in [`citations.csv`](outputs/citations.csv).

### M06. Recorded seedance_2_5 settings: 720p or 1080p, wide frames, varied lengths

seedance_2_5 jobs are mostly set to 720p or 1080p and to 16:9, with a large minority at 21:9. Clip lengths vary widely, with peaks at 20, 30 and 15 seconds.

- **How often:** Mean film share among 145 films using seedance_2_5: 720p 48.44%, 1080p 40.59%, 480p 10.96%; 16:9 62.94%, 21:9 35.55% (65 films use 21:9). Duration 20 s 16.46%, 30 s 13.87%, 15 s 10.36%.
- **Where:** Video generation controls. Literal models: `seedance_2_5`.
- **Evidence:** observed. Literal top-level control values.
- **Strength:** strong for recorded values; defaults unknown.
- **Study 04 status:** Study 09 top-level scalar control subset: confirmed. Hidden defaults and nested semantics remain unknown.
- **Example:** film all primary films using seedance_2_5; per-film generation:* control values; source `studies/06-video/outputs/controls_resolution.csv`; excerpt: per-film seedance_2_5 resolution, aspect_ratio and duration states
- **Denominator:** 31,080 seedance_2_5 jobs with valid control documents in 145 films.
- **Competing explanation:** Defaults, credit cost per second and resolution, and contest delivery specs shape settings.
- **Confidence:** Literal recorded values; jobs without a control value are kept separate in Study 06.
- **Rests on:** [`studies/06-video/outputs/summary_controls_resolution.csv`](../studies/06-video/outputs/summary_controls_resolution.csv), [`studies/06-video/outputs/summary_controls_aspect_ratio.csv`](../studies/06-video/outputs/summary_controls_aspect_ratio.csv), [`studies/06-video/outputs/summary_controls_duration.csv`](../studies/06-video/outputs/summary_controls_duration.csv); checked numbers `m06a`, `m06b`, `m06c`, `m06d`, `m06e`, `m06f`, `m06g`, `m06h`, `m06i`, `m06j`, `m06k` in [`citations.csv`](outputs/citations.csv).

### M07. Outputs of the input-taking image models are taken further most often

Outputs of gpt_image_2, seedream_v5_pro and nano_banana_2 are reused by later jobs more often than those of soul_cinematic or seedance_2_5.

- **How often:** Jobs whose output a later job uses, mean film share among films using the model: gpt_image_2 24.94%, seedream_v5_pro 22.57%, nano_banana_2 18.72%, soul_cinematic 10.02%, seedance_2_5 5.85%.
- **Where:** Recorded further use by model. Literal models: `gpt_image_2`, `seedream_v5_pro`, `nano_banana_2`, `soul_cinematic`, `seedance_2_5`.
- **Evidence:** observed. Recorded further use per literal model; not approval.
- **Strength:** moderate: batches and external assembly shift denominators.
- **Study 04 status:** Study 09 rerun-candidate motives: undecided.
- **Example:** film primary films using each model; per-film, per-model generation:* adoption counts; source `studies/09-iteration/outputs/by_model_identifier.csv`; excerpt: adopted and jobs by film and model_identifier
- **Denominator:** Jobs of each model in films using it: gpt_image_2 14,397 in 120 films; seedream_v5_pro 21,136 in 96; nano_banana_2 25,355 in 138; soul_cinematic 7,696 in 65; seedance_2_5 31,082 in 145.
- **Competing explanation:** Video outputs are assembled outside the platform; soul_cinematic runs in large batches, so most candidates are siblings; use is not quality.
- **Confidence:** Deterministic counts from Study 09.
- **Rests on:** [`studies/09-iteration/outputs/summary_model_identifier.csv`](../studies/09-iteration/outputs/summary_model_identifier.csv), [`synthesis/outputs/model_profiles.csv`](outputs/model_profiles.csv); checked numbers `m07a`, `m07b`, `m07c`, `m07d`, `m07e`, `m07f`, `m07g` in [`citations.csv`](outputs/citations.csv).

## Techniques and tips

These are techniques visible in the records: instructions and bindings that creators
used. None has been tested for benefit (L02). Read them as practices to try, not as
proven best practice.

### T01. Name the change, then name what must stay

Edit requests usually say both what to change and what to leave alone, often with a hard boundary such as "ONLY" and "stays exactly unchanged". What is protected is often identity.

- **How often:** Image edit prompts with preservation wording: 56.71% of the mean film's edit prompts versus 30.46% of all its image prompts (146 films; pooled 62.69% versus 31.04%). Provisional: image texts asking to preserve mention identity 74.67% of the time versus 58.85% overall.
- **Where:** Image edits and video edits. Literal models: `nano_banana_2`, `gpt_image_2`, `seedream_v5_pro`.
- **Evidence:** associated. Co-occurrence of edit and preservation wording within prompts; the case shows the wording; the identity pair uses provisional labels.
- **Strength:** strong for the co-occurrence; benefit untested.
- **Study 04 status:** Study 05 edit, preservation and short-edit proxies: changed. Semantic preservation is conditional on the weighted sample; edit intent is not a released component.
- **Example:** film 03f596b0-23da-4312-9e58-2e1cc4582348; 03f596b0-23da-4312-9e58-2e1cc4582348/generation:083272c6-2303-4ddd-87e3-27dd2531ee0e; 03f596b0-23da-4312-9e58-2e1cc4582348/asset:6640605c-455d-42cd-ab70-db0c327d7b20; source `studies/06-video/outputs/case_evidence.csv (THE LAST TRANSMISSION 06.5)`; excerpt: Edit: inside the CRT screen ONLY ... EVERYTHING outside the screen glass stays exactly unchanged
- **Denominator:** 23,074 image edit prompts in 146 films against 87,238 nonempty image prompts in 155 films; sampled successful image texts for the identity pair.
- **Competing explanation:** Templates may bundle edit and keep phrases; the keyword lists overlap in wording; whether naming invariants helps is untested.
- **Confidence:** Census-level co-occurrence reproduced from released features; provisional labels for the identity pair.
- **Rests on:** [`synthesis/outputs/technique_pairs.csv`](outputs/technique_pairs.csv), [`synthesis/outputs/semantic_pairs.csv`](outputs/semantic_pairs.csv), [`studies/06-video/outputs/revision_requests.json`](../studies/06-video/outputs/revision_requests.json), [`studies/05-image/README.md`](../studies/05-image/README.md); checked numbers `t01a`, `t01b`, `t01c`, `t01d`, `t01e`, `t01f`, `t01g`, `t01h` in [`citations.csv`](outputs/citations.csv).

### T02. Prepare a reference package, then attach it

Creators make dedicated reference images, typically several views of the same character or costume, and later attach them to image and video jobs. A prepared sheet can itself be edited for a variant.

- **How often:** Panel films preparing multi-angle references: 10 of 16, plus 1 that also prepared a location board. Jobs whose output becomes a named reference: 3,930 in 100 of 157 films. Jobs with a named reference attached: 32.67% of the mean film's jobs.
- **Where:** Reference preparation before image and video generation. Literal models: `gpt_image_2_5`, `seedream_v5_pro`, `gpt_image_2`.
- **Evidence:** observed. Panel prompts requesting sheets and recorded attachments; the sheet's form is not verified.
- **Strength:** moderate: purposive panel of 16; population counts are bindings only.
- **Study 04 status:** Study 03 package request or attachment distinct from fulfilment: confirmed. No sheet form is verified.
- **Example:** film aed4098b-3278-4e5d-a347-24fad9cfb9ae; aed4098b-3278-4e5d-a347-24fad9cfb9ae/generation:16536627-0f5a-4ac8-bdb8-b9d43902785a; aed4098b-3278-4e5d-a347-24fad9cfb9ae/asset:aec46fad-8f17-4e5f-94ab-166299a81706; source `studies/03-elements/outputs/case_evidence.csv (SNAP 03.3)`; excerpt: Character reference sheet of the SAME person ... One FRONT view ... one BACK view
- **Denominator:** 16 panel films; 130,704 jobs in 157 films.
- **Competing explanation:** Sheets may be made for pitching or style exploration rather than consistency; whether a sheet beats a text description is untested.
- **Confidence:** Single-coder panel coding with scoped excerpts; deterministic population counts.
- **Rests on:** [`studies/03-elements/README.md`](../studies/03-elements/README.md), [`studies/03-elements/outputs/panel_assignments.csv`](../studies/03-elements/outputs/panel_assignments.csv), [`studies/03-elements/outputs/reference_packages.json`](../studies/03-elements/outputs/reference_packages.json), [`studies/08-workflow/outputs/summaries.csv`](../studies/08-workflow/outputs/summaries.csv); checked numbers `t02a`, `t02b`, `t02c`, `t02d`, `t02e`, `t02f` in [`citations.csv`](outputs/citations.csv).

### T03. Write cuts and timing into the prompt

Video prompts lay out shots and timings in words, with counted cuts and timestamps, even when the multi-shot control is off (see P09).

- **How often:** Provisional timing component in 89.41% of the mean film's video texts. Lexical multi-shot wording in 25.01% of the mean film's video prompts (pooled 24.43%).
- **Where:** Video generation; shot structure. Literal models: `seedance_2_5`.
- **Evidence:** observed. Case wording is observed; the timing share is inferred from provisional labels.
- **Strength:** moderate: instruction only; executed cuts are not counted.
- **Study 04 status:** Study 06 requested shots distinct from jobs and cuts: confirmed. Study 06 possible conflicts between timing text and controls: confirmed, unadjudicated.
- **Example:** film 9b38b885-bf92-484e-8f36-a890e4e10d61; 9b38b885-bf92-484e-8f36-a890e4e10d61/generation:014a8505-858b-4b9a-9777-b4461d5957e2; source `studies/06-video/outputs/case_evidence.csv (prophecy-in-2047:06.1)`; excerpt: Six separate shots joined by five hard cuts ... 4.0s HARD CUT
- **Denominator:** Sampled successful video texts in 156 films (timing); 37,079 nonempty video prompts in 156 films (lexical).
- **Competing explanation:** The model may ignore timings; writers may copy timing templates; timing text and the duration control may disagree.
- **Confidence:** Provisional label agreement for timing is reported in Study 04; lexical counts are deterministic.
- **Rests on:** [`studies/06-video/README.md`](../studies/06-video/README.md), [`studies/06-video/outputs/motion_patterns.csv`](../studies/06-video/outputs/motion_patterns.csv), [`studies/04-prompts/outputs/semantic_summary_generation_type.csv`](../studies/04-prompts/outputs/semantic_summary_generation_type.csv), [`synthesis/outputs/summaries.csv`](outputs/summaries.csv); checked numbers `t03a`, `t03b`, `t03c` in [`citations.csv`](outputs/citations.csv).

### T04. Give the camera, the subject and the world their own sentences

Detailed video prompts describe what the camera does, what the subject does and what the environment does in separate statements, rather than one blended description.

- **How often:** Provisional components in the mean film's video texts: camera motion 90.53%, action 96.54%. Lexical camera wording: 86.28% of the mean film's video prompts (pooled 87.47%).
- **Where:** Video generation; motion description. Literal models: `seedance_2_5`.
- **Evidence:** observed. Case wording is observed; component shares are inferred from provisional labels.
- **Strength:** moderate: separation is shown in cases; shares only show presence.
- **Study 04 status:** Study 06 subject, camera, environment, events, audio and invariants in named spans: confirmed, without a dedicated environment-motion label.
- **Example:** film 9b38b885-bf92-484e-8f36-a890e4e10d61; 9b38b885-bf92-484e-8f36-a890e4e10d61/generation:014a8505-858b-4b9a-9777-b4461d5957e2; source `studies/06-video/outputs/case_evidence.csv (prophecy-in-2047:06.1)`; excerpt: tracking with her, handheld tremor ... Roopa hauls right to left ... Heavy rain falls in every frame.
- **Denominator:** Sampled successful video texts in 156 films; 37,079 nonempty video prompts in 156 films.
- **Competing explanation:** Presence of both components does not show they were separated; separation may be a writing habit with no effect on output.
- **Confidence:** Provisional labels; lexical counts deterministic.
- **Rests on:** [`studies/06-video/README.md`](../studies/06-video/README.md), [`studies/06-video/outputs/motion_patterns.csv`](../studies/06-video/outputs/motion_patterns.csv), [`studies/04-prompts/outputs/semantic_summary_generation_type.csv`](../studies/04-prompts/outputs/semantic_summary_generation_type.csv); checked numbers `t04a`, `t04b`, `t04c`, `t04d` in [`citations.csv`](outputs/citations.csv).

### T05. Say what each reference is allowed to decide

Some creators state the scope of a reference's authority, for example that one image governs the whole shot, instead of leaving the model to weigh several inputs.

- **How often:** Panel films with a creator-declared reference authority: 9 of 16.
- **Where:** Reference-guided image and video generation. Literal models: `seedance_2_5`.
- **Evidence:** creator-stated. The creator's own instruction about a reference; whether the model obeys is not observed.
- **Strength:** weak to moderate: purposive panel only.
- **Study 04 status:** Study 03 property location in prose or metadata with unknown media: confirmed.
- **Example:** film c3d8ee5e-b119-4654-99f9-c6545f650635; c3d8ee5e-b119-4654-99f9-c6545f650635/generation:4896743a-85d5-44df-8539-e08e0c8f7fdb; c3d8ee5e-b119-4654-99f9-c6545f650635/asset:288c7412-7e51-4301-af39-c1c460395c5c; source `studies/03-elements/outputs/case_evidence.csv (APEIROPHOBIA 03.6)`; excerpt: This single reference image is authoritative for the entire shot.
- **Denominator:** 16 panel films.
- **Competing explanation:** Authority wording may be boilerplate; panel selection is purposive; no population census of authority wording exists.
- **Confidence:** Single-coder panel coding; 7 of 16 panel films could not be coded.
- **Rests on:** [`studies/03-elements/README.md`](../studies/03-elements/README.md), [`studies/03-elements/outputs/authority.json`](../studies/03-elements/outputs/authority.json), [`studies/03-elements/outputs/panel_assignments.csv`](../studies/03-elements/outputs/panel_assignments.csv); checked numbers `t05a`, `t05b` in [`citations.csv`](outputs/citations.csv).

### T06. Put exclusions inside the main prompt

The separate negative-prompt field is almost unused; creators write what they do not want, such as music, voices or subtitles, into the main prompt instead.

- **How often:** Nonempty negative-prompt fields: 2 in 2 films. Exclusion wording in the mean film's prompts: video 90.87%, image 67.84%. Provisional exclusion component in video texts: 91.48%.
- **Where:** Image and video prompts. Literal models: `seedance_2_5`.
- **Evidence:** observed. Field states and lexical counts; the component share is inferred from provisional labels.
- **Strength:** strong for field use; exclusion wording is broad.
- **Study 04 status:** Study 06 lexical exclusion proxy: changed. It gains a provisional sampled semantic measure.
- **Example:** film 03f596b0-23da-4312-9e58-2e1cc4582348; 03f596b0-23da-4312-9e58-2e1cc4582348/generation:0a5dad36-f81f-4a32-a38a-bc7bcd103e7f; 03f596b0-23da-4312-9e58-2e1cc4582348/asset:9264c44d-ad74-4ddc-91fc-4490b55a5b18; source `studies/04-prompts/outputs/case_evidence.csv (THE LAST TRANSMISSION 04.2)`; excerpt: "camera":"locked frame on the dial and hands" ... no voice, no music
- **Denominator:** Negative-role fields in all 157 films; 37,079 nonempty video and 87,238 nonempty image prompts.
- **Competing explanation:** The negative field may be hidden in the interface for most models; exclusion keywords include common words in other senses.
- **Confidence:** Deterministic field and lexical counts; provisional semantic share.
- **Rests on:** [`studies/04-prompts/outputs/summary_text_role.csv`](../studies/04-prompts/outputs/summary_text_role.csv), [`synthesis/outputs/summaries.csv`](outputs/summaries.csv), [`studies/04-prompts/outputs/semantic_summary_generation_type.csv`](../studies/04-prompts/outputs/semantic_summary_generation_type.csv); checked numbers `t06a`, `t06b`, `t06c`, `t06d`, `t06e` in [`citations.csv`](outputs/citations.csv).

### T07. Continue from the previous clip

To carry action across clips, creators feed an earlier video back in, either guiding a new clip from it or declaring an extension, and say where to pick up.

- **How often:** Films with video guided by an earlier video: 113 of 156 video-bearing films. Declared extensions: 2,260 jobs in 53 films.
- **Where:** Video-to-video and extension. Literal models: `seedance_2_5`.
- **Evidence:** observed. Recorded video inputs and declared extension mode.
- **Strength:** strong for the routes; continuity achieved is not observed.
- **Study 04 status:** Study 07 raw input reuse or branch: undecided.
- **Example:** film 3b09c7c2-3f0c-48e3-8304-fad569bf50ce; 3b09c7c2-3f0c-48e3-8304-fad569bf50ce/generation:1d963033-bc45-495d-9bfa-a05e4d0cf918; 3b09c7c2-3f0c-48e3-8304-fad569bf50ce/asset:0e619b88-43ef-4a45-84c3-b7b86ac96fe4; source `studies/02-planning/outputs/case_evidence.csv (The Staff 02.4)`; excerpt: frame 1 same last frame from here <<<video_1>>>
- **Denominator:** 38,508 video jobs in 156 films.
- **Competing explanation:** Video inputs may be used for style or motion transfer rather than continuation; extension availability depends on the model.
- **Confidence:** Deterministic route counts; the media are not inspected.
- **Rests on:** [`studies/06-video/outputs/summaries.csv`](../studies/06-video/outputs/summaries.csv), [`synthesis/outputs/model_stages.csv`](outputs/model_stages.csv), [`studies/07-lineage/README.md`](../studies/07-lineage/README.md); checked numbers `t07a`, `t07b`, `t07c` in [`citations.csv`](outputs/citations.csv).

### T08. Combine source images and give each one a job

Composite image requests attach several images and say what to take from each, sometimes as an ordered checklist of properties to match.

- **How often:** Image jobs combining two or more inputs: 28.94% of the mean film's image jobs (pooled 30.63%; 150 of 155 films).
- **Where:** Image compositing and integration. Literal models: `seedream_v5_pro`, `nano_banana_2`, `gpt_image_2`.
- **Evidence:** observed. Recorded multi-input bindings; the ordered checklist is case wording.
- **Strength:** strong for multi-input use; checklist wording is case-scoped.
- **Study 04 status:** Study 05 integration properties and sheet, plate or poster purpose in cases: confirmed.
- **Example:** film d305f6e5-b906-49a1-a0c6-75ef7f653ad8; d305f6e5-b906-49a1-a0c6-75ef7f653ad8/generation:5bc1268c-ccc1-419e-bd13-79344eadf228; d305f6e5-b906-49a1-a0c6-75ef7f653ad8/asset:4ebd698e-e1f7-479d-93b0-4043e5e61913; d305f6e5-b906-49a1-a0c6-75ef7f653ad8/asset:c16ce530-c7d1-461a-acc8-63b8d7de63b1; source `studies/05-image/outputs/case_evidence.csv (Don't Poison Ivy 05.1)`; excerpt: TRANSPLANT THE PLANT FROM IMAGE 2 ONTO THE SHELF. FIRST, SCALE. SECOND, POSITION. THIRD, VIEWING ANGLE. FOURTH, LIGHTING.
- **Denominator:** 92,058 image jobs in 155 films.
- **Competing explanation:** Multiple inputs may be alternative candidates rather than parts; masks and layers are not recorded (L08).
- **Confidence:** Deterministic binding counts; single-coder case reading.
- **Rests on:** [`studies/05-image/README.md`](../studies/05-image/README.md), [`studies/05-image/outputs/summaries.csv`](../studies/05-image/outputs/summaries.csv), [`studies/05-image/outputs/construction_recipes.json`](../studies/05-image/outputs/construction_recipes.json); checked numbers `t08a`, `t08b`, `t08c` in [`citations.csv`](outputs/citations.csv).

### T09. Short edits ride on an attached image

Very short edit requests are almost always attached to an image and rarely use camera language; the image carries the context and the text names only the change.

- **How often:** Short image edits (4,116 prompts in 98 films) with an attached image: 98.39% per film versus 71.22% for all image prompts in those films (pooled 4,089/4,116). With camera wording: 4.81% versus 40.49%.
- **Where:** Image edits. Literal models: `nano_banana_2`.
- **Evidence:** associated. Co-occurrence of the short-edit proxy with recorded attachments and camera wording.
- **Strength:** strong for the association.
- **Study 04 status:** Study 05 short-edit proxy: changed. Edit intent is not a released semantic component.
- **Example:** film 655325cc-46d9-4b0b-b03d-d177defa4b3f; 655325cc-46d9-4b0b-b03d-d177defa4b3f/generation:19f73675-b69e-4314-b3a1-f74802df1da2; 655325cc-46d9-4b0b-b03d-d177defa4b3f/asset:6672ee33-d850-4db4-b78f-667905814400; source `studies/09-iteration/outputs/case_evidence.csv (The Kiss 09.3)`; excerpt: Move the entire title "The Kiss" UP ... Reduce the title's size slightly
- **Denominator:** 4,116 short-edit image prompts in 98 films.
- **Competing explanation:** The proxy is defined by length and edit wording, so dropping camera language partly follows from its definition.
- **Confidence:** Census-level association from released features.
- **Rests on:** [`synthesis/outputs/technique_pairs.csv`](outputs/technique_pairs.csv), [`studies/09-iteration/outputs/revision_spans.csv`](../studies/09-iteration/outputs/revision_spans.csv), [`studies/05-image/README.md`](../studies/05-image/README.md); checked numbers `t09a`, `t09b`, `t09c`, `t09d`, `t09e`, `t09f`, `t09g` in [`citations.csv`](outputs/citations.csv).

### T10. Lay out the frame in labelled sections, in prose rather than code

About a third of prompts use section labels, such as foreground, middle ground and background, to organise a description. Machine-style JSON prompts are rare.

- **How often:** Sectioned primary prompts: 35.45% per film (pooled 37.58%). JSON-structured prompts: image 0.55%, video 0.94% per film.
- **Where:** Image and video prompts. Literal models: `nano_banana_2`.
- **Evidence:** observed. Lexical section labels and JSON detection.
- **Strength:** moderate: section detection is lexical.
- **Study 04 status:** Study 02 section, reference and multi-shot lexical proxies: changed. The structural census stays; semantic components are a sampled addition.
- **Example:** film 3777eda4-c15e-4531-9f04-4c02a900f3c3; 3777eda4-c15e-4531-9f04-4c02a900f3c3/generation:3e7791d1-6165-4a81-bbaa-575811c1edd8; source `studies/05-image/outputs/case_evidence.csv (Dry Aged Dreams 05.4)`; excerpt: FOREGROUND: ... MIDDLE GROUND: ... BACKGROUND:
- **Denominator:** 124,449 nonempty primary prompts in 157 films; 87,238 image and 37,079 video prompts.
- **Competing explanation:** Section labels may come from templates or prompt-writing tools; labels in other languages are missed.
- **Confidence:** Deterministic lexical counts.
- **Rests on:** [`studies/02-planning/outputs/summaries.csv`](../studies/02-planning/outputs/summaries.csv), [`synthesis/outputs/summaries.csv`](outputs/summaries.csv), [`studies/05-image/outputs/construction_recipes.json`](../studies/05-image/outputs/construction_recipes.json); checked numbers `t10a`, `t10b`, `t10c`, `t10d` in [`citations.csv`](outputs/citations.csv).

### T11. Revise a clip by naming the fix and keeping the rest

Video revisions bound to an earlier clip ask for a specific fix and say everything else stays; video edit wording comes with preservation wording more often than other video prompts do.

- **How often:** Video edit prompts with preservation wording: 50.74% of the mean film's edit prompts versus 38.33% of its video prompts (148 films).
- **Where:** Video revision. Literal models: `seedance_2_5`.
- **Evidence:** associated. Co-occurrence of lexical edit and preservation wording; the case shows the revision wording.
- **Strength:** moderate.
- **Study 04 status:** Study 09 local correction, derivative and specificity scoped to cases: confirmed. Study 09 preservation and edit markers: changed.
- **Example:** film e5ce8a79-9375-4e31-84a8-620bd4f07550; e5ce8a79-9375-4e31-84a8-620bd4f07550/generation:09925f84-295d-42ac-a3f2-d8dbf98a1740; e5ce8a79-9375-4e31-84a8-620bd4f07550/asset:66411159-7e3c-4216-8031-e096668d53a1; source `studies/06-video/outputs/case_evidence.csv (Lost 06.5)`; excerpt: make everything the same but fix the sounds and color grading ... one continuous shot with no cuts
- **Denominator:** 12,676 video edit prompts in 148 films.
- **Competing explanation:** Edit words also describe in-scene actions; revisions outside the platform are invisible.
- **Confidence:** Census-level association from released features; single-coder case reading.
- **Rests on:** [`synthesis/outputs/technique_pairs.csv`](outputs/technique_pairs.csv), [`studies/09-iteration/README.md`](../studies/09-iteration/README.md), [`studies/06-video/outputs/revision_requests.json`](../studies/06-video/outputs/revision_requests.json); checked numbers `t11a`, `t11b`, `t11c`, `t11d` in [`citations.csv`](outputs/citations.csv).

## What the evidence cannot tell

### L01. What separates top films from others

Only the selected cohort has detailed records, so nothing here says what distinguishes these films from films outside it. Study 11, waiting for the festival winners, can describe the winners' records but not why they won.

- **How often:** Detailed histories exist for 157 primary films (130,704 jobs); there is no comparison group of non-selected films.
- **Where:** Whole programme. Literal models: none named.
- **Evidence:** observed. The scope of the published cohort.
- **Strength:** certain: a design limit.
- **Study 04 status:** No Study 04 dependency.
- **Example:** film all primary films; film:* in the published snapshot; source `studies/01-corpus/outputs/eligibility.csv`; excerpt: primary population membership
- **Denominator:** 157 primary workspaces; the supplemental Cosmic tracks pilot is excluded.
- **Competing explanation:** None: the limit follows from the data's scope.
- **Confidence:** Programme design and Study 01 populations.
- **Rests on:** [`PROGRAMME.md`](../PROGRAMME.md), [`studies/01-corpus/README.md`](../studies/01-corpus/README.md), [`studies/10-organisation/outputs/summaries.csv`](../studies/10-organisation/outputs/summaries.csv); checked numbers `l01a`, `l01b` in [`citations.csv`](outputs/citations.csv).

### L02. Whether any technique works

Every technique above is an instruction or a binding, not an outcome: no output was watched or judged. Testing them needs Study 12's controlled experiments, for example a reference sheet against a text description of identity, staged against one-pass generation, a local edit against regeneration, and continuing from a last frame against re-referencing.

- **How often:** Points in this synthesis labelled experimentally supported: 0 of 40.
- **Where:** All techniques. Literal models: none named.
- **Evidence:** proposed. The follow-up experiments are proposals.
- **Strength:** certain for the gap.
- **Study 04 status:** Study 04's confirmations concern definitions, not effects.
- **Example:** film not applicable; none; source `synthesis/points.json`; excerpt: evidence_label values of all points
- **Denominator:** All points in this synthesis.
- **Competing explanation:** Adoption or reuse could be read as success, but use is not approval or quality.
- **Confidence:** Follows from the evidence rules.
- **Rests on:** [`PROGRAMME.md`](../PROGRAMME.md), [`studies/04-prompts/dependencies.csv`](../studies/04-prompts/dependencies.csv); checked numbers none in [`citations.csv`](outputs/citations.csv).

### L03. Failure, retry and discard rates

The records hold no failure, rejection or approval state. Outputs that were not taken further are not failures, and rerun candidates have unknown motives.

- **How often:** Only 14.74% of the mean film's jobs are taken further; the rest have no recorded use, which is not the same as failure. Rerun candidates: 31.05% of the mean film's jobs, motive unknown.
- **Where:** Iteration. Literal models: none named.
- **Evidence:** observed. Absence of status fields in the released records.
- **Strength:** certain for the gap.
- **Study 04 status:** Study 09 equal-request rerun candidates: undecided. Motives need human validation.
- **Example:** film all primary films; generation:* per film; source `studies/09-iteration/outputs/film_metrics.csv`; excerpt: adopted and rerun_candidate counts per film
- **Denominator:** 130,704 jobs in 157 films.
- **Competing explanation:** Unused outputs may be used outside the platform; batches make many siblings by design.
- **Confidence:** Follows from the released fields; a study with creators or platform status data would be needed.
- **Rests on:** [`studies/09-iteration/README.md`](../studies/09-iteration/README.md), [`studies/09-iteration/outputs/summaries.csv`](../studies/09-iteration/outputs/summaries.csv); checked numbers `l03a`, `l03b` in [`citations.csv`](outputs/citations.csv).

### L04. Labour, cost and speed

Timestamps show when recorded jobs ran, not how long anyone worked, and no credits or costs are recorded. Spans and active dates are not effort measures.

- **How often:** Mean event span 21.7 days and 16.6 active UTC dates per film across 157 films; neither measures labour.
- **Where:** Whole production. Literal models: none named.
- **Evidence:** observed. Timestamp summaries; no cost fields exist.
- **Strength:** certain for the gap.
- **Study 04 status:** No Study 04 dependency.
- **Example:** film all primary films; generation:* timestamps per film; source `studies/10-organisation/outputs/film_metrics.csv`; excerpt: event_span_days and active_utc_dates per film
- **Denominator:** 157 films.
- **Competing explanation:** Work happens offline, in other tools and in unpublished workspaces.
- **Confidence:** Follows from the released fields.
- **Rests on:** [`studies/10-organisation/README.md`](../studies/10-organisation/README.md), [`studies/10-organisation/outputs/summaries.csv`](../studies/10-organisation/outputs/summaries.csv); checked numbers `l04a`, `l04b` in [`citations.csv`](outputs/citations.csv).

### L05. Agents, scripts and hidden orchestration

Nothing in the records distinguishes a person clicking from a script or agent submitting jobs, and any planning outside the platform is invisible.

- **How often:** Jobs recorded under the declared owner's author ID: 93.98% of the mean film's jobs; no field records what submitted a job.
- **Where:** Whole production. Literal models: none named.
- **Evidence:** observed. Author and declared owner IDs only; an author ID is not a person, tool or labour measure.
- **Strength:** certain for the gap.
- **Study 04 status:** No Study 04 dependency.
- **Example:** film all primary films; generation:* author records per film; source `studies/10-organisation/outputs/author_operations.csv`; excerpt: owner and author job counts
- **Denominator:** 130,704 jobs in 157 films.
- **Competing explanation:** Batch and repeat patterns could come from either people or automation.
- **Confidence:** Follows from the released fields.
- **Rests on:** [`studies/10-organisation/README.md`](../studies/10-organisation/README.md), [`studies/10-organisation/outputs/summaries.csv`](../studies/10-organisation/outputs/summaries.csv); checked numbers `l05a` in [`citations.csv`](outputs/citations.csv).

### L06. Why seedance_2_5 dominates

The concentration on one video model could reflect availability, defaults, price or timing as much as preference. Separating these needs the platform's model offer and default history over the contest window, or a controlled comparison.

- **How often:** seedance_2_5 pooled share of video jobs: 80.72%; reasons recorded: none.
- **Where:** Video generation. Literal models: `seedance_2_5`.
- **Evidence:** observed. The share is observed; reasons are not.
- **Strength:** certain for the gap.
- **Study 04 status:** No Study 04 dependency.
- **Example:** film all video-bearing primary films; per-film generation:* model counts; source `synthesis/outputs/model_concentration.csv`; excerpt: seedance_2_5_jobs per film
- **Denominator:** 38,508 video jobs in 156 films.
- **Competing explanation:** See the finding: offer, defaults, price, timing.
- **Confidence:** Follows from the released fields.
- **Rests on:** [`synthesis/outputs/summaries.csv`](outputs/summaries.csv); checked numbers `l06a` in [`citations.csv`](outputs/citations.csv).

### L07. Semantic findings rest on a provisional sample

The instruction-component findings come from one local model's provisional labels on a stratified sample, with long texts excluded and agreement measured against a single coder. A multilingual, adjudicated census would be needed to treat them as more than provisional.

- **How often:** Labelled 4,633 of 5,000 sampled texts; 5,922 of 61,422 distinct texts (9.64%) too long to label; pooled kappa 0.779 over 3,864 decisions against the single-coder gold.
- **Where:** All prompt interpretation. Literal models: none named.
- **Evidence:** observed. Coverage and agreement of the label release.
- **Strength:** certain for the limits.
- **Study 04 status:** Each of Study 04's dependency assessments names a remaining Study 12 step, such as adjudicated semantic coding or validation.
- **Example:** film not applicable; text_id:* in prompt-labels-v2; source `studies/04-prompts/outputs/coverage.json`; excerpt: long_texts.excluded_long_texts; sample.successes
- **Denominator:** 5,000 sampled texts; 61,422 distinct texts; 276 gold texts by 14 components.
- **Competing explanation:** Label errors may be systematic by language or task; the gold coder may share the labeller's blind spots.
- **Confidence:** Agreement pooled here from Study 04's per-component counts.
- **Rests on:** [`prompt-labels/RELEASE.md`](../prompt-labels/RELEASE.md), [`studies/04-prompts/README.md`](../studies/04-prompts/README.md), [`studies/04-prompts/outputs/coverage.json`](../studies/04-prompts/outputs/coverage.json), [`studies/04-prompts/outputs/agreement.csv`](../studies/04-prompts/outputs/agreement.csv), [`synthesis/outputs/label_agreement.csv`](outputs/label_agreement.csv); checked numbers `l07a`, `l07b`, `l07c`, `l07d`, `l07e`, `l07f`, `l07g`, `l07h`, `l07i` in [`citations.csv`](outputs/citations.csv).

### L08. What is in the media, where edits land and what reached the screen

Attached images and videos are never inspected, no mask or layer is recorded, and no job is linked to the final cut, so where an edit applied and which outputs appear in the film are unknown. External sound and editing pipelines are outside the records.

- **How often:** Of 92,058 image jobs, 0 have the inpaint flag on and 0 have an active mask or layer.
- **Where:** Image edits; final assembly. Literal models: none named.
- **Evidence:** observed. Literal control and field states.
- **Strength:** certain for the gap.
- **Study 04 status:** Study 03 property location with unknown media: confirmed.
- **Example:** film all image-bearing primary films; generation:* control states; source `studies/05-image/outputs/mask_layer_paths.csv`; excerpt: mask and layer parameter paths
- **Denominator:** 92,058 image jobs in 155 films.
- **Competing explanation:** Masks may exist in interface state that is not exported.
- **Confidence:** Follows from the released fields.
- **Rests on:** [`studies/05-image/README.md`](../studies/05-image/README.md), [`studies/05-image/outputs/summaries.csv`](../studies/05-image/outputs/summaries.csv); checked numbers `l08a`, `l08b`, `l08c` in [`citations.csv`](outputs/citations.csv).

### L09. Versions, aliases and approval

Versions of an element are inferred from lineage, not declared, and nothing marks an output as approved. Whether two records are the same asset under different IDs is undecided.

- **How often:** Panel films with inferred versions: 6 of 16; panel films where versions could not be coded: 10 of 16.
- **Where:** Elements and lineage. Literal models: none named.
- **Evidence:** inferred. Versions are inferred from recorded derivation.
- **Strength:** moderate.
- **Study 04 status:** Study 07 within-asset representations and zero cross-ID merges: undecided.
- **Example:** film d90fe8bd-3329-40b3-963c-d9b33075aec1; d90fe8bd-3329-40b3-963c-d9b33075aec1/generation:006dcc36-ec37-490f-9890-9524e3ed0ddd; d90fe8bd-3329-40b3-963c-d9b33075aec1/generation:011fbb97-732a-416b-825f-a9635b313b86; source `studies/03-elements/outputs/case_evidence.csv (Detour 03.5)`; excerpt: [producer model] seedream_v5_pro [consumer model] gpt_image_2 [changed property excerpt] The only change is a small mark of tomato ketchup
- **Denominator:** 16 panel films.
- **Competing explanation:** A derived image may be a new element rather than a version.
- **Confidence:** Single-coder panel coding.
- **Rests on:** [`studies/03-elements/outputs/panel_assignments.csv`](../studies/03-elements/outputs/panel_assignments.csv), [`studies/03-elements/outputs/versions.json`](../studies/03-elements/outputs/versions.json), [`studies/07-lineage/outputs/alias_audit.csv`](../studies/07-lineage/outputs/alias_audit.csv); checked numbers `l09a`, `l09b` in [`citations.csv`](outputs/citations.csv).

### L10. Whether longer or more structured prompts are better

Long, sectioned prompts are common, but nothing links length or structure to a better result; length is not quality. An optimal length or structure needs a controlled test.

- **How often:** Median of per-film median video prompt length 5,104 characters; outcome measures available: none.
- **Where:** Prompt writing. Literal models: none named.
- **Evidence:** observed. Lengths are observed; outcomes are absent.
- **Strength:** certain for the gap.
- **Study 04 status:** Study 09 exact, token and length deltas: confirmed as distinct from specificity.
- **Example:** film all video-bearing primary films; text_id:* per film; source `synthesis/outputs/technique_by_film.csv`; excerpt: median_characters per film and task
- **Denominator:** 37,079 nonempty video prompts in 156 films.
- **Competing explanation:** Long prompts may be templates; short prompts may rely on attached images (T09).
- **Confidence:** Follows from the released fields.
- **Rests on:** [`synthesis/outputs/summaries.csv`](outputs/summaries.csv), [`studies/04-prompts/README.md`](../studies/04-prompts/README.md); checked numbers `l10a` in [`citations.csv`](outputs/citations.csv).

### What would settle these questions

| Question | Why these records cannot answer it | What could |
| --- | --- | --- |
| What separates top films from others (L01) | Only the selected cohort has detailed records | Study 11 can describe the festival winners' records; a comparison with non-selected films needs records the programme does not hold |
| Whether a technique helps (L02, L10) | Records are instructions and bindings, never outcomes | Study 12 controlled experiments: reference sheet against text identity, staged against one-pass, local edit against regeneration, last-frame continuation against re-referencing, prompt length and structure |
| Failure, retry and discard rates (L03) | No status, rejection or approval field | Study 12 human validation of rerun candidates; platform status data or creator accounts |
| Labour, cost and speed (L04) | Timestamps are not working time; no costs | Creator-reported time and spend; outside these records |
| Agents and orchestration (L05) | No field records what launched a job | Platform client metadata or creator accounts |
| Why seedance_2_5 dominates (L06) | Model offer, defaults and prices over time are not recorded | The platform's model and default history for the contest window; a controlled comparison in Study 12 |
| Instruction components at census scale (L07) | Provisional sample, long texts excluded, single-coder gold | Study 12 multilingual, adjudicated semantic census |
| Media contents and final screen use (L08) | Media are not inspected; no job-to-final-cut link | Creator edit decision lists; inspecting media falls outside this programme's evidence rules |
| Versions, aliases and approval (L09) | Versions are inferred; alias equivalence undecided | Study 12 explicit alias and approval evidence |

## Method

The synthesis reran no study and edited none. It reads committed study outputs and
three published releases: prompt-labels-v1 (structural features and text
occurrences), prompt-labels-v2 (provisional semantic labels) and study-07-v1 (the
lineage graph). It does not read the source snapshot. The releases are verified
against their `SHA256SUMS` and pinned to the digests that Study 04 and Study 07
recorded.

New analyses, each written to `outputs/`:

1. **Models by production stage** (`model_stages.csv`): each literal model's share of
   a film's jobs in eleven stages, from image jobs with no recorded input to voice
   adapters, built from Study 08's role matrix.
2. **Model handoffs** (`model_handoffs.csv`): producer and consumer model shares for
   image-to-video, video-to-video, image-to-image and into-finishing handoffs, from
   Study 08's transitions and model inventory.
3. **Model profiles** (`model_profiles.csv`): for each model, among films using it,
   its input use, chaining, batching, further use, rerun candidates and prompt traits.
   This joins Study 08 roles, Study 09 iteration counts and Study 04 prompt counts.
4. **Model concentration** (`model_concentration.csv`): image and video model counts
   and top-model shares per film.
5. **Structural technique census** (`technique_by_film.csv`, `technique_pairs.csv`):
   fourteen prompt traits for every primary prompt, from prompt-labels-v1 features
   joined to Study 07 graph bindings, with per-film co-occurrence of each trait pair.
   The census is checked to reproduce Study 04's per-film primary counts exactly.
6. **Semantic co-occurrence** (`semantic_pairs.csv`, `semantic_breadth.csv`): pairs of
   provisional components and components per text, weighted with Study 04's stratum
   weights. The weighting is checked to reproduce Study 04's per-film semantic
   estimates exactly.
7. **Pooled label agreement** (`label_agreement.csv`): one kappa per comparison, from
   Study 04's per-component agreement counts.
8. **Summaries** (`summaries.csv`): per-film distributions behind the points.

`points.json` is the register: each point's text, provenance and cited numbers.
`points.csv` and `citations.csv` are its checked, rendered form. `reproduction.json`
records the release digests, input hashes and output hashes. Every output is a small
CSV or JSON file under 1 MB. No full prompt text is written; examples quote short spans
that committed study outputs already contain.

## Reproduction

From the repository root, download the three releases into new directories. With
`gh`:

```bash
uv sync --locked
gh release download prompt-labels-v1 --dir data/prompt-labels-v1
gh release download prompt-labels-v2 --dir data/prompt-labels-v2
gh release download study-07-v1 --dir data/study-07-v1
uv run python synthesis/build.py
```

Without `gh`, fetch each asset and its `SHA256SUMS` with
`curl -L https://github.com/TelesforoAleix/ai-film-practice/releases/download/<tag>/<asset>`.
The build verifies every asset. Without `--check` it rewrites `outputs/` and this
README. With `--check` and a separate output directory, it rebuilds there and
compares every output, and this README, byte for byte:

```bash
uv run python synthesis/build.py --v1 <fresh-v1> --v2 <fresh-v2> \
  --study07 <fresh-study07> --output data/synthesis-check --check
```

`tests/test_synthesis.py` checks the committed outputs against
`reproduction.json`, re-verifies every citation and re-renders this README from
committed files. It reruns the full build when the three releases are present.
