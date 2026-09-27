# Adoption regression — September 27, 2026

Both synthetic projects passed initial adoption and a fresh-session repeat.

| Project | Adoption | Repeat with no new evidence |
| --- | --- | --- |
| No documentation; CSV conversion script only | Source-backed context, README navigation and ongoing AGENTS.md rule created | All project files unchanged |
| Existing custom layout, authority rules and uncommitted blocker | Only AGENTS.md extended; existing knowledge and rules preserved | All project files unchanged |

Two trajectories, four model invocations, one attempt each. Harbor 0.23.0,
Codex CLI 0.158.0-alpha.2, gpt-6-astra with low reasoning effort, two concurrent
trials and a 240-second per-session limit. No scored execution errors or retries.
Both sibling skills were explicitly loaded from the supplied package. Core skill
v0.1.1 was unchanged; adoption skill v0.1.0 was fixed before execution.

Eight static grader controls passed before execution: reference acceptance,
first-pass no-op rejection, unchanged-repeat acceptance and broken-link rejection
for each case. Two separate Harbor oracle trajectories passed all four reference
steps. These controls are not model trials.

## Evidence

- [Frozen inputs, package/source hashes and control outcomes](manifest.json)
- [No-docs adoption](adopt-empty-docs-pass-1.json) and [repeat](adopt-empty-docs-pass-2.json)
- [Existing-project adoption](adopt-existing-pass-1.json) and [repeat](adopt-existing-pass-2.json)
- [Explicit author reviews and execution counts](reviews.json)
- [Recorded-input isolation audit](isolation.json)
- [Cases, criteria and reproduction](../../adoption/README.md)

Observed files are unmodified verifier exports with actual input/output documents
and mechanical checks. Each second-pass input matches its first-pass output and
its own output; non-document code and Git state also pass preservation checks.
The no-docs output distinguishes source observations from owner decisions and
runtime verification. The existing project's Approved offline rationale, Proposed
cloud sync and Unknown restore blocker remain unchanged.

The input audit found four expected task messages and four environment messages,
with no unexpected user messages or injected host AGENTS.md. Project AGENTS.md
was available for the model to read; disabling automatic host injection does not
remove that project evidence.

These small cases and semantic reviews are author-created, not independent or
blinded. There is no comparison arm or downstream reader measurement. These runs
do not establish automatic selection, behavior with ordinary host instructions,
missing-dependency handling, audit-only adoption, cross-client compatibility or
long-term maintenance reliability. Mechanical checks cover project files and Git;
no full filesystem-confinement claim is made. Raw agent sessions and private
service metadata remain local.
