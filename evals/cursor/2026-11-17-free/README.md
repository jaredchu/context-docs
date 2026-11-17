# Cursor CLI on Free: bounded compatibility observation (2026-11-17)

Evidence ID `cursor-free-compat-2026-11-17`. **Experimental CLI observation, one
attempt per case. Not evidence of general Cursor support.**

On one existing macOS arm64 Cursor Free account, the Cursor CLI ran seven fresh
non-interactive Context Docs sessions with **Grok 4.7 256K Medium**. It used the unchanged
published skills (core **0.2.7**, adoption **0.1.16**). Each session ran once,
with no retries. All seven exited successfully within their bounds, with no quota,
payment or entitlement error. One earlier attempt with a different model failed and is retained below.
Two of the seven sessions **do not meet the frozen skill-loading criterion**.
These are qualified observations, not seven unqualified passes.

[Machine-readable summary](summary.json) · [Portable extract](#portable-extract)
· [Installation guidance](../../../docs/getting-started.md#cursor-cli-experimental)

## Setup

- Client: Cursor CLI (`cursor-agent`), print mode (`-p`), `--output-format stream-json`,
  `--model grok-4.7-medium`, one new process per case. No `--force`, `--yolo`, resume
  or MCP approval was used. S4 used `--mode ask`.
- Builds: the CLI updated itself during S1. S1 ran on `2026.11.11-b912975`;
  S2–S7 ran on `2026.11.13-eacade1`. **This is a mixed-build set.**
- Skills: byte-identical copies of core 0.2.7 and adoption 0.1.16 were already
  installed in both `~/.claude/skills` and `~/.agents/skills`. This tests coexistence
  with existing installations, **not a clean or fresh install**.
- Fixture: Tidewatch, a fictional tide-gauge CLI. It has a seeded approved decision,
  a pending proposal, an external blocker, an unresolved configuration conflict,
  a broken runbook link and a typo. Cases, prompts, rubric and answer key were
  frozen before inference.
- Permissions: each workspace had a project CLI permission file. It denied shell,
  MCP and web fetch, and denied writes outside the workspace. Reads were allowed
  only in the workspace and the two skill packages. These are client permission
  settings, not OS isolation.
- Bounds: 180 s per case and 1260 s aggregate subject time. The CLI exposes no
  enforceable turn cap.

## Results

| Case | Prompt (abridged) | Build | Time | Skill files read (root) | Observed result |
| --- | --- | --- | ---: | --- | --- |
| S1 explicit adoption | `/adopt-context-docs Adopt Context Docs in this project.` | .11 | 132.7 s | core `SKILL.md`, standard, progress, template (`~/.claude`) | Added one maintenance rule and a dated marker to `AGENTS.md`, plus a progress view. Facts and decision status preserved. **Adoption `SKILL.md` read not observed.** |
| S2 unnamed refresh | Refresh context from a new standup note | .13 | 80.8 s | core `SKILL.md`, standard, progress | Core read as first tool call without naming the skill. Blocker updated from the note; pending proposal and conflict preserved. |
| S3 ordinary implementation | Add a `--station` option and unit test | .13 | 114.4 s | core `SKILL.md`, progress | Option and test added. Context updated without being asked. Protected config untouched. |
| S4 fresh resume (`--mode ask`) | Report decision, rationale, proposal, blocker, next action, conflict | .13 | 34.7 s | core `SKILL.md` | All answer-key items correct; no invented completion. No file, index or HEAD change. |
| S5 read-only audit | Audit context against sources | .13 | 132.6 s | core `SKILL.md`, standard | Located gaps, including the seeded missing runbook. No file, index or HEAD change. **Accuracy only partly checked.** |
| S6 repeat adoption | `/adopt-context-docs …` on a pre-adopted control | .13 | 73.2 s | core `SKILL.md`, standard, progress, template | No edits, no duplicate rule, original adoption date kept. **Adoption `SKILL.md` read not observed.** |
| S7 typo control | Fix one typo | .13 | 14.2 s | none | One comment line fixed; no skill read; documentation unchanged. |

Continuation subject time was **582.66 s**. With the failed attempt, the total
is **588.41 s**.

### Loading: observed versus inferred

- **Observed:** completed reads of the core `SKILL.md` in S1–S6, always from
  `~/.claude/skills`, never from the identical `~/.agents/skills` copy. Why Cursor
  chose that root is unknown.
- **Implicit core use:** S2, S3, S4 and S5 read the core skill although the prompt
  did not name it. The trace cannot show whether the project's `AGENTS.md` rule
  or the skill catalog prompted this. Stream output omits the system prompt.
- **Adoption skill (S1, S6):** no tool call read `adopt-context-docs/SKILL.md`, so
  **the frozen direct-read loading criterion is not met**. Behavior suggests that
  the slash command injected its content: S1's first action is the core read that
  the adoption skill requires, and S1 wrote rule wording found only in that skill.
  This is inference. The source root of the injected copy is unknown.
- **Instruction files:** S1 and S6 state that `AGENTS.md` loads as a workspace
  rule. Those are model claims. They agree with Cursor's
  [CLI documentation](https://cursor.com/docs/cli/using#rules) but were not
  independently verified here.

### Tests and permissions

- Cursor attempted shell five times: once in S1 (`python -m unittest`) and four
  times in S3 (test runs and `pwd`). All were `permissionDenied`, so
  **Cursor did not run its own tests**. A separate harness run of the S3 tests
  passed 2/2 ([output](extract/S3-unittest.txt)).
- No session tried to read or write outside its workspace or the skill packages,
  so the outside-path denies were **configured but not exercised**. No OS sandbox
  claim is made.

### Retained failed attempt

An earlier S1 attempt requested `composer-2.5`. The model appeared in the CLI's
model list, but the server rejected it before any tool call:

> ActionRequiredError: Model unavailable on Free Free includes Grok 4.7, Grok 4.6,
> and Auto with fixed settings. Switch to an included model to continue.

It ran for 5.75 s, made no tool calls and changed no fixture files. **A listed
model is not necessarily available on a plan.** The Grok continuation was
separately frozen. It reused the same cases, prompts, rubric and answer key.

## Client side effects

- The first `--model` invocation saved that model as the CLI's global default.
  The exact original model settings were later restored. The continuation used a
  task-local `CURSOR_CONFIG_DIR`, and the main CLI config stayed byte-identical
  across all seven cases.
- A separate config directory **does not isolate all state**. Trust markers,
  transcripts and project runtime entries, vendor skill sync and the automatic CLI
  update still affected the user profile. An earlier change to a runtime privacy
  cache value also remains.
- Print mode is not read-only. Cursor documents that it
  [edits workspace files and runs allowed commands](https://cursor.com/docs/cli/using#non-interactive-mode)
  without asking.

## Not established

- Tool-observed loading of `adopt-context-docs`, or which root supplied it
- Native `AGENTS.md`/`CLAUDE.md` instruction loading
- Fresh installation, `.cursor/skills` or `.agents/skills` placement on its own,
  root precedence or duplicate handling
- Interactive CLI sessions, the Cursor desktop editor, cloud agents, other models
  or builds
- Reliability beyond one attempt per case
- How much of the Free allowance remains, or any general quota guarantee. Free was
  sufficient for this run only.
- Full audit accuracy. S5's seeded runbook finding and selected others were
  spot-checked. Its first finding concerns ambiguous S1-written progress wording
  (per-station versus combined output); this record does not adjudicate it.

## Roles and review

Cursor with Grok 4.7 256K Medium was the only subject. Claude Opus 5.5 ran the
harness and wrote the private report as the single writer. Codex coordinated and
checked the evidence. An independent Astra review of the saved test sources
passed with no material findings. That review verified the receipts, traces,
snapshots and restoration records without rerunning any session. It made one
non-material wording suggestion about distinguishing public plan documentation
from observed account entitlement. The review covered saved evidence only. It
does not establish general Cursor support, clean installation, hidden instruction
loading or OS isolation.

## Portable extract

The extract is derived from the private originals and is **not a complete log or
an independent reproduction**.

- [`extract/tool-calls.jsonl`](extract/tool-calls.jsonl): every completed tool call
  per case, with tool, status and normalized target.
- [`extract/final-responses.jsonl`](extract/final-responses.jsonl): each session's
  final chat response. It contains model claims, including the instruction-loading
  statements above.
- [`extract/fixture-diffs/`](extract/fixture-diffs/): fixture changes for S1, S2, S3
  and S7. S4–S6 produced no changes.
- [`extract/S3-unittest.txt`](extract/S3-unittest.txt): separate harness test output.

Extraction replaced absolute paths with `<WORKSPACE>` (the per-case fixture
checkout) and `<USER>` (the home directory). It omitted thinking text, session
and call IDs, timestamps, account and configuration data, permission policy
paths and helper metadata. Raw traces, snapshots, workspaces, receipts and
reports remain private. [`summary.json`](summary.json) lists the SHA-256 of each
original source file, including the final synthesis
(`d8b15716d0e2b0f590a05e77f90a1dafbe6097fc0209653e8a335f9802a0dbe1`). A hash
identifies the source but does not let readers inspect it.
