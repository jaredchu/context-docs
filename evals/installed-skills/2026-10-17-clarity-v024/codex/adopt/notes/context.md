# Harbor export context

## Goal
Prepare CSV export for owner review. Deployment needs separate approval.

## Progress
Export verification passed for two sample files on October 12. The full suite was not run. Evidence: [sample export](checks.md#sample-export).

Mira approved keeping CSV so older clients still work. This does not approve deployment. JSON support remains a proposal. See [CSV](decisions.md#csv).

The empty-input check is blocked by its missing fixture. Its outcome is still unknown. See [empty input](checks.md#empty-input).

## Decisions
Mira approved retaining CSV for compatibility with older clients. JSON support is proposed, not approved. Deployment approval has not been given. See [CSV decision](decisions.md#csv).

## Next action
When the empty-input fixture becomes available, run its check. The missing fixture currently blocks the check. No result exists yet; this does not mean the check failed. See [empty input](checks.md#empty-input).

## Owner note
Owner wording: keep `format=csv`; do not polish this note.
