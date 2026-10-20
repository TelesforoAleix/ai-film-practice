-- All joins and counts retain film scope. Source views stay VARCHAR.
CREATE TEMP VIEW population AS
SELECT f.*, CASE WHEN in_priority_scope = 'True' THEN
 CASE WHEN most_watched_rank_top100 IS NOT NULL AND
 json_contains(shortlist_status, '"audience_choice"') THEN 'both'
 WHEN most_watched_rank_top100 IS NOT NULL THEN 'most_watched_only'
 ELSE 'shortlist_only' END ELSE 'supplemental' END AS cohort_group,
 CASE extraction_status WHEN 'complete_public_workspace' THEN
 CASE WHEN in_priority_scope = 'True' THEN 'primary' ELSE 'supplemental' END
 WHEN 'excluded_non_open_source' THEN 'excluded' ELSE 'unavailable' END AS population
FROM films f WHERE in_priority_scope = 'True'
 OR extraction_status = 'complete_public_workspace';

CREATE TEMP VIEW jobs AS
SELECT film_id, count(*) AS generations,
 count(*) FILTER (WHERE generation_type='image') AS image_jobs,
 count(*) FILTER (WHERE generation_type='video') AS video_jobs,
 count(*) FILTER (WHERE generation_type='audio') AS audio_jobs,
 count(DISTINCT model_identifier) AS models,
 count(DISTINCT author_user_id) AS authors,
 count(DISTINCT generation_batch_id) AS batches,
 count(*) FILTER (WHERE prompt IS NOT NULL AND prompt <> '') AS prompt_nonempty,
 count(*) FILTER (WHERE prompt = '') AS prompt_empty,
 count(*) FILTER (WHERE prompt IS NULL) AS prompt_unavailable,
 count(*) FILTER (WHERE created_at IS NOT NULL AND created_at <> '') AS dated,
 count(*) FILTER (WHERE author_user_id IS NOT NULL AND author_user_id <> '') AS authored,
 min(try_cast(created_at AS TIMESTAMPTZ)) AS first_event,
 max(try_cast(created_at AS TIMESTAMPTZ)) AS last_event
FROM generations GROUP BY film_id;

CREATE TEMP VIEW usage_counts AS
SELECT film_id,
 count(*) FILTER (WHERE asset_role <> 'output') AS input_occurrences,
 count(DISTINCT generation_id) FILTER (WHERE asset_role <> 'output') AS jobs_with_inputs,
 count(*) FILTER (WHERE asset_role = 'output') AS output_occurrences,
 count(DISTINCT generation_id) FILTER (WHERE asset_role = 'output') AS jobs_with_outputs
FROM asset_usages GROUP BY film_id;

CREATE TEMP VIEW profile AS
SELECT p.film_id, p.title, p.creator, p.population, p.cohort_group,
 p.duration AS declared_duration_seconds, p.category AS declared_category_json,
 p.editorial_selection, p.most_watched_rank_top100,
 p.project_brief IS NOT NULL AS brief_disclosed,
 p.project_brief = '' AS brief_explicitly_empty,
 e.brief_complete, e.generation_count_reconciles,
 j.* EXCLUDE(film_id), u.* EXCLUDE(film_id),
 (SELECT count(*) FROM folders x WHERE x.film_id=p.film_id) AS folders,
 (SELECT count(*) FROM reference_elements x WHERE x.film_id=p.film_id) AS reference_elements,
 (SELECT count(*) FROM generation_prompts x WHERE x.film_id=p.film_id) AS nested_text_fields,
 (SELECT count(*) FROM brief_assets x WHERE x.film_id=p.film_id) AS brief_embeddings,
 (SELECT count(*) FROM assets x WHERE x.film_id=p.film_id) AS asset_entities
FROM population p LEFT JOIN jobs j USING(film_id)
LEFT JOIN usage_counts u USING(film_id) LEFT JOIN extraction_log e USING(film_id);
