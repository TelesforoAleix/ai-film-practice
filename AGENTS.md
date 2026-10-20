# Repository rules for executors

Read README.md, DATA.md and PROGRAMME.md before a study. PROGRAMME.md is the design:
its scope, evidence labels and nine-item study output contract are binding. Do not
silently change it. AF0 is infrastructure only and writes no research findings.

## Evidence and scope

Study technical production records. Do not judge story, aesthetics, media quality,
continuity or anything requiring watching the films. Distinguish observed,
creator-stated, inferred, associated, experimentally supported and proposed claims.
Keep observations, interpretations and studio proposals separate. Do not infer agents,
internal orchestration, labour time, cost or failure rates from these public records.
Only the selected cohort has detailed records; it cannot establish what separates top
films from other films. Keep the 157 priority workspaces and supplemental pilot distinct.

Every substantive finding must record its study, film ID, generation/asset/reference IDs,
source path, excerpt, evidence label, competing explanation, denominator and confidence
rationale. Use compound film/entity keys. Keep unavailable values apart from empty text;
parse CSV and JSON properly. Label inferred lineage. Every measure needs a denominator.

## Data and originals

Never edit original/ or the published snapshot. Email and local-path redaction were
authorized during AF0 and are already reflected in the published data. Never write an
email address into
this repository, a log or a handover. Escalate removal requests or newly discovered
private content to the owner; do not retrieve private workspaces, hidden prompts,
blocked brief snapshots or authenticated libraries. No machine-specific paths or local
user names belong in committed files.

Data is never committed to git. data/ is ignored. Large derived datasets belong in
release assets, with checksums, like the source snapshot. Do not add exceptions to
.gitignore to commit data. Keep fixture tests synthetic; never copy actual records.

## Loading and outputs

Run `uv sync --locked`, then `uv run python scripts/fetch_data.py` (or use
`--transport gh` while the repository is private). The downloader verifies all assets.
Use `from film_practice import connect` and `connect("data")` for named DuckDB views;
`connection.sql("SELECT count(*) FROM generations").df()` returns a pandas frame.
All source columns remain strings; Study 01 owns derived typing and the dictionary.

Each study lives in studies/NN-slug/: README.md for its report, queries and code beside
it, derived data in its own outputs/. Keep large outputs out of git; document their
release location. Preserve reusable queries and provenance. Study 01 comes first; do
not invent upstream results when they are missing: document provisional definitions
and dependencies as the programme requires.

## Validation

Run `uv run ruff check .`, `uv run ruff format --check .`, `uv run pytest`, and
`uv run python scripts/check_repository.py`. The last check rejects tracked data/
files and any tracked file above 5 MB. CI runs the same checks. Corpus conversion
validation is recorded in validation/; it is distinct from study findings.
