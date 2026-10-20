# AF3a validation

- `uv sync --locked`: locked environment installed; no dependency changes.
- `uv run python scripts/fetch_data.py`: all 28 assets verified.
- A second independent `--output data/af3a-fresh` fetch verified all 28 assets;
  another `verify()` pass on that copy also matched all 28 checksums.
- `uv run python prompt-labels/build.py`: 61,479 distinct primary texts;
  61,542 combined texts; 160,753 compound field occurrences; 5,000 sampled
  texts, 300 gold selections, all 157 primary films in each selection.
- Fresh-copy rebuild using `--data data/af3a-fresh --output
  data/af3a-rebuilt-small --large data/af3a-rebuilt`: byte-identical three-asset
  SHA256SUMS, build counts, per-film/per-stratum summaries, strata and gold
  selection. Sample JSONL is covered by its deterministic gzip hash.
- `uv run python prompt-labels/gold.py`: 300 readings materialised; every
  positive span checked against its exact source field.
- `uv run python prompt-labels/checks.py`: all 5,000 source hashes and length
  limits checked; 300 gold sources and 4,200 decisions checked; no full-field
  spans; 157 films in each set. Self kappa 1; 300 deliberately inverted subject
  decisions produce micro kappa 0.8364409551848218 and accuracy 3900/4200.
- The agreement CLI was also run directly on the gold file against itself and
  against the deliberately perturbed local copy, reproducing the smoke outputs.
- `uv run ruff check .`: passed.
- `uv run ruff format --check .`: 56 Python files formatted.
- `uv run pytest`: 58 passed, including 17 AF3a synthetic tests.
- `uv run python scripts/check_repository.py`: passed; original hashes match,
  no tracked data/ files or files above 5 MB.
- New-file content scan: no matching email addresses or machine-specific paths.

No real model endpoint was called. Stub requests were loopback-only. These checks
validate software, source correspondence and reproducibility, not semantic
accuracy or actual-model agreement. Gold remains one agent coder, no adjudication.

## Release download

Fresh-download checksum verification is recorded here after publication and
before merge. The final handover records the PR and green CI run.
