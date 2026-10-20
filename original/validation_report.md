# Validation report

Generated: 2026-10-20T07:15:35.925395+00:00.

| Metric | Count |
| --- | ---: |
| Unique films in index | 6,224 |
| Priority films | 186 |
| Distinct generations | 130,899 |
| Generations with a nonempty primary prompt | 124,642 |
| Distinct nonempty primary prompt strings | 61,479 |
| Prompt/text fields, including nested fields | 161,836 |
| Folders | 3,246 |
| Asset entities, including index covers and final films | 163,184 |
| Generation-to-asset usage rows | 469,242 |
| Reference elements exposed in generation parameters | 5,223 |
| Generation records with model identifiers | 130,899 |

## Catalog completeness

The submissions endpoint reported 6,258 rows. All 63 pages were consumed until `next_cursor=null`. Exactly 6,258 rows were received; 34 publication IDs each appeared twice, leaving 6,224 unique films. See `catalog_duplicates.csv` for both occurrences. The 126 Audience Choice records and 46 Create in Public shortlist records were also fully paginated and are subsets of the submissions union. The dedicated Higgsfield Choice list returned zero records. This does not mean that no UI cards carry a Higgsfield Picks badge: the UI also derives that badge from voting eligibility.

## Agreed detailed scope

The user selected the union of the 126 shortlisted films and the first 100 records of the public most-watched feed. Their overlap is 40, so the priority set has 186 films. The most-watched feed covers 4,555 open projects, not every private/legacy listing. Rankings and counts are snapshots, not a permanent ranking or a quality score.

Of the priority set, 23 listings are marked non-open-source and are excluded from detailed collection and export. The remaining public priority set is 163 films. Statuses: 157 complete public workspace crawls; 0 partial crawls; 6 unavailable workspaces; 0 pending. Cosmic tracks is an additional, separately identified pilot case outside this set.

## Generation and relationship checks

CSV integrity checks passed: True. Primary-prompt fields, including explicitly empty strings, verified exactly: 125,725. Duplicate keys, JSON validity and foreign keys are checked in `csv_validation.json`.

- Generation source URLs from request logs: 126,729; generation rows whose URLs were reconstructed from saved pagination: 4,170. The latter retain raw source records, but missing original retrieval times are not invented. See `reconstructed_provenance.json`.
- Each generation is unique by `(film_id, generation_id)`. Repeated folder placements are exported separately; 85,753 repeated generation placements were collapsed.
- Each asset is unique by `(film_id, asset_id)`. An entity can have more than one role. Usage-specific roles are in `asset_usages.csv`.
- Relationship issues found: 0. The exact records are in `relationship_issues.json`; no placeholder parents are fabricated.
- Public projects with a completed item crawl whose distinct generation count differs from the project summary: 0. See the machine-readable validation file and per-film extraction log.
- Explicitly empty primary prompts: 1,083; these are preserved but excluded from the nonempty-prompt totals.
- Main prompts are exported exactly as stored. Nested prompt/text fields retain source paths. The longest primary prompt is 59,522 characters. `prompt_integrity.jsonl` contains source-text hashes for round-trip verification.
- The four browser-inspected generation prompts were matched to exported records: 4 of 4. Browser reference labels can differ from stored identifier tokens; no replacement is made in exported prompts.

## Resource and brief coverage

Direct-folder recovery completed for 158 workspaces, with 0 workspaces reporting recovery errors. Retained decoded briefs: 119. The extraction log records item/folder completeness and brief availability separately.

## Known limits

The generic reference-element listing endpoint returned HTTP 401, so it was not used. Reference elements explicitly disclosed inside generation parameters remain available. Some publicly visible item totals do not equal root recursive response rows, including Cosmic tracks (255 versus 231) and Don't Poison Ivy (608 versus 604). Direct-folder recovery supplements uploads and placements omitted by recursive responses. These rows are deduplicated by source entity keys; UI counters are not assumed to count the same grain. Their distinct generation counts reconcile. Public snapshot histories need not include every tool, external edit, rejected idea or offline production step.

Further brief-snapshot retrieval was also blocked by automatic approval review because it may expose hidden prompt content. Retrieval is disabled, encoded snapshots are omitted, and explicitly hidden values are redacted from retained decoded documents. Brief completeness is independent of workspace item/folder completeness.

A metadata request for a listing marked non-open-source was rejected by automatic approval review because it could expose private project data. There was no retry or workaround of that request. Non-open-source production payloads are excluded from the delivered archive and CSVs; their public catalog records remain in the index.
