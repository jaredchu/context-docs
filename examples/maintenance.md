# Maintenance example

Synthetic, authored example. This illustrates intended behavior; it is not an
independent agent evaluation or a claim about token savings.

## Request and evidence

The user asks to update project context after changing the configured request
timeout from 10 to 20 seconds. The current `config/service.yaml` says
`timeout_seconds: 20`. No deployment evidence is available. The owner previously
approved retaining SQLite for the pilot; PostgreSQL remains a suggestion. A
restore test is still blocked on obtaining a representative synthetic dataset.

## Before: existing context.md

```markdown
# Example service context

The request timeout is 10 seconds.

Approved: keep SQLite for the pilot to avoid migration work (owner, September 1).
Proposed: evaluate PostgreSQL after the pilot.

September 2: still using SQLite.
September 3: confirmed that SQLite remains in use.

Restore testing is blocked on a representative synthetic dataset.
Next: prepare that dataset and run the restore procedure.
```

## After: same context.md

```markdown
# Example service context

## Current state

As of September 26, the configured request timeout is 20 seconds
(`config/service.yaml`). Deployment of this change is unverified.

## Decisions

Approved: keep SQLite for the pilot to avoid migration work
(owner, September 1). Proposed: evaluate PostgreSQL after the pilot.

## Open work

Restore testing is blocked on a representative synthetic dataset.
Next: prepare that dataset and run the restore procedure.
```

The update removes repetitive diary entries and corrects the configuration claim.
It preserves the approval, rationale and blocker. It adds an explicit verification
limit rather than claiming the new value is deployed. The file path stays the
same, and no archive or extra register is needed for these redundant entries.
