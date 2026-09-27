# Evaluation framework research and next protocol

Reviewed: 2026-09-26. Status: historical recommendation and proposed protocol.
No framework integration or model evaluation was performed during that research.

Follow-up, 2026-09-27: the [Harbor suite](suite/README.md) is implemented and its
[48-trial evaluation](../docs/evaluation-2026-09-27.md) is complete. Both conditions
passed 24/24 trials; the report records resource overhead and limitations. The
protocol below is the original proposal, not a substitute for the executed method.

The owner subsequently clarified the evaluation priority: retained content,
accuracy and consistency, with weak or missing documentation as matched starting
conditions. The [quality-first protocol](quality-protocol.md) is the current
next-study design; the runner research and historical proposal below are retained.

## Recommendation

Use Harbor for a small public context-maintenance task suite, and use SkillsBench
as a reference for skill-versus-no-skill experimental design. Keep the current
skill fixed until the suite establishes a baseline. A runner provides execution
and reporting infrastructure; it does not supply the right documentation-specific
questions or prove that a skill is effective.

The search did not identify a ready-made benchmark specifically covering this
project's context-document lifecycle. That is a limited search finding, not proof
that no such benchmark exists. The current SkillsBench task-name scan did not
identify an obvious context-maintenance task; task names alone are not exhaustive
coverage analysis.

## Existing projects

| Project | Verified capability | Fit here |
| --- | --- | --- |
| [SkillsBench](https://github.com/benchflow-ai/skillsbench) | Benchmarks skill-assisted agent workflows; current task packages include environments, skills, reference solutions and verifiers | Closest research reference, but broad tasks are not automatically relevant to this particular skill |
| [Harbor](https://docs.harborframework.com/core-concepts/tasks/overview) | Reusable tasks combine instructions, environments and verification; supports labeled rewards and multi-step tasks | Recommended runner for filesystem changes, preservation checks and later longitudinal maintenance |
| [AWS sample-agent-skill-eval](https://github.com/aws-samples/sample-agent-skill-eval) | With/without-skill functional evaluation, trigger evaluation and reporting; its documented functional/trigger paths require Claude CLI | Relevant alternative, but not a direct fit for continuing the existing Codex experiment unchanged |

Harbor documents a Codex integration, including task-provided skills and native
configuration. Its illustrated setup uses an API key; reusing this project's
subscription-based CLI authentication has not been verified. Confirm the
authentication route and resource usage before execution. This comparison is an
engineering recommendation, not a successful integration test.
Source: [Harbor agent integrations](https://docs.harborframework.com/core-concepts/agents/pre-integrated-agents).

Version drift matters: the original
[SkillsBench paper](https://arxiv.org/abs/2602.12670) describes Harbor, while the
current [repository README](https://github.com/benchflow-ai/skillsbench) uses
BenchFlow and native `task.md` packages. Do not combine their commands or label a
custom Harbor run as an official SkillsBench result. The current SkillsBench
README documents Docker as a local alternative to its default cloud sandbox and
API credentials for agent runs.

Inspected upstream commits:

- SkillsBench: `9a1f4dd5f7659f75707435da3ce854b6e48321d1`.
- Harbor: `d10ac31727bc4428cf976e7a8a8e5328c9055928`.
- AWS sample: `13b2277b300d2beafa09bbbe425ca0cc41f34c8d`.

These pin the research snapshot, not installed dependencies. Pin and validate an
actual release before implementing the runner. Framework stars or an aggregate
audit grade would not demonstrate this skill's documentation quality.

## Improvements before another broad run

1. Turn the observed deployment-workflow miss into a public synthetic regression
   case. Accept an evidence-supported resolution or an explicit unresolved
   discrepancy; do not reward silently choosing whichever document is newer.
2. Add runnable, independently scored fixtures for the existing manual scenarios.
   Separate factual preservation, scope compliance, conflict handling and
   downstream reader usefulness from formatting or compression.
3. Keep development fixtures separate from held-out cases. After a skill change,
   rerun both the known regression and unseen variations.
4. Add machine-readable results and derive the README table from those results
   once a runner exists. Retain the eight-run local pilot as a separate historical
   dataset; do not relabel it as Harbor or SkillsBench output.

The skill already says to retain unresolved discrepancies explicitly. One miss
does not establish that more instructions would help. Test compliance on varied
conflicts before making that instruction longer.

## Proposed first public suite

Start with eight synthetic tasks: stale configuration, cross-document conflict,
approval/proposal separation, uncommitted edits, Markdown/anchor preservation,
audit without writes, minimal initialization, and repeated maintenance without
losing history or growing duplicate status notes. Include varied layouts and
realistic constraints, without copying private source documents.

For each task, provide the input snapshot, user request, expected invariants,
reference solution and verifier. Keep grading material and reference answers out
of the agent's view. Validate the verifier first: the reference solution must
pass, and deliberately corrupted artifacts must fail relevant checks. For tasks
requiring edits, unchanged artifacts must fail too; a correct read-only audit
must preserve the input. Accept multiple legitimate document layouts.

Then run both arms against identical snapshots with pinned skill, model, effort,
CLI and runner versions. Start with three attempts per task/arm: 8 × 2 × 3 = 48
agent runs for one model. This is a proposed initial sample, not an executed run
or a claim of statistical power. Rotate arm order, preserve failures/timeouts,
and record cache counters. Extend to another model only after the harness itself
is verified.

Use deterministic checks for exact protected content, changed-file scope,
byte-identical audit results, links and immutable inputs. Semantic questions
such as whether a conflict was actually resolved need a published rubric and
separate review; substring matches are insufficient. Blind semantic reviewers to
the condition when practical. Test whether a fresh reader can answer the same
project questions before and after maintenance, including unknowns.

## Reporting rules

Lead the README with task success and information-preservation results. Show
baseline and skill side by side, with task count, repetitions, model/runner/skill
revisions, run date and a reproducible command. Report failures explicitly.

Show entry-point and whole-corpus size separately. Report runtime distributions,
input/cached/output tokens and observed cost only when it was actually measured.
Do not equate a shorter file, lower wall time or a static audit grade with better
answers. Repeated trials of one task are not independent new tasks; avoid treating
every rubric assertion as a separate sample when quantifying uncertainty.

Maintain three distinct labels: **local private-data pilot**, **public custom
suite**, and **external benchmark result**. Only use the last label after running
that external benchmark under its stated protocol.
