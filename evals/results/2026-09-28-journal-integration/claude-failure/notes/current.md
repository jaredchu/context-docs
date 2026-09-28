# Current project context

## Earlier decision
Rina approved a batch limit of 2 for local smoke checks on 2026-09-01 to bound
memory use. Source: synthetic-owner:D0. Preserve this separate local scope.

## Current state
settings.json configures batch_limit=4 for the synthetic staging fixture.
Ran `python3 checks/probe.py` on 2026-09-28: it read batch_limit=4 and exited 7
with "queue overflow" (Source: checks/probe.py run output). Production is unverified;
the probe itself states it performs no production check.

## History
Earlier context history is retained in history/events/legacy.jsonl. Its existence
does not enable logging. Release checklist: manual review remains required.
