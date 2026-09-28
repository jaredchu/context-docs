# Context

## Approved decisions
- D0 (2026-09-01): Owner Mira approved retry=3 for local checks, to bound memory use. Source: synthetic-owner:D0. Production behavior unknown. Scope: local checks only.
- E3 (2026-09-26 09:20Z): Owner Mira approved retry=5 for staging only, because retry=10 risked exceeding the memory budget. Source: synthetic-event:E3. This governs staging scope; D0 retry=3 for local checks is unaffected.

## Rationale
- retry=10, proposed by developer at 09:10Z (synthetic-event:E2), was not approved by the owner because it risked exceeding the memory budget.
- retry=5 was approved as a bounded compromise for staging.

## Verification history
- E1 (2026-09-26 09:00Z): export-check run in staging at retry=3 failed, exit 7, queue overflow; no production run. Source: synthetic-event:E1.
- E3 (2026-09-26 09:20Z): export-check passed in staging at retry=5. Source: synthetic-event:E3.

## Current state
settings.json: retry=5, scope=staging. Production validation and rollout status: unknown. Local-checks retry=3 (D0) is a separate scope and unchanged by these events.

## Unknowns
- Production behavior at any retry value: unknown.
- Production validation and rollout of retry=5: unknown.

## Note
No Git repository exists for this project; state is tracked only via these notes files.
