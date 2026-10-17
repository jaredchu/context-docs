# Markdown progress regression scenarios

Scenarios for the progress feature; this full suite has not run. The revised
visual criteria below target unreleased core 0.2.1. A
[focused candidate smoke](smoke-0.2.1-2026-10-16/README.md) now passes these gates
on one copied-candidate create case per native client, with exact visual outputs.
The [October 16 smoke check](smoke-2026-10-16/README.md) exercises linked-view
creation and refresh in two guided Claude Code sessions, with one minor per-item
link-placement gap. The separate [installed v0.2.0 smoke](../installed-skills/2026-10-16-progress/README.md)
observes one guided linked-view creation in each of Codex and Claude Code, with
source links and preserved write boundaries. These small checks do not establish
a pass for every scenario below.
Use a disposable synthetic project and the packaged skill; preserve original
studies. Record actual client/model, input, output, changes and unmet criteria if
running these later. Do not grade exact headings, tree characters or prose.

## Visual acceptance criteria (core 0.2.1 candidate)

For an explicit visualization request, or maintenance of an already visual view,
inspect the rendered Markdown and its plain text. Ordinary maintenance of an
existing nonvisual view retains its format. Accept any compact tree, arrow path
or nested checklist that:

- Shows how the documented work contributes to the goal, with done and remaining
  conditions visible without reconstructing them from paragraphs.
- Places each blocker beside the work it stops, showing the supported prerequisite
  and next action. Labels absent or inferred relationships instead of inventing them.
- Keeps parallel conditions as branches; shows ordering only when supported.
  Proposed work stays outside required completion conditions unless approved there.
- Maps each item and relationship to a resolving, clickable source link. Source
  keys in a fenced diagram need an unambiguous Markdown link map outside the fence;
  link-looking text inside a code block alone fails this criterion.
- Uses text status labels and stays understandable without color, icons or a
  special renderer. A flat status table or prose alone fails visual acceptance,
  even if its status claims are correct.

Sparse sources may show the goal or path as unknown, with known work and its
sources; they must not invent completion conditions to satisfy the visual shape.
Read-only audits assess these criteria without writing. These revised criteria
have been exercised on the focused candidate create cases only; the other
scenarios below remain unexecuted against them. Earlier smoke results retain
their original scope and are not retroactive evidence for this visual gate.

## 1. Outcomes, learning and possible repetition

Fixture: use the three source sections of the [progress example](../../examples/progress.md)
as a synthetic project's existing context/evidence. Withhold its example view.

Request: "Use context-docs to visualize this project's progress in Markdown."

Check that the view links to sources, keeps the goal incomplete, distinguishes
the passed CSV check from unrun empty-input handling, retains the retry proposal,
and visually connects the blocked check to its missing-input prerequisite and
next action. Keep the two completion checks as parallel branches and the retry
proposal outside that path. Source keys must resolve through real links. Learning the correct path
is useful progress, not completed handling. Later repeated failures may be a
possible stall with the compared evidence/time range, not a definitive loop.

## 2. Existing view, separate file and repeat maintenance

Use scenario 1's two-check goal, owner decisions and source evidence: columns
passed, empty-input testing unrun and blocked on a missing representative input,
with obtaining/preparing that input as the next action. The project's entry point
links `notes/delivery.md`, its canonical grouped-bullet progress view containing
those same statuses, blocker and next action.
Request ordinary maintenance after supplying a later dated result stating that
the sample was provided and the empty-input check passed; then repeat with no
new facts. Run the separate visualization cases on the initial blocked fixture:
explicitly request visualization in that existing view, or a new linked view from
existing docs.

Check that maintenance updates the existing view and its justified completion
state, retains unrelated owner edits/decisions, and creates no parallel task list
or setup rewrite. Ordinary maintenance retains the grouped-bullet format. The
explicit visualization request makes relationships visible in the same section/file,
preserving owner edits and record locations. After the
new passing result, the old blocked status and next-action bullet must no longer appear
active, and the goal's two-check completion must be visible. The separate-file request is honored with discoverability and
source links. An identical repeat makes no edits or journal event.

## 3. Sparse, stale or conflicting evidence

Fixture: a project has no documented goal, Git history, journal or retained
attempt records. Its older note
claims deployment, while the only current evidence is configuration and a passing
unit check. Request a Markdown progress view and ask whether work is looping.

Check that goal, path, overall completion, deployment and repetition remain unknown
where unsupported. Preserve the older claim as dated/unverified or conflicting,
without treating it as current fact. No invented milestones, percentages, owners,
dependencies, live activity or history store; useful sourced work can still appear.
The visual must not invent arrows or make a passing unit check imply deployment.

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

## 8. Concise overview and preservation (core 0.2.3 candidate)

Use a synthetic project with a documented two-condition goal, one completed
condition, one blocked condition, a pending owner decision, and a detailed retained
evidence document containing test counts and dated review attempts. Ask for a
progress view, or adopt it without a separate visualization request.

Check that the overview makes the goal, meaningful outcomes, supported dependency,
blocker and next action easy to find, with clickable evidence links. It should not
reproduce the test/review chronology. Approval boundaries, relevant qualifications
and decision rationale remain findable, with unique information preserved in its
canonical location. Do not impose a word/line quota or add a new evidence store.

Repeat ordinary maintenance on an existing owner-edited table or linked view,
with one new result: retain its location, format and unrelated owner edits, update
only affected facts and create no duplicate tracker. A separate request for more
detail may provide it; concision is a default preference, not permission to hide
blockers or trim necessary detail from a complex project. A
[focused candidate smoke](smoke-0.2.3-2026-10-17/README.md) now exercises re-adoption
and linked-table refresh in both clients; progress checks pass with a Codex
temporary-file write/delete scope violation retained. Explicit extra detail and
other unexecuted branches remain unrun; earlier results retain their original scope.

## Validation boundary

Repository/package checks validate links, versions and self-contained references;
they do not execute these scenarios or prove visualization quality, automatic
selection, reliable stall detection or reduced user effort. A counterpart review
is artifact review, not a native behavioral run.
