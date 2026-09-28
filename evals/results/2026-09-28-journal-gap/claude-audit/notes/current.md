# Current project context

## Earlier decision
Rina approved a batch limit of 2 for local smoke checks on 2026-09-01 to bound
memory use. Source: synthetic-owner:D0. Preserve this separate local scope.

## Current state
settings.json configures batch_limit=4 for the synthetic staging fixture.
The staging probe has not been run in this trajectory. Production is unverified.

## Open questions and next actions
Restore verification is still pending; no restore check has been executed.
Source: synthetic-team:P1 (evidence/pending.md). Next action: run and record
the restore check before treating restore capability as verified.

## History
Earlier context history is retained in history/events/legacy.jsonl. Its existence
does not enable logging. Release checklist: manual review remains required.

Capture gap (2026-09-28): the context_update event for the restore-verification
item above could not be appended to history/events. CLAUDE.md configures the
event journal (jsonl, history/events), but this project's installed context-docs
skill has no scripts/event_journal.py helper — confirmed by direct invocation,
which exited 2 with "No such file or directory". Retry recording this event once
the helper is installed; this note preserves the gap in the meantime.
