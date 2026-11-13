# November 13 Markdown-maintenance comparison evidence

**Local publication draft; not published.** See the
[report](../../../docs/evaluation-2026-11-13-markdown-maintenance.md) for results,
method, attempt history and interpretation limits.

[evidence.json](evidence.json) is a public derivative of the completed local
study. It contains:

- All six condition-labeled receiver answers and final synthetic project
  snapshots, including source text inspected by receivers.
- Per-fact first-pass and final grading, support quotations, document IDs and
  line references, plus critical-error diagnostics and condition guesses.
- The frozen rubric and oracle, exact stage messages/order/caps, stage outcomes,
  read-evidence summaries, as-run scores and clean-comparison exclusions.
- A separate summary of the earlier partial grades and stopped attempts.

In each cell, `documents` maps grading document IDs to project-relative paths.
`origin` and `writer_modified` distinguish pre-existing evidence, the supplied
rule update and writer-created/modified context. Survival of an initial fact is
not presented as a newly captured chat-only fact. `answer` is the receiver's
emitted text, subject only to the transformations below.

## Derivation and boundaries

The extract uses these explicit transformations:

1. Absolute study workspace prefixes become `<project>/` in answers and
   citations. The proposed scratch directory becomes `<scratch-workspace>/`.
   These are portable placeholders, not live links or additional evidence.
2. Incidental operator storage references are generalized. One two-line backup
   destination passage is replaced with a clearly marked omission while
   preserving its line count. Its input-preservation rule remains intact.
3. Private invocation IDs, raw controller events, account/configuration details
   and operator workflow records are excluded from the extract.

The `derivation.substitutions` list identifies changed cell/field locations.
All included source-text transformations preserve line counts. Grades, fact
qualifications, thresholds, dates, numeric ratios, error counts and eligibility
flags are unchanged. No outcome-specific answer rewrite or regrade occurred.
The original frozen run remains unchanged. `original_content_sha256` refers to
the private original document bytes; it does **not** hash transformed text.
Original aggregate/grade/source-packet hashes are provenance references, not
proof of public availability or independent authenticity.

This is inspectable artifact evidence, not a self-contained experiment runner.
The initial fixture package and complete harness/startup logs are not included.
Read summaries report the retained local capture check; without raw tool events,
the public extract alone cannot independently establish what a model actually
read or all effective sandbox controls. Those boundaries and the excluded B
read check remain explicit in the report.

No new subject run or grading session was performed to prepare this extract.
