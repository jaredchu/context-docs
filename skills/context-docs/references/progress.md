# Progress views in Markdown

Turn saved project knowledge into a readable view of progress toward its goal.
Use the entry point and relevant linked documents as evidence. Markdown stays
authoritative; this feature writes reviewable files during an authorized session,
not a live dashboard or a separate tracking system.

## Adoption: a small inline view by default

During adoption, when the context documents a goal and enough supported work,
status or next-step facts to show a useful path, create a simple inline tree,
arrow path or nested checklist without requiring a separate visualization request.
Use a suitable existing section and its terminology; preserve headings, owner
edits, decisions, rationale and canonical record locations. Adapt the relevant
status lines in place rather than adding a second account of the same work.

Preserve an existing task list, status table, diagram or section/file designated
as the project's progress view, including nonvisual or linked views. Ordinary
status sentences in broader context may be grouped into a small inline path;
do not reshape an established view just for adoption. When that distinction is
unclear, retain the existing format. Keep detailed facts authoritative in one
place; a compact summary may link to them, not maintain an independent task list. Where the view
itself owns a fact, update it there and link to its supporting evidence.

If the goal is undocumented or the known work cannot support a useful path,
keep the supported facts in the existing context and skip the new view. Do not
invent a goal, populate empty progress scaffolding or infer completion conditions
merely to satisfy this default. Honor an explicit request to omit a view or use a
separate Markdown file, and preserve local-only storage boundaries.

An explicit adoption run may add a missing supported view even when an equivalent
maintenance rule and adoption marker already exist; preserve those setup records.
Once the view is current, repeating adoption with no new facts makes no edits.
After adoption, refresh the view alongside affected context during authorized
everyday maintenance; no repeated progress request is needed. Installation or
upgrade alone does not apply this default to projects, and audit-only adoption
remains read-only.

## Choose the destination

Reuse a suitable section, such as current work or milestones. Write a separate
Markdown file when requested or when it makes a larger context easier to navigate;
link it from the entry point and link its summaries back to canonical details.
Do not require `progress.md`, move existing records, or maintain duplicate task
lists with independent state. If facts already live in the view, update them there.

Routine maintenance updates the existing view in its current format. Reshape it
into a visual path when a visualization is requested, within the same agreed
section or file and preserving owner edits and canonical record locations.
Once a visual path exists, maintain that shape as relevant facts change; an
identical repeat with no durable change makes no edits.

Keep the existing audience and storage choice. For local-only context, apply the
[local-only guide](local-only.md): verify the view is ignored and untracked and
use local discovery. A shared progress summary must not expose private/local-only
content, including paraphrases, just because the source documents are accessible.

## Make the path visible

For a progress visualization, lead with a compact text tree, arrow path or nested
Markdown checklist that makes the structure visible: which work contributes to
the documented goal, what is done, what is blocked and what to do next. Put a
blocker's prerequisite beside the affected work. A flat status table or prose
alone does not meet this request; a table may supply supporting detail.

Use branches for parallel completion conditions. Use arrows or `depends on` only
for supported ordering or dependencies; label and cite inferred relationships.
Keep proposals outside the required completion path unless approved as part of
it. When the goal or a relationship is unknown, show that unknown instead of
inventing a path. Choose the smallest shape that fits the known work.

Keep it useful as plain text: words such as `DONE`, `BLOCKED`, `PROPOSED` and
`NEXT` carry status even without color, icons or a diagram renderer. Illustrative
shape only; replace these labels and source keys with the project's evidence:

```text
Goal: pilot export (incomplete) [G]
|-- DONE     Columns check [A]
`-- BLOCKED  Empty-input check [B]
    `-- NEXT Prepare missing sample, then run check [B]

Outside completion path: PROPOSED five retries [G]
```

Use real Markdown source links beside or below the visual. A link written inside
a fenced text diagram is not clickable: map each source key such as G/A/B to its
linked document or section outside the fence. Every summarized item and dependency
must be traceable; several may share a source. For a nested Markdown checklist,
links can sit inline. Do not add a second independent status list just for citations.
Mermaid is optional; retain a readable text explanation if using a special renderer.

## Show what the sources support

Include these when documented and useful, without requiring empty sections:

- The goal and conditions that would establish completion.
- Milestones or steps, distinguishing completed, active, blocked and proposed work.
- Current focus, the next actionable step and its unresolved dependency or decision.
- Recent meaningful advances with supporting evidence or source links.

Link each summarized item to its source document/section or retained result.
Explain a checked item or done status through an outcome or completion condition;
an attempt, a passing narrow check or an approved plan is not the whole outcome.
Keep proposal/approval status separate from implementation status. Do not invent
goals, milestones, percentages, deadlines, owners or dependencies to fill the view.
When missing information affects interpretation, say what is unknown; an absent
goal does not authorize deriving one from code or choosing it for the owner.

Show dependencies when recorded, or label an inference and cite the evidence
supporting that relationship; omit unsupported guesses. Note stale, conflicting
or unverified claims where they affect an item rather than presenting them as
current facts. Date only the snapshot or evidence actually checked. An active status means recorded work in
that snapshot, not proof an agent is currently running.

## Assess possible stalls only with history

A current snapshot can show a blocker, but cannot by itself establish a loop.
When a progress question calls for comparing attempts, inspect relevant Git
history, retained dated attempt records in existing docs, or an existing optional
journal under its [history rules](event-journal.md). Retained history can be read
for that question even when capture is now off; keep the logging setting unchanged.
Do not enable logging, scan all history during routine maintenance, or create a
history store just to populate the view. No history means repetition is unknown.

Distinguish activity (another attempt), useful learning (new evidence that changes
the next step), and a completed outcome (the documented condition is met).
Repeated attempts without a new result or useful finding can be a **possible
stall**. Link the compared evidence and its time range, explain what did not
advance and identify a useful next check or unresolved decision when supported.
Repetition alone is not definitive proof of a loop; necessary recurring work and
unrecorded learning are possible. Do not change status based on attempt counts
alone or call useful learning completed delivery.

## Keep the view useful

After meaningful work, update affected statuses, blockers, source links and next
actions alongside the canonical context. Keep historical detail in its existing
evidence location rather than appending a session diary. If the view is current
and nothing durable changed, leave it and the journal untouched. An audit explicitly
asking about repetition may read the relevant history under the same rules, but
writes no view, journal event or setting. Other audits do not scan history merely
because it exists.
