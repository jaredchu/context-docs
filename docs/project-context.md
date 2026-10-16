# Project context

Project direction updated: 2026-10-16. Release and website verification below is
from 2026-10-11; historical evaluations were not rerun.

## Purpose and scope

Context Docs helps people without an established context-management practice keep
useful, accurate project knowledge across AI sessions with minimal human effort.
This public repository serves contributors and skill users. Shared context should
retain project decisions, constraints and next actions; incidental personal
installations, backup locations and temporary machine state belong in suitable
local notes only when still useful.

## Current focus

**Goal:** integrate progress visualization into the reusable Context Docs skill,
with Markdown as the view. Jared Chu clarified on October 16 that this is a skill
feature, not only a change to this project's context. The owner set aside the
broad v1.0.0 graduation campaign. The current request prepares v0.2.0 release
notes and website updates; publication is not authorized by preparation.

Snapshot of saved work, not live agent activity:

| Work | State | Evidence / remaining work |
| --- | --- | --- |
| Experimental v0.1.9 bundle | Released | [Release record](releases/v0.1.9.md), [website verification](website-deployment-2026-10-11.json) and [installed smoke checks](../evals/installed-skills/2026-10-11/README.md), retaining their limits. Baseline: `5433e47`. |
| Markdown progress feature | Implemented in development; unreleased | [Core guidance](../skills/context-docs/references/progress.md), [adoption routing](../skills/adopt-context-docs/SKILL.md), [example](../examples/progress.md) and [guide](getting-started.md#progress-in-markdown). Installed skills are unchanged. |
| Validation and review | Initial review and focused guided smoke completed | [Artifact review](../evals/progress/review.md) and [two-session Claude Code smoke](../evals/progress/smoke-2026-10-16/README.md): create/refresh behavior and write boundaries pass, with a minor per-item source-link gap. The full scenario suite and native Codex use remain untested. |
| v0.2.0 release preparation | Ready for review; unpublished | [Draft notes](releases/v0.2.0.md) and [preparation checks](releases/v0.2.0-validation.json): website progress prompt, 32 local tests, static checks, build and desktop/mobile previews. No new native evaluation or installed upgrade. |

**Blockers and unknowns:** no implementation blocker is identified for this
development change. The smoke view's first two advances bullets lack direct
inline source links, although those sources are linked elsewhere in the view.
Whether the feature helps users assess progress remains unknown; a small guided
synthetic smoke does not prove usability. Earlier
release-readiness infrastructure is not a gate for this work. A local web viewer
and ChatGPT integration remain future possibilities.

**Next action:** review the [v0.2.0 draft notes](releases/v0.2.0.md) and website
update before authorizing publication. Continue [ordinary use](#next-actions). Markdown
remains authoritative, without an independent tracker, invented completion
percentages or claims of live activity.

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

Review the prepared v0.2.0 release notes and website update. They retain the
experimental status, prior evidence limits and v0.1.9 as the latest published
bundle. Commit/push, release publication, deployment and installed upgrades are
separate actions. Preparation changes no skill package or existing setup and
adds no native trial; its local checks are recorded in the
[preparation record](releases/v0.2.0-validation.json).

Use the development guidance during this project's next ordinary task: update
the Markdown view from actual outcomes and check that its evidence, statuses and
next action remain clear, including direct source links for each meaningful
advance. Record concrete gaps without starting a new infrastructure campaign.
The development
versions are core 0.2.0 and adoption 0.1.10; installed upgrades and a new release
are separate actions. A linked Markdown progress file is supported when useful
or requested; a web app and new evaluation infrastructure are outside this change.
The two-session synthetic smoke is not a target-user usability evaluation.

Continue normal use of the released skills and reproduce concrete failures with
public evidence or synthetic examples before validating focused fixes.
The owner reports that context updates occur during normal work
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
