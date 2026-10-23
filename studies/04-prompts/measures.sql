-- Original primary field and distinct nested paths; preserve null and empty.
CREATE TEMP TABLE text_fields AS
SELECT g.film_id,g.generation_id,g.prompt_source_path AS field_path,
       'primary' AS text_role,g.prompt AS text
FROM generations g JOIN eligible USING(film_id)
UNION ALL
SELECT p.film_id,p.generation_id,p.field_path,
       CASE WHEN p.prompt_role='negative' THEN 'negative'
            WHEN starts_with(p.field_path,'params.multi_prompt[') THEN 'shot_prompt'
            ELSE 'other_text' END,p.text
FROM generation_prompts p JOIN generations g USING(film_id,generation_id)
JOIN eligible e ON e.film_id=p.film_id
WHERE p.field_path IS DISTINCT FROM g.prompt_source_path;
-- Assert the omitted nested copy separately in the build.
CREATE TEMP TABLE context_counts AS
SELECT g.film_id,g.generation_id,
       count(DISTINCT CASE WHEN u.asset_role IN
         ('input_image','reference_image','input_start_image','input_end_image',
          'input_video','reference_video','input_audio','reference_audio')
         OR (u.asset_role='input_asset' AND
             (starts_with(u.parameter_path,'params.input_images[')
              OR u.parameter_path IN ('params.input_image','params.input_video',
                                      'params.input_audio','params.image_reference',
                                      'params.custom_reference','params.paint_image')))
         THEN u.asset_id END) AS media_inputs,
       count(DISTINCT u.reference_element_id) AS "references",
       count(DISTINCT CASE WHEN r.description IS NOT NULL AND r.description<>''
             THEN r.reference_element_id END) AS metadata_descriptions
FROM generations g JOIN eligible e USING(film_id)
LEFT JOIN asset_usages u ON g.film_id=u.film_id AND g.generation_id=u.generation_id
 AND u.asset_role<>'output'
LEFT JOIN reference_elements r ON u.film_id=r.film_id
 AND u.reference_element_id=r.reference_element_id
GROUP BY g.film_id,g.generation_id;
