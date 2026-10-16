# Progress views in Markdown

Turn saved project knowledge into a readable view of progress toward its goal.
Use the entry point and relevant linked documents as evidence. Markdown stays
authoritative; this feature writes reviewable files during an authorized session,
not a live dashboard or a separate tracking system.

## Choose the destination

Reuse a suitable section, such as current work or milestones. Write a separate
Markdown file when requested or when it makes a larger context easier to navigate;
link it from the entry point and link its summaries back to canonical details.
Do not require `progress.md`, move existing records, or maintain duplicate task
lists with independent state. If facts already live in the view, update them there.

Keep the existing audience and storage choice. For local-only context, apply the
[local-only guide](local-only.md): verify the view is ignored and untracked and
use local discovery. A shared progress summary must not expose private/local-only
content, including paraphrases, just because the source documents are accessible.

## Show what the sources support

Choose a small table, checklist or grouped bullets to fit the project. Include
these when documented and useful, without requiring empty sections:

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
current facts. Date only the
snapshot or evidence actually checked. An active status means recorded work in
that snapshot, not proof an agent is currently running. Simple Markdown must
remain useful without a special renderer; a diagram is optional for relationships
that a table or list does not explain clearly.

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
