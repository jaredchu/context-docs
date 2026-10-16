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

| Work | Status | Evidence and next step |
| --- | --- | --- |
| Preserve CSV columns | Done for this check | [Columns check passed](#source-checks-and-open-work). Deployment is unverified. |
| Handle empty input | Blocked; goal remains incomplete | [Representative input missing](#source-checks-and-open-work). Prepare it, then run the check. |
| Add five retries | Proposed | [Owner approval is absent](#source-goal-and-decisions); no implementation claimed. |

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
The headings and table are optional; the evidence and status distinctions matter.
