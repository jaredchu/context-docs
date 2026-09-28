# Handoff: native Claude Code smoke test — September 28, 2026

Author: Claude Opus 5, in the Claude Code desktop app. Addressed to Codex
(gpt-6-astra) as the collaborator continuing this branch. Kept in the repository
so the request, the decisions and their reasons stay with the work.
Branch: `claude/claude-support-and-static-checks`, head `6f1a9ac`, pushed.
Owner delegated contribution authority (commits and branch pushes) on 2026-09-28.

**Summary: the harness you asked for is complete, statically validated and in CI.
Its six model sessions did not run, because the Claude Code CLI in this environment
cannot authenticate. Nothing about native Claude Code behavior is established yet.
Six decisions are listed at the end; three of them change the fixtures, so please
settle them before the sessions are frozen and run.**

## 1. Branch state

| Commit | Author | Change |
| --- | --- | --- |
| `8f30089` | Claude | Static repository checks, CI workflow, per-skill `VERSION`, `CHANGELOG.md` |
| `894dcec` | Claude | Adoption v0.1.3: route the rule to the loaded instruction file; two routing cases |
| `0e88914` | Claude | Proposed discrimination protocol; project-context maintenance |
| `6597389` | Codex | Package/version validation fixes, 12 static-checker tests, Claude loading wording |
| `17e8dd7` | Codex | v0.1.3 evaluation, 8/9 sessions, split-file failure retained |
| `84a2cab` | Codex | Explicit file constraints, hash-validated installed references, 4/4 follow-up |
| `6f1a9ac` | Claude | Native Claude Code smoke test harness, not executed |

Installable skills on this branch: core `context-docs` 0.1.1, `adopt-context-docs`
0.1.3. Neither changed in `6f1a9ac`.

## 2. On your v0.1.3 review

Accepted without reservation. Both findings were defects in the fixture and
verifier I contributed, not in the skill:

- `knowledge/state.md` was marked immutable without the request saying so. Your fix
  — generating the constraint sentence into every request — is now the convention
  the Claude Code harness follows too.
- The project-only grader rejected a real installed-skill link, while the same path
  in a code span escaped the check entirely. Your `external_references` /
  `external_reference_roots` mechanism in [verify.py](../evals/suite/verify.py) is
  what the new harness uses to validate installed-file references by SHA-256.

The [initial 8/9 result](../evals/results/2026-09-28-adoption-v013/README.md) and its
retained failure should stay as dated evidence. The
[follow-up's 4/4](../evals/results/2026-09-28-adoption-v013-followup/README.md)
supersedes the recommendation, not the scores.

One portability concern from that review remains open and is not addressed here:
absolute installed paths such as `/opt/context-docs/...` do not survive a move to
another machine or client. The Claude Code harness sidesteps it by installing into
the project's own `.claude/skills/`, which is relative — but that is a property of
this harness, not a fix in the skill. See decision 1.

## 3. What `6f1a9ac` adds

[`evals/claude-code/smoke.py`](../evals/claude-code/smoke.py) plus its
[README](../evals/claude-code/README.md). Four trajectories,
six sessions, mapped to the four checks you requested:

| Requested check | Trajectory | How it is checked |
| --- | --- | --- |
| Skill discovery and `/adopt-context-docs` invocation | all four | `Skill` tool calls and reads under `.claude/skills`, parsed from the session's own `stream-json` output. `discovery` never names the skill, so selection must come from the description; the other three invoke `/adopt-context-docs`. |
| Rule placement, Claude-only project | `claude-instructions` | `CLAUDE.md` is the loaded file; rule and marker must land there, with no unloaded `AGENTS.md` holding the only copy. |
| Rule placement, mixed instructions | `split-instructions` | Both files present, only `CLAUDE.md` loaded; the rule must be reachable from it without duplicated guidance. |
| Repeat preserves files and dates | both routing trajectories, pass 2 | Project bytes identical to the previous output, and `Adopted: 2026-10-01` retained on a 2026-10-02 run. |
| Audit-only leaves files unchanged | `audit-only` | Whole-tree byte identity; findings reported in the final message. |

### Shared fixtures

Cases are imported, unmodified, from [instructions.py](../evals/adoption/instructions.py)
(both routing cases), [marker.py](../evals/adoption/marker.py) (`audit-only`) and
[build.py](../evals/adoption/build.py) (`adopt-empty-docs`, used for discovery). Both clients therefore exercise the same
projects, protected tokens, immutable files and rubric text. Immutable files are
stated explicitly in every generated request, per your fix.

### Necessary client deviations

All three are recorded in the generated `protocol.json`:

1. **Invocation.** A slash command, or an unnamed request for discovery. There is no
   `$skill` syntax on this client.
2. **Installation.** Skills are copied into the project's `.claude/skills/`, which
   Claude Code reads, committed with the fixture and SHA-256 checked after every
   session. Grading runs with the project as the working directory so the same
   relative path resolves for both the grader and a Markdown link.
3. **Audit destination.** This client has no `/output`, so the audit reports in its
   final message and grading asserts project byte identity directly instead of
   requiring a report file.

### Grading

The shared `grade()` runs over the complete working tree, including
`.claude/skills`, so a stray file there cannot hide. A narrower project-only view
(excluding `.claude/`) is what the report diffs and what the unchanged-project and
date checks use. Added per-session checks beyond `grade()`:
`installed_skill_unchanged`, `project_byte_identical` (where a no-op is required),
`original_date_retained`, `skill_selected_unnamed`, `no_execution_error`.

Semantics are not inferred. `report` requires a `reviews.json` of the form
`{"sessions": {"<trajectory>-pass-<n>": {"criteria": [bool, ...], "evidence": "..."}}}`,
one boolean per rubric item with a specific explanation, and says so when review is
incomplete.

### Isolation

`--permission-mode acceptEdits`, `--setting-sources project` (user settings are not
loaded), `--strict-mcp-config` with no MCP config, and a fixed tool allowlist:
`Read Write Edit Glob Grep Skill TodoWrite` plus read-only
`Bash(git status|git diff|git log|ls|cat)`. `CLAUDE_CODE_*` variables from the host
session are stripped from the child environment. `~/.claude/CLAUDE.md` and
`~/AGENTS.md` are absent on this machine and their absence is recorded in the
protocol. This is weaker than your container: no network isolation and no pinned
image. See decision 4.

### Validation actually performed

`python3 evals/claude-code/smoke.py selftest` — 34 assertions, credential-free, now
a CI step. It covers stream parsing on recorded positive, negative and error
streams; fixture materialization including that uncommitted material really is
uncommitted; and grader controls that accept the reference output while rejecting an
unrequested edit to an immutable file, a broken project link, a missing installed
file and a tampered installed skill.

I also ran the full pipeline once as a dry run and confirmed it records six
execution errors rather than silently passing, then discarded that output.

Two bugs were found and fixed during that validation, both mine:

- The grader resolved declared installed-file references against the repository
  working directory rather than the project, so every `external_reference` check
  failed. Grading now runs with the project as the working directory.
- The fixture builder wrote uncommitted material before the initial commit, so the
  `claude-instructions` dirty-tree case was committed clean. It now commits tracked
  files first, then writes uncommitted material, and asserts the tree is dirty.

## 4. Why no session ran, and how to run them

The nested CLI fails immediately:

```text
Failed to authenticate: OAuth session expired and could not be refreshed
```

The desktop app refreshes tokens for its own session; a `claude -p` subprocess
cannot. CLI version here is `2.1.234`. Unblock by refreshing the login in an
interactive terminal, or by exporting `ANTHROPIC_API_KEY`, then:

```sh
python3 evals/claude-code/smoke.py selftest
python3 evals/claude-code/smoke.py build .local/claude-code-smoke
# freeze .local/claude-code-smoke/protocol.json in Git before running
python3 evals/claude-code/smoke.py run .local/claude-code-smoke
python3 evals/claude-code/smoke.py report .local/claude-code-smoke --reviews reviews.json
```

`run` refuses to overwrite an existing `trials.json`; `build` refuses an existing
destination. Every session is retained, failures included. Published results would
go under `evals/results/2026-09-28-claude-code/`.

## 5. Decisions requested

1. **Installed-skill location.** The harness installs into the project's
   `.claude/skills/`, which makes references relative and portable but puts the
   package inside the graded tree. The alternative is a temporary
   `CLAUDE_CONFIG_DIR` for a personal-scope install, which keeps the project clean
   but may interfere with CLI authentication and makes installed references absolute
   again. *Recommendation: keep the project-scoped install; it is the configuration a
   Claude Code user is most likely to have, and the hash check covers tampering.*
2. **Audit report destination.** Final message, or a file written outside the
   project. *Recommendation: final message. Writing outside the project needs extra
   permission on this client and tests the harness rather than the skill.*
3. **Does unnamed selection gate acceptance?** `skill_selected_unnamed` is currently
   a scored check on the `discovery` trajectory. It measures client routing, not
   skill behavior, and a miss would not be a v0.1.3 defect.
   *Recommendation: record it, report it prominently, but exclude it from the
   trajectory's accept/reject decision.*
4. **Is this isolation sufficient?** No container, no network isolation, no pinned
   image; settings and MCP are excluded and tools are allowlisted.
   *Recommendation: accept for a smoke test, state the difference explicitly in the
   results, and do not compare its numbers against container-run Codex trials.*
5. **Model to freeze.** `--model` is supported and recorded; unset means the client
   default. *Recommendation: pin one model by name so the result is reproducible,
   and state that a single model establishes nothing about others.*
6. **AGENTS.md reading depends on CLI version.** Direct `AGENTS.md` reading requires
   v2.1.277 or later; this machine has 2.1.234. The fixtures state which file is
   loaded in the request rather than relying on client detection, so they are valid
   either way, but the `split-instructions` interpretation ("this client loads
   CLAUDE.md only") is only literally true on some versions.
   *Recommendation: record the CLI version in the results and keep the request
   wording, since the skill must handle a stated constraint regardless.*

## 6. Verified by execution on this branch

| Check | Result |
| --- | --- |
| `evals/checks/static_checks.py` | 291 links, 5 tables, 2 packages, 2 versions — pass |
| `evals/checks/test_static_checks.py` | 12 tests pass |
| `evals/suite/selftest.py` | 46 assertions pass |
| `evals/suite/test_verify.py` | 9 tests pass |
| `evals/quality/study.py selftest` | 66 assertions pass |
| `evals/claude-code/smoke.py selftest` | 34 assertions pass |
| `evals/adoption/build.py` | 8 grader controls pass |
| `evals/adoption/marker.py` | 12 grader controls pass |
| `evals/adoption/instructions.py` | 10 grader controls pass |
| Published report regeneration | quality, history and routing tables reproduce byte-identically |
| CI | 8 steps, all of the above, on every push |

All static. None of it is a model evaluation.

## 7. What is not established

- Native Claude Code behavior: no session has run. The harness currently records
  six authentication failures.
- Automatic skill selection on any client.
- Cross-machine portability of absolute installed-skill paths.
- Any accuracy, reliability or advantage claim. Six single-attempt sessions on one
  client, with author-created fixtures and author review, would be a smoke test with
  no comparison arm and no reader phase.
- The proposed [discrimination protocol](../evals/discrimination-protocol.md) is
  unapproved by the owner and unexecuted; it changes no published study.

## 8. Reference

Added in `6f1a9ac`: the harness and its README. This report is added separately.
Modified: `.github/workflows/checks.yml` (new selftest step), `evals/README.md`,
`evals/adoption/README.md` (cross-references), `docs/project-context.md` (current
state and next actions 6).
