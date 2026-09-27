# Project context

Last reviewed: 2026-09-27.

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

## Current state

- Skill supports audit, initialize and maintain operations.
- The [standard](../skills/context-docs/references/standard.md) defines document
  roles, evidence/decision distinctions and maintenance behavior.
- Two templates, an authored example and five behavioral evaluation scenarios
  are included. Templates are optional.
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
