# Unfamiliar-user trial

Status: **anonymous feedback received; the owner confirms human-observed
usability and actual cross-machine use.** The owner accepted this follow-up on
October 26, 2026. The [early feedback](#anonymous-early-feedback) is recorded
separately from this prepared Reading Queue trial, which is an exploratory
usability trial, not a controlled effectiveness study.

## Anonymous early feedback

On November 7, 2026, the owner supplied five responses: four individual responses
and one team response. This aggregate paraphrase omits names, direct quotations
and private project details.

- All five responses describe useful continuity across sessions or teammates
  and express an intention to keep using Context Docs.
- Two describe continuing work on another machine. Other examples describe
  retaining an earlier decision, recovering unfinished work and sharing project
  conventions and rationale with a teammate's fresh session.
- Reported friction includes remembering to commit context alongside code,
  prompting a progress refresh, correcting a stale note and asking to shorten
  an overly long decisions log. Setup was generally described as straightforward.

These owner-supplied self-reports support perceived usefulness for these
respondents. Session traces, context diffs, exact package/client versions and
measured assistance or effort were not supplied. Prior familiarity and use of
the frozen r1 materials are unknown; these responses are not scored trial
outcomes. They establish neither a comparative effort saving nor general
reliability. Cross-machine reports describe continuity with available context
files, not synchronization of model memory; one mentions Git commits, while
the other does not specify the transfer method. The structured procedure and
frozen materials below remain available for observed follow-up.

A separate [synthetic Git-transfer handoff check](../handoff/2026-11-07-git-transfer/README.md)
passes eight content criteria in two fresh Claude sessions on the same host. It
adds inspected agent evidence, not observed participant outcomes or a test on
different physical machines.

## Owner confirmation

In a follow-up on November 7, 2026, the owner explicitly confirmed human-observed
usability and actual cross-machine use, addressing the earlier pending status.
Record these as owner-confirmed outcomes for the reported use. The synthetic
agent check remains a separate same-host result.

The confirmation did not supply additional session records or identify use of
the frozen r1 procedure. It does not establish completion of that specific trial,
independent verification or measured comparative effort savings. Names and private
project details remain omitted.

## Question and scope

Can people who do not already use Context Docs complete its local workflow with
manageable assistance, retain accurate project knowledge and continue in a fresh
session? Observe installation, reuse of adopted context, maintenance and resumption.
The starter already has a maintenance rule: this trial does **not** test adoption
of an unconfigured project. Keep application/dependency trouble separate from
Context Docs trouble, while retaining both in the whole-user-experience report.

Start with three unfamiliar participants, allowing up to five if available. These
counts and a 45-minute observation window are coordinator choices. Record prior
coding-agent familiarity and context habits; do not exclude someone after a
failure. Stop at the time limit or whenever a participant wishes. Incomplete and
assisted attempts remain outcomes. If only one participates, report one case.

The participant uses their existing client/subscription. No extra purchase,
new cloud account, deployment or global-settings change is required. Offer help
when requested; record the question and help rather than treating assisted work
as unaided. Preserve existing installations and customizations.

## Materials and freeze

Share [participant-guide.md](participant-guide.md); keep the coordinator's
[observation form](observation-template.md) separate. Use synthetic/public example
data only. Retain consented originals privately; participant names, contact details,
session logs and private project context do not belong in this public repository.
Use an existing approved private destination, or an ignored directory such as
.local/user-feedback/ under a unique trial ID. Verify it is untracked and ignored
before writing records; keep the blank public forms unchanged.

Before the first session, retain a dated manifest beside the private observations:

- This packet's revision and file hashes; save the exact rendered walkthrough
  supplied to participants, not just its mutable URL.
- Released bundle **v0.2.6**, source commit
  `d74e69d3268676cf7eab19d241e8b590ddb1c60a`: core **0.2.6**, adoption **0.1.15**.
  Record all installed package file hashes and any existing customizations. Use a
  separate supported project installation if a different existing package must
  be preserved; record the installation route and assistance. Do not substitute
  the unreleased simplification candidate during this trial.
- Reading Queue starter commit
  `238d1d3c0921d304edc8770ced18355972cb7d64` (`tutorial-start`), repository URL,
  and exact supplied task text. Verify the checkout before starting.
- Client/version, selected model and reasoning setting (or unknown), available
  tools, relevant native memory/customization state, existing skill installation,
  Node/npm versions and starting working-tree state. Record participant-specific
  differences rather than assuming environments are equivalent.

Do not tune packages, task wording or coaching silently between participants.
If the pilot reveals a blocking error, retain that attempt, version the repaired
materials and report later sessions separately. New skill versions need their
own selected trial; results here describe the frozen released packages only.

### Prepared material set r1

Local material ID **reading-queue-2026-10-26-r1** contains the unchanged participant
guide, released skill folders, a website rebuild from recorded published source
`e8ace0c6984f9a10ebb052a53515ef05ff722658`, and a Git bundle of the pinned starter.
The supplied start instructions replace only remote clone/branch commands with
a local bundle clone and direct installation to the included released folders.
This supplies source/package acquisition: setup findings apply to that prepared
route, not finding/downloading the project from GitHub. Record another route as
a material deviation. Task prompts remain unchanged.

The per-file manifest, ZIP hash, coordinator snapshots and preflight receipts are
retained locally under that material ID; the ZIP is prepared for owner sharing,
not published here. The starter round-trip and static local-link/package checks
pass. No new app tests, browser interactions, model sessions or human results are
established by this preparation. External links remain external and were not
refetched. Keep completed observation files outside the participant archive.

## Session and measures

Use the local walkthrough through verification; omit deployment and defer the
completed-example comparison until after the continuation check. Observe these
phases without supplying the expected implementation answers:

| Phase | Record | Basis for an outcome |
| --- | --- | --- |
| Setup | Existing installation, instruction uncertainty, help needed, first unclear step | Actual package/setup evidence; distinguish reusable setup from a clean install |
| Work and save | Prompts changed or added, maintenance reminders, manual Markdown corrections, lost/unsupported claims | Prompt history, source evidence and before/after diffs |
| Fresh implementation | Whether a new chat continues from the saved requirement; context maintenance without a new skill reminder | New session identity where available, trace and resulting code/Markdown |
| Fresh continuation | Correct goal, remaining work, blocker, next action and verification limits | Another new chat, saved context and relevant sources; no pasted earlier conversation |

Record the number and purpose of supplied walkthrough prompts separately from
participant-authored prompts. Count human assistance events (each distinct
question/help exchange), extra maintenance prompts and human corrections
separately from agent self-corrections.
For a correction, record what was wrong, its source and whether it was actually
fixed. A reminder to use Context Docs counts even if it produces a good result.
Separate directly observed facts, participant reports and evaluator judgments.

Review the export against its source requirement: whole active queue under a
filter, browser isolation/expiry, empty result and failed-fetch behavior. Review
context for retained decisions/rationale, actual versus pending tests, deployment
boundary and actionable next work. Application test passes alone do not establish
a useful handoff. Missing client trace makes loading unknown, not a pass or fail.

Record active time per phase when practical and waiting time separately. Ask
which steps were confusing, whether the saved document helped, and what the
participant would use next time. Subjective usefulness is feedback, not causal
evidence. Do not reduce this trial to one score or time saving.

## Review and next decision

Report every attempt as completed unaided, completed with help, incomplete or
withdrawn; also report factual/context findings and assistance separately. Explain
withdrawals using only permissioned detail. Record the participant/client mix,
missing evidence and changes between material versions. No outcome implies zero
missed defects. Maintainer analysis of unfamiliar participants is not independent
grading or independent case selection.

Select the most consequential repeated or well-supported difficulty for a
synthetic reproduction and focused fix. If evidence is mixed, keep the uncertainty
and avoid a broad rewrite. A few successful sessions would support feasibility
for those users and conditions; they would not establish superiority, general
reliability or reduced effort against another workflow. Comparative claims need
a separately frozen matched baseline; the
[discrimination protocol](../discrimination-protocol.md) addresses that different
question. This packet does not launch that campaign or authorize outreach or
publication of participant information.
