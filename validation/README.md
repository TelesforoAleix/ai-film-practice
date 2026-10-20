# AF0 validation record

This records publication and format validation only; it contains no study findings.

## Conversion checks

All 14 tables were built and verified against the collected CSVs after the authorized
identifier redaction. Every Parquet field is a string or null; all values were compared in
order, not sampled. Per-column CSV/Parquet null and empty-string counts match exactly.
Full numbers are in [build-report.json](build-report.json).

| Table | CSV rows | Parquet rows |
| --- | ---: | ---: |
| films | 6,224 | 6,224 |
| priority_films | 186 | 186 |
| folders | 3,246 | 3,246 |
| generations | 130,899 | 130,899 |
| generation_prompts | 161,836 | 161,836 |
| assets | 163,184 | 163,184 |
| asset_usages | 469,242 | 469,242 |
| asset_folders | 142,513 | 142,513 |
| generation_folders | 136,313 | 136,313 |
| reference_elements | 5,223 | 5,223 |
| brief_assets | 456 | 456 |
| model_usage | 1,495 | 1,495 |
| extraction_log | 6,224 | 6,224 |
| other_items | 0 | 0 |

Generation compound keys: **130,899**; distinct film IDs: **158**.
Nonempty primary prompts: **124,642**; distinct: **61,479**
before and after redaction; explicitly empty: **1,083**.
No expected count required reconciliation or a scope change.

Ordered SHA-256 over redacted CSV `generations.prompt` values equals the Parquet hash:

`3a113b330c80f5e48b9b157f1ad652ec2a87bbb021ca7e209039779af073b1a5`

The framing is one byte `N` for null, otherwise `S`, then the UTF-8 byte length as an
unsigned 8-byte big-endian integer and the exact UTF-8 bytes. It distinguishes null,
empty text, boundaries and order. No prompt text or email address is stored here.

Each gzip was independently decompressed and its hash matched the source bytes after
applying the same redaction. Every other byte is preserved. The 57 email and 12 local-path replacements by
column are documented in [DATA.md](../DATA.md). All six source documents were checked;
five are byte-identical, and version 1 differs only by the specified one-sentence
replacement. No document needed identifier redaction. See
[original-verification.json](original-verification.json).

## Publication scan

The owner authorized redacting all 12 local-file path occurrences as
`[local path removed]`: four each in generation_prompts.text, generations.prompt,
and generations.parameters_json. The standing rule covers email addresses, local
file paths and phone numbers. No phone numbers, credentials or secret patterns matched.

All 20 files were scanned with CSV-aware parsing, an unrestricted field-size limit,
email/token/private-key/path patterns, and parsed URL checks for userinfo, credential
query parameters and private/loopback hosts. Matches are reported by file and column
with counts and redacted placeholders in [scan-report.json](scan-report.json).

The first scan flagged email addresses and stopped publication. The owner authorized
replacing every occurrence with `[email removed]`. Four distinct addresses account for
57 field occurrences, including repeated text in primary prompts and JSON parameters.
Public `@handle` URLs, escaped JSON newlines and a package/version token were initial
pattern false positives. The refined scan distinguishes these. Pattern scans cannot
prove the absence of every possible secret. No raw matches are recorded.

## Release asset inventory

The release is `data-2026-10-20`, created after merge. It contains the following 28 data
assets and SHA256SUMS (which covers all 28 and does not hash itself). The builder report
is documentation in git, not an extra release asset. Sizes are exact bytes.

| Asset | Bytes |
| --- | ---: |
| films.parquet | 2,450,743 |
| films.csv.gz | 2,342,896 |
| priority_films.parquet | 358,402 |
| priority_films.csv.gz | 328,158 |
| folders.parquet | 302,154 |
| folders.csv.gz | 164,261 |
| generations.parquet | 169,652,968 |
| generations.csv.gz | 172,887,873 |
| generation_prompts.parquet | 79,157,394 |
| generation_prompts.csv.gz | 109,736,943 |
| assets.parquet | 18,536,411 |
| assets.csv.gz | 9,460,702 |
| asset_usages.parquet | 20,994,415 |
| asset_usages.csv.gz | 13,832,671 |
| asset_folders.parquet | 3,201,350 |
| asset_folders.csv.gz | 3,403,832 |
| generation_folders.parquet | 5,941,430 |
| generation_folders.csv.gz | 6,337,484 |
| reference_elements.parquet | 746,812 |
| reference_elements.csv.gz | 520,751 |
| brief_assets.parquet | 232,686 |
| brief_assets.csv.gz | 140,568 |
| model_usage.parquet | 32,534 |
| model_usage.csv.gz | 28,204 |
| extraction_log.parquet | 271,077 |
| extraction_log.csv.gz | 259,755 |
| other_items.parquet | 668 |
| other_items.csv.gz | 78 |
| SHA256SUMS | 2,426 |

Total data assets: **621,323,220 bytes**; with manifest: **621,325,646 bytes**.
Every asset is below the 2 GiB GitHub release limit. SHA-256 values for each data asset
are recorded in build-report.json and the release manifest. Checksums establish download
integrity against that manifest; they are not a separate signed provenance attestation.

## Code checks

`uv run ruff check .`, `uv run ruff format --check .`, `uv run pytest`, and
`uv run python scripts/check_repository.py` are required before merge. The eight
synthetic fixture tests cover null/empty/string preservation, multiline and long text,
JSON, email/local-path/phone removal and byte-preserving gzip, compound keys and ordered prompt hashing,
DuckDB views/pandas, manifest validation, tamper detection and download staging.
The repository check also verifies preserved document hashes, and Ruff excludes
original/ and PROGRAMME.md so Markdown code formatting cannot change them.

GitHub Actions runs the same checks on pushes and pull requests. Full-corpus conversion
is independently recorded here; CI does not need the 622 MB snapshot. Post-merge release
and fresh-download verification are recorded in the AF0 handover and release notes.
