# Native Claude Code smoke test

Status: **harness complete and statically validated; no model session executed.**
Every published result so far ran on Codex with one model, and the
[v0.1.3 follow-up](../results/2026-09-28-adoption-v013-followup/README.md) records
native Claude Code behavior as unestablished. This checks the four questions raised
in that review on the other client, with the same fixtures and criteria.

This is a smoke test, not a comparison: there is no ordinary-maintenance arm, no
reader phase and one attempt per session. It can show that the skill loads and
behaves acceptably on this client, or that it does not. It cannot establish
accuracy, reliability or any advantage.

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

## Run it

Needs Python 3, Git and a Claude Code CLI that can authenticate. Sessions run
non-interactively with `--permission-mode acceptEdits`, `--setting-sources project`,
`--strict-mcp-config` and a fixed tool allowlist, in disposable directories only.

```sh
python3 evals/claude-code/smoke.py selftest
python3 evals/claude-code/smoke.py build .local/claude-code-smoke
python3 evals/claude-code/smoke.py run .local/claude-code-smoke
python3 evals/claude-code/smoke.py report .local/claude-code-smoke --reviews reviews.json
```

Freeze the built `protocol.json` in Git before running the sessions. Pass `--model`
to pin a model; the resolved CLI version, model, tool allowlist and permission mode
are all recorded. Use a new destination for each run: `run` refuses to overwrite an
existing `trials.json`, and every session is retained, including failures.

`selftest` needs no credentials and no network. It checks stream parsing on
recorded positive, negative and error streams, that each fixture materializes with
its uncommitted material actually uncommitted, and that the grader accepts the
reference output while rejecting an unrequested edit to an immutable file, a broken
project link, a missing installed file and a tampered installed skill.

## Review

`report` aggregates mechanical checks and invocation evidence. Semantic criteria
must be supplied in a `reviews.json` of the form
`{"sessions": {"<trajectory>-pass-<n>": {"criteria": [true, ...], "evidence": "..."}}}`,
with one boolean per rubric item and a specific explanation. Mechanical rewards are
not correctness, and invocation is not comprehension: a session can invoke the skill
and still place the rule wrongly.

Record the CLI version, model, session count, every failure and the review method.
Author-created fixtures with author review are not independent validation, and one
client with one model establishes nothing about others.
