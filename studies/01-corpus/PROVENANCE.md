# Evidence and measure contract

Release: data-2026-10-20, collected 19–20 October 2026. Both initial and independent
fresh downloads are checksum-verified with the repository downloader. No source
site, media URL, private workspace or external library is retrieved by this study.
The final handover records validation; source hashes remain in the release manifest.

Every numeric output is an observed aggregate of published fields, unless explicitly
identified as a proposed threshold or inferred taxonomy label. Each per-film row
joins [outputs/metric_evidence.csv](outputs/metric_evidence.csv) on film_id. That
ledger records Study 01, film key, entity scope, source/query path, numeric excerpt,
evidence label, competing explanation, denominator and confidence rationale.
The exact entity IDs remain selectable from the source views with that film ID;
an aggregate's scope is all compound keys in the named source tables, not one
illustrative generation. [outputs/aggregate_evidence.csv](outputs/aggregate_evidence.csv)
provides the same fields and exact film sets for the reported distributions and
weighted summaries. Source paths are table/column paths in the published release;
relative raw-record paths, where retained, are additional provenance only.

| Output / measure | Source and computation | Denominator and limits |
| --- | --- | --- |
| populations | profile.sql population; films status, in_priority_scope, shortlist_status, most_watched_rank_top100 | 6,224 catalogue; 186 priority; 157 primary; pilot separate. Presence of original top-100 rank identifies that cohort. |
| film_metrics: generations, image/video/audio jobs | Count rows in generations by film, exact generation_type | Jobs in that film; compound-key uniqueness checked. Other/null types remain outside those three subtotals. |
| models/authors/batches | Distinct non-null model_identifier/author_user_id/generation_batch_id per film | Same film's jobs; null coverage separately exposed. Names/providers are not inferred; authors are not team roles. |
| prompt_nonempty/empty/unavailable | Exact prompt predicates <> '', = '', IS NULL | All jobs in film. Whitespace-only text remains nonempty; substantive intent needs later coding. |
| dated/authored, first/last_event | Nonempty fields; try_cast timestamps and extrema | Jobs in film, parse errors in dictionary. Activity window only. |
| input/output occurrences and jobs_with_inputs/outputs | asset_usages role <> output versus output; row count versus distinct generation_id | Occurrences and distinct jobs are separate; job shares divide by film generations. References can duplicate other input representations. |
| folders/reference_elements/nested_text/brief_embeddings/asset_entities | Per-film row counts from named tables | Exported entities/fields/embeddings; no claim to private libraries. Assets include covers/final films; placements never increase entity count. |
| coverage | Numeric/field availability mapped to available/empty/unavailable | 187 rows; nonzero evidence does not mean every job has it. Read field counts beside states. |
| taxonomy | generation shares, literal model counts, exported reference/folder counts | Inferred orientation/proxies under documented proposed thresholds, not actual film content or qualitative production categories. |
| distributions | Per-film quantiles (pandas linear interpolation) within primary or cohort subgroup | measured_films and eligible_films explicit; sums are not independent observations. |
| by_generation_type/model_identifier/author_user_id | Grouped job counts at film x literal dimension x cohort | Film generations in film_metrics; omitted combinations have zero exported jobs. No role inference. |
| by_creator/duration/category | Film-level declared attribute plus job count | 157 primary rows; creator repeats are not independent; empty JSON categories remain explicit. |
| generation_weights/model_weights | Pooled jobs and average of per-film shares (zero for absent categories/models) | job_denominator versus film_denominator in each row. Models stay literal. |
| unusual_projects | Union of declared audit triggers, source reconciliation and grain checks | 157 primary films; flagged projects are not “bad” records. All retained for descriptive analysis. |
| panel | Frozen purposive eight-pair register, selected from primary metrics | 16 films; no representative or causal interpretation. Selection rationale is proposed sampling design. |
| calibration | Human assignment on selected excerpts; executable source-match checks | Four films x 49 codes; pilot explicitly supplemental; no film-wide absence or agreement estimates. Each row carries its own evidence fields. |
| eligibility | Evidence gates by study and film | Primary histories are the outer population; narrower questions must apply field/edge/text gates and report the resulting denominator. |

Observations, interpretations and studio proposals stay separate. Public histories
may omit rejected, external or private work. No cost, labour, failure rate, internal
scheduler, agents, achieved output quality or causal production benefit is measured.
