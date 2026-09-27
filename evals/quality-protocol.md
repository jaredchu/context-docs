# Documentation quality evaluation

Status: proposed next experiment, not executed. Direction clarified by the project
owner on September 27, 2026. This protocol replaces speed and concision as the
focus of future comparisons; it does not change earlier criteria or scores.

## Question

Does Context Docs preserve more useful project knowledge and produce more
accurate, consistent documentation that a fresh reader can use correctly?

Measure the quality of the stored record and the decisions it supports. Layout,
word count and editing speed are not proxies for accuracy. An accurate, longer
record can be better than a short record that loses a constraint or its rationale.

## Matched starting conditions

Use several projects, each with these separately reported starting conditions:

| Starting condition | Defect to exercise |
| --- | --- |
| Scattered documentation | Relevant facts are present but dispersed, duplicated or poorly linked |
| Stale and conflicting documentation | Old procedures disagree with current evidence; approval and proposal status are mixed |
| No maintained context | Code/configuration and raw work evidence exist, but no durable context entry or maintained account does |

For each project and starting condition, compare three arms:

1. **Unmaintained:** retain the original files and raw evidence without a
   documentation-maintenance pass.
2. **Ordinary maintenance:** a competent agent receives the same task and evidence
   and updates documentation without the Context Docs skill.
3. **Context Docs:** the same agent/model receives the same task and evidence,
   with the frozen skill as the only treatment difference.

This separates the benefit of doing documentation work from the incremental
benefit of the skill. Do not deliberately weaken the ordinary-maintenance prompt
or require the baseline to use an unhelpful layout. An independently curated
accurate record can serve as a reference control, not a competing agent result.

Keep code, configuration, event evidence, permissions and question scope matched.
Raw work notes remain available to readers in every arm; maintained arms gain
organization and derived context, not privileged facts. Do not supply source
facts only to the skill arm or put reference answers in a maintainer's prompt.
Starting defects must be distinct from legitimate differences in document layout.

Missing documentation and missing evidence are different. If an approval,
production state or rationale is absent from all supplied evidence, no arm can
recover it reliably. Include such questions deliberately, score a justified
unknown as correct, and record the unresolved information gap separately from
retention of available facts. Never reward fabricated content for completeness.

## Maintenance and independent reading

Create an evidence ledger with atomic facts, source locations, authority, dates,
status and critical constraints. Keep the ledger and expected answers outside
both maintainer and reader access. Owner approval and configured/runtime state
must remain separate. An unresolved source conflict is not a defect when the
record identifies the uncertainty accurately and preserves the needed next check.

Run initialization or maintenance in disposable copies. Later rounds deliver the
same new evidence to each arm, including superseded decisions, configuration
changes, resolved and unresolved blockers, and a round with no new information.
The unmaintained arm receives those raw updates too. Preserve each stage so loss
and drift can be traced rather than inferred from the final document length.

Then start fresh, read-only reader sessions. Give all readers the same neutral
instructions, questions, tool access and practical resource limits. Readers see
only their arm's project and common raw evidence, without the maintenance chat,
skill package, condition label or answer key. Ask for answers with source
locations and material uncertainty. Use the same question batch and evidence
cutoff within each matched comparison; readers do not inherit earlier answers.

Questions should require useful project conclusions, for example:

- Which release procedure currently applies, who approved it, and why?
- What is configured, and what is actually known about the running deployment?
- Which blocker remains unresolved, and what is the next action?
- Which proposal remains unapproved despite a newer implementation or note?
- Which constraint must survive the next change, and where is its rationale?

## Primary measures

| Measure | Scoring rule |
| --- | --- |
| Information retention | Fraction of available required facts, constraints, rationale and open work retained accurately in the maintained record; do not give documentation credit merely because a forgotten fact survives in an unlinked raw input |
| Document accuracy | Supported correct material claims versus assessed claims; enumerate invented or unsupported claims separately and report missing required facts so omission cannot inflate the score |
| Document consistency | Contradictory operative claims and superseded instructions left current; explicitly qualified history or genuinely unresolved evidence is not a false contradiction |
| Authority and uncertainty | Approved/proposed/observed/unknown distinctions are correct; invented approval or deployment is a critical failure |
| Reader accuracy | Correct evidence-supported answers over the fixed question set, with source support and appropriate handling of unknowns |
| Reader consistency | Agreement on supported conclusions across fresh sessions and equivalent question wording; report alongside accuracy because consistently wrong answers are not success |
| Durability | Facts lost, decisions distorted and stale claims retained after successive matched updates |

Score meaningful content rather than exact wording, filenames or a mandatory
folder structure. A stable, navigable canonical link may preserve detail without
copying it. Report source-finding failures as well as incorrect answers. Assess
retention across all provided original documents and uncommitted notes, not only
facts repeated in the entry point.

Keep critical failures visible per project and stage: lost unique decisions or
constraints, fabricated approvals, unreported operative contradictions, overwritten
uncommitted work, and edits outside the authorized scope. Do not average them away
inside a composite score. Preserve existing audit-only and link checks as regression
coverage even when they are not the main reader experiment.

## Secondary diagnostics

Retain words, duplicate claims, number of files, maintenance time and tokens to
explain tradeoffs after quality is assessed. No size or speed win compensates
for a critical knowledge failure.

If measuring efficiency, distinguish documentation preparation from subsequent
reading. Compare time to a correct, supported answer on the same questions across
matched weak-documentation and maintained arms. Include preparation plus repeated
reader work when discussing end-to-end effort, declare the number of reuse
sessions, and report failures/timeouts rather than omitting them from timing.
Do not rank maintenance speed against an unmaintained arm that does no preparation,
and do not infer financial savings from cached token counts.

## Freeze and report

Before model execution, freeze the skill, project snapshots, evidence ledger,
question sets, scoring rules, critical-failure definitions, number of projects,
repeats and maintenance rounds. Validate with an accurate reference and corrupted
controls that lose a fact, invent approval or retain a known contradiction. A
confidently wrong reader must fail; a justified unknown must pass.

Prefer independently contributed cases and condition-blind reviewers. Label
self-authored or self-reviewed evaluations honestly. Use the same isolated agent
configuration in all arms, audit injected inputs, rotate execution order and retain
failed runs. Hold automatic skill selection and normal global-instruction setups
as separate questions rather than silently mixing them into this comparison.

Report results per starting condition and project, then aggregate with explicit
weighting. Repeats and individual questions do not create independent projects.
Lead the README with retained knowledge, document accuracy/consistency and reader
outcomes, showing the untreated and ordinary-maintenance baselines. Put time and
size in supporting tables. Publish reference evidence and scored examples after
execution, including failures, without exposing private projects or raw login data.

The earlier [48-trial suite](../docs/evaluation-2026-09-27.md) and
[concision comparison](../docs/evaluation-2026-09-27-concise.md) remain maintenance
regressions. Neither already establishes the reader benefits defined here.
