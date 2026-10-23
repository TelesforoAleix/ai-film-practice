# Provisional prompt-label releases

[prompt-labels-v2](https://github.com/TelesforoAleix/ai-film-practice/releases/tag/prompt-labels-v2)
publishes the finished AF3b2 labels and report data for Study 04. The 27B labels
are primary; Jev remains a separate presence-only cross-check. Labels are
provisional inferred assignments to explicit text instructions, not achieved
media properties. Study 04 owns written conclusions.

## V2 assets and verification

The release contains exactly these five assets plus `SHA256SUMS`:

| Asset | Bytes | Contents |
| --- | ---: | --- |
| `labels.jsonl.gz` | 2,101,007 | Final primary successes and failures, source keys, settings and spans |
| `jev-presence.jsonl.gz` | 829,014 | Full-sample presence-only cross-check |
| `jev-gold-presence.jsonl.gz` | 51,952 | Separate gold-subset cross-check run |
| `report.json` | 2,508,720 | Coverage, agreement, disagreement IDs, prevalence and limits |
| `manifest.json` | 6,882 | Settings, input/tool hashes, cleaning rules and asset hashes/sizes |
| `SHA256SUMS` | 421 | SHA-256 hashes of all five assets |

`report.json` exceeds the 1 MB commit limit and lives only in the release.
Full source fields are not included. Local builds and downloads stay under
ignored `data/`; no data files are committed.

From a repository checkout, choose a new download directory:

```bash
uv sync --locked
gh release download prompt-labels-v2 --repo TelesforoAleix/ai-film-practice --dir data/prompt-labels-v2-download
uv run python prompt-labels/release.py --check data/prompt-labels-v2-download
```

The offline check verifies the exact asset set, checksums, manifest hashes and
sizes, schema, IDs, source linkage, model-name cleaning, coverage and privacy
patterns. The finished build and a fresh download to
`data/af3b-finished-download/` both passed. Exact-substring checks require the
corpus and ran during building; the offline check does not repeat them.
Rebuild commands and schema details are in [README.md](README.md#af3b-check-the-finished-journals-and-build-prompt-labels-v2).

## Finished run and descriptive checks

The eight primary journals finished on 23 October 2026 at 12:11. Every one of
5,000 sampled texts has a terminal record: **4,633 successes and 367 final
labelling failures (7.34%)**, with zero missing or pending. Failure types:
364 `ValueError`, two `Interrupted`, one `HTTPError`. Failures remain unknown,
never fourteen absent labels. Jev completed 5,000/5,000 sample texts and its
separate 300/300 gold texts without failures.

The primary reported model is `Qwen3.6-27B-Q4_K_M.gguf`, requested as
`local-model`, with AF3a-v3 labels and codebook 1.0. Recorded request settings:
temperature 0, max_tokens 1400, stream false; maximum three attempts per text,
timeout 600 seconds. Span resolution is
`nfc-casefold-whitespace-quotes-dashes+ellipsis-cover`. The manifest preserves
run/template hashes and settings. Jev reports `jev-1.14.0`; its configuration
hash is retained, while client defaults are not independently attested execution
settings.

Pooled presence agreement uses fourteen decisions per paired text:

| Comparison | Paired texts | Decisions | Cohen's kappa | Accuracy |
| --- | ---: | ---: | ---: | ---: |
| 27B–gold | 276 | 3,864 | 0.779205 | 0.906573 |
| Full-sample Jev–gold | 300 | 4,200 | 0.747471 | 0.889286 |
| Separate Jev gold run–gold | 300 | 4,200 | 0.743113 | 0.887143 |
| 27B–Jev | 4,633 | 64,862 | 0.732228 | 0.886929 |

The largest 27B–Jev component disagreement counts are preservation 976,
identity 844, material 681 and aesthetic intent 681, each over 4,633 paired
texts. These counts do not adjudicate which label is correct. The report
retains all component counts and disagreement IDs.

All **47,666 positive spans** passed exact-substring source checks, over
64,862 decisions in 4,633 successful texts. These include 1,930 ordinary
resolved spans and 1,329 joined ellipsis-cover spans. The release withholds
35 spans equal to their entire source field: they retain `present: true`,
`span: null`, `span_withheld: "full_source_field"`, a hash and character count.
Consumers must distinguish withheld positives from absent components. The
older raw-label agreement reader expects ordinary spans; released report data
already accounts for withholding.

An independent scan of every decompressed asset found **zero e-mail,
absolute-path, loopback/private-IP and phone-number matches**. Model names are
reduced to file names and endpoints are omitted by the release builder.
Pattern checks do not prove absence of every possible private item.

Gold is single-agent and unadjudicated; 24/300 gold texts lack successful
primary labels. No shot-prompt or negative-role gold coverage exists. The
balanced sample is not a corpus prevalence estimator; texts above 12,000
characters are excluded from semantic sampling. Repeated passages and films
by one creator are not independent observations. These checks establish source
correspondence and descriptive agreement, not semantic correctness. No new
licence is granted over third-party text.

## V1 structural features and sample

[prompt-labels-v1](https://github.com/TelesforoAleix/ai-film-practice/releases/tag/prompt-labels-v1)
contains AF3a structural features and semantic sample source IDs, built from the
verified `data-2026-10-20` snapshot under Study 01 codebook 1.0.

Assets: `features.parquet` (61,542 exact-text rows), `occurrences.parquet`
(160,753 compound source-field occurrences), `sample.jsonl.gz` (5,000 unique
primary-film text IDs), and `SHA256SUMS` (all three asset hashes). No full prompt
texts. The sample excludes texts above 12,000 characters; structural features
retain them. V2 adds the finished labels without replacing these inputs.

Method, exclusions, gold limits and commands: [README.md](README.md).
Neither release alters or relicenses the original third-party data.
