# Concision experiment

This compares the published v0.1.0 skill with a shorter entry point, subsequently
adopted as experimental v0.1.1. See the [completed results](../../docs/evaluation-2026-09-27-concise.md). It is separate
from the earlier ordinary-instructions versus skill comparison. Read the
[frozen plan](plan.md) before interpreting results. Both arms use the same
v0.1.0 references, templates, UI metadata and task prompt.

The `original-SKILL.md` and `candidate-SKILL.md` files are frozen package overlays;
their relative resource links resolve after `study.py build` assembles complete
skill folders. They are not standalone installable skills. The builder retrieves
supporting files from the local `v0.1.0` Git tag, so clone with tags available.

Three synthetic projects begin with 572–676 Markdown words. They were authored
after candidate freeze `136bd31`, but by the same assistant; they are new
**development fixtures**, not an independent held-out benchmark. Two attempts
per case/variant give 12 trials and 20 agent sessions. Semantic review remains
by the authoring assistant.

## Reproduce

Requires Docker, Python, `uv`, and an existing Codex login as described in the
[shared suite instructions](../suite/README.md). Use a new destination and prefix
for every experiment; do not overwrite failed runs.

```sh
python3 evals/suite/selftest.py
python3 evals/concise/study.py selftest
python3 evals/concise/study.py build .local/concise-suite
python3 evals/suite/run.py .local/concise-suite .local/harbor-jobs --mode oracle --prefix concise
python3 evals/suite/run.py .local/concise-suite .local/harbor-jobs --mode nop --prefix concise
python3 evals/suite/run.py .local/concise-suite .local/harbor-jobs --mode model --prefix concise
python3 evals/concise/study.py collect .local/harbor-jobs .local/concise-review --prefix concise
python3 evals/suite/audit_isolation.py .local/harbor-jobs .local/concise-suite .local/concise-review/isolation.json --prefix concise
```

Inspect every condition-hidden packet and tool trace, recording a Boolean for
each rubric criterion and a specific reason in `reviews.json`, in the same
[review format](../suite/README.md#export-and-review) as the shared suite. Then:

```sh
python3 evals/concise/study.py report .local/concise-review
```

The report checks completeness and calculates the preregistered adoption gate.
It does not supply semantic grades automatically. Passing supports further use;
it does not establish general superiority or practical significance.

## Input isolation and actual snapshots

Harbor starts a separate Codex home in each container. The runner passes only
its committed configuration and privately injects the login file; it does not
copy the user's global instructions, host configuration or personal skills.
The recorded-message audit checks that each session received only its exact
generated task request and the `/workspace` environment message as user input.
It publishes counts, not raw session logs.

The same default model/CLI instructions and common task constraints remain in
both conditions. In particular, both are explicitly told to preserve layout and
unique information. This may reduce incremental skill benefits. Host preferences
can still influence the authoring assistant's fixtures, skill and review; isolated
execution does not create independent evaluation or test behavior under a user's
usual global instructions.

Immediately before each pass, the harness snapshots actual project files outside
the project directory. The verifier records those Markdown inputs and a hash of
the complete input map. Missing snapshots fail verification. Snapshots are not
hardened against a malicious root agent; this is a trusted-task experiment.
Original non-document constraints and protected information remain separate checks.
