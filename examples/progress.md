# Markdown progress example

Synthetic, authored example of intended output, not an executed agent evaluation.
These fictional source notes are included here so every item can link to evidence;
in a real project, link to the existing documents and results instead.

## Source: goal and decisions

The owner wants a pilot CSV export that preserves `id,value` columns and handles
empty input. Completion requires both checks to pass. Five automatic retries
are proposed but have not been approved or implemented.

## Source: checks and open work

The CSV columns check passed on fictional October 1. Empty-input testing has not
run: a representative synthetic input is missing. Next, prepare that input and
run the check. Configuration and test results do not establish deployment.

## Source: retained attempt notes

Fictional September 29: an attempt failed because the input path was wrong;
the failure identified the required path, which is useful learning.
September 30 and October 1: attempts used the corrected path but still lacked
the representative input. Neither recorded a new result or useful finding.
These supplied notes cover only these attempts, not all project activity.

## Example Markdown view

Snapshot of the fictional October 1 evidence above; not live agent activity.

**Goal:** deliver the pilot CSV export with both completion checks passing.
[Goal and completion conditions](#source-goal-and-decisions).

```text
Pilot CSV export [G]                       GOAL INCOMPLETE
|
|-- DONE     CSV columns check [C]
|
`-- BLOCKED  Empty-input check [E]
    `-- NEEDS representative input [E]
        `-- NEXT prepare input, then run empty-input check [E]

Outside the completion path:
PROPOSED five retries [G] (not approved or implemented)
```

Sources for the visual:

- **G:** [Goal, both completion conditions and the separate retry proposal](#source-goal-and-decisions).
- **C:** [Passed columns check](#source-checks-and-open-work); this completes one check, not the goal.
- **E:** [Unrun empty-input check, missing input and next action](#source-checks-and-open-work).

The two checks are parallel completion conditions; neither is shown as a
prerequisite for the other. The missing input blocks only the empty-input check.
`NEEDS` marks that prerequisite; `NEXT` marks the action to take.
Deployment remains [unverified](#source-checks-and-open-work).

**Meaningful advance:** the first failed attempt established the correct input
path. That narrowed the problem without completing empty-input handling.
[Retained attempt notes](#source-retained-attempt-notes).

**Possible stall:** September 30–October 1 repeated the missing-input failure
without a recorded new finding. These notes suggest revisiting the prerequisite;
they do not prove a loop or rule out unrecorded work.
[Compared attempts](#source-retained-attempt-notes).

**Current focus and next action:** prepare the missing synthetic input, then test
empty-input handling. [Open work](#source-checks-and-open-work).

A real project can keep this in its current context section or use a linked file.
Adapt the visual shape to the documented work; retain source links and status
distinctions. A nested checklist with explicit dependencies is another option.
