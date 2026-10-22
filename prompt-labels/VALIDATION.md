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
- `uv run ruff format --check .`: 58 Python files formatted.
- `uv run pytest`: 58 passed, including 17 AF3a synthetic tests.
- `uv run python scripts/check_repository.py`: passed; original hashes match,
  no tracked data/ files or files above 5 MB.
- New-file content scan: no matching email addresses or machine-specific paths.

No real model endpoint was called. Stub requests were loopback-only. These checks
validate software, source correspondence and reproducibility, not semantic
accuracy or actual-model agreement. Gold remains one agent coder, no adjudication.

## AF3a2 span resolution

The harness first uses `nfc-casefold-whitespace-quotes-dashes` for near-exact
positive spans. If that fails, AF3a-v3 splits spans on runs of at least two full
stops or `…`, resolves nonempty fragments in order using the same exact-then-
normalised search, and stores the shortest contiguous source passage covering
them. Components resolved this way are recorded in `joined_spans`; ordinary
normalised matches remain in `resolved_spans`, with no overlap between the lists.
Missing or out-of-order fragments fail. Exact full-span matches take precedence.
The standalone validator and released gold remain exact-span checks. The
`nfc-casefold-whitespace-quotes-dashes+ellipsis-cover` metadata and AF3a-v3 label
version refuse existing AF3a-v2 journals through the configuration hash check.
Synthetic tests cover exact, case, whitespace, apostrophe, dash, repeated
occurrence, ellipsis fragments and v2 journal refusal. No real model endpoint was
called.

## Release download

The public `prompt-labels-v1` release was freshly downloaded with:

```bash
gh release download prompt-labels-v1 --repo TelesforoAleix/ai-film-practice --dir data/af3a-release-download
```

The downloaded SHA256SUMS was byte-identical to the build manifest. Recomputing
SHA-256 from all three fresh assets matched every entry:

| Asset | Bytes | SHA-256 |
| --- | ---: | --- |
| features.parquet | 5,186,343 | `92073c8beda0014a23a66cec0340a3909e76f04e520e1bf8d8b66c0e7cf6f55a` |
| occurrences.parquet | 10,558,538 | `dbe844be049351560acb1a1b785e1921c7ac2a96afe26318b76454c440cd667c` |
| sample.jsonl.gz | 483,896 | `9a2e83a63486d2bb3d65a59d6a9146be98514c33e9f331add214e501c8ea17d6` |

The small-output CSV writer was made explicitly LF-delimited, then the build
was repeated from the fresh source copy. Asset hashes and the small outputs
still matched byte for byte. PR #7 contains the change; the final handover
records green CI at its final head and the merge commit.

## AF3c Jev client and cross-check

AF3c adds a one-request-per-text, fourteen-choice-question client for Jev and
a descriptive presence comparison against AF3a and optionally the single-coder
gold. Jev is secondary and supplies no spans. Its journal uses the same
append-only, locked, fsynced, resumable pattern as the AF3a harness and hashes
the requested model, endpoint and exact question set. The credential is read
only from `TYPESAFE_API_KEY`; tests use a generated ephemeral value and a
loopback HTTP server. No real API request was made.

Tests cover exact request wording and state, authorization header placement,
credential exclusion from records/errors, missing-key rejection, resume and
attempt limits, truncated-tail recovery, configuration mismatch, HTTP 429 retry,
invalid choice/probabilities and known agreement counts/kappa. Cross-check
reports are descriptive and do not weight, interval-estimate or adjudicate.

The client accepts plain or gzip-compressed sample JSONL. Example commands:

```bash
uv run python prompt-labels/jev.py --sample data/af3a-release-download/sample.jsonl.gz --data data --output data/af3c-jev.jsonl
uv run python prompt-labels/crosscheck.py --harness data/af3a-labels.jsonl --jev data/af3c-jev.jsonl --gold prompt-labels/outputs/gold.jsonl --output data/af3c-crosscheck.json
```

The implementation validation commands and their results are recorded in the
AF3c PR handover; no source data was modified.
