# Working on Context Docs

- Read `README.md` and `docs/project-context.md` first.
- For context audits, initialization or maintenance, read and apply
  [this project's skill](skills/context-docs/SKILL.md). An audit leaves files unchanged.
- Keep installable skills under `skills/`. The core `context-docs` skill is
  self-contained; `adopt-context-docs` depends on its sibling `context-docs`.
  Package references with the skill that owns them, not only in repository docs.
- The standard is canonical in `skills/context-docs/references/standard.md`.
  Link to it instead of maintaining a second copy.
- Preserve the distinction between observed facts, owner decisions and proposals.
- Keep guidance applicable to varied project layouts. Do not add a universal
  rule for an isolated example without a demonstrated need.
- Validate skill metadata, packaged reference links and affected evaluation
  scenarios. Report static checks separately from actual agent evaluations.
- Use synthetic examples. Do not copy private project context into this repo.
- Update current project context when behavior, scope or status changes.
- Publication requires authorization from the task; these instructions grant none.

## Context documentation

Method: context-docs
Adopted: 2026-09-27
Entry point: docs/project-context.md
