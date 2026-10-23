#!/usr/bin/env python3
"""Findings synthesis of Studies 01-10: cross-study analyses and citation checks.

Reads only committed study outputs and three verified derived releases
(prompt-labels-v1, prompt-labels-v2, study-07-v1). Every new number is written
to outputs/; every number cited from a study is checked against its committed
output by points.json. Nothing here is a tested best practice.
"""

import argparse
import gzip
import hashlib
import json
import re
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
NULL = r"\N"
STUDIES = ROOT / "studies"
COMPONENTS = [
    "subject",
    "identity",
    "action",
    "environment",
    "spatial",
    "composition",
    "lens_framing",
    "camera_motion",
    "lighting",
    "material",
    "aesthetic_intent",
    "timing",
    "exclusion",
    "preservation",
]
STRATA = ["film_id", "generation_type", "text_role"]
# Structural census flags: AF3a lexical features plus Study 07 graph bindings.
LEXICAL = {
    "reference_token": "reference_matches",
    "section": "section_matches",
    "camera": "camera_matches",
    "lens": "lens_matches",
    "preservation": "preservation_matches",
    "exclusion": "exclusion_matches",
    "edit": "edit_matches",
    "multi_shot": "multi_shot_matches",
    "repeated_lines": "repeated_lines",
}
BOOLEAN = {
    "structured_json": "structured_json",
    "long_description": "long_description_proxy",
    "short_edit": "short_edit_proxy",
}
FLAGS = ["attached_input", "named_reference", *LEXICAL, *BOOLEAN]
# Equality with Study 04's primary_by_generation_type.csv (same rules, same grain).
STUDY04_COLUMNS = {
    "attached_input": "media_bound",
    "named_reference": "reference_bound",
    "reference_token": "reference",
    "section": "section",
    "camera": "camera",
    "lens": "lens",
    "preservation": "preservation",
    "exclusion": "exclusion",
    "edit": "edit",
    "multi_shot": "multi_shot",
    "repeated_lines": "repeated_lines",
    "structured_json": "structured_json",
    "long_description": "long_description_proxy",
    "short_edit": "short_edit_proxy",
}
BUNDLES = {
    # A video request carrying the four most frequent structural traits together.
    "video_full_request": (
        "video",
        ["attached_input", "long_description", "camera", "exclusion"],
    ),
    # An image request asking for a change while naming what must stay.
    "image_change_with_keep": ("image", ["attached_input", "edit", "preservation"]),
}
STAGES = {
    "image_no_recorded_input": "Image jobs with no recorded input",
    "image_with_input": "Image jobs with at least one attached input",
    "image_multi_input": "Image jobs combining two or more input images",
    "image_foundation": "Image jobs whose output a video job takes as an image",
    "reference_preparation": "Jobs whose output is attached as a named reference",
    "video_from_image": "Video generation from attached images or frames",
    "video_from_video": "Video generation guided by an input video",
    "video_extension": "Declared extension of an input video",
    "video_text_candidate": "Video request with explicitly empty media",
    "finishing": "Editor, upscale and declared finishing jobs",
    "voice": "Voiceover, voice-change and lip-sync adapters",
}


def listed(directory):
    """Regular, non-hidden files of an output directory, by name."""
    return sorted(
        p for p in directory.iterdir() if p.is_file() and not p.name.startswith(".")
    )


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return pd.read_csv(path, keep_default_na=False, na_values=[NULL])


def read_strings(path):
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def write(frame, path):
    frame.to_csv(
        path, index=False, na_rep=NULL, float_format="%.9f", lineterminator="\n"
    )


def js(path, value):
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    )


def verify_release(directory, expected_assets=None, expected_manifest=None):
    """Check every listed asset, then pin the release by manifest or asset hashes."""
    listed = {}
    for line in (directory / "SHA256SUMS").read_text().splitlines():
        value, name = line.split("  ", 1)
        if digest(directory / name) != value:
            raise ValueError(f"Checksum mismatch: {directory.name}/{name}")
        listed[name] = value
    if expected_manifest and digest(directory / "SHA256SUMS") != expected_manifest:
        raise ValueError(f"Unexpected release manifest in {directory}")
    if expected_assets and listed != expected_assets:
        raise ValueError(f"Unexpected release assets in {directory}")
    return digest(directory / "SHA256SUMS")


def stats(rates):
    rates = pd.Series(rates, dtype=float).dropna()
    if rates.empty:
        return dict(equal_film_mean=None, median=None, q25=None, q75=None)
    return dict(
        equal_film_mean=rates.mean(),
        median=rates.median(),
        q25=rates.quantile(0.25),
        q75=rates.quantile(0.75),
    )


def share_summary(metric, task, model, eligible, num, den, note):
    """Per-film shares first; a film enters only with a positive denominator."""
    num = pd.Series(num, dtype=float).reset_index(drop=True)
    den = pd.Series(den, dtype=float).reset_index(drop=True)
    measured = den > 0
    total = den[measured].sum()
    return dict(
        metric=metric,
        task=task,
        model_identifier=model,
        eligible_films=eligible,
        measured_films=int(measured.sum()),
        positive_films=int((num[measured] > 0).sum()),
        numerator=num[measured].sum(),
        denominator=total,
        **stats(num[measured] / den[measured]),
        pooled_share=num[measured].sum() / total if total else None,
        note=note,
    )


def value_summary(metric, task, model, values, note):
    """Distribution of one per-film value (a count or a median), films equal."""
    values = pd.Series(values, dtype=float)
    return dict(
        metric=metric,
        task=task,
        model_identifier=model,
        eligible_films=len(values),
        measured_films=int(values.notna().sum()),
        **stats(values),
        note=note,
    )


# --------------------------------------------------------------------------
# Model preference by task and stage (committed Study 08/09/04 outputs)


def stage_counts(role):
    """Film x model x stage job counts from Study 08's role matrix."""
    image = role.generation_type == "image"
    video = role.video_candidate > 0
    route = role.route
    columns = {
        "image_no_recorded_input": role.no_recorded_media.where(image, 0),
        "image_with_input": role.media_bound.where(image, 0),
        "image_multi_input": role.jobs.where(image & (route == "image:multi_input"), 0),
        "image_foundation": role.image_foundation.where(image, 0),
        "reference_preparation": role.reference_preparation,
        "video_from_image": role.video_candidate.where(
            video & route.isin(["video:image_guided", "video:start_end"]), 0
        ),
        "video_from_video": role.video_candidate.where(
            video & (route == "video:video_guided"), 0
        ),
        "video_extension": role.video_candidate.where(
            video & (route == "video:extension"), 0
        ),
        "video_text_candidate": role.video_candidate.where(
            video & (route == "video:text_candidate"), 0
        ),
        "finishing": role.finishing_job,
        "voice": role.voice_adapter,
    }
    frame = role[["film_id", "model_identifier"]].copy()
    for name, column in columns.items():
        frame[name] = column.astype(int)
    frame = frame.groupby(["film_id", "model_identifier"], as_index=False).sum()
    return frame.melt(
        ["film_id", "model_identifier"], var_name="stage", value_name="jobs"
    ).query("jobs > 0")


def share_table(counts, group, item, eligible_films):
    """For each group, every item's per-film share among films with the group."""
    rows = []
    for key, part in counts.groupby(group, sort=True):
        film_total = part.groupby("film_id").jobs.sum()
        wide = part.pivot_table(
            index="film_id", columns=item, values="jobs", aggfunc="sum", fill_value=0
        ).reindex(film_total.index, fill_value=0)
        shares = wide.div(film_total, axis=0)
        top = shares.eq(shares.max(axis=1), axis=0)
        for name in sorted(wide.columns):
            rows.append(
                dict(
                    **{group: key, item: name},
                    eligible_films=eligible_films,
                    films_with_group=len(film_total),
                    films_using=int((wide[name] > 0).sum()),
                    top_films=int(top[name].sum()),
                    jobs=int(wide[name].sum()),
                    group_jobs=int(film_total.sum()),
                    **stats(shares[name]),
                    pooled_share=wide[name].sum() / film_total.sum(),
                )
            )
    return pd.DataFrame(rows)


def model_stages(role):
    counts = stage_counts(role)
    table = share_table(counts, "stage", "model_identifier", 157)
    table.insert(1, "stage_description", table.stage.map(STAGES))
    order = {s: i for i, s in enumerate(STAGES)}
    table = table.sort_values(
        ["stage", "jobs", "model_identifier"],
        key=lambda c: c.map(order) if c.name == "stage" else c,
        ascending=[True, False, True],
    )
    table = table.rename(columns={"films_with_group": "films_with_stage"})
    table = table.rename(columns={"group_jobs": "stage_jobs"})
    table["evidence_label"] = "observed counts under inferred Study 05/06/08 routes"
    return table.reset_index(drop=True)


def model_profiles(role, iteration, prompts):
    """What each literal model is used for, per film among films using it."""
    image = role.generation_type == "image"
    role = role.assign(
        multi_input=role.jobs.where(role.route == "image:multi_input", 0),
        image_foundation=role.image_foundation.where(image, 0),
    )
    job_measures = [
        ("no_recorded_input", "no_recorded_media"),
        ("attached_input", "media_bound"),
        ("multi_input", "multi_input"),
        ("consumes_recorded_output", "chained"),
        ("consumes_other_model_output", "cross_model"),
        ("output_feeds_video", "image_foundation"),
        ("output_becomes_named_reference", "reference_preparation"),
    ]
    per = role.groupby(["film_id", "model_identifier", "generation_type"]).sum(
        numeric_only=True
    )
    per = per.reset_index()
    it = iteration.set_index(["film_id", "model_identifier"])
    pr = prompts.set_index(["film_id", "model_identifier"])
    key = pd.MultiIndex.from_frame(per[["film_id", "model_identifier"]])
    for name, column in [
        ("output_used_later", "adopted"),
        ("multi_job_batch", "batch_member"),
        ("rerun_candidate", "rerun_candidate"),
    ]:
        per[name] = it[column].reindex(key).to_numpy()
        job_measures.append((name, name))
    if per[[name for name, _ in job_measures[-3:]]].isna().any().any():
        raise ValueError("Study 09 lacks a film/model present in Study 08")
    # Films whose jobs under a model all lack nonempty text have no text rate.
    per["text_fields"] = pr["nonempty"].reindex(key).fillna(0).to_numpy()
    per["long_description"] = pr["long_description_proxy"].reindex(key).to_numpy()
    per["short_edit"] = pr["short_edit_proxy"].reindex(key).to_numpy()
    rows = []
    for (model, kind), part in per.groupby(["model_identifier", "generation_type"]):
        for measure, column in job_measures:
            rows.append(
                share_summary(
                    measure, kind, model, len(part), part[column], part.jobs, "jobs"
                )
            )
        for measure in ["long_description", "short_edit"]:
            rows.append(
                share_summary(
                    measure,
                    kind,
                    model,
                    len(part),
                    part[measure].fillna(0),
                    part.text_fields,
                    "nonempty primary fields",
                )
            )
    table = pd.DataFrame(rows).rename(
        columns=dict(
            task="generation_type",
            eligible_films="films_using_model",
            note="denominator_name",
        )
    )
    return table.sort_values(["generation_type", "model_identifier", "metric"])


def model_concentration(inventory):
    rows = []
    for (film, kind), part in inventory.groupby(["film_id", "generation_type"]):
        if kind not in ("image", "video"):
            continue
        jobs = part.groupby("model_identifier").jobs.sum()
        ordered = jobs.sort_index().sort_values(ascending=False, kind="stable")
        rows.append(
            dict(
                film_id=film,
                generation_type=kind,
                jobs=int(jobs.sum()),
                models=int((jobs > 0).sum()),
                top_model=ordered.index[0],
                top_model_jobs=int(ordered.iloc[0]),
                seedance_2_5_jobs=int(jobs.get("seedance_2_5", 0)),
            )
        )
    return pd.DataFrame(rows).sort_values(["film_id", "generation_type"])


def handoffs(transitions, inventory, role):
    kinds = inventory.groupby("model_identifier").generation_type.first()
    finishing = set(role.loc[role.finishing_job > 0, "model_identifier"])
    voice = set(role.loc[role.voice_adapter > 0, "model_identifier"])
    t = transitions.assign(
        producer_type=transitions.producer_model.map(kinds),
        consumer_type=transitions.consumer_model.map(kinds),
    )
    adapter = t.consumer_model.isin(finishing | voice)
    groups = {
        "image_to_video_generation": (t.producer_type == "image")
        & (t.consumer_type == "video")
        & ~adapter,
        "video_to_video_generation": (t.producer_type == "video")
        & (t.consumer_type == "video")
        & ~adapter,
        "image_to_image": (t.producer_type == "image") & (t.consumer_type == "image"),
        "into_finishing": t.consumer_model.isin(finishing),
    }
    tables = []
    for name, mask in groups.items():
        for side in ["producer_model", "consumer_model"]:
            part = t[mask].rename(columns={"pairs": "jobs"})
            part = part.assign(handoff=name)[["handoff", "film_id", side, "jobs"]]
            table = share_table(
                part.rename(columns={side: "model_identifier"}),
                "handoff",
                "model_identifier",
                157,
            )
            tables.append(table.assign(side=side.removesuffix("_model")))
    table = pd.concat(tables, ignore_index=True)
    table = table.rename(
        columns=dict(
            films_with_group="films_with_handoff",
            group_jobs="handoff_pairs",
            jobs="pairs",
        )
    )
    table["evidence_label"] = "observed explicit producer/asset/consumer pairs"
    columns = ["handoff", "side", *[c for c in table if c not in ("handoff", "side")]]
    return table[columns].sort_values(
        ["handoff", "side", "pairs", "model_identifier"],
        ascending=[True, True, False, True],
    )


# --------------------------------------------------------------------------
# Techniques: structural census over every nonempty primary field


def census(v1, study07):
    db = duckdb.connect()
    edges = str(study07 / "edges.csv.gz").replace("'", "''")
    db.execute(
        "CREATE VIEW edges AS SELECT * FROM read_csv("
        f"'{edges}', all_varchar=true, nullstr='\\N', header=true)"
    )
    occ = str(v1 / "occurrences.parquet").replace("'", "''")
    feat = str(v1 / "features.parquet").replace("'", "''")
    lexical = ", ".join(f"(f.{c} > 0) AS {n}" for n, c in LEXICAL.items())
    boolean = ", ".join(f"f.{c} AS {n}" for n, c in BOOLEAN.items())
    frame = db.sql(f"""
        WITH bound AS (
          SELECT DISTINCT film_id, target_id AS generation_id, edge_type
          FROM edges WHERE target_kind = 'generation'
            AND edge_type IN ('media_input', 'reference_binding'))
        SELECT o.film_id, o.generation_id, o.generation_type, o.model_identifier,
               f.characters,
               EXISTS (SELECT 1 FROM bound b WHERE b.film_id = o.film_id
                 AND b.generation_id = o.generation_id
                 AND b.edge_type = 'media_input') AS attached_input,
               EXISTS (SELECT 1 FROM bound b WHERE b.film_id = o.film_id
                 AND b.generation_id = o.generation_id
                 AND b.edge_type = 'reference_binding') AS named_reference,
               {lexical}, {boolean}
        FROM read_parquet('{occ}') o JOIN read_parquet('{feat}') f USING (text_id)
        WHERE o.text_role = 'primary' AND o.source_table = 'generations'
          AND o.population = 'primary'
        ORDER BY o.film_id, o.generation_id""").df()
    db.close()
    if frame.duplicated(["film_id", "generation_id"]).any():
        raise ValueError("A job has two primary fields")
    frame[FLAGS] = frame[FLAGS].astype(bool)
    return frame


def check_census(frame, study04):
    sums = frame.groupby(["film_id", "generation_type"])[FLAGS].sum()
    sums["nonempty"] = frame.groupby(["film_id", "generation_type"]).size()
    expected = study04.set_index(["film_id", "generation_type"])
    columns = {"nonempty": "nonempty", **STUDY04_COLUMNS}
    for ours, theirs in columns.items():
        left = sums[ours].astype(int)
        right = expected[theirs].reindex(left.index).astype(int)
        if not left.equals(right) or len(expected) != len(left):
            raise ValueError(f"Census disagrees with Study 04 on {ours}")


def technique_by_film(frame):
    group = frame.groupby(["film_id", "generation_type"])
    table = group[FLAGS].sum().astype(int)
    table.insert(0, "nonempty_fields", group.size())
    table.insert(1, "median_characters", group.characters.median())
    for name, (kind, flags) in BUNDLES.items():
        hit = frame[flags].all(axis=1) & (frame.generation_type == kind)
        table[name] = hit.groupby([frame.film_id, frame.generation_type]).sum()
    return table.reset_index()


def pair_rows(matrix_by_film, names, task, weighted):
    """Conditional co-occurrence P(B|A) per film, beside P(B) in the same films."""
    rows = []
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            if i == j:
                continue
            given, base = [], []
            n_a = n_ab = n_b = n = 0.0
            for co, total in matrix_by_film:
                if co[i, i] <= 0:
                    continue
                given.append(co[i, j] / co[i, i])
                base.append(co[j, j] / total)
                n_a, n_ab = n_a + co[i, i], n_ab + co[i, j]
                n_b, n = n_b + co[j, j], n + total
            given, base = pd.Series(given, dtype=float), pd.Series(base, dtype=float)
            rows.append(
                dict(
                    task=task,
                    given=a,
                    also=b,
                    films_with_given=len(given),
                    given_mass=n_a,
                    both_mass=n_ab,
                    also_mass=n_b,
                    total_mass=n,
                    mean_share_given=given.mean() if len(given) else None,
                    median_share_given=given.median() if len(given) else None,
                    mean_share_same_films=base.mean() if len(base) else None,
                    mean_difference=(given - base).mean() if len(given) else None,
                    pooled_share_given=n_ab / n_a if n_a else None,
                    pooled_share_same_films=n_b / n if n else None,
                    weighting="stratum weight N_s/r_s" if weighted else "none",
                )
            )
    return rows


def technique_pairs(frame):
    rows = []
    for task in ["image", "video"]:
        part = frame[frame.generation_type == task]
        matrices = []
        for _, film in part.groupby("film_id", sort=True):
            x = film[FLAGS].to_numpy(dtype=float)
            matrices.append((x.T @ x, float(len(x))))
        rows += pair_rows(matrices, FLAGS, task, weighted=False)
    table = pd.DataFrame(rows)
    table["evidence_label"] = "observed lexical/binding co-occurrence"
    return table


# --------------------------------------------------------------------------
# Techniques: provisional semantic co-occurrence on the weighted 27B sample


def semantic_sample(v2, strata, by_film):
    rows = []
    with gzip.open(v2 / "labels.jsonl.gz", "rt", encoding="utf-8") as handle:
        for line in handle:
            r = json.loads(line)
            item = {k: r[k] for k in [*STRATA, "text_id", "status"]}
            item["success"] = r["status"] == "success"
            for c in COMPONENTS:
                item[c] = int(r["labels"][c]["present"]) if item["success"] else None
            rows.append(item)
    sample = pd.DataFrame(rows).merge(strata, on=STRATA, validate="many_to_one")
    ok = sample[sample.success].copy()
    # Reproduce Study 04's per-film weighted masses before any new use of them.
    expected = by_film.set_index("film_id")
    mass = ok.success_weight.groupby(ok.film_id).sum()
    checks = {"covered_mass": mass}
    for c in COMPONENTS:
        checks[c + "_weighted"] = (ok[c] * ok.success_weight).groupby(ok.film_id).sum()
    for column, values in checks.items():
        if not np.allclose(values.reindex(expected.index), expected[column]):
            raise ValueError(f"Weights disagree with Study 04 on {column}")
    return ok


def semantic_tables(ok):
    rows, breadth = [], []
    primary = ok[ok.text_role == "primary"]
    for task in ["image", "video"]:
        part = primary[primary.generation_type == task]
        matrices = []
        for film, group in part.groupby("film_id", sort=True):
            x = group[COMPONENTS].to_numpy(dtype=float)
            w = group.success_weight.to_numpy(dtype=float)
            matrices.append((x.T @ (w[:, None] * x), float(w.sum())))
            count = x.sum(axis=1)
            breadth.append(
                dict(
                    film_id=film,
                    generation_type=task,
                    successful_texts=len(group),
                    covered_mass=w.sum(),
                    weighted_mean_components=float((w * count).sum() / w.sum()),
                )
            )
        rows += pair_rows(matrices, COMPONENTS, task, weighted=True)
    pairs = pd.DataFrame(rows)
    pairs["evidence_label"] = "inferred provisional 27B labels, Study 04 weights"
    return pairs, pd.DataFrame(breadth)


# --------------------------------------------------------------------------
# Headline summaries of the new analyses


def summaries(concentration, by_film, semantic_breadth):
    rows = []
    for kind in ["image", "video"]:
        c = concentration[concentration.generation_type == kind]
        rows.append(
            value_summary(
                f"{kind}_models_per_film",
                kind,
                None,
                c.models,
                "distinct literal models per film with that job type",
            )
        )
        rows.append(
            share_summary(
                f"{kind}_top_model_share",
                kind,
                None,
                len(c),
                c.top_model_jobs,
                c.jobs,
                "share of the film's jobs of that type on its most-used model",
            )
        )
        part = by_film[by_film.generation_type == kind]
        rows.append(
            value_summary(
                f"{kind}_median_characters",
                kind,
                None,
                part.median_characters,
                "per-film median characters of nonempty primary fields",
            )
        )
    v = concentration[concentration.generation_type == "video"]
    one = pd.Series(1, index=v.index)
    rows.append(
        share_summary(
            "seedance_2_5_video_share",
            "video",
            "seedance_2_5",
            len(v),
            v.seedance_2_5_jobs,
            v.jobs,
            "share of the film's video jobs; films without the model count 0",
        )
    )
    for threshold in [0.5, 0.9]:
        hit = (v.seedance_2_5_jobs / v.jobs >= threshold).astype(int)
        rows.append(
            share_summary(
                f"films_seedance_2_5_at_least_{round(threshold * 100)}pct",
                "video",
                "seedance_2_5",
                len(v),
                hit,
                one,
                "films whose video jobs reach this seedance_2_5 share",
            )
        )
    rows.append(
        share_summary(
            "films_top_video_model_seedance_2_5",
            "video",
            "seedance_2_5",
            len(v),
            (v.top_model == "seedance_2_5").astype(int),
            one,
            "films whose most-used video model is seedance_2_5",
        )
    )
    for name, (kind, _) in BUNDLES.items():
        part = by_film[by_film.generation_type == kind]
        rows.append(
            share_summary(
                name,
                kind,
                None,
                len(part),
                part[name],
                part.nonempty_fields,
                "nonempty primary fields with every listed trait",
            )
        )
    for flag in FLAGS:
        for kind in ["image", "video"]:
            part = by_film[by_film.generation_type == kind]
            rows.append(
                share_summary(
                    flag,
                    kind,
                    None,
                    len(part),
                    part[flag],
                    part.nonempty_fields,
                    "nonempty primary fields",
                )
            )
    for kind in ["image", "video"]:
        part = semantic_breadth[semantic_breadth.generation_type == kind]
        rows.append(
            value_summary(
                "semantic_components_per_text",
                kind,
                None,
                part.weighted_mean_components,
                "27B provisional labels, Study 04 stratum weights, primary role",
            )
        )
    return pd.DataFrame(rows)


def label_agreement(agreement):
    """Pool Study 04's per-component agreement counts into one kappa per pair."""
    rows = []
    for comparison, part in agreement.groupby("comparison", sort=True):
        a = part.both_present.sum()
        d = part.both_absent.sum()
        b = part.left_only_present.sum()
        c = part.right_only_present.sum()
        n = a + b + c + d
        observed_share = (a + d) / n
        left, right = (a + b) / n, (a + c) / n
        chance = left * right + (1 - left) * (1 - right)
        rows.append(
            dict(
                comparison=comparison,
                components=len(part),
                texts=int(part.n.iloc[0]),
                decisions=int(n),
                agreeing=int(a + d),
                accuracy=observed_share,
                pooled_kappa=(observed_share - chance) / (1 - chance),
            )
        )
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Citation checks and the point register


LABELS = {
    "observed",
    "creator-stated",
    "inferred",
    "associated",
    "experimentally supported",
    "proposed",
}
KIND_ORDER = {"pattern": 0, "model": 1, "technique": 2, "limit": 3}
KIND_TITLES = {
    "pattern": "Main patterns",
    "model": "Model preferences",
    "technique": "Techniques and tips",
    "limit": "What the evidence cannot tell",
}
FORMATS = {
    "pct": lambda v: f"{v * 100:.2f}%",
    "int": lambda v: f"{round(v):,}",
    "f1": lambda v: f"{v:.1f}",
    "f2": lambda v: f"{v:.2f}",
    "f3": lambda v: f"{v:.3f}",
}
PLACEHOLDER = re.compile(r"\{\{([a-z0-9:-]+)\}\}")
# Text fields that may carry {{citation}} placeholders.
TEXT_FIELDS = [
    "finding",
    "frequency",
    "evidence_note",
    "strength",
    "study04",
    "denominator",
    "competing_explanation",
    "confidence",
]
POINT_FIELDS = [
    "id",
    "kind",
    "rank",
    "title",
    "finding",
    "frequency",
    "stage",
    "models",
    "evidence_label",
    "evidence_note",
    "strength",
    "study04",
    "studies",
    "sources",
    "example",
    "denominator",
    "competing_explanation",
    "confidence",
    "numbers",
]


def located(name, output):
    # Synthesis outputs are read from the directory being built, so --check
    # verifies citations against the fresh build rather than the committed copy.
    local = "synthesis/outputs/"
    return output / name[len(local) :] if name.startswith(local) else ROOT / name


def observed(spec, output):
    path = located(spec["file"], output)
    if path.suffix == ".json":
        value = json.loads(path.read_text())
        for key in spec["key"].split("."):
            value = value[key]
        return float(value)
    # Selectors match the literal CSV text, so typed parsing cannot change them.
    frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    for column, wanted in spec.get("where", {}).items():
        if isinstance(wanted, dict):
            numbers = pd.to_numeric(frame[column], errors="coerce")
            frame = frame[numbers > wanted["gt"]]
        else:
            frame = frame[frame[column] == str(wanted)]
    if spec.get("aggregate") == "count":
        return float(len(frame))
    values = pd.to_numeric(frame[spec["column"]])
    if spec.get("aggregate") == "sum":
        return float(values.sum())
    if len(frame) != 1:
        raise ValueError(f"{spec['id']}: {len(frame)} rows match")
    return float(values.iloc[0])


def citations(points, output):
    rows = []
    for point in points["points"]:
        for spec in point["numbers"]:
            value = observed(spec, output)
            places = spec["round"]
            rows.append(
                dict(
                    point_id=point["id"],
                    citation_id=spec["id"],
                    label=spec["label"],
                    file=spec["file"],
                    selector=json.dumps(
                        spec.get("where", spec.get("key", {})), sort_keys=True
                    ),
                    column=spec.get("column", NULL),
                    aggregate=spec.get("aggregate", "value"),
                    cited=spec["value"],
                    observed=round(value, 9),
                    round=places,
                    format=spec["format"],
                    display=FORMATS[spec["format"]](value),
                    matches=round(value, places) == round(spec["value"], places),
                )
            )
    columns = [
        "point_id",
        "citation_id",
        "label",
        "file",
        "selector",
        "column",
        "aggregate",
        "cited",
        "observed",
        "round",
        "format",
        "display",
        "matches",
    ]
    table = pd.DataFrame(rows, columns=columns)
    bad = table[~table.matches.astype(bool)]
    if len(bad):
        raise ValueError("Cited numbers disagree:\n" + bad.to_string())
    if table.citation_id.duplicated().any():
        raise ValueError("Duplicate citation IDs")
    return table


def displays(points, table):
    values = dict(zip(table.citation_id, table.display, strict=True))
    values["points-total"] = str(len(points["points"]))
    for label in sorted(LABELS):
        count = sum(p["evidence_label"] == label for p in points["points"])
        values["points-" + label.replace(" ", "-")] = str(count)
    for kind in KIND_ORDER:
        count = sum(p["kind"] == kind for p in points["points"])
        values["points-" + kind] = str(count)
    return values


def fill(text, values):
    def replace(match):
        if match.group(1) not in values:
            raise ValueError(f"Unknown placeholder {match.group(0)}")
        return values[match.group(1)]

    return PLACEHOLDER.sub(replace, text)


def check_points(points):
    seen, ranks = set(), set()
    for point in points["points"]:
        missing = [f for f in POINT_FIELDS if f not in point]
        if missing:
            raise ValueError(f"{point.get('id')}: missing {missing}")
        if point["id"] in seen:
            raise ValueError(f"Duplicate point ID {point['id']}")
        seen.add(point["id"])
        if point["kind"] not in KIND_ORDER:
            raise ValueError(f"{point['id']}: unknown kind")
        if (point["kind"], point["rank"]) in ranks:
            raise ValueError(f"{point['id']}: duplicate rank")
        ranks.add((point["kind"], point["rank"]))
        if point["evidence_label"] not in LABELS:
            raise ValueError(f"{point['id']}: unknown evidence label")
        for path in point["sources"]:
            if not (ROOT / path.split("#")[0]).exists():
                raise ValueError(f"{point['id']}: missing source {path}")
        text = " ".join(point[f] for f in TEXT_FIELDS)
        used = set(PLACEHOLDER.findall(text))
        for spec in point["numbers"]:
            if spec["id"] not in used:
                raise ValueError(f"{point['id']}: citation {spec['id']} unused")


def point_register(points, table):
    values = displays(points, table)
    rows = []
    for point in points["points"]:
        text = {f: fill(point[f], values) for f in TEXT_FIELDS}
        example = point["example"]
        rows.append(
            dict(
                point_id=point["id"],
                kind=point["kind"],
                rank=point["rank"],
                title=point["title"],
                finding=text["finding"],
                frequency=text["frequency"],
                stage=point["stage"],
                literal_models=";".join(point["models"]),
                evidence_label=point["evidence_label"],
                evidence_note=text["evidence_note"],
                strength=text["strength"],
                study04_status=text["study04"],
                studies=";".join(point["studies"]),
                sources=";".join(point["sources"]),
                example_film_id=example["film_id"],
                example_entities=example["entities"],
                example_source_path=example["source_path"],
                example_excerpt=example["excerpt"],
                denominator=text["denominator"],
                competing_explanation=text["competing_explanation"],
                confidence_rationale=text["confidence"],
                citations=";".join(n["id"] for n in point["numbers"]),
            )
        )
    table = pd.DataFrame(rows)
    order = table.kind.map(KIND_ORDER) * 1000 + table["rank"].astype(int)
    return table.iloc[np.argsort(order.to_numpy(), kind="stable")]


def link(path):
    target = (
        path[len("synthesis/") :] if path.startswith("synthesis/") else "../" + path
    )
    return f"[`{path.split('#')[0]}`]({target})"


def render_point(point, values):
    t = {f: fill(point[f], values) for f in TEXT_FIELDS}
    example = point["example"]
    models = ", ".join(f"`{m}`" for m in point["models"]) or "none named"
    checks = ", ".join(f"`{n['id']}`" for n in point["numbers"]) or "none"
    lines = [
        f"### {point['id']}. {point['title']}",
        "",
        t["finding"],
        "",
        f"- **How often:** {t['frequency']}",
        f"- **Where:** {point['stage']}. Literal models: {models}.",
        f"- **Evidence:** {point['evidence_label']}. {t['evidence_note']}",
        f"- **Strength:** {t['strength']}.",
        f"- **Study 04 status:** {t['study04']}",
        f"- **Example:** film {example['film_id']}; {example['entities']}; "
        f"source `{example['source_path']}`; excerpt: {example['excerpt']}",
        f"- **Denominator:** {t['denominator']}.",
        f"- **Competing explanation:** {t['competing_explanation']}",
        f"- **Confidence:** {t['confidence']}",
        "- **Rests on:** "
        + ", ".join(link(s) for s in point["sources"])
        + f"; checked numbers {checks} in [`citations.csv`](outputs/citations.csv).",
    ]
    return "\n".join(lines)


def readme(points, table):
    """Render README.md from its template, filling only checked numbers."""
    values = displays(points, table)
    ordered = sorted(points["points"], key=lambda p: (KIND_ORDER[p["kind"]], p["rank"]))
    for kind in KIND_ORDER:
        values["section:" + kind] = "\n\n".join(
            render_point(p, values) for p in ordered if p["kind"] == kind
        )
    return fill((HERE / "README.template.md").read_text(), values)


# --------------------------------------------------------------------------


def committed_inputs(points):
    cited = {
        ROOT / spec["file"]
        for point in points["points"]
        for spec in point["numbers"]
        if not spec["file"].startswith("synthesis/")
    }
    return sorted(
        set(
            [
                STUDIES / "04-prompts/outputs/primary_by_generation_type.csv",
                STUDIES / "04-prompts/outputs/primary_by_model_identifier.csv",
                STUDIES / "04-prompts/outputs/semantic_strata.csv",
                STUDIES / "04-prompts/outputs/semantic_by_film.csv",
                STUDIES / "04-prompts/outputs/agreement.csv",
                STUDIES / "04-prompts/outputs/reproduction.json",
                STUDIES / "07-lineage/outputs/release_manifest.json",
                STUDIES / "08-workflow/outputs/role_matrix.csv",
                STUDIES / "08-workflow/outputs/model_inventory.csv",
                STUDIES / "08-workflow/outputs/transitions.csv",
                STUDIES / "09-iteration/outputs/by_model_identifier.csv",
                HERE / "build.py",
                HERE / "points.json",
                HERE / "README.template.md",
            ]
        )
        | cited
    )


def build(v1, v2, study07, output):
    output.mkdir(parents=True, exist_ok=True)
    pinned = json.loads((STUDIES / "04-prompts/outputs/reproduction.json").read_text())[
        "source_manifests"
    ]
    graph = json.loads(
        (STUDIES / "07-lineage/outputs/release_manifest.json").read_text()
    )["assets"]
    releases = {
        "prompt-labels-v1": verify_release(
            v1, expected_manifest=pinned["prompt-labels-v1"]
        ),
        "prompt-labels-v2": verify_release(
            v2, expected_manifest=pinned["prompt-labels-v2"]
        ),
        "study-07-v1": verify_release(
            study07, expected_assets={k: v["sha256"] for k, v in graph.items()}
        ),
    }
    role = read(STUDIES / "08-workflow/outputs/role_matrix.csv")
    inventory = read(STUDIES / "08-workflow/outputs/model_inventory.csv")
    transitions = read(STUDIES / "08-workflow/outputs/transitions.csv")
    iteration = read(STUDIES / "09-iteration/outputs/by_model_identifier.csv")
    prompts = read(STUDIES / "04-prompts/outputs/primary_by_model_identifier.csv")
    primary_types = read(STUDIES / "04-prompts/outputs/primary_by_generation_type.csv")
    strata = read(STUDIES / "04-prompts/outputs/semantic_strata.csv")
    semantic_film = read(STUDIES / "04-prompts/outputs/semantic_by_film.csv")

    concentration = model_concentration(inventory)
    write(concentration, output / "model_concentration.csv")
    write(model_stages(role), output / "model_stages.csv")
    write(model_profiles(role, iteration, prompts), output / "model_profiles.csv")
    write(handoffs(transitions, inventory, role), output / "model_handoffs.csv")

    frame = census(v1, study07)
    check_census(frame, primary_types)
    by_film = technique_by_film(frame)
    write(by_film, output / "technique_by_film.csv")
    write(technique_pairs(frame), output / "technique_pairs.csv")

    ok = semantic_sample(v2, strata, semantic_film)
    pairs, breadth = semantic_tables(ok)
    write(pairs, output / "semantic_pairs.csv")
    write(breadth, output / "semantic_breadth.csv")
    write(summaries(concentration, by_film, breadth), output / "summaries.csv")
    agreement = read(STUDIES / "04-prompts/outputs/agreement.csv")
    write(label_agreement(agreement), output / "label_agreement.csv")

    # Citations check committed study outputs and the summaries just written.
    points = json.loads((HERE / "points.json").read_text())
    check_points(points)
    table = citations(points, output)
    write(point_register(points, table), output / "points.csv")
    write(table, output / "citations.csv")

    outputs = {
        p.name: digest(p) for p in listed(output) if p.name != "reproduction.json"
    }
    js(
        output / "reproduction.json",
        dict(
            releases=releases,
            inputs={
                str(p.relative_to(ROOT)): digest(p) for p in committed_inputs(points)
            },
            outputs=outputs,
        ),
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--v1", type=Path, default=Path("data/prompt-labels-v1"))
    p.add_argument("--v2", type=Path, default=Path("data/prompt-labels-v2"))
    p.add_argument("--study07", type=Path, default=Path("data/study-07-v1"))
    p.add_argument("--output", type=Path, default=HERE / "outputs")
    p.add_argument("--check", action="store_true")
    a = p.parse_args()
    if a.check and a.output.resolve() == (HERE / "outputs").resolve():
        p.error("--check requires a separate output directory")
    build(a.v1, a.v2, a.study07, a.output)
    points = json.loads((HERE / "points.json").read_text())
    text = readme(points, read_strings(a.output / "citations.csv"))
    if not a.check:
        (HERE / "README.md").write_text(text)
        return
    produced = {q.name: digest(q) for q in listed(a.output)}
    committed = {q.name: digest(q) for q in listed(HERE / "outputs")}
    if produced != committed:
        raise SystemExit("Outputs differ from the committed synthesis outputs")
    if text != (HERE / "README.md").read_text():
        raise SystemExit("README.md differs from the rendered template")
    print("All committed synthesis outputs and README.md reproduced byte for byte.")


if __name__ == "__main__":
    main()
