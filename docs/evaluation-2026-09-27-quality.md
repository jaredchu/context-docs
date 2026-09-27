# Documentation quality and fresh-reader evaluation

Run September 27, 2026, using unchanged experimental skill v0.1.1.

Both ordinary maintenance and Context Docs produced final records with
**54/54 correctly captured knowledge items**, versus **12/54 unmaintained**.
Neither method lost a required item during the evidence update. **The skill did
not outperform ordinary maintenance on these quality measures.**

Fresh readers answered **72/72 questions correctly with supporting sources in
every arm**, including unmaintained documents. They could recover the answers from
the small, explicit raw evidence set. This is a ceiling result: it does not show
that maintained documentation is unnecessary, nor that the skill improves reader
accuracy or is equivalent to ordinary maintenance in general.

| Final-artifact measure | Unmaintained | Ordinary maintenance | Context Docs v0.1.1 |
| --- | ---: | ---: | ---: |
| Required knowledge recorded | 12/54 | 54/54 | 54/54 |
| Correct, supported reader answers | 72/72 | 72/72 | 72/72 |
| Correct in both reader sessions | 36/36 | 36/36 | 36/36 |
| Target-claim accuracy | 37.5% | 100.0% | 100.0% |
| Missing required items | 22 | 0 | 0 |
| Incorrect required items | 20 | 0 | 0 |
| Critical document findings | 11 | 0 | 0 |
| Conflicting required items | 0 | 0 | 0 |

The 20 incorrect unmaintained items include 11 critical findings, such as invented
approval, runtime state and ownership. Missing documentation counts against
coverage, not as a fabricated fact. See the scoring distinctions below.

## What was compared

Two synthetic projects, Kestrel and Oriole, each start with scattered notes,
conflicting guidance, or no maintained context. Every condition retains the same
underlying evidence, configuration and uncommitted work note. Each scenario has
three arms: unmaintained, ordinary agent maintenance, and explicitly invoked
Context Docs. The unmaintained arm receives the same later evidence/configuration
updates without a documentation edit.

The two maintenance arms each perform an initial update, respond to new evidence,
and review again with no new information. That is **12 maintenance trials / 36
agent sessions**. Each of the **18 final artifacts** receives two fresh readers
answering equivalent versions of six questions: **36 reader sessions / 216
answers**. Documentation is reviewed at all three stages: **54 snapshots / 486
ledger-item judgments**, including the unmaintained arm. These are two projects,
not 216 independent examples; each scenario/maintenance arm has only one trial.

The questions test current approval and rationale, proposed features, configured
versus runtime state, closed versus open work, durable constraints and unknown
responsibility. Examples include keeping an allocated restore fixture's sparse-file
constraint after its exercise closes, and approving local JSON output without
silently approving a hosted viewer or input modification.

Readers receive the actual final project, including any defects, and all common
raw evidence. They receive no skill, maintenance conversation, treatment label or
answer key. Both variants use identical prompts across arms within each world.
The model can inspect every file; there is no artificial restriction forcing it to
trust maintained Markdown or ignore raw evidence.

## Results by starting condition

| Project / starting condition | Recorded items: unmaintained | Ordinary | Context Docs | Reader answers: each arm |
| --- | ---: | ---: | ---: | ---: |
| kestrel / scattered | 6/9 | 9/9 | 9/9 | 12/12 |
| kestrel / conflicting | 0/9 | 9/9 | 9/9 | 12/12 |
| kestrel / absent | 0/9 | 9/9 | 9/9 | 12/12 |
| oriole / scattered | 6/9 | 9/9 | 9/9 | 12/12 |
| oriole / conflicting | 0/9 | 9/9 | 9/9 | 12/12 |
| oriole / absent | 0/9 | 9/9 | 9/9 | 12/12 |

Both question variants pass every scenario; each arm has 6/6 consistently correct
question pairs per scenario. All 36 reader projects remain byte-identical, and
all 36 maintenance sessions pass file/link/Git checks.

## Preservation and evidence handling

Across all stages, both maintenance methods capture every required ledger item:
**162/162 per arm**, with no assessed incorrect, missing or conflicting item and
no observed critical document error. Neither loses a previously correct item
through the evidence update. All six final no-change passes per maintenance arm
leave Markdown byte-identical to the preceding output.

The unmaintained record declines from **15/54** correctly recorded items initially
to **12/54** after the common evidence update. Three previously correct items
become stale: Kestrel's completed restore task and Oriole's approved output scope
and completed sample task. Other incorrect or missing items already existed.
Raw evidence is preserved throughout; low document coverage does not mean that
information was deleted from the project.

All maintained artifacts preserve the uncommitted input bytes and source files.
Both methods retain rationale, unresolved ownership and operation details beyond
the fixed ledger, including revision-specific preview acceptance or source-export
retention. No additional material unsupported claims or lost unique details were
identified in the author review. This is observed coverage, not a guarantee that
all possible future questions have been anticipated.

Two inspectable unmaintained examples show the reader ceiling:

- Kestrel conflicting reader `f8ffa268f222-1` rejects the working note's automatic
  publication policy, cites Mira's DEC-101 and the later reaffirmation, and keeps
  the production timeout unknown despite the false production claim.
- Oriole conflicting reader `491aa2395738-1` distinguishes approved local JSON
  from the unapproved hosted viewer, preserves composite string identifiers,
  and rejects the working note assigning ledger-correction authority to Lina.

The complete answers and citations are in
[reader trials](../evals/results/2026-09-27-quality/reader-trials.json), with
[explicit reviews](../evals/results/2026-09-27-quality/reader-reviews.json).
Trace inspection found raw-evidence reads in all 36 sessions, commonly loading the
entire small source set in one batch. No reader critical errors were identified.

## Scoring and controls

The [execution plan](../evals/quality/README.md), fixtures, evidence ledger,
questions, review rules and harness were frozen in commit `64e059d` before scored
runs. Skill v0.1.1 remained unchanged. After execution, the table renderer was
expanded to expose incorrect/missing items, target-claim accuracy and critical
findings already present in the summary; all summary and score values remained
identical. Completion links/status text were also updated. Score-count field order
was made deterministic for repeatable JSON output. No grading rule changed.
No trial was tuned, retried, replaced or
excluded after seeing its result. All model trials completed without Harbor
execution exceptions.

Required knowledge coverage counts a correct maintained account or a specific,
meaningful link to its authoritative detail. A bare evidence-directory pointer
or surviving raw file does not count as maintained coverage. Target-claim
accuracy is correct / (correct + incorrect + conflicting) across the nine fixed
items; missing items are reported separately. It is not an exhaustive audit of
every factual sentence. No assessed claims means undefined accuracy, not 100%.

A false current instruction is scored **incorrect**; incompatible operative claims
left together in maintained documentation are scored **conflicting**. Thus the
conflicting-start condition can contain many incorrect items while scoring zero
in the narrower conflicting-item category. Read the incorrect and missing counts
alongside conflicts. Critical errors are explicit review findings, not additional
independent denominators.

Each reader answer must be correct, supported by the actual cited contents or
source chain, and pass the mechanical read-only/schema checks. A justified unknown
is correct; a fabricated approval, runtime state or owner is a critical error.
Consistent-correct pairs require both versions to pass, so consistently wrong
answers earn no credit. Questions and pairs are weighted equally in this balanced
six-scenario design; no significance test treats them as independent projects.

The authoring assistant reviewed every document stage and reader answer, with
reasons and source paths recorded. Review packets omit treatment labels, but
project structure and run diagnostics can reveal them. **This is neither
independent nor fully blinded review.** The five predeclared semantic controls
exercise missing detail, contradiction, invented approval, false production
inference and justified uncertainty; they are manual scoring examples, not an
independent automatic judge.

- Local controls passed 66 reference/scope/schema assertions, including rejecting
  broken links, missing reader answers and unauthorized reader edits.
- Six maintenance reference controls passed all stages; six no-op controls failed
  both required edits and passed only the no-change stage.
- Two reader reference controls passed; both no-op readers failed.
- All later maintenance inputs match actual preceding outputs. Reader hashes match
  actual final artifacts, and non-Markdown evidence is identical across arms.
- Recorded-input audits pass all 72 model sessions: 72 expected task messages,
  72 container environment messages, zero unexpected user or injected `AGENTS.md`
  messages. All 18 skill maintenance sessions read the skill and standard; no
  ordinary maintainer or reader reads the skill.

## Limits and next decision

These author-created inputs contain only 514–656 total whitespace-separated words
initially, including 32–160 Markdown words. Facts and authority are deliberately
explicit. There is no implementation code, long search space, real production
access, human reader or independent project contributor. The same model performs
maintenance and reading in separate sessions. Shared task instructions already
ask ordinary maintenance to preserve evidence, decisions and scope.

Questions name relevant tickets and explicitly ask readers to separate configured
from running state and approved from proposed scope. They test those answers,
not whether a reader notices an unprompted risk during an unrelated task.

The next useful evidence is independently authored, larger project cases with
natural continuation questions and longer maintenance histories, frozen before
further skill tuning. Keep equal evidence access and a competent ordinary baseline.
Do not hide sources or select weaker baselines just to produce a skill win.

The [earlier local-project pilot](evaluation-2026-09-26.md) still includes a
workflow contradiction the skill missed. This study does not erase it. Keep
v0.1.1 experimental; these results do not establish automatic skill selection,
other-model performance or long-term maintenance quality.

## Reproduction and evidence

Harbor 0.23.0, Codex CLI 0.158.0-alpha.2, `gpt-6-astra` at low effort; three
concurrent trials, 240-second agent limit, no automatic retries. Matched maintenance
submission order alternates; reader order uses opaque hashes. Containers and an
isolated Codex home exclude host skills/global instructions. Each maintenance
stage starts a fresh agent session over its preceding artifact; readers start in
fresh containers without maintenance history. This is a trusted fixture harness,
not a security boundary against malicious root access.

See the [commands and frozen rules](../evals/quality/README.md) and
[published artifacts](../evals/results/2026-09-27-quality/README.md). Regenerate
summaries from the saved snapshots and explicit reviews:

```sh
python3 evals/quality/report.py evals/results/2026-09-27-quality
```

Time, tokens and document size remain supporting diagnostics in the artifacts;
there is no speed ranking or claim of cost savings. Raw authenticated sessions
and private project contents are not published.
