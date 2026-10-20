# Data: collected snapshot of 19–20 October 2026

This project is **not affiliated with or endorsed by Higgsfield**. It is public,
non-commercial research. The corpus was collected on 2026-10-19 and 2026-10-20 from
Higgsfield's public pages and public workspaces only. Detailed collection used open-source
listings: 23 non-open-source listings were excluded. Brief snapshots were sanitized for
visibility before this repository received them. Do not retrieve private workspaces,
hidden prompts, blocked brief snapshots or authenticated libraries.

The catalogue contains 6,224 films; the priority union contains 186 (126 shortlisted plus
100 most-watched, with 40 in both). Of these, 23 non-open-source listings were excluded
from detailed collection; six public priority workspaces were unavailable and 157 have
complete public histories. Cosmic tracks is a separate supplemental pilot. Generation
records cover 158 distinct film IDs. Only the selected cohort has detailed records; this
cannot show what separates top films from the rest. Public histories can omit external
work and discarded work.

## Publication and format

Data is never committed to git. The
[data-2026-10-20 release](https://github.com/TelesforoAleix/ai-film-practice/releases/tag/data-2026-10-20)
contains each of 14 tables as zstd Parquet and gzip-compressed CSV, plus SHA256SUMS.
Each of the 28 data assets has a SHA-256 entry in SHA256SUMS. The manifest does not hash
itself. GitHub's automatically generated source archives are not data assets.

**Email addresses were redacted at the owner's decision:** every occurrence was replaced
with the literal text `[email removed]` in both formats. Four distinct addresses accounted
for 57 occurrences across the collected CSV fields (not 57 independent contacts).
Addresses themselves are never recorded in this repository, logs or handovers.

| Table | Column | Occurrences replaced |
| --- | --- | ---: |
| films | description | 1 |
| films | project_brief | 1 |
| priority_films | project_brief | 1 |
| generation_prompts | text | 15 |
| generations | prompt | 15 |
| generations | parameters_json | 24 |
| **Total** | | **57** |

All other columns and tables had zero email replacements.

**Local file paths were also redacted at the owner's decision:** all 12 occurrences
were replaced with `[local path removed]` in both formats.

| Table | Column | Local-path occurrences replaced |
| --- | --- | ---: |
| generation_prompts | text | 4 |
| generations | prompt | 4 |
| generations | parameters_json | 4 |
| **Total** | | **12** |

All other columns and tables had zero local-path replacements. These were attachment
and mounted-filesystem references in text, repeated across the primary, nested and JSON
exports. Their original values are not recorded here. The standing AF0 rule also redacts
phone numbers as `[phone removed]`; **zero were detected in every table and column**.
Per-column zero counts are also recorded in build-report.json.
The detector checks valid international numbers and explicitly labelled US-format contacts,
without treating arbitrary IDs, seeds and dates as phone numbers. Like the other pattern
checks, it is not proof of absence of every possible notation.

None of the six source documents contained an email address, local-file path or detected
phone number. A package/version token in the source README was an initial
scan false positive and was preserved.

The data is otherwise unchanged from the collected CSVs. Decompressing a published CSV
produces bytes identical to the source after applying the same email, local-path and
phone redactions. CSV quoting, record order, line endings, whitespace and all other
content are preserved;
the builder does not reserialize CSV. It compares SHA-256 hashes of the transformed source
bytes and the decompressed gzip bytes. The redaction recognizers are defined in
scripts/build_parquet.py; a letter-only final domain label distinguishes email addresses
from package/version tokens. No address is substituted into fixture source or reports.

- CSV is UTF-8. `\N` means unavailable; an empty string remains empty.
- Every Parquet column is a string: only the literal `\N` becomes null. No number, date,
  boolean, whitespace, JSON value or other text is converted. The authorized
  identifier redactions above are the only content changes. Typing belongs to Study 01.
- JSON fields are serialized JSON, with identifier occurrences inside strings redacted too.
- Use a CSV parser with `csv.field_size_limit(sys.maxsize)`, never line splitting.
  Prompts span lines and can exceed 59,000 characters. The builder's line iteration only
  replaces authorized identifier substrings while preserving bytes; all tabular parsing
  uses csv.
- Join generations on `(film_id, generation_id)`, assets on `(film_id, asset_id)`, and
  folders on compound film/folder keys. IDs may recur across films. Placements and usage
  rows are occurrences, not independent entities.
- Relative source-record paths retained in fields identify collection provenance. They
  do not imply those raw files or validation sidecars are available here.

## Tables

| Table | Rows | Contents |
| --- | ---: | --- |
| films | 6,224 | Public catalogue, creator/profile/project links and available metadata |
| priority_films | 186 | Selected/popular union, with catalogue fields |
| folders | 3,246 | Workspace folder entities and paths |
| generations | 130,899 | Compound-key generation records, prompts, models, parameters and provenance |
| generation_prompts | 161,836 | Primary/nested text fields with source paths and roles |
| assets | 163,184 | Asset entities, including catalogue covers and final films |
| asset_usages | 469,242 | Generation-to-asset usages, roles and parameter paths |
| asset_folders | 142,513 | Asset folder placements |
| generation_folders | 136,313 | Generation folder placements |
| reference_elements | 5,223 | Disclosed reusable reference elements |
| brief_assets | 456 | Media and related records decoded from sanitized briefs |
| model_usage | 1,495 | Exported model usage summaries |
| extraction_log | 6,224 | Collection status and coverage per film |
| other_items | 0 | Header-only table retained for schema completeness |

The snapshot has 124,642 nonempty primary prompts, 61,479 distinct nonempty primary prompts
and 1,083 explicitly empty primary prompts. These counts reconcile before and after
redaction. The remaining 5,174 primary prompts are unavailable. Detailed per-column null
and empty-string counts and the ordered prompt hash are in validation/build-report.json.
These are conversion checks, not study findings or a derived data dictionary.

## What is missing

The provided corpus contains 14 CSVs and six collection documents. The extraction scripts,
raw responses and validation sidecar files cited by those documents are not available.
No film/image/audio binaries were provided: media fields are links. There is no claim to
have revalidated extraction against the unavailable responses or sidecars. The preserved
reports describe the collection's original checks; AF0 independently checks conversion
against the supplied CSVs only. Links and rankings are collection-time snapshots and may
change or expire. No private or authenticated source is needed to query the released data.

The six documents are under original/. The source README is original/source-README.md;
original/README.md is the explanatory index. Version 1 of the programme has only the
specified unrelated-attachment sentence replaced. The five other documents remain
byte-identical. PROGRAMME.md is the owner's version 2, committed verbatim.

## Rights and removal

**No new licence is granted over this data.** Rights in prompts, briefs, names and media
stay with their creators. Each film links back to its public project page through the
catalogue's project_url. Public availability and redistribution here do not establish
permission for other uses. Code's MIT licence and the repository's own writing's CC BY 4.0
licence do not license third-party material, quotations or linked media.

Anything is removed on request: [open an issue](https://github.com/TelesforoAleix/ai-film-practice/issues).
The owner will handle requested removals from the relevant repository material or release
assets. Do not put private information in an issue. This repository's purpose is
non-commercial research into technical creator practice.
