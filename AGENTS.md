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
- Keep public context focused on users and contributors. Maintainer-specific
  operator preferences and bookkeeping belong outside this repository; retain
  appropriate public summaries and reproducible evidence when needed.
- Update current project context when behavior, scope or status changes.
- End a routine no-change refresh with a concise chat result, then stop. Follow
  the [refresh recording and publication boundary](docs/project-decisions.md#refresh-recording-and-publication-boundary);
  do not turn an unchanged check into another documentation or publication task.
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

## Agent working rules

- Keep one writer per change and hand off ownership explicitly. Reviewers return
  findings; the implementation owner validates and resolves them. Parallelize
  independent assignments without overlapping edits. Prefer narrow changes and
  reread/reconcile current contents after conflicts.
- Give substantial assignments clear editable scope, relevant context, acceptance
  criteria, expected evidence and a usage/time bound. Review the resulting patch
  and its important boundaries; repeat investigation only for a concrete gap.
- Have another reviewer assess consequential behavior, skill, evaluation or design
  changes against specific risks: correctness, regressions and unsupported claims.
  Give them the relevant diff, requirements and check results. Small fixes and
  routine wording, formatting or mechanical updates need proportionate checks,
  without a mandatory additional reviewer unless another project rule requires one.
- Verify findings against evidence before acting. Allow one initial review and
  one focused follow-up for material fixes. Stop and report unresolved issues
  rather than looping. Resolve technical disagreements through source inspection
  or focused checks within those bounds; ask the maintainer only for consequential
  scope or product choices.
- Do not change global settings, provision services or incur new costs without
  task authorization. Existing project safeguards and publication boundaries apply.
- Report checks and assistance actually used, including model identities and
  verification limits where relevant. Do not claim review that did not occur or
  silently substitute a specifically requested collaborator.

## Context documentation

Method: context-docs
Adopted: 2026-09-27
Entry point: docs/project-context.md
Event journal: jsonl
Event journal directory: .context/events
