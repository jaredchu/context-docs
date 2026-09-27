# Public context-maintenance suite

Eight synthetic tasks compare ordinary instructions with the unchanged Context
Docs skill. These are custom tasks run by **Harbor 0.23.0**, not a SkillsBench
leaderboard submission or an external benchmark score.

## Reproduce

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
48 trials and 60 agent invocations. Model caching is not controlled.

Grading criteria and skill stay fixed before scored runs. These fixtures were
authored with knowledge of the skill; they are a public development/regression
suite, **not a genuinely held-out test set**. Three attempts per task do not make
24 independent tasks per arm. Report per-task counts and observed spread, without
claiming statistical superiority. The suite does not yet measure separate-reader
answer accuracy, automatic activation or cross-model generalization.

Docker provides filesystem separation from the user's source projects. No host
project directories are mounted. Network access is available for authentication;
the agent is instructed not to contact services and web search is disabled.
This is a trusted synthetic-task evaluation, not an adversarial isolation test.

Runner references: [Harbor tasks](https://docs.harborframework.com/core-concepts/tasks/overview)
and [Codex skill evaluation guidance](https://developers.openai.com/blog/eval-skills).
