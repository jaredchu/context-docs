# Discrimination protocol

Status: **proposed on September 28, 2026; not accepted by the project owner and not
executed.** It adds no result and changes no published study. It extends the
[quality-first protocol](quality-protocol.md), which remains the standard for
claims about reader benefit; every measure, control and honesty requirement there
still applies. This document only removes conditions that currently make a tie the
expected outcome whatever the skill does.

## Why the completed studies tie

Five completed studies report no skill-specific advantage over competent ordinary
maintenance. Three properties of the current designs would produce that result
even from a skill that worked well, so the tie is weak evidence either way.

1. **The baseline receives much of the treatment.** The shared task text in
   [suite/build.py](suite/build.py) tells both arms to "preserve existing project
   layout and unique information" and that "no live environment access is
   supplied". Per-case requests in [suite/cases.py](suite/cases.py) add "preserve
   decisions and useful design rationale", "avoid bookkeeping-only edits" and
   "avoid speculative architecture and empty templates". Those instructions are
   the skill's contribution restated as the task. These suites are honestly
   described as maintenance regressions, and they work as such; they cannot
   measure incremental benefit.
2. **Fixture evidence labels its own status.** The inputs in
   [quality/fixtures.py](quality/fixtures.py) contain sentences such as "not an
   owner decision", "a new proposal date is not approval" and "says nothing about
   production rollout". The skill's central discipline is separating approved,
   proposed, observed and unknown claims. When the evidence has already made that
   separation, no arm has to.
3. **Readers cannot be short of the answer.** Every arm keeps the raw evidence,
   the inputs total 514-656 words, and readers answer six questions with no
   practical budget limit. Reading everything is cheaper than consulting a summary,
   so all arms reach the ceiling, including unmaintained ones.

Fixing these is not a matter of more trials. The 48-trial, 12-trial, 72-session,
16-session and 28-session studies would all tie again at greater cost.

## Changes to make before the next comparison

Keep the matched arms, the common raw evidence, the frozen criteria, the retained
failures and the explicit review method unchanged. Change only these conditions,
and freeze the result before execution as usual.

**A. Give the baseline a neutral request.** The ordinary arm should receive the
work, not the method: for example "update the project documentation from this
evidence". Keep scope and safety text identical across arms, since it protects the
harness rather than teaching maintenance. Do not weaken the baseline in any other
way: it keeps the same model, effort, evidence, time and tool access. Record both
prompts verbatim in the manifest so the remaining difference is auditable.

**B. Write evidence that does not classify itself.** Sources should state what
happened and let status follow from authority, dates and wording, as real records
do: a contributor's design note that reads as a plan, an owner's message that
carries approval without the word "approved", an implementation that landed
without a decision, a dashboard screenshot that shows configuration rather than
production. Derive the ledger's expected statuses from those sources during
authoring, and keep the ledger outside every session as the existing protocol
requires. An unlabeled source with genuinely ambiguous authority is a valid case:
score a recorded, accurate uncertainty as correct.

**C. Make retrieval cost real.** Choose at least one of these, declare which, and
apply it identically to every arm:

- A reader budget: a fixed tool-call or token allowance, or a session timeout,
  reported with every timeout retained as a failure.
- Evidence volume: enough raw material that reading it all is impractical, with
  distractors and superseded versions that resemble the current record.
- Cross-referencing: questions whose answers require combining three or more
  sources, so a single well-chosen document beats a single well-chosen file.

Report time and tool calls to a correct supported answer alongside accuracy. A
method that reaches the same accuracy with less reader work is a real result under
this protocol, provided the budget and failures are reported.

**D. Separate availability from consumption.** The public pilot found that none of
its eight handoff readers opened the handoff, and the routing follow-up reached
full exposure only after the harness added orientation links. Treat discovery as
its own factor: hold the documents fixed and vary whether the entry point is
linked from the project's README and whether the maintenance rule sits in the
instruction file that the client actually loads. Measure exposure from
model-visible tool output, as the routing study does, and keep it separate from
accuracy. This is the one place where existing evidence already suggests an effect.

## What a result would mean

With A-C in place, a tie becomes informative: it would indicate that the skill's
guidance adds little to a competent agent given the same evidence, which is a
publishable finding and a reason to simplify the package. A difference would need
the same caveats the completed studies carry, and this protocol does not lower
them: author-created cases, author review without blinding, one client and one
model remain limits until independently contributed cases and condition-blind
review exist. Do not describe any outcome here as an independent benchmark.

Run this on a small scale first: two projects, one maintenance sequence per arm,
and the reader budget calibrated in a pilot whose results are reported whatever
they show. Do not modify a frozen fixture or published artifact to fit this
protocol; add new cases beside them and leave the existing record intact.
