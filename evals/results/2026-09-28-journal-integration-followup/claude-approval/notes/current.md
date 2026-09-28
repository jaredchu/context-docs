# Current project context

## Earlier decision
Rina approved a batch limit of 2 for local smoke checks on 2026-09-01 to bound
memory use. Source: synthetic-owner:D0. Preserve this separate local scope.

## Current state
Fixture owner Rina approved batch_limit=6, and only for the synthetic staging
scope, because larger batches increase peak memory (evidence/approval.md,
source synthetic-owner:A1, 2026-09-28). The developer's earlier proposal of
batch_limit=12 has no owner approval. settings.json now configures
batch_limit=6 for the synthetic staging fixture, matching that approval.
Observed 2026-09-28: `python3 checks/probe.py` printed "Synthetic staging
fixture: batch_limit=6; passed; exit 0. No production check." and exited 0,
so the gate passes at this threshold. The script itself states it performs
no production check, so production remains unverified; production validation
and rollout are not approved or established. An earlier run against
batch_limit=4 failed this same gate (exit 7); see
history/events/ctxdocs-20260928.jsonl for that superseded verification and
history/events/ctxdocs-20260928-2.jsonl for the current approval and
verification events.

## History
Earlier context history is retained in history/events/legacy.jsonl. Its existence
does not enable logging. Release checklist: manual review remains required.
