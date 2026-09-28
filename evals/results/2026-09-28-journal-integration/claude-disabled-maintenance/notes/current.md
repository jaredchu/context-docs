# Current project context

## Earlier decision
Rina approved a batch limit of 2 for local smoke checks on 2026-09-01 to bound
memory use. Source: synthetic-owner:D0. Preserve this separate local scope.
Reaffirmed unchanged as of 2026-09-28. Source: evidence/approval.md, synthetic-owner:A1.

## Staging batch limit decision
Fixture owner Rina approved batch_limit=6, only for staging, on 2026-09-28,
because larger batches increase peak memory. Source: evidence/approval.md,
synthetic-owner:A1. A developer proposal of batch_limit=12 has no owner approval
(proposed, not current policy). Production validation and rollout are not
approved or established here.

## Current state
settings.json currently configures batch_limit=6, matching the approved staging
limit above (Observed: settings.json). Ran `python3 checks/probe.py` on
2026-09-28 at batch_limit=6: passed, exit 0 (Source: checks/probe.py run output).
The probe itself states it performs no production check; production remains
unverified.

An earlier note recorded a 2026-09-28 probe run reading batch_limit=4 and
exiting 7 with "queue overflow" (Source: checks/probe.py run output). That
reading no longer matches the current batch_limit=6 in settings.json and is
superseded by the current-state observation above; it is retained here as
historical evidence.

## Open questions
Restore verification is still pending; no restore check has been executed.
Source: evidence/pending.md, synthetic-team:P1.

The fixture owner has scheduled the manual review (see release checklist below)
for the next work session. This is a plan, not a completed review; no review has
occurred yet. Source: evidence/followup.md, synthetic-owner:F1.

## History
Earlier context history is retained in history/events/legacy.jsonl. Its existence
does not enable logging. Release checklist: manual review remains required.
