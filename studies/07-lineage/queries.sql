-- After build.py (or downloading study-07-v1 assets and verifying SHA256SUMS):
CREATE VIEW lineage_nodes AS
SELECT * FROM read_csv('data/study07-release/nodes.csv.gz', all_varchar=true,
                      nullstr='\N');
CREATE VIEW lineage_edges AS
SELECT * FROM read_csv('data/study07-release/edges.csv.gz', all_varchar=true,
                      nullstr='\N');
-- Complete panel maps: join either view to Study 01's 16 panel film IDs.
-- Do not drop nodes merely because they have no input/dependency edge.
SELECT n.node_kind, count(*) AS nodes
FROM lineage_nodes n
JOIN read_csv('studies/01-corpus/outputs/panel.csv', all_varchar=true) p
  USING(film_id)
GROUP BY ALL ORDER BY ALL;
-- Raw duplicate channels do not increase distinct consumers.
SELECT film_id, source_id AS asset_id,
       count(DISTINCT target_id) AS consumer_jobs
FROM lineage_edges
WHERE edge_type='media_input'
GROUP BY film_id,source_id
HAVING count(DISTINCT target_id)>=2
ORDER BY film_id,consumer_jobs DESC,asset_id;
-- Only explicit produced assets support a generation handoff.
SELECT DISTINCT i.film_id,p.source_id AS producer,i.source_id AS asset_id,
       i.target_id AS consumer,i.asset_role,i.parameter_path
FROM lineage_edges i JOIN lineage_edges p
 ON i.film_id=p.film_id AND i.source_id=p.target_id
 AND p.edge_type='produces' AND p.target_kind='asset'
WHERE i.edge_type='media_input' AND p.source_id<>i.target_id
ORDER BY ALL;
