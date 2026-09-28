# Project context

Last reviewed: 2026-09-28.

## Purpose and scope

Context Docs provides a reusable skill and Markdown convention for project
continuity across AI sessions. Its primary goal is retaining useful content and
improving documentation accuracy and consistency. It addresses inconsistent
structures and maintenance drift while adapting to existing project layouts.

The public package contains instructions, references, templates and synthetic
examples. A hosted memory service, automatic scheduler and retrieval backend are
outside the first version's scope.

## Decisions

Approved by the project owner in the founding request on September 26, 2026:

- Publish an open-source project under `jaredchu` named `context-docs`.
- Begin with a reusable context standard and maintenance skill.
- Keep Markdown/Git authoritative and cloud integrations optional for later.

Initial implementation choices: MIT license; skill at `skills/context-docs`;
experimental version 0.1.0 at launch; no runtime dependencies. These are choices
made while implementing the authorized first version, not additional attributed
owner quotes.

On September 27 the owner accepted the proposed eight-task, two-condition,
three-attempt evaluation. Harbor is the selected execution framework; evaluation
dependencies are separate from the instruction-only skill package.

On September 27 the owner clarified that retained content, documentation accuracy
and consistency are the product goals. Speed and concision are secondary diagnostics.
Future comparisons should include scattered, stale or missing documentation and
measure the resulting record and fresh readers' supported answers. This clarification
does not change the already executed studies or their frozen acceptance criteria.

On September 28 the owner delegated authority to contribute changes to this
repository directly, including commits and pushes to branches. That delegation
covers contribution mechanics; it does not approve new product claims. Changes
made under it are recorded as ordinary implementation choices, and proposals
still need owner acceptance.

## Current state

- Core skill supports audit, initialize and maintain operations.
- Optional [adoption skill](../skills/adopt-context-docs/SKILL.md), experimental
  v0.1.3, applies the core method and merges ongoing maintenance into the project's
  loaded agent instruction file. Install it alongside `context-docs`; it is not standalone.
  Completed setup now records a small adoption marker with the original date and
  actual entry point. Missing markers do not imply non-adoption; unrecorded dates
  remain unknown, and audit-only requests never create markers.
  New sections prefer a `Context maintenance` heading, marker, then instructions;
  existing equivalent layouts stay intact. This v0.1.2 presentation preference
  received static validation only; model results below cover earlier versions.
  v0.1.3 places the rule and marker in the instruction file the client actually
  loads, rather than assuming `AGENTS.md`, and states the rule without a
  client-specific invocation prefix. Claude Code loading depends on version,
  configuration and local instruction files; the [installation guidance](../README.md#install-in-claude-code)
  records the documented defaults and exceptions checked on 2026-09-28.
  Its [instruction-file cases](../evals/adoption/instructions.py) pass ten static
  grader controls. The [v0.1.3 merge review](../evals/results/2026-09-28-adoption-v013/README.md)
  ran nine model sessions across routing and older marker cases: eight met frozen
  acceptance. All repeats and the audit preserved bytes. Split-file routing passed
  semantic review but failed immutable-heading and installed-link checks. A
  [separate follow-up](../evals/results/2026-09-28-adoption-v013-followup/README.md)
  passed four routing/repeat sessions after making constraints explicit and
  validating declared installed references by hash across links, code spans and
  prose. Both repeats preserved bytes and dates. Skills and the original failed
  result remain unchanged. The reviewer now recommends merging within the
  documented experimental scope; this is not an owner merge decision.
  The earlier v0.1.0 [adoption regression](../evals/results/2026-09-27-adoption/README.md): two synthetic
  projects passed adoption and unchanged repeat passes across four fresh sessions.
  These author-reviewed cases do not establish automatic selection or general reliability.
  The [marker regression](../evals/results/2026-09-27-adoption-marker/README.md)
  retains an initial equivalent-guidance rewrite and ambiguous test dates. Ten
  sessions include targeted follow-ups; the final revision passed marker-only
  adoption and read-only auditing on the two affected unmarked cases.
- The [standard](../skills/context-docs/references/standard.md) defines document
  roles, evidence/decision distinctions and maintenance behavior.
- Two templates, an authored example and five behavioral evaluation scenarios
  are included. Templates are optional.
- Packaging, links, published-table agreement and the container-free study
  self-tests run as [static repository checks](../evals/checks/static_checks.py)
  in GitHub Actions since 2026-09-28. Package checks enforce boundaries including
  nested references and the adoption skill's declared sibling dependency; version
  checks compare current README status and latest per-skill changelog entries.
  Regression controls cover escaped package links and stale version declarations.
  These mechanical repository checks establish nothing about agent behavior.
- A [native Claude Code smoke test](../evals/claude-code/README.md) exists for skill
  discovery and invocation, rule placement in Claude-only and mixed instruction
  projects, repeat preservation and audit-only read-only behavior. It reuses the
  shared adoption fixtures, and its harness and static controls pass. Observed on
  2026-09-28: no model session has been executed, because the Claude Code CLI
  available here could not authenticate, so the harness records six execution
  failures rather than behavior. Client behavior stays unestablished until it runs.
- Installation into Claude Code is documented and its packaging validated;
  no evaluation has been executed on any client other than Codex.
- Public repository: [jaredchu/context-docs](https://github.com/jaredchu/context-docs).
- Current package: experimental skill v0.1.1; standard/resources remain v0.1.0.
  The package is instructions only, with no background maintenance or sync.
- Completed studies cover initialization, stale/conflicting guidance, decision
  preservation, uncommitted work, links, audit-only behavior and repeated maintenance.
  The [dated evaluation summary](evaluation-summary-2026-09-27.md) preserves all
  prior study summaries, frozen versions, outcomes and validation details.
- Reviewed results support supervised use, but establish no general accuracy,
  speed, cost or correctness advantage over competent ordinary maintenance.
  Reader results often tie because common source evidence remains available.
- Retain the [private-pilot deployment-conflict miss](evaluation-2026-09-26.md)
  and [history-study temporary out-of-scope backup](evaluation-2026-09-27-history.md)
  when assessing reliability; perfect content scores do not prove full compliance.
- Automatic skill selection, cross-client behavior and long-term maintenance
  remain unestablished. Prior controlled model runs excluded host/global
  instructions; authoring and review were not independent or fully blinded.

## Next actions

1. Monitor v0.1.1 on real work before further prompt tuning. Avoid adding rules for
   isolated examples. Cloud adapters still need a concrete retrieval or cross-machine
   use case.
2. Seek independently contributed histories from other projects and condition-blind
   review before expanding correctness claims. Keep common raw-evidence access,
   verified context reading, a competent ordinary baseline and frozen criteria.
   Repeating the current searchable questions is unlikely to distinguish accuracy.
   Include command-scope review alongside project-file checks; the temporary backup
   violation shows those mechanical rewards do not establish full task compliance.
   Preserve all earlier results and the original private-project miss.
3. Evaluate automatic selection, other models, normal global-instruction setups
   and longer maintenance sequences when those become relevant. Current evidence
   covers explicit use on one model and up to four passes.
4. Proposed, not yet approved: address the three conditions that hold reader and
   document scores at a ceiling before running further comparisons. The shared
   task prompts already state much of the skill's guidance to both arms, the
   fixture evidence labels its own approval and observation status, and the
   question sets stay answerable from small raw inputs. Until those change, a tie
   is the expected result and cannot distinguish the methods. See the
   [discrimination protocol](../evals/discrimination-protocol.md).
5. Preserve the distinction between the initial v0.1.3 failure and the passing
   follow-up under explicit file constraints. Native Claude Code behavior and
   installed-path portability across machines remain untested; do not describe
   either as evaluated support.
6. Execute the native Claude Code smoke test on a CLI that can authenticate, then
   publish its sessions, failures and explicit review. Freeze the built protocol
   first. Six sessions on one client with one attempt each would be a smoke test,
   not a comparison: no accuracy or reliability claim follows from it.

## Canonical references

- [README and installation](../README.md)
- [Skill entry point](../skills/context-docs/SKILL.md)
- [Evaluation scenarios](../evals/README.md)
- [Completed quality and fresh-reader study](evaluation-2026-09-27-quality.md)
- [Larger public-source pilot](evaluation-2026-09-27-public.md)
- [README routing and verified reading](evaluation-2026-09-27-routing.md)
- [Public decision histories across sessions](evaluation-2026-09-27-history.md)
- [Quality-first comparison protocol](../evals/quality-protocol.md)
- [September 26 local-project benchmark](evaluation-2026-09-26.md)
- [September 27 public Harbor evaluation](evaluation-2026-09-27.md)
- [Concision comparison and v0.1.1 adoption](evaluation-2026-09-27-concise.md)
- [Contribution guidance](../CONTRIBUTING.md)
- [Per-version changelog](../CHANGELOG.md)
- [Proposed discrimination protocol](../evals/discrimination-protocol.md)
- [Native Claude Code smoke test](../evals/claude-code/README.md)
- [September 28 Claude Code handoff and open decisions](handoff-2026-09-28-claude-code.md)
