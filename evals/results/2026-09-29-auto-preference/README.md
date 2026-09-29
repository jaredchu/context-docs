# Optional auto preference — 2026-09-29

Core 0.1.5/adoption 0.1.6 pass the bounded auto-enablement and preservation checks
in native Claude and Codex CLI sessions using direct candidate file reads. This
is not a test of automatic skill selection or installed global preferences.

## Conditions and results

The [runner](../../event-journal/auto-preference/run.py) builds isolated synthetic
projects and freezes candidate hashes and acceptance before execution. Each setup
session receives six already-adopted projects: no Git with a custom history path,
explicit off with history, no preference, a parent Git repository, a linked
worktree and a broken Git pointer. Only the no-Git project should gain one
`Event journal: jsonl` line. All wording, original dates, paths, package files and
legacy history bytes must survive. The harness then initializes Git in that
project. A fresh session maintains it and separately audits an unconfigured
no-Git project with an auto preference; all project bytes must remain unchanged.
Git metadata is excluded from byte comparisons. Legacy JSONL is deliberately
opaque fixture data; setup must not inspect, validate or migrate it.

| Condition | Setup | Repeat after Git + read-only audit |
| --- | --- | --- |
| Initial Codex harness | Blocked before skill read; no edits | Blocked; no edits |
| Claude | Exact one-line enablement; other files unchanged | No file changes; enabled setting retained; audit did not enable |
| Corrected Codex harness | Exact one-line enablement; other files unchanged | No file changes; enabled setting retained; audit did not enable |

The original prompt incorrectly restricted Codex shell commands while assuming
file-reading tools were available. Codex reported the missing capability and
stopped. The corrected condition allows read-only shell inspection and patch
edits. Candidate bytes are identical; original failures remain separate. Six
sessions total, four functional passes, two harness-blocked sessions. Setup and
repeat created no new journal files or events and preserved legacy files.

Claude Code 2.1.234 reports `claude-sonnet-5`. Codex CLI is
0.158.0-alpha.2.1; these streams do not report its model identity. Claude runs with
an evaluation-only file/command guard; Codex uses workspace-write sandboxing.
Both read the candidate files directly, with no global installation changes.

## Qualifications and evidence

Claude attempted three shell commands denied by the evaluation guard (`find`,
`pwd`, and `ls cases/`). It completed the functional tasks using permitted tools.
During repeat/audit it also used a broad Glob that enumerated legacy journal
filenames. Thus byte preservation is not a clean no-history-access pass. Its final
claim that it did not open the journal directory omits that enumeration, and its
labeling of absent audit-only history as a gap does not establish a need to log.
The Codex setup also enumerated fixture files. These outcomes do not justify a
new general reliability, efficiency or recording-cost claim.

[Compact evidence](evidence.json) retains frozen package hashes, exact requests,
final responses, changed-file lists, instruction outcomes, normalized tool
operations and raw-stream hashes, including the failed condition. The large raw
streams and complete temporary fixtures remain local under the ignored
`.local/auto-preference-20260929` and
`.local/auto-preference-20260929-codex-followup` directories. This compact record
supports review but is not a complete public replay archive. The runner regenerates
fixtures; it cannot reproduce nondeterministic model responses.

Mechanical checks are separate: eight new policy tests cover real no-Git/root/
parent/worktree/bare cases, saved settings after Git, environment redirection and
conservative missing-Git/permission/timeout/broken-repository handling. The native
guard has one regression with eight boundary assertions. All 35 journal/policy
tests, 13 checker regressions, that guard regression, both skill metadata
validators and repository static checks passed locally. No writer or event-schema
change was made; personalized global instruction loading, absent Python, varied
platforms and unrestricted-client reliability were not exercised natively.

To run a fresh check from the repository root (uses authenticated native CLIs):

```sh
python3 evals/event-journal/auto-preference/run.py build --output .local/auto-preference-new
python3 evals/event-journal/auto-preference/run.py run --output .local/auto-preference-new --client codex
python3 evals/event-journal/auto-preference/run.py run --output .local/auto-preference-new --client claude
```
