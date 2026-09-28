# Public context-maintenance suite

Eight synthetic tasks compare ordinary instructions with Context Docs. The
published 48-trial study used the unchanged v0.1.0 skill; current builds use the
package in `skills/context-docs`. These are custom tasks run by **Harbor 0.23.0**, not a SkillsBench
leaderboard submission or an external benchmark score.

## Reproduce

For the exact published 48-trial setup, use execution commit `f308aa1` (or
`f51dabf` for its completed reporting tools). Current main includes the input
snapshot fix below. The [separate concision experiment](../concise/README.md)
uses that fix with larger fixtures and two skill variants.

Requires Python 3.9+, uv, Docker, and an existing Codex login in `auth.json`.
Harbor's adapter uploads that login into disposable local containers and removes
its copy after execution. Do not publish raw Harbor jobs, authentication files or
environment dumps. The runner does not send results to Harbor Hub.

```sh
python3 evals/suite/selftest.py
python3 evals/suite/build.py .local/harbor-suite-v1
python3 evals/suite/run.py .local/harbor-suite-v1 .local/harbor-jobs --mode oracle --prefix validation
python3 evals/suite/run.py .local/harbor-suite-v1 .local/harbor-jobs --mode nop --prefix validation
python3 evals/suite/run.py .local/harbor-suite-v1 .local/harbor-jobs --mode model --prefix evaluation
```

Use a new destination/prefix for a new experiment. Existing jobs are never
overwritten and failed trials are not silently retried. `CODEX_AUTH_JSON_PATH`
can identify a different existing login file. The model runner uses the existing
subscription login; it removes API-key overrides from its child environment.

The package builder records hashes of the skill and suite source. Model and
effort are fixed at `gpt-6-astra`, low; the container CLI is pinned to
`0.158.0-alpha.2`. This differs from the earlier private pilot's CLI and execution
environment, so compare conditions within this suite, not speed across studies.

## Tasks and scoring

| Task | Main semantic question |
| --- | --- |
| stale-config | Does configured state remain distinct from runtime? |
| workflow-conflict | Is the specific superseded workflow qualified at its source? |
| decision-status | Does newer proposal text remain unapproved? |
| uncommitted-work | Are unique edits, decisions and open work preserved? |
| links-and-fences | Does consolidation preserve commands and navigation? |
| audit-only | Are contradictions reported without changing project bytes? |
| initialize | Is minimal context useful, supported and discoverable? |
| repeated-maintenance | Does context survive successive changes and a no-change pass? |

`cases.py` publishes inputs, reference solutions and per-step semantic rubrics.
The builder puts only project inputs in the Docker image; tests and solutions are
injected by Harbor after the agent phase. The skill condition additionally gets
the unchanged package at `/opt/context-docs` and an explicit instruction to read
it. This tests explicit use, not automatic activation. Both arms share all other
task instructions and configuration. Test and solution directories are removed
before each subsequent maintenance step.

`verify.py` checks file retention, immutable inputs, protected literal commands
and identifiers, local links/anchors, allowed edit scope, and Git commit/staging
state. Audit reports go to `/output/audit.md`; the project itself stays unchanged.
These mechanical checks do **not** establish semantic correctness. Inline links
and ordinary heading anchors are supported; this is not a complete Markdown
parser. Whole-input-file retention is intentional for these fixtures, not a
universal restriction on documentation maintenance.

Fixtures that supply installed skills outside the project can declare exact
`external_references` paths and SHA-256 hashes in their verifier specifications.
The verifier checks those files' presence and integrity before using them as
valid link targets, without adding them to project snapshots. References under
declared `external_reference_roots` are checked in links, prose and code spans,
so formatting cannot hide a missing installed file. Undeclared or changed files
still fail, as do broken project links and edits to immutable project files.
This bounded path check does not attempt to parse every Markdown or shell form.
Without those optional fields, existing project-only link checks are unchanged.

Current builds capture actual project files immediately before each agent pass,
after any fixture update. Change and retention checks use that snapshot, including
files created in earlier passes; original immutable constraints remain separate.
The snapshot lives outside the project and is recorded in `observed.json` as
Markdown input plus a full-input hash. Missing snapshots fail verification.
The published 48-trial experiment predates this fix: its later change checks used
reference-stage input and could give partial no-op reward. Its scores have not
been rewritten. Overall accuracy always requires full-trial semantic review;
Harbor's mean mechanical reward is not task accuracy.

Each generated test writes `observed.json` with document contents, checks and
counts. Review every rubric item against these outputs and original evidence.
Record pass/fail, a supporting reason and reviewer identity separately. Overall
task success requires every mechanical and semantic criterion across all steps,
and no execution error. A source identifier merely appearing in text does not
prove its decision was preserved. Contradiction review must reject blanket
disclaimers that leave the conflicting instruction operative.

Reference solutions must pass all checks. Unchanged artifacts must fail tasks
requiring edits; a deliberately broken link or lost input must fail. A no-change
third maintenance pass may legitimately pass without edits. These controls test
the graders, not the skill, and are excluded from agent results.

## Experimental boundaries

Three blocks each run eight tasks in both conditions, with two concurrent trials.
Submitted condition order alternates by task and block; concurrency means actual
completion order varies. Each trial uses a fresh container. The repeated task
has three fresh agent sessions over the same evolving files, with configuration
updates injected between passes; other tasks have one session. Thus there are
48 trials and 60 agent invocations. Model caching is not controlled. Authentication
probes and oracle/no-op control runs are separate and excluded from these counts.

Grading criteria and skill stay fixed before scored runs. These fixtures were
authored with knowledge of the skill; they are a public development/regression
suite, **not a genuinely held-out test set**. Three attempts per task do not make
24 independent tasks per arm. Report per-task counts and observed spread, without
claiming statistical superiority. The suite does not yet measure separate-reader
answer accuracy, automatic activation or cross-model generalization.

Docker provides filesystem separation from the user's source projects. No host
source directories are mounted. Network access is available for authentication;
the agent is instructed not to contact services and web search is disabled.
This is a trusted synthetic-task evaluation, not an adversarial isolation test.
Snapshots are not hardened against deliberate modification by a root agent.

Host global instructions and personal configuration are not copied to the test
containers. The shared committed configuration disables project-instruction
injection and host skill discovery. A recorded-input audit of all 60 published
sessions found exactly the expected task/environment user messages and no
injected `AGENTS.md` messages. See the [count-only audit](../results/2026-09-27-harbor/isolation.json).
This does not remove authoring/review bias or measure the skill alongside a user's
usual global instructions. Both conditions also share explicit preservation rules.

## Export and review

```sh
python3 evals/suite/collect.py .local/harbor-jobs .local/review-export --prefix evaluation
```

The collector exports allowlisted metrics, synthetic documents and agent tool
calls into `trials.json`; it omits raw logs, system prompts and authentication.
Inspect exports before publication. `review-packets.json` omits condition labels
and orders packets by opaque ID to support semantic review. This does not by
itself make the authoring assistant an independent or fully blinded reviewer.

Write `reviews.json` with reviewer/method metadata and a `steps` object keyed by
each `review_id`. Each entry needs `criteria` (three Boolean rubric outcomes) and
`reason` (specific supporting evidence or a failure explanation). Inspect tool
calls as well as documents for scope and Git-history requirements. Then run:

```sh
python3 evals/suite/report.py .local/review-export
```

The report requires all 48 trials and their reviews, and derives `summary.json`
and `table.md`. Add `--readme README.md` to replace its existing evaluation-table
marker block from those same scores. Incomplete or errored experiments must remain explicitly labeled;
do not replace them with favorable retries. Runtime is agent-phase time, excluding
container build/setup. Repeated-task time and token usage sum all three sessions.
Harbor's estimated dollar figures are not treated as observed subscription cost.
Word counts cover project Markdown only; the audit report outside the project is
excluded. Report lengths remain available in the published audit text.

Runner references: [Harbor tasks](https://docs.harborframework.com/core-concepts/tasks/overview)
and [Codex skill evaluation guidance](https://developers.openai.com/blog/eval-skills).
