# Unchanged v0.2.6 refresh baseline

October 26, 2026. **Both passes satisfy the focused criteria.** Existing core
maintenance handled this synthetic accumulated-drift case, and the second fresh
run made no file changes. The resulting change is a documented refresh prompt;
neither skill nor its version is changed.

## What ran

Two fresh Codex CLI **0.164.0-alpha.11.1** sessions requested `gpt-6.1-sol` with
High reasoning and an explicit local skill path. The package's complete 12-file
set, bytes and executable flags were checked against release `v0.2.6` at
`d74e69d3268676cf7eab19d241e8b590ddb1c60a` before execution. User configuration and
rules were ignored, memories and delegation disabled, and execution used the
workspace-write sandbox and existing ChatGPT subscription authentication.
API/provider environment overrides were removed; no fallback or retries were
configured. Served-model and effective-effort telemetry were not independently
exposed.

The [pre-run protocol](../protocol.md), [frozen inputs](frozen.json) and
[digest](frozen.sha256) fix criteria, prompt, source/release revisions, package
hashes, runner/protocol identities and the uncommitted-note setup. The minimal
prompt asks to refresh against current evidence, names the skill, and restricts
execution and writes; it supplies no expected values or preservation/no-change
reminder. There is no ordinary/no-skill comparison.

Both sessions exit zero and complete: pass one takes **54.38 seconds**, pass two
**29.10 seconds**. These are process observations, not an efficiency finding.
State-database lookup warnings occur on stderr in both runs; no command fails,
and the original stderr is retained locally. No model output was repaired or run
again. All application check results in the fixture are supplied fiction; no
application tests or live checks ran.

## Results

The [maintained context](project/docs/current.md) is the exact first-pass output.
The [semantic assessment](summary.json) records each criterion and its evidence;
[mechanical results](mechanical.json) retain both after-pass hash sets, and the
frozen inputs retain baseline hashes. The runner's pending-semantic-review field
is unchanged; the separate assessment records the completed coordinator review.

| Check | Result |
| --- | --- |
| Configured timeout corrected from 10 to 30 with a source | Pass |
| Four approved retries distinguished from two configured; approval/rationale retained | Pass |
| One-job local timeout result kept separate from unverified retry, restore, suite and deployed behavior | Pass |
| Restore blocker, Leena's next action, compatibility rationale and uncommitted YAML note preserved | Pass |
| Current state and progress consistent; superseded status points to current evidence | Pass |
| Existing top-level headings and eight affected links/anchors preserved | Pass |
| Only `docs/current.md` changes on pass one; all other project/package files and Git HEAD/staging preserved | Pass |
| All 19 non-Git project files exactly equal after pass two; no observed second-pass write | Pass |

Exact native reports are retained as [pass one](pass-1.txt) and [pass two](pass-2.txt).
The second pass reads the explicit skill and current sources, reports no needed
edits and has no file-change event or observed write command. Stability counts
only alongside the semantically correct first result.

Separately, [repository static checks](static-checks.json) pass relative links,
published-table agreement, both skill packages and their declared versions.
These checks do not evaluate model behavior.

## Review and limits

Claude Opus 5.5 (`claude-opus-5-5`), requested High, reviewed the evaluation design
and one focused follow-up. The initial review identified a coached prompt and
insufficient package provenance. The follow-up confirmed prompt correction and
requested comparison of the complete release file set. Codex inspected the last
file-set/executable-flag correction locally; the runner successfully executed
those checks before either model call. No further reviewer run occurred. Opus
did not score the native outcomes; Codex authored and scored this case.

This is one synthetic layout on one client with an explicit skill path and narrow
write boundary. It supports this invocation on the tested case, not a claim of
skill-specific advantage, automatic loading, general preservation/idempotence,
privacy guarantees or user-effort savings. A Claude subject was not tested. File
equality excludes `.git` internals and runtime/cache state outside the isolated
project; Git HEAD and staging were checked separately. Tool traces are not a
filesystem syscall audit.

Public project output and frozen metadata are exact copies. Raw traces, stderr
and review records remain local under evidence ID
`refresh-v026-baseline-20261026`; their hashes are in the assessment. Those hashes
do not provide access or independent verification. Installed skills, existing
project adoption rules, source package versions and earlier studies are unchanged.
