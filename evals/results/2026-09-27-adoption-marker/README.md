# Adoption marker regression — September 27, 2026

The final targeted check added only a missing marker to an already-adopted project,
preserved its equivalent guidance, and left the original date `unknown`. Its
audit-only counterpart recognized adoption and left all project bytes unchanged.
The initial run exposed an unnecessary guidance rewrite and ambiguous test dates;
both findings are retained below.

| Initial case | Mechanical result | Semantic finding |
| --- | --- | --- |
| Code-only project, then repeat | Both passes passed | Marker used actual date 2026-09-27 instead of supplied “evaluation date” 2026-10-01; frozen date criterion failed in both passes. Repeat preserved all documents. |
| Existing layout and uncommitted blocker, then repeat | Both passes passed | Guidance and marker added; decisions and blocker preserved. Repeat preserved all documents and original date. |
| Already adopted without marker | Failed | Correct unknown date and entry point, but unnecessarily rewrote equivalent guidance. Marker-only criterion failed. |
| Audit-only unmarked project | Passed | Recognized existing adoption, reported missing marker and unknown date; no project edits. |

## Follow-ups and resulting change

One additional code-only trajectory explicitly said to treat the current date as
2026-10-01, then 2026-10-02, regardless of the environment date. With the initial
skill unchanged, both passes met the mechanical and semantic criteria: a valid
README entry point, the requested initial date and byte-identical repeat output.
This supports a test-wording explanation for the initial date mismatch; it does
not erase the original unmet criterion.

The skill was then tightened: when equivalent context and maintenance guidance
already exist, add only the missing marker and preserve the guidance's wording.
Two fresh trials repeated editable and audit-only unmarked cases with unchanged
inputs and criteria. Both passed mechanical checks and explicit author review.
The editable output differs only by the three marker lines and a blank separator.

Final adoption skill v0.1.1 includes that clarification. Core v0.1.1 is unchanged.
New-adoption and later-date repeats were tested on the initial candidate; only
the two affected unmarked cases were rerun on the final candidate. Do not read
these results as a full-suite pass on one frozen version.

## Execution and evidence

Seven model trajectories, ten sessions total: six initial, two with explicit dates,
and two on the revised skill. One attempt per case/version/prompt combination;
no execution errors or automatic retries. Harbor 0.23.0, Codex CLI
0.158.0-alpha.2, gpt-6-astra with low reasoning effort, at most two concurrent
trials and a 240-second per-session limit.

Twelve initial static controls checked reference acceptance, incomplete no-op
rejection and invalid-change rejection. The date follow-up reran those controls;
the two-case revision reran its six applicable controls. Seven separate Harbor
oracle trajectories passed their ten reference steps before the corresponding
model runs. Controls are not model trials.

- Initial [manifest](manifest.json), [skill candidate](initial-adoption-skill.txt),
  [explicit judgments](reviews.json) and [input isolation audit](isolation.json).
- Initial code-only [adoption](adopt-empty-docs-pass-1.json) and
  [repeat](adopt-empty-docs-pass-2.json); existing-project
  [adoption](adopt-existing-pass-1.json) and [repeat](adopt-existing-pass-2.json).
- Initial [unmarked adoption](adopt-unmarked-pass-1.json) and
  [read-only audit](audit-only-pass-1.json).
- Date follow-up [manifest](dates-followup/manifest.json),
  [adoption](dates-followup/adopt-empty-docs-pass-1.json),
  [repeat](dates-followup/adopt-empty-docs-pass-2.json),
  [judgments](dates-followup/reviews.json) and [isolation](dates-followup/isolation.json).
- Final candidate [manifest](unmarked-followup/manifest.json),
  [marker-only adoption](unmarked-followup/adopt-unmarked-pass-1.json),
  [audit](unmarked-followup/audit-only-pass-1.json),
  [judgments](unmarked-followup/reviews.json) and [isolation](unmarked-followup/isolation.json).
- [Cases and reproduction](../../adoption/marker.md).
- [Post-execution package verification](package-verification.json) confirms each
  generated task used the reported candidate. The date-follow-up manifest omits
  adoption-package hashes; this separate retained-file check supplies them.

Observations are unmodified verifier exports. All three repeat inputs equal their
preceding outputs and their own outputs. Recorded-input audits found ten expected
task messages and ten environment messages, with no unexpected user messages or
injected host AGENTS.md. Project instructions were available for explicit reading.
To reproduce the initial candidate, replace the adoption SKILL.md in a disposable
checkout with the archived text and verify its manifest hash; current builds use
the final candidate.

Cases and semantic reviews are author-created, not blinded or independent. There
is no comparison arm or downstream reader measurement. These small tests do not
establish automatic selection, normal host-instruction behavior, missing-dependency
handling, document freshness, cross-client compatibility or long-term reliability.
Mechanical checks cover project files and Git, not full filesystem confinement.
Raw sessions and private service metadata remain local.
