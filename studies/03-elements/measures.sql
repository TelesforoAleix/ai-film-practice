-- Registered eligible comes from Study 01, Study 03 primary production eligibility.
CREATE TEMP TABLE j AS SELECT g.* FROM generations g JOIN eligible USING(film_id);
CREATE TEMP TABLE inputs AS
SELECT DISTINCT u.film_id,u.generation_id,u.asset_id,u.reference_element_id,
 u.asset_role,u.parameter_path FROM asset_usages u JOIN j USING(film_id,generation_id)
WHERE asset_role IN ('input_audio','input_video','input_image','reference_video',
 'input_end_image','reference_image','input_start_image','input_asset');
CREATE TEMP TABLE input_pairs AS
SELECT DISTINCT film_id,generation_id,asset_id FROM inputs;
CREATE TEMP TABLE input_reuse AS
SELECT film_id,asset_id,count(*) AS consumers FROM input_pairs GROUP BY ALL;
CREATE TEMP TABLE refs AS
SELECT r.*,
 (SELECT count(DISTINCT i.generation_id) FROM inputs i WHERE i.film_id=r.film_id
  AND i.reference_element_id=r.reference_element_id) AS consumers,
 (SELECT count(DISTINCT i.asset_id) FROM inputs i WHERE i.film_id=r.film_id
  AND i.reference_element_id=r.reference_element_id) AS attached_asset_ids
FROM reference_elements r JOIN eligible USING(film_id);
CREATE TEMP TABLE attachments AS
SELECT i.*,a.generation_id AS producer FROM inputs i
LEFT JOIN assets a USING(film_id,asset_id);
CREATE TEMP TABLE job_channels AS
SELECT j.*,
 (SELECT count(DISTINCT asset_id) FROM inputs i WHERE i.film_id=j.film_id
  AND i.generation_id=j.generation_id) AS input_assets,
 (SELECT count(DISTINCT reference_element_id) FROM inputs i WHERE i.film_id=j.film_id
  AND i.generation_id=j.generation_id) AS attached_references,
 EXISTS(SELECT 1 FROM attachments i JOIN j p ON p.film_id=i.film_id
  AND p.generation_id=i.producer WHERE i.film_id=j.film_id
  AND i.generation_id=j.generation_id AND i.producer<>i.generation_id) AS resolved_input
FROM j;
