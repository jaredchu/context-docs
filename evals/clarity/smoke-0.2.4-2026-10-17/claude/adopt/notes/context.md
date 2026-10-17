# Harbor export context

## Goal
Prepare CSV export for owner review. Deployment needs separate approval.

## Progress
The export verification passed for two sample files on October 12. The full suite was not run. Mira approved keeping CSV so older clients still work; that approval does not approve deployment. JSON support is only a proposal. The next step is to run the empty-input check when its fixture is available. That check's outcome is still unknown. Evidence: [sample export](checks.md#sample-export); decision: [CSV](decisions.md#csv).

## Decisions
Mira approved retaining CSV for compatibility with older clients. JSON support is proposed, not approved. Deployment approval has not been given. See [CSV decision](decisions.md#csv).

## Next action
When the empty-input fixture becomes available, run its check. The missing fixture currently blocks the check. The result is unknown. See [empty input](checks.md#empty-input).

## Owner note
Owner wording: keep `format=csv`; do not polish this note.
