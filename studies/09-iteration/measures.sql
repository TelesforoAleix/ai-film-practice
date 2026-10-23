-- eligible is the unchanged Study 01 Study 09 primary register.
CREATE TEMP TABLE jobs AS
SELECT g.* FROM generations g JOIN eligible USING(film_id);
CREATE TEMP TABLE bindings AS
SELECT u.* FROM asset_usages u JOIN jobs USING(film_id,generation_id);
CREATE TEMP TABLE film_assets AS
SELECT a.* FROM assets a JOIN eligible USING(film_id);
CREATE TEMP TABLE elements AS
SELECT r.* FROM reference_elements r JOIN eligible USING(film_id);
