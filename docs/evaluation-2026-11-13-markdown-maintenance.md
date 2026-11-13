# Context Docs and ordinary Markdown: a small continuation experiment

**November 13, 2026 · Exploratory agent-only comparison.**

This agent-only experiment compared Context Docs with competent ordinary
Markdown maintenance on three synthetic projects. All twelve subject sessions
completed, and all six continuation answers received two-pass grades.

The observed recovery scores favored ordinary Markdown in two cases and tied
in the third. All six proposed continuations scored 2/2. One Context Docs
receiver lacked required captured read evidence, leaving two eligible pairs
and **no clean three-pair average**. These results demonstrate neither a Context
Docs advantage nor general equivalence or disadvantage.

Context Docs provides a [documented standard](../skills/context-docs/references/standard.md)
and an adoption workflow for people who do not already have context-documentation
conventions. Comparisons with competent maintenance are quality diagnostics;
outperforming that comparator is not a requirement for providing a useful
standard. This experiment did not measure how easily newcomers adopt that
standard, how much organization it avoids, or human effort savings.

## What was compared

Each case began with the same project files in both conditions, including a
README and existing behavior notes, history and planned checks. Ordinary
Markdown received active maintenance, rather than an unattended or deliberately
weak baseline. Both conditions could choose their document layout and links.

| Case | Planning task | Later rule change, with code deliberately unchanged |
| --- | --- | --- |
| A: Ledgerlight | Export acceptance checklist | Preview limit changes from 100 to 50 rows |
| B: Fieldtally | Offline import test plan | Skipping blank identifiers changes to rejecting the whole file and reporting the first offending input line |
| C: Shelfsweep | Cache-cleanup dry-run checklist | Candidate age threshold changes from 30 to seven days |

For each condition and case, a writer performed setup, work/save and update/save
in one session. Four facts were supplied in the work conversation only: a choice,
its rationale, an approval boundary or blocker, and an owner-reported untested
behavior. The update stage supplied a dated rule note; the code continued to
implement the earlier rule. A separate fresh receiver then read the saved
project and proposed the next local action and check, without writer history.

This tests the whole workflow with explicitly prompted maintenance and directed
reading. It does not isolate the documents from receiver guidance or test
spontaneous maintenance. Applications and proposed checks were not executed.

The client was Codex CLI app-server **0.167.0-alpha.4.1**, with
**`gpt-6-astra`**, requested **High**, for subjects and grader. Context Docs used
published bundle **v0.2.7**: core **0.2.7**, adoption **0.1.16**, source
`00c4b5175c04fdf173d6802f20a76e688c63fbe0`. Logging was off.
These are the selected and observed startup controls; runtime reasoning effort
was not independently attested.

The ordinary condition had the target skills disabled and their package reads
denied. The treatment condition had the released skills enabled and readable,
with native adoption input at setup. Both used the same non-treatment controls,
case evidence, work/update/resume messages and caps. Writers could edit only
Markdown; receivers were read-only. Network, native memories, apps/plugins,
MCP, hooks and delegation were disabled by the study configuration. Captured
startup and sandbox checks support these bounded controls; they are not proof
against every possible bypass or hidden influence. Inspected generic global
preferences remained present, without case, oracle or Context Docs guidance.

All three treatment projects' saved instruction files leave the adoption marker
pending because automatic loading of the newly created project instruction file
was not confirmed. Completed experiment stages and enabled native skills do not
resolve that saved adoption qualification. This is separate from B's missing
captured read output, described below.

Setup/work/update/resume caps were **5/8/5/5 minutes**. Writer order was ordinary
then Context Docs for A and C, and the reverse for B; receiver order reversed
each pair. Every completed session paused for a coordinator scope audit, without
extra subject guidance. All 24 stages completed uncapped, all twelve scope
audits were accepted, and there were no clarification replies or unscripted
assistance events. Utility failures are retained separately from model-stage
completion; a completed stage does not imply every utility check succeeded.

## How scores work

- **Recovery /4:** a chat-only fact must be stated or used accurately in the
  receiver's answer, with saved Markdown support and required owner-choice,
  approval and report qualifications. A citation alone cannot recover an
  unmentioned fact.
- **Chat-only preservation /4:** those four facts are accurately preserved in
  saved Markdown, whether or not the receiver mentions them.
- **All preservation and answer coverage /8:** the same four facts plus behavior,
  next check, replacement rule and constraint, scored separately for notes and
  supported answers.
- **Continuation /2:** 2 means a concrete proposed action/check fits the current
  rule, constraints and authorization; 1 means an appropriate but insufficiently
  concrete proposal; 0 means absent, unsupported, obsolete or unauthorized.

Correctly identifying that code still implements the old rule is allowed.
Proposing a later authorized fix followed by the governing-rule check is allowed;
the study gives no credit for implementation or checks actually being performed.
Critical omissions, false/outdated assertions and other unsupported inventions
are reported separately, without double penalties.

One fresh grader first assessed all six answers with method labels and citation
paths masked, against the frozen rubric and oracle. It recorded condition guesses.
Every first-pass judgment and guess was frozen before source delivery. In the
same grader session, pass two received original answers, saved documents, read
flags and provenance, then checked support. Allocation truth was withheld until
outputs froze. Both passes finished with no tool attempts, in **568.68 seconds**
under their shared **900-second** cap. The coordinator inspected source meaning
and accepted the grades without a correction or model regrade.

This is fresh-session, same-model grading within a maintainer-run study, not an
external independent benchmark or model diversity. Masking did not establish
blinding: one first-pass guess identified Context Docs with high confidence,
one identified ordinary Markdown with low confidence, and four were unknown.
After seeing source documents, all six guesses matched allocation with high
confidence. Wording and structure remained recognizable.

## Results

These are all six final as-run grades, including the excluded cell.

| Case | Condition | Recovery /4 | Chat-only preservation /4 | All preservation /8 | Answer coverage /8 | Continuation /2 | Eligible for clean comparison |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| A | Ordinary Markdown | 3 | 4 | 8 | 7 | 2 | Yes |
| A | Context Docs | 2 | 4 | 8 | 6 | 2 | Yes |
| B | Ordinary Markdown | 2 | 4 | 8 | 5 | 2 | Yes |
| B | Context Docs | 2 | 3 | 7 | 5 | 2 | No: required read output missing |
| C | Ordinary Markdown | 2 | 4 | 8 | 6 | 2 | Yes |
| C | Context Docs | 1 | 4 | 8 | 5 | 2 | Yes |

Raw Context Docs minus ordinary recovery differences are **−1, 0, −1** for A/B/C.
The corresponding chat-only preservation differences are **0, −1, 0**;
continuation differences are **0, 0, 0**. These are descriptive per-case
differences, not an effect estimate. Five cells and two pairs qualify for the
clean comparison. The planned three-pair mean and range are **unavailable**;
they were not replaced with zero or calculated from only the two eligible pairs.

The exclusions and losses have different meanings:

- **Missing read evidence:** the B Context Docs receiver read the README and
  substantive linked notes, but did not emit the full linked `AGENTS.md` through
  a read tool. The frozen rule required captured full-file output for every
  detected note-entry candidate. Automatic instruction loading and citations
  were not substituted for that proof. Its completed answer was graded and its
  scope audit accepted, but its cell and pair remain excluded. No coached reread
  or eligibility override was performed.
- **A saved qualification loss:** B's Context Docs notes retained that duplicate
  handling was untested, but dropped that the owner reported it. That loses
  one preservation point under the frozen rubric. It is not a false claim that
  duplicate handling was tested. The read-evidence exclusion is separate.
- **Answer omissions:** all six answers omitted owner-report attribution for
  the untested behavior, so none recovered that qualified fact. Five snapshots
  retained it. Context Docs A omitted the spreadsheet-inspection rationale;
  both B answers omitted the disconnected-use rationale and local TSV input
  description. Both C answers omitted the inspect-first rationale, and Context
  Docs C stated the mode without expressing the owner's choice. Except for B's
  saved report qualification, these losses do not indicate missing notes.
- **Continuation:** all answers recognized the old-code/new-rule mismatch and
  proposed a fitting governing-rule check with prerequisites and authorization
  limits. The tied 2/2 score is a ceiling of this rubric, not evidence of equal
  general usefulness.

The grader recorded no critical omissions, critical false/outdated assertions
or unsupported inventions in the scored notes and answers. This is a bounded
rubric judgment, not a guarantee that every artifact detail is correct.

## Earlier attempts and interpretation limits

The completed run followed controller repairs; it was not the only attempt.
An earlier partial run produced two graded A answers and four missing answers:
ordinary recovery **2/4**, Context Docs **3/4**, both chat-only preservation
**4/4** and continuation **2/2**. Three subsequent scored launches stopped before
any receiver or grader when the controller rejected harmless executable discovery
or a local Markdown-check utility. Two unscored preparation candidates also
stopped before scored subjects, for configuration drift and a censoring defect
found in prelaunch review. Original attempts remain preserved separately.

The controller's screening, masking punctuation and failed-stage censoring were
corrected before the final run, with neutral rehearsals and source review. A
narrow environment-guard amendment permitted unrelated project trust entries
while keeping study-relevant settings guarded. Final subjects started from the
original reviewed fixtures, without earlier writer files or answers. Earlier
scores were neither pooled into this table nor used to fill missing cells.
The observed earlier A recovery difference points in the opposite direction;
this history further limits a broad interpretation of single-case scores.

There was only one generation per condition/case in the final run, three
author-created cases and one selected model. The partial order counterbalance
cannot separate workflow effects from model variation. Subjects knew their
workflow, the grader could recognize it, and human effort was not prospectively
measured. No p-value, causal claim, superiority/equivalence conclusion, speed
advantage or novice effort-saving estimate follows.

The practical finding is narrow: both workflows supported concrete proposed
continuations, while qualified facts could be omitted from answers and one
owner-report attribution was lost from saved notes. This comparison does not
answer the separate question of how much a ready-to-apply standard helps people
establish conventions. It supplies no evidence requiring a product change or
another experiment now.

## Inspect the evidence

The [public evidence extract](../evals/results/2026-11-13-markdown-maintenance/README.md)
contains all six receiver answers, final synthetic snapshots, both sets of
per-fact judgments, the rubric/oracle, exact stage text, caps, read summaries and
all grades/eligibility flags. Workspace paths and incidental operator storage
references were normalized or explicitly omitted. Score-bearing content and
original study bytes were preserved; the extract describes every transformation.

The extract is a maintainer-prepared derivative, not the complete original
capture or an independently authenticated replay package. Private controller
logs, account/configuration details and operator records are not public evidence.
Readers can inspect the included artifacts and scoring reasoning; exact client
re-execution requires additional environment and harness preparation.

Return to the [evidence overview](evaluation-results.md).
