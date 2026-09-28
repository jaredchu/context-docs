# Live journal trial

Status: **Closed after three maintenance tasks in the same authoring chat.**
Authorized by the owner on September 28, 2026 after the initial synthetic
evaluation. This tracker applies only to this repository. No recurring task,
automatic capture or global logging requirement is installed.

**Historical recommendation at closure:** stop routine journaling here and retain
the command for explicit, task-specific use. The two handoff reviews recovered no missing fact from the
journal beyond docs/raw evidence. Grouped pointers were useful organization, but
independent retrieval benefit and net time savings remain unmeasured. The temporary
`AGENTS.md` trial rule has been removed; runtime code and saved evidence remain.
This is the assistant's recommendation, not an owner adoption or removal decision.

**Subsequent owner clarification:** prioritize efficient event recording for later
investigation; current-context improvement or savings are not logging's success
criteria. The [current logging goals](event-journal-pilot.md#efficient-logging-goals)
supersede using this trial's handoff criterion as a reason to stop capturing useful
history. Earlier findings and artifacts remain unchanged; they do not evaluate
the clarified purpose. The temporary trial itself remains closed.

## What counts

A session is a distinct real maintenance task with a useful handoff, not a new
JSONL filename or repeated test invocation. Do not invent work to reach three.
Session 1 is trial setup and handoff verification in the existing authoring chat;
it is not an independent or fresh-reader evaluation. Later sessions should follow
actual maintenance needs. Record whether the reader has prior chat context.
Audit-only work stays read-only and does not advance the trial.

Markdown/Git and original evidence remain authoritative sources for their claims.
Use the [pilot command and schema](event-journal-pilot.md) only for meaningful
checks, decisions, contradictions and context changes. Preserve observations,
proposals and approval sources distinctly. Keep project events in `.context/events`;
retain scoped evidence under `.context/trials/journal-2026-09-28`.

## Progress

| Session | Actual work | Evidence | Status |
| --- | --- | --- | --- |
| 1 — September 28 | Start the approved trial, preserve dirty-worktree snapshots, verify evaluated writer/test hashes, and check the updated handoff | [Evidence directory](../.context/trials/journal-2026-09-28/session-01), [events](../.context/events/journal-trial-20260928-01.jsonl) | Complete; setup session, retrieval benefit unmeasured |
| 2 — September 28 | Review the prior handoff, compare source routes, and correct stale integration wording in project context | [Baseline answers](../.context/trials/journal-2026-09-28/session-02/baseline.json), [comparison](../.context/trials/journal-2026-09-28/session-02/comparison.json) | Complete; same-chat review, no independent reader or speed result |
| 3 — September 28 | Review session 2's handoff, assess duplication and upkeep, and retire the temporary rule | [Baseline answers](../.context/trials/journal-2026-09-28/session-03/baseline.json), [comparison](../.context/trials/journal-2026-09-28/session-03/comparison.json) | Complete; same-chat review and closure |

Session 1 introduced no new writer behavior. The [earlier evaluation](../evals/results/2026-09-28-event-journal/README.md)
remains a synthetic result; beginning this live trial does not convert it into
real-work or fresh-agent evidence. Setup cost and reading benefit must remain
separate. Existing reports already contain the implementation/test findings, so
the first events primarily index evidence that also exists elsewhere.

Session 2 saved answers to all three handoff questions before its current-turn
journal read. The two events supplied no missing fact beyond docs and raw evidence;
they grouped the same checks, rationale and pending work. This reader retained
the original chat, so the result does not measure independent accuracy or speed.
The actual maintenance change clarified that the temporary repository rule is
agent guidance while the installable skills still do not invoke the journal.

Session 3 likewise answered the three questions from docs/raw evidence before
its current-turn journal read. The event repeated the same check, rationale and
pending decision. The closure removed the temporary logging instruction and
reconciled active documentation with the completed trial.

These were three actual maintenance tasks, all concerning the journal itself,
within one continuous chat. They were not three fresh-agent sessions or natural
multi-day handoffs. No unrelated feature work, incident response or independent
reader was tested. The result supports declining further routine integration for
now; it does not prove that JSONL cannot help a different workflow.

## Recorded trial procedure

The following procedure and source routes are retained for inspection. The trial
is closed; they do not instruct future sessions to continue automatic logging.

1. Read the normal context, relevant Git changes and raw evidence first, before
   reading the previous session's journal. Answer the three questions below with
   source references; record unknowns without looking at the journal to fill them.
2. Read the prior journal with `read --session`. Record what it added, duplicated
   or made misleading, including corrections and omitted events. Same-reader
   order effects are expected; do not claim a controlled accuracy or speed gain.
3. Perform the actual authorized maintenance task. Preserve the starting and final
   source revisions or scoped snapshots for uncommitted files. Append only events
   that carry durable information, with actual check output as evidence. Do not
   rerun unchanged checks merely to produce a log entry.
4. Update this tracker and leave a short handoff. Record event count, payload/record
   bytes, extra commands and any observed logging friction. Record elapsed effort
   only when measured; otherwise mark it unmeasured. Include missed events.

Questions for the previous session:

- What was checked, against which revision or snapshot, with what scope/result?
- Why did current context change, and which authority supported it?
- What unresolved issue needs the next reader's attention?

For the completed session 2 review, the baseline source route was `docs/project-context.md`,
`AGENTS.md`, the initial evaluation report, and session 1's source snapshots,
`before.json`, `after.json`, `final.json`, `evaluated-source-check.json` and
`static-checks.txt`. Exclude `payloads/`, `append-*.json` and the journal itself
from the baseline: those files contain the additional journal content. Trial
review notes are not baseline evidence either. The second route adds the JSONL
file while retaining the same raw evidence. No time comparison is valid if the
same author already remembers the answers.

For session 3, start with the current docs, the source snapshots and the actual
static-check output in session 2's evidence directory. Its `baseline.json` and
`comparison.json` are review artifacts; do not use them as hidden reference
answers when assessing independent retrieval. Exclude journal files, event
payloads and append outputs until after recording baseline answers. Then read
session 2's journal and record any added information or duplication. The decision
remains whether continuing optional logging justifies its cost.

```sh
python3 tools/event_journal.py read --session journal-trial-20260928-02
```

Use a distinct ID for session 3. A continuation of the same task
keeps its session ID and does not increment the count. A task adding no durable
information needs no event. Errors, corrections and negative findings stay in the
record; do not delete evidence to improve the outcome.

## Outcome and remaining limits

The decision rule was to keep routine logging only if it preserved useful supported
history or reduced retrieval effort enough to justify upkeep. Both same-chat
reviews found duplication of already retained evidence; neither measured a net
effort saving. Manual event fields, additional CLI calls and raw-evidence retention
were real costs, though authoring time was not separately measured. Snapshot and
comparison artifacts are evaluation overhead, not requirements of the JSONL format.

Routine logging has ended with the planned removal of the temporary rule. The
optional tool, journals, failed controls and original evidence remain available.
No indexing, automated capture, cleanup or installable-skill integration was added.
Reconsider only when a concrete history/retrieval need arises; repeating this small,
familiar handoff is unlikely to establish a broader benefit.

Session 3's [check output](../.context/trials/journal-2026-09-28/session-03/static-checks.txt)
and [source identity check](../.context/trials/journal-2026-09-28/session-03/source-identity.json)
are mechanical evidence. The retained 25-test result still applies to the identical
writer/test source; that suite was not rerun during this documentation-only closure.
