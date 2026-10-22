-- eligible contains Study 01's 157 primary histories, never the pilot.
CREATE TEMP TABLE j AS SELECT g.* FROM generations g JOIN eligible USING(film_id);
CREATE TEMP TABLE attachments AS
SELECT DISTINCT u.film_id,u.generation_id,u.asset_id,u.asset_role,u.parameter_path,
 u.reference_element_id,p.generation_id AS producer,p.generation_type AS producer_type,
 (u.asset_role IN ('input_image','reference_image','input_start_image','input_end_image')
  OR (u.asset_role='input_asset' AND
   (regexp_matches(u.parameter_path,'^params\.input_images\[')
    OR u.parameter_path IN ('params.input_image','params.image_reference',
     'params.custom_reference','params.paint_image','params.end_input_image')))) AS image_binding,
 (u.asset_role IN ('input_video','reference_video') OR
  (u.asset_role='input_asset' AND u.parameter_path='params.input_video')) AS video_binding,
 (u.asset_role='input_audio' OR
  (u.asset_role='input_asset' AND u.parameter_path='params.input_audio')) AS audio_binding
FROM asset_usages u JOIN j USING(film_id,generation_id)
LEFT JOIN assets a USING(film_id,asset_id)
LEFT JOIN j p ON p.film_id=a.film_id AND p.generation_id=a.generation_id
 AND p.generation_id<>u.generation_id
WHERE u.asset_role IN ('input_image','reference_image','input_start_image',
 'input_end_image','input_asset','input_video','reference_video','input_audio');
CREATE TEMP TABLE video_jobs AS
SELECT j.*,
 (SELECT count(DISTINCT asset_id) FROM attachments a WHERE a.film_id=j.film_id
  AND a.generation_id=j.generation_id AND image_binding) AS image_inputs,
 (SELECT count(DISTINCT asset_id) FROM attachments a WHERE a.film_id=j.film_id
  AND a.generation_id=j.generation_id AND video_binding) AS video_inputs,
 (SELECT count(DISTINCT asset_id) FROM attachments a WHERE a.film_id=j.film_id
  AND a.generation_id=j.generation_id AND audio_binding) AS audio_inputs,
 EXISTS(SELECT 1 FROM attachments a WHERE a.film_id=j.film_id
  AND a.generation_id=j.generation_id AND asset_role='input_start_image') AS has_start,
 EXISTS(SELECT 1 FROM attachments a WHERE a.film_id=j.film_id
  AND a.generation_id=j.generation_id AND (asset_role='input_end_image'
   OR parameter_path='params.end_input_image')) AS has_end,
 (SELECT count(DISTINCT producer) FROM attachments a WHERE a.film_id=j.film_id
  AND a.generation_id=j.generation_id AND image_binding
  AND producer_type='image') AS image_parents,
 (SELECT count(DISTINCT producer) FROM attachments a WHERE a.film_id=j.film_id
  AND a.generation_id=j.generation_id AND video_binding
  AND producer_type='video') AS video_parents,
 (SELECT count(*) FROM attachments a WHERE a.film_id=j.film_id
  AND a.generation_id=j.generation_id AND NOT image_binding AND NOT video_binding
  AND NOT audio_binding AND parameter_path NOT IN ('params.style','params.camera_lens',
   'params.camera_model','params.color_preset','params.camera_aperture',
   'params.camera_focal_length','params.pacing','params.light','params.genre_control',
   'params.era_control','params.preset','params.motion','params.application')
  AND NOT regexp_matches(parameter_path,'^params\.multi_prompt\[[0-9]+\]\.preset$')) AS unknown_inputs
FROM j WHERE generation_type='video';
