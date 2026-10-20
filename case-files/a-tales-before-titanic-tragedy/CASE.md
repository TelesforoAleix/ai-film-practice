# A Tales Before Titanic Tragedy — technical case file

Film `3f6e509b-f3da-4324-a746-b9d35f0b9845`, primary, most-watched only.
Codebook 1.0: **27 coded, 13 unknown, eight not_applicable, one
not_observed_in_scope**, 49 assignments. [Full evidence ledger](codes.csv);
[full-record profile and reading IDs](profile.json). All four jobs, primary
texts, parameters and usages were inspected; all film-scoped rows in all 14
tables were profiled. Exact duplicate text was read once with all four contexts
checked. The brief is unavailable. The catalogue film and its four-job public
history are different units; this case does not claim complete production capture.
Only the selected cohort has detailed records; no distinction between top films
and other films can follow.

## Study 02 — Planning

**Observed:** a persistent character sheet is explicitly requested (02.2), while
the technical brief is unavailable (02.1, 02.6). No separate shot plan, plan/task
binding or build order is established (02.3–02.5 unknown).
**Interpretation:** package preparation is visible as intent, not a project-level
production plan. **Proposed:** retain a sheet task without inventing scene order.

## Study 03 — Reusable elements

**Observed:** `416eb299-5a02-4dd1-99c1-8a11d9de0b04` requests “Generate face
close-up, side profil view, rear profil, and full body.” Subject and wardrobe
bind to two image tokens (03.1, 03.3–03.4). The export has zero named
reference-element rows. **Interpretation:** multi-angle packaging can be requested
without a disclosed named library; output fulfilment and canonical status are
unknown (03.5–03.6). **Proposed:** store package request separately from verified
package and approved version.

## Study 04 — Prompt and context

**Observed:** Subject, Grooming, Wardrobe and location sections contain numbered
image tokens, with actual `input_asset` rows at `params.input_images[0]` and `[1]`
(04.1–04.5). **Interpretation:** explicit text and attached media coexist, but the
media's property content cannot be recovered without viewing it. No context
conflict is established (04.6 unknown). **Proposed:** show text bindings and
content-unknown attachments independently.

## Study 05 — Image construction

**Observed:** one named sheet request has two distinct input IDs:
`7a44e44c-7b45-4fc5-8c8b-303f25779194` and
`612f580b-00fe-4730-a3eb-b2c49902c939` (05.1–05.2). It explicitly requests a
reference sheet (05.5), while the editing mechanism is unspecified (05.4).
**Interpretation:** two inputs establish conditioning, not layers, compositing
implementation or a successful sheet. **Proposed:** preserve multi-input identity
and intended purpose without claiming output verification.

## Study 06 — Video control

**Observed:** all four exported jobs are images; no video job is exported.
All seven video codes are `not_applicable` to this history (06.1–06.7).
**Interpretation:** this says nothing about video work outside this export or
the media in the finished film. **Proposed:** keep record eligibility separate
from catalogue publication type.

## Study 07 — Lineage

**Observed:** the same two input asset IDs feed all four jobs (07.1–07.2, 07.4).
Their producers do not resolve among the four jobs. The named consumers are
`416eb299-5a02-4dd1-99c1-8a11d9de0b04`,
`6e4ad139-8170-444a-9063-2b01b69444f9`,
`7277e1f4-4d8a-4120-b001-9a651fc36c2f` and
`a1d84f68-04f9-4894-b9f8-65e7f6eafa2d`. Exact IDs are deduplicated per consumer;
07.3 records an explicit raw/min metadata grouping, without cross-ID merging.
**Interpretation:** this is a scoped shared-input branch, not proof of a canonical
reference or resolved upstream creation chain. **Proposed:** preserve unresolved
producers in the graph rather than invent earlier generation nodes.

## Study 08 — Models and roles

**Observed:** all four jobs use `nano_banana_2`, independently retaining its
source name `Nano Banana Pro` (08.2). Reference-sheet requests support that
operation role and the shared-input graph supports a branch (08.1, 08.4).
Cross-model handoff is `not_applicable` (08.3); audio/finishing remains unknown
(08.5). **Interpretation:** the single-model record cannot describe the finished
film's whole stack. **Proposed:** preserve the boundary of the visible model graph.

## Study 09 — Iteration

**Observed:** all four primary texts and the two input IDs are identical; each
job has a different batch ID (09.1). **Interpretation:** `rerun` is a provisional
interpretation of equal requests, not four independent trials or evidence of
failure (09.2, inferred). No text/input delta is observed in the exhaustive
four-member comparison (09.3 `not_observed_in_scope`); directional revision
intent is not established. Reuse or approval of the resulting outputs remains
unknown (09.4). **Proposed:** group candidates without creating version or approval
events from equality alone.

## Study 10 — Organisation and resources

**Observed:** root/Watermarks supports a flat organisation proxy (10.1). All four
jobs have one recorded author and parseable UTC events, from 2026-08-12
00:40:50.345596 to 00:40:57.527251 (10.2–10.3). Four nonempty primary fields contain
one distinct text, giving three repeat occurrences beyond the first; none of the
four generations has multiple folder placements (10.4). The proxy is four jobs /
(313.25 catalogue-declared seconds / 60) = **0.766161 jobs per declared minute**
(10.5). **Interpretation:** the short event interval cannot be converted to labour
time; the ratio cannot measure productivity or full production effort.
**Proposed:** show numerator, declared duration and capture boundary together.

Later studies should retain this as the repeated-request example, with no verified
sheet output, upstream producer, element version or final adoption. All proposals
await the tests in the [case-file index](../README.md).
