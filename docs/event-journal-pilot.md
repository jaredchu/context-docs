# Optional event journal pilot

Status: optional integration candidate, schema version 1. Core v0.1.3 packages
[the helper](../skills/context-docs/scripts/event_journal.py) and
[its portable guide](../skills/context-docs/references/event-journal.md).
Adoption v0.1.5 merges opt-in settings on request. Logging is off by default;
installing or updating a skill does not enable it. Python 3.9+ is required only
for the optional CLI. There is no background capture or scheduler.

The owner authorized a small optional JSONL pilot on September 28, 2026 and later
clarified its purpose: efficient recording of history for investigation when
needed. Improving current context, saving context tokens or speeding up routine
handoffs are not the logging feature's success criteria. The CLI and schema are
implementation choices; capture and later diagnostic usefulness need their own
evaluation.

## Roles and scope

Markdown remains the curated account of current state, decisions and procedures,
following the [canonical standard](../skills/context-docs/references/standard.md).
The journal records meaningful verification, contradictions, decision changes and
context updates, with their sources. It is original evidence, not a disposable
cache. Do not log every tool call, conversation transcript or repetitive progress
message. Use synthetic examples in this public repository; keep private-project
journals with their own projects. Capture significant events when they happen;
waiting until a question arises can lose the evidence. Read the relevant logs
when investigating a failure, checking past work or reconstructing a decision.
Do not routinely load the journal into current context.

The [packaged command](../skills/context-docs/scripts/event_journal.py) records statements supplied by the caller.
Validation checks structure, not whether evidence exists, a check ran, an approval
is genuine or a claim is correct. Never turn a proposal into approval just because
it was implemented. `actor` names the recorder; `authority` identifies who approved
a statement and where that approval was recorded.

## Efficient logging goals

- Keep events compact and factual: what happened, when, which session/actor and
  revision, outcome and scope, and a useful source reference. Include approval
  authority or correction references when applicable.
- Record meaningful failures, checks, state changes and decisions. Avoid repeated
  narration of the same event. A log's value does not depend on being read during
  the next session or introducing a fact absent from current documentation.
- Keep normal capture lightweight. The earlier trial's repeated file snapshots,
  comparison reports and payload archives were evaluation apparatus, not a
  requirement for every log entry. Preserve external evidence separately when a
  compact event and source reference would otherwise lose needed diagnostic detail.
- Keep history reliable and investigate errors explicitly. An acknowledged event
  should remain readable; partial writes, missing events, duplicate retries and
  corrections must be considered when assessing reliability. Existing limitations
  below remain in force.
- Control growth through session files and a deliberate retention policy. Read
  the smallest relevant set on demand. Automatic cleanup is still unimplemented;
  low read frequency alone is not a reason to discard historical evidence.

These are the current design goals, not a claim that the prototype already meets
them. In particular, append currently validates all prior records in its session,
and the CLI still requires manually supplied event fields. Their recording cost
is an implementation concern, independent of current-context quality.

## Requirements before broader integration

The owner added three requirements on September 28, 2026: evaluate Claude as well
as Codex, support projects that already adopted Context Docs seamlessly, and first
determine whether a separate journal is necessary alongside Markdown/Git.

### Establish necessity

Git preserves committed document/code history, including any event evidence people
choose to record there. It does not automatically capture command results, failed
attempts, runtime observations or the authority behind a change. Existing Markdown,
commit messages, CI artifacts and application logs may already preserve enough.
A separate Context Docs journal is useful only for a concrete recording or later
investigation need those sources leave unmet at reasonable effort.

Separate two questions: whether more event capture is needed, and whether JSONL
is the right format. A dated Markdown event log can preserve the same facts, with
or without Git. JSONL's structured validation and filtering are potential conveniences,
not evidence that another storage format is inherently necessary.

The owner also identified projects without Git and projects with infrequent
commits as important cases. Files written between commits can retain events,
but Git cannot recover intermediate versions that were never committed. In a
project without Git, either Markdown or JSONL can provide durable event history;
neither format captures events automatically or substitutes for backups.

The [native comparison protocol](../evals/event-journal/native/protocol.md)
tests these two cases with equal capture opportunities. A separate mechanical
control checks recovery of a committed observation from Git. This is a bounded
comparison before expanding the helper or packaging it:

1. Competent ordinary Markdown/Git maintenance with the project's existing logs
   and check artifacts available.
2. The same environment with a simple Markdown event log, committed when Git is used.
3. The same environment with the JSONL helper.

Give all conditions the same events, authority information, source access and
permission to preserve useful evidence. Include a case whose history is already
fully recorded, and a case with transient failure/check observations. Do not
prevent the baseline from recording those observations or remove its evidence
to manufacture an advantage. Distinguish what was captured from what a later
reader correctly reconstructs. Measure recording effort, missed/duplicate events,
history preservation and on-demand diagnostic completeness; routine context
quality or savings remain outside the logging acceptance criteria.

If ordinary Markdown/Git covers the requirements, do not require another journal.
If extra capture helps but Markdown records it just as effectively with less work,
prefer that simpler approach. Keep JSONL optional unless its practical benefit is
demonstrated. Existing synthetic and same-chat results do not settle these choices.

### Test Claude and Codex

Run the selected capture, investigation and upgrade cases in actual native Claude
Code and Codex sessions. Record client/model versions, tool/instruction exposure,
execution outcomes, source/event preservation and semantic review separately.
Repeat/no-change maintenance and audit-only behavior belong in both client suites.
Python tests alone, or another client's scores, do not establish Claude behavior.

The [native history comparison](../evals/results/2026-09-28-native-journal/README.md)
ran 12 actual Claude Code and Codex sessions with no-Git and sparse-commit cases.
All formats retained the requested facts; Claude overstatements and recovered
capture failures remain recorded. Twenty-two actual helper appends succeeded.
This constrained bridge comparison establishes neither JSONL necessity nor
natural capture efficiency. Its fresh read-only investigations preserved files;
full skill instructions, automatic loading, repeat maintenance and upgrades were
not exercised. The earlier file-only Claude guard still does not cover execution;
this run used a separately tested exact-command guard for the evaluation bridge.

### Preserve existing adopters

Acceptance requirements for any selected upgrade path:

- Reuse existing context paths, maintenance rules, adoption dates and decision
  history. Do not reinitialize a project or rewrite its layout to add logging.
- Update the instruction file actually loaded by the client, including Claude-only
  and mixed-instruction projects; do not create competing maintenance rules.
- Updating skills must not leave dangling references to a helper available only
  in this development repository. Package required resources with the owning
  skill, or supply a documented compatible installation path.
- Existing Markdown maintenance must keep working without a logger. Report an
  unavailable logging command when capture is requested; do not silently claim
  that an event was recorded. Avoid a new mandatory runtime dependency unless
  justified by the chosen design.
- Repeating setup with no new work must preserve project bytes and the original
  adoption marker. Audit-only operations remain read-only, including journals.
  Disabling optional logging must preserve existing event history.

These remain integration requirements. The native comparison checks preserved
instruction files, original dates and custom paths, but does not test a package
upgrade or install the skills in its fixtures. The owner subsequently authorized
a minimal opt-in integration and native upgrade/lifecycle tests. The
[integration protocol](../evals/event-journal/integration/protocol.md) covers actual
project-installed packages, sequential checks, repeated setup, missing-helper
behavior, audits and disabling. Existing projects retain ordinary Markdown
maintenance; only explicit enablement adds logging settings. The
[completed lifecycle results](../evals/results/2026-09-28-journal-integration/README.md)
retain the initial Claude failures and separate passing functional follow-up.
The [capture-gap repair](../evals/results/2026-09-28-journal-gap/README.md) preserves
failure reasons in Markdown when logging is unavailable; fresh readers in both
clients recovered them. These are bounded experimental results, not a general
reliability or recording-effort guarantee.

## Try it

Run from this repository root. These commands record a clearly labeled synthetic
example in the existing gitignored scratch area:

```sh
python3 tools/event_journal.py --directory .local/event-journal-demo append \
  --session demo-001 --input examples/event-journal/verification.json
python3 tools/event_journal.py --directory .local/event-journal-demo read \
  --session demo-001 --type verification
```

The append command also accepts one JSON object on standard input when `--input`
is omitted. Success prints the stored event, including its generated UUID. Failure
returns a nonzero exit code and a diagnostic on standard error. Repeating append
creates a new event; there is no retry deduplication.

For real work, omit `--directory` to use `.context/events` relative to the current
working directory, or select a project's directory explicitly. Choose a unique
session ID, for example a UUID, and reuse it for that session. Session names allow
1–80 ASCII letters, digits, underscores or hyphens, beginning with a letter or digit.
Each session writes one `<session-id>.jsonl` file. Review event files before choosing
to commit them; this tool never commits or publishes them. Runtime lock files in
the default directory are gitignored; other journal locations need their own rule.

`read` with no filters validates and emits all `.jsonl` files directly in the
directory. `--session` selects one file; `--type` filters output after validation.
Reading creates no directories or files. A missing directory or selected session
is an error; an existing empty directory returns no events. Output preserves file
order within each session and filename order across sessions, not global chronology.
Timestamps are recording times from the local clock, not causal ordering or a claim
about when earlier evidence occurred. State earlier observation dates in the summary
and source reference when they matter.

## Schema version 1

The canonical [payload fields and recorder/authority definitions](../skills/context-docs/references/event-journal.md#payload-schema-version-1)
ship with the core skill. The packaged guide also owns enable/disable settings,
installed-path resolution and capture-failure behavior.

The writer adds `schema_version` (1), `event_id` (UUID), `recorded_at` (UTC) and
`session_id`. Caller-supplied generated fields, unknown fields, duplicate JSON keys,
non-JSON numeric constants and invalid field types are rejected. Embedded newlines
are JSON-escaped, so each event occupies one UTF-8 line ending with a newline.

For a context update, record what changed and why in `summary`, and reference the
changed document and supporting evidence in `sources`. A Git commit alone does not
identify uncommitted content; retain the relevant output or snapshot separately.
The journal does not copy evidence files or execute the command named in `check`.
Git is not a runtime requirement. Without it, record `unavailable (no Git)` and
retain the relevant event details/output. With infrequent commits, label the
working state as uncommitted; an old HEAD alone does not identify that state.

Correct an earlier event by appending a new one with `supersedes`; preserve the
original bytes. That reference is checked for UUID syntax, but its target is not
resolved or marked automatically. Readers see both events, including earlier claims;
this CLI does not compute an authoritative current view or update Markdown.

## Write failures and concurrent access

Append validates the payload before creating the directory. It takes an exclusive
per-session lock, validates the entire existing session, appends the record, flushes
and calls `fsync` before reporting success. Concurrent calls through this command
for the same session are rejected while the lock is held; different sessions use
different files. This is a local cooperative writer protocol, not a distributed
lock, database transaction or security boundary. Other editors can bypass it.

A killed process may leave a `<session-id>.lock` file. Confirm the writer has stopped,
inspect and preserve the session file, then remove only that stale lock. The tool
does not guess when a lock can safely be stolen. A reader overlapping an append can
encounter an incomplete last record; retry after the writer finishes.

Malformed history, duplicate event IDs in the selected files and an unterminated
last record cause a failure. The tool does not silently skip, truncate or repair
them. Preserve the original file before any manual recovery. If an interrupted
record cannot be recovered, start a fresh session and retain the damaged artifact
outside the directory scanned by `read`, with a reference from the new event.

An I/O error or lost success response can occur after bytes were written. Inspect
the session before retrying to avoid duplicate events. File flushing does not
provide atomicity with Markdown edits or a guarantee of crash-safe directory
creation. The synthetic failure controls cover malformed tails, a killed writer
and a simulated `fsync` failure; they are not power-loss testing.

## Rotation and retention

The pilot rotates naturally by starting a new session file. It does not implement
size-based rotation, compression, archival or automatic deletion. Completed sessions
remain readable; they are closed by convention, not sealed or immutable. Both append
validation and unfiltered reads scan selected history, so this design targets small
project journals. Use session filtering as history grows; measure before adding an
index or more retention machinery.

Preserve durable events and cited evidence. A summary does not automatically replace
the originals. Deleting a committed file only removes it from the current tree, not
Git history. Define any future retention policy separately for disposable operational
logs, rather than applying a blanket age cutoff to project evidence.

## Evaluate the pilot

Evaluate logging against later diagnostic needs:

| Concern | Evidence to collect |
| --- | --- |
| Capture fidelity | Known significant events recorded with correct scope, source and status; omitted or duplicate events reported |
| Recording cost | Manual effort, append latency, bytes per event and growth under realistic event volume |
| History reliability | Previously acknowledged records survive the tested failures; recovery preserves evidence and reports incomplete history |
| On-demand investigation | Later questions can reconstruct the relevant change, check/failure or decision using recorded events and available evidence |
| Lifecycle | Session selection, rotation and any explicit retention policy preserve the history required for investigation |

Use synthetic incident/change histories for controlled tests, then actual logging
work for capture effort. Keep capture and investigation separate: an event may
be valuable even if it is never needed during ordinary maintenance. Do not invent
incidents or remove common source evidence to create a journal advantage. No
general incident-investigation benefit is established by these small authored cases.
The native comparison and current integration protocol keep capture and fresh
investigation separate.

### Earlier context-retrieval trial

The [bounded live trial in this repository](event-journal-live-trial.md) is closed
after three maintenance tasks in the same chat. Its two handoff reviews found
grouping but no missing fact recovered beyond docs/raw evidence. That led to an
assistant recommendation to end routine logging. The owner's later clarification
supersedes using that context-retrieval criterion to decide whether logging is
worthwhile. The old trial does not establish that historical logging is unnecessary;
its observations and limitations remain recorded. Its temporary rule remains removed.

Original trial design: try three meaningful maintenance sessions in a consenting
project, using unique session IDs and recording only events that answer the questions
below. This is a usability pilot, not a benchmark or an instruction to manufacture
events when nothing changed. No recurring task is installed.

Before each session, retain the starting Markdown/Git revision. Afterward, retain
the final revision and any dirty-state evidence along with the journal. For each
question, compare the same final Markdown/Git/evidence with and without the journal:

1. What was checked, against which revision, and with what result and scope?
2. Why did the current context change, and what evidence supported the change?
3. Which contradiction or unresolved issue needs the next reader's attention?

Record supported answers, omissions or false claims, evidence references, retrieval
effort and logging effort. When one person reads both conditions, note order effects;
do not interpret that as a controlled accuracy comparison. Preserve failed or missed
events and corrections. Share only synthetic or explicitly publishable evidence here.

The original decision rule judged whether the feature added information or reduced
handoff effort enough to justify maintenance. That rule is retained as historical
method, not the current logging goal. Numerical speed, accuracy or reliability
claims still require a separately designed evaluation.

## Mechanical validation

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
python3 evals/checks/static_checks.py
```

The [synthetic tests](../tests/test_event_journal.py) exercise CLI input/output,
validation, read-only behavior, preservation on malformed input, correction history,
competing writers and selected I/O failures. CI runs them separately from packaging
and link checks. The [September 28 evaluation](../evals/results/2026-09-28-event-journal/README.md)
retains two initial failures from one nesting-error defect and 25 passing tests
after repair. A three-stage synthetic replay preserved ten events, with separate
author review and local latency diagnostics. The later live trial covers real
documentation tasks in one authoring chat, not independent reader sessions or
unrelated project work. The later native comparison includes fresh readers but establishes no JSONL
advantage. Installed-skill lifecycle testing is recorded separately from these
earlier studies.
