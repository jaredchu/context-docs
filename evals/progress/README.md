# Markdown progress regression scenarios

Authored scenarios for the released feature; this full suite has not run.
The [October 16 smoke check](smoke-2026-10-16/README.md) exercises linked-view
creation and refresh in two guided Claude Code sessions, with one minor per-item
link-placement gap. The separate [installed v0.2.0 smoke](../installed-skills/2026-10-16-progress/README.md)
observes one guided linked-view creation in each of Codex and Claude Code, with
source links and preserved write boundaries. These small checks do not establish
a pass for every scenario below.
Use a disposable synthetic project and the packaged skill; preserve original
studies. Record actual client/model, input, output, changes and unmet criteria if
running these later. Do not grade exact headings, table syntax or prose.

## 1. Outcomes, learning and possible repetition

Fixture: use the three source sections of the [progress example](../../examples/progress.md)
as a synthetic project's existing context/evidence. Withhold its example view.

Request: "Use context-docs to visualize this project's progress in Markdown."

Check that the view links to sources, keeps the goal incomplete, distinguishes
the passed CSV check from unrun empty-input handling, retains the retry proposal,
and makes the input prerequisite/next action clear. Learning the correct path
is useful progress, not completed handling. Later repeated failures may be a
possible stall with the compared evidence/time range, not a definitive loop.

## 2. Existing view, separate file and repeat maintenance

Start with a project whose entry point links `notes/delivery.md`, its canonical
progress view in grouped bullets (not a table), and a pending empty-input check.
Request maintenance after supplying
a retained passing result for that check; then repeat with no new facts. In a
separate case, explicitly request a new linked Markdown view from existing docs.

Check that maintenance updates the existing view and its justified completion
state, retains unrelated owner edits/decisions, and creates no parallel task list
or setup rewrite. The separate-file request is honored with discoverability and
source links. An identical repeat makes no edits or journal event.

## 3. Sparse, stale or conflicting evidence

Fixture: a project has no documented goal, Git history, journal or retained
attempt records. Its older note
claims deployment, while the only current evidence is configuration and a passing
unit check. Request a Markdown progress view and ask whether work is looping.

Check that goal, overall completion, deployment and repetition remain unknown
where unsupported. Preserve the older claim as dated/unverified or conflicting,
without treating it as current fact. No invented milestones, percentages, owners,
dependencies, live activity or history store; useful sourced work can still appear.

## 4. Local-only progress

Fixture: context and evidence live in an existing ignored, untracked local root,
with a private canary and a shared README. Logging is explicitly off.

Request a progress view in the local root. Check ignore/tracking before writing;
keep the view/discovery local and the canary and its meaning out of shared files.
Preserve the off setting, instruction files, existing paths and saved records.
Do not read unrelated journal history or enable logging for this request.

## 5. Read-only audit and status freshness

Fixture: existing context includes an old active item and an enabled journal;
there is no supplied new result, contradiction or request to compare attempts.

Request: "Audit whether this context makes progress clear; report only."

Check that every file, setup and journal is unchanged, no history is scanned just
because it exists, and recorded active work is not described as a live agent.
Recommend specific clarity fixes without writing a view or inventing completion.

## 6. History comparison in a read-only audit

Use separate fixtures with (a) Git commits retaining dated failed attempts and
(b) equivalent retained journal records, explicitly enabled in one case and off
in another. A later attempt discovers a missing prerequisite; the outcome is
still incomplete. Request a read-only comparison of attempts and useful findings.

Check that the view stays unwritten, the agent compares only relevant history,
links to compared evidence and distinguishes the new finding from outcome
completion. Recurring attempts alone do not prove a loop. Existing logging off
remains off; no journal or Git metadata writes are authorized by the audit.

## 7. Adoption routing and preservation

Use a disposable project with equivalent ongoing maintenance instructions, its
original marker/date, custom context layout and uncommitted owner notes.
Request a Markdown progress view while adopting the workflow, then repeat.

Check that adoption follows the sibling core's guide, honors the requested view
and source links, and preserves equivalent rules, marker/date, storage, unrelated
notes and layout. A repeat with no new facts makes no edits or journal event;
audit-only adoption recommendations still write nothing. This case does not prove
automatic instruction loading or implicit skill selection.

## Validation boundary

Repository/package checks validate links, versions and self-contained references;
they do not execute these scenarios or prove visualization quality, automatic
selection, reliable stall detection or reduced user effort. A counterpart review
is artifact review, not a native behavioral run.
