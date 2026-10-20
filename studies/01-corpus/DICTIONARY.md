# Data dictionary and derived typing

[outputs/dictionary.csv](outputs/dictionary.csv) inventories every column of all
14 tables: proposed derived type, row denominator, unavailable/null count,
explicit empty-string count, invalid parse count and key membership.
[outputs/grains.json](outputs/grains.json) gives each table's grain/key and checks
its distinct count against its row count. [outputs/json_paths.csv](outputs/json_paths.csv)
lists the observed paths and JSON types, including null and empty strings. Array
indices are normalized to `[*]`: occurrences count array children; documents count
rows containing that path/type at least once; table_rows includes missing documents.
The path inventory is structural and contains no prompt or profile values.

## Column semantics and join rules

| Table | Grain and interpretation |
| --- | --- |
| films | Catalogue publication; film_id. Selection/popularity fields are snapshot context, duration is declared seconds, category/shortlist_status are JSON lists. project_brief is visible flattened text, not the unavailable decoded document. authors_json and model_usage_summary are source summaries, not inferred labour/cost measures. |
| priority_films | The 186-row subset, same column meanings as films. Validate cohort membership from shortlist_status audience_choice and presence of most_watched_rank_top100. editorial_selection is a separate source label, not another union. |
| folders | (film_id, folder_id); parent_folder_id joins within film. folder_path is a derived human-readable path, source_folder_path retains source UUID path. Counts are source-reported item/subfolder counts, not distinct generation counts. |
| generations | (film_id, generation_id); generation_batch_id is a batch identifier, not necessarily a multi-job family. model_identifier and model_name remain literal, provider remains undisclosed if null. prompt_source_path identifies the primary field; parameters_json retains raw model semantics. created_at is an event, not elapsed labour. Source-record paths refer to unavailable collection responses. |
| generation_prompts | (film_id, generation_id, field_path); prompt_role and field_path distinguish primary, negative, shot, script and other text. A primary prompt duplicated here is one source text field, not an independent prompt. |
| assets | (film_id, asset_id); generation_id is a known producer where exposed. source_asset_id is distinct from fallback URL-hash IDs. Includes catalogue covers/final films outside the detailed cohort. metadata_json is descriptive, not verified media content. |
| asset_usages | (film_id, generation_id, asset_id, asset_role, parameter_path) is unique in this snapshot. It is an occurrence key, not a universal API guarantee. Join film/generation and film/asset; reference_element_id joins film/reference element. input_* and reference_* roles are inputs, output is an output. parameter_role/path preserve the model-specific input role. |
| asset_folders | (film_id, asset_id, folder_id), an asset placement, not another asset. |
| generation_folders | (film_id, generation_id, folder_id), a generation placement. folder_job_id retains the source placement ID; it is not the generation ID. |
| reference_elements | (film_id, reference_element_id); literal name/category/description and metadata disclosed in parameters. **category here is VARCHAR**, unlike catalogue category JSON. This does not enumerate an authenticated library. |
| brief_assets | (film_id, embedding_id); document_path identifies a sanitized embedding. reference_id/reference_kind/media_kind are separate from asset IDs and roles; no implicit cross-table identity. prompt_hidden flags visibility; no hidden value is reconstructed. |
| model_usage | (film_id, model_identifier) is unique here; source summary counts/percentages remain separate from direct job counts. Providers are not inferred. |
| extraction_log | film_id; explicit collection completeness, source reconciliation, brief completeness, errors and recovery flags. Index-only is not an empty workspace. Missing brief_complete is unavailable, not false. |
| other_items | (film_id, record_hash), preserved unknown source item grain. Zero rows; column types are provisional VARCHAR/JSON by schema, not inferred from nonexistent values. |

IDs, names, URLs, paths, statuses and free text are VARCHAR. Named counts/ranks are
BIGINT, durations/usage percentages DOUBLE, explicit flags BOOLEAN and timestamps
TIMESTAMPTZ. The inventory declares the mapping per column; no numeric inference
from identifier shape is allowed. JSON fields are validated before use. JSON-path
absence, JSON null, empty string, empty object/array and false remain different
states. Empty array/object is visible as a container path without children; a
missing child cannot be counted as an explicitly empty child.

## Optional typed layer and parse defects

`typed.add_typed_views(db, Path("studies/01-corpus/outputs/dictionary.csv"))` adds
`typed_<table>` temporary views beside the original string views. Import typed
from this study directory. Every field gains `__empty` and `__invalid` flags;
non-text empty values and failed casts become null only in the typed projection.
VARCHAR keeps empty text. A raw null yields a null empty flag; the original view
is always the authority for unavailable/empty distinctions. `connect("data")`
is unchanged and no typed view is added implicitly.

Nine parameters_json strings, all in one film, fail JSON parsing in the published
release. [outputs/invalid_json.csv](outputs/invalid_json.csv) gives the compound
keys and retained provenance paths. These strings are never repaired; JSON-only
derivations are unavailable for those nine jobs. Independently exported fields
and relationships remain usable. No other declared scalar or JSON field fails
its proposed parse. Original collection reports describe their checks; this study
reports the released strings, without claiming to revalidate the absent responses
or explaining a defect's origin from unavailable evidence.

Read derived CSVs with a real parser. In pandas use
`pd.read_csv(path, keep_default_na=False, na_values=[r"\N"])`: pandas defaults
would incorrectly treat literal `null` (a JSON type label) as missing. Numeric
absence in film_metrics/taxonomy is written as `\N`; zero is a measured zero in
an accessible export. See the coverage semantics in the report.
