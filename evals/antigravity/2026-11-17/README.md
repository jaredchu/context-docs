# Antigravity CLI compatibility observation — November 17, 2026

**Provisional setup guidance, not a validated end-to-end adoption workflow.**
The constrained CLI trial recognized project skills and completed some tasks.
Initial adoption, changed-note refresh and audit did not complete. These failures
are observations under the stated permissions, not general Antigravity
incompatibility findings. App and IDE were not separately tested.

Evidence ID: `antigravity-compat-2026-11-17`. Evaluation preparation, inspection
and scoring: Codex (GPT-6 Astra). This is author-scored synthetic evidence;
independent review of the documentation patch is a separate activity.

## Conditions and frozen method

- Client: `agy 1.5.7`, print mode, existing authenticated account; account tier
  unknown. Parent model explicitly requested `gemini-3.8-flash-medium` throughout.
- Packages: unchanged core **0.2.7**, adoption **0.1.16**, copied in full into each
  fixture's `.agents/skills/`. See [package hashes](skills-manifest.json).
- Seven fresh processes, one model attempt per case, 180 seconds per case and
  1,260 seconds aggregate. Actual parent-process wall time including failed setup:
  **630.372 seconds**. No timeout, model retry or quota/payment barrier occurred.
- Prompts, fictional facts, answer key, rubric, settings, bases and budgets were
  frozen before inference. The first settings form used `agentMode: "default"`;
  three startup invocations rejected that value before inference, produced empty
  traces and changed no fixture files. A separately frozen amendment removed that
  key. Both original hashes and the rejected invocations remain in
  [provenance](provenance.json); the [portable executable protocol](protocol.json)
  is a sanitized derivative, not the original byte stream.
- Session-only settings used `useG1Credits: false`, an empty `modelProvider`, and
  `toolPermission: "request-review"`. Every emitted startup confirmed
  `request-review`. Credit fallback was disabled; no API key or paid fallback
  was used. Native `/usage` reported Gemini weekly quota **100% before, 72% after**.
  That establishes reported remaining quota, not a Free tier or billing audit.

The invocation shape was:

```text
agy --settings <session-settings-json> --model gemini-3.8-flash-medium \
  --output-format stream-json --print-timeout 180s -p <frozen-prompt>
```

The permission settings explicitly allowed fixture `read_file` and `write_file`,
denied `command(*)`, `mcp(*)`, `read_url(*)` and `execute_url(*)`, and protected
`.git`, copied skills and external private inputs. No permission bypass or global
configuration edit was used. This was existing-account coexistence, not a clean
home or OS sandbox. Runtime conversations and logs were created outside fixtures.

## Cases and results

S1 used the unadopted [B0 fixture](fixtures/B0.json). Because it did not adopt,
S2, S3 and S7 used the independently frozen [C0 control](fixtures/C0.json),
with no adoption credit. S4/S5 used S3 output; S6 always used C0. These are separate
branches, so S2's new access-granted note was not present in S3–S5.

| Case | Behavioral outcome | Preservation and loading |
| --- | --- | --- |
| S1 explicit `/adopt-context-docs` | **Incomplete/fail:** returned “Wait for subagent response.”; no adoption rule or marker added. | No fixture changes. Native skill expansion observed; core direct read observed; adoption direct read absent. |
| S2 unnamed refresh | **Incomplete/fail:** returned a wait message without incorporating the new access-granted standup note. | No changes from C0 plus the harness-added note. Core direct read observed. |
| S3 ordinary station-filter implementation | **Pass on C0:** implemented `--station`, added tests and updated current state, progress and next action without a skill/doc request. | Only source, tests and context changed. Approved decision/rationale, pending proposal, blocker and unresolved timezone conflict preserved. Core direct read observed. |
| S4 fresh resume | **Pass:** correctly recovered SQLite and rationale, unapproved Parquet, CDX-4471 blocker, next action and UTC/local conflict. | All fixture and Git metadata bytes identical. No skill read; this was directed file reading. |
| S5 read-only audit | **Incomplete/fail:** final answer only said it was waiting; no concrete audit finding delivered. | All fixture and Git metadata bytes identical, so read-only preservation passes. Core direct read observed. |
| S6 repeat adoption | **Pass for no-change behavior:** preserved original `2026-10-01` marker, maintenance rule and progress view without duplication. | All bytes identical. Native skill expansion and core direct read observed; adoption direct read absent. Its automatic-instruction-loading claim is unverified. |
| S7 typo control | **Pass:** only `recieve` → `receive` in the source comment. | Docs, configuration and skills unchanged; no skill read. |

The external harness separately ran `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src
python3 -m unittest discover -s tests -v` on S3: **3 tests passed**. The subject's
own test commands were denied. External success is not subject-run validation.
See the [implementation patch](S3-changes.diff), [typo patch](S7-changes.diff),
[structured results](results.json) and per-case extracts:
[S1](S1-trace-extract.json), [S2](S2-trace-extract.json),
[S3](S3-trace-extract.json), [S4](S4-trace-extract.json),
[S5](S5-trace-extract.json), [S6](S6-trace-extract.json),
[S7](S7-trace-extract.json).

## What the traces establish

The startup `expanded_commands` field explicitly identifies the adoption skill
in S1/S6. This is observed native expansion, rather than inferred slash injection.
It does **not** satisfy the frozen requirement for a completed direct tool read
of the adoption `SKILL.md`. That criterion remains unmet in both cases. Completed
`read_file` calls establish core skill reads from project `.agents/skills/` in
S1/S2/S3/S5/S6. No global skill location was exercised.

The advertised tools included `list_dir`, `find_by_name`, `grep_search`,
`view_file` and edit tools. The trace uses `read_file` and `edit_file` aliases;
reads succeeded and S3/S7 edits succeeded. The failed cases chose shell-based
listing and native research children. Shell listing/tests and an attempted
`run_workflow` test script were denied. The available native listing tools were
not observed being used, so these failures do not establish that fixture access
was impossible. We did not widen permissions or retry a failed model case.

The subject itself spawned research children in S1, S2 and S5. Their retained
transcripts record `gemini-3.8-flash-tiered` in S1 and
`gemini-3.8-flash-medium` in S2/S5. Thus the explicit parent-model setting did not
establish fixed-model-only execution; S1 child routing is a protocol limitation.
Child command denials are retained. No child was separately launched by the
evaluator. Native instruction injection is not independently exposed by these
extracts. S6's claim of verified automatic AGENTS.md loading therefore remains
unverified, despite correct no-change behavior.

## Preservation, provenance and limits

Hashes show no changes to the selected existing installed skill trees or settings,
repository skill packages, copied fixture skills, configuration or data. Git
metadata bytes stayed identical in every case; disposable fixtures had an unborn
HEAD and no index before and after. S1/S2/S4/S5/S6 changed no fixture bytes;
S3/S7 changed only the files listed above. The [fixture manifests](fixture-manifests.json)
include complete copied-skill hashes; public fixture JSON maps store relative paths and exact text, omitting those
packages and `.git`. Their missing runbook link is an intentional audit defect. Copy the unchanged packages from bundle v0.2.7 to reconstruct placement.

[Provenance](provenance.json) binds raw protocol, trace and child-transcript hashes
through the [results](results.json). Extracts retain completed/error tool steps,
final responses and child-model/error summaries. Private paths and runtime IDs
are removed or replaced. Raw traces remain private; hashes identify them but do
not let a public reader independently inspect inaccessible originals. The
[answer key](answer-key.json) stayed outside subject workspaces. Extracts and
fixtures are synthetic; this is not a private-project performance test.

One observation per case does not establish repeatability, general implicit
selection, automatic rule loading, fresh network installation, global/duplicate
precedence, interactive behavior, App/IDE behavior or comparative benefit.
Published package versions and original Cursor trials are unchanged.

Current vendor references, checked November 17, 2026: [skills](https://antigravity.google/docs/skills),
[rules](https://antigravity.google/docs/rules),
[headless mode](https://antigravity.google/docs/cli/headless/),
[settings](https://antigravity.google/docs/settings?tab=cli),
[permissions](https://antigravity.google/docs/permissions?tab=cli) and
[credits](https://antigravity.google/docs/cli/credits/). Documented capabilities
are separate from the observations above.
