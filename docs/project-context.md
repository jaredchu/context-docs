# Project context

Current state reviewed: 2026-10-10. Cleanup was reviewed on October 9. Earlier
evaluation findings are retained from their linked reports, not rerun here.

## Purpose and scope

Context Docs is an experimental convention and reusable agent skill for maintaining
useful Markdown project knowledge across AI sessions. Retained content, factual
accuracy and consistency are the product goals; speed and brevity are secondary.
It adapts to existing layouts and distinguishes observations, approved decisions,
proposals and unknowns. Ordinary maintenance has no runtime dependency. The
optional journal helper requires Python 3.9+; no background service or sync exists.

This is a public open-source repository. Shared context should serve contributors
and skill users. Personal installations, backup locations and disposable session
state belong in local notes when still useful, rather than this entry point.
Relevant runtime constraints and failed evaluations remain shared evidence.

## Decisions

- Keep Markdown/Git authoritative and cloud integrations optional. A hosted memory
  service or retrieval backend needs a concrete use case.
- Keep logging optional. Its goal is efficient event capture for later
  investigation, not routine context savings. Broader integration requires need
  beyond Markdown/Git, native Claude/Codex evidence and compatibility with existing
  adopters. See the [journal requirements](event-journal-pilot.md#requirements-before-broader-integration).
- An explicit project logging setting wins. The opt-in auto preference enables
  JSONL only when no setting exists and Git confirms no repository; audits do not
  enable it. See the [packaged guide](../skills/context-docs/references/event-journal.md).
- Use GPT 6 Astra High and Claude Opus 5.5 for implementation and focused counterpart
  review as described in [AGENTS.md](../AGENTS.md#model-collaboration).
- Keep Jared Chu as creator/maintainer and credit actual AI contributions under
  the [attribution policy](../CONTRIBUTING.md#commit-attribution).
- Choose retained information for its audience, destination and lasting usefulness.
  The owner requested this guidance and cleanup before release on October 9.

[Decision history](project-decisions.md) preserves authority, rationale and earlier
approvals. An earlier release approval does not authorize a new publication.

## Current state

- Released bundle: [v0.1.6](releases/v0.1.6.md), containing core **0.1.6** and
  adoption **0.1.7**, with standard **0.1.1**. Release-commit remote CI passed;
  [PR #2](https://github.com/jaredchu/context-docs/pull/2) merged the reviewed changes.
- Core adds audience/destination guidance. Adoption preserves equivalent existing
  rules while making newly added instructions client-neutral. The earlier native
  Claude integration was merged in [PR #1](https://github.com/jaredchu/context-docs/pull/1).
- Core supports audit, initialize and maintain. Adoption is a sibling-dependent
  wrapper that adds guidance and a marker to instructions actually loaded by the
  client. [README](../README.md) owns installation and invocation details.
- The core package owns the standard, references, templates and optional journal
  helper. This repository enables JSONL through [AGENTS.md](../AGENTS.md); its
  `CLAUDE.md` imports those instructions. No other project's setting is implied.
- [Repository checks](../.github/workflows/checks.yml) cover packaging, versions,
  links, grader controls and report regeneration. They are mechanical checks;
  actual agent evaluations remain separate.

## Evidence and limits

The [changelog](../CHANGELOG.md) records per-version changes and validation;
[evaluation documentation](../evals/README.md) and the
[earlier study summary](evaluation-summary-2026-09-27.md) lead to detailed evidence.
Keep failed attempts and frozen conditions; do not convert small author-reviewed
studies into claims of general reliability or superiority over ordinary maintenance.

- Earlier reader studies often tied because raw evidence was available. The
  [public-source handoff pilot](evaluation-2026-09-27-public.md) did not establish
  readers consumed the handoffs; the [routing follow-up](evaluation-2026-09-27-routing.md)
  separates availability from verified reading.
- Native integration passed restricted loading and boundary gates, with retained
  factual errors and invocation limitations. The [guarded report](../evals/results/2026-09-28-native-guarded/README.md)
  supports supervised experimental use, not unrestricted-client reliability.
  Reliable implicit selection and cross-machine installed-path portability remain
  unestablished.
- Logging evaluations preserve capture, upgrade and read-gating results along with
  their failures. [Integration findings](../evals/results/2026-09-28-journal-integration/README.md)
  and [auto-preference results](../evals/results/2026-09-29-auto-preference/README.md)
  do not establish JSONL necessity or natural recording-cost advantage.
- The [October 9 adoption regression](../evals/results/2026-10-09-public-adoption/README.md)
  retains execution 4/4 and mechanical 3/4, plus separate Astra/Claude semantic
  assessments. The [v2 evaluator](../evals/public-adoption/protocol.md) handles
  supported fenced markers for future freezes only; original scores remain intact.
- The [October 10 audience/destination pilot](../evals/results/2026-10-10-audience/README.md)
  passed execution 5/5. Both counterpart reviewers accepted 19 target and 15 general
  criteria. The mixed case used an allowed handoff question; audit attempted no
  writes or history access. Five authored synthetic cases establish no broader
  reliability or comparative benefit.
- The [October 10 public-history comparison](../evals/results/2026-10-10-public-history/README.md)
  completed four native Claude Opus 5.5 handoffs across HTTPX and ripgrep, pairing
  ordinary maintenance with explicit core-skill reading. Execution gates passed
  4/4 with no denied actions; additional unsupported claims occurred in both
  methods. Separate semantic reviews preserve the failures. No reader benefit,
  native skill-discovery reliability or comparative accuracy advantage is established.
- Preserve the [private-pilot deployment-conflict miss](evaluation-2026-09-26.md)
  and [history-study scope violation](evaluation-2026-09-27-history.md) when assessing
  reliability. Perfect artifact scores do not establish full task compliance.
- [Evidence redactions](evidence-redaction-2026-10-09.md) identify normalized public
  copies, original hashes and unchanged scores. This is metadata cleanup, not a
  new evaluation or a claim that older Git history was sanitized.

## Next actions

The public-history comparison is complete; the released skills remain unchanged.
Seek cases and review independent of protocol authors before broader correctness
claims. Any follow-up needs a new frozen manifest and must preserve completed
results. The [discrimination protocol](../evals/discrimination-protocol.md) remains
a separate proposal.

## Canonical references

- [README and installation](../README.md)
- [Standard](../skills/context-docs/references/standard.md)
- [Decision history](project-decisions.md)
- [Contribution and validation](../CONTRIBUTING.md)
- [Per-version history](../CHANGELOG.md)
