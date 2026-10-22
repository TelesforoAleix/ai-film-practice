-- eligible is the unchanged Study 01 Study 05 production population.
CREATE TEMP TABLE j AS SELECT g.* FROM generations g JOIN eligible USING(film_id);
CREATE TEMP TABLE attachments AS
SELECT DISTINCT u.film_id,u.generation_id,u.asset_id,u.asset_role,u.parameter_path,
 u.reference_element_id,a.asset_type,p.generation_id AS producer,
 p.generation_type AS producer_type,
 (u.asset_role IN ('input_image','reference_image','input_start_image','input_end_image')
  OR (u.asset_role='input_asset' AND
   (regexp_matches(u.parameter_path,'^params\.input_images\[')
    OR u.parameter_path IN ('params.input_image','params.image_reference',
      'params.custom_reference','params.paint_image')))) AS image_binding
FROM asset_usages u JOIN j USING(film_id,generation_id)
LEFT JOIN assets a USING(film_id,asset_id)
LEFT JOIN j p ON p.film_id=a.film_id AND p.generation_id=a.generation_id
 AND p.generation_id<>u.generation_id
WHERE u.asset_role IN ('input_image','reference_image','input_start_image',
 'input_end_image','input_asset','input_video','reference_video','input_audio');
CREATE TEMP TABLE image_jobs AS
SELECT j.*,
 (SELECT count(DISTINCT asset_id) FROM attachments a WHERE a.film_id=j.film_id
  AND a.generation_id=j.generation_id AND image_binding) AS image_inputs,
 (SELECT count(DISTINCT asset_id) FROM attachments a WHERE a.film_id=j.film_id
  AND a.generation_id=j.generation_id AND NOT image_binding
  AND parameter_path NOT IN ('params.style','params.camera_lens','params.camera_model',
  'params.color_preset','params.camera_aperture','params.camera_focal_length')) AS other_inputs,
 (SELECT count(DISTINCT producer) FROM attachments a WHERE a.film_id=j.film_id
  AND a.generation_id=j.generation_id AND image_binding
  AND producer_type='image') AS image_parents,
 EXISTS(SELECT 1 FROM attachments a WHERE a.film_id=j.film_id
  AND a.producer=j.generation_id AND a.image_binding
  AND a.generation_id IN (SELECT generation_id FROM j v WHERE v.film_id=j.film_id
    AND v.generation_type='video')) AS video_consumer
FROM j WHERE generation_type='image';
