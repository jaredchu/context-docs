# Markdown ticket lifecycle

Use a ticket when a work item needs to be resumed on its own across sessions.
Reuse an existing ticket or issue and follow the project's naming, storage and
link conventions. For smaller work, a next action in the existing context is
enough. Projects can use this workflow through their normal Context Docs rule.

## Open and maintain

Record scope, completion criteria, status and the next action in the ticket.
Include the blocker and what would unblock it when relevant. Link the ticket from
the existing progress view where it helps someone resume. Label proposals as
proposed. Update task details in the ticket and project outcomes in the progress
view. Keep audits read-only.

## Close and file

Close when the ticket's completion criteria have been met. Record the outcome
and link its evidence. Remove the link from active work and retain any references
needed to understand project outcomes or find the closed ticket. Refresh the
progress view if the project-level outcome changes.

Move completed tickets into a `done/` subfolder of the existing ticket directory
when requested or when the project already uses that convention. For a project
with `tickets/`, a request can be as simple as:

> Move the completed Markdown tickets to `tickets/done/`.

“Archive the resolved Markdown tickets” is also a request to file closed work.
Use the project's established archive convention when it applies. For a
`done/` move, check each ticket's recorded outcome and evidence. Move only
completed work and skip tickets already filed there. Leave tickets with unclear
completion, canceled or superseded work, and destination conflicts in place
and report relevant skips. If no destination is specified and the project has
no archive convention, use `done/` under its ticket directory for completed
work. Limit bulk filing to a request that covers multiple tickets.

Check known incoming links and outgoing relative links from the new location,
including anchors. Update editable references and keep the ticket at its
existing path when a known shared URL must stay usable. A move can break
bookmarks and links outside the repository. Report affected references you cannot
repair. Preserve the project's storage boundary. For local-only context, follow
the [local-only guide](local-only.md) and verify the destination is ignored and
untracked before moving anything.

## Reopen

When the original scope needs more work, preserve the earlier result as history,
update the status and next action, and restore the active link. If the ticket
was moved solely to mark completion, return it to the active ticket directory
when the same storage and link checks permit the move. If its path must stay
stable, restore the active link to that path and report the exception. For work
outside the original scope, keep the completed ticket and link a follow-up if
it needs its own handoff.
