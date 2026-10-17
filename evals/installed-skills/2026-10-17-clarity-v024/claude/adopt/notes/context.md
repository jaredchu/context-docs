# Harbor export context

## Goal
Prepare CSV export for owner review. Deployment needs separate approval.

## Progress
The export verification passed for two sample files on October 12. The full suite was not run. Mira approved keeping CSV so older clients still work; that approval does not cover deployment. JSON support is only a proposal. Next, run the empty-input check when its fixture is available; that check's outcome is still unknown. Evidence: [sample export](checks.md#sample-export); decision: [CSV](decisions.md#csv).

## Decisions
Mira approved retaining CSV for compatibility with older clients. JSON support is proposed, not approved. Deployment approval has not been given. See [CSV decision](decisions.md#csv).

## Next action
Run the empty-input check when its fixture becomes available. The missing fixture currently blocks the check. The result is unknown, which does not mean failed. See [empty input](checks.md#empty-input).

## Owner note
Owner wording: keep `format=csv`; do not polish this note.
