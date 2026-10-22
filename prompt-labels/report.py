"""Read-only AF3b collection, exact-span checks and descriptive report data."""

import argparse
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import agreement
import crosscheck
import pandas as pd

from film_practice import connect
from film_practice.prompt_labels import COMPONENTS, canonical, load_text, validate

SOURCE_KEYS = (
    "text_id",
    "film_id",
    "generation_id",
    "field_path",
    "source_table",
    "source_record_file",
    "generation_type",
    "text_role",
    "model_identifier",
    "population",
)
RUN_KEYS = (
    "run_sha256",
    "labels_version",
    "requested_model",
    "request_settings",
    "template_sha256",
    "max_attempts",
    "timeout_seconds",
    "codebook_version",
    "span_resolution",
    "study",
    "code_id",
    "provisional",
    "evidence_label",
    "denominator",
    "competing_explanation",
    "confidence_rationale",
)


def read_rows(path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as stream:
        rows = [json.loads(line) for line in stream if line.strip()]
    result = {row["text_id"]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError("duplicate_text_id")
    return result


def snapshot(path):
    """Bound the read at the initial size; ignore only an unterminated tail.

    Never use the harness's recover(): that function truncates the live file.
    Hash precisely the consumed, newline-terminated prefix for reproducibility.
    """
    with path.open("rb") as stream:
        size = path.stat().st_size
        raw = stream.read(size)
    end = raw.rfind(b"\n") + 1
    prefix = raw[:end]
    try:
        rows = [json.loads(line) for line in prefix.split(b"\n")[:-1]]
    except (ValueError, UnicodeError):
        raise ValueError("malformed_complete_journal_line") from None
    return rows, {
        "sha256": hashlib.sha256(prefix).hexdigest(),
        "consumed_bytes": len(prefix),
        "ignored_tail_bytes": len(raw) - end,
        "records": len(rows),
    }


def check_source(row, sample):
    key = row["text_id"]
    if key not in sample:
        raise ValueError("text_outside_sample")
    if any(row.get(name) != sample[key].get(name) for name in SOURCE_KEYS):
        raise ValueError("source_metadata_mismatch")


def collect(paths, sample, kind="primary"):
    """Last terminal event wins within a shard; overlapping shards are errors.

    Duplicate terminal events for one (text, attempt) are errors too. A started
    retry does not erase the previous terminal event; pending attempts stay visible.
    """
    final, pending, inputs = {}, {}, []
    configuration = None
    owners = {}
    for index, path in enumerate(paths):
        rows, info = snapshot(path)
        inputs.append({"input_index": index, **info})
        seen = set()
        previous_attempt = {}
        for row in rows:
            check_source(row, sample)
            key = row["text_id"]
            if key in owners and owners[key] != index:
                raise ValueError("duplicate_final_record_across_journals")
            owners[key] = index
            config = (
                tuple(canonical(row.get(name)) for name in RUN_KEYS)
                if kind == "primary"
                else (row.get("configuration_sha256"),)
            )
            if (
                kind == "primary"
                and any(not row.get(name) for name in ("run_sha256", "labels_version"))
            ) or (kind == "jev" and not config[0]):
                raise ValueError("missing_run_configuration")
            if configuration is None:
                configuration = config
            if config != configuration:
                raise ValueError("mixed_run_configuration")
            attempt = row.get("attempt")
            if type(attempt) is not int or attempt < 1:
                raise ValueError("invalid_attempt")
            if attempt < previous_attempt.get(key, 0):
                raise ValueError("out_of_order_attempt")
            previous_attempt[key] = attempt
            status = row.get("status")
            if status == "started":
                pending[key] = attempt
                continue
            if status not in ("success", "failure"):
                raise ValueError("invalid_status")
            if (key, attempt) in seen:
                raise ValueError("duplicate_final_record")
            seen.add((key, attempt))
            final[key] = row
            pending.pop(key, None)
    return final, {"inputs": inputs, "pending_attempts": pending}


def presence(rows, kind="primary"):
    result = {}
    for key, row in rows.items():
        if row.get("status", "success") != "success":
            continue
        if kind == "jev":
            values = row["presence"]
            if set(values) != set(COMPONENTS) or any(
                type(value) is not bool for value in values.values()
            ):
                raise ValueError("invalid_jev_presence")
            result[key] = values
        else:
            result[key] = {
                name: value["present"]
                for name, value in validate(row["labels"]).items()
            }
    return result


def check_successes(db, rows):
    joined = Counter()
    resolved = Counter()
    successes = 0
    positive_spans = 0
    for row in rows.values():
        if row["status"] != "success":
            continue
        text = load_text(db, row)
        if len(text) > 12000:
            raise ValueError("sample_exceeds_documented_limit")
        validate(row["labels"], text)
        for field in ("joined_spans", "resolved_spans"):
            names = row.get(field, [])
            if (
                not isinstance(names, list)
                or len(set(names)) != len(names)
                or any(
                    name not in COMPONENTS or not row["labels"][name]["present"]
                    for name in names
                )
            ):
                raise ValueError("invalid_span_resolution_metadata")
        if set(row.get("joined_spans", [])) & set(row.get("resolved_spans", [])):
            raise ValueError("overlapping_span_resolution_metadata")
        joined.update(row.get("joined_spans", []))
        resolved.update(row.get("resolved_spans", []))
        positive_spans += sum(v["present"] for v in row["labels"].values())
        successes += 1
    return {
        "successful_texts_denominator": successes,
        "component_decisions_denominator": successes * len(COMPONENTS),
        "positive_spans_denominator": positive_spans,
        "joined_spans": sum(joined.values()),
        "joined_by_component": {name: joined[name] for name in COMPONENTS},
        "resolved_spans": sum(resolved.values()),
        "resolved_by_component": {name: resolved[name] for name in COMPONENTS},
    }


def ratio(n, d):
    return n / d if d else None


def coverage(sample, final, keys):
    groups = defaultdict(list)
    for key, row in sample.items():
        groups[tuple(row.get(name) for name in keys)].append(key)
    output = []
    for group, ids in sorted(groups.items(), key=lambda pair: canonical(pair[0])):
        successes = sum(final.get(key, {}).get("status") == "success" for key in ids)
        failures = [
            final[key] for key in ids if final.get(key, {}).get("status") == "failure"
        ]
        terminal = successes + len(failures)
        output.append(
            {
                **dict(zip(keys, group, strict=True)),
                "sample_texts_denominator": len(ids),
                "terminal_texts_denominator": terminal,
                "successes": successes,
                "failures": len(failures),
                "without_terminal": len(ids) - terminal,
                "failure_share_of_terminal": ratio(len(failures), terminal),
                "error_types": dict(
                    sorted(Counter(r["error_type"] for r in failures).items())
                ),
            }
        )
    return output


def prevalence(sample, predictions):
    films = defaultdict(list)
    for key in sample:
        films[sample[key]["film_id"]].append(key)
    per_film = []
    for film, ids in sorted(films.items()):
        available = [key for key in ids if key in predictions]
        components = {}
        for name in (*COMPONENTS, "overall"):
            denominator = len(available) * (len(COMPONENTS) if name == "overall" else 1)
            n = sum(
                sum(predictions[key].values())
                if name == "overall"
                else predictions[key][name]
                for key in available
            )
            components[name] = {
                "present": n,
                "denominator": denominator,
                "share": ratio(n, denominator),
            }
        per_film.append(
            {
                "film_id": film,
                "sample_texts_denominator": len(ids),
                "successful_texts": len(available),
                "components": components,
            }
        )
    overall = {}
    for name in (*COMPONENTS, "overall"):
        values = [row["components"][name] for row in per_film]
        defined = [value["share"] for value in values if value["share"] is not None]
        n = sum(value["present"] for value in values)
        d = sum(value["denominator"] for value in values)
        overall[name] = {
            "per_film_mean": ratio(sum(defined), len(defined)),
            "films_with_success_denominator": len(defined),
            "sample_films_denominator": len(films),
            "text_weighted": {"present": n, "denominator": d, "share": ratio(n, d)},
        }
    return {
        "per_film": per_film,
        "summary": overall,
        "overall_definition": (
            "Present component decisions / fourteen decisions per successful "
            "text; not any-component presence."
        ),
    }


def agreement_data(left, right, gold=False):
    result = crosscheck.compare(left, right)
    # The shared comparator repeats missing-ID lists in each component and micro
    # result. Keep one authoritative pair of lists at the comparison level.
    for metrics in [*result["per_component"].values(), result["micro"]]:
        metrics.pop("left_lacks", None)
        metrics.pop("right_lacks", None)
    if gold:

        def wrapped(values):
            return {
                key: {name: {"present": value} for name, value in row.items()}
                for key, row in values.items()
            }

        # Preserve gold-as-reference precision/recall as well as symmetric counts.
        result["gold_reference_metrics"] = agreement.compare(
            wrapped(right), wrapped(left)
        )
    return result


def concentration(rows, overall):
    available = [row for row in rows if row["terminal_texts_denominator"]]
    above = [
        row
        for row in available
        if row["failures"] and row["failure_share_of_terminal"] > overall
    ]
    maximum = max((r["failure_share_of_terminal"] for r in available), default=None)
    return {
        "groups_with_terminal_denominator": len(available),
        "groups_above_pooled_failure_share": len(above),
        "maximum_group_failure_share": maximum,
        "statement": (
            (
                "Observed terminal failure shares vary across groups; inspect "
                "counts and denominators."
            )
            if above
            else "No group has a terminal failure share above the pooled share."
        ),
        "limit": (
            "Descriptive only; small cells and unfinished order can explain "
            "differences. These are labelling failures, never production "
            "failure rates."
        ),
    }


def long_text_bias(features, occurrences):
    """Distinct texts within film first; the pilot never enters these counts."""
    fields = [
        "characters",
        "semantic_eligible",
        "structured_json",
        "xml_like",
        "preservation_matches",
        "exclusion_matches",
        "camera_matches",
        "lens_matches",
    ]
    frame = pd.read_parquet(features, columns=["text_id", *fields])
    occ = pd.read_parquet(occurrences)
    if frame.text_id.duplicated().any():
        raise ValueError("duplicate_feature_text")
    primary = occ[occ.population == "primary"]
    if not set(primary.text_id) <= set(frame.text_id):
        raise ValueError("missing_structural_features")
    joined = primary.merge(frame, on="text_id", validate="many_to_one")

    def summary(part):
        unique = part.drop_duplicates("text_id")
        return {
            "distinct_texts_denominator": len(unique),
            "excluded_long_texts": int((~unique.semantic_eligible).sum()),
            "excluded_share": ratio(
                int((~unique.semantic_eligible).sum()), len(unique)
            ),
            "structural_by_eligibility": [
                {
                    "semantic_eligible": eligible,
                    "texts_denominator": len(group),
                    **{
                        name + "_mean": float(group[name].mean())
                        if len(group)
                        else None
                        for name in fields
                        if name != "semantic_eligible"
                    },
                }
                for eligible, group in unique.groupby("semantic_eligible")
            ],
        }

    return {
        "primary_text_weighted": summary(joined),
        "per_film": [
            {"film_id": film, **summary(group)}
            for film, group in joined.groupby("film_id")
        ],
        "by_stratum": [
            {
                "film_id": keys[0],
                "generation_type": keys[1],
                "text_role": keys[2],
                **summary(group),
            }
            for keys, group in joined.groupby(
                ["film_id", "generation_type", "text_role"], dropna=False
            )
        ],
        "limit": (
            "Long texts retain structural features only. Structural "
            "differences describe selection; their semantic prevalence and "
            "the direction of semantic bias are unknown. Strata and film "
            "counts overlap for shared texts."
        ),
    }


def build_report(
    sample, final, primary_info, jev, jev_gold, gold, span_checks, long_bias
):
    predictions = presence(final)
    jev_presence = presence(jev, "jev")
    gold_presence = presence(gold)
    gold_jev_presence = presence(jev_gold, "jev")
    films = coverage(sample, final, ("film_id",))
    strata = coverage(sample, final, ("film_id", "generation_type", "text_role"))
    failures = [row for row in final.values() if row["status"] == "failure"]
    if any(
        not isinstance(row.get("error_type"), str) or not row["error_type"]
        for row in failures
    ):
        raise ValueError("missing_error_type")
    pooled = ratio(len(failures), len(final))
    bounds = {}
    for name in COMPONENTS:
        n = sum(row[name] for row in predictions.values())
        bounds[name] = {
            "success_present": n,
            "success_texts_denominator": len(predictions),
            "terminal_texts_denominator": len(final),
            "if_all_failures_absent": ratio(n, len(final)),
            "if_all_failures_present": ratio(n + len(failures), len(final)),
            "if_all_unlabelled_sample_absent": ratio(n, len(sample)),
            "if_all_unlabelled_sample_present": ratio(
                n + len(sample) - len(predictions), len(sample)
            ),
        }
    return {
        "study": "04",
        "code_id": "04.2",
        "provisional": True,
        "evidence_label": "inferred",
        "scope": (
            "Descriptive provisional semantic assignments to explicit text "
            "instructions in the primary-film sample; no achieved output, "
            "causal, quality or top-versus-other claims."
        ),
        "competing_explanation": (
            "Wording ambiguity, reference scope, single-coder choices, "
            "stratified selection, text repetition and unfinished run order."
        ),
        "confidence_rationale": (
            "Exact source hashes and spans are checked; semantic agreement is"
            " descriptive and is not independent human validation."
        ),
        "denominator": (
            "One exact sampled text; fourteen decisions. Per-film means use "
            "only films with successes, with missing films counted "
            "separately."
        ),
        "coverage": {
            "sample_texts_denominator": len(sample),
            "terminal_texts": len(final),
            "successes": len(predictions),
            "failures": len(failures),
            "without_terminal": len(sample) - len(final),
            "pending_attempts": len(primary_info["pending_attempts"]),
            "failure_share_of_terminal": pooled,
        },
        "span_checks": span_checks,
        "failure_error_types": dict(
            sorted(Counter(r["error_type"] for r in failures).items())
        ),
        "coverage_per_film": films,
        "coverage_per_stratum": strata,
        "failure_concentration": {
            "per_film": concentration(films, pooled) if pooled is not None else None,
            "per_stratum": concentration(strata, pooled)
            if pooled is not None
            else None,
        },
        "prevalence": prevalence(sample, predictions),
        "agreement": {
            "primary_vs_gold": agreement_data(predictions, gold_presence, gold=True),
            "jev_vs_gold": agreement_data(jev_presence, gold_presence, gold=True),
            "jev_gold_run_vs_gold": agreement_data(
                gold_jev_presence, gold_presence, gold=True
            ),
            "primary_vs_jev": agreement_data(predictions, jev_presence),
        },
        "gold_limits": {
            "texts_denominator": len(gold),
            "single_agent_coder": True,
            "adjudication": False,
            "present_counts": {
                name: sum(row[name] for row in gold_presence.values())
                for name in COMPONENTS
            },
            "by_role": dict(Counter(row["text_role"] for row in gold.values())),
            "limit": (
                "Lopsided marginal counts constrain kappa; no validated "
                "shot-prompt or negative-role coverage. Jev is presence-only, "
                "secondary, never merged into primary labels."
            ),
        },
        "failure_sensitivity_bounds": bounds,
        "failure_bias_limit": (
            "Failure labels are unknown. Bounds are extremes, not estimates. "
            "Pending and unstarted texts remain missing, never absent; "
            "partial order may bias observed prevalence."
        ),
        "long_text_bias": long_bias,
        "sampling_limit": (
            "Balanced film/type/role sample, not proportional or "
            "probability-weighted corpus prevalence. Shared texts use their "
            "assigned sample stratum; repeated texts and films by a creator "
            "are not independent."
        ),
    }


def materialise_sources(db):
    # Avoid repeated Parquet scans; load_text still verifies source hashes.
    db.execute(
        "CREATE TEMP TABLE af3b_primary AS "
        "SELECT film_id,generation_id,prompt FROM generations"
    )
    db.execute("CREATE TEMP TABLE af3b_nested AS SELECT * FROM generation_prompts")
    db.execute("CREATE OR REPLACE VIEW generations AS SELECT * FROM af3b_primary")
    db.execute("CREATE OR REPLACE VIEW generation_prompts AS SELECT * FROM af3b_nested")


def prepare(args):
    sample = read_rows(args.sample)
    if not sample:
        raise ValueError("empty_sample")
    if any(row.get("population") != "primary" for row in sample.values()):
        raise ValueError("sample_not_primary")
    final, info = collect(args.journals, sample)
    jev, jev_info = collect([args.jev], sample, "jev")
    gold = read_rows(args.gold)
    for row in gold.values():
        check_source(row, sample)
    jev_gold, jev_gold_info = collect([args.jev_gold], gold, "jev")
    if (
        set(jev) != set(sample)
        or set(jev_gold) != set(gold)
        or any(
            row["status"] != "success" for row in [*jev.values(), *jev_gold.values()]
        )
    ):
        raise ValueError("incomplete_jev_crosscheck")
    if not args.allow_partial and (
        set(final) != set(sample) or info["pending_attempts"]
    ):
        raise ValueError("unfinished_primary_run_use_allow_partial_for_dry_run")
    with connect(args.data) as db:
        materialise_sources(db)
        for row in sample.values():
            if len(load_text(db, row)) > 12000:
                raise ValueError("sample_exceeds_documented_limit")
        checks = check_successes(db, final)
        check_successes(
            db, {key: {**row, "status": "success"} for key, row in gold.items()}
        )
    bias = long_text_bias(args.features, args.occurrences)
    report = build_report(sample, final, info, jev, jev_gold, gold, checks, bias)
    sources = {
        "primary_journals": info,
        "jev_journal": jev_info,
        "jev_gold_journal": jev_gold_info,
        **{
            name + "_sha256": hashlib.sha256(
                getattr(args, name).read_bytes()
            ).hexdigest()
            for name in ("sample", "gold", "features", "occurrences")
        },
    }
    return sample, final, jev, jev_gold, report, sources


def arguments(parser):
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument(
        "--sample", type=Path, default=Path("data/prompt-labels-v1/sample.jsonl.gz")
    )
    parser.add_argument(
        "--gold", type=Path, default=Path("prompt-labels/outputs/gold.jsonl")
    )
    parser.add_argument(
        "--features", type=Path, default=Path("data/prompt-labels-v1/features.parquet")
    )
    parser.add_argument(
        "--occurrences",
        type=Path,
        default=Path("data/prompt-labels-v1/occurrences.parquet"),
    )
    parser.add_argument("--journals", type=Path, nargs="+", required=True)
    parser.add_argument("--jev", type=Path, required=True)
    parser.add_argument("--jev-gold", type=Path, required=True)
    parser.add_argument("--allow-partial", action="store_true")


def write_json(path, value):
    # JSON null, never NaN, represents unavailable values (including strata).
    value = normalise_nulls(value)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def normalise_nulls(value):
    if isinstance(value, dict):
        return {key: normalise_nulls(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalise_nulls(item) for item in value]
    return None if isinstance(value, float) and pd.isna(value) else value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    arguments(parser)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    *_, report, sources = prepare(args)
    args.output.mkdir(parents=True, exist_ok=False)
    write_json(args.output / "report.json", report)
    write_json(args.output / "sources.json", sources)
