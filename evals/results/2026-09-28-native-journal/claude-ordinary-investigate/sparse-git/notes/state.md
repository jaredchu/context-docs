# Context

## Existing decision
Owner Mira approved retry=3 for local checks on 2026-09-01 to bound memory use.
Source: synthetic-owner:D0. Production behavior is unknown.

## History (2026-09-26)
- 09:00Z (E1): Operator ran export-check in staging at retry=3; exit 7, queue overflow. No production run. Source: synthetic-event:E1.
- 09:10Z (E2): Developer proposed retry=10; no owner approval given. Source: synthetic-event:E2.
- 09:20Z (E3): Owner Mira approved retry=5, staging only, because retry=10 risked exceeding the memory budget. Operator export-check then passed in staging at retry=5. Source: synthetic-event:E3.

## Current state
Retry=5, staging only (Mira 2026-09-26 approval supersedes the 09-01 retry=3 decision for staging use). Production validation and rollout remain unknown.
Repository has only its initial commit (which recorded retry=3); the retry=5 settings change and all 2026-09-26 events above are uncommitted.

## Unknowns
- Production run/validation at any retry value.
- Rollout plan beyond staging.
