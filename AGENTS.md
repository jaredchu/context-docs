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
- For optional journal work, follow the [logging goals](docs/event-journal-pilot.md#efficient-logging-goals):
  efficient, reliable event capture for later investigation. Do not judge logging
  by routine current-context improvement or context savings.
- Before broadening logging integration, apply the [journal requirements](docs/event-journal-pilot.md#requirements-before-broader-integration):
  establish need beyond Markdown/Git, evaluate native Claude and Codex behavior,
  and preserve projects that already adopted Context Docs.
- Keep guidance applicable to varied project layouts. Do not add a universal
  rule for an isolated example without a demonstrated need.
- Validate skill metadata, packaged reference links and affected evaluation
  scenarios with `python3 evals/checks/static_checks.py`; CI runs it on every push.
  Report static checks separately from actual agent evaluations.
- Record each skill change in `CHANGELOG.md` with the version it lands in and what
  was actually tested. Keep each skill's `VERSION` file in step with it.
- Use synthetic examples. Do not copy private project context into this repo.
- Update current project context when behavior, scope or status changes.
- For commits containing Codex-assisted work, follow the
  [commit attribution policy](CONTRIBUTING.md#commit-attribution): add
  `Co-authored-by: Codex <noreply@openai.com>` exactly once, preserving the human
  author and existing co-author trailers. Do not add it to work Codex did not
  assist or rewrite existing history solely to add credit.
- Publication requires authorization from the task; these instructions grant none.

## Context documentation

Method: context-docs
Adopted: 2026-09-27
Entry point: docs/project-context.md
Event journal: jsonl
Event journal directory: .context/events
