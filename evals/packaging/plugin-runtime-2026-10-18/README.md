# Synthetic plugin runtime smoke

October 18, 2026. **Partial: Claude passes the focused journey; Codex execution is blocked.**
Both use the unchanged frozen candidate ZIP pinned in the [protocol](protocol.json).
No persistent plugin installation, submission or publication occurs. Earlier
[metadata results](../codex-plugin-loading-2026-10-18/README.md) remain unchanged.

## What ran

One native process per client, with two planned model turns: adopt an existing tiny
fictional project, then maintain it after the operator adds one new fictional
sample result. Each process has a 300-second cap within the owner's 20-minute
budget. No retries, output repairs or broader permissions follow. This is explicit,
guided invocation, authored and scored by Sol; Claude is a subject, not an independent
reviewer. The [summary](summary.json) records tool sources, results and raw hashes.

Codex requests `gpt-6.1-sol`, medium; responding identity is unconfirmed. Claude
requests/reports `claude-opus-5-5`, medium, through existing subscription access.
Codex reports ChatGPT authentication; Claude reports `apiKeySource: none`.
No API fallback, dependency install or new account is used. The inputs and final
context files contain only synthetic project information.

## Results

| Check | Codex | Claude Code |
| --- | --- | --- |
| Native packaged entry discovery | Both names returned by plugin/read | Both namespaced Skill invocations succeed |
| Execute adoption and read bundled core/progress guide | Unverified; runtime blocked | Pass |
| Add one inline path and one maintenance rule/marker | No edits | Pass |
| Update that same path from the new source evidence | No edits | Pass |
| Preserve decision/rationale, owner gate, missing-fixture blocker and unrun suite | Original fixture unchanged | Pass; two-sample-only pass remains qualified |
| Preserve setup/source files and exact frozen package bytes | Pass | Pass |

Claude completes both turns in **67.11 seconds**, exit zero, without permission
denials. Adoption edits only AGENTS.md and Current work in the existing context;
maintenance changes only that context's Current work and Next action. It invokes
`context-docs:adopt-context-docs`, reads the packaged sibling core and progress
guide, then invokes `context-docs:context-docs` for maintenance. The context has
one text path at both stages, preserving all original headings. 6 adoption
links and eight final links resolve. The sample pass remains limited to two files;
empty-input verification remains blocked and owner review is still required.
Original source evidence, logging off and the CLAUDE.md import are unchanged.

Exact Claude outputs: [adopted context](claude/adoption/notes/context.md),
[adoption rule](claude/adoption/AGENTS.md),
[maintained context](claude/maintenance/notes/context.md) and
[new fictional evidence](claude/maintenance/notes/checks-update.md).

Codex completes its two responses in **34.12 seconds**, exit zero, but performs
**no fixture edits**. The app-server reads both plugin entries, then receives
explicit native skill inputs using the returned names and paths. The enclosing
plugin remains uninstalled and disabled. The model reports that shell reads fail
with `sandbox-exec: sandbox_apply: Operation not permitted` and the selected
namespaced skills are unavailable. Stderr confirms sandbox violations, but the
captured stream lacks native tool-result events establishing the exact failing
operation or the selection failure's cause. This is a blocked test route, not
proof of candidate incompatibility or successful skill execution.

The runner incorrectly equated protocol `completed` with task completion and
sent the planned maintenance turn after no-op adoption. Both responses and
unchanged outputs are retained; neither is scored as a pass. No retry or permission
expansion follows. The private post-run checker also initially failed on its own
heading regex; its corrected version passed without touching model outputs or
rerunning either client. These harness qualifications remain distinct from model
behavior. Codex outputs remain the [original context](codex/maintenance/notes/context.md).

## Preservation and limits

Both clients run inside macOS write sandboxes limited to their respective scratch
trees, with the extracted candidate denied writes. Codex retains the previously
assessed exact runtime identity-file exception; its bytes, owner/group, mode,
inode, links and timestamps remain unchanged. Real project and standalone skill
reads are denied. Native inference and startup network traffic are permitted;
network tools are forbidden. Codex still reads existing user/runtime configuration
and remote catalog state; its attempted global cache/snapshot writes are denied.
There is no clean-account or complete runtime isolation claim.

All 21 candidate files in each extraction equal the frozen ZIP. All protected
installed skill/setup/study files match the pre-run inventory; existing study
outputs, frozen evidence and setup preferences are unchanged. Raw transcripts,
receipts, checks and the original private checker are retained privately. Current
status summaries and this separate record are the only project documentation additions.

This checks one guided journey on an existing context layout. It does not establish
implicit selection, automatic everyday maintenance, cross-session continuity,
duplicate standalone selection, install/upgrade behavior or directory eligibility.
Claude initialization also lists two built-in helper plugins; only the two selected
Context Docs Skill calls occur. This is not a claim that all other plugin metadata
was absent. No skill or packaging fix is attempted. Repository checks are separate from
these model results; original release and smoke qualifications remain intact.
