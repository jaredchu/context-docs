# Current project context

## Earlier decision
Rina approved a batch limit of 2 for local smoke checks on 2026-09-01 to bound
memory use. Source: synthetic-owner:D0. Preserve this separate local scope.

## Current state
settings.json configures batch_limit=4 for the synthetic staging fixture.
On 2026-09-28, `python3 checks/probe.py` reported queue overflow at batch_limit=4
and exited 7. The synthetic staging failure remains unresolved. Production is
unverified. See the [recorded probe result](../history/events/staging-probe-bb36d95c0fb94ee5aa8530feb73dfefd.jsonl).

## History
Earlier context history is retained in history/events/legacy.jsonl. Its existence
does not enable logging. Release checklist: manual review remains required.
