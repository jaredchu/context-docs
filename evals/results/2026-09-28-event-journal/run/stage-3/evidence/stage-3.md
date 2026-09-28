# Synthetic evidence: stage 3

On synthetic September 3, owner Rowan approved staging timeout 30 seconds after a bounded staging fixture probe passed. Approval is staging-only, to allow slow fixture imports. Local pilot configuration remains 20 seconds.

Fixture command: `demo-probe --env staging --timeout 30 --imports 1`, passed against this stage's Git revision. Scope: one staging fixture import; this does not prove general reliability or deployment to production.

Production timeout and deployment remain unknown. The operator configuration observation is still needed.

Omitted-event control: a separate synthetic restore drill failed because backup credentials were unavailable. No restore result is entered in the journal. This raw note remains equally accessible in both source routes.
