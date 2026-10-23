# Project context

Use standalone experimental **v0.2.6** for everyday work. The
[progress view](#current-focus) summarizes status; [evidence and limits](#evidence-and-limits)
links release, installation and qualified checks.

## Purpose and scope

Context Docs helps people without an established context-management practice keep
useful, accurate project knowledge across AI sessions with minimal human effort.
This public repository serves contributors and skill users. Shared context should
retain project decisions, constraints and next actions; incidental personal
installations, backup locations and temporary machine state belong in suitable
local notes only when still useful.

## Current focus

Continue everyday use and record concrete misses. No skill change, new release,
infrastructure campaign or smoke rerun is selected. Release and installation
outcomes are recorded under [evidence and limits](#evidence-and-limits).

Saved snapshot: October 19, 2026; this is not live agent activity.

```text
Goal: make progress clear during everyday context work
│
├─ RELEASED  Markdown progress, adoption and concise views
├─ RELEASED  Clarity and shared-file coordination
└─ RELEASED  v0.2.6 metadata filtering and portable references
   ├─ DONE     Release and website verification
   ├─ DONE     Installed in Codex and Claude Code
   └─ CHECKED  Focused installed smoke; qualifications retained

NEXT: use v0.2.6 in everyday work; record concrete misses.
```

**Blockers:** none recorded for the current standalone everyday-use path.

**Deferred:** [Codex plugin runtime validation](project-decisions.md#codex-plugin-runtime-deferral)
and the broad v1.0.0 campaign. Plugin activation and execution remain unverified.

**Qualifications:** focused checks retain earlier failures and limitations; they
do not establish broad reliability or simultaneous-write safety.

Sources: [release and feature history](releases/README.md),
[current website verification](../site/README.md#latest-deployment),
[qualified installed checks](../evals/installed-skills/2026-10-19-filtering-v026/README.md),
[detailed sources and limits](#evidence-and-limits), and [next action](#next-actions).

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
- Follow the [collaboration rules](../AGENTS.md#model-collaboration) for model
  assignments, bounded reviews, one-writer coordination and subscription/spending
  safeguards. AGENTS.md owns the operative policy; local notes retain duplicate
  operator rationale.

[Decision history](project-decisions.md) records authority and rationale.
[AGENTS.md](../AGENTS.md) owns collaboration rules;
[CONTRIBUTING.md](../CONTRIBUTING.md) owns contribution and attribution guidance.
Earlier release approvals do not authorize new publication.

## Current state

- Core supports audit, initialize and maintain. Adoption uses its sibling core
  and adds or reuses maintenance guidance in loaded project instructions.
  [Installation and usage](getting-started.md) owns setup and runtime details.
- This repository enables JSONL in [AGENTS.md](../AGENTS.md); `CLAUDE.md` imports it.
  Consult history only when needed, not as routine context. Other projects keep
  their own settings; the packaged guide owns
  [logging precedence and auto rules](../skills/context-docs/references/event-journal.md#optional-auto-preference).
  There is no background service or sync.
- The [landing page](https://context-docs.com/) and
  [beginner guide](https://context-docs.com/getting-started/) are live on GitHub Pages,
  built from selected public sources. [Deployment](../site/README.md#github-pages)
  is manual. Recorded domain settings are Cloudflare proxying, Full SSL and Always
  Use HTTPS. Earlier deployment receipts are linked in [release history](releases/README.md).
  The [October 23 deployment](../site/README.md#latest-deployment) from `main` at
  `f5f5b50` succeeded; all eight served files matched the build and uploaded
  artifact. Detailed operator verification is retained in local notes.
- The site publishes canonical metadata, a sitemap and crawler policy. Search
  indexing and AI citations remain unestablished; operator registration details
  are retained in local notes.
  [Search discovery guidance](../site/README.md#search-discovery) owns the process.
- The deferred v1.0.0 [graduation criteria](v1.0.0-readiness.md),
  [support proposal](v1.0.0-support.md), [validation plan](v1.0.0-validation-plan.md),
  [Wave 1 fixtures](../evals/v1-readiness/wave1/README.md),
  [isolation proposal](v1.0.0-wave1-isolation-setup.md) and
  [feasibility packet](v1.0.0-wave1-feasibility.md) remain history, outside the current
  everyday-use path.

## Evidence and limits

Native integration remains experimental. The [evidence overview](evaluation-results.md)
indexes results, factual errors, scope violations and reviewer disagreements.
[Release history](releases/README.md) links the original candidate and installed
records; passing checks do not establish general reliability, comparative accuracy,
privacy guarantees or savings in users' effort or tokens. Reliable implicit
selection, cross-machine installed-path portability, JSONL necessity and natural
recording-cost advantage remain unestablished.
[Repository checks](../.github/workflows/checks.yml) validate mechanics, not agent behavior.

- **Current release and installation:** experimental v0.2.6 was published October 19,
  2026, with core **0.2.6**, adoption **0.1.15** and standard **0.1.1**. It strengthens
  destination filtering, portable references and meaningful event selection.
  The [release notes](releases/v0.2.6.md) and [publication record](releases/v0.2.6-publication.json)
  retain identities and limits: the website was deployed from `d74e69d`, and all
  eight checked live public files matched that build. The [preparation record](releases/v0.2.6-validation.json)
  keeps its original prepublication scope. The separately authorized
  [installed upgrade](../.context/events/installed-v026-upgrade-20261019.jsonl)
  verified all 32 package files against the release, including metadata, packaged
  links and anchors. Detailed local installation bookkeeping is retained in
  operator notes; the historical upgrade record is unchanged. Publication does
  not change logging settings or clean historical records.
- **Current checks:** the [candidate smoke](../evals/content-filtering/smoke-0.2.6-2026-10-19/README.md)
  passes visible saved-Markdown checks but leaves Claude's unlinked private-note
  coverage gap. The separate [installed smoke](../evals/installed-skills/2026-10-19-filtering-v026/README.md)
  names the incoming note; both clients read it and pass focused filtering,
  portability and context-quality checks. Claude's five failed reads while finding
  the public report remain recorded. These guided, explicit-path checks do not
  establish implicit loading or general privacy guarantees, and do not clear the
  earlier candidate gap.
- **Earlier progress features:** [v0.2.0](releases/v0.2.0.md), [v0.2.1](releases/v0.2.1.md),
  [v0.2.2](releases/v0.2.2.md) and [v0.2.3](releases/v0.2.3.md) cover Markdown progress,
  adoption and concise views; [v0.2.4](releases/v0.2.4.md) owns clarity and its qualified checks.
- **Earlier coordination and installation:** the [shared-file guide](getting-started.md#when-sessions-share-a-context-file),
  [v0.2.5 publication record](releases/v0.2.5-publication.json),
  [upgrade](../.context/events/installed-v025-upgrade-20261018.jsonl) and
  [installed smoke](../evals/installed-skills/2026-10-18-concurrency-v025/README.md)
  retain their original scopes. The publication and October 18 resource checks
  used `89c91f4`; the installed smoke passed focused ownership, handoff and recovery
  with one forced mismatch per client. It does not validate v0.2.6, establish
  simultaneous-write safety or clear the earlier
  [Claude second-mismatch failure and Codex checking error](../evals/concurrency/smoke-0.2.5-2026-10-17/README.md).
- **Retained qualifications:** the [Codex write-scope failure](../evals/progress/smoke-0.2.3-2026-10-17/README.md),
  [Claude source-grounding qualifications](../evals/installed-skills/2026-10-16-progress-v021/README.md#results)
  and [v0.2.0 evidence limits](../evals/progress/smoke-2026-10-16/README.md) remain.
  Installed smokes use explicit paths and a stricter temporary-write boundary;
  they are guided and author-scored. Fresh adoption, the full suite, broad
  reliability, implicit loading and user benefit remain unestablished.
- **Discovery:** the [initial skills.sh check](../evals/installed-skills/2026-10-18-skills-sh/README.md)
  passes direct discovery and isolated installation. The separate
  [telemetry-enabled install](../evals/installed-skills/2026-10-18-skills-sh-telemetry/README.md)
  passes and both public pages show content; owner-filtered search returns zero
  results in two October 18 snapshots. Telemetry received HTTP 200; indexing
  completion and counted installs remain unconfirmed. Native behavior was not retested.
  The October 23 [verified refresh result](releases/v0.2.6.md#discovery-verification)
  records both pages matching v0.2.6's rendered skill text and its verification
  limits. Detailed operator evidence is retained in local notes.
  Future authorized releases include the
  [isolated refresh and verification checklist](../CONTRIBUTING.md#release-checklist).
- **Deferred plugin:** the [minimal candidate](plugin-candidate.md) bundles both
  then-current unchanged skills and passes local packaging checks. The
  [loading check](../evals/packaging/plugin-loading-2026-10-18/README.md) registers
  both Claude commands; the [Codex follow-up](../evals/packaging/codex-plugin-loading-2026-10-18/README.md)
  parses both entries with a narrow shared-runtime identity exception, preserving
  checked identity contents and metadata. The [runtime smoke](../evals/packaging/plugin-runtime-2026-10-18/README.md)
  passes explicit Claude adoption/maintenance. The [non-model Codex diagnostic](../evals/packaging/codex-route-diagnostic-2026-10-18/README.md)
  reproduces sandbox nesting and verifies one command under the unchanged outer
  boundary. Active Codex plugin registration and execution remain unverified;
  earlier harness qualifications and directory eligibility questions remain.
  No persistent installation, submission or publication occurred. The
  [owner's deferral](project-decisions.md#codex-plugin-runtime-deferral) keeps standalone
  skills as the everyday-use path; official directory work remains deferred.
- **Illustrative demo:** the [public demo source](outreach-v0.2.5.md) retains the
  fictional work notes, saved context and fresh-session prompt. The promotional
  draft and operational outreach are retained in local notes. The
  [website demo](https://context-docs.com/#demo) reuses the three
  blocks near “What you get,” with experimental limits. Its separate October 19
  [deployment record](website-demo-deployment-2026-10-19.json) verifies eight matching
  live resources and desktop/mobile rendering with JavaScript disabled. It is
  illustrative, not an agent evaluation.
- **Earlier baseline:** experimental v0.1.9 at `5433e47`; its [release record](releases/v0.1.9.md),
  [website verification](website-deployment-2026-10-11.json) and
  [installed checks](../evals/installed-skills/2026-10-11/README.md) remain retained.

The owner set aside the broad v1.0.0 graduation campaign; its
[infrastructure proposals](#current-state) remain history. A local web viewer
and ChatGPT integration are future possibilities; no implementation is selected.
Markdown remains authoritative, without an independent tracker or completion percentage.

The [offline concurrency diagnostic](../evals/concurrency/offline-2026-10-17/README.md)
retains exact synthetic inputs/results and forced filesystem/tool outcomes; it
is separate from native sessions and is not an independent reproduction.
The [fresh-session handoff pilot](../evals/results/2026-10-10-handoff/README.md) and
[larger follow-up](../evals/results/2026-10-10-handoff-large/README.md) retain their
original outcomes, errors and qualifications without establishing general user-effort
or subscription-allowance benefit.
[Metadata cleanup](evidence-redaction-2026-10-09.md) records original/public hashes
and unchanged scores; it did not sanitize older Git history or constitute a
comprehensive privacy audit. No historical cleanup has been performed for v0.2.6.

## Next actions

Continue everyday work with installed standalone v0.2.6. After meaningful outcomes, update
the existing concise view and check its statuses, source links, blockers and next
action. Reproduce concrete misses with public evidence or synthetic examples
before focused fixes; no new infrastructure campaign or smoke rerun is selected.
Preserve existing setups, installed customizations, decisions and saved studies.

The owner reports context updates during normal work without naming the skill in
every prompt. This is maintainer feedback, not general implicit-selection evidence.
Routine use needs no evaluation log or outside reviewer. The
[contribution packet](../evals/external-validation/README.md) welcomes feedback,
not independent validation. New studies need a fresh freeze and must preserve
earlier results; the [discrimination protocol](../evals/discrimination-protocol.md)
remains a proposal.

## Canonical references

- [Overview](../README.md) · [Standard](../skills/context-docs/references/standard.md)
- [Evaluation scenarios](../evals/README.md)
- [Release history](releases/README.md) · [Changelog](../CHANGELOG.md)
