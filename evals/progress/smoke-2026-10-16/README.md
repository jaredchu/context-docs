# Markdown progress smoke check — October 16, 2026

**Outcome: core create/refresh behavior passed, with one minor source-link
presentation gap.** Two fresh Claude Code sessions used one synthetic Reed Export
project. No real project was opened or modified, and no product fix was made.

## What ran

- Source: `360aabbde81c156b8d4f2dfc4676ffdbb354813e`, core 0.2.0 development
  package, copied into the private fixture; installed packages were not upgraded.
- Claude Code 2.1.296, requested/reported model `claude-opus-5-5`, medium effort.
  Sol prepared the fixture, inspected transcripts/outputs and checked preservation;
  Claude generated the files. This is author-scored, not independent validation.
- Existing authenticated access; no API-key environment fallback. The CLI init
  reports `apiKeySource: none`; its modelUsage record is not backend identity proof.
- Per-process `--safe-mode --restricted`, file tools `Read,Write,Edit` only,
  `acceptEdits`, no permission prompts, no session persistence, strict empty MCP,
  hooks/auto-memory disabled. No persisted configuration was edited. This tests
  explicit reads of a copied skill, not ordinary default loading or installation.
- One create session and one fresh refresh session, each capped at 180 seconds,
  no retries. Observed process durations were 33.62 and 34.27 seconds; these are
  execution observations, not evidence of user-effort or subscription savings.

## Inputs and retained outputs

The synthetic owner goal requires both CSV-column compatibility and empty-input
handling checks to pass; deployment is separate and unapproved. Initially, the
columns check passes, empty-input testing is blocked on missing input, and five
retries remain a proposal. Dated notes distinguish discovering the correct input
path from later attempts with no new finding. An unrelated owner-work sentinel
and the manual-release note must survive.

1. [Create prompt](create-prompt.txt): write `notes/delivery.md`, link it from
   existing context, and change no other files. The model read core and the progress
   reference, then wrote the [initial view](create/notes/delivery.md) and updated
   [context](create/docs/context.md). The accompanying source snapshots preserve
   the initial [decisions](create/docs/decisions.md) and [evidence](create/docs/evidence.md).
2. The coordinator appended one fictional October 2 retained passing empty-input
   result to the source evidence, leaving the older note in place. No actual CSV
   implementation or application test was executed; the retained results are fixture
   data. This is the only coordinator source change between phases.
3. [Refresh prompt](refresh-prompt.txt): maintain the same view/context using the
   changed evidence, without supplying the expected state in the request. The fresh
   session again read core and the progress reference and produced the
   [refreshed view](refresh/notes/delivery.md) and [context](refresh/docs/context.md).
   [Refresh evidence](refresh/docs/evidence.md) retains both dated claims.

The `.md` outputs and source snapshots are exact generated/input text, not edited
reference answers. Raw native transcripts, complete fixture inventories and
command/status receipts are retained privately. The source snapshots above are
synthetic; the initial evidence copy was hash-verified against its frozen input.

## Observations and checks

| Check | Result | Evidence / limit |
| --- | --- | --- |
| Read development instructions | Pass | Native traces show direct reads of core and its packaged progress guide in both sessions. No automatic-selection claim. |
| Initial goal and status | Pass | Initial view keeps the two-check goal incomplete; passed columns and blocked/unrun empty-input work remain distinct. |
| Learning versus outcome | Pass | Wrong-path finding is useful learning; later no-finding attempts suggest a possible stall, with a dated range and history limits. |
| Refresh from newer evidence | Pass | The same view now marks both documented checks passed, resolves the blocker, and labels the older unrun claim as superseded/conflicting evidence. |
| Approval and runtime scope | Pass | Retries stay proposed; deployment remains unapproved/unverified. No percentages or live-agent claims observed. |
| Next action / unknowns | Pass | Initially prepare the input and check it; after completion, no next step is invented and owner decisions remain open. |
| Source-link resolution | Pass | 15 initial and 22 refresh link occurrences in view/context resolve to fixture files and anchors. |
| Per-item source-link placement | Partial | The first two meaningful-advances bullets lack their own inline links in both outputs; their facts are sourced elsewhere in the status/history sections. Preserve this presentation miss rather than claim complete per-item compliance. |
| Subject write boundaries | Pass | Create: one new view and one context edit. Refresh: only the same two files changed. No other fixture files, copied skill, owner note, sentinel or source evidence changed during either subject session. |

Both native commands exited zero with `terminal_reason: completed` and no
permission denials. Traces show only the three available file tools: initial
7 reads/1 write/1 edit; refresh 6 reads/1 write/1 edit. All observed tool paths
are inside the disposable project. After closeout, the preservation comparison
passes for the repository outside Git metadata (including saved studies), four
installed Context Docs package roots and selected Codex config / Claude settings
and instruction files. Only the new smoke evidence, current context, changelog,
scenario-index update and new event are allowed changes. Runtime caches and
routine client bookkeeping are outside that scope; this is not a claim of
byte-for-byte global client-state preservation.

## Limits and next step

This exercises creation of a linked view, source-based status refresh, retained-note
history and proposal preservation in one guided fixture. It does not execute the
whole seven-scenario suite. No Codex native, adoption, local-only, read-only audit,
no-change repeat, Git/journal history or default automatic-loading trial ran.
There is no general reliability, privacy or target-user usability conclusion.

No retry, new harness, infrastructure or skill rewrite follows from the minor
link-placement miss. Inspect per-item links during the next ordinary use; broader
changes need a concrete recurring problem. Release and installed upgrades remain
separate actions. Previous saved studies and the initial artifact-review record
are unchanged.
