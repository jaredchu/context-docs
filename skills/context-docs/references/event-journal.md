# Optional event journal

Record compact evidence for later investigation when the project opts in. Git
is not required. Existing Markdown history, CI results or application logs may
already suffice; a journal is optional, not a replacement for current context.
Consult history when needed, not as routine session context. No automatic capture,
background process, cleanup or factual verification is provided.

Decide whether history is needed before accessing journal files. No-change
maintenance uses current context and supplied evidence; do not scan or read the
journal merely to confirm that nothing changed or to check a context-to-history
link. Read relevant records for a historical question, a contradiction requiring
history, or an uncertain write. New event capture still uses the helper, including
its internal validation of the selected session. A successful append already
returns the stored record; an additional history read needs a concrete reason.

## Enable, upgrade, disable

Logging is off when no setting exists. Installing or updating this skill does
not enable it. On an explicit request to enable JSONL, merge these two lines beside
the existing maintenance rule in the instruction file the client actually loads:

```text
Event journal: jsonl
Event journal directory: .context/events
```

The directory is relative to the project root, not the installed skill. Honor a
user-chosen directory and existing equivalent settings. If the project already
uses another logging method, preserve it unless a change is requested. Keep the
original adoption date, entry point, maintenance wording and instruction routing.
Do not re-adopt, copy the helper into the project, add competing rules, create
an empty journal or log the setup itself. An identical repeat setup makes no edits.
Audit-only requests do not enable, migrate or write logs.

To disable, change only `Event journal: jsonl` to `Event journal: off`; retain the
directory setting and every existing record. Disabling logging does not disable
Markdown maintenance. An off setting takes precedence over an old enablement note.
Conflicting active settings need resolution before capture, not an assumed choice.

## Optional auto preference

A user can select `Context Docs logging preference: auto` in a task request or
already loaded personal/project instructions. This is an opt-in fallback, not
`Event journal: auto` and not a global enable switch. With no preference, logging
stays off. Do not edit personal instructions just to persist a task preference.

During adoption or authorized maintenance, resolve existing project settings
first. Explicit `jsonl`, `off`, or another logging method takes precedence; preserve
its directory and history without probing Git. Resolve conflicting settings or
preferences before enabling anything. Audits remain read-only and never apply
this preference. Skill installation alone does not apply it.

Only when the preference is `auto` and no project setting exists, run the packaged
[read-only policy helper](../scripts/journal_policy.py):

```sh
python3 /path/to/installed/context-docs/scripts/journal_policy.py --project /path/to/project --preference auto
```

Use the actual project root. The helper asks Git about repository membership,
including parent repositories, worktrees and bare repositories. It removes shell
Git redirection variables and uses English diagnostics to distinguish confirmed
absence from errors. Missing Git/Python, permission errors, broken repositories,
timeouts or unrecognized results leave logging unchanged; report detection as
unconfirmed rather than treating failure as absence. Do not fall back to testing
for a `.git` directory.

On `action: enable`, merge `Event journal: jsonl` and the existing or requested
journal directory (default `.context/events`) into the loaded project maintenance
section using the preservation rules above. Report that auto enabled it because
Git confirmed no repository. Do not create a journal or event for setup. On
`action: none`, make no logging-setting edits. An existing explicit setting can
also be passed as `--setting off` or `--setting jsonl`; `action: preserve` requires
no Git probe or edits. The helper only returns a decision; the skill applies it.

Once saved, `Event journal: jsonl` is a project setting: adding Git later does not
disable it or delete records. A later request to disable changes it to `off`.
The auto preference does not authorize commits, publication or background capture.
Projects without Git may already have sufficient Markdown history; this preference
is a convenience, not evidence that they require another log.

## Capture during maintenance

When enabled, record meaningful check results, failures, decisions or corrections
as the evidence becomes available. Skip repetitive progress, routine reads,
no-change maintenance, setup and restatements of already recorded events. Do not
add a second summary event merely to announce that the first was written. Keep
current Markdown focused; link historical detail rather than copying the log into
it. Record only the facts needed to understand the event, with their qualifications.

Use the [packaged helper](../scripts/event_journal.py) from this installed skill,
not a path to the development repository. Python 3.9+ and its standard library
are needed only for this optional command. Resolve the skill directory from the
loaded skill's location. From the project root, use its script with the configured
journal directory, a unique session ID, and one JSON payload:

```sh
python3 /path/to/installed/context-docs/scripts/event_journal.py \
  --directory .context/events append --session session-unique-id --input event-input.json
```

Omit `--input` to supply JSON on stdin. Keep temporary payloads outside the journal;
reuse/remove them only when safe. Only JSONL history belongs in the journal directory.
Use a unique session ID per working session (1–80 ASCII letters, digits, `_` or `-`,
starting with a letter/digit). Reuse it for that session's distinct events. The
helper generates event IDs and recording timestamps; include an earlier event's
actual observation date in its summary when relevant.

### Payload, schema version 1

| Field | Meaning |
| --- | --- |
| `type` | `verification`, `decision`, `contradiction` or `context_update` |
| `status` | `observed`, `approved`, `proposed`, `unknown` or `superseded`; this is statement status, not pass/fail |
| `actor` | The recorder, such as `Claude Code` or `Codex`; name other participants in summary/authority |
| `summary` | Compact factual event with scope, qualifications and relevant observation date |
| `sources` | Nonempty array of evidence references: output paths, source locations or identifiable owner messages |
| `revision` | Source revision qualified for uncommitted changes, a snapshot reference, `unavailable (no Git)` or `unknown`; do not imply HEAD covers uncommitted facts |
| `authority` | Required for approved statements: approving person/role and approval source |
| `check` | Required for verification: object with nonempty `command`, `scope`, `result` strings |
| `supersedes` | Optional UUID of an earlier record being corrected |

All listed fields except `authority`, `check` and `supersedes` are required.
Do not supply the generated `schema_version`, `event_id`, `recorded_at` or
`session_id`. Extra fields are rejected. Sources and authority are caller claims,
not independently validated facts. Distinguish checks actually run from supplied
outcomes; the helper does not execute the command named in `check` or copy evidence.
Retain important transient output when its summary/source would otherwise be lost.

A successful append exits zero and prints the stored event. An error may follow
bytes already written; inspect the selected session before retrying. Retrying an
append is not idempotent. Repeated setup or maintenance with no new event should
not append anything. Report a missing helper/runtime or capture failure honestly;
continue authorized Markdown maintenance without claiming an unrecorded success.
When requested capture fails, retain a concise capture-gap note in the affected
existing Markdown: the unrecorded or unconfirmed event, the observed failure
reason and its date or source. This preserves why the gap occurred for a later reader; a final chat
report alone may not survive. Describe the failure as historical if the helper
later becomes available. Audits do not backfill or clear that note.

## Investigation and preservation

Read the relevant session on demand using the same installed script:

```sh
python3 /path/to/installed/context-docs/scripts/event_journal.py \
  --directory .context/events read --session session-unique-id
```

Omit `--session` to read all session files; `--type verification` filters output
after validation. Reads write nothing and fail on missing or malformed history.
Records are in append order within a session and filename order across sessions,
not global chronological order. Recording timestamps are not observation times.

Correct a record by appending a new one with `supersedes`; retain the original.
The helper checks reference syntax, not existence or an authoritative current
view. Old guidance does not become current merely because it appears in a log.
Audits may investigate history but never append, repair or clean it up.

Each session has its own JSONL file and cooperative exclusive writer lock.
Append validates the existing session, writes, flushes and fsyncs. A killed writer
may leave a lock or partial tail; do not silently truncate history, steal a lock
or retry endlessly. Preserve the file and report the failure. After confirming
no writer remains, an authorized repair can remove the stale lock or start a
new session while retaining damaged evidence outside the scanned directory.
Writes are not transactional with Markdown edits; external editors can bypass
the lock. Large session files cost more to append because validation scans them.

Starting a new session provides rotation. There is no automatic retention or
deletion. Preserve records when disabling or upgrading, and apply only an explicit
project retention policy. Logs are evidence, not disposable caches or backups.
