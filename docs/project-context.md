# Project context

Last reviewed: 2026-09-27.

## Purpose and scope

Context Docs provides a reusable skill and Markdown convention for project
continuity across AI sessions. It addresses inconsistent document structures and
maintenance drift while adapting to existing project layouts.

The public package contains instructions, references, templates and synthetic
examples. A hosted memory service, automatic scheduler and retrieval backend are
outside the first version's scope.

## Decisions

Approved by the project owner in the founding request on September 26, 2026:

- Publish an open-source project under `jaredchu` named `context-docs`.
- Begin with a reusable context standard and maintenance skill.
- Keep Markdown/Git authoritative and cloud integrations optional for later.

Initial implementation choices: MIT license; skill at `skills/context-docs`;
experimental version 0.1.0; no runtime dependencies. These are choices made while
implementing the authorized first version, not additional attributed owner quotes.

On September 27 the owner accepted the proposed eight-task, two-condition,
three-attempt evaluation. Harbor is the selected execution framework; evaluation
dependencies are separate from the instruction-only skill package.

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
  superiority or equivalence is established. The README table is generated from
  recorded trials/reviews and retains the earlier natural-cleanup miss.
- Controls passed before scored runs. Later multi-step mechanical change checks
  compare against reference-stage input; actual input capture remains a harness
  improvement. Full task scoring also requires semantic review of progression.

## Next actions

1. Capture actual per-step input snapshots and add larger held-out fixtures with
   dispersed/ambiguous evidence; keep the completed baseline intact.
2. Evaluate a fresh reader's answers, automatic selection, other models and longer
   maintenance sequences. The current study covers explicit use on one model.
3. Test any verbosity reduction as a separate skill candidate, especially for
   workflow guidance and initialization. Do not add more instructions merely
   because the private pilot missed one conflict. Cloud adapters still require a
   concrete retrieval or cross-machine need.

## Canonical references

- [README and installation](../README.md)
- [Skill entry point](../skills/context-docs/SKILL.md)
- [Evaluation scenarios](../evals/README.md)
- [September 26 local-project benchmark](evaluation-2026-09-26.md)
- [September 27 public Harbor evaluation](evaluation-2026-09-27.md)
- [Contribution guidance](../CONTRIBUTING.md)
