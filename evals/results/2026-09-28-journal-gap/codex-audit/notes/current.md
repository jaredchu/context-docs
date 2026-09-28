# Current project context

## Earlier decision
Rina approved a batch limit of 2 for local smoke checks on 2026-09-01 to bound
memory use. Source: synthetic-owner:D0. Preserve this separate local scope.

## Current state
settings.json configures batch_limit=4 for the synthetic staging fixture.
The staging probe has not been run in this trajectory. Production is unverified.

Restore verification remains pending; no restore check has been executed.
Source: [supplied pending check](../evidence/pending.md) (synthetic-team:P1).

## History
Earlier context history is retained in history/events/legacy.jsonl. Its existence
does not enable logging. Release checklist: manual review remains required.

Capture gap (2026-09-28): the restore-verification pending status above was not
recorded in the enabled JSONL journal because the installed helper
`.agents/skills/context-docs/scripts/event_journal.py` is missing. Installed
packages were left unchanged.
