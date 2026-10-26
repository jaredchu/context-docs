# Parcel Relay context

## Goal

Prepare the pilot worker for a maintainer handoff while keeping the legacy reader
compatible. Deployment needs a separate maintainer decision.

## Current state

The worker is configured with a 10-second timeout in
[worker configuration](../config/worker.json). Retry-limit implementation is
complete at four retries, matching the approved
[retry decision](decisions.md#retry-budget).

The local timeout check is pending. Deployed behavior is unknown; no live-system
evidence is available. [Check evidence](../evidence/local-check.md) owns verification
scope and results.

## Progress

```text
Goal: prepare a compatible pilot handoff
├─ DONE     Retry-limit implementation at four
├─ PENDING  Local timeout check
└─ BLOCKED  Restore verification: missing legacy reader fixture
NEXT: obtain the legacy reader fixture, then run the restore check.
```

## Blocker and next action

Restore verification is blocked by the missing legacy reader fixture. Leena will
supply that fixture; then the maintainer can run the restore check. Keep the
compatibility constraint from [the storage decision](decisions.md#storage-envelope).

## Earlier status

The worker timeout is 10 seconds and the local timeout check is still pending.
Retry-limit implementation at four is complete.
