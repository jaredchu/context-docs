# Native Claude Code smoke test

Status: **native evaluation completed with mixed results; merge recommendation
on hold.** The [eight-session paired comparison](../results/2026-09-28-native-paired/README.md)
finds CSV overclaims in both ordinary and skills conditions, with stale-state
updates passing in both. It does not establish a skill-specific cause for the
original errors. Some loading confirmations remain unverified, and command traces
show out-of-project scratch writes in both conditions. The report distinguishes
those findings from preserved files and optional command denials.

The earlier [second unreleased candidate](../results/2026-09-28-native-v014-followup/README.md)
passes five of six semantic sessions; [targeted discovery](../results/2026-09-28-native-state-followup/README.md)
retains a CSV overclaim and stale README summary. All earlier authentication,
input-contamination, parser and factual failures remain recorded without rescoring.

This is a smoke test, not a comparison: there is no ordinary-maintenance arm, no
reader phase and one attempt per session. It can show that the skill loads and
behaves acceptably on this client, or that it does not. It cannot establish
accuracy, reliability or any advantage.

The completed [bounded paired comparison](paired-protocol.md) tests two fresh cases with
and without the unchanged skills, using identical requests and two attempts per
condition. Its frozen decision rule separates a repeatable adverse association
from shared model errors. This adds a baseline absent from the smoke runs.

## What it checks

| Question | How it is checked |
| --- | --- |
| Skill discovery and invocation | `Skill` tool calls and installed-package reads, parsed from the session's own streamed output. One trajectory never names the skill, so selection must come from the description. |
| Rule placement, Claude-only project | `CLAUDE.md` is the loaded file; the rule and marker must land there, with no unloaded `AGENTS.md` holding the only copy. |
| Rule placement, mixed instructions | Both files exist and only `CLAUDE.md` is loaded; the rule must be reachable from it without duplicating guidance. |
| Repeat adoption | A next-day repeat pass must leave project bytes identical and retain the original `Adopted: 2026-10-01` date. |
| Audit-only | Every project file must stay byte-identical, with findings reported in the final message rather than written to a file. |

Four trajectories, six sessions: `claude-instructions` (adopt, repeat),
`split-instructions` (adopt, repeat), `audit-only`, and `discovery`.

## Shared fixtures, client-specific wrapper

Cases come from [instructions.py](../adoption/instructions.py),
[build.py](../adoption/build.py) and [marker.py](../adoption/marker.py), so both
clients exercise the same projects, protected content and immutable files. Three
things necessarily differ, and all three are recorded in `protocol.json`:

- **Invocation.** `/adopt-context-docs` for the routing and audit trajectories; a
  plain request that never names the skill for discovery.
- **Installation.** The skills are copied into the project's own
  `.claude/skills/`, which Claude Code reads. They are committed with the fixture
  and hash-checked after every session, so a reference to an installed file
  validates while tampering fails.
- **Audit output.** This client has no `/output`, so an audit reports in its final
  message. Grading asserts project byte-identity directly instead of requiring a
  report file.

Requests state each immutable file explicitly, following the fix the
[initial v0.1.3 review](../results/2026-09-28-adoption-v013/README.md) required.

The [September 28 handoff](../../docs/handoff-2026-09-28-claude-code.md) records
the original design proposals. The repaired harness retains project-scoped
installation, final-message audits and the explicit unnamed-selection check.
A discovery miss therefore fails that trajectory; it is not by itself a skill
content defect. This local smoke test has no container or network isolation and
must not be compared numerically with the Codex studies.

## Run it

Needs Python 3, Git and a Claude Code CLI that can authenticate. Sessions run
non-interactively with `--permission-mode acceptEdits`, `--setting-sources project`,
`--strict-mcp-config` and fixed tool permission rules, in disposable directories
only. These rules preapprove tool calls; they are not a sandbox. Prefer a temporary
directory outside this repository so ancestor project instructions cannot leak
into the synthetic fixtures.

```sh
python3 evals/claude-code/smoke.py selftest
python3 -m unittest discover -s evals/claude-code -p 'test_*.py'
python3 evals/claude-code/smoke.py build /tmp/context-docs-claude-smoke --model claude-opus-5
# Copy protocol.json to the evaluation results directory and commit before running.
python3 evals/claude-code/smoke.py run /tmp/context-docs-claude-smoke
python3 evals/claude-code/smoke.py report /tmp/context-docs-claude-smoke --reviews reviews.json
```

Freeze the built `protocol.json` in Git before running the sessions. Pass `--model`
at build time to select a full model ID (the example uses
[Claude Opus 5](https://platform.claude.com/docs/en/models/opus-5/overview)). The CLI
version, requested model, tool permission rules, timeout and grading inputs are
recorded. `run` consumes the frozen requests and criteria, rejects conflicting
model overrides and checks the initial project hashes before any session. Old
protocols without frozen inputs require a new build. The model reported in the
client's initialization event is retained separately when available.

Use a new destination for each run: existing trials or logs are never overwritten.
Results are saved after each session; authentication failures, missing terminal
results and nonzero CLI exits stop the remaining sessions. A completed response
with denied commands keeps its failing execution check but no longer prevents
coverage of later sessions. Each session has a ten-minute timeout.
The subprocess receives empty standard input so parent launch scripts cannot be
appended to requests. For targeted follow-ups, repeat `--trajectory <id>` at build
time; freeze that selection before execution. Read-only hash/inspection commands
are preapproved (the exact rules are frozen in each protocol), but other commands
can still be denied and must remain recorded as failures.

`selftest` needs no credentials and no network. It checks stream parsing on
recorded positive, negative and error streams, that each fixture materializes with
its uncommitted material actually uncommitted, and that the grader accepts the
reference output while rejecting an unrequested edit to an immutable file, a broken
project link, a missing installed file and a tampered installed skill. Additional
unit tests exercise protocol/model drift, changed initial inputs, whole-tree byte
identity (including `.claude/` and newline changes), absolute and relative
installed references, incomplete streams, textual permission events and retained
execution failures. The shared verifier also accepts directory links containing
known sources, while rejecting unknown directories and directory anchors. Installed
absolute links are validated for this machine; that does not establish portability.

## Review

`report` aggregates mechanical checks and invocation evidence. Semantic criteria
must be supplied in a `reviews.json` of the form
`{"sessions": {"<trajectory>-pass-<n>": {"criteria": [true, ...], "evidence": "..."}}}`,
with one boolean per rubric item and a specific explanation. Mechanical rewards are
not correctness, and invocation is not comprehension: a session can invoke the skill
and still place the rule wrongly.

New protocols also score factual claims in documents and final responses, including
the scope of version, publication and automatic-loading evidence. Discovery must
provide README/index navigation. These criteria strengthen the review after the
retained failures; they do not retroactively change earlier scores or requests.

Record the CLI version, model, session count, every failure and the review method.
Author-created fixtures with author review are not independent validation, and one
client with one model establishes nothing about others.
