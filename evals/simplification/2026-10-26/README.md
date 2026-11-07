# Instruction deduplication candidate check

October 26, 2026. **Qualified: focused saved-file and preservation checks pass;
the adoption report's automatic-loading confirmation remains unverified.**
This checks unreleased core **0.2.7** and adoption **0.1.16**, not installed or
published packages and not human benefit.

## Scope and method

The candidate consolidates a repeated canonical-location rule, removes the
incidental ASD-STE100 wording and shortens adoption's repeated coordination and
storage/setup text. The mandatory sibling-core read, guide routes, anchors and
underlying safeguards remain. Core changes from 1,473 to 1,451 words; adoption
changes from 1,138 to 1,116. Word counts describe the edit, not an outcome benefit.

The [protocol manifest](protocol.json) was saved before model execution. It
contains exact prompts, candidate file hashes, the before inventory, fixed
semantic criteria, client version and command flags. The fixture reuses the
[refresh baseline](../../refresh/protocol.md): an approved retry decision, drifted
current context, limited check evidence and an uncommitted recovery note/YAML.
The baseline runner and all previous results are unchanged. This fixture is
author-created and previously exercised, not held out.

Three fresh ephemeral Codex CLI sessions request **gpt-6.1-sol, High**, with
existing subscription authentication, workspace-write sandbox, user config/rules
ignored, memories/delegation disabled, no API/provider overrides or fallback,
240 seconds per session and no retries. Delivered model identity and effective
effort were not independently exposed by the captured event stream. The prompt
names each copied skill explicitly; this does not test implicit selection.

## Results

| Session | File outcome | Semantic review |
| --- | --- | --- |
| Refresh | Only docs/current.md changes | Timeout 30; configured two versus approved four retries; limited local check, restore blocker, rationale and exact recovery YAML retained |
| Identical refresh request in a new session | All 23 project files unchanged | Correct state remains stable in this one case |
| Re-adopt existing setup in a new session | All 23 project files unchanged | Sibling core read; marker/date, logging off, maintenance rule and one progress view reused; loading statement qualified below |

The [saved context](current.txt) and exact final reports for
[refresh](refresh.txt), [no-change](no-change.txt) and [adoption](adopt.txt) retain
the original bytes. Relative paths inside them belong to the synthetic workspace.
The [summary](summary.json) separates hash checks and coordinator semantic/trace
review. All three sessions complete once. Git metadata hashes remain unchanged;
the candidate source package hashes remain equal. Existing installed package
hashes were compared in memory and stayed equal, but separate installed manifests
were not retained. This is not an inventory of all global/client runtime state.

The adoption report says “AGENTS.md loading is confirmed by this session.” The
trace shows the explicit file read and the session's report; it does not expose
delivered startup context independently. Retain that statement as unverified,
not as a confirmed loader defect or reliable-loading result. File preservation
does not make this a clean verification-report pass. The adoption Git inspection
also returns exit 1 for an unignored path; it is retained and not retried.

## Reproduction and limits

[runner.txt](runner.txt) preserves the exact one-off Python runner. To repeat in
a separately selected diagnostic, copy it to a new ignored directory immediately
under .local/ as run.py, then run it from this repository. It creates a new
evidence/ child, copies the then-current source skills and invokes three model
sessions; it refuses an existing output. This is a subscription-backed run, not
an offline check. The manifest hash identifies the runner used here. Raw event
streams remain in local evidence; their hashes are retained in the summary.

These are guided, coordinator-authored/scored regression observations on one
layout/client, with no baseline arm or independent grading. They do not establish
unchanged behavior everywhere, general idempotence, concurrent-write safety,
privacy, implicit selection or effort savings. At this original Codex check, no
fresh adoption, local-only, logging or Claude runtime journey ran. The separate
Claude extension below adds bounded client coverage. The Codex loading limitation is
not repaired by rerunning or redefining this attempt.

Separately, repository static checks and 24 site-build tests pass. Both optional
skill validators could not start under the current Python because PyYAML is
missing; repository package metadata/link/version checks passed instead. No
dependency was installed. This candidate remains unreleased; existing installed
skills, deferred plugin/Cursor work and prior evidence remain intact.

Codex reviewed Opus's skill edits and integrated the candidate. Opus 5.5, requested
High and confirmed by CLI model usage, separately reviewed the coordinator's
context cleanup, trial packet and result framing. Three preservation/private-record
destination findings were corrected locally; no follow-up model review ran.
Opus did not independently review its own skill implementation, rerun checks or
validate human outcomes. Review originals remain in local evidence.

## Claude extension

A separate three-session check uses the exact same candidate package bytes,
requested and reported **Claude Opus 5.5**, configured **High**, on Claude Code
**2.1.310** through the existing subscription. Effective effort is not separately
exposed. The [Claude manifest](claude-protocol.json) was frozen before execution;
the earlier Codex protocol, outputs and scores remain unchanged.

The fixture adds CLAUDE.md importing AGENTS.md and copies the skills under
.claude/skills/. The task requests an explicit package read, with slash commands
disabled, file tools only, project settings, auto memory off and no MCP/Chrome
or delegation. Existing evaluation hooks restrict reads and edits to the fixture
and its allowed Markdown destinations. Six scope controls and instruction-event
hashing passed before subjects ran. The hooks are not an OS sandbox; client
runtime bookkeeping is outside the fixture inventory.

| Session | File outcome | Loading and review |
| --- | --- | --- |
| Refresh | Only docs/current.md changes | Approved/configured retry distinction, limited check, blocker, rationale and recovery YAML retained |
| Identical refresh in a new session | All 24 project files unchanged | Correct saved state remains stable in this case |
| Re-adoption in a new session | All 24 project files unchanged | Sibling core read; setup, marker/date, logging off and one progress view reused |

All three sessions complete once, without retries or tool denials. All 28 tool
calls have matching pre/post hook records. Each session records CLAUDE.md loading
at session_start and its AGENTS.md include before the first tool call, with
hashes matching the frozen files. This supports the Claude adoption report's
loading statement for these sessions; it does not verify the earlier Codex claim
or establish model compliance, implicit skill selection or general reliability.

The [Claude context](claude-current.txt) and final reports for
[refresh](claude-refresh.txt), [repeat](claude-no-change.txt) and
[re-adoption](claude-adopt.txt) preserve the output bytes. It retains the earlier
timeout value and an absent timeout-decision note; those additions are supported
but unnecessary for the next action. No deletion quota or wording target was
scored. The [reviewed summary](claude-summary.json) separates mechanical checks,
coordinator semantic review and limits. Source packages, all 32 installed package
files and fixture Git metadata stay unchanged; installed before/after hash
manifests are retained locally.

The original runner's loading-event summary missed events because it compared
temporary path aliases lexically. Post-run inspection resolved the paths, matched
the file hashes and checked ordering against the first tool. The original
[runner](claude-runner.txt), manifest and local trial summaries are preserved;
the [post-run review](claude-review.txt) documents the correction. No subject
rerun or acceptance-rule change occurred. [Normalized hook events](claude-events.json)
retain path/decision and loading evidence with sequence order; the file documents
identifier/path normalization and omitted payloads. Raw stream and event hashes
are in the reviewed summary; originals remain local.

Codex scored and checked the outputs against source evidence; Opus was the
subject, not an independent reviewer. These reused synthetic cases add Claude
coverage only. They add no baseline comparison, fresh setup, concurrency,
local-only/logging journey, application test, independent grading or human result.
Published/installed v0.2.6 and the frozen participant r1 materials remain unchanged.
