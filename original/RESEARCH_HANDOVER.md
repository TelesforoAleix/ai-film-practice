# Higgsfield Global Film Festival — research handover

## Executive summary

The live catalog was enumerated through its public interface and the structured endpoints used by that interface. The archive contains a 6,224-film deduplicated index from 6,258 returned submission rows. Following the user's scope choice, detailed extraction targets 186 films: the 126 shortlisted entries union the top 100 most watched, with 40 overlaps. Twenty-three non-open-source workspaces are excluded from detailed collection. Cosmic tracks is an additional technical pilot.

The normalized export contains 130,899 distinct generation records, 124,642 with nonempty primary prompts, 3,246 folders and 163,184 asset entities. The asset total includes covers and final films from the full index; it must not be interpreted as the number of production assets in the priority cohort. Source URLs, raw responses, retrieval provenance and resumable scripts are included. Current priority statuses: 157 complete public workspace crawls, 0 partial, 6 unavailable, 23 excluded and 0 pending. Consult the validation report before treating any portion as complete.

## Festival overview

Official source: https://higgsfield.ai/contests/higgsfield-global-film-festival

The live page contains General, Timeline, Rules and Submissions. Submissions has All submissions and Shortlist views, a search box and personal Default/Liked/Voted filters. At browser inspection, voting was closed, jury review was in progress, and the page said winners would be announced in the last week of October. That page-state statement is dated to the inspection, not asserted as a later announcement.

The public shortlist list has 126 records, including 46 in the Create in Public shortlist. The other shortlisted cards receive a Higgsfield Picks label through the UI's eligibility fallback; the separate explicit Higgsfield Choice list returned no records. The dataset records this provenance rather than treating all those labels as explicit `higgsfield_choice` list membership. The most-watched feed has 4,555 open projects; only its first 100 were used for the agreed popularity cohort.

| Export metric | Count |
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

## Four case studies

The full case studies and folder structures are in `reports/four_film_case_studies.md`. The inspected cases are Cosmic tracks, The Kiss, Fallen Leaves, and Don't Poison Ivy. Their distinct generation counts reconcile with the visible/source summaries (195, 391, 356 and 553 respectively). Cosmic tracks is a supplemental pilot outside the priority union.

### Cosmic tracks

- Project: https://higgsfield.ai/@ahmed_atef/projects/cosmic-tracks
- Creator: ahmed_atef
- Approach: A multi-world fantasy with character continuity and deliberately different environments.
- Export: 195 distinct generations, 193 generation records with a nonempty primary prompt, 16 folders and 239 asset entities.
- Models observed: Nano Banana 2, Seedance 2.0, Gemini Omni Flash 1.1, Seedance 2.5, Nano Banana Pro, Soul Cinematic, FLUX.2, GPT Image 2.0, Cinematic Studio Soul Location, GPT Image 2.5, Seedream 4.5, Voiceover.

The brief specifies contemporary realism, a 1930s speakeasy, a neon city and an ancient world. The visible organization separates Main character and Scene 1–4, with nested resources. The model stack is broad. The inspected poster prompt explicitly separates subject, environment, world regions, lighting, composition and style.

**Manual cross-check.** Browser: 6:18, 195 generations, All assets 255; poster generation Nano Banana 2, 2k, 3168×1344. The API returns 231 recursive item rows and 195 unique generation IDs. A direct-folder recovery pass adds uploads and placements omitted by the recursive response; the generation count reconciles.

**Public folder structure.**

- /Cosmic tracks
- /Cosmic tracks/All assets
- /Cosmic tracks/Main character
- /Cosmic tracks/Main character/Assets
- /Cosmic tracks/Scene 1
- /Cosmic tracks/Scene 1/S1 Assets
- /Cosmic tracks/Scene 1/Videos
- /Cosmic tracks/Scene 2
- /Cosmic tracks/Scene 2/S2 Assets
- /Cosmic tracks/Scene 2/Videos
- /Cosmic tracks/Scene 3
- /Cosmic tracks/Scene 3/S3 Assets
- /Cosmic tracks/Scene 3/Videos
- /Cosmic tracks/Scene 4
- /Cosmic tracks/Scene 4/videos
- /Cosmic tracks/Watermarks

**Qualification.** This case is retained as a supplemental pilot outside the selected/popular 186-film set.

### The Kiss

- Project: https://higgsfield.ai/@seifhussam/projects/the-kiss
- Creator: seifhussam
- Approach: A character-driven jealousy narrative combining a candy-game world with spatial references.
- Export: 391 distinct generations, 383 generation records with a nonempty primary prompt, 13 folders and 429 asset entities.
- Models observed: Seedream 5.0 Pro, Nano Banana Pro, Seedance 2.5, Cinematic Video Editor, Cinema Studio 4.0, GPT Image 2.0, Soul Cinema Studio, Higgsfield Soul V2, Seedream 4.5, Soul Cinematic, Seedance 2.0.

The project separates Characters, Locations, Props, Editing, Sound, Scene folders, Test_Images and Test_Videos. The observed location prompt uses a 3D layout/blockout, named scene objects and a world-style reference. Several brief headings retain generic template placeholder text; their presence does not establish that the corresponding production planning was completed.

**Manual cross-check.** Browser: 3:46, 391 generations, All assets 393. The inspected image uses Seedream 5.0 Pro, 2k, 2720×1536. API: 393 item rows and 391 unique generations.

**Public folder structure.**

- /AI Film Festival
- /AI Film Festival/Characters
- /AI Film Festival/Editing
- /AI Film Festival/Locations
- /AI Film Festival/Props
- /AI Film Festival/Scene_01
- /AI Film Festival/Scene_02
- /AI Film Festival/Scene_03
- /AI Film Festival/Scene_05
- /AI Film Festival/Sound
- /AI Film Festival/Test_Images
- /AI Film Festival/Test_Videos
- /AI Film Festival/Watermarks

**Qualification.** The initial UI prompt substitutes human-readable reference labels for raw reference tokens; raw token text is preserved in the dataset.

### Fallen Leaves

- Project: https://higgsfield.ai/@jacob_everett/projects/fallen-leaves
- Creator: jacob_everett
- Approach: A naturalistic historical short with a relatively flat project organization.
- Export: 356 distinct generations, 356 generation records with a nonempty primary prompt, 2 folders and 369 asset entities.
- Models observed: Seedance 2.5, GPT Image 2.0, Seedance 2.0.

The brief describes a Sengoku-period setting, naturalistic camera movement, winter lighting and film emulation. The public folder panel has All assets and Watermarks rather than a detailed scene hierarchy. The inspected reference-sheet prompt specifies geography, supporting angles, textures and an explicit Avoid section. An embedded title-card prompt is preserved in the raw brief document.

**Manual cross-check.** Browser: 5:39, 356 generations, All assets 357. Inspected location-sheet image: GPT Image 2, High quality, 2688×1520. API: 357 item rows and 356 unique generations.

**Public folder structure.**

- /Fallen Leaves
- /Fallen Leaves/Watermarks

**Qualification.** Its visible production history is dominated by Seedance 2.5, in contrast with the broader stack of Cosmic tracks.

### Don't Poison Ivy

- Project: https://higgsfield.ai/@joeysnoisygroup/projects/don-t-poison-ivy
- Creator: joeysnoisygroup
- Approach: A stylized, dialogue-free animated film with a handmade visual aesthetic.
- Export: 553 distinct generations, 552 generation records with a nonempty primary prompt, 27 folders and 725 asset entities.
- Models observed: Seedance 2.5, Nano Banana Pro, Cinematic Video Editor, Seedream 5.0 Pro.

The brief describes character sheets in Nano Banana Pro, scene plates in Seedream 5.0 Pro and video in Seedance 2.5. Folders separate Characters, Locations, Props, Score and Video Generations, with nested folders. The brief describes exaggerated character features, detailed clothing and deliberate color/surface rules. An observed short edit prompt changes only paint on a pot, illustrating a local revision rather than a fresh scene description.

**Manual cross-check.** Browser: 15:38, 553 generations, All assets 608. Inspected pot edit: Nano Banana Pro, 4k, 5504×3072; generation author bydany differs from project owner joeysnoisygroup. API: 604 recursive item rows and 553 unique generations.

**Public folder structure.**

- /Don't Poison Ivy
- /Don't Poison Ivy/Characters
- /Don't Poison Ivy/Characters/Daughter
- /Don't Poison Ivy/Characters/Extras
- /Don't Poison Ivy/Characters/Mom
- /Don't Poison Ivy/Characters/Outfits
- /Don't Poison Ivy/Locations
- /Don't Poison Ivy/Locations/Bedrooms
- /Don't Poison Ivy/Locations/City
- /Don't Poison Ivy/Locations/Elementary School
- /Don't Poison Ivy/Locations/Grocery store
- /Don't Poison Ivy/Locations/Home Exterior
- /Don't Poison Ivy/Locations/Home Interior
- /Don't Poison Ivy/Props
- /Don't Poison Ivy/Score
- /Don't Poison Ivy/Video Generations
- /Don't Poison Ivy/Video Generations/Act 1: Town Intro
- /Don't Poison Ivy/Video Generations/Act 2: Privilege
- /Don't Poison Ivy/Video Generations/Act 3: Art Secret
- /Don't Poison Ivy/Video Generations/Act 4: The Break
- /Don't Poison Ivy/Video Generations/Act 5: The Coda
- /Don't Poison Ivy/Video Generations/Bloopers
- /Don't Poison Ivy/Video Generations/Misc BROLL
- /Don't Poison Ivy/Video Generations/Potential Replacement Scenes
- /Don't Poison Ivy/Video Generations/Trailer
- /Don't Poison Ivy/Video Generations/Transitional Scenes
- /Don't Poison Ivy/Watermarks

**Qualification.** Root recursive response rows and UI totals have different counting behavior. Direct-folder recovery supplements the exported resource placements; generation totals reconcile.
## Technical extraction methodology

The signed-out cloud browser was used to inspect the live festival, switch All submissions/Shortlist, scroll lazy-loaded cards, open film previews and canonical projects, expand the model stack, inspect folders, and open individual generation showcases. The visible cards are lazily rendered and replaced with placeholders outside the active range, so DOM card counts alone are not a reliable total.

Public client JavaScript identified the same endpoints used by the interface. Browser titles, authors, durations, model summaries, folder structures and generation prompts were cross-checked against returned structured data. `reports/data_model_validation.md` distinguishes observed interface fields from additional structured fields and documents the validated entity relationships. No authentication token, paid API, third-party scraping service or media download was used.

Public endpoints used:

- `https://fnf-api-gw.higgsfield.ai/fnf/contest-participations/publications?tab=submissions&contest_key=ai_film_festival&size=100`, following the returned `next_cursor`.
- `/contest-participations/lists/audience_choice`, `/lists/top_50` and `/lists/higgsfield_choice`, following `next_cursor` to termination.
- `/contest-participations/publications?tab=most_watched&contest_key=ai_film_festival&size=100` for the chosen popularity cohort.
- `/project-publications/<publication_id>` for open project metadata and exact source model-count summaries.
- `/folders/<published_snapshot_id>/items/v2?size=100&include_subfolders=true`, following the returned `cursor` until null. This retrieves the recursive All assets data without assuming that the first 100 rows are complete.
- `/folders/<id>?include_folders_count=true` and `/folders/<id>/children?size=100`, recursively following source-returned child identifiers and cursors. Empty folders are retained.
- Previously collected brief documents were decoded with Yjs 13.6.33. Automatic approval review subsequently blocked further snapshot retrieval because these documents can contain hidden prompt content. Retrieval is disabled in the supplied extractor. Explicitly hidden prompt values are removed from retained decoded JSON; all encoded snapshots are omitted. `reports/visibility_redactions.json` records the exclusions. Some public project briefs therefore remain unavailable.
- Direct-folder `/folders/<id>/items/v2?size=100&include_subfolders=false` pagination supplements resource placements when folder counts exceed recursive results, and checks nonempty internal folders. Recovery status/errors are recorded per film.

The scripts cache each response, retry transient failures up to three times, stop on authentication/access errors for that route, detect repeated cursors, checkpoint each film, and use a global maximum of two new API requests per second in the current extractor. Existing responses are reused on resume. A failed route is recorded rather than bypassed. Source JSON is retained unchanged except for documented visibility redactions and encoded-snapshot omissions. These records permit future changes to the normalization without re-requesting the site.

The reproducibility scripts reconstruct the captured corpus from public responses. A fresh rerun can differ because publications, lists, labels, view counts and public availability change. The saved raw archive is the authoritative snapshot for this handover.

## Dataset documentation

All CSVs use UTF-8 and standard quoted CSV escaping. `\N` means unavailable/not disclosed; an empty string remains an explicitly empty string. Arrays and objects are compact JSON strings. Prompt text is not shortened, rewritten or limited to Excel cell sizes. Dates from generation epochs are converted to UTC ISO 8601; server-supplied timestamps retain their original timezone information. Durations are seconds.

| File | Grain and keys | Important fields |
| --- | --- | --- |
| `films.csv` | One film; `film_id` is the source publication UUID | Public metadata, creator/profile, canonical project URL when exposed, final-film/cover URLs, submission date, brief, source-reported model stack, selection, popularity and extraction status. |
| `priority_films.csv` | The 186-film chosen scope | Same fields as films, ordered by available views. `most_watched_rank_top100` is the original feed rank and is missing outside that first page. |
| `folders.csv` | One `(film_id, folder_id)` | Parent UUID, human-readable derived folder path, original UUID path, source item/subfolder counts. Root folders are explicitly labeled. |
| `generations.csv` | One `(film_id, generation_id)` | Job UUID; job-set batch UUID; media type; exact primary/negative prompt; complete parameters JSON; raw model identifier, display model name, creation date, author and provenance. |
| `assets.csv` | One `(film_id, asset_id)` | Generated output, uploaded asset, reference, cover or final film. Missing source IDs use a documented `url-sha256:` identifier derived from the exact URL. `generation_id` identifies a known producer; no output is invented for failed jobs without a URL. |
| `model_usage.csv` | One model in a source project summary | Source counts retained as counts; percentage calculated as count/reported generation count. Provider remains missing when undisclosed. These are not counts reverse-engineered from rounded UI percentages. |
| `extraction_log.csv` | One film | Status, discovered counts, source-reported generations, count reconciliation, missing fields, errors and completion flags. Outside-scope films are index-only. |
| `asset_usages.csv` | One generation/asset/role/source-path occurrence | Inputs, references and outputs, including the actually used URL/metadata, explicit parameter roles and reference-element IDs. Join this table to assets and generations on compound film/asset or film/generation keys. |
| `asset_folders.csv` | One asset placement per folder | Retains uploaded and generated asset placements without duplicating asset entities. |
| `generation_folders.csv` | One generation placement per folder | Keeps many-to-many folder organization without duplicating the generation. Folder-job UUID is retained when exposed. |
| `reference_elements.csv` | One reference element per film | Names, categories, descriptions and media metadata explicitly disclosed inside generation parameters. This is not a claim to have enumerated the authenticated element library. |
| `other_items.csv` | One otherwise unmapped source item per film/content hash | Preserves any unrecognized public item type and its exact metadata without inventing an asset or generation classification. |
| `brief_assets.csv` | One rich-brief asset embedding per film/document path | Embedded reference IDs, URLs, visible prompts and attributes; explicitly hidden prompt values are redacted. Synthetic embedding IDs hash the document path, not an invented source object. |
| `generation_prompts.csv` | One generation/text-field path | Full nested prompt/text values, including multi-shot fields and negative prompts. `prompt_or_text` includes model script/brief/text fields; use the source path to select the intended concept. |

The primary prompt prefers a string `params.prompt`, then `creative_direction`, `brief`, `script` or `text`; `prompt_source_path` records which. A missing primary prompt can coexist with nested text fields. `production_notes` remains missing when there is no separately exposed field; relevant prose is retained in the project brief. The retained, visibility-sanitized rich document, including embedded asset references or visible prompts omitted by plain-text flattening, is available in `raw/projects/<film_id>/brief.json`.

`source_url` and `source_record_file` on film rows identify the original paginated catalog response; `project_metadata_source_url` identifies additional public project metadata where collected. `source_url` on generation rows identifies the public item-page endpoint for its saved response; `source_record_file` locates its raw JSON in the archive. `source_provenance_method` distinguishes request-log URLs from URLs reconstructed from saved snapshot identifiers and the previous response cursor. Reconstructed URLs and missing retrieval times are explicitly documented in `reports/reconstructed_provenance.json`; no retrieval timestamp is invented. `generation_id` is an individual job/output identifier; `generation_batch_id` is its source job-set identifier. Treat provider and version labels literally: no provider is inferred from a product nickname. Shared generation/asset IDs can recur across films, so use compound keys.

`raw/catalog` retains listing pages and the top-100 most-watched response. `raw/projects` retains publication metadata, recursive item pages, folder responses and visibility-sanitized decoded briefs. `raw/requests.jsonl` records source URLs and successful retrieval times. Media binaries are not included. URLs are retained as supplied and have not been bulk-downloaded or individually HTTP-tested.

## Extraction quality

See `reports/validation_report.md`, `reports/validation_counts.json`, `reports/csv_validation.json`, `reports/browser_cross_checks.json`, `reports/catalog_duplicates.csv` and `data/extraction_log.csv` for exact counts, failures, reconciliation and integrity checks. Completed item and folder pagination does not imply access to private histories or an authenticated reference-element library.

## Initial observations and future analysis

**Observed:** Individual prompts range from short local edits to long, sectioned descriptions. Some prompts explicitly name subjects, lighting, materials, camera behavior, continuity and exclusions. Input/reference records distinguish textual references from actual attached media. Folder structures vary from nearly flat asset collections to nested character, location and scene organization. A project owner and a generation author can differ. Some brief sections retain template text.

**Next analysis:**

1. Compare prompt length, sections, camera/motion instructions, continuity language and negative constraints, separating image, video and spoken-text generation. Sample nested multi-shot prompts separately from primary prompts.
2. Compare project organization using actual folder paths and generation placements, controlling for project size and avoiding duplicated generation counts.
3. Build an asset-reuse graph from explicit asset IDs and usage roles. Distinguish references whose producers are in the captured corpus from external references; do not infer lineage from visual similarity or filenames alone.
4. Compare image-to-video, text-to-video and video-reference workflows using explicit input roles and output types. Treat unavailable roles as missing, rather than assuming text-only generation.
5. Compare prompting and reference strategies by the literal model identifier and source label. Do not confuse summary percentages with direct generation counts or assume all naming versions are equivalent.
6. Compare the editorial-selected cohort with highly viewed films, accounting for overlap, publication date, exposure and unavailable/non-open-source entries. Views and likes measure observed engagement, not production quality or a causal effect of model choice.

**Hypotheses, not findings:** More structured prompts may aid continuity; reusable reference elements may reduce repeated character descriptions; scene-based folders may be associated with longer films. These require downstream coding and testing. No statistical or causal conclusions are made in this collection report.

## Extract the archive

The two largest CSV tables use LZMA compression inside the ZIP to fit the download size limit. Python 3 supports every archive member. Extract with:

```bash
python3 -m zipfile -e higgsfield_festival_research.zip higgsfield_extracted
```

The standalone `generations.csv.gz` download decompresses to the same plain generation CSV included in the ZIP.
