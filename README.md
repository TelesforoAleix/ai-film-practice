# How top AI creators build films

Public, non-commercial research into how the strongest creators of the Higgsfield Global
Film Festival technically build AI images and films: project structure, tools and models,
steps, asset connections and reuse, and how creators describe their work. Story, aesthetics
and judgments of media quality are outside the programme.

**Status:** AF0 establishes the frozen data, query tools, programme and repository rules.
No study has started. [PROGRAMME.md](PROGRAMME.md) is the binding version 2; Study 01 will
establish the evidence map, panel and codebook. Earlier collection documents are preserved
in [original/](original/README.md), including pre-existing case studies.

This project is **not affiliated with or endorsed by Higgsfield**. The corpus was collected
on 19–20 October 2026 from public pages and public workspaces only, using open-source
listings for detailed collection. This is non-commercial research. Rights in prompts,
briefs, names and media stay with their creators; each film links back to its public
project page. Anything is removed on request: [open an issue](https://github.com/TelesforoAleix/ai-film-practice/issues).
Email addresses and local file paths have been redacted. See [DATA.md](DATA.md) for scope, provenance and rights.

## Get the snapshot and query it

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/). From the repository root:

```bash
uv sync --locked
uv run python scripts/fetch_data.py
```

The downloader fetches all 28 data files and SHA256SUMS from the
[data-2026-10-20 release](https://github.com/TelesforoAleix/ai-film-practice/releases/tag/data-2026-10-20),
verifies every data file, and installs them under ignored data/. While the repository is
private, use `--transport gh` with an authenticated GitHub CLI instead of public HTTPS.
Use `--output data/another-copy` for an independent download. About 622 MB is downloaded;
allow room for temporary staging and, if needed, decompressed CSVs.

```python
from film_practice import connect

with connect("data") as db:
    print(db.sql("SELECT count(*) AS generations FROM generations").fetchone())
    # (130899,)
    frame = db.sql("SELECT film_id, generation_id FROM generations LIMIT 5").df()
```

There is one DuckDB view per table. Every column remains VARCHAR or NULL; schema typing
belongs to Study 01. `connect` requires all 14 Parquet tables. Use compound film/entity
keys, not generation or asset IDs alone. See [DATA.md](DATA.md) for parsing rules.

## Layout

| Location | Contents |
| --- | --- |
| PROGRAMME.md | Research design and binding study output contract |
| AGENTS.md | Rules for future executors |
| original/ | Six collection documents and an explanatory index |
| src/film_practice/ | DuckDB connection and named views |
| scripts/ | Build, verify, fetch and repository checks |
| tests/ | Small synthetic fixtures, never real data |
| studies/NN-slug/ | Each study's README.md, queries/code, and outputs/ |
| validation/ | AF0 scan and conversion counts, hashes and asset sizes |
| data/ | Ignored downloads and local builds; never committed |

Large study outputs are release assets, never git files. No analysis is included in AF0.

## Rebuild and validate

The collected CSV folder is read-only. Supply its location as an argument; no local paths
are stored here:

```bash
uv run python -m scripts.scan_corpus <source-folder>
uv run python scripts/build_parquet.py <source-folder>
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run python scripts/check_repository.py
```

The builder writes under data/build/, redacts personal identifiers, preserves every other CSV
byte in gzip, creates zstd Parquet with string columns, and verifies every value plus row,
null/empty, compound-key and prompt counts. build-report.json is a local validation report;
the release contains only the 28 data files and SHA256SUMS. Detailed recorded results are
in [validation/README.md](validation/README.md). CI runs the code and git-boundary checks.

Code is [MIT](LICENSE). The repository's own writing (programme, findings and documentation)
is [CC BY 4.0](LICENSE-docs). The data receives **no new licence**; these licences do not grant
rights over third-party prompts, briefs, names or media. See [DATA.md](DATA.md).
