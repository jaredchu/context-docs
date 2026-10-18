# Cedar context

## Goal
Prepare the CSV export for owner review after schema, sample and empty-input verification.

## Current work
Schema review is complete. Sample verification is pending. Empty-input verification
is blocked by a missing fixture; do not infer it passed. See [checks](checks.md#initial-checks).

## Decisions
Keep semicolon-separated output for compatibility with the owner's importer.
This is an owner decision, not an agent proposal. See [decision](decision.md#format).

## Owner note
Keep the owner review gate; this work does not authorize deployment.

## Next action
Verify sample exports, then obtain the missing empty-input fixture.
