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
- Two templates, an authored example and four behavioral evaluation scenarios
  are included. Templates are optional.
- Public repository: [jaredchu/context-docs](https://github.com/jaredchu/context-docs).
- Initial static validation passed on September 26: skill frontmatter/scaffold
  validation, UI metadata checks, 21 repository-local links, and four links in an
  isolated copy of the installable skill. The copied package retains its license.
- These are packaging checks. No independent behavioral evaluation, automatic
  selection result or cross-client compatibility result is claimed.

## Next actions

1. Run the synthetic scenarios in fresh agent sessions and record model/revision
   and observed results separately from the expected outcomes.
2. Pilot on an existing project with authorized access; assess preservation of
   decisions and blockers, factual correctness and maintenance effort.
3. Change the standard based on demonstrated friction. Evaluate a cloud adapter
   only after a concrete retrieval or cross-machine workflow need is established.

## Canonical references

- [README and installation](../README.md)
- [Skill entry point](../skills/context-docs/SKILL.md)
- [Evaluation scenarios](../evals/README.md)
- [Contribution guidance](../CONTRIBUTING.md)
