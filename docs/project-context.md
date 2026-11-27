# Project context

Context Docs helps people preserve decisions, current work and next steps across
AI sessions using their project's Markdown. The
[v0.2.10 experimental prerelease](releases/v0.2.10.md) bundles core **0.2.10**
and adoption **0.1.17**. The installation guide selects this bundle. The earlier
[v0.2.9 release](releases/v0.2.9.md) retired optional JSONL capture and
preserved historical records.

## Purpose and scope

The core skill audits, initializes and maintains context. The adoption skill sets
up or reuses a project maintenance rule. Both use existing layouts, including
Markdown progress views and opt-in local-only storage. Ordinary maintenance
runs during active sessions and needs no runtime or cloud service.

This public repository serves skill users and contributors. Keep maintainer
workflows in their private destination and use suitable public summaries or
evidence IDs when needed. See the [public context decision](project-decisions.md#public-project-context-boundary).

## Current focus

- **Goal:** Preserve accurate project context with little manual organization.
  - **Available:** Use the [standalone workflow](getting-started.md#use-it) and
    the [Reading Queue walkthrough and cross-client handoffs](switching-agents-examples.md).
  - **Optional workflow:** The [Markdown ticket example](../examples/progress.md#opt-in-markdown-ticket)
    shows work-item handoffs. Core 0.2.10 adds a shared
    [ticket lifecycle](../skills/context-docs/references/tickets.md) for filing
    completed tickets and reopening them in projects that opt in.

## Decisions

- Keep Markdown/Git authoritative and cloud integrations optional. Preserve
  observations, approvals, proposals and unknowns with their sources, and choose
  detail by audience and lasting usefulness. See the [standard](../skills/context-docs/references/standard.md).
- Judge effectiveness by accuracy, useful handoff and the effort of setting up,
  prompting, organizing and correcting context. File size and model cost are
  diagnostics. See the [learner validation decision](project-decisions.md#review-follow-up-and-learner-validation).
- The [journal removal decision](project-decisions.md#retire-optional-jsonl-event-capture)
  keeps current maintenance in Markdown and preserves historical records.
- Preserve existing layouts, approved decisions and frozen evidence. Follow the
  [no-change stop rule](project-decisions.md#refresh-recording-and-publication-boundary)
  and the [deployment checklist](../site/README.md#deployment-checklist). Publication,
  release and installed upgrades each use their own authorization.

## Current state

- **Client support:** Codex and Claude Code have standalone instructions.
  [Cursor](getting-started.md#cursor-experimental) and
  [Antigravity](getting-started.md#antigravity-experimental) have experimental
  support validated through bounded CLI trials. Cursor's editor and Antigravity's
  App and IDE were not separately tested.
- **Website:** The [deployment record](../site/README.md#latest-deployment) gives
  the verified source (`9008ac6`) and deployment history. Relevant pushes to
  `main` deploy through Workers Static Assets. The
  [Reading Queue app record](reading-queue-example.md) covers its separate deployment
  and walkthrough checks. [Search indexing and AI citations](../site/README.md#search-discovery)
  remain unestablished.
- **Discovery:** [GitHub metadata](github-discovery.md) and the
  [skills.sh refresh workflow](skills-sh-refresh.md) have their own procedures.
  The [v0.2.9 publication check](releases/v0.2.9.md#publication-and-upgrade-verification)
  verified both installed packages. Both skills.sh listings still showed earlier
  text at the final check.
- **Project setup:** [AGENTS.md](../AGENTS.md), imported by [CLAUDE.md](../CLAUDE.md),
  records the maintenance rule. For existing JSONL records, see the
  [upgrade note](getting-started.md#older-jsonl-journal-setups).

## Evidence and limits

- [Evaluation results](evaluation-results.md) retain native trials, comparative
  studies, failures and grading limits. A skill-specific accuracy advantage,
  lower effort for intended users, reliable automatic instruction loading and
  general reliability remain unestablished. Separate mechanical checks from model
  behavior. [Refresh observations](refresh-observations-2026-10-26.md) keep the
  real-repository checks distinct from synthetic trials.
- [User feedback and owner confirmation](../evals/user-feedback/README.md#anonymous-early-feedback)
  describe useful continuity, cross-machine use and concrete friction. They do
  not establish measured effort savings or use of the frozen r1 trial materials.
- The qualified [Cursor trial](../evals/cursor/2026-11-17-free/README.md) and
  [Antigravity follow-up](../evals/antigravity/2026-11-17-long-timeout/README.md)
  retain loading and repeatability gaps. The
  [resume and troubleshooting guide](getting-started.md#verify-a-resumed-session)
  provides authored prompts whose human usefulness is unmeasured.

## Next actions

- Maintain the standalone workflow in ordinary use and address concrete issues
  with focused checks. The [unfamiliar-user trial materials](../evals/user-feedback/README.md#prepared-material-set-r1)
  are available for separately scoped follow-up. The
  [comparison protocol](../evals/discrimination-protocol.md) remains a separate proposal.
- [v1.0.0 validation](v1.0.0-readiness.md) and
  [Codex plugin runtime work](project-decisions.md#codex-plugin-runtime-deferral)
  remain deferred. The [older plugin candidate](plugin-candidate.md) retains its
  bounded Claude result and unresolved eligibility, activation and upgrade questions.
  Further native client trials, a web viewer and ChatGPT integration are outside
  the selected work.

## Canonical references

- [Decision history](project-decisions.md) · [Contributor rules](../CONTRIBUTING.md)
- [Overview](../README.md) · [Usage guide](getting-started.md) · [Standard](../skills/context-docs/references/standard.md)
- [Release history](releases/README.md) · [Changelog](../CHANGELOG.md) · [Deployment history](../site/README.md#latest-deployment)
- [Evaluation scenarios](../evals/README.md) · [Outside-contributor packet](../evals/external-validation/README.md)
