"""Study 04: released structural features, provisional labels and scoped context."""

import argparse
import gzip
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

from film_practice import connect
from film_practice.prompt_labels import COMPONENTS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NULL = r"\N"
STRATA = ["film_id", "generation_type", "text_role"]
FLAGS = [
    "section",
    "reference",
    "camera",
    "lens",
    "preservation",
    "exclusion",
    "edit",
    "multi_shot",
]
FLAGS += [
    "structured_json",
    "xml_like",
    "repeated_lines",
    "short_edit_proxy",
    "long_description_proxy",
    "long_text",
]
ALT = (
    "Selection, language, task/model mix, repeated text, shared creators and omitted "
    "External work and unseen media limit semantic interpretation."
)
CONF = (
    "Exact released-key/count correspondence; lexical matches are structural. "
    "27B semantics are provisional, single-agent gold unadjudicated; see agreement.csv "
    "and semantic_bounds.csv. No outcome or causal inference."
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return pd.read_csv(
        path, keep_default_na=False, na_values=[NULL], dtype={"code_id": str}
    )


def write(frame, path):
    frame.to_csv(
        path, index=False, na_rep=NULL, float_format="%.9f", lineterminator="\n"
    )


def js(path, value):
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    )


def module(path):
    spec = importlib.util.spec_from_file_location("af11_" + path.parent.name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def verify_manifest(directory):
    for line in (directory / "SHA256SUMS").read_text().splitlines():
        expected, name = line.split(maxsplit=1)
        assert digest(directory / name.lstrip(" *")) == expected, name


def evidence(
    fid, excerpt, denominator, label="observed", source="build.py; measures.sql"
):
    return dict(
        study="04",
        film_id=fid,
        entity_ids=f"{fid}/generation:*; asset:*; reference:*",
        source_path=source,
        excerpt=excerpt,
        evidence_label=label,
        competing_explanation=ALT,
        denominator=denominator,
        confidence_rationale=CONF,
    )


def summarize(frame, metrics, dimensions=()):
    rows = []
    groups = [("all", "primary", frame)]
    for dim in dimensions:
        groups.extend((dim, val, g) for val, g in frame.groupby(dim, dropna=False))
    for dim, val, g in groups:
        for num, den in metrics:
            valid = g[g[den] > 0]
            rates = valid[num] / valid[den]
            n, d = float(valid[num].sum()), float(valid[den].sum())
            rows.append(
                dict(
                    dimension=dim,
                    value=val,
                    metric=num,
                    denominator_name=den,
                    eligible_films=len(g),
                    measured_films=len(valid),
                    numerator=n,
                    denominator=d,
                    equal_film_mean=rates.mean(),
                    median=rates.median(),
                    q25=rates.quantile(0.25),
                    q75=rates.quantile(0.75),
                    pooled_share=n / d if d else None,
                )
            )
    return pd.DataFrame(rows)


def weight_sample(sample, candidates):
    """Descriptive poststratification, not inverse inclusion probabilities."""
    mass = (
        candidates.groupby(STRATA, dropna=False)
        .text_id.nunique()
        .rename("candidate_texts")
    )
    s = sample.groupby(STRATA, dropna=False).agg(
        sampled=("text_id", "size"), successful=("success", "sum")
    )
    s = mass.to_frame().join(s).fillna({"sampled": 0, "successful": 0}).reset_index()
    s["failed"] = s.sampled - s.successful
    s["success_weight"] = s.candidate_texts / s.successful.replace(0, float("nan"))
    s["sample_weight"] = s.candidate_texts / s.sampled.replace(0, float("nan"))
    return sample.merge(s, on=STRATA, validate="many_to_one"), s


def label_rows(records):
    rows = []
    for r in records:
        item = {
            k: r[k]
            for k in [
                *STRATA,
                "text_id",
                "generation_id",
                "field_path",
                "model_identifier",
                "status",
            ]
        }
        item["success"] = r["status"] == "success"
        for c in COMPONENTS:
            item[c] = int(r["labels"][c]["present"]) if item["success"] else None
        rows.append(item)
    return pd.DataFrame(rows)


def panel(db, output, jobs, labels):
    rows, contexts = [], []
    for p in sorted((ROOT / "case-files").glob("*/codes.csv")):
        codes = read(p)
        codes = codes[codes.code_id.str.startswith("04.")].copy()
        codes["case_source"] = str(p.relative_to(ROOT))
        rows.extend(codes.to_dict("records"))
        for r in codes.itertuples():
            ids = re.findall(r"/generation:([a-z0-9-]+)", r.entity_ids)
            for gid in ids:
                j = jobs.loc[(r.film_id, gid)]
                usages = db.execute(
                    "SELECT asset_id,asset_role,parameter_path,reference_element_id "
                    "FROM asset_usages WHERE film_id=? AND generation_id=? "
                    "AND asset_role <> 'output' ORDER BY ALL",
                    [r.film_id, gid],
                ).df()
                refids = sorted(set(usages.reference_element_id.dropna()))
                metadata = []
                for rid in refids:
                    rr = db.execute(
                        "SELECT name,category,description FROM reference_elements "
                        "WHERE film_id=? AND reference_element_id=?",
                        [r.film_id, rid],
                    ).fetchone()
                    metadata.append(
                        dict(
                            reference_element_id=rid,
                            name_state=state(rr[0]) if rr else "unresolved",
                            category=rr[1] if rr else None,
                            description_state=state(rr[2]) if rr else "unresolved",
                        )
                    )
                contexts.append(
                    dict(
                        film_id=r.film_id,
                        generation_id=gid,
                        evidence_id=r.evidence_id,
                        model_identifier=j.model_identifier,
                        generation_type=j.generation_type,
                        field_path=j.prompt_source_path,
                        text_state=state(j.prompt),
                        text_sha256=hashtext(j.prompt) if j.prompt else None,
                        inputs=usages.astype(object)
                        .where(pd.notna(usages), None)
                        .to_dict("records"),
                        metadata=metadata,
                        media_property_content="unobservable",
                        raw_controls=controls(j.parameters_json),
                        evidence_label="observed",
                    )
                )
    write(pd.DataFrame(rows), output / "case_evidence.csv")
    js(output / "panel_contexts.json", contexts)
    assignments = (
        pd.DataFrame(rows).groupby(["code_id", "status", "value"], dropna=False).size()
    )
    a = assignments.rename("assignments").reset_index()
    a["panel_denominator"] = 16
    write(a, output / "panel_assignments.csv")
    # The original 04.4 assignments are scoped channel evidence, not property censuses.
    js(
        output / "information_locations.json",
        [
            dict(
                film_id=r["film_id"],
                evidence_id=r["evidence_id"],
                channels=r["value"],
                media_properties="unobservable",
                contradictions="unadjudicated",
                component_scope="Only named 04.2 properties; other components unknown",
                source_path=r["source_path"],
                excerpt=r["scope_note"],
                evidence_label="inferred",
                denominator=r["denominator"],
                competing_explanation=r["competing_explanation"],
                confidence_rationale=r["confidence_rationale"],
            )
            for r in rows
            if r["code_id"] == "04.4"
        ],
    )
    histories = json.loads(
        (ROOT / "studies/09-iteration/outputs/revision_histories.json").read_text()
    )
    result = []
    for h in histories:
        if h["code_id"] != "09.3":
            continue
        members = []
        for m in h["members"]:
            j = jobs.loc[(h["film_id"], m["generation_id"])]
            tid = hashtext(j.prompt) if j.prompt else None
            record = labels.get(tid)
            members.append(
                dict(
                    generation_id=m["generation_id"],
                    model_identifier=j.model_identifier,
                    characters=len(j.prompt) if j.prompt is not None else None,
                    text_sha256=tid,
                    sample_status=record["status"] if record else "not_sampled",
                    components={c: v["present"] for c, v in record["labels"].items()}
                    if record and record["status"] == "success"
                    else None,
                    raw_controls=controls(j.parameters_json),
                )
            )
        result.append(
            dict(
                film_id=h["film_id"],
                evidence_id=h["evidence_id"],
                comparison_order=h["comparison_order"],
                members=members,
                interpretation=h["interpretation"],
                evidence_label="inferred",
                source_path=(
                    "studies/09-iteration/outputs/revision_histories.json; generations"
                ),
                denominator="One named pair; seven purposive histories",
                competing_explanation=(
                    "Preparation or new candidate; "
                    "ordered correction is not established"
                ),
                confidence_rationale=CONF,
            )
        )
    js(output / "revision_contexts.json", result)


def hashtext(text):
    return hashlib.sha256(text.encode()).hexdigest()


def state(value):
    return "unavailable" if value is None else "empty" if value == "" else "nonempty"


def controls(raw):
    try:
        obj = json.loads(raw)
    except (ValueError, TypeError):
        return {"document_state": "unavailable" if raw is None else "invalid"}
    if not isinstance(obj, dict):
        return {"document_state": "nonobject"}
    keys = [
        "duration",
        "multi_shots",
        "generate_audio",
        "is_inpaint",
        "model",
        "mode",
        "model_version",
        "resolution",
        "aspect_ratio",
    ]
    return {
        k: {
            "state": "absent"
            if k not in obj
            else "null"
            if obj[k] is None
            else "container"
            if isinstance(obj[k], (dict, list))
            else "scalar",
            "value": obj.get(k) if not isinstance(obj.get(k), (dict, list)) else None,
        }
        for k in keys
    }


def build(data, v1, v2, output):
    output.mkdir(parents=True, exist_ok=True)
    verify_manifest(data)
    verify_manifest(v1)
    subprocess.run(
        [sys.executable, str(ROOT / "prompt-labels/release.py"), "--check", str(v2)],
        check=True,
        capture_output=True,
    )
    upstream = ROOT / "studies/01-corpus/outputs"
    eligible = read(upstream / "eligibility.csv")
    eligible = eligible[eligible.study == 4]
    write(eligible, output / "eligibility.csv")
    ids = sorted(
        eligible.loc[
            (eligible.population == "primary") & eligible.production_eligible, "film_id"
        ]
    )
    assert len(ids) == 157
    taxonomy = read(upstream / "taxonomy.csv")
    tax = taxonomy[taxonomy.film_id.isin(ids)][
        ["film_id", "cohort_group", "record_orientation", "scale"]
    ]
    features = pd.read_parquet(v1 / "features.parquet")
    occ = pd.read_parquet(v1 / "occurrences.parquet")
    occurrences = occ[occ.film_id.isin(ids)].copy()
    with connect(data) as db:
        db.register("eligible", pd.DataFrame({"film_id": ids}))
        db.execute((HERE / "measures.sql").read_text())
        source = db.sql("SELECT * FROM text_fields").df()
        source = source.astype(object).where(pd.notna(source), None)
        assert (
            db.sql(
                "SELECT count(*) FROM generation_prompts p JOIN "
                "generations g USING(film_id,generation_id) "
                "WHERE p.field_path=g.prompt_source_path "
                "AND p.text IS DISTINCT FROM g.prompt"
            ).fetchone()[0]
            == 0
        )
        source["text_id"] = source.text.map(
            lambda t: hashtext(t) if t is not None and t != "" else None
        )
        nonempty = source[source.text_id.notna()]
        comparison = nonempty.merge(
            occurrences,
            on=["film_id", "generation_id", "field_path"],
            suffixes=("_source", "_v1"),
            validate="one_to_one",
        )
        assert len(comparison) == len(nonempty) == len(occurrences)
        assert (comparison.text_id_source == comparison.text_id_v1).all()
        assert (comparison.text_role_source == comparison.text_role_v1).all()
        jobs = db.sql("SELECT g.* FROM generations g JOIN eligible USING(film_id)").df()
        jobs = (
            jobs.astype(object)
            .where(pd.notna(jobs), None)
            .set_index(["film_id", "generation_id"])
        )
        context = db.sql("SELECT * FROM context_counts").df()
        records = [json.loads(line) for line in gzip.open(v2 / "labels.jsonl.gz", "rt")]
        # Independently verify every released positive span, including withholding.
        source_lookup = nonempty.set_index(["film_id", "generation_id", "field_path"])
        positive_spans = withheld_spans = 0
        for r in records:
            text = source_lookup.loc[
                (r["film_id"], r["generation_id"], r["field_path"]), "text"
            ]
            assert hashtext(text) == r["text_id"]
            if r["status"] == "success":
                for v in r["labels"].values():
                    if v["present"]:
                        positive_spans += 1
                        if v.get("span_withheld"):
                            withheld_spans += 1
                            assert v["span_sha256"] == hashtext(text)
                            assert v["span_characters"] == len(text)
                        else:
                            assert v["span"] in text and v["span"] != text
        panel(db, output, jobs, {r["text_id"]: r for r in records})
    f = features.copy()
    for key in FLAGS:
        if key in [
            "section",
            "reference",
            "camera",
            "lens",
            "preservation",
            "exclusion",
            "edit",
            "multi_shot",
        ]:
            f[key] = (f[key + "_matches"] > 0).astype(int)
        elif key == "long_text":
            f[key] = (~f.semantic_eligible).astype(int)
        else:
            f[key] = (f[key] > 0).astype(int)
    all_fields = occurrences.merge(
        f[["text_id", "characters", *FLAGS]], on="text_id", validate="many_to_one"
    )
    all_fields = all_fields.merge(
        context, on=["film_id", "generation_id"], how="left", validate="many_to_one"
    )
    all_fields["media_bound"] = (all_fields.media_inputs > 0).astype(int)
    all_fields["reference_bound"] = (all_fields.references > 0).astype(int)
    all_fields["metadata_nonempty"] = (all_fields.metadata_descriptions > 0).astype(int)
    flags = FLAGS + ["media_bound", "reference_bound", "metadata_nonempty"]
    dims = ["cohort_group", "record_orientation", "scale"]
    metric_rows = []
    primary = all_fields[all_fields.text_role == "primary"]
    film = (
        primary.groupby("film_id", sort=True)
        .agg(
            nonempty=("text_id", "size"),
            distinct_texts=("text_id", "nunique"),
            **{k: (k, "sum") for k in flags},
        )
        .reset_index()
        .merge(tax, on="film_id")
    )
    film["repeat_excess"] = film.nonempty - film.distinct_texts
    write(film, output / "film_metrics.csv")
    metrics = [(k, "nonempty") for k in flags + ["repeat_excess"]]
    write(summarize(film, metrics, dims), output / "summaries.csv")
    for dim, fields, prefix in [
        (dim, all_fields, "")
        for dim in ["generation_type", "model_identifier", "text_role"]
    ] + [(dim, primary, "primary_") for dim in ["generation_type", "model_identifier"]]:
        by = (
            fields.groupby(["film_id", dim], dropna=False, sort=True)
            .agg(
                nonempty=("text_id", "size"),
                distinct_texts=("text_id", "nunique"),
                **{k: (k, "sum") for k in flags},
            )
            .reset_index()
            .merge(tax, on="film_id")
        )
        write(by, output / f"{prefix}by_{dim}.csv")
        summary = []
        for value, g in by.groupby(dim, dropna=False, sort=True):
            s = summarize(g, [(k, "nonempty") for k in flags], ["cohort_group"])
            s[dim] = value
            summary.append(s)
        write(
            pd.concat(summary, ignore_index=True), output / f"{prefix}summary_{dim}.csv"
        )
    states = (
        source.assign(text_state=source.text.map(state))
        .groupby(["film_id", "text_role", "text_state"], dropna=False)
        .size()
        .rename("fields")
        .reset_index()
    )
    write(states, output / "field_states.csv")
    distinct = all_fields.drop_duplicates(["film_id", "text_id"])
    structural = (
        distinct.groupby("film_id")
        .agg(texts=("text_id", "size"), **{k: (k, "sum") for k in flags})
        .reset_index()
    )
    write(structural, output / "distinct_structural.csv")
    for row in film.to_dict("records"):
        metric_rows.append(
            evidence(
                row["film_id"],
                json.dumps(row, sort_keys=True),
                "primary fields; distinct all-role film/text for distinct_structural; "
                "literal row dimensions select all-role source fields",
                source=(
                    "generations; generation_prompts; asset_usages; "
                    "reference_elements; measures.sql; build.py"
                ),
            )
        )
    write(pd.DataFrame(metric_rows), output / "metric_evidence.csv")
    sample = label_rows(records)
    candidates = occurrences.merge(
        features[["text_id", "semantic_eligible"]], on="text_id"
    )
    candidates = candidates[candidates.semantic_eligible].drop_duplicates(
        STRATA + ["text_id"]
    )
    weighted, strata = weight_sample(sample, candidates)
    write(strata, output / "semantic_strata.csv")
    for c in COMPONENTS:
        weighted[c + "_weighted"] = weighted[c] * weighted.success_weight
        weighted[c + "_failure_low"] = weighted[c].fillna(0) * weighted.sample_weight
        weighted[c + "_failure_high"] = weighted[c].fillna(1) * weighted.sample_weight
    weighted["covered_mass"] = weighted.success_weight.where(weighted.success, 0)
    weighted["sample_mass"] = weighted.sample_weight
    numeric = ["success", "covered_mass", "sample_mass", *COMPONENTS]
    numeric += [
        c + suffix
        for c in COMPONENTS
        for suffix in ["_weighted", "_failure_low", "_failure_high"]
    ]
    # A positive component means explicit text only. Attachment and metadata
    # availability cannot identify properties carried by their content.
    linked = weighted.merge(
        context, on=["film_id", "generation_id"], validate="many_to_one"
    )
    matrix = []
    for fid, group in linked.groupby("film_id", sort=True):
        for c in COMPONENTS:
            ok = group[group.success]
            positive = ok[ok[c] == 1]
            matrix.append(
                dict(
                    film_id=fid,
                    component=c,
                    successful_texts=len(ok),
                    sampled_texts=len(group),
                    text_explicit=len(positive),
                    text_with_media=int((positive.media_inputs > 0).sum()),
                    text_with_reference=int((positive.references > 0).sum()),
                    text_with_description_field=int(
                        (positive.metadata_descriptions > 0).sum()
                    ),
                    weighted_text_explicit=float(positive.success_weight.sum()),
                    weighted_success_denominator=float(ok.success_weight.sum()),
                    media_property_content="unobservable",
                    metadata_property_assignment="not_coded",
                    contradiction="unadjudicated",
                )
            )
    write(pd.DataFrame(matrix), output / "information_matrix.csv")
    lexical = []
    for c, feature in [
        ("preservation", "preservation_matches"),
        ("exclusion", "exclusion_matches"),
        ("camera_motion", "camera_matches"),
        ("lens_framing", "lens_matches"),
    ]:
        paired = weighted[weighted.success].merge(
            features[["text_id", feature]], on="text_id"
        )
        for fid, group in paired.groupby("film_id", sort=True):
            lex = group[feature] > 0
            sem = group[c] == 1
            lexical.append(
                dict(
                    film_id=fid,
                    component=c,
                    successful_texts=len(group),
                    both=int((lex & sem).sum()),
                    lexical_only=int((lex & ~sem).sum()),
                    semantic_only=int((~lex & sem).sum()),
                    neither=int((~lex & ~sem).sum()),
                )
            )
    write(pd.DataFrame(lexical), output / "lexical_semantic.csv")
    report = json.loads((v2 / "report.json").read_text())
    agreement = []
    for comparison_name, comparison_report in report["agreement"].items():
        for c in COMPONENTS:
            a = comparison_report["per_component"][c]
            agreement.append(
                dict(
                    comparison=comparison_name,
                    component=c,
                    **{k: v for k, v in a.items() if not isinstance(v, (list, dict))},
                )
            )
    write(pd.DataFrame(agreement), output / "agreement.csv")
    # Per-film tables precede summaries; split by dimension to keep every file <1 MB.
    semantic_evidence = []
    for dim in [None, "generation_type", "model_identifier", "text_role"]:
        keys = ["film_id"] + ([dim] if dim else [])
        by = (
            weighted.groupby(keys, dropna=False, sort=True)[numeric]
            .sum(min_count=1)
            .reset_index()
        )
        counts = (
            weighted.groupby(keys, dropna=False).size().rename("sampled").reset_index()
        )
        by = by.merge(counts, on=keys).merge(tax, on="film_id")
        write(
            by, output / (f"semantic_by_{dim}.csv" if dim else "semantic_by_film.csv")
        )
        if dim is None:
            for row in by.to_dict("records"):
                semantic_evidence.append(
                    evidence(
                        row["film_id"],
                        json.dumps(row, sort_keys=True),
                        "successful assigned texts; covered stratum membership mass; "
                        "join semantic_strata and semantic_bounds for missingness",
                        label="inferred",
                        source=(
                            "prompt-labels-v2/labels.jsonl.gz; "
                            "prompt-labels-v1/occurrences.parquet; "
                            "build.py weight_sample"
                        ),
                    )
                )
        metrics = [(c + "_weighted", "covered_mass") for c in COMPONENTS]
        summaries = []
        groups = (
            [("all", by)]
            if dim is None
            else list(by.groupby(dim, dropna=False, sort=True))
        )
        for value, group in groups:
            s = summarize(group, metrics, ["cohort_group"])
            s["component"] = s.metric.str.removesuffix("_weighted")
            population_cache = {}
            for row_index, row in s.iterrows():
                members = (
                    group
                    if row.dimension == "all"
                    else group[group.cohort_group == row.value]
                )
                c = row.component
                s.loc[row_index, "successful_texts"] = members.success.sum()
                s.loc[row_index, "sampled_texts"] = members.sampled.sum()
                s.loc[row_index, "failures"] = (
                    members.sampled.sum() - members.success.sum()
                )
                cache_key = (row.dimension, row.value)
                if cache_key not in population_cache:
                    population = all_fields[all_fields.film_id.isin(members.film_id)]
                    if dim is not None:
                        population = population[population[dim] == value]
                    population = population.drop_duplicates(STRATA + ["text_id"])
                    population_cache[cache_key] = (
                        len(population),
                        population.long_text.sum(),
                    )
                total, long = population_cache[cache_key]
                s.loc[row_index, "population_memberships"] = total
                s.loc[row_index, "long_memberships"] = long
                # Excluded long-text component prevalence is unidentified in each
                # subgroup, independently of transported successful-text estimates.
                s.loc[row_index, "long_component_lower"] = 0
                s.loc[row_index, "long_component_upper"] = 1
                mass = members.sample_mass.sum()
                s.loc[row_index, "failure_low"] = (
                    members[c + "_failure_low"].sum() / mass if mass else None
                )
                s.loc[row_index, "failure_high"] = (
                    members[c + "_failure_high"].sum() / mass if mass else None
                )
            s["label_source"] = "27B provisional"
            s["agreement_source"] = "agreement.csv component join"
            s["long_text_bounds_source"] = "semantic_bounds.csv component join"
            s["conditioning"] = dim or "all"
            s["condition"] = value
            summaries.append(s)
        write(
            pd.concat(summaries, ignore_index=True),
            output / (f"semantic_summary_{dim}.csv" if dim else "semantic_summary.csv"),
        )
    write(pd.DataFrame(semantic_evidence), output / "semantic_evidence.csv")
    bounds = []
    covered = strata.loc[strata.successful > 0, "candidate_texts"].sum()
    sampled_mass = strata.loc[strata.sampled > 0, "candidate_texts"].sum()
    total_mass = strata.candidate_texts.sum()
    all_mass = occurrences.drop_duplicates(STRATA + ["text_id"]).shape[0]
    for c in COMPONENTS:
        lo, hi = weighted[c + "_failure_low"].sum(), weighted[c + "_failure_high"].sum()
        # Long and zero-sampled strata are free to be all absent/all present.
        bounds.append(
            dict(
                component=c,
                successes=int(sample.success.sum()),
                sampled=len(sample),
                present=int(sample[c].sum()),
                covered_stratum_mass=int(covered),
                sampled_stratum_mass=int(sampled_mass),
                eligible_stratum_mass=int(total_mass),
                all_length_stratum_mass=all_mass,
                weighted_sample_failure_low=lo / sampled_mass,
                weighted_sample_failure_high=hi / sampled_mass,
                eligible_missing_low=lo / total_mass,
                eligible_missing_high=(hi + total_mass - sampled_mass) / total_mass,
                all_length_missing_low=lo / all_mass,
                all_length_missing_high=(hi + all_mass - sampled_mass) / all_mass,
                raw_failure_low=int(sample[c].sum()) / len(sample),
                raw_failure_high=(
                    int(sample[c].sum()) + len(sample) - int(sample.success.sum())
                )
                / len(sample),
            )
        )
    write(pd.DataFrame(bounds), output / "semantic_bounds.csv")
    # Known global exclusions stay distinct from overlapping film/type/role mass.
    js(
        output / "coverage.json",
        dict(
            source_fields=len(source),
            nonempty_fields=len(nonempty),
            primary_fields=len(primary),
            globally_distinct_texts=occurrences.text_id.nunique(),
            crosswalk_matches=len(comparison),
            sample=report["coverage"],
            long_texts=report["long_text_bias"]["primary_text_weighted"],
            strata=len(strata),
            sampled_strata=int((strata.sampled > 0).sum()),
            successful_strata=int((strata.successful > 0).sum()),
            covered_stratum_mass=int(covered),
            eligible_stratum_mass=int(total_mass),
            all_length_stratum_mass=all_mass,
            source_span_checks=positive_spans,
            withheld_full_fields=withheld_spans,
        ),
    )
    inputs = [
        HERE / "build.py",
        HERE / "measures.sql",
        HERE / "context_contract.json",
        HERE / "taxonomy.json",
        HERE / "dependencies.csv",
        ROOT / "PROGRAMME.md",
        ROOT / "AGENTS.md",
    ]
    inputs += list(upstream.glob("*.csv"))
    inputs += [
        ROOT / f"studies/{n}/README.md"
        for n in [
            "01-corpus",
            "02-planning",
            "03-elements",
            "05-image",
            "06-video",
            "07-lineage",
            "08-workflow",
            "09-iteration",
            "10-organisation",
        ]
    ]
    inputs += [ROOT / "studies/09-iteration/outputs/revision_histories.json"]
    inputs += [
        ROOT / "prompt-labels" / n
        for n in ["README.md", "VALIDATION.md", "RELEASE.md", "release.py", "build.py"]
    ]
    inputs += [ROOT / "src/film_practice/prompt_labels.py"]
    for p in sorted((ROOT / "case-files").glob("*/codes.csv")):
        inputs += [p, p.with_name("CASE.md")]
    js(
        output / "reproduction.json",
        dict(
            source_manifests={
                n: digest(p / "SHA256SUMS")
                for n, p in [
                    ("data-2026-10-20", data),
                    ("prompt-labels-v1", v1),
                    ("prompt-labels-v2", v2),
                ]
            },
            inputs={str(p.relative_to(ROOT)): digest(p) for p in sorted(set(inputs))},
            outputs={
                p.name: digest(p)
                for p in sorted(output.iterdir())
                if p.name != "reproduction.json"
            },
        ),
    )
    assert all(p.stat().st_size < 1_000_000 for p in output.iterdir())
    print(
        f"Built {len(film)} films, {len(primary)} primary fields, "
        f"{len(sample)} sample records."
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--data", type=Path, default=Path("data"))
    p.add_argument("--v1", type=Path, default=Path("data/af11-labels-v1"))
    p.add_argument("--v2", type=Path, default=Path("data/af11-labels-v2"))
    p.add_argument("--output", type=Path, default=HERE / "outputs")
    p.add_argument("--check", action="store_true")
    a = p.parse_args()
    if a.check and a.output.resolve() == (HERE / "outputs").resolve():
        p.error("--check requires a separate output directory")
    build(a.data, a.v1, a.v2, a.output)
    if a.check:
        assert {q.name: digest(q) for q in a.output.iterdir()} == {
            q.name: digest(q) for q in (HERE / "outputs").iterdir()
        }
        print("All committed outputs reproduced byte for byte.")


if __name__ == "__main__":
    main()
