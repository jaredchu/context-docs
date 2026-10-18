# Installed v0.2.5 concurrency smoke

October 18, 2026. **Both clients pass the focused installed-skill checks** for
writer ownership, explicit handoff, recovery after the forced stale edit and
final context preservation. Earlier candidate qualifications remain unchanged.

## What ran

One fresh native session per client reads installed core **0.2.5** and adoption
**0.1.14** directly. Each uses two tiny fictional cases: a context owned by Quinn
with no handoff, and a context explicitly handed to the acting session, Blue.
The second case requires one exact obsolete replacement before reconciliation.
Only Progress and Next action in an owned context may change. Existing rules,
logging off, decisions, owner notes and source evidence remain protected.

The [frozen protocol](protocol.json) contains all inputs, criteria, installed
package identities, prompts and normalized commands. Actual expanded prompts,
traces, receipts and inventories remain in durable private evidence. No copied
package exists in either fixture. Both clients directly read installed adoption,
core and progress guidance. All application results are fictional; no application
checks run.

Codex CLI **0.163.0-alpha.10.2** requests `gpt-6.1-sol`, medium; responding model
identity is unconfirmed. Claude Code **2.1.302** requests/reports
`claude-opus-5-5`, medium, using existing subscription access (`apiKeySource: none`).
Codex uses ephemeral workspace-write execution with user config ignored and
memories/delegation disabled. Claude uses Read/Write/Edit only, project settings,
and no MCP, Chrome, hooks, auto memory or session persistence. Its file boundary
is prompt-based and checked afterward, not enforced by an OS sandbox.

Both finish once, exit 0, inside the 180-second cap: Codex **36.30 seconds**;
Claude **46.57 seconds**. Claude reports success without permission denials.
Sol authors and scores; Claude is a subject, not an independent reviewer.

## Results

| Check | Codex | Claude |
| --- | --- | --- |
| Read installed adoption/core directly; no package copying or edits | Pass | Pass |
| Keep Quinn's peer-owned context unchanged and return findings for Quinn | Pass | Pass |
| Accept explicit handoff and write only Blue's context | Pass | Pass |
| Exact queued stale edit fails; reread current file before reconciliation | Pass | Pass |
| Keep completed schema review, decisions, rationale and owner text | Pass | Pass |
| Two-sample-only pass, full suite unrun and missing empty-input fixture retained | Pass | Pass |
| Only permitted sections change; other fixture bytes/modes equal | Pass | Pass |
| Source targets retained; all final context links/anchors resolve | 7 checked | 7 checked |

Each session has exactly one text-mismatch error: the deliberately queued edit.
Claude's trace shows the rejection at line 31, a fresh Read at line 34, then
successful narrow edits at lines 41 and 43. Codex's stderr records the rejected
patch; stdout reports it, then shows the reread (`item_5`) before the successful
patch (`item_6`). Failed patches are not separate stdout file-change events.
All five Codex read-only shell commands exit 0; no extra checker error is observed.
The [summary](summary.json) retains tool ordering, assessment and evidence hashes.

Exact outputs: Codex [peer context](codex/peer/notes/context.md) and
[handoff context](codex/handoff/notes/context.md); Claude
[peer context](claude/peer/notes/context.md) and
[handoff context](claude/handoff/notes/context.md). Unchanged fictional checks and
decisions sit beside each output. No output repair or model rerun occurred.

## Limits and preservation

This reuses the [earlier candidate fixture](../../concurrency/smoke-0.2.5-2026-10-17/README.md)
and semantic criteria, with explicit installed paths; it is guided, author-scored
and not held out. The inherited narrow-edit criterion mentions candidate packages;
here the installed packages named in the prompt are verified unchanged instead.
The two cases share each client's session. The peer and handoff are simulated,
and the initial stale edit is deliberately prescribed, not independently found.

No second mismatch arises in this run. It does not retest or clear Claude's earlier
failure to reread after its own second mismatch, or erase Codex's earlier corrected
read-only anchor-check error. Their original outputs and qualifications remain
unchanged. Passing final content and one recovery sequence do not establish
consistent compliance, implicit discovery, automatic everyday behavior, fresh
adoption, cross-session continuity, general reliability or conflict prevention.
No simultaneous-agent, locking or Git-merge test runs; the full suite is unrun.

All 32 installed package files and 16 source package files remain byte/mode equal.
Existing setup rules, saved studies, earlier private evidence and the uncommitted
upgrade event remain unchanged. Only new synthetic evidence, current context,
changelog validation and a new journal event are added or updated. Git metadata
and routine client bookkeeping outside protected trees are excluded; no global
state-equality claim is made. No installed update, skill edit, release or deployment
is part of this smoke.
