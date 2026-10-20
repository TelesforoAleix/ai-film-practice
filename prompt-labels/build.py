"""Build exact-text structural features and balanced AF3a ID-only samples."""

import argparse
import csv
import gzip
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

from film_practice import connect
from film_practice.prompt_labels import digest

SEED = "AF3a-v1-20261020"
MAX_CHARS = 12000
PATTERNS = {
    "section": (
        "(?m)^\\s*(?:#{1,6}\\s+\\S|[A-Z][A-Z /_-]{2,40}:|[A-Za-z][\\w /-]{1,35}:\\s*$)"
    ),
    "reference": (
        "(?i)(?:@\\w+|\\b(?:image|img|reference|ref|video)\\s*#?\\s*\\d+"
        "\\b|<[^<>\\n]{1,80}>)"
    ),
    "camera": r"(?i)\b(?:camera|pan|tilt|dolly|tracking|orbit|handheld|crane|zoom)\b",
    "lens": (
        "(?i)\\b(?:lens|\\d{1,3}\\s*mm|f/\\d+(?:\\.\\d+)?|close[- ]up|wid"
        "e shot|medium shot|telephoto|anamorphic)\\b"
    ),
    "preservation": (
        "(?i)\\b(?:preserve|retain|unchanged|keep (?:the |it |all |e"
        "verything |exactly |same)|same (?:identity|character|face|"
        "layout))\\b"
    ),
    "exclusion": (
        "(?i)\\b(?:no|without|avoid|exclude|never|do not|don't|negative prompt)\\b"
    ),
    "edit": r"(?i)\b(?:replace|remove|change|add|edit|swap|recolor|recolour)\b",
    "multi_shot": r"(?i)\b(?:shot\s*\d+|multi[- ]shot|\d+\s+shots)\b",
}
REGEX = {key: re.compile(value) for key, value in PATTERNS.items()}


def features(text):
    result = {
        "characters": len(text),
        "utf8_bytes": len(text.encode()),
        "words_whitespace": len(text.split()),
        "lines": text.count("\n") + 1,
    }
    for name, pattern in REGEX.items():
        matches = list(pattern.finditer(text))
        result[name + "_matches"] = len(matches)
        result[name + "_excerpt"] = (
            matches[0].group()
            if matches and len(matches[0].group()) < len(text)
            else None
        )
    try:
        result["structured_json"] = isinstance(json.loads(text), (dict, list))
    except (ValueError, RecursionError):
        result["structured_json"] = False
    result["xml_like"] = bool(re.search(r"<([A-Za-z]\w*)\b[^>]*>.*?</\1>", text, re.S))
    lines = [line.strip() for line in text.splitlines() if len(line.strip()) >= 40]
    result["repeated_lines"] = sum(n - 1 for n in Counter(lines).values())
    result["short_edit_proxy"] = len(text) <= 300 and result["edit_matches"] > 0
    result["long_description_proxy"] = len(text) >= 1000
    result["semantic_eligible"] = len(text) <= MAX_CHARS
    return result


def rank(salt, value):
    return digest(SEED + salt + value)


def balanced(candidates, target, salt):
    "Round robin films then operations; globally unique text hashes, no substitution."
    buckets = defaultdict(lambda: defaultdict(list))
    for row in candidates:
        operation = (row["generation_type"], row["text_role"])
        buckets[row["film_id"]][operation].append(row)
    for operations in buckets.values():
        for rows in operations.values():
            rows.sort(key=lambda r: rank(salt, r["text_id"]), reverse=True)
    films = sorted(buckets, key=lambda f: rank(salt, f))
    ops = {f: sorted(buckets[f], key=lambda o: rank(salt, str(o))) for f in films}
    cursor = Counter()
    selected, seen = [], set()
    while len(selected) < target:
        progress = False
        for film in films:
            options = ops[film]
            for _ in options:
                operation = options[cursor[film] % len(options)]
                cursor[film] += 1
                rows = buckets[film][operation]
                while rows and rows[-1]["text_id"] in seen:
                    rows.pop()
                if rows:
                    row = rows.pop()
                    selected.append(row)
                    seen.add(row["text_id"])
                    progress = True
                    break
            if len(selected) == target:
                break
        if not progress:
            break
    return selected


def write_json(path, value):
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    )


def write_jsonl(path, rows):
    path.write_text(
        "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    )


def build(data, output, large):
    output.mkdir(parents=True, exist_ok=True)
    large.mkdir(parents=True, exist_ok=True)
    taxonomy = pd.read_csv(
        "studies/01-corpus/outputs/taxonomy.csv", keep_default_na=False
    )
    populations = dict(zip(taxonomy.film_id, taxonomy.population, strict=True))
    with connect(data) as db:
        # The nested export of a primary source field must be byte-identical.
        mismatch = db.sql("""
            SELECT count(*) FROM generation_prompts p JOIN generations g
            USING(film_id,generation_id)
            WHERE p.field_path=g.prompt_source_path AND p.text IS DISTINCT FROM g.prompt
        """).fetchone()[0]
        if mismatch:
            raise ValueError("primary_crosswalk_mismatch")
        # All primary fields, plus nested fields except the same primary field path.
        occurrences = db.sql("""
            SELECT film_id,generation_id,prompt_source_path AS field_path,
                   'primary' AS text_role,'generations' AS source_table,
                   generation_type,model_identifier,source_record_file,prompt AS text
            FROM generations
            UNION ALL
            SELECT p.film_id,p.generation_id,p.field_path,
              CASE WHEN p.prompt_role='negative' THEN 'negative'
                   WHEN starts_with(p.field_path, 'params.multi_prompt[')
                   THEN 'shot_prompt'
                   ELSE 'other_text' END,
              'generation_prompts',g.generation_type,g.model_identifier,
              g.source_record_file,p.text
            FROM generation_prompts p JOIN generations g
            USING(film_id,generation_id)
            WHERE p.field_path IS DISTINCT FROM g.prompt_source_path
        """).df()
        primary = db.sql(
            "SELECT prompt FROM generations WHERE prompt IS NOT NULL AND prompt<>''"
        ).df()
    occurrences = occurrences.astype(object).where(pd.notna(occurrences), None)
    states = Counter(
        "unavailable" if t is None else "empty" if t == "" else "nonempty"
        for t in occurrences.text
    )
    texts = {}
    rows = []
    for row in occurrences.to_dict("records"):
        text = row.pop("text")
        if text is None or text == "":
            continue
        row["text_id"] = digest(text)
        row["population"] = populations[row["film_id"]]
        if row["text_id"] in texts and texts[row["text_id"]] != text:
            raise ValueError("text_hash_collision")
        texts[row["text_id"]] = text
        rows.append(row)
    frame = pd.DataFrame(
        [{"text_id": key, **features(value)} for key, value in sorted(texts.items())]
    )
    frame.to_parquet(large / "features.parquet", index=False)
    occ = pd.DataFrame(rows).sort_values(["film_id", "generation_id", "field_path"])
    occ.to_parquet(large / "occurrences.parquet", index=False)
    # Each summary counts a text once within its film / film-operation context.
    joined = occ.drop_duplicates(
        ["film_id", "generation_type", "text_role", "text_id"]
    ).merge(frame, on="text_id")
    numeric = [
        c
        for c in frame
        if c not in {"text_id", "semantic_eligible"} and not c.endswith("_excerpt")
    ]
    for name, keys in [
        ("film", ["population", "film_id"]),
        ("stratum", ["population", "film_id", "generation_type", "text_role"]),
    ]:
        base = joined.drop_duplicates(keys + ["text_id"])
        groups = base.groupby(keys, dropna=False)
        result = groups[numeric].sum().add_suffix("_sum")
        result["distinct_texts_denominator"] = groups.size()
        result.to_csv(output / f"features_by_{name}.csv", na_rep=r"\N")
    candidates = [
        r
        for r in rows
        if r["population"] == "primary" and len(texts[r["text_id"]]) <= MAX_CHARS
    ]
    # One representative per film/operation/text; ties resolved by compound key.
    candidates.sort(
        key=lambda r: (r["film_id"], r["generation_id"], r["field_path"] or "")
    )
    candidates = list(
        {
            (r["film_id"], r["generation_type"], r["text_role"], r["text_id"]): r
            for r in reversed(candidates)
        }.values()
    )
    sample = balanced(candidates, 5000, "sample")
    gold = balanced(sample, 300, "gold")
    write_jsonl(large / "sample.jsonl", sample)
    write_jsonl(output / "gold_selection.jsonl", gold)
    counts = Counter(
        (r["film_id"], r["generation_type"], r["text_role"]) for r in candidates
    )
    sc = Counter((r["film_id"], r["generation_type"], r["text_role"]) for r in sample)
    gc = Counter((r["film_id"], r["generation_type"], r["text_role"]) for r in gold)
    with (output / "strata.csv").open("w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "film_id",
                "generation_type",
                "text_role",
                "eligible_distinct_texts",
                "sample",
                "gold",
            ]
        )
        for key in sorted(counts, key=str):
            writer.writerow(
                [
                    *(r"\N" if k is None else k for k in key),
                    counts[key],
                    sc[key],
                    gc[key],
                ]
            )
    report = {
        "seed": SEED,
        "max_characters": MAX_CHARS,
        "field_states": dict(states),
        "all_primary_distinct": primary.prompt.nunique(),
        "snapshot_manifest_sha256": digest((data / "SHA256SUMS").read_text()),
        "primary_primary_distinct": len(
            {
                r["text_id"]
                for r in rows
                if r["population"] == "primary" and r["text_role"] == "primary"
            }
        ),
        "primary_role_rows": dict(
            Counter(r["text_role"] for r in rows if r["population"] == "primary")
        ),
        "sample_roles": dict(Counter(r["text_role"] for r in sample)),
        "gold_roles": dict(Counter(r["text_role"] for r in gold)),
        "sample_occupied_strata": len(sc),
        "gold_occupied_strata": len(gc),
        "eligible_occupied_strata": len(counts),
        "all_text_distinct": len(texts),
        "nonempty_field_occurrences": len(rows),
        "primary_all_roles_distinct": len(
            {r["text_id"] for r in rows if r["population"] == "primary"}
        ),
        "supplemental_all_roles_distinct": len(
            {r["text_id"] for r in rows if r["population"] == "supplemental"}
        ),
        "long_all_distinct": sum(len(t) > MAX_CHARS for t in texts.values()),
        "long_primary_distinct": len(
            {
                r["text_id"]
                for r in rows
                if r["population"] == "primary" and len(texts[r["text_id"]]) > MAX_CHARS
            }
        ),
        "sample": len(sample),
        "sample_films": len({r["film_id"] for r in sample}),
        "gold": len(gold),
        "gold_films": len({r["film_id"] for r in gold}),
        "sample_characters": sum(len(texts[r["text_id"]]) for r in sample),
        "gold_characters": sum(len(texts[r["text_id"]]) for r in gold),
        "sample_per_film": dict(
            sorted(Counter(Counter(r["film_id"] for r in sample).values()).items())
        ),
        "gold_per_film": dict(
            sorted(Counter(Counter(r["film_id"] for r in gold).values()).items())
        ),
    }
    write_json(output / "build.json", report)
    print(json.dumps(report, indent=2))
    # Reproducible compressed manifest assets, no full prompt texts.
    for name in ("sample.jsonl",):
        with (
            (large / name).open("rb") as source,
            (large / (name + ".gz")).open("wb") as out,
        ):
            with gzip.GzipFile(
                filename="", mode="wb", fileobj=out, mtime=0
            ) as compressed:
                compressed.write(source.read())
    assets = ["features.parquet", "occurrences.parquet", "sample.jsonl.gz"]
    (large / "SHA256SUMS").write_text(
        "".join(
            f"{hashlib.sha256((large / n).read_bytes()).hexdigest()}  {n}\n"
            for n in assets
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, default=Path("prompt-labels/outputs"))
    parser.add_argument("--large", type=Path, default=Path("data/prompt-labels-v1"))
    args = parser.parse_args()
    build(args.data, args.output, args.large)
