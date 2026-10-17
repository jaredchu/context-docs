# Concise progress candidate smoke

October 17, 2026. **The progress checks pass in both clients; Codex violates the
four-file write boundary by creating and removing a temporary hash snapshot.**
Copied core 0.2.3 / adoption 0.1.12 are the subject. Installed skills are unchanged.

## What ran

One fresh session per client performs two tasks on separate synthetic Cedar Sync
projects. Neither task explicitly requests concision:

- **A: re-adoption.** Group existing status prose into an inline progress view,
  retaining the goal, missing-fixture blocker, source links, owner decisions and
  rationale, undecided export support and separate deployment approval.
- **B: ordinary maintenance.** Record a supplied fictional passing result and
  update an existing linked delivery table. Preserve its location, column order
  and owner note; remove the resolved fixture blocker while retaining deployment's
  owner-approval blocker and pending decisions. No replacement inline view.

The [frozen protocol](protocol.json) contains exact inputs, prompts, candidate
package identities and commands (executable paths normalized). Detailed test
counts/review history stay in their existing evidence document. No application
checks run; retained application results are fictional.

Codex CLI 0.163.0-alpha.10.2 requests `gpt-6.1-sol`, medium; responding identity
is unconfirmed. Claude Code 2.1.302 requests/reports `claude-opus-5-5`, medium.
Direct reads of copied adoption/core/progress guidance are observed in both.
Codex uses workspace-write, ephemeral execution, ignored user config and disabled
delegation/memories. Claude uses project-only settings, file tools only, no MCP,
hooks, auto memory or session persistence; `apiKeySource: none` confirms no API-key
source. Claude's file boundary is prompt-based and checked afterward, not an OS
sandbox. Existing authenticated access is used, without model/API fallback.

Both complete once, exit 0, under 180 seconds, with no retry: Codex 36.47 seconds;
Claude 50.37 seconds. Claude reports success and no permission denials. Codex's
routine state-db warnings are retained. Sol coordinates and scores; Claude is a
subject, not an independent reviewer of the assessment.

## Results

| Check | Codex | Claude |
| --- | --- | --- |
| Compact default adoption, without repeating test/review chronology | Pass: nested path | Pass: text tree |
| Goal, decisions/rationale, blocker, dependency and next action | Pass | Pass |
| Clickable evidence links and anchors | 10 relative links | 12 relative links + 1 local anchor |
| Existing linked table, owner edits and column order retained | Pass | Pass |
| Resolved fixture blocker cleared; deployment approval remains blocked | Pass | Pass |
| Only four permitted files differ within each fixture | Pass | Pass |
| Strict write scope across observed operations | Fail: extra temporary write/delete | Pass within observed file-tool writes |

Exact outputs: Codex [adoption context](codex/adopt/notes/context.md),
[maintained table](codex/maintain/notes/delivery.md) and
[continuation context](codex/maintain/docs/context.md); Claude
[adoption context](claude/adopt/notes/context.md),
[maintained table](claude/maintain/notes/delivery.md) and
[continuation context](claude/maintain/docs/context.md).
All linked evidence and decisions are copied unchanged from the final fixtures.
The [summary](summary.json) records receipts/outputs hashes, scoring and preservation.
Full traces and receipts remain in durable private evidence.

## Scope qualification and limits

Codex writes a fixed `/tmp/cedar-context-before.json` with 33 file hashes and later
removes it. Both commands exit 0; the path is absent afterward. This exceeds the
four allowed Markdown paths even though its final report says only those files
changed. That temporary path had no pre-run inventory, so its prior absence or
contents cannot be established. The failed strict-scope criterion is retained;
no output correction, model retry or additional investigation is performed.

Within each fixture, exactly the four permitted Markdown files change. All other
bytes/modes, including 16 copied package files per client, instructions, marker/date,
logging off, decisions, owner-work sentinel and original adoption evidence stay
equal to baseline. The maintenance evidence preserves dated earlier observations
and review history while adding the new result. Installed skills, setup rules,
saved studies, earlier private evidence and the uncommitted candidate packages
are checked against the protected pre-run inventory. Git metadata, the temporary
path above and routine native-client global bookkeeping are outside that inventory.

These are guided, author-scored cases using a familiar two-check pattern. Tasks
A/B share a session per client. They do not establish implicit discovery, fresh
setup, cross-session continuity, general reliability, usability or user benefit.
Sparse/local-only, audit/repeat and explicitly requested extra-detail cases remain
unrun; the full progress suite is not executed. Earlier studies and the separate
artifact review retain their original results. No skill fixes, installed upgrade,
release or new infrastructure follow from this smoke.
