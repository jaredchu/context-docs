# Maple working context

## Intent
Prepare the config migration for maintainer review. Completion requires the backward-compatibility check and the interrupted-write check to pass. Deployment needs separate owner approval.

## Work
- [x] Backward-compatibility check — passed October 15; see the [retained compatibility result](results.md#compatibility).
- [x] Interrupted-write check — passed October 16; see the [retained interrupted-write result](results.md#interrupted-write).
- **NEXT:** [Maintainer review](#next-move).

Owner note: keep the migration example in this file.

Example: existing `mode=plain` config must remain accepted.

## Decision trail
The owner approved retaining the existing config format for old clients. See [decisions](decisions.md).

## Next move
Both documented checks have passed; proceed to maintainer review. Deployment still requires separate owner approval.
