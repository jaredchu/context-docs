# From project source to usable documentation: three public cases

**November 14, 2026 · Exploratory, agent-only study · Local draft; not published.**

We compared the original documentation of three pinned public projects with
documentation written by an AI agent using ordinary Markdown or Context Docs.
A fresh agent then answered eight questions per project using only saved documents.

Both writing conditions yielded more fully correct, validly cited answers than
the original docs on the sampled supported questions. **Context Docs did not
outperform ordinary Markdown on this metric:** ordinary scored **4/6, 3/6 and
3/6**; Context Docs scored **3–4/6, 2/6 and 2/6**. Two key/question disputes remain
unresolved. These are AI assessments on three selected cases, with one writer
per writing condition and case, rather than a general ranking of methods.

Context Docs supplies a [ready-to-apply documentation standard](../skills/context-docs/references/standard.md).
This experiment did not measure the work avoided by having conventions ready,
newcomer understanding, human effort, or ongoing maintenance. Providing a useful
standard does not require beating competent ordinary writing; factual omissions
and errors in its outputs still matter.

## Cases and conditions

The cases were the first three eligible entries in a frozen twelve-repository
screening frame, at ranks 1, 2 and 4. Rank 3 exceeded the size bound; later
candidates were not fully screened. Selection sought thin or fragmented existing
docs with recoverable source facts. These projects already had documentation;
they were not a random sample of undocumented projects.

| Case | Pinned project | Commit | Captured files |
| --- | --- | --- | ---: |
| P01 | [ulyssestenn/omt](https://github.com/ulyssestenn/omt/tree/8a08c6e76824b02b971a43b414518fb1f5a28e3c) | `8a08c6e76824b02b971a43b414518fb1f5a28e3c` | 4 |
| P02 | [Alex72-py/aria-termux](https://github.com/Alex72-py/aria-termux/tree/98140598c0a81e2ffc352a9886d28ee83d118d47) | `98140598c0a81e2ffc352a9886d28ee83d118d47` | 29 |
| P03 | [kMegapnbedt/Bench-B](https://github.com/kMegapnbedt/Bench-B/tree/0dafa0494c0946a9ad25a6e7234f6155c0f1a651) | `0dafa0494c0946a9ad25a6e7234f6155c0f1a651` | 28 |

These are local copies of pinned trees, not changes adopted by the upstream
projects or statements about their current documentation. Original license
notices are retained in the evidence. P01 is mostly one Python file; its source
variety relies partly on `.gitignore` and README examples.

Each project had three conditions:

- **Original docs:** no writer; the reader received eligible documents from the
  captured tree.
- **Ordinary Markdown:** a writer received the project and the goal of preparing
  useful documentation for a returning collaborator, preserving useful material
  and documenting only what evidence supports. It could choose its layout.
- **Context Docs:** the same goal and source access, plus an explicit
  `$adopt-context-docs` instruction and the two pinned method packages.

Writers did not receive the reader questions or reference keys. Both writing
conditions could create or replace visible Markdown, including `AGENTS.md` or
`CLAUDE.md`, and received the same technical limits. Ordinary writing was an
active comparator, not an unattended baseline.

Readers received only visible UTF-8 `.md`/`.markdown` files and the root `LICENSE`.
Dot-paths, any `skills/` directory, source code, configuration and history were
excluded. Reader working directories were empty and outside those document views;
saved agent instructions were project data, not automatically loaded instructions.
No project code, tests, builds or package scripts were executed.

## Execution and controls

All **21 sessions** completed: six writers, nine readers and six graders. Every
reader and grader output passed its JSON validation; there were no unavailable
outputs, session retries, timeouts, fallback models or invalidity halts.

All study roles used configured **Codex CLI 0.167.0-alpha.4.1**, **`gpt-6-astra`**,
requested **High**, with fresh ephemeral sessions and one submitted user turn.
These are client/configuration observations, not independent attestation of
provider model weights or runtime reasoning effort. Internal inference/tool
rounds were allowed within the role limits; one turn is not one inference call.
Token usage was measured and uncapped.

The method packages were core **0.2.7** and adoption **0.1.16**, from product
commit `ff0a123bd2b7f284e1f2a1e84fcbfd3e81d16f22`, with exact file hashes in the
[evidence](../evals/results/2026-11-14-public-project-docs/study.json).
The treatment is **explicitly invoked, creation-only, skill-guided adoption**.
Automatic loading of the newly written project instructions and ongoing
maintenance were deliberately untested; no fully verified setup is claimed.

| Role | Sessions | Wall-clock cap each | Filesystem-call cap each |
| --- | ---: | ---: | ---: |
| Writer | 6 | 1,800 seconds | 60 |
| Reader | 9 | 300 seconds | 20 |
| Grader | 6 | 600 seconds | 0 observable tool attempts |

Saved Markdown was limited to 98,304 UTF-8 bytes per writing condition/project,
with at most 65,536 bytes per line. Complete grader input was capped at 800,000
bytes, with no truncation or selective omission. That byte cap does not guarantee
token fit. The largest actual input was 488,195 bytes; all six grading sessions
finished within their limits.

The writing order was ordinary then Context Docs for P01/P03, reversed for P02.
Reader order followed a three-condition Latin square. All writers finished before
all readers; all first grading passes finished and were locked before any second
pass. There was one run per condition/case, with no replication.

The configuration disabled shell, network, apps/plugins, memories, hooks and
delegation. A trusted scoped filesystem server enforced role access and Markdown
writes alongside the native read-only filesystem policy. Ordinary writers and
readers had the target skills disabled; treatment writers had exactly the two
pinned project packages enabled and readable. Project-instruction autoload was
suppressed equally. Inspected generic global preferences remained present,
without study-key or method guidance.

Graders had complete packets inline and no filesystem server. All six recorded
zero observable tool attempts. Native orchestration/read-only helpers may remain
exposed, and CLI telemetry does not show every invocation: this is not proof of
literal zero tool calls or whole-host isolation.

Before the first scored call, controller review required repairs to outcome
integrity, unavailable/report guard paths and context-limit handling. Thirty-seven
synthetic checks and a focused independent review passed afterward. The initial
static preparation is retained separately and produced no scored sessions.
Original inputs/configuration and before/after session guards matched throughout
the scored run; no outcomes were used to revise prompts, keys or scoring.

## Scoring and two-pass grading

Each project had six supported questions, K1–K6, and two bounded-unknown questions,
U1–U2: **72 reader-answer cells and 144 model-grade cells** across both passes.
Keys were source-derived, prepared by `claude-opus-5-5` and independently reviewed
by `gpt-6-astra` before the run, without human oracle validation.

- **Supported correct /6:** every required point is covered and no rejection
  condition fires. Partial answers count zero here and are reported separately.
- **Useful cited correct /6:** supported correct, a saved-document citation that
  supports the answer and agrees with the key/source, and a passing mechanical
  file/line existence check.
- **Unknown correct /2:** the answer states that the matter is not established
  within the pinned tree and does not invent intent, approval, plans or dates.
  This does not mean the answer is absent from all history or external sources.
- **Flags:** invented unknown facts, critical fabrications, lost constraints and
  invalid citations are separate from correctness counts.

Each project received two fresh grading sessions using the same configured model
as writers/readers. Pass 1 received the frozen reference items, answers and every
saved document. Pass 2 also received the entire pinned source tree, checked each
key and audited consequential document claims. It never received pass-1 grades.
Grader labels A/B/C were permuted using a seed frozen before outcomes; the
coordinator knew the maps. Documents could reveal conditions, so blinding was
partial. Same-model systematic biases may be shared across every role.

An interval's lower endpoint counts what both passes award or flag; its upper
endpoint counts what either does. This is **grading disagreement, not a statistical
confidence interval**. Disputed items stay unresolved even where grades agree,
and remain scored against the unchanged frozen key. There was no tie-breaker,
coordinator semantic adjudication or additional grading pass. Missing-reader and
missing-grader rules retained fixed denominators, although no output was missing.

## Results

| Case | Condition | Supported correct /6 | Partial /6 | Useful cited correct /6 | Unknown correct /2 |
| --- | --- | ---: | ---: | ---: | ---: |
| P01 | Original docs | 0 | 3 | 0 | 2 |
| P01 | Ordinary Markdown | 4 | 2 | 4 | 2 |
| P01 | Context Docs | 3–4 | 2–3 | 3–4 | 2 |
| P02 | Original docs | 0 | 2 | 0 | 2 |
| P02 | Ordinary Markdown | 3 | 3 | 3 | 2 |
| P02 | Context Docs | 2 | 4 | 2 | 2 |
| P03 | Original docs | 0 | 2 | 0 | 2 |
| P03 | Ordinary Markdown | 3 | 2 | 3 | 2 |
| P03 | Context Docs | 2 | 3 | 2 | 2 |

Zero in the original-docs supported columns means no sampled answer satisfied
every required point. Those readers still gave partial answers and correctly
bounded both unknowns. It does not mean the original documentation was useless.

Both passes recorded zero invented-unknown facts, critical fabrications and lost
constraints in the **reader answers** in every condition. P03 ordinary and Context
Docs each had one invalid-citation flag; all other reader citation-error counts
were zero. These bounded judgments do not guarantee that every answer detail is
correct, and they are separate from the document audit below.

### Unresolved key and question disputes

- **P01 K6:** pass 1 flagged an oracle error: a `.gitignore` rule alone does not
  prove that an output is untracked, since an already tracked file stays tracked.
  Pass 2 assessed the key as supported. The disagreement is retained; the key was
  not repaired. K6 is unresolved for all three conditions, even where grades agree.
- **P03 K2:** both passes flagged ambiguity in “the README's scan command exactly
  as written.” The pinned README omits `--id-field`; the two generated READMEs
  include it. Readers could answer about the document actually supplied. Pass 2
  marked the key disputed for this referent ambiguity while noting that the key
  describes the pinned command accurately. Grades retain the original rejection
  rule; K2 stays unresolved for all conditions.

All other items were agreed within the two passes. These disputes are not grounds
for silently dropping items, changing denominators or declaring revised winners.

### Document-claim audit: pass 2 only, unreconciled

Each cell below is **flagged claims / claims flagged critical**. These counts are
single-pass model assessments, not confirmed defects or independent error events.
They cover consequential claims beyond the eight questions.

| Case | Condition | Contradicted | Unsupported | Fabricated authority | Lost constraint |
| --- | --- | ---: | ---: | ---: | ---: |
| P01 | Original docs | 0/0 | 0/0 | 0/0 | 1/0 |
| P01 | Ordinary Markdown | 0/0 | 0/0 | 0/0 | 0/0 |
| P01 | Context Docs | 0/0 | 2/1 | 1/1 | 0/0 |
| P02 | Original docs | 19/16 | 4/2 | 0/0 | 12/7 |
| P02 | Ordinary Markdown | 0/0 | 0/0 | 0/0 | 0/0 |
| P02 | Context Docs | 3/3 | 0/0 | 0/0 | 2/1 |
| P03 | Original docs | 4/4 | 5/2 | 0/0 | 3/3 |
| P03 | Ordinary Markdown | 0/0 | 0/0 | 0/0 | 0/0 |
| P03 | Context Docs | 0/0 | 0/0 | 1/1 | 0/0 |

Original-docs findings concern unchanged project prose. Flags in a generated
condition can concern retained upstream statements, including text inside a
modified file; they are not necessarily new errors introduced by that writer.
For example, P02 Context Docs flags include retained claims about key validation,
confirmation prompts and model compatibility. Accurate explanations elsewhere
did not cancel the auditor's flags.

**Method-authority evidence gap:** P01/P03 Context Docs flags include instructions
in generated `AGENTS.md` to use the skill for maintenance, a selected documentation
destination and a quoted adoption rule. The original grader packet deliberately
excluded writer requests and method packages. The auditor could therefore observe
that those instructions were absent from the upstream tree, but could not establish
whether the study's adoption request or authentic package authorized them.

These flags remain in the table and raw output, unreconciled. They are not proof
of fabricated product authority, and they have not been reclassified as harmless.
The public evidence supplies prompt and package provenance separately for
inspection; it was not retroactively given to graders. Neither a zero audit count
nor a large count establishes overall document quality.

## What this supports, and what remains unmeasured

Under this configuration, both writing approaches produced documentation that
supported more fully correct, validly cited answers on the sampled questions.
Neither approach covered every required detail; Context Docs showed no advantage
over ordinary writing on the primary metric. The experiment supports this narrow
observation, not superiority, equivalence or a general disadvantage conclusion.

There are three selected projects, one generation per writing condition/case,
one selected model, sparse questions, AI-prepared keys, shared model biases and
partial blinding. Public-code familiarity from training cannot be excluded.
The study was maintainer-run, not an external independent benchmark. Static source
reading does not establish runtime behavior. The disputed keys and audit evidence
gap further limit interpretation.

The convenience of having a standard ready, the effort of establishing conventions,
human/novice understanding, instruction-loading closure and ongoing maintenance
were not measured. This evidence supplies no compelling reason to change the
product or run another experiment now; it supplies no beginner-effort or accuracy
advantage claim for promotion.

## Inspect the evidence

The [portable evidence extract](../evals/results/2026-11-14-public-project-docs/README.md)
includes all 61 selected source files with licenses, all nine reader document views
and answers, all six final grading outputs, grader-visible keys, per-item
reconciliation, exact prompt templates/schemas, order/label maps, caps and usage.
Disputes, flags and scores are unchanged. No new subject run, grading session or
key correction was performed to prepare this write-up.

It is a maintainer-prepared derivative, not the complete original capture, an
independently authenticated replay or a turnkey runner. Private invocation IDs,
raw tool/transport logs, client/account settings and operator records are excluded.
The extract alone cannot independently verify model reads, every runtime control
or hidden tool activity. Its README describes the derivation and byte/hash limits.

This draft and evidence remain local. Publication, deployment and release are
separate actions requiring authorization.

Return to the [evidence overview](evaluation-results.md).
