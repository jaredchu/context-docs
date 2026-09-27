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
- Initial static validation passed on September 26: skill frontmatter/scaffold
  validation, UI metadata checks, 21 repository-local links, and four links in an
  isolated copy of the installable skill. The copied package retains its license.
- An eight-run paired maintenance pilot on temporary local-project documentation
  copies is complete. Both arms met all 30 controlled checks; the skill produced
  smaller additions, but missed a specific conflict that the broader cleanup
  baseline resolved. See the [dated evaluation](evaluation-2026-09-26.md).
- Model runs were fresh and separate; semantic review was by the authoring agent,
  not a blinded judge. General superiority, automatic selection and cross-client
  compatibility remain unestablished. Original project files were unchanged.
- The [public Harbor suite](../evals/suite/README.md) completed 48 trials / 60
  agent invocations with frozen v0.1.0 instructions. Both arms passed 24/24 tasks
  under mechanical checks and author-reviewed semantic criteria. The skill used
  more time/tokens and added more words in five of eight task categories.
  See [results, reproducible evidence and limits](evaluation-2026-09-27.md).
- Public fixtures are small development cases, not held-out projects. No general
  superiority or equivalence is established. The 48-trial README table is generated from
  recorded trials/reviews and retains the earlier natural-cleanup miss.
- The [concision follow-up](evaluation-2026-09-27-concise.md) completed 12 trials /
  20 sessions on new 572–676-word synthetic projects. Original and candidate both
  passed 6/6 trials; candidate median growth was lower for release guidance and
  initialization, unchanged for repeated maintenance. It met the frozen acceptance
  rule and is adopted as experimental skill v0.1.1. Supporting resources and the
  standard remain v0.1.0. This is an implementation choice supported by these tests.
- v0.1.1 has a shorter entry point (417 vs 645 words), but was slower and emitted
  more output tokens in the follow-up. Initialization did not shrink in every
  attempt. No general speed, cost or correctness advantage is established.
- The harness now captures actual input before each pass and verifies continuity
  against actual prior output. Reference/no-op controls and preservation checks
  passed. The earlier 48-trial scores remain unchanged with their original limits.
- Recorded-input audits passed for all 80 sessions across the two public studies:
  no host global instructions were injected. Authoring/review influence and shared
  scope/preservation prompts remain limitations; normal global-instruction use has
  not been evaluated.

The [quality-first protocol](../evals/quality-protocol.md) defines the next study:
matched unmaintained, ordinary-maintenance and Context Docs arms, with the same
underlying evidence and fresh readers. It is a plan, not an executed evaluation.
The README now leads with knowledge quality and separates historical maintenance
checks from unmeasured reader benefits.

## Next actions

1. Implement the quality-first study on scattered, conflicting and absent-context
   starting conditions. Freeze matched evidence, reader questions and critical
   failures before running. Use independent or externally contributed fixtures
   where available; measure stored knowledge and fresh-reader answers. Keep both
   completed studies and the private pilot miss visible.
2. Evaluate automatic selection, other models, normal global-instruction setups
   and longer maintenance sequences when those become relevant. Current evidence
   covers explicit use on one model and up to three passes.
3. Monitor v0.1.1 on real work before further prompt tuning. Avoid adding rules for
   isolated examples. Cloud adapters still need a concrete retrieval or cross-machine
   use case.

## Canonical references

- [README and installation](../README.md)
- [Skill entry point](../skills/context-docs/SKILL.md)
- [Evaluation scenarios](../evals/README.md)
- [Quality-first comparison protocol](../evals/quality-protocol.md)
- [September 26 local-project benchmark](evaluation-2026-09-26.md)
- [September 27 public Harbor evaluation](evaluation-2026-09-27.md)
- [Concision comparison and v0.1.1 adoption](evaluation-2026-09-27-concise.md)
- [Contribution guidance](../CONTRIBUTING.md)
