-- Study 01 eligibility is registered as eligible. Every join is film-scoped.
CREATE TEMP TABLE jobs AS
SELECT g.* FROM generations g JOIN eligible e USING (film_id);

-- Reuse the AF3a primary/nested crosswalk, retaining missing and empty fields.
CREATE TEMP TABLE fields AS
SELECT film_id, generation_id, prompt_source_path AS field_path,
  'primary' AS text_role, prompt AS text FROM jobs
UNION ALL
SELECT p.film_id, p.generation_id, p.field_path,
  CASE WHEN p.prompt_role='negative' THEN 'negative'
    WHEN starts_with(p.field_path, 'params.multi_prompt[') THEN 'shot_prompt'
    ELSE 'other_text' END, p.text
FROM generation_prompts p JOIN jobs j USING (film_id, generation_id)
WHERE p.field_path IS DISTINCT FROM j.prompt_source_path;

CREATE TEMP TABLE usage_edges AS
SELECT DISTINCT u.film_id, u.generation_id AS consumer, u.asset_id,
  a.generation_id AS producer, u.asset_role, u.parameter_path,
  u.reference_element_id
FROM asset_usages u JOIN eligible e USING (film_id)
LEFT JOIN assets a USING (film_id, asset_id)
WHERE u.asset_role <> 'output';
