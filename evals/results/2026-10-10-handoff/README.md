# Fresh-session handoff pilot — October 10, 2026

Both fresh Claude Opus 5.5 sessions implemented the synthetic continuation
correctly, but the curated agent omitted restating the approved constraint’s
rationale in its own output. Scattered notes met all six semantic criteria; curated
context met five. No curated advantage was observed in this one pair. Actual
human correction effort was not measured.

| Observation | Curated context | Scattered notes |
| --- | --- | --- |
| Semantic criteria | 5/6 pass | 6/6 pass |
| Independent CLI acceptance checks | 8/8 pass | 8/8 pass |
| Agent-written local tests | 12 pass | 8 pass |
| Agent wall time | 42.5 seconds | 27.2 seconds |
| Tool calls / file reads | 11 / 7 | 11 / 7 |
| Test-command calls / denied calls | 1 / 0 | 1 / 0 |
| Code corrections / report omissions identified | 0 / 1 | 0 / 0 |

Both arms found the owner-approved arrival-order constraint, superseded sorting
proposal and unresolved missing-v3-sample blocker. Curated consumed the rationale
in its documents but did not restate it in agent-authored evidence or its final
answer. Scattered explicitly named arrival order as downstream priority. The
reviewer distinguished consuming evidence from identifying the rationale; the
coordinator accepted a conservative fail on that part of the frozen criterion.
Both implementations preserve default output and source bytes and reject invalid
limits with argparse exit 2. Both final answers retain the sanitized-sample next
action and production uncertainty. All fixture reads were considered relevant.
The curated reader used the summary and opened the three substantive linked
notes; the scattered reader opened all four notes. Neither needed investigation
outside the fixture.

The question was whether curated context helps a fresh agent continue correctly,
with fewer omissions and less human correction. Correct continuation was
observed in both arms. No correction was supplied by design. The reviewer found
no required code correction, but identified one curated report omission under
the frozen criteria. Actual human correction effort
was therefore **not measured**. This is a small supplied-handoff test, not an
assessment of context maintenance or ordinary novice-user work.

## Protocol and execution

The [frozen manifest](protocol.json) records complete fixture text, exact task,
expected outcomes, acceptance criteria and hashes before subject execution.
[SHA-256](protocol.sha256) identifies the final freeze. The
[initial preflight manifest](preflight-protocol.json) and its
[hash](preflight-protocol.sha256) are retained. Following preflight, the final
freeze added protected-byte checks and scoring clarifications; it changed no
subject task, fixture or acceptance outcome. The
[coordinator disposition](preflight-verdict.json) records why both conditions
were met.

Identical code, baseline tests, raw notes, model and tools were supplied. The
curated arm additionally received a README link, an explicit instruction to read
the entry point, and an author-prepared summary containing no unique facts.
Both sessions disabled skills, used project-only settings, disabled auto-memory,
exposed the same six tools and loaded no MCP servers. There were no observed
external instruction-loading events. That is an observation, not a guarantee
about all hidden runtime instructions. Requested effort was high in both; the
runtime effort level was not independently exposed.

Each arm had one attempt, seven minutes maximum, with curated first. Opus
preflight and final assessment reviews had three minutes each. No retry, resume,
model fallback, API fallback or global setting changes were used. Total agent
execution, including both reviews, was **204.5 seconds** (3 minutes 24.5 seconds),
within the 20-minute cap. The launcher
used existing Claude.ai Max authentication, verified before execution; API and
alternate-provider environment settings were removed from its process.
Streams confirm the responding model as **`claude-opus-5-5`**. Codex performed
the Sol coordination, implementation and validation role; this chat did not
independently expose its precise model identifier, so confirmed Sol 6.1 runtime
identity is not claimed. No substitute collaborator was used; Opus was available.

The harness reuses the native smoke launcher and file-tool event recorder, with
a pilot-specific code/test write scope and one permitted test command. These
hooks are not an OS sandbox: agent-written Python tests could bypass file-tool
controls. Code and tests were inspected for external reads, writes and network
behavior; none were found. All protected fixture, frozen protocol and control
bytes remained unchanged. Bytecode caches and temporary test files are normal
Python execution artifacts, excluded from source diffs. This does not establish
adversarial isolation.

## Evidence and validation

- [Protocol and harness](../../handoff/README.md); exact frozen harness snapshots
  are retained in `harness/`.
- [Trial records](trials.json), [coordinator assessment](assessment.json),
  [curated patch](curated.patch) and [scattered patch](scattered.patch).
- [Curated checks](curated-checks.json) and [scattered checks](scattered-checks.json)
  contain eight independent CLI cases and coordinator reruns of each generated
  suite. [Baseline control](verifier-baseline-control.json) shows the verifier
  rejects the starting code's missing limit behavior.
- [Verifier freeze](verification-freeze.json): the independent check script was
  finalized after the curated session completed and immediately before scattered
  started. The coordinator reports no output inspection before this freeze;
  session logs do not independently verify that inspection timing. Expected
  outcomes were already frozen; this is supporting validation, not a
  prospectively frozen new endpoint.
- Raw streams in `logs/`, hook records in `control/`, final project trees in
  `projects/`, and [curated](curated-final.txt)/[scattered](scattered-final.txt)
  final answers retain the complete attempts. These are synthetic fixtures.
- [Opus preflight review](preflight-final.txt) and
  [execution record](preflight-execution.json) retain its conditions and limits.
  [Final Opus review](review-final.txt) and its
  [execution record](review-execution.json) retain the rationale-scoring finding
  and verifier/timing qualifications. [Initial assessment](assessment-before-review.json)
  preserves the coordinator’s initial all-pass score; the final assessment
  accepts all four findings without changing agent artifacts or rerunning.

Repository static checks validate packaging, links and published historical tables;
they are separate from the two actual fresh-agent sessions. Historical studies,
released skills and scores were not modified. No skill version or release change
was required. Nothing was committed or published.

## Limits and next step

This is one author-created, small, fixed-order case with unblinded assessment.
Observed timing also reflects the fixed order, additional routing text/document,
different final response length/thinking and different generated test counts; it
is not a causal efficiency estimate. The summaries expose status labels directly, and the ordinary notes also make
owner authority and chronology easy to recover. Both agents could read the
relevant facts cheaply. No statistical significance, allowance savings or general
comparative benefit follows from the result, test count or model timing.

If a further study is authorized, use a larger matched fixture with dispersed
code dependencies and a prospectively frozen retrieval budget. Equal reads and
correct outcomes here indicate that this case did not create meaningful retrieval
pressure. This is a proposal; no broader evaluation was launched.
