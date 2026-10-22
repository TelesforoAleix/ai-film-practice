-- Run from the repository root. All derived CSVs use the explicit \N marker.
CREATE VIEW workflow_films AS
SELECT * FROM read_csv('studies/08-workflow/outputs/film_metrics.csv', nullstr='\N');
CREATE VIEW workflow_transitions AS
SELECT * FROM read_csv('studies/08-workflow/outputs/transitions.csv', nullstr='\N');
-- Each producer/consumer pair belongs to exactly one ordered literal model pair.
SELECT cross_model, sum(pairs) AS pairs,
 (SELECT sum(pairs) FROM workflow_films) AS resolved_pair_denominator
FROM workflow_transitions GROUP BY ALL ORDER BY ALL;
-- Per-film cross-model pair shares, only for films with a positive pair denominator.
WITH cross_counts AS (
 SELECT film_id,sum(pairs) AS cross_pairs FROM workflow_transitions
 WHERE cross_model GROUP BY film_id
)
SELECT f.film_id,coalesce(c.cross_pairs,0) AS cross_pairs,f.pairs AS pair_denominator,
 coalesce(c.cross_pairs,0)::DOUBLE/nullif(f.pairs,0) AS cross_pair_share
FROM workflow_films f LEFT JOIN cross_counts c USING(film_id)
ORDER BY f.film_id;
-- Co-occurrence without an observed cross-model handoff is a separate disclosure state.
SELECT film_id,jobs,literal_models,chained,cross_model
FROM workflow_films WHERE literal_models>1 AND cross_model=0 ORDER BY film_id;
-- Reuse the exact graph function/compound joins in build.py to retrieve source entities.
-- No date/folder/name similarity adds a producer. The named exemplars are fully
-- enumerated in outputs/handoff_examples.csv; all other transition scopes are
-- film + producer model + consumer model on Study 07's material graph.
