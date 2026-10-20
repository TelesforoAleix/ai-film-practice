# Higgsfield festival research dataset

Start with `RESEARCH_HANDOVER.md` and `reports/validation_report.md`. `data/priority_films.csv` is the selected/popular 186-film set, sorted by available views. `data/films.csv` is the full 6,224-film index.

Detailed scope: 163 public priority listings after 23 non-open-source exclusions, plus one supplemental pilot. Current public priority statuses: {"complete_public_workspace": 157, "unavailable_workspace": 6}. This scope supersedes the initial request to deeply extract every festival film.

## Reproduce or resume

Requirements: Python 3.10+, curl, Node.js 18+. No API key is needed. Brief snapshot retrieval is disabled following visibility review; saved sanitized briefs support offline export. From this directory:

```bash
npm install --prefix scripts --no-audit --no-fund yjs@13.6.33
python scripts/extract.py
python scripts/enrich.py
python scripts/recover_leaf_assets.py
python scripts/sanitize_visibility.py
python scripts/export_dataset.py
python scripts/validate_csv.py
python scripts/build_reports.py
python scripts/package_archive.py
```

After collection and resource recovery finish, `python scripts/finalize.py` runs the offline sanitation, export, integrity checks, reports and ZIP build in order, stopping if required checks fail.

Cached raw responses are reused. The included `reports/extraction_scope.json` preserves the agreed scope; the extractor filters out non-open-source projects. `--all` expands to all open listings only and can be substantially larger. Do not remove exclusions or substitute authenticated/private endpoints. A fresh catalog snapshot may change membership; retain the supplied raw files to reproduce this specific dataset.

CSV encoding is UTF-8. `\N` means unavailable; empty strings remain empty. JSON fields are serialized JSON. Use a CSV-aware parser with an adequate field-size limit, rather than splitting on lines or commas. Complete prompts can exceed spreadsheet cell limits. Example:

```python
import csv, sys
csv.field_size_limit(sys.maxsize)
with open('data/generations.csv', encoding='utf-8', newline='') as f:
    for generation in csv.DictReader(f):
        pass
```

No film/image/audio binaries or installed dependencies are included. The archive retains only metadata, source JSON, sanitized document records, scripts and reports. Model/provider names and asset lineage are only assigned where disclosed. See the handover for compound keys, counts, field definitions and limitations.

## Extract the archive

The two largest CSV tables use LZMA compression inside the ZIP to fit the download size limit. Python 3 supports every archive member. Extract with:

```bash
python3 -m zipfile -e higgsfield_festival_research.zip higgsfield_extracted
```

The standalone `generations.csv.gz` download decompresses to the same plain generation CSV included in the ZIP.
