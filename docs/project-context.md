# Project context

Snapshot checked: 2026-10-16. Experimental v0.2.1 is published and its website
verified. Installed v0.2.1 visual-path smoke checks complete in both clients,
with one Claude prose qualification. Earlier evidence, installed skills,
saved studies and existing project setups are preserved.

## Purpose and scope

Context Docs helps people without an established context-management practice keep
useful, accurate project knowledge across AI sessions with minimal human effort.
This public repository serves contributors and skill users. Shared context should
retain project decisions, constraints and next actions; incidental personal
installations, backup locations and temporary machine state belong in suitable
local notes only when still useful.

## Current focus

**Goal:** make progress easy to see during everyday context work, starting with a
simple inline path during adoption when documented context supports one. Reuse
existing views, layouts and canonical details rather than adding duplicate tracking.
The owner requested this default; missing goals or insufficient facts do not
justify scaffolding. The development candidate is core **0.2.2** / adoption
**0.1.11**, with [checks and limits](../evals/progress/adoption-default-2026-10-16/README.md).

**Experimental v0.2.1 remains published and its website verified.** It requires
requesting the initial view, then maintains it during meaningful updates. Installed
packages and setup rules remain unchanged. Its visual-path gate supersedes the
earlier v0.2.0 status/source checks without changing that earlier evidence.

Snapshot checked October 16, 2026; saved status does not imply live agent activity.

```text
Markdown progress
|
|-- RELEASED  v0.2.0 baseline and focused smoke checks [R]
|
|-- RELEASED  Visual-path improvement, core 0.2.1 [V]
|   |-- DONE  Guidance and source-linked example [E]
|   |-- DONE  Visual acceptance criteria [A]
|   |-- DONE  Local validation and counterpart review [C]
|   |-- DONE  Focused Codex and Claude visual-path smoke [S]
|   |-- DONE  Release notes and website preparation [P]
|   |-- DONE  Experimental release, deployment and live verification [D]
|   `-- CHECKED  Installed visual-path smoke; Claude prose qualified [I]
|
`-- CANDIDATE  Default inline progress during adoption [N]
    |-- DONE  Guidance, three guided native sessions and local checks [N]
    |-- DONE  Bounded Opus review and preservation checks [N]
    `-- NEXT  Review prepared changes [N]

NEXT: review prepared default-adoption changes [N]
```

Sources for the visual:

- **R:** [v0.2.0 release](releases/v0.2.0.md), [publication/website record](releases/v0.2.0-publication.json)
  and [installed Codex/Claude smoke](../evals/installed-skills/2026-10-16-progress/README.md).
  Eight live responses matched the release build; each installed create case had
  17 resolving links. These were narrow status/source checks, not the new visual gate.
- **V:** [Published v0.2.1 bundle](releases/v0.2.1.md) and
  [development change](../CHANGELOG.md#context-docs-021--2026-10-16-bundled-in-v021). Adoption 0.1.10
  and standard 0.1.1 are unchanged; installed skills and earlier release records are untouched.
- **E:** [Core guide](../skills/context-docs/references/progress.md),
  [source-linked visual example](../examples/progress.md), [adoption routing](../skills/adopt-context-docs/SKILL.md)
  and [user guide](getting-started.md#progress-in-markdown). Ordinary maintenance
  preserves an existing format; an explicit visualization request may reshape the
  view within its existing section/file, preserving owner edits and record locations.
- **A:** [Visual acceptance criteria](../evals/progress/README.md#visual-acceptance-criteria-core-021-candidate)
  now require visible goal relationships, supported dependencies/blockers and
  clickable sources. A focused create case now exercises them in each client;
  the full manual suite remains unexecuted.
- **C:** [Correction checks and review](../evals/progress/visual-path-review-2026-10-16.md).
  Mechanical checks and Opus artifact review are separate from native evaluation.
- **S:** [Candidate smoke and exact outputs](../evals/progress/smoke-0.2.1-2026-10-16/README.md).
  One copied-candidate case per client passes the visual-path, dependency, blocker
  and clickable-source gates; 18 Codex and 14 Claude view/context links resolve.
  These are guided, author-scored cases, not a general visual-usability result.
- **P:** [v0.2.1 notes](releases/v0.2.1.md) and unchanged
  [preparation checks](releases/v0.2.1-validation.json) retain the original checks,
  local previews and limits separately from publication.
- **D:** [Publication and live verification](releases/v0.2.1-publication.json).
  The experimental release and website use `0c897c0` after both release-commit
  Actions pass. Eight live HTTPS resources match the build, including the visual
  path, source maps and released labels. Installed skills remain unchanged.
- **I:** [Installed v0.2.1 smoke and exact outputs](../evals/installed-skills/2026-10-16-progress-v021/README.md).
  One fresh guided case per client uses the installed core and progress guide.
  Both visual paths, dependencies and blockers pass; 17 Codex and 15 Claude
  view/context links resolve. Claude's prose adds an unsupported provider-choice
  prerequisite; its diagram preserves the documented sequence. No correction or
  retry is performed. This is author-scored evidence, not a general benefit claim.
- **N:** [Default-adoption candidate checks](../evals/progress/adoption-default-2026-10-16/README.md).
  Core 0.2.2 / adoption 0.1.11 is unreleased. The default inline checklist and
  ordinary-work refresh pass two initial-candidate Codex phases; a third session
  on the clarified candidate leaves a current nested checklist unchanged.
  Opus review/follow-up resolve material findings. Fresh setup with a new rule,
  linked/nonvisual views, sparse/local-only/no-view and audit cases remain
  unexecuted natively. The record owns exact package identities and qualifications.

Earlier baseline: experimental v0.1.9 at `5433e47`, with its
[release record](releases/v0.1.9.md), [website verification](website-deployment-2026-10-11.json)
and [installed smoke checks](../evals/installed-skills/2026-10-11/README.md) retained.

**Blockers and gaps:** focused candidate and installed visual paths pass; the
installed Claude output has the [source-grounding qualification](../evals/installed-skills/2026-10-16-progress-v021/README.md#results)
recorded above. The full progress
suite, default/implicit loading and benefit to
intended users remain unestablished. The [earlier copied-development smoke](../evals/progress/smoke-2026-10-16/README.md)
retains its two advances bullets without direct inline links; newer outputs do
not replace that result. The [initial v0.2.0 artifact review](../evals/progress/review.md)
is also unchanged.

**Next action:** see [next actions](#next-actions). The candidate's
[check record](../evals/progress/adoption-default-2026-10-16/README.md) owns remaining
validation qualifications; earlier installed v0.2.1 evidence remains unchanged.

The owner set aside the broad v1.0.0 graduation campaign. Its retained
[infrastructure proposals](#current-state) remain deferred. A local web viewer and
ChatGPT integration are future possibilities, with no implementation selected.
Markdown stays authoritative; no independent tracker, completion percentage or
live-activity claim is introduced.

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

- Installed v0.2.1 now has a [focused native smoke record](../evals/installed-skills/2026-10-16-progress-v021/README.md),
  separate from the copied-candidate evidence. Both clients produce the required
  visual path; Claude's extra prose prerequisite remains qualified. No installed
  skill, setup, earlier evidence or saved-study change is part of this check.
- Released core **0.2.1** tightens explicit visualization requests to show a visual path
  with supported dependencies, blockers and clickable sources. It is published in
  experimental v0.2.1; a focused copied-candidate create case passes acceptance in
  each native client, with [outputs and limits](../evals/progress/smoke-0.2.1-2026-10-16/README.md).
  Adoption remains **0.1.10**;
  its existing sibling routing inherits the core guide. The [correction record](../evals/progress/visual-path-review-2026-10-16.md)
  owns local checks and the bounded Opus artifact review. Existing setups,
  installed packages and saved studies are unchanged.
- [v0.2.1 release preparation](releases/v0.2.1.md) adds the canonical
  source-linked visual example to both public website templates. The
  [preparation record](releases/v0.2.1-validation.json) owns current local checks
  and previews separately from earlier native evidence. No new model request,
  publication, deployment or installed upgrade is part of that historical preparation.
- Current released bundle: [v0.2.1](releases/v0.2.1.md), with core **0.2.1**,
  unchanged adoption **0.1.10** and standard **0.1.1**, published and deployed
  from `0c897c0`. Both release-commit Actions and deployment pass; all eight
  checked live responses match the build. The [publication record](releases/v0.2.1-publication.json)
  owns release/deployment identities and limits. Installed skills, existing setups
  and saved studies are preserved.

- Previous released bundle: [v0.2.0](releases/v0.2.0.md), with core **0.2.0**,
  adoption **0.1.10** and standard **0.1.1**. Published as an experimental prerelease
  at `d341695` after both main-branch release-commit Actions passed. Website
  deployment passed from that commit; eight live public responses match the build.
  The [publication record](releases/v0.2.0-publication.json) retains hashes and
  limits separately from unchanged preparation evidence. Installed skills, project
  setups, saved studies and prior main-branch planning records are preserved.
- Earlier main-branch [graduation criteria](v1.0.0-readiness.md),
  [support proposal](v1.0.0-support.md), [validation plan](v1.0.0-validation-plan.md),
  [Wave 1 fixtures](../evals/v1-readiness/wave1/README.md),
  [isolation proposal](v1.0.0-wave1-isolation-setup.md) and
  [feasibility packet](v1.0.0-wave1-feasibility.md) remain as deferred history.
  Their proposed infrastructure and gates are not requirements for v0.2.0.

- Previously released bundle: [v0.1.8](releases/v0.1.8.md), with core **0.1.8**, adoption
  **0.1.9** and standard **0.1.1**. Published as an experimental prerelease after
  both release-commit Actions runs passed.
- Previous released bundle: [v0.1.9](releases/v0.1.9.md), with core **0.1.9**,
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

- [Landing page](https://context-docs.com/): live on GitHub Pages, built from
  selected public sources. The [v0.2.1 deployment](https://github.com/jaredchu/context-docs/actions/runs/38911491498)
  passed from `0c897c0`; the [publication record](releases/v0.2.1-publication.json)
  records eight matching live responses, visual paths/source maps and released
  labels on both pages. The [v0.2.0 record](releases/v0.2.0-publication.json),
  [October 11](website-deployment-2026-10-11.json)
  and [October 10](website-deployment-2026-10-10.json) verification is retained.
  [Deployment](../site/README.md#github-pages) is manual; Cloudflare proxies the
  custom domain with Full SSL and Always Use HTTPS enabled.
- The site publishes canonical metadata, a sitemap, crawler policy and a
  [beginner guide](https://context-docs.com/getting-started/) built from canonical
  commands and prompts. The owner reports search registration and sitemap
  submission complete on October 10; indexing and AI citations are not established
  by that report. [Search discovery guidance](../site/README.md#search-discovery)
  owns the process.

## Evidence and limits

The [installed v0.2.0 progress smoke](../evals/installed-skills/2026-10-16-progress/README.md)
passes one explicit linked-view creation request in each native client. Core and
progress-guide use are observed; goals, blockers, proposals, useful learning and
possible stalls remain distinct. This does not test implicit selection, default
interactive UI behavior or the remaining progress scenarios. No skill change or
new infrastructure follows from these two author-scored cases.

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

Review the prepared [default-adoption candidate](../evals/progress/adoption-default-2026-10-16/README.md).
Commit/push, installation, release, deployment and existing project changes remain
outside this completed edit/check task. Released and installed versions retain
their original behavior.

The [v0.2.1 bundle](releases/v0.2.1.md) is published and its website verified.
Use the released guidance and preserve the historical
[preparation checks](releases/v0.2.1-validation.json) and
[publication receipt](releases/v0.2.1-publication.json).
The [candidate smoke outputs](../evals/progress/smoke-0.2.1-2026-10-16/README.md)
retain both guided create cases passing the visual gate; the full suite and
target-user benefit remain unestablished. Installed upgrades still require
separate authorization; publication does not change installed copies.

The experimental v0.2.1 release and website are published and verified. Use the
released guidance and address concrete findings; no graduation infrastructure
campaign is required. Installed upgrades remain a separate authorized action,
preserving customizations and existing setups.

Use the released guidance during this project's next ordinary task: update
the Markdown view from actual outcomes and check that its evidence, statuses and
next action remain clear, including direct source links for each meaningful
advance. Record concrete gaps without starting a new infrastructure campaign.
The v0.2.1 bundle contains core 0.2.1 and adoption 0.1.10; installed upgrades
remain separate. A linked Markdown progress file is supported when useful
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
