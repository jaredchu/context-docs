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
- Credit Claude on every commit it helps implement, validate or review, including
  completed validation or review without file edits, following the same
  [commit attribution policy](CONTRIBUTING.md#commit-attribution). Include both
  attribution trailers when both models assisted, each exactly once.
- Publication requires authorization from the task; these instructions grant none.

## Model collaboration

Use GPT 6.1 Sol and Claude Opus 5.5 with these suggested responsibilities:
This policy applies only to this project. Preserve its existing safeguards;
do not change global settings.

| Work | Suggested responsibility |
| --- | --- |
| Coordination, scope, task breakdown, integration | Sol 6.1 |
| Small fixes and straightforward changes | Sol, working alone unless project rules require independent review |
| Substantial implementation or sustained investigation | Opus 5.5, with a bounded assignment |
| Review of consequential changes | The other model, focused on specific risks |
| Validation and context-docs maintenance | Sol, using actual tests and accepted decisions |

- Roles may change when the task warrants it.
- Sol coordinates without redoing all of Opus's work. Hand over a compact task
  with clear editable scope, relevant context, acceptance criteria, expected evidence
  and a usage/time bound;
  receive a patch plus evidence, then inspect the important boundaries and
  specific risks. Repeat investigation only to resolve a concrete gap or concern,
  so coordination does not consume the ChatGPT allowance it is meant to preserve.
- Keep one writer per change. Reviewers return findings; the implementation owner
  validates and resolves them. Sol handles integration and validation.
  Parallelize independent assignments without overlapping edits.
- Have the other model review consequential behavior, skill, evaluation or design
  changes. Give the reviewer the relevant diff, requirements and check results;
  focus on specific risks, including correctness, regressions and unsupported
  claims. Routine wording, formatting and mechanical updates need only
  proportionate local checks.
- Verify review findings against evidence before acting. Allow one initial review
  and one focused follow-up for material fixes. Stop and report unresolved issues
  rather than looping. Resolve technical disagreements through source inspection
  or focused checks within those bounds; ask the project owner only for
  consequential scope or product choices.
- Use existing subscription-authenticated access. Do not use Astra, API fallback
  or additional spending without the project owner's explicit request.
- Report the models actually used and any unavailable collaborator; do not
  silently substitute another model or claim review that did not occur.

The objective is useful completed work from both subscriptions while reducing
pressure on the owner's ChatGPT allowance. Better quality and allowance savings
remain goals to verify, not assumed benefits.

## Context documentation

Method: context-docs
Adopted: 2026-09-27
Entry point: docs/project-context.md
Event journal: jsonl
Event journal directory: .context/events
