# Project context

Release and website verified: 2026-10-11. Historical evaluations were not rerun.
Installed skills and project setup files are unchanged; Wave 1 preparation's
global-state drift is qualified below.

## Purpose and scope

Context Docs helps people without an established context-management practice keep
useful, accurate project knowledge across AI sessions with minimal human effort.
This public repository serves contributors and skill users. Shared context should
retain project decisions, constraints and next actions; incidental personal
installations, backup locations and temporary machine state belong in suitable
local notes only when still useful.

## Decisions

- Keep Markdown/Git authoritative and cloud integrations optional; a hosted service
  needs a concrete use case.
- Select information by audience, destination and lasting usefulness. The agent
  must filter what it writes; publication still requires project authorization.
- Keep logging optional, for efficient event capture and later investigation.
  Local-only context is a concrete use case for retaining significant events as
  current Markdown changes without Git history; complete version recovery still
  needs snapshots or backups.
  Broader integration must meet the [journal requirements](event-journal-pilot.md#requirements-before-broader-integration).
- Prioritize useful, accurate context and reduced human effort. Model speed, token
  use and file length alone do not establish success; outperforming expert
  maintenance is not the product's success gate.
- Credit Claude on every commit it helps implement, validate or review, alongside
  the existing Codex rule. The [attribution policy](../CONTRIBUTING.md#commit-attribution)
  owns trailer formats and preserves human authorship and existing history.
- Use Sol 6.1 for coordination, integration, validation and context maintenance;
  use Opus 5.5 for bounded substantial work, with focused counterpart review for
  consequential changes. Sol inspects returned patches and evidence at important
  boundaries without repeating Opus's work. The
  [collaboration rules](../AGENTS.md#model-collaboration) own the responsibility split,
  assignment and review bounds, and subscription-only access constraints. This
  policy applies only to this project; better quality and reduced ChatGPT allowance
  pressure remain goals to verify, not established benefits.

[Decision history](project-decisions.md) records authority and rationale.
[AGENTS.md](../AGENTS.md) owns collaboration rules;
[CONTRIBUTING.md](../CONTRIBUTING.md) owns contribution and attribution guidance.
Earlier release approvals do not authorize new publication.

## Current state

- The [v1.0.0 graduation criteria and release-readiness checklist](v1.0.0-readiness.md)
  are drafted as proposed gates, with v0.1.9 evidence and remaining work separated.
  The proposed [support matrix and compatibility rules](v1.0.0-support.md) now
  recommend local macOS Codex/Claude routes, preservation across upgrades and an
  experimental logging extension. Scope, exact configurations and compatibility
  commitments need a maintainer decision. No v1.0.0 candidate or release is
  approved; the published skills remain experimental.
  The [bounded validation plan](v1.0.0-validation-plan.md) now proposes a 22-session
  CLI pilot and separate 54-session expansion covering native journeys, two upgrade
  variants per combination and preservation checks. Isolation, combinations and
  budgets are for review; no new native subject run or execution freeze exists.
  [Wave 1 preparation](../evals/v1-readiness/wave1/README.md) now supplies synthetic
  fixtures, exact session prompts, preservation controls and read-only isolation
  evidence. Execution remains blocked on native/profile/credential boundaries,
  counterpart checker review and an accepted distinct candidate; current package
  bytes still match v0.1.9. No model trials or installed upgrades were launched.
  Preparation detected owner-global configuration/state drift of unproved origin;
  a read-only follow-up established unrelated workspace trust additions and Claude
  cache refreshes, qualified in the isolation record without rollback.
  Existing studies, installed skills and project setup files remain unchanged;
  full global-state preservation is not established.
  The [concrete Wave 1 isolation setup proposal](v1.0.0-wave1-isolation-setup.md)
  recommends independent macOS guest disks with guest-only authentication,
  inaccessible evaluator/owner storage, memory controls and explicit setup/review/
  execution gates. No qualifying existing environment was identified; provisioning
  would require an accepted amendment to the existing-only scope and a reviewed
  budget. Hardware virtualization capability is observed, but no runner or guest
  is established. The proposal is pending counterpart review; nothing was provisioned.
  The [feasibility and decision packet](v1.0.0-wave1-feasibility.md) proposes
  reviewing VirtualBuddy first, while holding provisioning on network enforcement,
  a hard new-storage limit and an accepted remaining/revised preparation budget.
  Inspected Tart/Softnet startup writes host network preferences, conflicting with
  existing-setup preservation. No runner or environment amendment is accepted;
  counterpart review remains pending and historical fixtures/receipts are unchanged.
- Previously released bundle: [v0.1.8](releases/v0.1.8.md), with core **0.1.8**, adoption
  **0.1.9** and standard **0.1.1**. Published as an experimental prerelease after
  both release-commit Actions runs passed.
- Current released bundle: [v0.1.9](releases/v0.1.9.md), with core **0.1.9**,
  adoption **0.1.9** and standard **0.1.1**, published as an experimental prerelease
  at `14acc74` after both release-commit Actions workflows passed.
  The [focused source-selection check](../evals/source-selection/README.md)
  reproduces importing a stale timeout from earlier notes in one of two released
  core trials. Initialization now explicitly checks relevant project sources
  before importing current-state claims. Both candidate trials record the actual
  configured value and preserve decisions and unfinished work. Installed skills,
  existing setup and earlier study artifacts remain unchanged. Mechanical checks
  and native outcomes are recorded separately; these trials establish no general
  reliability improvement.
  The [validation record](releases/v0.1.9-validation.json) retains earlier native
  evidence and preparation checks separately from publication. The website is
  deployed from the same release commit; all eight checked public responses match
  its build, both pages show experimental/released status and SEO titles have no
  em dash. The [verification record](website-deployment-2026-10-11.json) owns
  release/deployment Actions, hashes and limits. Installed upgrades remain separate.
- The released v0.1.8 bundle adds
  explicit [local-only context](getting-started.md#local-only-context-excluded-from-git)
  while preserving existing setups. Storage, ignored-entry discovery and sharing
  controls have 21 real-Git/canary tests. The
  [broader local-only follow-up](../evals/local-only/validation-2026-10-10/README.md)
  now exercises seven cases per client and fresh audits; storage/preservation gates
  pass, with a stale-source finding, denied journal writes and a parser failure
  retained separately. Saved studies and this repository's shared context/journal setup
  remain unchanged. The opted-in auto preference now also covers explicitly
  selected local-only context inside Git after verifying ignored, untracked
  context and journal paths; every explicit logging setting wins. The website
  guide includes canonical setup/auto prompts and SEO titles omit em dashes.
  The [auto-policy validation](../evals/event-journal/auto-preference/local-only.md)
  records 156 mechanical tests and six bounded native sessions, distinguishing
  final setup checks from earlier repeat/audit checks and retaining review limits.
  [Changelog](../CHANGELOG.md) records validation and review limits.
  [v0.1.8 release records](releases/v0.1.8.md) retain package identities,
  preparation checks and publication evidence.
- Core supports audit, initialize and maintain. Adoption uses the sibling core
  and adds or reuses maintenance guidance in loaded project instructions.
  [Installation and usage](getting-started.md) owns setup and runtime details.
- This repository enables JSONL in [AGENTS.md](../AGENTS.md); `CLAUDE.md` imports it.
  Consult history only when needed, not as routine context. Other projects keep
  their own settings;
  [logging precedence and auto rules](../skills/context-docs/references/event-journal.md#optional-auto-preference)
  are defined in the packaged guide. There is no background service or sync.

- [Landing page](https://context-docs.com/): live on GitHub Pages,
  built from selected public sources. The [v0.1.9 deployment](https://github.com/jaredchu/context-docs/actions/runs/38102425605)
  passed from `14acc74`; the [October 11 verification](website-deployment-2026-10-11.json)
  records matching live response bytes. Earlier
  [October 10 verification](website-deployment-2026-10-10.json) is retained.
  [Deployment](../site/README.md#github-pages) is manual; Cloudflare proxies the
  custom domain with Full SSL and Always Use HTTPS enabled.
- The site publishes canonical metadata, a sitemap, crawler policy and a
  [beginner guide](https://context-docs.com/getting-started/) built from canonical
  commands and prompts. The owner reports search registration and sitemap
  submission complete on October 10; indexing and AI citations are not established
  by that report. [Search discovery guidance](../site/README.md#search-discovery)
  owns the process.

## Evidence and limits

The [installed v0.1.9 smoke checks](../evals/installed-skills/2026-10-11/README.md)
retain two fresh sessions per client and two additional Claude diagnostics.
Codex used installed skills and corrected source-backed context. Claude's initial
project-only settings hid user skills; its maintenance did not use installed core.
A corrected-scope follow-up invoked core successfully, preserving decisions and
pending work, but refreshed the temporary Git index metadata. Staged content and
history stayed unchanged. Original studies/packages/setup files remain intact;
Codex trust additions for other workspaces and Claude CLI global-state changes
are qualified in the record. These guided cases do not establish general implicit
selection or independent automatic-instruction-loading proof.

Native integration remains experimental. Factual errors and scope violations are
retained in the [evidence overview](evaluation-results.md); passing checks do not
establish general reliability, comparative accuracy, privacy guarantees or savings
in users' effort or tokens. Reliable implicit selection, cross-machine installed-path
portability, JSONL necessity and natural recording-cost advantage remain unestablished.
[Repository checks](../.github/workflows/checks.yml) validate mechanics, not agent behavior.
A separate [fresh-session handoff pilot](../evals/results/2026-10-10-handoff/README.md)
ran one Opus 5.5 continuation per condition on identical synthetic code and raw
facts. Both implementations passed; curated omitted restating the approved
rationale (5/6 semantic criteria versus scattered 6/6). No curated advantage was
observed. Actual human correction effort was not measured; the small fixture
establishes no general benefit or subscription allowance savings.
The separate [larger handoff follow-up](../evals/results/2026-10-10-handoff-large/README.md)
froze retrieval quotas and its verifier before both Opus 5.5 sessions. Both
implementations and six literal criteria passed. Curated used fewer reads (9
versus 13) but slightly more file bytes; neither quota was exhausted. The
preparation timeout, scattered read-count reporting error and review
qualifications are retained; no general effort or allowance benefit is established.
[Metadata cleanup](evidence-redaction-2026-10-09.md) records original/public hashes
and unchanged scores; it did not sanitize older Git history or constitute a
comprehensive privacy audit.

## Next actions

For v1.0.0, review and accept the proposed [graduation gates](v1.0.0-readiness.md#proposed-graduation-gates)
and [support matrix/compatibility rules](v1.0.0-support.md), then review the
[bounded validation plan](v1.0.0-validation-plan.md) before freezing new validation.
Review the [Wave 1 preparation and blockers](../evals/v1-readiness/wave1/README.md#isolation-evidence-and-blockers)
before selecting a protected native environment and a distinct candidate.
Review the [isolation setup proposal](v1.0.0-wave1-isolation-setup.md#stop-conditions-and-review-decisions)
and its resource/scope choices before authorizing any provisioning or login.
Use the [feasibility packet's pending decisions](v1.0.0-wave1-feasibility.md#maintainer-decisions-to-record)
to select an environment direction and bounded implementation-review scope first.
Remaining work includes supported native user journeys, candidate
upgrade/preservation checks and an outside-user pilot with
outside artifact review. Existing authored tests and maintainer daily use support
that work but do not close those gates. Criteria preparation authorizes no outreach,
new study execution, installed upgrade or publication.

Use the released skills in normal daily work and improve them when concrete issues
arise. Reproduce failures with public evidence or synthetic examples, then validate
focused fixes. The owner reports that context updates occur during normal work
without naming the skill in each prompt; the guide now explains the loaded
maintenance rule and optional explicit prompts. This is maintainer feedback,
not a general implicit-selection evaluation. Routine use needs no evaluation log
or outside reviewer. The [contribution packet](../evals/external-validation/README.md) welcomes maintainer
feedback; it is not independent validation. New studies need a fresh freeze and
must preserve earlier results; the [discrimination protocol](../evals/discrimination-protocol.md)
is still a proposal.

The source-selection fix and v0.1.9 release are published; release-commit static
and landing-page Actions and website deployment passed. Earlier release preparation
passed 59 local tests and desktop/mobile previews, with Opus 5.5 review. Publication
reran static checks, 12 site tests and the build, then verified live response bytes;
no native study was rerun. Continue normal use and address concrete findings.
Installed upgrades remain a separate authorized action; preserve customizations,
existing setups and saved study evidence.

## Canonical references

- [Overview](../README.md) · [Standard](../skills/context-docs/references/standard.md)
- [Evaluation scenarios](../evals/README.md)
- [Per-version history](../CHANGELOG.md)
