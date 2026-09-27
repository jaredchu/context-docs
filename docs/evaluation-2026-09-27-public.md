# Public-source handoff evaluation — September 27, 2026

The larger-source pilot completed **16 model sessions and 72 reader answers**.
Upstream-only and Context Docs readers passed 24/24 answers each; ordinary-handoff
readers passed 23/24. Both maintenance methods covered all 24 required handoff
criteria and preserved every supplied upstream file.

**This does not establish a Context Docs accuracy advantage.** Recorded traces
show no handoff-content reading in any of the eight maintained-artifact readers;
they answered from upstream docs, code and tests. This measures availability and
natural discovery under this harness, not the effect of actually consuming the
new handoffs. The one-answer difference is a single incomplete answer, not a
replicated artifact effect.

| Reader outcome | Upstream docs/code | Ordinary handoff | Context Docs v0.1.1 |
| --- | ---: | ---: | ---: |
| Flask | 12/12 | 11/12 | 12/12 |
| Click | 12/12 | 12/12 | 12/12 |
| **Total** | 24/24 | 23/24 | 24/24 |
| Correct in both phrasings | 12/12 | 11/12 | 12/12 |

## The single incomplete answer

One ordinary-artifact Flask reader explained application-context scope, lazy
`g.db` initialization and teardown, but did not say how cleanup handles a
connection that was never created. The frozen second criterion required that
guard, so it fails that criterion. The other five questions in that session pass.
This was an omitted answer detail, not execution of unsafe cleanup code or a
false deployment claim. Its cited guide contains the guarded cleanup example, but
a citation alone does not supply the required reader answer detail.

The ordinary handoff itself **does contain** `g.pop('db', None)` and conditional
close. Its reader did not open that handoff. The other phrasing in the same
condition includes the guard and passes. See the actual answer and explicit
review in [the evidence](../evals/results/2026-09-27-public/README.md).

## Discovery limits the interpretation

A post-execution inspection of recorded commands and outputs found:

- **0/8** maintained-artifact readers explicitly opened a handoff, showed its
  heading/content or filename-prefixed search matches, or cited it.
- Two readers saw a handoff filename in a file listing; that is not evidence of
  consuming its content. Other searches went straight to upstream source paths.
- Both upstream-only Flask readers independently resolved the request-limit typo,
  and both upstream-only Click readers recovered the version-specific flag rule.

This is a **post-hoc diagnostic**, not an additional frozen success metric or a
system-call audit. [Recorded source commands and detection details](../evals/results/2026-09-27-public/reader-discovery.json)
make the observation inspectable. The protocol prohibited editing upstream files,
including the README, and disabled automatic project-instruction injection.
Readers were allowed to search freely but were not told to open a handoff. Those
choices limit discovery; they do not establish a defect in the skill's usual
initialization workflow.

Larger repository size alone has not produced a useful test of handoff consumption.
The next evaluation should separately test discoverability through a permitted
project entry point and answer quality after confirmed handoff reading, with the
same reader instructions across arms. Longer update histories and independently
authored questions/reviews are still needed. **The skill remains v0.1.1; no prompt
change is justified by this result.**

## What was tested

The [protocol and cases](../evals/public/README.md) were frozen at `a2442c6`
before scored model execution. Source snapshots are historical pinned releases,
not claims about current Flask or Click behavior.

| Source | Release | Supplied text files | All source/test/doc words | Markdown/RST words |
| --- | --- | ---: | ---: | ---: |
| Flask | 3.1.1 | 226 | 143,604 | 70,036 |
| Click | 8.2.1 | 138 | 102,647 | 29,207 |

Counts use whitespace-delimited words, including code and tests in the all-files
column. All tracked UTF-8 files were supplied unchanged. Eight Flask images and
five Click images were omitted, consistently across arms; these are reading
corpora, not complete runnable checkouts. Exact revisions, per-file hashes and
omissions are in the [manifest](../evals/results/2026-09-27-public/maintenance-manifest.json).

These projects already have extensive documentation. This is an upstream-as-is
comparison that complements the earlier scattered/conflicting/absent-context
study; it does not label their documentation poor or replace that weak baseline.
Upstream source authorship is external. Question selection, prompts and semantic
review remain by the Context Docs authoring agent, not independent evaluators.
Both sources are familiar Pallets projects in the Python ecosystem.

Four maintainers (two projects × ordinary/skill) each added one root Markdown
handoff. Both arms received the same six focus areas and a competent request to
check code, tests and documentation. The skill arm additionally received explicit
Context Docs v0.1.1 invocation and its package. Exact questions and answer keys
were withheld. All original files were immutable, so maintainers could not link
the handoff from the existing README. No generated output was repaired before
readers received it.

Twelve fresh readers (two projects × three artifact conditions × two question
phrasings) each answered six questions. They could inspect the same complete
upstream text sources in every arm. The prompts supplied no condition labels,
previous conversation, skill or answer key. A passing answer needs both frozen
semantic criteria, supporting citations and no material false claim, as well as
scope/schema checks. Equivalent valid solutions count. Paired phrasings share
an artifact and are not independent project samples.

Harbor 0.23.0, Codex CLI 0.158.0-alpha.2, gpt-6-astra with low effort, concurrency
three, 480-second session limit, no retries. Skills/global instructions were not
injected into reader sessions. Agents inspected source without installing
dependencies, executing upstream tests or browsing externally. Author reference
validation separately executed the pinned Click flag example before freezing:
explicit `LEVEL=8` and `LEVEL=0` both produce integer `10` for the tested flag.

## What the handoffs contained

| Added-handoff measure | Ordinary | Context Docs v0.1.1 |
| --- | ---: | ---: |
| Required criteria covered | 24/24 | 24/24 |
| Missing / incorrect / conflicting criteria | 0 / 0 / 0 | 0 / 0 / 0 |
| Material additional document errors identified | 0 | 0 |
| Upstream files preserved | 2/2 artifacts | 2/2 artifacts |

Coverage is 12 criteria per project, assessed in each added document. Specific
canonical pointers are allowed; a generic docs link is insufficient. One ordinary
Click lazy-file item receives this pointer credit, explicitly documented in the
review. Upstream-only has **no added-handoff score**, not zero stored knowledge:
its existing documentation remains present.

Both Flask handoffs correct the config guide's `max_form_memory_parts` typo to
`max_form_memory_size`, describe the 3.1.1 key-rotation behavior, and distinguish
proxy examples from unknown deployment topology. Both Click handoffs distinguish
explicit environment-flag substitution from automatic-prefix lookup, child/group
resource ownership, and lazy opening from atomic replacement. They also state
source-derived limitations rather than claiming that upstream tests were run.

The handoffs cite their temporary checkout's commit. The runner creates a fresh
one-commit repository, so those IDs are not upstream commits. The
[provenance mapping](../evals/results/2026-09-27-public/provenance.json) preserves
both identities. This is a harness provenance limitation; generated documents
were not rewritten to add upstream pins before reader execution.

## Verification and limits

Four reference controls passed and four no-op controls failed as expected before
scored runs. Eighteen local scope/schema controls covered source edits, extra
non-Markdown files, invalid links, absent answers, missing citations and reader
edits. Reference success validates mechanics, not semantic-judge independence.
The frozen report aggregator was also checked with criterion, citation-support,
material-error and execution-failure controls.

All 16 model sessions passed mechanical checks and recorded-input isolation
audits, with no unexpected user/global AGENTS messages, execution exceptions or
retries. All 12 readers preserved the supplied project bytes and Git state.

All explicit reviews, handoffs, reader answers, task/source hashes, controls,
isolation counts and secondary timing/token observations are available in the
[evidence directory](../evals/results/2026-09-27-public/README.md). Source trees
are fetched at pins rather than vendored. BSD notices are retained; no upstream
endorsement is implied. Raw sessions stay local because they can contain service
metadata. Published evidence is inspectable, not a tamper-proof runner audit.

Review was unblinded and by the authoring agent. Three Click answers use broad
“write files” wording for lazy defaults, where automatic lazy opening
applies only to modes containing `w`; reviews record this as a non-material imprecision
for the explicit lazy/atomic rewrite question. The score reflects the frozen
material criteria, not a claim that every sentence is perfectly precise.
Independent reviewers can replace the published judgments and regenerate counts.

There is one maintenance attempt per arm/project, one initialization pass, two
reader phrasings, one model/client, and no evidence-update or no-change stage in
this pilot. It cannot establish general accuracy, equivalence, longitudinal
retention, cost superiority or normal global-instruction behavior. The earlier
private-project workflow miss and all previous study results remain visible.
