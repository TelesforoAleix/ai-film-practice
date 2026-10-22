-- Eligible is Study 01's primary Study 07 population. All joins are film-scoped.
CREATE TEMP TABLE jobs AS
SELECT g.* FROM generations g JOIN eligible USING(film_id);
CREATE TEMP TABLE bindings AS
SELECT u.* FROM asset_usages u JOIN jobs USING(film_id,generation_id);
CREATE TEMP TABLE film_assets AS
SELECT a.* FROM assets a JOIN eligible USING(film_id);
CREATE TEMP TABLE elements AS
SELECT r.* FROM reference_elements r JOIN eligible USING(film_id);
-- These queries deliberately retain occurrences, role/path and reference IDs.
-- build.py deduplicates graph edges and consumer sets independently.
