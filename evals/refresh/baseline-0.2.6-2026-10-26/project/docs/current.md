# Parcel Relay context

## Goal

Prepare the pilot worker for a maintainer handoff while keeping the legacy reader
compatible. Deployment needs a separate maintainer decision.

## Current state

The [local worker configuration](../config/worker.json) sets a 30-second timeout,
two retries and the `legacy-v1` recovery format. The retry setting does not match
the approved [retry decision](decisions.md#retry-budget): Mira approved four
retries to tolerate transient offline failures. That approval remains in force;
completion of the approved retry change is not established by the current evidence.

The supplied October 22, 2026 [check evidence](../evidence/local-check.md) reports
that the isolated timeout configuration check passed for one example job using
the 30-second timeout and two retries. It does not verify retry-limit behavior,
restore compatibility or the full test suite. No deployment occurred in that
check, and deployed behavior remains unknown; no staging or production behavior
was observed.

## Progress

```text
Goal: prepare a compatible pilot handoff
├─ DONE     Local timeout configuration check for one example job
├─ PENDING  Align retry configuration with approved four; verify behavior
└─ BLOCKED  Restore verification: missing legacy reader fixture
NEXT: resolve the retry mismatch; obtain the legacy reader fixture,
      then run the restore check.
```

Sources: [configuration and check scope](#current-state),
[retry approval](decisions.md#retry-budget), and
[restore dependency](#blocker-and-next-action).

## Blocker and next action

Align the retry configuration with the approved four-retry budget and verify
retry-limit behavior.

Restore verification is blocked by the missing legacy reader fixture. Leena will
supply that fixture; then the maintainer can run the restore check. Keep the
compatibility constraint from [the storage decision](decisions.md#storage-envelope).

## Earlier status

Earlier claims of a 10-second timeout, a pending local timeout check and completed
four-retry implementation are superseded by the [current evidence](#current-state).

## Working note

Uncommitted operator note: retain the recovery envelope until the restore fixture
exists; the legacy reader cannot parse a bare payload.

```yaml
recovery_envelope:
  format: legacy-v1
  retain_until: restore-fixture-verified
```
