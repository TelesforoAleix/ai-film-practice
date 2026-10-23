<!-- Generated from README.template.md and points.json by synthesis/build.py; edit those, not this file. -->

# Findings synthesis of Studies 01–10

This document gathers what Studies 01–10 found into small, self-contained points. It
covers the {{l01a}} primary workspace histories only; the supplemental Cosmic tracks
pilot is excluded. It is a synthesis, not the Study 12 deliverables: there is no
playbook, architecture, contract, experiment backlog or MVP here.

## The short version, for creators

These films' production records show how people worked on the platform. They do not
show what worked, because nothing here was watched or judged.

1. **Video starts from a picture.** In almost every film, clips were generated from an
   image or frame rather than from words alone: {{p01a}} of the average film's video
   jobs had an image attached. Creators make stills first, then animate them.
2. **One video model, several image models.** Most films made nearly all of their video
   with one model, seedance_2_5, the main video model in {{m01a}} of the {{p01h}} films
   with video. For images, a typical film used about {{m02a}} different models, led by
   three that take an uploaded image and change it.
3. **Video prompts are written out in full.** The typical film's video prompt runs to
   about {{p04a}} characters, several paragraphs covering the camera, the action, the
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

This synthesis has {{points-total}} points: {{points-pattern}} main patterns, {{points-model}} model preferences, {{points-technique}} techniques and {{points-limit}} limits.

## Main patterns

{{section:pattern}}

## Model preferences

"Preference" here means recorded use of a literal model identifier. Why creators
chose a model is not recorded (L06).

{{section:model}}

## Techniques and tips

These are techniques visible in the records: instructions and bindings that creators
used. None has been tested for benefit (L02). Read them as practices to try, not as
proven best practice.

{{section:technique}}

## What the evidence cannot tell

{{section:limit}}

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
