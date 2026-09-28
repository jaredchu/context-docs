# Native event-history comparison — 2026-09-28

**Meaningful history survived without Git and between commits in all three
formats. This study does not establish a need for JSONL over Markdown.** Keep the
helper optional; recording useful events is the key behavior. A project whose
existing documents/check artifacts already preserve that evidence needs no
additional journal for these cases.

## What actually ran

Twelve fresh native sessions: Claude Code and Codex × three capture formats ×
capture/fresh investigation. Each session handled two existing-adopter fixtures
(no Git and one initial Git commit), so these are grouped cases, not 24
independent trials. Ordinary Markdown could preserve dated history in its
existing context; the other arms could use a separate Markdown log or JSONL.
All received the same evidence and capture permission.

- Claude Code 2.1.234, actual stream model `claude-sonnet-5`.
- Codex CLI 0.158.0-alpha.2.1, client default with user config ignored. The retained
  stream does not expose the model identifier; it is not inferred from another
  session's settings. This limits reproducibility and model comparisons.
- Synthetic check outcomes were supplied observations, **not export checks run
  by this evaluation**. The actual journal helper CLI executed 22 appends:
  10 for Claude and 12 for Codex. All succeeded; all four journals pass read/schema
  validation, with unique IDs and no repeated successful append attempts.
- All six no-Git probes fail to find a repository; all six sparse-Git fixtures
  still have one commit. A separate mechanical regular-commit control recovers an
  observation from Git after the current document text was replaced.

The [protocol](protocol.md) and [frozen inputs/hashes](frozen.json) were written
before model execution. Frozen source copies live under `source/`.
[Fixture checks](fixture-checks.json), [native outcomes](trials.json),
[mechanical summary](mechanical-summary.json) and [author reviews](reviews.json)
retain the evidence. Each condition also has its prompt, stream, final response,
stderr and resulting project files; Claude guard decisions are preserved.

## Results and errors

Every fresh reader recovered the five requested fact groups for both projects:
original local approval, staging failure, unapproved proposal, scoped owner
approval/pass, and unknown production status/Git coverage. This means required
facts appeared; it is **not a perfect-answer or error-free capture score**.

Claude's three conditions fail strict semantic acceptance because an unapproved
proposal became an explicitly rejected proposal in capture or reader wording.
The JSONL reader repeated the stronger assertion stored in its event. Structure
validation did not prevent that factual overstatement. The original-local versus
later-staging scopes were also blurred in some Claude summary wording; detailed
records generally retained the distinction. Codex's three conditions meet the
factual target acceptance. Its ordinary reader includes one incorrect extra JSON
field locator alongside a valid Markdown citation supporting the same claim.
These single attempts establish no general model ranking.

Execution errors remain separate:

- Each Claude Markdown capture first tried event arrays reserved for the JSONL
  arm. The bridge rejected two calls before any write; corrected saves succeeded.
- Claude JSONL capture had one noncanonical shell-quoting attempt denied by the
  evaluation guard, then recovered. No helper append failed. The native terminal
  result retains the permission denial, so this is not a clean execution pass.
- All observed Claude tool calls have matching guard decisions. Every Codex
  command follows the same bridge-only command policy. No unexpected project
  files appeared. Codex's read-only Git calls emitted Git/Xcode cache-permission
  warnings while successfully returning the records; readers disclosed that limit.
- Every protected instruction/README/configuration file kept its bytes. All six
  fresh investigations preserved all non-Git project file bytes, including logs.
  This is a constrained read-only check, not unrestricted-agent reliability.

Both JSONL clients used event participants for some `actor` values, whereas the
pilot guide describes the recorder. The abbreviated evaluation prompt named that
field without defining the distinction. Thus schema success does not establish
compliance with the full guide's metadata semantics. No full guide or packaged
skill was installed or exercised by this bridge-only comparison.

[Observed duration, calls and record sizes](table.md) are descriptive only.
Claude's corrected calls and the common bridge/schema prompt confound timing.
One attempt, differing models, and a simplified interface cannot establish a
speed advantage. Separate logs also duplicate facts retained in current Markdown;
these captures do not establish lower recording overhead or less duplication.

## Existing adopters and remaining limits

All fixtures retained their original September 1 adoption date, both instruction
files, custom `notes/state.md` path, and original local decision. Neither skill nor
its version changed. Existing adopters need no migration for these repository-only
evaluation changes.

**The upgrade requirement remains open.** This tests coexistence with existing
layout and read-only investigation, not installation, automatic instruction
loading, repeat/no-change maintenance, missing-helper behavior, disabling, or a
real skill upgrade. The protocol's installed-package preservation criterion was
not exercised: fixture packages were not installed. Keep those gates before any
broader integration; do not infer them from unchanged instruction files.

The helper was invoked through an evaluation-only fixed-path bridge; readers
received file contents through that bridge rather than discovering the helper or
using its filtered read command. Claude's exact-command hook is not an OS sandbox;
Codex used its native workspace-write/read-only modes. Host instructions may
influence both clients. Authoring and review were neither independent nor blind.
Capture saw all supplied events at once, so this does not test interruptions or
missed events across real working sessions. Reader source IDs refer to retained
summaries of the ephemeral feed, not independent external evidence. The same
capture opportunities were given to ordinary Markdown.

The practical direction is optional history capture where existing records leave
a gap, including no Git and infrequent commits. Prefer the project's existing
usable format. JSONL remains available for structured validation/filtering needs;
its necessity, natural capture-effort advantage and seamless package upgrade
are not established here. Earlier studies and their scores remain unchanged.
