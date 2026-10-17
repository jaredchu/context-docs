# Harbor cache context

## Goal
Prepare the cache retry results for release review. Release needs Noor's approval.

## Progress
The cache was reset before the retry. The record does not identify who reset it. The retry passed only on the small dataset. Release is still blocked because the large-dataset result has not been recorded. If that check passes, ask Noor for release approval; that approval has not been given. A switch from SQLite to Postgres remains undecided. Evidence: [small retry](checks.md#small); decision: [storage](decisions.md#storage).

## Decisions
Keep SQLite until measured needs justify a change, to avoid an unproven migration cost. A switch to Postgres remains undecided. Noor has not approved release. See [storage rationale](decisions.md#storage).

## Next action
Obtain the large-dataset result. Its absence does not establish failure. If the check passes, ask Noor for release approval. Do not treat the passing check as that approval. See [large retry](checks.md#large).

## Owner note
Owner wording: retain `cache_mode=normal`; do not polish this note.
