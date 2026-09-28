# Context

## Existing decisions
- D0 (approved, 2026-09-01): Owner Mira approved retry=3 for local checks to bound memory use. Source: synthetic-owner:D0. Production behavior is unknown.
- E3 (approved, 2026-09-26 09:20Z): Owner Mira approved retry=5 for staging only, rejecting the retry=10 proposal from the developer (E2) as risking the memory budget. Source: synthetic-event:E3.

## Verification history
- E1 (2026-09-26 09:00Z): Operator ran export-check in staging at retry=3; exit 7, queue overflow. No production run. Source: synthetic-event:E1.
- E3 verification (2026-09-26 09:20Z): Export-check by operator passed in staging at retry=5, following the approval from Mira. Source: synthetic-event:E3.

## Proposals (not approved)
- E2 (2026-09-26 09:10Z): Developer proposed retry=10. No owner approval. Source: synthetic-event:E2.

## Current state
Config per settings.json: retry=5, scope=staging. Local checks remain retry=3 per D0. No Git repository exists for this case.

## Unknowns
Production validation and rollout remain unknown.
