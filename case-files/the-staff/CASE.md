# The Staff — technical case file

Film `3b09c7c2-3f0c-48e3-8304-fad569bf50ce`, primary, shortlist only.
Codebook 1.0: **43 coded, six unknown**, 49 assignments.
[Full evidence ledger](codes.csv); [full-record profile and reading IDs](profile.json).
All 82 job contexts were inspected through their technical prompt sections,
controls and usages; the visible brief, 28-folder register and 23 reference
records were read. All film-scoped records in all 14 tables were profiled. Long
prompts were inspected for technical instructions, not exhaustively annotated
word by word; unknown semantic codes remain unknown. This selected case cannot
establish what separates top films from other films.

## Study 02 — Planning

**Creator-stated:** the substantive Production section specifies an “18-minute
episodic anime pilot” (02.1, 02.6), while Resources names character sheets (02.2).
**Observed:** `04b90dc8-b9f9-48cf-858f-1cdcc2dceecb` contains timed shot boundaries
(02.3). `1d963033-bc45-495d-9bfa-a05e4d0cf918` explicitly says “frame 1 same last
frame from here” with an attached input video (02.4). **Interpretation:** local
planning and a task binding are visible; neither the claimed whole pipeline nor
actual project build order is established (02.5 unknown). **Proposed:** keep
brief declarations and local task bindings as separate, source-linked objects.

## Study 03 — Reusable elements

**Observed:** all 23 disclosed reference records include literal character,
prop and environment categories (03.1; mapping environment to location is
inferred). Image job `6d514bd2-9aa3-4543-89a2-8f547a5385bb` requests poses and
expressions “while maintaining the exact original identity and art style.”
(03.2–03.4). Video job `27e11480-06e7-4b7a-8420-2be1c09b058a` assigns elements
“final authority” within its task (03.6). **Interpretation:** requested packaging,
identity preservation and scoped authority do not establish a verified sheet,
global canonical library or element version chain (03.5 unknown).
**Proposed:** scope authority to the task and store version approval independently.

## Study 04 — Prompt and context

**Observed:** the sheet-edit request has an actual input image; text explicitly
specifies preservation while its media content remains unknown (04.1–04.5).
`46e851da-ea8f-45ea-8602-88660f0885e3` says “THIS CLIP HAS NO SPEECH IN IT.” and
later appends “A man speaks in Japanese, alone, close on his face.”
**Interpretation:** this is a possible context conflict (04.6, inferred); the
appended directions may be separate drafting material rather than instructions
for that silent clip. No model-confusion or output claim follows.
**Proposed:** show the paired spans and ask a reviewer to settle their intended scope.

## Study 05 — Image construction

**Observed:** the film's one image job uses `seedream_v5_pro`, an attached input,
a sheet/expression-change request and `is_inpaint=false` (05.1, 05.3–05.5).
**Interpretation:** reference-guided local-edit intent is visible, while a mask,
layer or successful expression change is not. Image convergence is unresolved
(05.2). **Proposed:** preserve requested change, identity constraint and literal
mechanism disclosure independently.

## Study 06 — Video control

**Observed:** the named video example `04b90dc8-b9f9-48cf-858f-1cdcc2dceecb`
contains “SHOT 1 (0–4s)” and “HARD CUT TO SHOT 2 (4–7s)” while `multi_shots=false`;
it has `duration=15`, `resolution=1080p`, `aspect_ratio=16:9`,
`generate_audio=true`, `draft=false`, `extension_mode=null` (06.1, 06.3–06.4,
06.6). “handheld tilt down and in, about half a metre” specifies camera action
(06.2), and a staff-appearance invariant specifies what to preserve (06.5).
**Interpretation:** shot wording is not a control activation or achieved timing;
no scoped shot revision is established (06.7 unknown). **Proposed:** retain the
planned boundaries beside raw model controls and invariants.

## Study 07 — Lineage

**Observed:** producer `0e619b88-43ef-4a45-84c3-b7b86ac96fe4` is consumed by
`1d963033-bc45-495d-9bfa-a05e4d0cf918` through the identically named asset at
`params.medias[1].data`, role `input_video` (07.1, 07.4). Searching all 82 jobs,
121 assets and 462 usages resolves only this producer/consumer pair. A separate
two-consumer motif shares four exact reference assets (07.2); raw/min metadata
representations are retained under one asset ID (07.3).
**Interpretation:** numerous disclosed references do not imply resolved upstream
producers. **Proposed:** after the named producer changes, review its one reachable
generation, `1d963033-bc45-495d-9bfa-a05e4d0cf918`, under the exported graph boundary
(07.5). This does not prove visual change or include hidden dependencies.

## Study 08 — Models and roles

**Observed:** literal identifiers are `seedream_v5_pro` (one image),
`cinematic_studio_video_4_0` (six videos) and `seedance_2_5` (75 videos). The image
request supports a sheet/local-edit role (08.1–08.2); the only resolved transition
is seedance_2_5 → seedance_2_5 (08.3–08.4). **Interpretation:** the three models
co-occur, with one observed stage, but a cross-model handoff is not established.
Audio intent and the brief's sound-design pipeline do not establish a standalone
audio job or an explicit external-tool record (08.5 unknown).
**Proposed:** show model co-occurrence separately from traced transitions.

## Study 09 — Iteration

**Observed:** `04b90dc8-b9f9-48cf-858f-1cdcc2dceecb` and
`ec163001-6ba3-4ebf-9155-b6c73e05a9b6` have identical primary texts and share four
exact reference assets (09.1). **Interpretation:** these support a candidate
rerun family (09.2, inferred), not independent experiments, directional revision
intent or a measured failure. Revision delta remains unknown (09.3). The explicit
producer/video-input edge establishes further-work adoption, not approval (09.4).
**Proposed:** separate candidate grouping, actual deltas, reuse and acceptance.

## Study 10 — Organisation and resources

**Observed:** ACT/Scene folders and Ref support scene/entity organisation (10.1,
inferred meaning of literal labels). All 82 jobs have one recorded author and
parseable UTC events, from 2026-08-18 01:36:52.348671 to 2026-08-22
20:14:42.841588 (10.2–10.3). There are 70 distinct nonempty primary texts among 82
fields, or 12 repeat occurrences beyond the first; no generation has multiple
folder placements (10.4). The proxy uses 82 jobs /
(266.791667 catalogue-declared seconds / 60) = **18.441356 jobs per declared
minute** (10.5). **Interpretation:** the brief's stated 18-minute format and the
catalogue duration have distinct provenance; neither should silently replace the
other. This proxy and event window do not estimate labour, cost or productivity.
**Proposed:** preserve both duration declarations and the proxy's chosen denominator.

Unknowns are build order, element versions, image convergence, shot revision,
audio/finishing visibility and directional revision delta. Later studies should
retain the possible speech-scope conflict for adjudication and the sharp boundary
between reference disclosure and resolved lineage. All proposals await the tests
in the [case-file index](../README.md).
