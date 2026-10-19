# Project context

Experimental v0.2.5 was published October 18, 2026. Its website demo was deployed
and verified October 19 from `d8c624c`; all eight checked live public resources
match that demo build. Claude's second mismatch without a reread and Codex's
corrected checking error remain qualified.
Unreleased source core 0.2.6/adoption 0.1.15 strengthens destination filtering,
portable references and concise event selection. The
[focused synthetic checks](../evals/content-filtering/README.md) describe its
acceptance examples and verification limits; published standalone v0.2.5 remains
the everyday-use release.

## Purpose and scope

Context Docs helps people without an established context-management practice keep
useful, accurate project knowledge across AI sessions with minimal human effort.
This public repository serves contributors and skill users. Shared context should
retain project decisions, constraints and next actions; incidental personal
installations, backup locations and temporary machine state belong in suitable
local notes only when still useful.

## Current focus

The filtering candidate has passing offline checks and qualified counterpart
review; its final schema correction was checked locally. A
[copied-candidate smoke](../evals/content-filtering/smoke-0.2.6-2026-10-19/README.md)
passes visible saved-Markdown checks; Claude's private-note coverage gap is retained.
Keep operational outreach
in separate local notes; this work does not clean historical records or change
logging settings.

Use installed standalone experimental **v0.2.5** in everyday work and record concrete misses.
The bundle contains core **0.2.5**, adoption **0.1.14** and standard **0.1.1**.
Publication and website verification are complete from `89c91f4`; the
[publication record](releases/v0.2.5-publication.json) owns pinned identities,
the October 18 resource verification and its limits. The separate
[website demo deployment record](website-demo-deployment-2026-10-19.json) owns
the October 19 build and live checks.

Installed Codex and Claude Code sibling pairs match the release; all 32 package
files and packaged references are checked in the
[upgrade record](../.context/events/installed-v025-upgrade-20261018.jsonl).
The separate [installed native smoke](../evals/installed-skills/2026-10-18-concurrency-v025/README.md)
passes focused ownership, handoff and recovery checks, with only one mismatch per
client. It does not clear earlier qualifications. Existing setups and saved studies
are preserved. [Release history](releases/README.md) links earlier versions,
preparation/publication records and original candidate and installed evidence.

The [initial skills.sh check](../evals/installed-skills/2026-10-18-skills-sh/README.md)
passes direct discovery and isolated installation. A separate
[telemetry-enabled install](../evals/installed-skills/2026-10-18-skills-sh-telemetry/README.md)
passes; both public skill pages now show content, while owner-filtered search still
returns zero results in two October 18 snapshots. Telemetry receives HTTP 200;
indexing completion and counted installs remain unconfirmed. No native behavior is retested.

A [minimal plugin candidate](plugin-candidate.md) bundles both unchanged skills for
review. Local packaging checks pass. An [isolated loading check](../evals/packaging/plugin-loading-2026-10-18/README.md)
registers both Claude Code commands. A [Codex follow-up](../evals/packaging/codex-plugin-loading-2026-10-18/README.md)
parses both skill entries with a narrow shared-runtime identity exception; checked
identity contents and metadata remain unchanged. A [synthetic runtime smoke](../evals/packaging/plugin-runtime-2026-10-18/README.md)
passes explicit Claude adoption/maintenance. A [non-model Codex diagnostic](../evals/packaging/codex-route-diagnostic-2026-10-18/README.md)
reproduces sandbox nesting and verifies one command under the unchanged outer
boundary; active plugin registration and execution remain unverified. Earlier
harness qualifications and directory eligibility questions remain; no persistent
install, submission or publication occurred.
The owner has [deferred Codex plugin runtime validation](project-decisions.md#codex-plugin-runtime-deferral);
standalone v0.2.5 remains the everyday-use path.

A [short synthetic demo and outreach post](outreach-v0.2.5.md) invites standalone
Codex and Claude Code users to try the experimental release and report concrete
misses. The outreach post remains a draft, not posted or submitted. The
[live website demo](https://context-docs.com/#demo) reuses its three example
blocks near “What you get,” with experimental limits. Its
[deployment record](website-demo-deployment-2026-10-19.json) verifies eight matching
live resources and desktop/mobile rendering with JavaScript disabled. The demo
is illustrative, not an agent evaluation. Official directory work remains deferred.

Saved snapshot: October 19, 2026; this is not live agent activity.

```text
Goal: make progress clear during everyday context work
|
|-- RELEASED  Markdown progress and visual paths
|-- RELEASED  Default adoption and concise views
|-- RELEASED  Clarity preference
`-- RELEASED  v0.2.5 shared-file coordination
    |-- DONE     Release and website verification
    |-- DONE     Installed in Codex and Claude Code
    `-- CHECKED  Focused installed smoke; qualifications retained

NEXT: review the filtering candidate; keep using standalone v0.2.5.
```

**Blockers:** none recorded for the current standalone everyday-use path.

**Deferred:** [Codex plugin runtime validation](project-decisions.md#codex-plugin-runtime-deferral)
and the broad v1.0.0 campaign. Plugin activation and execution remain unverified.

**Qualifications:** focused checks retain earlier failures and limitations; they
do not establish broad reliability or simultaneous-write safety.

Sources: [release and feature history](releases/README.md),
[live demo verification](website-demo-deployment-2026-10-19.json),
[qualified installed checks](../evals/installed-skills/2026-10-18-concurrency-v025/README.md),
[detailed sources and limits](#evidence-and-limits), and [next action](#next-actions).

Earlier baseline: experimental v0.1.9 at `5433e47`, with its
[release record](releases/v0.1.9.md), [website verification](website-deployment-2026-10-11.json)
and [installed smoke checks](../evals/installed-skills/2026-10-11/README.md) retained.

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
- The site publishes canonical metadata, a sitemap and crawler policy. The owner
  reported search registration and sitemap submission complete on October 10;
  indexing and AI citations are not established by that report.
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

Progress source details:

- **Markdown progress, adoption and concise views:** [v0.2.0](releases/v0.2.0.md), [v0.2.1](releases/v0.2.1.md),
  [v0.2.2](releases/v0.2.2.md) and [v0.2.3](releases/v0.2.3.md) release notes.
- **Clarity:** [Clarity preference and qualified checks](releases/v0.2.4.md).
- **Coordination and publication:** [Shared-file coordination](getting-started.md#when-sessions-share-a-context-file)
  and [publication and website verification](releases/v0.2.5-publication.json).
- **Installation and focused checks:** [Installed upgrade](../.context/events/installed-v025-upgrade-20261018.jsonl)
  and [qualified installed smoke](../evals/installed-skills/2026-10-18-concurrency-v025/README.md).
- **Everyday next action:** [Next actions](#next-actions).

**Qualifications:** the installed smoke checks one forced conflict per client;
it does not establish simultaneous-write safety or clear the earlier
[Claude second-mismatch failure and Codex checking error](../evals/concurrency/smoke-0.2.5-2026-10-17/README.md).
The [earlier Codex write-scope failure](../evals/progress/smoke-0.2.3-2026-10-17/README.md)
remains retained. Focused smoke checks pass, with explicit installed paths and a
stricter temporary-write boundary; they are guided and author-scored. Fresh
adoption, the full suite, broad reliability, implicit loading and user benefit
remain unestablished. Earlier [Claude source-grounding qualifications](../evals/installed-skills/2026-10-16-progress-v021/README.md#results)
and [v0.2.0 evidence limits](../evals/progress/smoke-2026-10-16/README.md) remain retained.

**Deferred:** [Codex plugin runtime validation](project-decisions.md#codex-plugin-runtime-deferral)
is paused by owner decision. The owner also set aside the broad v1.0.0 graduation campaign. Its
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
comprehensive privacy audit.

## Next actions

Review the [filtering candidate and qualified checks](../evals/content-filtering/README.md).
No release, installed upgrade or historical metadata cleanup is selected.
Operational outreach belongs in separate local notes; directory work remains deferred.

Continue everyday work with installed standalone v0.2.5. After meaningful outcomes, update
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
