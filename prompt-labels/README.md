# Provisional prompt labels — AF3a v1

This is the feature, sampling, gold and harness infrastructure for Study 04,
under PROGRAMME.md and codebook **1.0**. Structural features describe exported
text. Semantic labels describe explicit instructions, never achieved media
properties. No film was watched, model run performed, or source site retrieved.
The later slice must run the chosen local model, assess agreement and publish
its provisional labels. This is not the completed Study 04 report or its
nine-item findings contract.

The only source is the verified `data-2026-10-20` snapshot, joined through
`film_practice.connect`. Study 01's compound field grain and primary/nested
crosswalk are binding. Original data, Study 01 and the case files are unchanged.
Only the selected cohort has detailed records; none of these outputs establish
what separates top films from other films, successful practices, quality,
agents, internal orchestration, labour, costs or failure rates.

## Units, reconciliation and provenance

[build.py](build.py) starts with `generations.prompt`, then appends
`generation_prompts.text` except the **same compound generation and primary
source path**. It asserts that those duplicate exports are byte-identical.
It keeps null/unavailable and explicitly empty fields separate and excludes
both from exact-text feature/sampling units. No whitespace, Unicode, case or
line-ending normalisation occurs. A `text_id` is SHA-256 of exact UTF-8 bytes;
hash collisions with different text cause an error.

| Unit / denominator | Count |
| --- | ---: |
| Nonempty primary fields, all 158 histories | 124,642 |
| Distinct primary texts, all 158 histories | **61,479** |
| Distinct primary texts, 157 primary films | 61,359 |
| Distinct texts after adding nested fields, all 158 histories | **61,542** |
| Distinct all-role texts, 157 primary films | **61,422** |
| Distinct all-role texts, supplemental pilot | 122 |
| All-role texts shared between primary and supplemental | 2 |
| Nonempty source-field occurrences after primary crosswalk | 160,753 |
| Explicit empty / unavailable primary fields | 1,083 / 5,174 |

Thus 61,479 is exactly reproduced, with no discrepancy: 63 additional distinct
nested texts give 61,542. Removing the pilot's 120 exclusive texts gives 61,422;
61,422 + 122 − 2 = 61,542. Primary fields alone contain 120 pilot-exclusive
texts too. Repeats across jobs, roles, films or creators are not independent
observations. The pilot is retained in structural outputs with its own population,
and excluded from sampling and gold.

Roles use source paths, not a semantic guess: primary comes from
`generations.prompt`; the negative role is explicit; `params.multi_prompt[*].prompt`
is `shot_prompt`; all remaining nested fields are `other_text`. The snapshot has
no explicit script path. `other_text` includes `params.prompt_language` (language
metadata), enhanced prompts and a source prompt. Preserve that distinction when
using the labels: language metadata is not a generation instruction. The export's
literal `prompt_or_text` role alone does not make these interchangeable prompts.
There are 124,449 primary, 36,056 other-text, 19 shot-prompt and 2 negative
nonempty field occurrences in primary films, after the crosswalk.

`occurrences.parquet` retains every nonempty compound film/generation/field key,
source table, source-record path, generation type, literal model, population and
text hash. `features.parquet` has one row per exact text hash. Join these for the
named source of any measure; join source usages/references later on compound
keys for codes 04.3–04.4. Tokens alone never prove an attachment or its contents.
No inferred lineage is introduced here.

Structural matches are **observed lexical/format measures**; interpreting them as
an operation or semantic component is **inferred** and unvalidated. For every
feature row the denominator is one exact text, and its excerpt is the first
literal match (null when absent, or when quoting it would reproduce the entire
field). The source hash and occurrence crosswalk permit complete retrieval.
For every summary, the explicit `distinct_texts_denominator` is authoritative.
Competing explanations include multilingual wording, boilerplate, quoting,
negation and terminology unrelated to a requested operation. Confidence is high
in the deterministic count under the documented rule, not in semantic coverage
or execution. These rules are the common measure/provenance contract for the
feature tables, not evidence of benefits or prevalence outside this cohort.

## Structural features over every text

The exact regular expressions and thresholds live in [build.py](build.py).

| Feature | Literal rule / limit |
| --- | --- |
| Characters / UTF-8 bytes / whitespace words / lines | Python length; encoded byte length; `split()` count; LF count + 1. Not tokenizer counts. |
| Sections | Line-start Markdown headings, uppercase labels with colon, or short standalone colon headings. |
| Structured JSON | Whole field parses with `json.loads` into an object or array; JSON-shaped prose is insufficient. |
| XML-like | Matching opening/closing tag pattern, explicitly a lexical proxy, not XML validation. |
| Reference tokens | `@` words, numbered image/ref/video mentions and angle-bracket tokens. Unresolved until joined to usages. |
| Camera / lens vocabulary | English movement words, lens terms, focal length, aperture and shot sizes; counts can overlap. |
| Preservation / exclusion / edit phrases | Explicit English lexical matches, not a semantic classifier; quoted or negated phrases still match. |
| Multi-shot | Numbered shot, multi-shot or numeric shot-count wording; not enabled controls. |
| Repeated lines | Extra exact stripped line occurrences, only lines at least 40 characters long; not arbitrary repeated substrings or cross-text similarity. |
| Short edit / long description proxies | At most 300 characters plus edit vocabulary / at least 1,000 characters; never claims of actual edits or full descriptive content. |
| Semantic eligibility | Nonempty field with at most 12,000 characters. |

[features_by_film.csv](outputs/features_by_film.csv) counts each text once within
its film. [features_by_stratum.csv](outputs/features_by_stratum.csv) counts each
text once within film × literal generation type × text role. `_sum` columns sum
counts or true indicators; divide by that row's text denominator to obtain means
or shares, respectively. Summing strata can count a shared text more than once.
Null generation types remain `\N` in CSV, distinct from empty strings; JSON uses
null. These are text-weighted summaries within each film, not job-weighted rates.
For comparisons, give films equal weight rather than pooling prolific histories.
The pilot's summary rows are separate and must stay separate.

The lexical rules primarily recognise English, despite the multilingual corpus.
Their absence is not semantic absence. Aesthetic *intent* is coded as words,
never an assessment of aesthetics or output quality.

## Semantic definitions

All fourteen binary components below use the same definitions in the gold and
in the harness. JSON keys follow code 04.2 (`spatial`, `aesthetic_intent`,
`exclusion`, `preservation` correspond to spatial relations, aesthetic, exclusions
and preservation instructions). Definitions and the strict response schema are
in the additive [shared module](../src/film_practice/prompt_labels.py).

Presence requires an explicit supporting span in the **field being labelled**;
choose the shortest sufficient contiguous exact source span. Otherwise use false
and null, not empty text. Overlap between components is allowed. An instruction
to retain a property's existing state can count for that property and for
preservation. Names/reference bindings may establish requested identity without
revealing the media. Do not infer unspecified properties from a reference.
Scripted dialogue is content, not automatically an instruction to depict every
entity or event it mentions; explicit performance directions can qualify.
Time of day alone does not establish lighting or timing.

The stored span must always be an exact contiguous substring of the source field.
The local harness first tries the AF3a2 closed normalisation: NFC, case-folding,
whitespace-run collapse, trimmed span-edge whitespace, typographic quote
normalisation and en/em-dash normalisation. If that fails, it may split on an
ellipsis separator (two or more full stops, or `…`) and resolve each fragment in
order using the same exact-then-normalised rule, starting each search at the end
of the preceding match. It stores the shortest contiguous source passage covering
the ordered fragments and records that component in `joined_spans`. A leading or
trailing ellipsis resolves its single nonempty fragment. Missing or out-of-order
fragments remain `unsupported_span`; no fuzzy matching, reordering or other
separator is allowed. Ordinary normalised matches are listed in `resolved_spans`;
each component appears in only one list. An exact full-span match takes precedence,
including when the source itself contains ellipses. The standalone `validate`
function and gold release continue to require exact spans.

| Component / key | Inclusion | Exclusion |
| --- | --- | --- |
| `subject` | Explicit entity to depict or manipulate: person, animal, object or group. | Exclude setting alone and generic image/video placeholders without an entity. |
| `identity` | Explicit named identity, identifying appearance, or same-entity binding to a reference. | Exclude generic category alone (a man) and style-only reference bindings. |
| `action` | Explicit subject activity, pose, expression or physical state to depict. | Exclude camera movement and editing verbs alone (replace, generate). |
| `environment` | Explicit location, setting, weather or surrounding scene context. | Exclude isolated object material and image background references without a setting. |
| `spatial` | Explicit relative placement, orientation, scale, distance or occlusion of entities. | Exclude camera framing alone and location nouns without a relation. |
| `composition` | Explicit arrangement of the image: balance, layout, view angle, focus or depth. | Exclude entity relations alone and bare shot-size/lens terms. |
| `lens_framing` | Explicit lens, focal length, aperture, shot size, crop or framing specification. | Exclude vague cinematic intent and camera movement without framing. |
| `camera_motion` | Explicit camera movement or an instruction to keep the camera static. | Exclude subject motion and a fixed viewing angle without movement constraints. |
| `lighting` | Explicit illumination source, direction, softness, exposure, shadow or light colour. | Exclude time of day alone, object colour and emotional mood without illumination. |
| `material` | Explicit substance, surface texture, finish or physical wear of depicted entities. | Exclude colour alone, film grain and rendering style. |
| `aesthetic_intent` | Explicit rendering medium, stylistic treatment, palette or aesthetic intent. | Exclude evaluation of achieved quality and object colour without stylistic treatment. |
| `timing` | Explicit duration, speed, temporal ordering, beats, pauses or synchronisation. | Exclude time-of-day settings and motion verbs without temporal qualification. |
| `exclusion` | Explicit forbidden content, behaviour or alteration, including negative lists. | Exclude mere absence descriptions and preservation-only positive instructions. |
| `preservation` | Explicit instruction to retain a property, identity, source or state unchanged. | Exclude a reference mention alone or a new desired property without retention. |


## Deterministic sample and long texts

Seed: `AF3a-v1-20261020`. No labels influenced selection. [strata.csv](outputs/strata.csv)
records eligible distinct-text candidates, sampled and gold counts for every
film × literal generation type × text-role stratum (481 eligible occupied strata).
`generation_type` is a recorded job type, not an inferred operation ontology.
Null and empty values stay distinct.

Selection rotates across films, then across each film's nonempty operation/role
buckets, using SHA-256 seed/salt rankings for film order, operation order and text
order. One representative per film/type/role/text is chosen by sorted compound
source key. On each visit select one unseen text; skip text hashes already
selected anywhere, including in another film or operation. Empty/exhausted
buckets are skipped and unused film capacity is redistributed by the same
rotation. This is balanced stratified coverage, not a proportional job sample
or an estimator with known equal inclusion probabilities. A shared text has one
assigned source stratum for sampling but all its occurrences remain available.

The result is **5,000 globally distinct texts from all 157 primary films**,
occupying 338 strata. Film allocations: 80 films have 32 texts, 72 have 33;
five exhausted films have 1, 11, 15, 15 and 22. This prevents prolific histories
from dominating while retaining small histories. Global deduplication means the
481 bucket candidate counts overlap: not all can receive separate unique texts.
The sample has 2,338 image, 2,622 video and 40 audio records; roles are 4,948
primary, 38 other-text, 12 shot-prompt and 2 negative. Rare/unknown job types
without a selected unique nonempty text do not acquire invented observations.

**Long-text rule:** exclude texts longer than 12,000 Unicode characters from the
semantic sampling frame, never truncate. All still receive structural features.
This affects **5,929/61,542** distinct all-history texts and **5,922/61,422**
primary-population texts (9.64% of the latter). It conditions semantic results on
the remaining 55,500 primary texts and may remove systematically different
instructions. Sample maximum: 11,991 characters. Text exported incomplete by the
source remains exactly as exported; this code performs no repair or truncation.

## Gold subset and its limits

The same film/operation rotation, with a separate `gold` salt, selects **300 texts
from the sample**, across all **157 films** and **298 strata**: 143 films have two
texts and 14 have one. Types: 153 image, 137 video, 10 audio. Roles: 287 primary
and 13 other-text. There are no shot-prompt or negative-role gold records; the
later agreement report must state that coverage gap, not claim validation of
those roles. All 300 complete sampled fields were read by one Codex agent coder;
[readings.json](readings.json) stores that coder's positive spans by text hash.
[gold.py](gold.py) materialises all fourteen decisions and validates exact spans.
No classifier, endpoint or lexical rule assigned the semantic gold labels.

[gold.jsonl](outputs/gold.jsonl) contains IDs, paths, short spans, labels,
provisional status, coder, evidence label, denominator, competing explanation and
confidence rationale. No full prompt is committed. The source wording is observed;
component interpretation is **inferred**. This is **single-coder, agent-labelled,
with no adjudication**, independent human coder or inter-coder reliability estimate.
It can contain semantic mistakes and reflects the same agent's definition choices.
It is a provisional reference, not verified ground truth. Absent means not explicit
in this text under these rules, never absent from the film or attached media.

| Component | Present / 300 |
| --- | ---: |
| subject | 278 |
| identity | 220 |
| action | 219 |
| environment | 190 |
| spatial | 240 |
| composition | 232 |
| lens_framing | 212 |
| camera_motion | 131 |
| lighting | 226 |
| material | 213 |
| aesthetic_intent | 238 |
| timing | 150 |
| exclusion | 237 |
| preservation | 200 |

## Run the harness later

Requires Python 3.11+, the locked project environment, and a local OpenAI-compatible
chat server with JSON-schema response support. No model choice is hardcoded.
From the repository root:

```bash
uv sync --locked
uv run python scripts/fetch_data.py
gh release download prompt-labels-v1 --repo TelesforoAleix/ai-film-practice --dir data/prompt-labels-v1
(cd data/prompt-labels-v1 && shasum -a 256 -c SHA256SUMS)
gzip -dc data/prompt-labels-v1/sample.jsonl.gz > data/prompt-labels-v1/sample.jsonl
uv run python prompt-labels/harness.py --sample data/prompt-labels-v1/sample.jsonl --data data --base-url http://127.0.0.1:8080/v1 --model local-model --output data/semantic-labels.jsonl --max-attempts 3 --timeout 180 --max-tokens 1400
uv run python prompt-labels/agreement.py --gold prompt-labels/outputs/gold.jsonl --labels data/semantic-labels.jsonl --output data/agreement.json
```

Replace `local-model` with the chosen server's accepted model name. Configure its
context window for the complete request with that model's tokenizer; disable any
server-side prompt truncation. The character ceiling is not a tokenizer guarantee.
Mean/median sample text: 3,352/2,339 characters, approximately 838/585 tokens at
four characters/token. Definitions/template are 2,885 characters, the context wrapper 99 and schema 2,596,
roughly another 1,395 tokens combined. Budget **about 2,300 input tokens plus
350–900 output tokens per prompt** (about 11.5 million input tokens for 5,000
requests, before retries); long and non-Latin texts can be substantially larger.
The 1,400 output-token setting is configurable, not an assertion about a chosen
model's requirements or actual usage. No GPU-time or cost estimate is inferred.

[harness.py](harness.py) retrieves each sampled source by compound key and checks
its hash. Each request contains one whole prompt, its recorded generation type/text role,
definitions and strict JSON schema at `POST <base-url>/chat/completions`. Source text is untrusted user content;
it is never executed. Temperature is zero, streaming is off. Schema validation
requires exactly fourteen keys, boolean presence, positive nonempty spans, and
null spans for negatives. The harness resolves eligible near-exact spans to the
source text under `nfc-casefold-whitespace-quotes-dashes`; successes record
ordinary normalized components in `resolved_spans` and ellipsis-covered components
in `joined_spans`. Missing reported model, non-stop finish, invalid JSON/schema or
spans not found under that closed rule are failures. Metadata uses
`labels_version: AF3a-v3` and the ellipsis-cover rule identifier, so an AF3a-v2
journal fails the existing configuration check.

An append-only JSONL journal flushes and `fsync`s each started attempt and its
success/failure immediately. A nonblocking POSIX file lock prevents concurrent
writers. Resume skips successes and respects the total attempt limit, including
interrupted requests. It records an interrupted reserved attempt as a failure;
there can be at most one repeated request per interrupted in-flight operation,
within the same total attempt budget. Only an unterminated tail is discarded on
recovery; malformed complete lines fail loudly. Changed endpoint/model/settings/
template/schema are refused in an existing journal: choose another output file.

Every event retains requested model, endpoint-reported model (null until known),
request settings, timeout/retry policy and SHA-256 of the canonical system template, user context wrapper
and response schema, alongside source IDs and provisional evidence metadata.
Raw invalid replies and exception messages are not persisted, because they can
echo source text. Failed texts remain failures, not fourteen absent labels.
This harness uses the Python standard library; POSIX locking targets Linux/macOS.
All real model calls belong to the subsequent GPU run, not AF3a.

## Agreement and validation

[agreement.py](agreement.py) uses each text's last journal event and excludes
failed/missing predictions while reporting their count against the full gold
size. It reports TP/FP/FN/TN, compared N, precision, recall, accuracy and Cohen's
kappa for each component, pooled micro counts and unweighted macro metrics.
Undefined ratios and degenerate kappa are null, never automatically perfect.
There are no prevalence weights, confidence intervals or span-overlap scores;
presence agreement is descriptive over the paired texts, with film/creator and
repeated-passage dependence. Exact span validity is a separate source check.

```bash
uv run python prompt-labels/build.py
uv run python prompt-labels/gold.py
uv run python prompt-labels/checks.py
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/check_repository.py
```

`checks.py` verifies all 5,000 source hashes and the 12,000-character limit,
all 300 gold texts and 4,200 decisions, sample membership, full-field-span
exclusion and film coverage. It compares gold with itself and with a copy in
which all 300 subject decisions are deliberately inverted. Committed smoke
outputs: [self](outputs/agreement_self.json), [perturbed](outputs/agreement_perturbed.json).
Self micro precision/recall/kappa are 1; perturbed micro kappa is 0.836441,
accuracy 3,900/4,200. These are software checks, not real model agreement.
The tests exercise only synthetic prompts and a loopback stub, including HTTP,
invalid output, retry exhaustion, interruption/resume, truncated-tail recovery,
configuration mismatch, model/settings/template metadata and known kappa counts.

For an independent source rebuild (all 28 source checksums verified first):

```bash
uv run python scripts/fetch_data.py --output data/af3a-fresh
uv run python prompt-labels/build.py --data data/af3a-fresh --output data/af3a-rebuilt-small --large data/af3a-rebuilt
diff -r prompt-labels/outputs/build.json data/af3a-rebuilt-small/build.json
diff data/prompt-labels-v1/SHA256SUMS data/af3a-rebuilt/SHA256SUMS
```

## Public outputs and handoff

Large outputs are assets of the public [prompt-labels-v1 release](https://github.com/TelesforoAleix/ai-film-practice/releases/tag/prompt-labels-v1):
`features.parquet`, `occurrences.parquet`, `sample.jsonl.gz`, and `SHA256SUMS`.
They contain no full prompt texts. The source texts remain retrievable from the
separate original snapshot. Summaries, strata, build counts, gold selection and
gold annotations are small committed files here. No `data/` exception was added.

The later slice needs the selected model and its literal reported identity,
unchanged definitions/template hash, complete success/failure ledger, tokenizer
and context settings, agreement against this limited gold, and review of semantic
errors by component, length, film and operation/role. It must publish failures,
long-text exclusions and gold coverage limits with any labels. Study 04 still
owns attached-context joins, the information-location matrix, patterns by task/
model/cohort, traced examples, counterexamples and studio proposals under the
programme's full output contract. Nothing here verifies media contents, resolves
hidden instructions or turns shared wording into a tested practice.

## AF3c: Jev presence cross-check

`jev.py` is a secondary, presence-only cross-check using TypeSafe's hosted Jev
System One API. It asks the same fourteen inclusion/exclusion definitions as
AF3a in one request per text. Jev returns a choice, probability distribution
and confidence, but no supporting spans; it cannot replace AF3a span evidence.
The request treats the sampled text as untrusted input. The API key is read from
`TYPESAFE_API_KEY` and is never recorded. The append-only journal reserves each
attempt before requesting, resumes by `text_id`, and refuses a changed model,
endpoint or question set. Three HTTP retries for rate limits and server errors
are made inside each attempt; `--max-attempts` bounds attempts per text.

```bash
uv run python prompt-labels/jev.py --sample data/af3a-release-download/sample.jsonl.gz --data data --output data/af3c-jev.jsonl
uv run python prompt-labels/crosscheck.py --harness data/af3a-labels.jsonl --jev data/af3c-jev.jsonl --gold prompt-labels/outputs/gold.jsonl --output data/af3c-crosscheck.json
```

The client reads plain or gzip-compressed JSONL samples. `crosscheck.py` compares successful rows by `text_id`,
reports both-present/both-absent/disagreement counts, accuracy, Cohen's kappa,
and missing IDs per component and micro. Optional gold produces additional
descriptive comparisons. The JSON output lists disagreement IDs; it applies no
weights or intervals and does not resolve disagreements. These are agreement
descriptions, not evidence that either label is correct.
