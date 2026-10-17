# Cedar working context

## Goal
Prepare profile import for owner review. Completion requires format compatibility and duplicate-name checks to pass. Deployment is separate and requires owner approval.

## Work
- Prepare profile import for owner review:
  - DONE: [Format compatibility passed](evidence.md#format-compatibility).
  - BLOCKED: [Duplicate-name check has not run; its representative fixture is missing](evidence.md#duplicate-names).
    - NEXT: obtain the fixture, then run the check.

Owner note: keep the `mode=plain` example here.

Example: older profiles containing `mode=plain` must remain accepted.

## Decisions
The owner approved keeping the existing profile format for older clients. A proposed binary format is not approved. Whether to add export support is undecided and outside the import-review goal. See [decision rationale](decisions.md).

## Next move
Obtain the duplicate-name fixture, then run the check. Deployment is not approved.
