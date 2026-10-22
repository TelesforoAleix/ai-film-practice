-- eligible is Study 01's Study 08 primary population. Every join is compound.
CREATE TEMP TABLE jobs AS
SELECT g.* FROM generations g JOIN eligible USING(film_id);
CREATE TEMP TABLE bindings AS
SELECT u.* FROM asset_usages u JOIN jobs USING(film_id,generation_id);
CREATE TEMP TABLE film_assets AS
SELECT a.* FROM assets a JOIN eligible USING(film_id);
CREATE TEMP TABLE elements AS
SELECT r.* FROM reference_elements r JOIN eligible USING(film_id);
-- Co-occurrence is deliberately a separate relation from asset-backed transitions.
CREATE TEMP TABLE cooccurrence AS
SELECT DISTINCT a.film_id,a.model_identifier AS producer_model,
 b.model_identifier AS consumer_model
FROM (SELECT DISTINCT film_id,model_identifier FROM jobs) a
JOIN (SELECT DISTINCT film_id,model_identifier FROM jobs) b ON a.film_id=b.film_id
WHERE a.model_identifier<b.model_identifier;
