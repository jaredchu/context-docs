# Context

## Approved decisions and scope
Owner Mira approved retry=3 for local checks on 2026-09-01 to bound memory use. Source: synthetic-owner:D0. This local-check decision remains preserved; the later staging approval has a different scope.

Owner Mira approved retry=5 only for staging on 2026-09-26 09:20Z because retry=10 risks exceeding the memory budget. Source: synthetic-event:E3. The retry=10 developer proposal at 09:10Z was not owner-approved (synthetic-event:E2).

## Current state
settings.json contains retry=5 and scope=staging, consistent with E3. The previous current-state text (retry=3, local checks only, no staging result) is stale; it is retained as historical evidence in events. There is no Git repository; revision is unavailable.

## Verification evidence
Supplied evidence, not checks executed during this maintenance:
- 2026-09-26 09:00Z: operator ran export-check in staging at retry=3; exit 7, queue overflow. No production run. Source: synthetic-event:E1.
- 2026-09-26 09:20Z: following staging approval, operator ran export-check in staging at retry=5; passed. No numeric exit code supplied. Source: synthetic-event:E3.

## Unknowns and follow-up
Production behavior, validation, and rollout remain unknown. Staging approval and a staging pass do not establish production approval or readiness. Preserve the local memory-bound rationale and staging-only scope in further work; obtain production evidence and authorization before treating production as validated or approved.

## History
Event history is in events; it preserves the supplied event times, proposal, approval, check outcomes, and stale-state discrepancy.
