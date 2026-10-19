# Installed v0.2.6 metadata-filtering smoke

October 19, 2026. **Both clients pass the focused saved-Markdown checks.**
Both successfully read the named synthetic private note and retain suitable
findings without copying its incidental metadata into shared context. Claude makes
five failed reads while locating the public report, then reads it successfully;
those errors remain in the original evidence.

## What ran

One fresh Codex session and one Claude Code session read installed core **0.2.6**
and adoption **0.1.15** directly at their explicit user skill paths. All 32
installed package files match the [v0.2.6 release](../../../docs/releases/v0.2.6.md)
from `d74e69d` before and after execution. The [pre-run protocol](protocol.json)
and [digest](protocol.sha256) freeze inputs, prompts, criteria, package identities
and native commands before model execution.

Two fictional tasks share each client's session: re-adopt existing contributor
context, then maintain personal offline notes. This reuses the earlier candidate
fixture, adding an explicit `public/private/session.md` pointer and unique
incidental account/path data in that incoming note. It is not held out. The
[earlier candidate's discovery gap](../../content-filtering/smoke-0.2.6-2026-10-19/README.md)
is retained; this new run does not repair its outputs or change its coverage.

Codex CLI **codex-cli 0.163.0-alpha.10.2** requests `gpt-6.1-sol`,
medium; responding model identity is unconfirmed. Claude Code
**2.1.302 (Claude Code)** requests/reports `claude-opus-5-5`,
medium, with `apiKeySource: none`. Existing subscription access is used without
API-key/provider fallback. Each has one attempt and a 180-second cap. Both exit
zero: Codex **32.64 seconds**, Claude
**65.94 seconds**. These times establish no efficiency advantage.

Codex uses ephemeral workspace-write execution with user config ignored and
memories/delegation disabled. Claude uses Read/Write/Edit only, safe mode and an
OS write sandbox limited to its new private scratch subtree and temporary directory;
hooks, MCP, Chrome, memory and session persistence are disabled. Both read installed
skill files explicitly. No implicit discovery or instruction auto-loading is established.

## Results

| Check | Codex | Claude |
| --- | --- | --- |
| Public incidental metadata and repeated bookkeeping omitted | Pass | Pass |
| Named incoming note read; unique private account/path not copied | Pass | Pass |
| Private evidence ID keeps access limit and public summary link | Pass | Pass |
| Decisions, rationale, uncertainty, blockers and next action retained | Pass | Pass |
| Useful personal path, offline/case constraints and limited result retained | Pass | Pass |
| Relative source links and anchors resolve | 11 checked | 13 checked |
| Only Progress and Next action in two context files change | Pass | Pass |
| Installed files, source evidence, rules, dates, logging off and owner text preserved | Pass | Pass |

Exact outputs and unchanged fictional sources: Codex [public context](codex/public/notes/context.md)
and [personal context](codex/personal/notes/context.md); Claude
[public context](claude/public/notes/context.md) and
[personal context](claude/personal/notes/context.md). The [summary](summary.json)
retains hashes, scope checks, normalized operations, source-read coverage and manual
semantic assessment. All supplied application results are fictional; no app tests ran.

Both keep the sample-only staging/runtime result separate from unrun full-suite
and unknown production behavior. They preserve the missing-fixture condition,
CSV compatibility rationale, proposed JSON and separate deployment approval.
Personal notes keep `/Volumes/FieldNotes/Originals`, distinct case-sensitive filenames,
one-sample thumbnail repair, unchanged originals, unrun whole-library verification
and the owner's winter-indexing action after mounting the volume.

Claude's five failed reads are public-report filename guesses and one directory
read, not an incoming-note coverage gap in this run. It eventually reads the report.
Codex rereads both edits; Claude does not reread after its edits. Sol separately
checks final artifacts and source anchors. No model retry or output repair occurs.

## Limits and preservation

These are guided, Sol-authored and Sol-scored checks, with explicit installed paths
and two tasks per session. Claude is a subject, not an independent reviewer. They
establish no general privacy guarantee, automatic everyday compliance, implicit
loading, cross-session continuity or user benefit. Logging stays off; native
journal capture is not tested. Earlier results and qualifications remain intact.

The recorded **32136 original entries** preserve bytes/modes after the native sessions:
installed packages, source skills, setup rules, saved studies, prior evidence and
the existing uncommitted upgrade record are unchanged. Authorized current-context
updates and new smoke records are separate additions. Routine native runtime/cache
bookkeeping and the new private scratch root are outside the equality claim.

Raw traces, receipts and inventories are privately retained under evidence ID
`installed-v026-filtering-smoke-58908f1f-ff4d-43bc-86d6-751ba6263d01`. That identifier and public hashes
do not grant access or establish independent verification. Exported fixtures are
fully synthetic; real operator home, credentials and evidence locations are not
included in these public records.
