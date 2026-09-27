# README routing and handoff exposure follow-up

Freeze this protocol, prompts, decoder, aggregator and input hashes before model
execution. This is a follow-up to the [public-source pilot](../../docs/evaluation-2026-09-27-public.md),
whose readers did not consume added handoffs. It is not a new held-out benchmark.
The skill, handoffs, upstream pins, questions and semantic criteria stay unchanged.

## Design

Reuse the four actual [published handoffs](../results/2026-09-27-public/maintenance.json)
without editing or regenerating them. Reconstruct all six original artifacts
(two projects × upstream/ordinary/skill), verify their hashes, then prepend the
same labeled `Contributor orientation` block to each temporary README. Its
`Project orientation` link targets the generated handoff in maintained artifacts,
or the existing `docs/index.rst` in upstream-only artifacts. The target differs;
label and placement are identical. This is a harness-authored routing intervention,
not evidence that the skill itself installs routing automatically. Upstream clones
and earlier published results stay untouched. All other source bytes stay equal.

Two reader modes × two projects × three artifact conditions = **12 fresh model
sessions, 72 answers**. Use the existing second question phrasing (variant 1)
for every session, including the question whose ordinary reader previously
omitted a cleanup guard. This is an explicit known-case follow-up, not a fresh
sample or a comparable replacement for the earlier two-phrasing aggregate.

- **README-first discovery:** begin by reading README.md, then choose sources.
  Following its orientation link is not explicitly required.
- **Directed reading:** read README.md, follow its Project orientation link and
  read the target in full before writing answers, then check relevant sources.

Within each mode, prompts are identical across arms apart from project questions.
No arm labels, skills, global instructions, score keys, hints about the previous
miss, or maintenance conversations reach readers. All can inspect the complete
same upstream source, docs and tests; orientation is a guide, not privileged truth.
Existing source evidence stays available. No upstream code/test execution,
dependency installation, external services, project edits or Git changes.

## Outcomes and interpretation

Report answer quality and orientation exposure **separately by mode and arm**.
Keep all assigned sessions in the accuracy denominator, including missing answers
and execution failures. Do not exclude readers who skip the orientation.
Reuse the [frozen answer criteria](../public/cases.json): both required criteria,
material citation support and no material false claim. Review omissions explicitly,
including missing-resource cleanup. Citations alone do not supply an omitted
reader answer detail. Unasked trivia does not fail an answer. Minor lazy-default
shorthand is recorded consistently with the previous review. Author review is
unblinded and not independent. A one-answer difference establishes no superiority.

Exposure means that the linked document's full text was returned in recorded,
**model-visible** tool responses before the first tool call referencing
`answers.json`. It does not prove comprehension, reliance or causal benefit.
Raw execution output may contain material truncated before reaching the model,
so it is not sufficient. Parse `response_item` tool-output events from session
JSONL, decode text blocks / JSON-wrapped exec outputs, then compare stripped
nonblank document lines with visible output lines. Every distinct nonblank line
must occur; split reads count. No fuzzy match or post-run override. Unrecognized
formatting or early answer-file preparation can yield conservative false negatives.
A file listing, a heading, a partial excerpt, a citation or self-report alone does
not establish full exposure. Require the same detector for upstream index and
both kinds of handoff, and audit README exposure as a separate diagnostic.

Report the fraction fully exposed for all six sessions in each mode. If directed
readers are not verified, state that the planned consumption manipulation failed;
do not claim an effect of consumption. Even verified exposure plus a tied score
cannot establish equivalence. The original tasks may remain too easy with common
source access. Do not keep changing prompts until a preferred result appears.

## Execution, controls and publication

Reuse Harbor 0.23.0, Codex CLI 0.158.0-alpha.2, gpt-6-astra/low, concurrency three,
480-second session limit, sorted opaque task IDs and no retries from the previous
study. Global/project instruction injection remains disabled. A model session is
not a delegated authoring agent; no subagents are used to build or judge this study.

Before scored execution, run reference and no-op scope/schema controls for both
projects (four container runs); the same frozen grader applies to both modes.
Test the exposure decoder against no output, file listing, partial, split and full
text, and JSON-wrapped model output. Check the reconstructed input hashes and
README-only changes. Freeze everything in Git before building scored packages.
Retain execution failures and report any later rerun separately.

Publish all answers, explicit reviews, exposure counts/missing-line indices,
source-call evidence, input hashes, controls, isolation audit and generated table.
Raw sessions stay local due to service metadata. This is inspectable evidence,
not a tamper-proof runner audit. Timing/token diagnostics remain secondary.
No skill change follows merely from these scores.

## Reproduce

From the repository root, with the previous study's Docker/uv/Codex login setup:

```sh
python3 evals/routing/run.py selftest
python3 evals/routing/run.py build .local/routing-readers
python3 evals/public/study.py run .local/routing-readers .local/routing-jobs --prefix routing --mode oracle
python3 evals/public/study.py run .local/routing-readers .local/routing-jobs --prefix routing --mode nop
python3 evals/public/study.py run .local/routing-readers .local/routing-jobs --prefix routing --mode model
python3 evals/public/study.py collect .local/routing-readers .local/routing-jobs .local/routing-export --prefix routing
python3 evals/routing/run.py exposure .local/routing-readers .local/routing-jobs .local/routing-exposure.json --prefix routing
python3 evals/suite/audit_isolation.py .local/routing-jobs .local/routing-readers .local/routing-isolation.json --prefix routing
```

Prepare explicit per-answer reviews, then call `evals/routing/report.py` with the
exported trials, reviews, exposure audit and output directory. No semantic score
is inferred from the mechanical reward or exposure detector.

Limits: same two familiar Pallets projects, four prior handoffs, one reader sample
per project/arm/mode, reused questions, no independent judge and no longitudinal
maintenance sequence. This isolates a reader-entry intervention, not the complete
real-world workflow or the effects of removing source evidence.
