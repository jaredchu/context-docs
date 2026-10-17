# Maple working context

## Intent
Prepare the config migration for maintainer review. Completion requires the backward-compatibility check and the interrupted-write check to pass. Deployment needs separate owner approval.

## Work
Prepare the config migration for maintainer review ([completion conditions](#intent)):

- [x] DONE: Backward-compatibility check passed October 15, 2026 ([result](results.md#compatibility)).
- [x] DONE: Interrupted-write check passed October 16, 2026 after the fixture was provided ([result](results.md#interrupted-write)).

Both documented checks have passed. NEXT: [Maintainer review](#next-move).

These retained results are synthetic observations for a documentation check, not executed application tests. See [retained results](results.md).

Owner note: keep the migration example in this file.

Example: existing `mode=plain` config must remain accepted.

## Decision trail
The owner approved retaining the existing config format for old clients. See [decisions](decisions.md).

## Next move
Maintainer review. Deployment still requires separate owner approval.
