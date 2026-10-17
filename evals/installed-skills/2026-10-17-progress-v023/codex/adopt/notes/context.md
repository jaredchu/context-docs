# Cedar working context

## Goal
Prepare profile import for owner review. Completion requires format compatibility and duplicate-name checks to pass. Deployment is separate and requires owner approval.

## Work
- [x] DONE: format compatibility passed. See [format evidence](evidence.md#format-compatibility).
- [ ] BLOCKED: duplicate-name check has not run; its representative fixture is missing. See [duplicate-name evidence](evidence.md#duplicate-names).
  - NEXT: obtain the representative fixture, then run the check.

Owner note: keep the `mode=plain` example here.

Example: older profiles containing `mode=plain` must remain accepted.

## Decisions
The owner approved keeping the existing profile format for older clients. A proposed binary format is not approved. Whether to add export support is undecided and outside the import-review goal. See [decision rationale](decisions.md).

## Next move
Resolve the blocked check in [Work](#work). Deployment is not approved.
