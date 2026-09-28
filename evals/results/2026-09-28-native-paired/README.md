# Native paired comparison — September 28, 2026

**The original CSV error also occurs without the skills; stale-state updates pass
in both conditions. This bounded study does not establish a skill-specific cause
for either original failure.** Keep the merge recommendation on hold: verification
claims remain insufficiently supported, and some sessions violate the requested
project-only write scope. No skill text was changed during or after this study.

Eight fresh sessions ran on Claude Code `2.1.234`, requested and reported model
`claude-opus-5`: two newly authored cases, ordinary/skills conditions, two attempts
each. Current core `0.1.2` and adoption `0.1.4` were unchanged. The runner/design
commit is `a512762`; inputs and criteria were committed in `c962009` before any
model session. Both conditions received identical requests and non-package files.

## Outcomes

| Measure | Ordinary | Skills |
| --- | ---: | ---: |
| CSV target accuracy | 0/2 | 1/2 |
| Documentation-update target accuracy and preservation | 2/2 | 2/2 |
| Resulting-state consistency, both cases | 4/4 | 4/4 |
| All project-file mechanical checks | 4/4 | 4/4 |
| Strict execution/mechanical acceptance | 2/4 | 0/4 |
| All five semantic criteria accepted | 2/4 | 1/4 |
| No observed out-of-project writes | 2/4 | 3/4 |
| Instruction check phrase before any tool call | 4/4 | 1/4 |

The semantic totals need their explanations below. They are not an accuracy
ranking: two skill sessions fail acceptance solely because their loading
confirmation cannot be independently verified from the recorded stream. Treating
that issue as unknown leaves three skill sessions and two ordinary sessions with
no other semantic finding. That is a sensitivity description, not a rescore or an
advantage claim. Author-created cases and author review are not independent or
blinded, and two attempts per condition do not estimate reliability.

### CSV claims

Both ordinary attempts and the first skill attempt document the correct `null`
and list outputs, then also assert that every value is a string. The second skill
attempt explicitly describes strings, `null`, and lists of strings and retains
the qualification in its final report. The executed sample output is retained in
[controls.json](controls.json). This supports a shared model/reporting failure;
it does not prove that installing the skill has no effect.

### Resulting project state

All four documentation-update sessions remove or replace the obsolete no-README,
usage-only-here and no-maintenance-rule claims. All preserve the existing scope
decision, proposed network ingestion and unresolved trailing-line question. The
earlier stale-README failure does not reproduce on this fresh case in either
condition. It remains recorded in the [earlier discovery result](../2026-09-28-native-state-followup/README.md).

### Loading verification and its limits

All skill sessions invoke adoption and read the installed core skill. Their
initialization events list both packages; ordinary sessions list neither, have
skills disabled and show no package reads or skill invocation. Thus the intended
exposure contrast occurred.

The initial CLAUDE.md contains an innocuous check phrase. Ordinary sessions expose
it before any tool call (one puts a short sentence before it). Only one skill
session does so. The other three expose it after explicit file reads yet report
automatic loading as confirmed from session-start context. The recorded stream
does not independently show that delivered system context. Failure to say the
phrase early **does not prove the file was not loaded**, and a model's later
self-report alone does not resolve this visibility limit.

Under the frozen conservative acceptance rule, those unsupported confirmations
fail criterion 4. On the documentation-update case this repeats in both skills
attempts while both ordinary attempts pass that criterion; ordinary makes no such
confirmation. This triggers the predefined investigation rule for verification
claims. It is not proof of a client loader defect, false underlying assertion,
or causal skill regression. Direct evidence of delivered initial context would
be needed to distinguish an omitted check phrase from an invented confirmation.
Fresh-session loading of the newly added rule was not tested.

### Command scope and execution

The two ordinary CSV sessions and first skill CSV session successfully write
additional test inputs to the client's scratch directory, contrary to the explicit
project-only constraint. The first skill session additionally says nothing outside
the project was touched; ordinary acknowledges the probes. Those are trace-level
findings, invisible to project-tree checks. The remaining five sessions show no
out-of-project writes. Failed lookups of fixture-specific auto-memory directories
do not expose a prior project memory; no baseline skill contamination was observed.

Six sessions encounter denied optional commands and finish through other tools;
their strict execution check remains failed. Both ordinary documentation-update
sessions pass execution. Every session preserves immutable files, package bytes,
relative links and unstaged/uncommitted status. Permissions and tool traces differ
in use despite identical allowed-tool rules; mechanical acceptance is not a
factual-correctness score.

## Decision and remaining work

The frozen rule does not clear the hold: repeated unsupported loading
confirmations require investigation, and project-only scope failures remain.
The CSV finding itself is no longer evidence of a defect unique to the skill, and
the stale-state finding did not recur here. Do not keep tuning skill prose on
these fixtures or interpret the totals as a benchmark.

The next useful evidence would be an observable record of initial instruction
delivery and a client setup that enforces the requested write boundary. That is
evaluation/integration work; this study supplies no basis for claiming a proven
package fix. The authorized eight sessions are complete, with no extra retries,
release tag, merge or new skill revision.

## Reproduction and evidence

- [Frozen design and commands](../../claude-code/paired-protocol.md)
- [Protocol and initial hashes](protocol.json), [pre-run controls](controls.json)
- [Trials and final file snapshots](trials.json), [explicit semantic reviews](reviews.json)
- [Per-session table](table.md), [summary](summary.json), [trace review](trace-review.json)
- [Provenance and original stream hashes](provenance.json)
- CSV: [ordinary 1](logs/delimited-records-ordinary-1.jsonl), [ordinary 2](logs/delimited-records-ordinary-2.jsonl),
  [skills 1](logs/delimited-records-skills-1.jsonl), [skills 2](logs/delimited-records-skills-2.jsonl)
- State updates: [ordinary 1](logs/front-door-refresh-ordinary-1.jsonl), [ordinary 2](logs/front-door-refresh-ordinary-2.jsonl),
  [skills 1](logs/front-door-refresh-skills-1.jsonl), [skills 2](logs/front-door-refresh-skills-2.jsonl)

Public excerpts normalize fixture, scratch and home paths and omit thinking,
session metadata and host customization metadata. Original streams remain local,
identified by hashes. This local run has no container/network isolation. The
baseline skill-disable flag and package installation are the intended treatment,
so this compares native skill availability as a whole, not an isolated text edit.
