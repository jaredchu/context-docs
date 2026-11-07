# Two directed coding-agent handoffs

November 7, 2026. **One guided Codex → Claude Code case and one guided Claude
Code → Codex case completed their scoped implementation handoffs.** In each,
the receiving session used saved files to recover the API-complete/browser-pending
state and continue the browser work. Separate coordinator API and browser checks
pass. Command-boundary deviations are retained below; this is not an unqualified
walkthrough or strict-boundary pass.

## Setup and method

Both cases start from Reading Queue's authored `switching-start` commit
`ed3a02a70a328c1b4140d45959f0a29dad3a47d3`, based on the original
`tutorial-start` commit `238d1d3c0921d304edc8770ced18355972cb7d64`.
The exercise makes the versioned empty shape explicit and limits the next work
to local implementation. Original tutorial tags and the deployed application
are unchanged. The switching starter retains the older `docs/walkthrough.md` as
background; its scope/deployment steps are not the switching instructions. Use
the new direction-specific pages and this starter's current context instead.

Each case had two fresh native CLI sessions, **four subjects total**, using
existing subscription authentication. Codex CLI **0.167.0-alpha.3.2** requested
**GPT 6.1 Sol**; its JSON stream does not independently expose the served model.
Claude Code **2.1.319** requested and reported **Claude Opus 5.5**.
Both requested **High** reasoning; effective effort was not independently exposed.
Memory was disabled per invocation and sessions were ephemeral/nonpersistent.
No global setting change, installed upgrade or authentication-profile reconfiguration
was requested or performed by the coordinator.

Each fixture supplied project-local copies of published bundle **v0.2.7**:
core **0.2.7**, adoption **0.1.16**. The project was already adopted, with an
`AGENTS.md` maintenance rule and a `CLAUDE.md` import. File consumption and
continuation are observed here; this is not a fresh installation/adoption trial
or a general instruction-loading guarantee.

The outgoing subject implemented only `GET /api/export` and meaningful API tests,
then updated the existing project context and decisions. It left the browser
integration as the next authorized task. The receiver got only the neutral
[continuation prompt](subject-prompts.json) and the same checkout's saved files;
neither the sender's conversation nor its answer was supplied. The prompt did
not restate the feature, its scope or rationale.

The starter already contained the export requirement, scope, rationale and
API-before-browser exercise split. Receivers retained and applied that shared
knowledge. The sender's new contributions were completed API work, exact pending
status, unrun-test limits and implementation choices. This case does not isolate
what the sender's notes added over the starter documents or code inspection.

The predeclared criteria covered whole-queue scope despite filters, the backup
rationale, browser isolation/expiry, the versioned empty shape with no metadata
or data writes, the API/browser split, continuation from files, honest test
limits and preservation of the project write boundary. The coordinator accepts
all eight content/continuation criteria in both directions, separately from the
command deviations. Only authorized project files changed.

The subjects were limited to file inspection/editing. They added tests but did
not execute them, and their saved context retains that distinction. The
user-facing walkthrough additionally asks its users to run local tests; these
bounded subjects did **not** execute every walkthrough prompt unchanged.

## Results and artifacts

| Direction | Agent API suite, run by coordinator | Adapted reference API suite | Actual browser checks |
| --- | --- | --- | --- |
| Codex → Claude Code | 20/20 pass | 18/18 pass | Whole queue under Unread filter; exact public fields and filename; fresh empty export without reload; failed fetch shows error with no download |
| Claude Code → Codex | 21/21 pass | 18/18 pass | Same checks pass |

The agent-suite totals include the 16 existing baseline tests plus four export
tests in Codex → Claude Code or five in Claude Code → Codex. API tests execute the real Worker in workerd/Miniflare with local D1. Browser
checks use fresh local headless Chrome against each completed fixture's local
Wrangler server and database. Actual JSON downloads are inspected. The failure
case substitutes an HTTP 500 response for `/api/export` in the browser; it is
not a production outage. No remote resources or application deployment ran.

The reference API suite reuses the earlier completed example and removes two
details not prescribed by this exercise: an HTTP Content-Disposition header and
creation of a session cookie for an empty export. It was selected/adapted after
subject outputs. Browser checks were also authored after outputs. These are
coordinator checks, not frozen independent acceptance tests or grading. The unadapted reference
suite requires behavior these implementations do not both provide; these passes
do not mean that original suite passed. Codex's API creates a fresh session cookie
for a missing/malformed cookie, following the existing GET policy; Claude's API
does not. Neither mutates D1 during export or includes cookies/IDs in JSON.

- Codex → Claude Code: [outgoing context](codex-claude-sender-context.txt),
  [receiving context](codex-claude-receiver-context.txt), [complete case diff](codex-claude.patch).
- Claude Code → Codex: [outgoing context](claude-codex-sender-context.txt),
  [receiving context](claude-codex-receiver-context.txt), [complete case diff](claude-codex.patch).
- [Structured summary and artifact hashes](summary.json),
  [exact bounded subject prompts](subject-prompts.json).

The context files are exact saved bytes; they describe their original
pre-verification state. The coordinator's later checks do not rewrite subject
notes or turn their unrun tests into subject-executed tests. Diffs are the full
tracked changes from the teaching starter, not patches against product code.
Raw streams, hook logs, local browser downloads and task scripts remain in
private task storage under evidence ID `examples-implementation-2026-11-07`.

## Retained deviations and limits

The original Codex → Claude Code [receiver note](codex-claude-receiver-context.txt)
describes malformed-response rejection too broadly. The saved implementation
checks `schema_version` and whether `items` is an array, without validating every
item's fields. For example, an HTTP-success response containing
`{"schema_version":1,"items":[{}]}` passes that envelope check and can produce an
invalid downloaded item. This is a source-derived counterexample, not a newly
reproduced runtime failure. The checked API constructs valid items, and
comprehensive malformed-item validation was not an exercise acceptance criterion.
The reported acceptance checks remain valid; the original note and case patch
are preserved unchanged.

The original private protocol used the shorthand “frozen API checks” in one
limit. The criteria were predeclared, but the actual reference suite was adapted
after outputs. That label was inaccurate; the public summary uses “post-output
coordinator API checks.” The original protocol remains unchanged as evidence.

Both Codex subjects ran `pwd` once despite the tighter command restriction to
file inspection/editing. They disclosed this, and the command is retained in
their streams. No outside-allowlist project edit occurred. The content and
implementation outcomes do not erase those command-boundary deviations.

The initial coordinator browser verifier expected repeated downloads to receive
distinct filenames; Chrome overwrote the existing filename. Corrected checks
verified the parsed downloaded JSON and counted download attempts. Both empty
downloads have the required versioned structure; Claude → Codex uses pretty
printing and a trailing newline, while Codex → Claude uses compact JSON. The
browser check establishes semantic JSON equality, not identical file bytes. No subject
was rerun and no app code was repaired.

These are two coordinator-authored, guided cases on one host, one attempt per
direction, without a comparator, held-out projects, independent grading or
unfamiliar users. Each direction uses a single checkout, so this does not test
Git transfer, distinct physical machines, missing or ignored files, unsaved
buffers, native-memory conflicts, runtime/credential transfer or simultaneous
writers. Claude file-tool hooks constrain exposed operations, not an OS sandbox;
Codex uses its workspace-write sandbox for shell inspection. Host runtime
bookkeeping is outside the project inventory.

The checks support these two observed continuations. They do not establish
general switching reliability, exclusive Markdown capabilities, lower effort,
token/allowance savings or dependable automatic maintenance. Native instructions
and competent ordinary Markdown can support the same workflow. Skill behavior
and versions are unchanged.

## Artifact review

A separate Claude Opus 5.5 session, configured High, reviewed the coordinator's
protocol, supplied outputs, case patches and proposed report. It found no app
correctness regression or public privacy issue, and requested narrower claims
about starter knowledge, post-output tests and parsed-JSON comparison. The
coordinator applied those corrections. One focused follow-up confirmed the test
and JSON corrections and caught an omitted starter-information paragraph; the
coordinator inserted it and verified the exact resulting source. No third model
review ran. The reviewer did not regrade cases, audit raw streams, recompute
hashes or execute checks. This is artifact review, not independent validation.
Original review reports and runtime metadata are retained under the same private
evidence ID as the case records.
