# Public decision histories across sessions — September 27, 2026

**Both maintenance methods preserved all assessed knowledge through four passes;
reader accuracy tied across all three conditions.** This completed study ran
28 model sessions and produced 96 correct, supported reader answers. All 12 readers
received the full Markdown in their assigned workspace before answer-writing.
No Context Docs accuracy advantage or general equivalence is established.

| Outcome | Unmaintained | Ordinary maintenance | Context Docs v0.1.1 |
| --- | ---: | ---: | ---: |
| Required knowledge in final context | 0/16 | 16/16 | 16/16 |
| Required knowledge across all stages | 0/63 | 63/63 | 63/63 |
| Correct, supported reader answers | 32/32 | 32/32 | 32/32 |
| Correct in both reader sessions | 16/16 | 16/16 | 16/16 |
| Readers exposed to all Markdown | 4/4 | 4/4 | 4/4 |
| Critical document findings across stages | 0 | 0 | 0 |

Raw-only readers could recover every answer from the same complete policy history.
Those original PEPs are already structured documents, even though the workspaces
have no maintained context initially. Zero unmaintained context coverage therefore
does not imply unavailable evidence, and the reader tie remains a ceiling.

**One skill session temporarily wrote a backup outside the permitted directories,
then corrected it.** It passed the project-file grader, whose limited scope missed
that action. Content quality and full task compliance must not be conflated;
see the trace finding below. No output was corrected by the harness, and no scored
run was retried or discarded.

## What the maintenance results establish

Both methods captured all **63/63 stage-specific knowledge items**, including
**16/16 in final context**, compared with **0/16 in the unmaintained README**.
The latter still had every original policy snapshot; zero is a maintained-context
score, not a claim that the source knowledge was unavailable. Neither method
lost a previously correct item or left an unqualified operative contradiction in
the assessed record. All four final no-new-evidence passes left Markdown unchanged.

Examples preserved by both methods:

- A five-year removal **preference** does not erase the two-year minimum or make
  five years mandatory. Earlier terminology remains explicitly historical.
- Soft deprecation provides neither scheduled removal nor a shortcut through
  later hard-deprecation rules.
- Draft, Accepted and Active policy states remain distinct from downstream
  implementation and from approval of separate version-number changes.
- The latest release policy's explicit version-specific support rule is retained
  while its inconsistent generic LTS wording stays visible and qualified.
- Superseded phase/support choices and their rationale remain recoverable; old
  rules are not left as concurrent instructions.

The ordinary release-policy run used two linked documents; the skill used one
context document. Neither layout receives extra credit. Final Markdown totals
(including README) were 1,717 ordinary versus 1,778 skill words for compatibility,
and 2,441 versus 2,093 for releases. Every maintained final artifact is longer than its
first-pass summary; preserving useful history takes space. Word counts alone do not
show whether a document is better, and this study sets no universal size target.

## Scope finding the mechanical score missed

All 16 maintenance sessions passed the frozen **project-file** preservation,
link and Git checks. That is not proof of full filesystem confinement.
In release-policy skill pass 2, a command successfully copied `context.md` to
`/output-context-backup.md`, outside the allowed `/workspace` and `/output`
directories. The next command moved it to `/output/context-before.md`.
This was a temporary violation corrected within the run, with no observed project
or source corruption. The run is retained unchanged.

The [trace review](../evals/results/2026-09-27-history/trace-review.json) records
both successful commands. This supplementary finding does not rewrite the frozen
content scores; it prevents interpreting perfect mechanical rewards as full task
compliance. No critical factual document error was found in the reviewed records.
The command review is not a filesystem syscall audit and cannot prove the absence
of all possible out-of-scope activity.

## Method and limits

This study replays two real policy histories from one project, Python, using six
pinned PEP texts. It is a documentation-workspace experiment, not a deployment or
full-repository coding benchmark. PEP 387's three cutoffs span 2020–2025; PEP 602's
span 2019–2024. Each begins with only a README and raw evidence index. All source
texts remain unchanged, including their inconsistencies. Images and externally
linked pages are not included; scored facts are available in the supplied text.

The protocol, sources, questions, reviews' acceptance rules, harness and skill
were frozen in `85936ea` before scored model execution. Two maintenance methods
receive the same task and evidence; Context Docs v0.1.1 adds only its explicit
invocation and package. Each has an initial pass, two chronological updates and
a final no-new-evidence review. Prior actual outputs carry forward in fresh
sessions. A third unmaintained arm receives the same raw updates without editing.

Four maintenance trajectories produce 16 sessions. Each of the six final
artifacts gets two fresh read-only readers answering eight questions in two
frozen wordings: 12 reader sessions, 96 answers; **28 model sessions total**.
Readers see the same raw history across arms. The history concerns policy,
approval and rationale rather than facts recoverable from implementation code.
Readers are instructed to read all Markdown context before answering; the same
conservative model-visible exposure check as the routing follow-up checks every
unique nonblank line. Exposure does not prove comprehension or causal use.

Document review covers all Markdown at all four stages, including source links,
status, rationale, exceptions and historical supersession. Missing, incorrect and
conflicting items remain separate. Raw source survival or an unlabeled source
index alone does not earn context-retention credit. Explicitly qualifying a real
source contradiction is correct; changing the raw text or inventing its resolution
is not. Reader support requires relevant citations, not merely existing paths.
Justified unknowns about downstream adoption count as correct.

The unchanged execution configuration is Harbor 0.23.0, Codex CLI
0.158.0-alpha.2, gpt-6-astra low, three concurrent trials and a 480-second session
limit, with no retries. Runtime and token use remain secondary diagnostics.
Reference and no-op trials test mechanics; semantic correctness is explicitly
reviewed separately. Source pins, snapshots, outputs, reviews and reproduction
commands are linked in the evidence directory and frozen protocol.

These are two selected histories from the same ecosystem and one maintenance
trajectory per method/history. Their decisions were externally authored; snapshot
selection, workspace, questions and judgments are by the authoring agent, not an
independent or blinded reviewer. Public PEPs may be familiar to the model. The
cutoffs are historical and the study does not assess current Python policy.
Question counts and repeated readers do not create independent projects. Ties
establish neither equivalence nor a general benefit; isolated failures do not
justify broad instruction changes without replication. Skill v0.1.1 is unchanged.

## Validation and practical conclusion

All eight reference/no-op control trials behaved as expected. The two reader
control packages were built while maintenance finished; all 28 files match their
corresponding scored packages byte-for-byte. Recorded-input audits passed for all
28 sessions, without unexpected user/global AGENTS instructions. All 12 readers
preserved project bytes and Git state; all answer schemas/citation paths passed.
No Harbor execution exceptions or timeouts occurred. Some commands were corrected
within a session; this is distinct from rerunning a scored session.

The source and skill hashes match the freeze, all four maintenance trajectories
have verified actual-input continuity, and the reader artifacts match actual final
outputs. The published table reproduces from 24 explicit document reviews and
96 explicit answer reviews. Every unique nonblank Markdown line was displayed to
each reader before the first answer-file call. Citation contents and complete
answers were reviewed against the frozen criteria; mechanical rewards alone do
not establish semantic correctness. Publication checks verify original output
exports, local links and absence of host paths/credential patterns in artifacts.

The useful result is preservation through changing requirements and stability when
nothing changes. It does not justify additional skill rules or a superiority
claim. Repeating similar searchable policy questions would add little; a stronger
next contribution would be independently supplied histories from other projects
and condition-blind review. The earlier private-project contradiction miss and all
previous studies remain visible.

See the [frozen protocol](../evals/history/README.md),
[source provenance](../evals/history/provenance.json),
[criteria](../evals/history/cases.json), and
[reproducible evidence](../evals/results/2026-09-27-history/README.md).
