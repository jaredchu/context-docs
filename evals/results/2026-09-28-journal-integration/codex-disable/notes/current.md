# Current project context

## Earlier decision
Rina approved a batch limit of 2 for local smoke checks on 2026-09-01 to bound
memory use. Source: synthetic-owner:D0. Preserve this separate local scope.

## Current state
[settings.json](../settings.json) configures batch_limit=6 for the synthetic staging
fixture. Rina approved this staging-only limit on 2026-09-28 because larger batches
increase peak memory. The developer's proposed limit 12 has no owner approval.
Source: [supplied owner decision](../evidence/approval.md), synthetic-owner:A1.

On 2026-09-28, `python3 checks/probe.py` passed at batch_limit=6 and exited 0.
See the [approval and probe records](../history/events/staging-approved-f60e7d0fe50e4f5696e4e1f9942f5e34.jsonl).
Production remains unverified; production validation and rollout are not approved.

## Pending verification
Restore verification is still pending; no restore check has been executed.
Source: [supplied pending check](../evidence/pending.md), synthetic-team:P1.

## History
The earlier 2026-09-28 probe at batch_limit=4 reported queue overflow and exited 7;
it predates the current passing configuration. Its
[recorded result](../history/events/staging-probe-bb36d95c0fb94ee5aa8530feb73dfefd.jsonl)
is retained as historical evidence.

Earlier context history is retained in history/events/legacy.jsonl. Its existence
does not enable logging. Release checklist: manual review remains required.
