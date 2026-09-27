# Public Harbor evaluation

Date: 2026-09-27. Skill: unchanged v0.1.0. Frozen execution source:
`f308aa1` (full commit and file hashes in the manifest).

**Outcome:** both conditions passed all 24 trials. The skill showed no correctness
advantage on these small fixtures, used more tokens and time, and produced larger
additions in several tasks. This is useful regression coverage, not evidence of
general superiority or equivalence. No skill instructions were tuned during or
after the experiment.

## Task results

Success requires every mechanical check and every semantic rubric item across
all steps, with no execution error. These are eight distinct tasks, each repeated
three times per condition, not 24 independent tasks per condition.

| Task | Ordinary instructions | With Context Docs |
| --- | ---: | ---: |
| stale-config | 3/3 | 3/3 |
| workflow-conflict | 3/3 | 3/3 |
| decision-status | 3/3 | 3/3 |
| uncommitted-work | 3/3 | 3/3 |
| links-and-fences | 3/3 | 3/3 |
| audit-only | 3/3 | 3/3 |
| initialize | 3/3 | 3/3 |
| repeated-maintenance | 3/3 | 3/3 |
| **Total trials** | **24/24** | **24/24** |

All six audit trials left project files byte-for-byte unchanged. All six final
no-change maintenance passes left project Markdown unchanged. The specific
workflow conflict was reconciled in all six trials. The
[earlier private pilot](evaluation-2026-09-26.md) still records a skill miss on a
larger natural-cleanup task; success on this explicit synthetic fixture does not
invalidate that observation or prove the failure fixed.

## Resources and document growth

| Metric | Ordinary instructions | With Context Docs |
| --- | ---: | ---: |
| Median agent time per trial | 40.2 s | 45.3 s |
| Total input tokens | 1,341,914 | 1,748,347 |
| Cached input tokens | 1,035,136 | 1,421,952 |
| Uncached input tokens | 306,778 | 326,395 |
| Output tokens | 17,436 | 24,525 |

Agent-phase time excludes container build/setup and author review; repeated-task
trials sum their three sessions. Runtime ranges were 24.2–76.1 seconds for ordinary
instructions and 31.2–93.0 seconds with the skill. Caching and service latency were
not controlled. Token totals include repeated context and tool output. Harbor's
estimated dollar figures are excluded: subscription cost was not measured.

Whole-project Markdown growth depends strongly on the task:

| Task | Baseline median word change | Skill median word change |
| --- | ---: | ---: |
| stale-config | +16 | +33 |
| workflow-conflict | +230 | +323 |
| decision-status | +54 | +71 |
| uncommitted-work | -8 | -9 |
| links-and-fences | -4 | -4 |
| audit-only | +0 | +0 |
| initialize | +53 | +117 |
| repeated-maintenance | +2 | +14 |

Words are counted by whitespace splitting. Growth is final project Markdown minus
its initial snapshot, including all context files. Audit reports live outside the
project and are excluded; their full text is available in the evidence. The skill
added more project text in five of eight task categories, less in one and the same
median amount in two. Extra evidence and caveats can be useful, but these results
do not support a claim that the skill generally shrinks documentation. In
particular, workflow guidance and initialization warrant a closer verbosity review.

## Method and controls

- Runner: Harbor 0.23.0, local Docker; Codex CLI 0.158.0-alpha.2;
  `gpt-6-astra`, low reasoning effort, existing subscription authentication.
- Three sequential blocks, each with both conditions for all eight tasks; two
  concurrent trials. Submitted condition order alternated by task/block. Actual
  completion order depended on execution time.
- Fresh containers per trial. Repeated maintenance used three fresh sessions over
  evolving files: configuration 60, then 45, then a no-change review. The 48
  scored trials therefore contain 60 agent invocations. One separate authentication
  probe was excluded, as were all reference/no-op controls and authoring work.
- Both conditions received identical project bytes and ordinary scope/preservation
  constraints. Only the treatment received the skill files and an explicit use
  instruction. Traces show skill-read requests in all 30 treatment sessions and
  none in the 30 baseline sessions. Automatic activation was not tested.
- Eight reference controls passed and eight complete no-op trials were rejected.
  Local reference/broken-link/lost-file checks passed 41 assertions. A setup-script
  cleanup defect was found during preflight, repaired, and its affected controls
  rerun before any scored trial. Unaffected packages were byte-identical.
- Mechanical graders checked scope, protected literals, input retention, links,
  anchors and Git state. The authoring assistant reviewed all 60 step outputs
  against the published three-item semantic rubrics and inspected all six
  uncommitted-edit traces. Review packets omitted condition labels, but this was
  **not independent or fully blinded judging**. Reasons are published per step.
- No scored trial was retried, discarded or replaced. All 48 completed without
  execution exceptions. Skill, fixtures, rubrics and execution settings stayed
  fixed; postprocessing changes handled timestamp parsing and report generation.

## Limits and next improvement

The initial Markdown corpora contain only 19–87 whitespace-separated words.
They are synthetic development fixtures authored with knowledge of the skill,
not held-out projects. The competent baseline also received explicit preservation
and scope instructions. Perfect scores here suggest a ceiling in this suite;
they do not prove reliability on large, noisy or ambiguous repositories.

Later maintenance stages compare a mechanical document-change check against the
reference-stage input rather than the preceding actual output. The no-op control
can consequently earn partial Harbor reward, while still failing the whole trial.
Semantic review checked actual progression and final no-change behavior. Do not
interpret Harbor's mean mechanical reward as accuracy. Capturing actual per-step
input snapshots is a concrete harness improvement for the next version.

Keep this baseline intact. Next, add larger unseen fixtures with dispersed and
ambiguous evidence, improve per-step snapshot grading, and test a fresh reader's
answers. If reducing repeated caveats or guidance in the skill, evaluate that as
a separate candidate against this baseline and unseen tasks. Cross-model results,
automatic activation, long-term maintenance and real cost remain unmeasured.

## Reproduce and inspect

- [Suite instructions and reproducible commands](../evals/suite/README.md)
- [Synthetic fixtures, reference outputs and rubrics](../evals/suite/cases.py)
- [Per-trial synthetic documents, tool calls and metrics](../evals/results/2026-09-27-harbor/trials.json)
- [Semantic review decisions and reasons](../evals/results/2026-09-27-harbor/reviews.json)
- [Derived summary](../evals/results/2026-09-27-harbor/summary.json)
- [Versions, frozen hashes and provenance](../evals/results/2026-09-27-harbor/manifest.json)
- [Reference and no-op control results](../evals/results/2026-09-27-harbor/controls.json)

These are custom Harbor tasks, not a SkillsBench submission or external leaderboard
score. Published evidence contains synthetic project material and selected tool
calls only. Raw Harbor logs, system prompts, authentication, and the earlier
private-project snapshots remain outside the public repository.
