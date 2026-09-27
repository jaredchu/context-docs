# Public decision history evaluation

Frozen protocol for four maintenance passes and fresh readers. No results yet at
protocol freeze. The installable skill remains v0.1.1; no prompt tuning is part
of this study. Extends the [quality-first protocol](../quality-protocol.md).

## Question and sources

Can project context preserve changing decisions, rationale, authority and
exceptions across sessions, and support correct answers by new readers?
Speed and document length are secondary diagnostics.

Two externally authored **decision histories from one project**, Python PEP 387
and PEP 602, are replayed in disposable documentation workspaces. These are not
two independent projects or full production repositories. They contain no code
from which the policy decisions could be recovered. The six complete text
snapshots are unmodified, pinned and hashed in [provenance.json](provenance.json).
Original images and externally linked discussions are not included. All scored
facts are in supplied text. See [attribution](THIRD-PARTY-NOTICES.md).

| History | Initial cutoff | Update 1 | Update 2 | Pass 4 |
| --- | --- | --- | --- | --- |
| Compatibility | 2020-07-20 Active policy | 2023-07-03 soft-deprecation text | 2025-02-24 five-year preference and other intervening updates | No new evidence |
| Releases | 2019-09-10 draft | 2019-11-07 accepted terms | 2024-05-28 Active/Process, version-specific support | No new evidence |

Dates are source snapshots, not necessarily approval/effective dates. Source
history contains authentic inconsistencies: the first release draft's 16/17-month
total, later LTS wording versus the version-specific implementation section,
and historical deprecation terminology. Identifying a conflict with its limits is
correct; inventing a resolution or silently changing immutable evidence is not.
Neither protocol nor reviews may infer downstream adoption from policy acceptance.

The decision texts are independent of Context Docs. Snapshot selection, workspace,
questions, reference synthesis and reviews are author-created, neither independent
nor blinded. Familiar public PEPs may be in model training data. Historical-cutoff
answers must cite supplied evidence, not present-day knowledge.

## Matched comparison

Each starts with a minimal README linking an evidence index and no maintained
context. Compare unmaintained, competent ordinary maintenance, and explicitly
invoked Context Docs. Both maintainers receive identical substantive requests;
only the skill invocation/package differ. Layout is free and README links are
allowed. No treatment gets exclusive facts or reference answers.

Passes 1–3 receive chronologically accumulating raw snapshots, with the index
updated to the cutoff. Previous sources remain accessible unchanged. Pass 4 is a
no-new-evidence correctness/consistency review. Actual prior agent outputs—not
reference solutions—carry to each next fresh agent session. Inspect and publish
all four artifacts; a failed scope check is not repaired before reading.

Two histories × two methods × four passes = **16 maintenance sessions** in four
multi-step trials. Each of six final artifacts gets two fresh readers with the
same two frozen question variants: **12 readers, 96 answers**, total **28 model
sessions**. One maintenance trajectory per method/history limits generalization.
No statistical-significance, equivalence, speed or broad superiority claim.

All readers have equal access to complete raw evidence. They must start at README
and read every Markdown context document before answering. Verify displayed text
with the existing conservative [exposure detector](../routing/exposure.py): every
unique nonblank line before the first answer-file call, allowing split reads.
This measures exposure, not comprehension or dependence. Keep skipped-document
readers in the accuracy denominator. Raw-only readers may still answer perfectly;
that is a ceiling, not grounds to remove evidence or weaken the baseline.

Harbor 0.23.0, Codex CLI 0.158.0-alpha.2, gpt-6-astra low, three concurrent trials,
480 seconds per session, no retries. Same isolated configuration as earlier
studies, no host global/project instructions. Alternate method submission order
by history; reader ordering is by opaque ID. These sessions have no skill or
maintenance conversation. No browsing or external source execution is allowed.

## Scoring fixed before execution

[cases.json](cases.json) defines stage-specific atomic knowledge items, their
sources and two question phrasings. Seven compatibility items at stage 1 and eight
thereafter; eight release items at every stage. This is **63 item assessments per
arm across four stages**, including 16 at the final stage. New soft-deprecation
semantics are not required before they appear in evidence.

Review all maintained Markdown, using `correct`, `missing`, `incorrect`, or
`conflicting` per item with source-backed notes. Correct requires material
status, rationale and constraints in the item, or a specifically labeled canonical
link to that detail. A general evidence directory/index or raw-file survival does
not earn retention credit. An explicitly qualified historical claim is not an
operative conflict. Read the source cited before accepting a link as preservation.
Scan other claims as well; record invented approval, erased unique constraints,
unsupported current instructions and unqualified contradictions as critical
findings, with minor wording issues separately. Missing initial context alone is
a gap, not a critical fabrication. If an item is incomplete but all recorded parts
are true, score missing and identify the missing parts rather than calling it
false. Unresolved authentic source conflicts should remain explicit.

Measure final and every-stage knowledge coverage; show missing/incorrect/conflicting
items and critical findings, including their stage. Target-claim accuracy can be
derived as correct / (correct + incorrect + conflicting), with missing separately;
no assessed claims means undefined. Track previously correct items becoming
non-correct at later stages against stage-appropriate truth, and report the exact
loss/change rather than interpreting correct supersession as forgetting. Report
whether the final no-change pass preserves Markdown bytes; justified repairs are
allowed and must be explained.

Each reader answer has explicit `correct`, `supported`, and `critical` review
fields and reasoning. Correct requires all material requested conclusions, status,
exceptions and uncertainty. Sources or their explicit source chain must support
the answer; a path existing is insufficient. A justified unknown passes. Fabricated
approval/adoption is critical. Success also requires mechanical scope checks and
no execution error. Count answers correct in both question variants separately.
No composite score trades away a critical failure for brevity.

## Validation and execution

Freeze this protocol, source snapshots, skill hashes, prompts, criteria, exposure
and reporting code before scored models. Run reference/no-op controls on each
history for maintenance and reading (eight control trials total). Reference docs
are controls, not competing agent artifacts. Unit controls exercise raw-source
preservation, missing answers, fabricated/unsupported claims, omitted facts,
conflicts and execution errors. Semantic examples below calibrate author review;
they are not an automatic semantic classifier:

- “Five years is mandatory for every removal”: incorrect timing claim.
- “The 2019 draft was accepted”: incorrect authority and critical fabrication.
- “All versions receive 24 months of bugfix support”: incorrect version scope.
- Unqualified 18-month and 24-month current rules together: conflicting.
- “Only upstream policy is supplied; downstream adoption is unknown”: correct.
- Accurate short context that drops exception authority: missing exception item.

Audit actual pre-pass input continuity, source bytes, Git and file scope, local
Markdown links, answer schema/citation paths, recorded user inputs, and reader
exposure. Failures/timeouts remain in published denominators with no reruns.
Semantic review is by the authoring agent and is reported separately from Harbor
mechanical rewards. Publish source pins, all resulting files, answers, explicit
reviews, checks, generated table, limits and unchanged skill version.

```sh
python3 evals/history/study.py selftest
python3 evals/history/report.py selftest
python3 evals/history/study.py build-maint .local/history-maint
python3 evals/history/study.py run .local/history-maint .local/history-jobs --prefix history-maint --mode oracle
python3 evals/history/study.py run .local/history-maint .local/history-jobs --prefix history-maint --mode nop
python3 evals/history/study.py run .local/history-maint .local/history-jobs --prefix history-maint --mode model
python3 evals/history/study.py collect .local/history-maint .local/history-jobs .local/history-maint-export --prefix history-maint
python3 evals/history/study.py build-readers .local/history-readers .local/history-maint-export
python3 evals/history/study.py run .local/history-readers .local/history-jobs --prefix history-read --mode oracle
python3 evals/history/study.py run .local/history-readers .local/history-jobs --prefix history-read --mode nop
python3 evals/history/study.py run .local/history-readers .local/history-jobs --prefix history-read --mode model
python3 evals/history/study.py collect .local/history-readers .local/history-jobs .local/history-read-export --prefix history-read
```
