# Maple working context

## Intent
Prepare the config migration for maintainer review. Completion requires the backward-compatibility check and the interrupted-write check to pass. Deployment needs separate owner approval.

## Work
```text
Goal: config migration ready for maintainer review (incomplete) [I]
|-- DONE     Backward-compatibility check passed October 15 [C]
`-- BLOCKED  Interrupted-write check has not run [W]
    `-- NEXT Obtain the missing interruption fixture, then run the check [N]

Outside completion path: deployment needs separate owner approval [I] [D]
```

Sources: [I] [Intent](#intent); [C] [compatibility result](results.md#compatibility); [W] [interrupted-write result](results.md#interrupted-write); [N] [Next move](#next-move); [D] [owner decision](decisions.md#owner-decision).

Owner note: keep the migration example in this file.

Example: existing `mode=plain` config must remain accepted.

## Decision trail
The owner approved retaining the existing config format for old clients. See [decisions](decisions.md).

## Next move
Obtain the interruption fixture, then run the interrupted-write check.
