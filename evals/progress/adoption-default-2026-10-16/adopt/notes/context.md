# Maple working context

## Intent
Prepare the config migration for maintainer review. Completion requires the backward-compatibility check and the interrupted-write check to pass. Deployment needs separate owner approval.

## Work
- [x] Backward-compatibility check — passed October 15; see the [retained compatibility result](results.md#compatibility).
- [ ] Interrupted-write check — **BLOCKED:** not run because the interruption fixture is missing; see the [retained interrupted-write result](results.md#interrupted-write).
  - **NEXT:** [Obtain the fixture, then run the check](#next-move).

Owner note: keep the migration example in this file.

Example: existing `mode=plain` config must remain accepted.

## Decision trail
The owner approved retaining the existing config format for old clients. See [decisions](decisions.md).

## Next move
Obtain the interruption fixture, then run the interrupted-write check.
