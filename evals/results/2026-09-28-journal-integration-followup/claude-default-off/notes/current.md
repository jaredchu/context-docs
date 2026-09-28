# Current project context

## Earlier decision
Rina approved a batch limit of 2 for local smoke checks on 2026-09-01 to bound
memory use. Source: synthetic-owner:D0. Preserve this separate local scope.

## Current state
settings.json configures batch_limit=4 for the synthetic staging fixture.
The staging probe has not been run in this trajectory. Production is unverified.

## History
Earlier context history is retained in history/events/legacy.jsonl. Its existence
does not enable logging. Release checklist: manual review remains required.
