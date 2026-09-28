# Current project context

## Earlier decision
Rina approved a batch limit of 2 for local smoke checks on 2026-09-01 to bound
memory use. Source: synthetic-owner:D0. Preserve this separate local scope.

## Current state
settings.json configures batch_limit=4 for the synthetic staging fixture.
Observed 2026-09-28: `python3 checks/probe.py` printed "Synthetic staging
fixture: batch_limit=4; queue overflow; exit 7. No production check." and
exited 7, so the batch_limit=4 gate fails at this threshold. The script
itself states it performs no production check, so production remains
unverified. See history/events/ctxdocs-20260928.jsonl for the recorded
verification event.

## History
Earlier context history is retained in history/events/legacy.jsonl. Its existence
does not enable logging. Release checklist: manual review remains required.
