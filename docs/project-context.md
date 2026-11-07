# Project context

Context Docs packages a Markdown maintenance workflow for people without an
established way to preserve project knowledge across AI sessions. Keep useful
decisions, current work and next steps accurate with little manual organization.
Standalone experimental **v0.2.7** is published. The owner separately authorized
website deployment; installed upgrades remain separate actions.

## Purpose and scope

The core skill audits, initializes and maintains existing project documents;
the adoption skill establishes or reuses ongoing maintenance instructions.
Markdown/Git stays authoritative. Progress views and optional local-only storage
fit existing layouts; ordinary maintenance needs no runtime or cloud service.
This public repository serves skill users and contributors. Keep maintainer-specific
operator preferences and incidental state outside it; use suitable public summaries
and evidence IDs when those records explain a project issue.

## Current focus

The owner accepted a focused review follow-up: simplify this entry point, prepare
an unfamiliar-user trial and deduplicate skill instructions incrementally. The
[decision](project-decisions.md#review-follow-up-and-learner-validation) owns scope;
the [trial packet](../evals/user-feedback/README.md) owns the procedure and measures.
The owner supplied [anonymous early feedback](../evals/user-feedback/README.md#anonymous-early-feedback)
from five responses, including one team response. Reported usefulness is positive;
the owner subsequently [confirmed human-observed usability and actual
cross-machine use](../evals/user-feedback/README.md#owner-confirmation).
The published release contains core **0.2.7** and adoption **0.1.16**. The
[candidate check](../evals/simplification/2026-10-26/README.md) passes focused file
checks in Codex and Claude. Claude startup/import events support its loading
statement; the earlier Codex statement remains unverified. Published v0.2.6 and
frozen participant r1 materials remain unchanged. The [v0.2.7 release notes](releases/v0.2.7.md)
own bundle scope; the [preparation record](releases/v0.2.7-validation.json) retains
its original unpublished scope and local checks. The contributor instructions and
this context now follow the [public audience boundary](project-decisions.md#public-project-context-boundary).

Progress snapshot updated November 7, 2026; earlier technical checks retain their
recorded dates. This is not live agent activity.

~~~text
Goal: useful, accurate context with less manual organization
├─ AVAILABLE  Released standalone v0.2.6 and Reading Queue walkthrough
├─ PREPARED   Concise context, trial packet and qualified simplification candidate
├─ RECEIVED   Five positive self-reports, including one team response
│  └─ LEARNED Continuity is valued; keeping context current needs occasional help
├─ CONFIRMED  Human-observed usability and cross-machine use (owner confirmation)
├─ CHECKED    One synthetic Git-transfer handoff; fresh reader recovered all 8 items
├─ CHECKED    Stale dependency note corrected; rationale and blocker retained
│  └─ OUTCOME No skill fix needed in this synthetic case; focused check complete
├─ PREPARED   Public context and model-neutral contributor rules
├─ READY      Published-release install pins, current evidence index and transfer guidance
└─ PUBLISHED  v0.2.7 at 00c4b51; release CI and website deployment pass
   ├─ CHECKED Website build matches repo; owner retains edge analytics difference
   ├─ CHECKED Isolated install matches all 16 package files; existing skills unchanged
   └─ UNKNOWN skills.sh pages still show v0.2.6; public-content refresh unverified
~~~

The [publication record](releases/v0.2.7-publication.json) owns exact release/deployment
source and discovery limits. The [usage guide](getting-started.md) owns installation pinned to published bundle
v0.2.7 and shared-context transfer guidance. The
[evidence overview](evaluation-results.md#more-recent-studies) now links the newer
feedback, candidate and synthetic records with their distinct scopes and limits.

The [feedback summary](../evals/user-feedback/README.md#anonymous-early-feedback)
owns the reports, friction and evidence limits. No blocker is recorded for
experimental everyday use. Human-observed usability and actual cross-machine
use are owner-confirmed; measured comparative effort remains unestablished.
The [Git-transfer check](../evals/handoff/2026-11-07-git-transfer/README.md)
adds inspected agent evidence on one host, separate from participant outcomes.
The [stale-note check](../evals/stale-note/2026-11-07/README.md) passes one ordinary
refresh using source core 0.2.7. It did not reproduce the reported miss and did
not require a skill change; the private case's cause remains unknown.
The broad v1.0.0 campaign,
[Codex plugin runtime work](project-decisions.md#codex-plugin-runtime-deferral)
and [Cursor support/testing](project-decisions.md#cursor-support-postponement)
remain deferred.

## Decisions

- Keep Markdown/Git authoritative and cloud integrations optional; a hosted
  service needs a concrete use case.
- Preserve the [standard's](../skills/context-docs/references/standard.md)
  distinction between observations, approved decisions, proposals and unknowns;
  choose retained detail by audience, destination and lasting usefulness.
- Judge success by useful knowledge, accuracy and users' setup, organization,
  prompting and correction effort. Faster models, fewer tokens or shorter files
  alone do not establish benefit; beating expert maintenance is not the gate.
- Keep logging optional, for efficient event capture and later investigation.
  Local-only context without Git history is a concrete use case; Markdown/Git
  may otherwise suffice. Broader integration must meet the
  [journal requirements](event-journal-pilot.md#requirements-before-broader-integration).
  A journal is not complete version recovery; use snapshots or backups for that.
- Preserve existing setups, customizations, unique rationale and frozen evidence.
  Structural changes and publication need their own scope. Follow the
  [no-change stop rule](project-decisions.md#refresh-recording-and-publication-boundary)
  and [deployment checklist](../site/README.md#deployment-checklist); record-only
  changes do not require another deployment.

[Decision history](project-decisions.md) owns authority and rationale;
[AGENTS.md](../AGENTS.md) owns repository working and review rules;
[CONTRIBUTING.md](../CONTRIBUTING.md) owns contribution checks and Codex/Claude credit.
Earlier release approvals do not authorize new publication.

## Current state

- The [skills.sh metadata workflow](skills-sh-refresh.md) defines daily and manual
  refreshes with public star-count verification. Its preflight skips installation
  when both pages already agree with GitHub.
- The [usage guide](getting-started.md) owns installation, instruction loading,
  maintenance and progress-view procedures. Refresh after outside work is an
  existing maintenance invocation, not a new operation.
- This repository enables JSONL in AGENTS.md, imported by CLAUDE.md. Consult
  history only for a concrete need. Other projects retain their own logging
  settings; the [packaged journal guide](../skills/context-docs/references/event-journal.md)
  owns precedence and auto resolution. There is no background sync.
- The website, comparison and Reading Queue walkthrough have recorded successful
  publication checks. The [deployment summary](../site/README.md#latest-deployment)
  owns the actual website revision, artifact/live comparisons and browser checks.
  The [example summary](reading-queue-example.md) owns its separate app revision,
  automatic app deployment and native walkthrough observations. Website deployment
  remains manual. Search indexing and AI citations remain unestablished; see
  [search discovery](../site/README.md#search-discovery).
- The [plugin candidate](plugin-candidate.md) deliberately freezes older skills.
  Its bounded Claude runtime check passed; Codex activation/execution, duplicate
  installation/upgrade behavior and directory eligibility remain unresolved.
  Standalone skills remain the everyday path.

## Evidence and limits

The [evidence overview](evaluation-results.md) owns study outcomes, factual errors,
scope violations and reviewer disagreements. It establishes neither a
skill-specific accuracy advantage nor reduced target-user effort. Native
integration remains experimental; broad reliability, privacy guarantees,
simultaneous-write safety, reliable implicit selection, installed-path portability,
JSONL necessity and a natural recording-cost advantage remain unestablished.
Repository checks validate mechanics, not agent behavior.

- [v0.2.6 release notes](releases/v0.2.6.md) own published core **0.2.6**, adoption
  **0.1.15**, separately versioned standard **0.1.1**, installation and discovery
  verification. The [installed filtering check](../evals/installed-skills/2026-10-19-filtering-v026/README.md)
  names the incoming note explicitly; it does not clear the earlier candidate's
  unlinked-note coverage gap. [Release history](releases/README.md) retains prior
  progress, clarity, coordination and installation checks with their failures.
- The [refresh baseline](../evals/refresh/baseline-0.2.6-2026-10-26/README.md)
  repairs synthetic drift and leaves all 19 project files unchanged on a second
  fresh run. [Real-repository observations](refresh-observations-2026-10-26.md)
  are bounded same-chat maintainer checks, separate from that synthetic study.
  Neither establishes general idempotence or completeness.
- The [Reading Queue observations](reading-queue-example.md#scope-and-status)
  include maintenance under ordinary follow-up prompts. The Codex walkthrough
  retains a no-install violation; Claude's earlier case retains a wording
  qualification. Neither is independent learner validation or general selection
  evidence. The app's tests are not tests of Context Docs' effectiveness.
- The [handoff pilot](../evals/results/2026-10-10-handoff/README.md) and
  [larger follow-up](../evals/results/2026-10-10-handoff-large/README.md) retain
  the initial loss and later correctness tie. The [comparison research](context-management-comparison.md)
  is source-based desk research, not installed-tool testing. The
  [metadata transformation record](evidence-redaction-2026-10-09.md) preserves
  provenance and scores; it is not a comprehensive privacy or Git-history audit.

## Next actions

The stale-note check, public-context cleanup and selected installation/evidence/
transfer documentation follow-up are complete; no additional skill fix is selected.
Release publication and the subsequently authorized website deployment are complete
at `00c4b51`. The owner chose to keep the Cloudflare-injected analytics beacon;
record the live-byte difference while retaining the repository/artifact match.
The isolated skills.sh install passes, but both public page bodies remain on
v0.2.6 after a bounded wait. Retain that discovery verification gap; do not treat
HTTP 200 telemetry as an updated page or repeat installs/replay telemetry.
Existing installed upgrades remain separate; retain the actual deployed source. Keep the
[discrimination protocol](../evals/discrimination-protocol.md)
as a separate proposed comparative study, not a prerequisite for everyday use.

The [trial packet](../evals/user-feedback/README.md) and frozen
[r1 material set](../evals/user-feedback/README.md#prepared-material-set-r1)
remain available for further structured follow-up. The owner confirmation does
not identify use of that material set. If used, record actual installation state,
assistance, corrections, incomplete attempts and fresh-session outcomes against
its material ID; agents cannot substitute for participants.

Keep the [deferred v1.0.0 criteria](v1.0.0-readiness.md),
[validation plan](v1.0.0-validation-plan.md),
[Wave 1 fixtures](../evals/v1-readiness/wave1/README.md),
[isolation proposal](v1.0.0-wave1-isolation-setup.md) and
[feasibility packet](v1.0.0-wave1-feasibility.md) as retained proposals.
A web viewer or ChatGPT integration is not selected. Routine use needs no
evaluation diary; a no-change refresh ends with its concise chat result.

## Canonical references

- [Overview](../README.md) · [Standard](../skills/context-docs/references/standard.md)
- [Evaluation scenarios](../evals/README.md) · [Outside-contributor packet](../evals/external-validation/README.md)
- [Release history](releases/README.md) · [Changelog](../CHANGELOG.md)
