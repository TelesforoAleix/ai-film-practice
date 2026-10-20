-- Study 10. Population is registered from Study 01 eligibility by build.py.
-- Never infer lineage from dates or folder proximity.
CREATE TEMP TABLE j AS
SELECT g.* FROM generations g JOIN eligible e USING(film_id);
CREATE TEMP TABLE placements AS
SELECT film_id, generation_id, count(DISTINCT folder_id) AS n
FROM generation_folders GROUP BY ALL;
CREATE TEMP TABLE inputs AS
SELECT DISTINCT u.film_id, u.generation_id, u.asset_id
FROM asset_usages u JOIN eligible e USING(film_id)
WHERE u.asset_role IN ('input_audio','input_video','input_image','reference_video',
 'input_end_image','reference_image','input_start_image','input_asset');
CREATE TEMP TABLE edges AS
SELECT DISTINCT i.film_id, a.generation_id AS producer, i.generation_id AS consumer,
 i.asset_id, p.author_user_id AS producer_author, c.author_user_id AS consumer_author
FROM inputs i JOIN assets a USING(film_id, asset_id)
JOIN j p ON p.film_id=i.film_id AND p.generation_id=a.generation_id
JOIN j c ON c.film_id=i.film_id AND c.generation_id=i.generation_id
WHERE a.generation_id <> i.generation_id;
CREATE TEMP TABLE edge_pairs AS
SELECT DISTINCT film_id, producer, consumer, producer_author, consumer_author FROM edges;
CREATE TEMP TABLE reuse AS
SELECT film_id, asset_id, count(*) AS consumers FROM inputs GROUP BY ALL;
-- A folder boundary is disjoint placement sets; unplaced endpoints are unknown.
CREATE TEMP TABLE pair_folders AS
SELECT x.*,
 EXISTS(SELECT 1 FROM generation_folders f WHERE f.film_id=x.film_id
  AND f.generation_id=x.producer) AND
 EXISTS(SELECT 1 FROM generation_folders f WHERE f.film_id=x.film_id
  AND f.generation_id=x.consumer) AS placed_endpoints,
 EXISTS(SELECT 1 FROM generation_folders p JOIN generation_folders c
  ON p.film_id=c.film_id AND p.folder_id=c.folder_id
  WHERE p.film_id=x.film_id AND p.generation_id=x.producer
  AND c.generation_id=x.consumer) AS shared_folder
FROM edge_pairs x;
CREATE TEMP TABLE job_counts AS
SELECT film_id, count(*) AS jobs,
 count(*) FILTER(WHERE author_user_id IS NOT NULL AND author_user_id<>'') AS authored,
 count(DISTINCT nullif(author_user_id,'')) AS authors,
 count(*) FILTER(WHERE try_cast(created_at AS TIMESTAMPTZ) IS NOT NULL) AS dated,
 min(try_cast(created_at AS TIMESTAMPTZ)) AS first_event,
 max(try_cast(created_at AS TIMESTAMPTZ)) AS last_event,
 count(DISTINCT cast(try_cast(created_at AS TIMESTAMPTZ) AS DATE)) AS active_utc_dates,
 count(*) FILTER(WHERE prompt IS NULL) AS prompt_unavailable,
 count(*) FILTER(WHERE prompt='') AS prompt_empty,
 count(*) FILTER(WHERE prompt<>'') AS prompt_nonempty,
 count(DISTINCT prompt) FILTER(WHERE prompt<>'') AS distinct_nonempty,
 count(*) FILTER(WHERE n>1) AS multiply_placed_jobs,
 coalesce(sum(n),0) AS generation_placements,
 count(*) FILTER(WHERE n IS NOT NULL) AS placed_jobs
FROM j LEFT JOIN placements USING(film_id,generation_id) GROUP BY film_id;
CREATE TEMP TABLE film_measures AS
SELECT e.*, f.title, f.creator, try_cast(f.duration AS DOUBLE) AS declared_seconds,
 k.*, epoch(last_event-first_event)/86400 AS event_span_days,
 prompt_nonempty-distinct_nonempty AS repeat_excess,
 (SELECT count(*) FROM folders x WHERE x.film_id=e.film_id) AS folders,
 (SELECT count(DISTINCT folder_id) FROM generation_folders x
  WHERE x.film_id=e.film_id) AS occupied_folders,
 (SELECT count(*) FROM asset_folders x WHERE x.film_id=e.film_id) AS asset_placements,
 (SELECT count(DISTINCT asset_id) FROM asset_folders x
  WHERE x.film_id=e.film_id) AS placed_assets,
 (SELECT count(*) FROM (SELECT asset_id FROM asset_folders x
  WHERE x.film_id=e.film_id GROUP BY asset_id HAVING count(DISTINCT folder_id)>1))
  AS multiply_placed_assets,
 (SELECT count(*) FROM reference_elements x WHERE x.film_id=e.film_id) AS elements,
 (SELECT count(*) FROM inputs x WHERE x.film_id=e.film_id) AS distinct_input_pairs,
 (SELECT count(*) FROM reuse x WHERE x.film_id=e.film_id) AS input_assets,
 (SELECT count(*) FROM reuse x WHERE x.film_id=e.film_id AND consumers>1) AS reused_input_assets,
 (SELECT count(*) FROM edge_pairs x WHERE x.film_id=e.film_id) AS resolved_job_pairs,
 (SELECT count(*) FROM edge_pairs x WHERE x.film_id=e.film_id
  AND nullif(producer_author,'') IS NOT NULL AND nullif(consumer_author,'') IS NOT NULL)
  AS authored_job_pairs,
 (SELECT count(*) FROM edge_pairs x WHERE x.film_id=e.film_id
  AND nullif(producer_author,'') IS NOT NULL AND nullif(consumer_author,'') IS NOT NULL
  AND producer_author<>consumer_author) AS cross_author_pairs,
 (SELECT count(*) FROM pair_folders x WHERE x.film_id=e.film_id AND placed_endpoints)
  AS placed_job_pairs,
 (SELECT count(*) FROM pair_folders x WHERE x.film_id=e.film_id
  AND placed_endpoints AND NOT shared_folder) AS disjoint_folder_pairs
FROM eligible e JOIN films f USING(film_id) JOIN job_counts k USING(film_id);
