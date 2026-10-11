# Pending counterpart review

Status: **not launched**. This packet is development review, not a pilot subject
trial. Use Claude Opus 5.5 through existing subscription-authenticated access only
after its credential/global-state boundaries are established. Sol implemented
the preparation because a safely isolated Opus development environment has not
been established. Do not claim a review from the earlier plan review.

Budget: one initial review and one focused follow-up for material corrections,
90 seconds each; no further loop, substitution, API fallback or additional spend.
Return specific findings with file/function references; do not edit files.

Review [requirements](../../../docs/v1.0.0-validation-plan.md),
[cases](cases.json), [recipes](fixtures.json), [ledger](ledger.json),
[checker](checker.py), [preparer](prepare.py), [controls](test_wave1.py),
[isolation evidence](isolation.json) and [actual checks](preparation.json).

Focus on:

- Scope and preservation: read-only Git inspection, ignored descendants, added or
  deleted files, symlinks/modes, strict index bytes, original journal prefix and
  unrelated staged versus working content. Does any allowed path hide collateral
  writes or a customization loss?
- Trial validity: 22 sessions/4,080 seconds, separate old-release variants and
  core-only scope, actual journey output carried forward, no exposed answer key,
  exact prompt sequences and no implicit retries or fabricated native success.
- Scoring boundaries: mechanical/literal controls versus required source-backed
  semantic, non-leakage, task-test and loading/fresh-session evidence. Is any
  unsupported outcome promoted to pass?
- Isolation: source/help observations are distinct from unverified authentication,
  user skill selection, memory, shared stores and access control. Routes must stay
  blocked when those prerequisites or counterpart review are missing.

The current package snapshot equals released v0.1.9 and is not approved as a stable
candidate. Preparation tests use synthetic temporary copies; no native subject
session exists. The packet must remain outside subject access during later trials.
