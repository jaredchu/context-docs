# Synthetic evidence: stage 1

On synthetic September 1, owner Rowan approved changing the local pilot timeout from 10 to 20 seconds to accommodate slow imports. Approval applies only to the local pilot.

Fixture check: `demo-validator config.json` passed against this stage's Git revision. Scope: configuration shape and positive timeout only; no network request or deployment was checked.

The old operations note claims production uses 10 seconds, while local config is now 20. Production access is unavailable; production timeout and deployment remain unknown. Next action: obtain a production configuration observation from the operator.
