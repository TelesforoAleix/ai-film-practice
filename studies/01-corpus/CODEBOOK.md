# Shared codebook, version 1.0

The 49 operational codes are in [outputs/codebook.csv](outputs/codebook.csv),
with stable IDs, target study, allowed values, inclusion rules and exclusions.
[codebook_source.py](codebook_source.py) is the human-authored source. A code can
have several values. Apply it to a named excerpt, entity, edge or family, not to an
entire film by default. Codes describe technical instructions and records; they
never judge the story, aesthetics, achieved appearance or media quality.

## Coding protocol

1. Open only the published release via `connect`. Establish film population and
   coverage first. Read each panel film once across Studies 02–10; preserve literal
   model identifiers, original parameter semantics and source paths.
2. Separate the unit: film/brief section, text-field path, generation, batch, asset,
   reference element, folder placement, explicit edge or candidate iteration family.
   Use film/entity compound keys throughout. The table grains are in
   [outputs/grains.json](outputs/grains.json).
3. Record `coded`, `unknown`, `empty`, `not_applicable` or `not_observed_in_scope`.
   Unknown means evidence cannot decide. Empty means the exported value/collection
   is explicitly empty. Not applicable needs a stated reason. Not observed needs
   the exhaustive inspected scope and denominator; sample absence is always unknown.
4. For each code record study, codebook version, film ID, entity IDs, field path,
   short exact excerpt, assigned values, evidence label, competing explanation,
   denominator and confidence rationale. Retain unavailable values as null, never
   empty text. Excerpts must come from the published redacted source. Do not copy
   full prompts into committed outputs. The source text remains retrievable by ID.
5. Distinguish **observed** fields/relationships, **creator-stated** brief claims,
   **inferred** interpretations, **associated** measured relationships,
   **experimentally supported** results and **proposed** studio behaviour.
   A folder label is observed; its inferred organisational meaning needs a separate
   claim. No controlled experiments or causal claims occur in Study 01.
6. Use explicit usage/producer links before names, dates or proximity. Missing
   input records never establish text-only generation. Deduplicate occurrence
   rows and audit raw/preview aliases before graph degree or reuse claims.
7. Preserve both the request and the mechanism: an edit instruction is not a mask;
   a sheet instruction is not a verified sheet; multi-shot text is separate from
   an enabled control; an authoritative frame instruction is scoped to that task.
8. Mark ambiguous codes unknown and log the competing interpretations. Revisions
   to definitions need a version and reapplication to previously coded records.
   A second coder can adjudicate; none was available for this calibration.

## Calibration scope and revisions

[calibration.py](calibration.py) contains manual assignments for the four existing
cases, checked against the published fields on each run. All 49 codes are applied
to each film (196 assignments). Unknown entries are deliberate boundaries of the
sample, not film-wide negative labels. The evidence ledger includes the technical
brief excerpt, folder register, three disclosed reference records, selected image
and video prompts/controls/usages, one shared-input candidate family and one
explicit cross-model producer/input edge per film. Cosmic tracks is supplemental.

The assignments contain 134 coded values and 62 unknowns: Ivy 33/16,
The Kiss 31/18, Fallen Leaves 33/16 and Cosmic tracks 37/12 (coded/unknown,
49 each). The row-level unknown notes are the record of missing calibration
evidence; none is a film-wide absence claim.

These are **calibration notes, not full case files**. Prompt excerpts are short;
full source fields stay in the release. The sample deliberately includes short
edits, long shot instructions, a reference-sheet request, template brief sections,
a flat folder register and external editing statements. It is purposive and has
no population-level agreement or accuracy estimate. Semantic prompt labels at
scale are a later slice with stratified sampling and a hand-labelled gold subset.

| Revision from draft 0.1 to 1.0 | Calibration evidence | Decision |
| --- | --- | --- |
| “Brief present” was too broad for planning | The Kiss:B: generic Production section alongside substantive Context | Code sections; mixed template brief does not establish a production plan (02.6). |
| “Reference sheet” conflated request and attached output | Fallen_Leaves:I: location sheet request; Cosmic_tracks:X: three-view request; Ivy:B: creator statement | Keep requested, creator-stated and attached package evidence distinct (03.3, 05.5). Generic sheet has its own value; do not infer multi-angle from “sheet”. |
| “Edit” implied a mechanism | Ivy:I and Cosmic_tracks:I have explicit `is_inpaint=false`; The_Kiss:I has no disclosed mechanism | Code local-edit request and mechanism independently (05.1, 05.4). |
| Multi-shot wording was conflated with control activation | Ivy:X says two shots while `multi_shots=false` | Code request and literal controls separately (02.3, 06.1, 06.6); scopes may differ, so this alone is not a proven conflict. |
| Media attachment was treated as property content | Every calibration input ledger | Code content unknown while retaining explicit text/metadata (03.4, 04.4). No media was watched. |
| Reference authority was conflated with project canonical approval | Cosmic_tracks:V makes the start frame authoritative for one sequence | Scope the declaration to that task (03.6); no global canonical-library claim. |
| Batch identifier was assumed to identify several alternatives | Selected records have batch IDs, but shared batch membership is not guaranteed | Require actual membership; use observed shared inputs only as candidate families (09.1). |
| Downstream adoption was read as acceptance | Each film:E: explicit asset producer/consumer edge | Record further-work reuse, not final acceptance (09.4). |
| Flat folders implied no element strategy | Fallen_Leaves:F versus R and the full metric row (10 disclosed elements) | Organisation and reference disclosure are independent dimensions (10.1, 03.1). |
| Missing graph/version evidence was coded absent | All four samples leave some 03/07/09 codes unresolved | Use unknown pending the complete case file; no invented upstream results. |

Remaining ambiguity: semantic entity categories, iteration-family equivalence,
alias collapsing, version intent, and actual build order require deeper case-file
coding. Each later session should retain this log and add disagreements rather
than silently treating the calibration as an exhaustive film analysis.
