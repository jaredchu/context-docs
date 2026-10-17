# Installed v0.2.2 default inline progress smoke

October 17, 2026. **Both clients create a default inline progress path during
re-adoption and maintain it during ordinary work.** Installed core 0.2.2 and
adoption 0.1.11 are used directly; no package copy or upgrade occurs.

## What ran

One synthetic Maple CLI project per client, with two fresh sessions each:

1. Re-adopt the already-adopted project without requesting visualization. The
   documented goal requires two checks; one passed and one is blocked on a missing
   fixture. Existing instructions, marker/date, owner example and logging off
   must remain unchanged. Only the context may change.
2. Record a later synthetic passing result, then follow the existing maintenance
   rule. The task does not name a skill or request progress maintenance. Only the
   results and context may change. Deployment still requires separate approval.

The [frozen protocol](protocol.json) contains exact inputs, prompts, installed
package identities and commands (executable paths normalized). Application results
are fictional retained evidence; no application tests run.

- Codex CLI 0.163.0-alpha.10.2 requests `gpt-6.1-sol`, medium; responding model
  identity is unconfirmed. Installed adoption/core/progress reads are observed.
  User config is ignored, delegation and memories disabled, and workspace-write
  sandboxing and ephemeral execution selected. Routine state-db warnings are retained.
- Claude Code 2.1.302 requests/reports `claude-opus-5-5`, medium. Adoption invokes
  installed `Skill(adopt-context-docs)` and reads core/progress; ordinary maintenance
  invokes installed `Skill(context-docs)` without a skill request in the task.
  Only file/Skill tools are enabled; MCP, hooks, auto memory and session persistence
  are disabled for the process. Existing authenticated access is used with
  `apiKeySource: none`; no API-key fallback. Both sessions report success with no
  permission denials. Claude's file boundary is prompt-based and checked afterward,
  rather than enforced by an OS sandbox.
- Each session has one attempt under 180 seconds, with no retry. Sol coordinates
  and scores; Claude produces its own output, without independent assessment review.

## Results

| Check | Codex | Claude |
| --- | --- | --- |
| Default inline path, without progress request | Pass: nested checklist | Pass: text tree |
| Supported goal, dependency, blocker and next action | Pass | Pass |
| Everyday update retains path and removes resolved blocker | Pass | Pass |
| Earlier evidence, owner decisions and separate deployment approval retained | Pass | Pass |
| No duplicate tracker or separate progress file | Pass | Pass |
| Source links and local anchors resolve, each phase | 4 relative links + 2 local anchors | 4 relative links + 2 local anchors |
| Only permitted fixture files change | Pass | Pass |
| Adoption / maintenance elapsed seconds | 26.42 / 19.12 | 29.43 / 18.33 |

Inspect the unchanged exact outputs: Codex [adoption context](codex/adopt/notes/context.md)
and [maintenance context](codex/maintain/notes/context.md), or Claude
[adoption context](claude/adopt/notes/context.md) and
[maintenance context](claude/maintain/notes/context.md). Each phase includes its
linked decisions/results. The [summary](summary.json) records scoring, hashes,
preservation and mechanical checks separately from native behavior.
Full traces and receipts are retained in durable private evidence.

## Limits and preservation

This is a guided, author-scored re-adoption case in each client, followed by an
ordinary result-recording task under a pre-existing maintenance rule. It does not
test fresh adoption that adds a new rule, implicit initial skill discovery, future
instruction loading, sparse/local-only/no-view cases, repeat/audit behavior, the
full progress suite or general user benefit. No Git fixture or probes are used.
Claude's loading claims in its final report are not independent proof of future
automatic loading. The maintenance prompt supplies the new result and next action;
the agent's tested task is integrating them into the existing context/view.

Adoption changes only `notes/context.md`; maintenance changes only that file and
`notes/results.md`. The earlier blocked observation remains dated in evidence
(Claude marks it superseded). Instructions, marker/date, logging off, owner-work
sentinel and decisions remain unchanged. Installed skills, existing project
setups, earlier evidence and saved studies are compared with the pre-run byte/mode
inventory; routine native-client global bookkeeping and Git metadata are outside
that inventory. No global-state equality or general isolation guarantee is claimed.
No skill changes, infrastructure or further model review are added.
