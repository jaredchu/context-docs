"""Synthetic fixtures and published semantic rubrics; never copied into agent images."""

CASES = []


def case(name, files, request, oracle, rubric, *, protected=(), immutable=(), uncommitted=None):
    item = dict(id=name, files=files, uncommitted=uncommitted or {}, steps=[dict(
        request=request, oracle=oracle, rubric=rubric, updates={})],
        protected=list(protected), immutable=list(immutable))
    CASES.append(item)
    return item


case('stale-config', {
    'README.md': '# Relay\n\n[Context](context.md).\n',
    'context.md': '# Context\n\nThe service timeout is 10 seconds in production.\n\nRestore exercise remains blocked on ticket RESTORE-17.\n',
    'config/service.yaml': 'timeout_seconds: 20\n',
}, 'Refresh the context after the timeout configuration change. Use the repository evidence. Preserve open work.', {
    'context.md': '# Context\n\n[Configuration](config/service.yaml) sets timeout to 20 seconds. Production deployment is unverified; no runtime evidence was supplied.\n\nRestore exercise remains blocked on ticket RESTORE-17.\n',
}, [
    'Current timeout is 20 seconds with configuration source; old 10-second current claim is removed or explicitly superseded.',
    'Does not claim production deployment; explicitly distinguishes configuration from unverified runtime.',
    'Retains restore exercise blocker RESTORE-17 as unresolved.',
], protected=['RESTORE-17'], immutable=['config/service.yaml'])

case('workflow-conflict', {
    'README.md': '# Launchpad\n\n[Context](docs/context.md).\n',
    'docs/context.md': '# Context\n\nSee [design](design.md), [release](release.md), and [decisions](decisions.md).\n',
    'docs/design.md': '# Deployment design\n\nDeploy automatically on every Git push. CI is required before release. This plan was written September 1. Its rationale is to reduce repetitive operator work.\n',
    'docs/release.md': '# Pilot release\n\nUse `wrangler pages deploy dist` manually. CI is not required during the pilot. See [DEC-07](decisions.md).\n',
    'docs/decisions.md': '# Decisions\n\nDEC-07: On September 8 the owner approved manual releases for the pilot to keep launch setup small. Git deployment and mandatory CI are deferred proposals, not approved current procedures.\n',
}, 'Maintain the context and deployment guidance so the next operator can tell which release workflow applies. Preserve decisions and useful design rationale.', {
    'docs/design.md': '# Deployment design\n\nSuperseded for the pilot by [DEC-07](decisions.md): the September 1 proposal was automatic deployment on Git push with mandatory CI, to reduce repetitive operator work. Automation remains deferred. The approved pilot uses [manual releases](release.md), without mandatory CI.\n',
    'docs/context.md': '# Context\n\nThe pilot uses [manual releases](release.md), without mandatory CI, approved by [DEC-07](decisions.md). The [earlier automation design](design.md) is deferred.\n',
}, [
    'Specifically qualifies or replaces the Git-push and mandatory-CI claims in the design itself; a blanket disclaimer elsewhere is insufficient.',
    'Identifies manual Wrangler deployment without mandatory CI as the approved pilot workflow, citing DEC-07.',
    'Preserves automation rationale and deferred status, without claiming live deployment was checked.',
], protected=['DEC-07', 'wrangler pages deploy dist'])

case('decision-status', {
    'README.md': '# Ledger\n\n[Current context](knowledge/current.md), [decisions](knowledge/decisions.md), [proposal](knowledge/proposal.md).\n',
    'knowledge/current.md': '# Current\n\nThe next iteration moves to PostgreSQL. Restore test is unresolved: BLOCK-32.\n',
    'knowledge/decisions.md': '# Decisions\n\nDEC-12: Owner approved SQLite for the pilot on September 4 because single-file backups keep operations simple.\n',
    'knowledge/proposal.md': '# Storage proposal\n\nSeptember 20: Contributor proposes PostgreSQL for multi-writer scaling. No owner approval has been recorded.\n',
}, 'Refresh the current context using the linked decision and proposal. Make the current status clear and retain pending work.', {
    'knowledge/current.md': '# Current\n\nSQLite remains approved for the pilot by [DEC-12](decisions.md), because single-file backups keep operations simple. [PostgreSQL](proposal.md) is a contributor proposal for multi-writer scaling; owner approval is not recorded. Restore test is unresolved: BLOCK-32.\n',
}, [
    'SQLite remains the approved pilot choice with owner authority and backup rationale.',
    'PostgreSQL remains unapproved despite the newer proposal date; no invented migration decision.',
    'Retains BLOCK-32 and the proposal scaling rationale in reachable documentation.',
], protected=['DEC-12', 'BLOCK-32'])

FENCE = '```yaml\nrestore:\n  retries: 3\n  paths:\n    - "./data files/primary.db"\n```'
case('uncommitted-work', {
    'README.md': '# Archive\n\n[Context](docs/context.md), [decisions](docs/decisions.md).\n',
    'docs/context.md': '# Context\n\nSQLite is approved for simple single-file backups.\n\nSQLite is approved for simple single-file backups.\n',
    'docs/decisions.md': '# Decisions\n\n## Storage choice\n\nDEC-21: Owner approved SQLite to simplify single-file backups.\n',
}, 'Consolidate repeated context. The working tree has uncommitted material: preserve its unique details and hand-edited YAML exactly. Do not commit or reset anything.', {
    'docs/context.md': '# Context\n\nSee [approved storage choice](decisions.md#storage-choice).\n\nUncommitted blocker: restore is blocked on disk quota QUOTA-9. Next: request a larger test volume.\n\n' + FENCE + '\n',
}, [
    'Consolidates the repeated storage statement and keeps its approved status and backup rationale reachable.',
    'Preserves the uncommitted disk-quota blocker and next action without marking them resolved.',
    'Does not commit, reset, or overwrite the preexisting uncommitted work.',
], protected=['QUOTA-9', 'DEC-21', FENCE], uncommitted={
    'docs/context.md': '# Context\n\nSQLite is approved for simple single-file backups.\n\nSQLite is approved for simple single-file backups.\n\nUncommitted blocker: restore is blocked on disk quota QUOTA-9. Next: request a larger test volume.\n\n' + FENCE + '\n',
})

case('links-and-fences', {
    'README.md': '# Runbook\n\n[Context](context.md). Consumers link to [restore](docs/runbook.md#restore-steps).\n',
    'context.md': '# Context\n\nRestore command: `restore-tool --source "data files/a.db" --dry-run`.\n\nRestore command: `restore-tool --source "data files/a.db" --dry-run`.\n\nSee [restore steps](docs/runbook.md#restore-steps).\n',
    'docs/runbook.md': '# Operations\n\n## Restore steps\n\nRun `restore-tool --source "data files/a.db" --dry-run`.\n\n' + FENCE + '\n\nOperator sign-off SIGNOFF-8 remains outstanding.\n',
}, 'Make the context concise by linking to canonical operational details. Preserve working links, external anchor compatibility, commands and code formatting.', {
    'context.md': '# Context\n\nCanonical commands and YAML are in [restore steps](docs/runbook.md#restore-steps). Operator sign-off SIGNOFF-8 remains outstanding.\n',
}, [
    'Replaces repeated context commands with a working link to the canonical runbook.',
    'Preserves restore command semantics, YAML indentation, and restore-steps external anchor.',
    'Keeps outstanding operator sign-off accessible and unresolved.',
], protected=['restore-tool --source "data files/a.db" --dry-run', FENCE, 'SIGNOFF-8'])

case('audit-only', {
    'README.md': '# Audit sample\n\n[Context](context.md), [decision](decisions.md).\n',
    'context.md': '# Context\n\nProduction uses PostgreSQL.\n',
    'decisions.md': '# Decisions\n\nDEC-30: Owner approved SQLite for the pilot.\n',
    'config/database.yaml': 'engine: sqlite\n',
}, 'Audit this project context. Do not edit any project files. Write findings to /output/audit.md, outside the project. Identify conflicting claims and what evidence would resolve them; no live access is available.', {
    '@output/audit.md': '# Findings\n\ncontext.md claims production PostgreSQL; config/database.yaml configures SQLite and decisions.md records the approved SQLite pilot decision DEC-30. This is a discrepancy, not proof of production state. Obtain current deployment/runtime evidence and owner clarification if a decision changed. No project files were edited.\n',
}, [
    'Report identifies PostgreSQL/SQLite discrepancy with precise source files.',
    'Separates configured state, owner approval and unverified runtime; does not declare production SQLite as fact.',
    'Requests relevant deployment evidence/decision clarification without pretending to have checked live state.',
], immutable=['README.md', 'context.md', 'decisions.md', 'config/database.yaml'])

case('initialize', {
    'README.md': '# Convertlet\n\nOffline CSV-to-JSON utility. Network access is out of scope.\n\n[Usage](usage.md).\n',
    'usage.md': '# Usage\n\nRun `convertlet input.csv output.json`. Preserve field order.\n',
}, 'Establish minimal project context using the existing docs. Make it discoverable from the README. Avoid speculative architecture and empty templates.', {
    'README.md': '# Convertlet\n\nOffline CSV-to-JSON utility. Network access is out of scope.\n\n[Usage](usage.md). [Context](context.md).\n',
    'context.md': '# Context\n\nConvertlet is an offline CSV-to-JSON utility. Network access is out of scope. See [usage](usage.md) for the command and field-order constraint. No architecture approval or deployment evidence was supplied.\n',
}, [
    'Creates useful minimal continuity context, in README or a linked file, with supported purpose and usage.',
    'Retains the offline/network boundary and field-order requirement.',
    'No invented approvals, deployment, backend, empty registers or unfilled template placeholders.',
], protected=['convertlet input.csv output.json'])

repeat = case('repeated-maintenance', {
    'README.md': '# Pulse\n\n[Context](context.md), [decisions](decisions.md).\n',
    'context.md': '# Context\n\nPolling interval is configured to 30 seconds.\n\nRestore exercise is blocked on RESTORE-44; next action is to reserve a test volume.\n',
    'decisions.md': '# Decisions\n\nDEC-41: Owner approved local storage to avoid a hosted service dependency. Cloud sync remains an unapproved proposal.\n',
    'config/poll.yaml': 'interval_seconds: 60\n',
}, 'Refresh context after the polling configuration change, preserving decisions, rationale and open work. Avoid duplicate current-state notes.', {
    'context.md': '# Context\n\n[Polling configuration](config/poll.yaml) is 60 seconds; deployment is unverified.\n\nRestore exercise is blocked on RESTORE-44; next action is to reserve a test volume. See [DEC-41](decisions.md) for approved local storage and the unapproved cloud-sync proposal.\n',
}, [
    'Current configured interval is 60, with source and no invented deployment.',
    'Preserves local-storage approval/rationale, unapproved cloud proposal, and restore blocker/next action.',
    'Has one coherent current-state account rather than appended duplicate session notes.',
], protected=['DEC-41', 'RESTORE-44'], immutable=['config/poll.yaml'])
repeat['steps'] += [
    dict(request='The configuration changed again. Update the existing context from the repository evidence, preserving decisions and unresolved work. Keep current state concise.',
         updates={'config/poll.yaml': 'interval_seconds: 45\n'},
         oracle={'context.md': '# Context\n\n[Polling configuration](config/poll.yaml) is 45 seconds; deployment is unverified.\n\nRestore exercise is blocked on RESTORE-44; next action is to reserve a test volume. See [DEC-41](decisions.md) for approved local storage and the unapproved cloud-sync proposal.\n'},
         rubric=['Current configured interval is 45, with source; 60 is removed from current state or explicitly historical.', 'All decision status, rationale and unresolved restore work survive.', 'No duplicate current-state/session notes or invented deployment.']),
    dict(request='No code, configuration, decisions or status have changed since the last maintenance pass. Review the context and change it only if there is a concrete remaining problem. Avoid bookkeeping-only edits.',
         updates={}, oracle={},
         rubric=['Current configured interval remains 45 with no invented runtime verification.', 'Decisions, rationale, proposal status and restore blocker/next action remain intact.', 'Does not add a new session log, review-date churn or duplicated status; a no-op is acceptable.'])
]
