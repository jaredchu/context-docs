# Larger matched handoff with a frozen retrieval budget

A separate continuation of the small handoff pilot. It compares supplied curated
context plus explicit routing with ordinary scattered notes on identical synthetic
code and underlying facts. It does not change released skills or previous results.

Preparation is a bounded Opus 5.5 assignment: author `fixture.json` and an
independent executable verifier. Codex inspects the important code boundaries,
source authority, information equivalence, budget feasibility and baseline
controls. Freeze includes complete fixture text, prompts, expected outcomes,
acceptance criteria, verifier and harness hashes **before both subjects start**.

The first preparation attempt timed out without artifacts; Codex completed the
predefined fixture and verifier, retaining that failed assignment.

Both fresh readers use exact `claude-opus-5-5`, existing Claude.ai subscription
access, high requested effort, no skills or MCP, and the same five file tools.
Their scoped patch adds a CLI limit through dispersed modules while preserving
validation, tenant filtering, deduplication, arrival order and source bytes.

Each condition has:

- 16 full-file Read calls and 16,000 UTF-8 file bytes, charged before admission.
  Repeat reads consume the budget again; admitted failed calls count conservatively.
- Six Glob/Grep calls. Grep matches file contents but returns filenames only, revealing
  routing/match information; full file contents must be loaded with Read. Filename-result bytes are not charged to the content budget.
- Seven minutes and one attempt, with no human correction, retry or resume.

Read offset/limit/pages, outside-project paths and unscoped writes are denied.
No subject code execution is exposed: tests run only during coordinator validation
of the finished patches, preventing a test from bypassing the retrieval budget by
reading notes. Subjects must report that execution limit honestly. This common
tool change from the first pilot is part of the design, not an observed skill
benefit. File-tool guards are not a general OS sandbox.

Total delegated-agent execution cap: 20 minutes, allocating 180 seconds to fixture
authoring, 420 per condition, and 180 to counterpart outcome review. Fixed order
is scattered then curated. These are one-off sessions, not an automation.

The `study.py` modes are `freeze`, `run`, and `review`, each followed by the external
workspace path. `freeze` requires an author fixture/verifier and a coordinator
`preflight.json` with `accepted: true`. The coordinator owns this disposition;
a subject never sees criteria or verifier through the permitted tools. Run modes
reject existing attempts and source/hash drift. Do not bypass those checks or
retry an exhausted subject. Retain all results, partial artifacts and failures.

Mechanical controls can be checked independently:

```sh
python3 -m unittest discover -s evals/handoff-large -p 'test_hook.py' -v
python3 evals/checks/static_checks.py
```

Semantic review distinguishes preserving a constraint in code from explicitly
identifying its owner rationale. Read exposure alone does not fulfill an
agent-authored acknowledgement criterion. Count budget denials and incomplete
work; do not equate time, bytes or model-token fields with human effort or
subscription allowance savings. This is one author-created pair with fixed order
and unblinded review; report no statistical significance.

[October 10 results](../results/2026-10-10-handoff-large/README.md).
