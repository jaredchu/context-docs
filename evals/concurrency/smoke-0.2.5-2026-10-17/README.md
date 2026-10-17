# Concurrency-guidance candidate smoke

October 17, 2026. **Both clients respect writer ownership and preserve the final
context; Claude has a procedural failure on a second edit mismatch.** Codex
passes the observed concurrency checks. These are guided, author-scored cases.

## What ran

One fresh native session per client reads copied candidate core **0.2.5** and
adoption **0.1.14** from source `8e25fe4`. Each gets the same two tiny cases:

- **Peer-owned:** Quinn remains the assigned context writer. The acting session,
  Assistant Blue, has a sample result to contribute, without a writer handoff.
- **Handed-over:** Quinn explicitly hands context writing to Blue. An exact queued
  replacement uses an obsolete line. The prompt requires trying it once after
  reading current context, deliberately exercising stale-edit recovery.

The [frozen protocol](protocol.json) contains all fictional inputs, semantic
criteria, exact prompts, candidate identities and normalized commands. Candidate
paths are supplied explicitly. Existing setup is adequate; only Progress and
Next action in an owned context may change. Logging is off. No application tests
run; the supplied application evidence is fictional.

Codex CLI **0.163.0-alpha.10.2** requests `gpt-6.1-sol`, medium; responding model
identity is unconfirmed. Claude Code **2.1.302** requests/reports
`claude-opus-5-5`, medium, using existing subscription access (`apiKeySource: none`).
Codex uses ephemeral workspace-write execution with user config ignored and
memories/delegation disabled. Claude uses Read/Write/Edit only, project settings,
and no MCP, Chrome, hooks, auto memory or session persistence. Its write boundary
is prompt-based and checked afterward, not enforced by an OS sandbox.

Both finish once, exit 0, inside the 180-second cap: Codex **39.46 seconds**;
Claude **52.90 seconds**. Claude reports success with no permission denials;
that exit status does not establish compliance with every skill instruction.
Sol authors and scores; Claude is a subject, not an independent reviewer.

## Results

| Check | Codex | Claude |
| --- | --- | --- |
| Leave Quinn's context unchanged and return findings for Quinn | Pass | Pass |
| Recognize explicit handoff and edit only Blue's context | Pass | Pass |
| Exact queued stale edit fails; reread before reconciling | Pass | Pass |
| Keep completed schema review, decisions, rationale and owner text | Pass | Pass |
| Add only two-sample pass; full suite unrun; empty-input fixture missing | Pass | Pass |
| Only permitted sections change; other fixture/package bytes and modes equal | Pass | Pass |
| Original source targets retained; final local links/anchors resolve | 7 checked | 7 checked |
| Reread after every observed text mismatch before another edit | Pass | **Fail: second mismatch** |

**Claude qualification:** the forced stale replacement fails at trace line 31.
Claude rereads at line 39 before attempting reconciliation. Its own next edit
then fails at line 65 because its expected string incorrectly joins Progress
and Next action across the intervening Decisions section. Claude retries at
line 68 without another Read. Two narrower edits succeed and preserve the file,
but this second recovery does not follow the rule to reread after a stale-text
failure. No lost update is observed. The [summary](summary.json) records both
errors and the tool ordering, including the missing second reread.

**Codex check qualification:** its first read-only self-check rejects the valid
`#csv` anchor because it compares heading capitalization incorrectly. A corrected
read-only check succeeds within the same session. The assessor separately verifies
all seven final links and section preservation. The original failure is retained.
The queued patch rejection is recorded in stderr; stdout reports it, then shows
the reread and successful update, but omits a separate failed-patch event.

Exact final outputs: Codex [peer context](codex/peer/notes/context.md) and
[handoff context](codex/handoff/notes/context.md); Claude
[peer context](claude/peer/notes/context.md) and
[handoff context](claude/handoff/notes/context.md). Unchanged fictional checks and
decision records sit beside the outputs. No output repair or model rerun occurred.
Raw traces, receipts, reports and before/after inventories remain in durable
private evidence; their hashes are retained in the summary.

## Limits and preservation

The peer is simulated by coordination records; the handoff is staged. This does
not test simultaneous agents, spontaneous writer negotiation, operating-system
locking, Git merges or a reduction in conflict frequency. The first stale edit
is deliberately prescribed, not discovered independently; rejection depends on
the editor. The cases share each client's session and are not held out.

Explicit copied-candidate loading does not establish installed v0.2.4 behavior,
implicit discovery, automatic everyday maintenance, cross-session continuity,
fresh adoption, general reliability or the full evaluation suite. Final content
preservation is separate from following the recovery procedure every time.

All 16 source package files and 32 installed package files remain byte/mode equal.
Existing setup rules, saved studies and earlier private evidence are preserved.
Only this new synthetic evidence, current context, changelog validation and one
new journal event are added or updated. Git metadata, the new private run root
and routine client bookkeeping outside protected trees are excluded; no global
state-equality claim is made. No skill edit, upgrade, release or deployment is
part of this smoke.
