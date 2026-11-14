# November 14 public-project documentation evidence

**Experiment date: November 14, 2026.** See the [report](../../../docs/evaluation-2026-11-14-public-project-docs.md)
for methods, all scores, disputes, audit flags and interpretation limits.

| File | Contents |
| --- | --- |
| [study.json](study.json) | Captured client/model configuration, method-package hashes, exact prompts and output schemas, order/label maps, caps, session outcomes/usage and complete results summary |
| [P01.json](P01.json) | Pinned `ulyssestenn/omt` source, three reader views/answers, reference items, both final grades and reconciliation |
| [P02.json](P02.json) | Pinned `Alex72-py/aria-termux` source and the same evidence fields |
| [P03.json](P03.json) | Pinned `kMegapnbedt/Bench-B` source and the same evidence fields |
| [derivation.json](derivation.json) | Included/excluded fields and any privacy-only text substitutions |

All 61 files in the three captured trees are included in `source_files`, including
their original MIT `LICENSE` texts and copyright notices. Upstream material retains
those notices and licenses; its inclusion is not an upstream endorsement. Repository
URLs and exact commits identify the captured sources, not their present state.

Each condition's `documents` contains its complete filtered reader view; `text`
retains original line numbers through unchanged newline structure. `file_origin`
distinguishes unchanged, modified and created whole files. A modified file can
retain inaccurate upstream claims; this field does not attribute individual claims.
Answers and grades are final emitted JSON objects, not coordinator rewrites.

## Derivation and integrity

The private originals remain unchanged. The public derivative preserves:

- All nine reader answers, all six final grade objects, every dispute, key
  assessment, document-audit flag and per-item judgment.
- Every per-project metric and fixed denominator, including partials, uncertainty
  intervals, mechanical citation checks and missing-output status.
- The exact reference-item fields supplied to graders. Selection-only
  `existing_prose_coverage` and other preparation metadata were not grader input
  and are omitted; the key's original byte hash is retained.
- Complete selected source and reader-document text with original/public UTF-8
  byte hashes and line counts. `original_content_sha256` hashes the original bytes;
  `public_content_sha256` hashes the included text encoded as UTF-8.

Known private workspace prefixes would be replaced with explicit portable
placeholders, preserving newline counts and recording every changed field in
`derivation.substitutions`. **No included score-bearing text required a substitution
in this extract.** Private paths in session metadata were excluded by field
selection, along with private invocation IDs, account/global configuration,
operator workflow records, raw tool/transport logs and writer conversations.
Original aggregate/input/output hashes are provenance references, not claims that
private original files are publicly accessible or independently authenticated.

The original pass-2 packet contained the pinned project source, reference items,
saved docs and reader answers; it did not contain writer requests or method
packages. This extract additionally exposes the prompt templates and package
provenance for inspection. They were **not** retrospectively supplied to graders.
The report retains the resulting method-authority audit limitation and every flag.

## Verification limits

This is an inspectable derivative, not a complete harness or turnkey replay.
The nonselected screening corpus, controller source, raw startup/tool capture and
private environment are not included. Included source, answers and judgments let
readers inspect scoring reasoning; they do not independently establish actual
model reads, full isolation or every effective runtime setting.

The keys and grades have no human oracle validation. Same-model dependence,
partial blinding, disputed items and single-pass document-audit uncertainty remain.
No new model session, adjudication or score change was used to prepare the extract.
