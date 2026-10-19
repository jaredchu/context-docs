# Metadata-filtering candidate smoke

October 19, 2026. **Both clients pass the visible saved-Markdown checks.**
Claude could not locate an unlinked operator note with its restricted discovery
tools, so filtering incoming metadata from that note is untested in Claude.
This coverage gap is retained without a session rerun or output repair.

## What ran

One fresh session per client uses copied core **0.2.6** / adoption **0.1.15** from
[08bc875](https://github.com/jaredchu/context-docs/commit/08bc87548435a31f288d154e584db42227462dc9).
The [pre-run protocol](protocol.json) and [digest](protocol.sha256) retain exact
inputs, prompt, criteria, package identities and normalized native commands.
Two tiny fictional cases share each client's session:

- Re-adopt public contributor context: remove explicitly retired personal setup
  details and repeated bookkeeping; retain the small-sample result, runtime,
  staging boundary, unknown production behavior, missing-fixture blocker,
  compatibility rationale, proposed JSON and separate deployment approval.
- Maintain owner-only offline notes: retain the useful volume path, case-sensitive
  filenames, offline boundary, sample-only repair and conditional next action.

Only Progress and Next action in two context files are writable. Source evidence,
decisions, owner notes, rules, adoption date, logging off and copied packages are
protected. No application tests, installed upgrade or native journal capture run.

Codex CLI **0.163.0-alpha.10.2** requests `gpt-6.1-sol`, medium; responding model
identity is unconfirmed. Claude Code **2.1.302** requests/reports
`claude-opus-5-5`, medium, with `apiKeySource: none`. Codex uses ephemeral
workspace-write execution with user config ignored and memories/delegation
disabled. Claude uses Read/Write/Edit only, safe mode and a write sandbox limited
to its new scratch subtree and scratch temporary directory; hooks, MCP, Chrome,
auto memory and session persistence are disabled. Candidate instructions are
read explicitly as files; automatic loading is not established.

Both sessions exit zero within the 180-second cap: Codex **31.54 seconds**,
Claude **134.30 seconds**. These timings do not establish comparative efficiency.

## Results

| Check | Codex | Claude |
| --- | --- | --- |
| Incidental public usernames/home paths/account ID and routine bookkeeping removed | Pass | Pass |
| Decisions, rationale, conditions, uncertainty, blockers and next action retained | Pass | Pass |
| Useful personal path, filesystem/offline constraints and repair limits retained | Pass | Pass |
| Context source links are relative and resolve, including anchors | 10 checked | 11 checked |
| Only permitted files/sections change; owner text and other fixture entries preserved | Pass | Pass |
| All 16 copied package files preserve their hashes and modes | Pass | Pass |
| Private incoming operator note located and used | Yes | Not covered |

Exact outputs: Codex [public context](codex/public/notes/context.md) and
[personal context](codex/personal/notes/context.md); Claude
[public context](claude/public/notes/context.md) and
[personal context](claude/personal/notes/context.md). Linked fictional sources
are exported alongside them unchanged. The [summary](summary.json) records
artifact hashes, criteria, operation audits and preservation scope.

**Fixture qualification:** the prompt did not name `public/private/session.md`,
and Claude's tools had no directory-listing operation. It made 44 failed reads
while guessing source names, found the public check report, and accurately
disclosed that it had not found or used the private note. Its output filters
metadata already present in context; it does not demonstrate filtering metadata
from the unseen note. Codex used a read-only file listing and read the note.
The note's source contents remain in the frozen synthetic protocol. Any future
repeat should supply a direct source pointer or suitable read-only discovery;
this run and its frozen inputs remain unchanged.

Codex retains a compact nested list; Claude renders an inline path inside the
existing public Progress section. Both retain the section boundaries and owner
text. Sol inspected all observed operations; Claude did not reread its edited
files, and final artifacts were checked externally. There is no implicit-loading
claim or claim that unseen private input was safely handled.

## Limits and preservation

Sol authors and scores this guided smoke; Claude is a subject, not an independent
reviewer. No comparison arm, fresh setup, cross-session continuity, general
privacy guarantee or automatic everyday application is established. Logging
remains off in these fixtures; journal filtering retains its separate
[offline schema/control coverage](../README.md).

Source packages, installed packages, setup rules and original studies preserve
their recorded bytes/modes. Setup settings are unchanged; routine client cache
metadata is outside the equality claim. No global runtime-state equality is
claimed. Original studies, private evidence and setup files were not restored or
rewritten. New results do not clear earlier study qualifications.

Raw native traces, receipts and preservation inventories are retained privately
under evidence ID `candidate-v026-filtering-smoke-d172530a-34a4-49c2-b19f-9a2c93d60466`.
The identifier and hashes do not make raw evidence publicly accessible or
independently verified. Public exports contain synthetic inputs/outputs and
normalized commands, without real home/evidence-directory locations.
