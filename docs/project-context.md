# Project context

Last reviewed: 2026-09-26.

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
- The README presents the paired pilot results and known miss explicitly.
  [Framework research](../evals/frameworks.md) recommends Harbor for a public
  custom suite, with SkillsBench as a methodological reference. This is a
  recommendation; no framework integration or new model run is complete.

## Next actions

1. Implement public fixtures and verifiers, beginning with the explicit conflict
   regression. Validate reference and failing controls before model runs; use the
   proposed framework protocol rather than another ad hoc private-data run.
2. Evaluate audit-only behavior, initialization and automatic selection separately;
   measure downstream reader accuracy and repeated maintenance effort.
3. Change the standard based on demonstrated friction. Evaluate a cloud adapter
   only after a concrete retrieval or cross-machine workflow need is established.

## Canonical references

- [README and installation](../README.md)
- [Skill entry point](../skills/context-docs/SKILL.md)
- [Evaluation scenarios](../evals/README.md)
- [September 26 local-project benchmark](evaluation-2026-09-26.md)
- [Contribution guidance](../CONTRIBUTING.md)
