# Adoption and repeated-use regression

Two synthetic projects exercise the optional adoption skill: one has only a CSV
conversion script and no documentation; the other already has a custom knowledge
layout, approval rules, decision statuses and an uncommitted blocker. Each receives
an adoption request followed by the same request with no new evidence, in fresh
agent sessions. This is four invocations, not a comparative accuracy benchmark.

The existing Harbor runner and verifier are reused. `build.py` supplies the cases,
reference outputs, semantic criteria and both sibling skill packages. Only those
packages and project inputs are available during model execution. Instructions
explicitly load the adoption skill; automatic selection is not tested.

## Reproduce

For the exact published v0.1.0 run, use commit `d0febcf`. Current builds use the
current installed-source package; historical results retain their frozen hashes.

Requires the same Docker, uv and subscription-login setup as the
[core suite](../suite/README.md). Choose fresh output directories for each run.

```sh
python3 evals/adoption/build.py .local/adoption-suite
python3 evals/suite/run.py .local/adoption-suite .local/adoption-jobs --mode oracle --prefix adoption
python3 evals/suite/run.py .local/adoption-suite .local/adoption-jobs --mode model --prefix adoption
```

The builder verifies a passing reference, a rejected no-op first pass, an accepted
no-change repeat, and a rejected broken link for each case before execution. Harbor
oracle runs separately check the generated container/grader integration. Inspect
control results before running the model. The source/skill hashes and controls are
saved beside the generated suite; original cases remain in `build.py`.

Model runs retain the core suite's fixed model, reasoning level, CLI version,
isolation configuration and no-retry policy. Raw jobs remain ignored and local.
Do not publish authentication files or raw environment dumps.

## Review

Mechanical checks cover file retention, preserved literals, immutable code, links,
allowed document edits and Git state. Separately review the criteria in `build.py`
against actual outputs. In particular:

- New context must reflect the script without inventing product decisions.
- Existing layout, approval rules, decision distinctions and the uncommitted
  blocker must remain useful and intact.
- AGENTS.md must establish ongoing maintenance without a duplicate skill install.
- The second pass must leave actual first-pass project bytes unchanged. Compare
  its captured input and output; the generic verifier permits no-ops but does
  not require them, so a mechanical pass alone cannot establish this result.

Report every trial, including failures. These are small author-created development
cases with author review, not independent or held-out validation. No comparison
arm, downstream reader trial, audit-only adoption test, missing-dependency behavior,
or cross-client compatibility is established by these two cases.

Completed results: [September 27 adoption and repeat checks](../results/2026-09-27-adoption/README.md).

Marker behavior has a separate [v0.1.1 regression](marker.md), including already-adopted but unmarked projects and audit-only requests.

## Instruction-file routing (v0.1.3)

A maintenance rule only takes effect in the instruction file the client loads.
[instructions.py](instructions.py) adds two cases on that boundary: a project whose
instructions live in `CLAUDE.md` with no loaded `AGENTS.md`, and a project holding
both files where only one is loaded and guidance must not be duplicated. The
fixtures state which file is in effect in the request; detecting a client's loading
rules is outside these cases.

```sh
python3 evals/adoption/instructions.py .local/adoption-instructions-suite
python3 evals/suite/run.py .local/adoption-instructions-suite .local/adoption-instructions-jobs --mode oracle --prefix instructions
python3 evals/suite/run.py .local/adoption-instructions-suite .local/adoption-instructions-jobs --mode model --prefix instructions
```

The builder runs ten static controls: a passing reference, rejected unchanged first
pass, accepted no-change repeat, rejected broken link and rejected removed marker
for each case, with the last asserted to fail on the marker preservation token
rather than incidentally. These controls establish no model behavior.

The [September 28 v0.1.3 merge review](../results/2026-09-28-adoption-v013/README.md)
ran these cases with explicit dates, plus the older marker regressions: eight of
nine sessions met frozen acceptance. The split-file case routed correctly but
failed immutable-file and external-link checks; the report preserves that failure
and its fixture limitations. Before model execution, routing requests were made
client-neutral and the CLAUDE-only condition was repeated in the fresh repeat
session, removing inherited instructions to write an unloaded `AGENTS.md`.

Review placement semantically: the rule must be in the loaded file or reachable from
it through that file's own reference or import mechanism, both original instruction
files must keep their content, and the rule and marker must not be copied into both.
The mechanical verifier cannot tell a loaded file from an unloaded one.

Current routing builds state every immutable-file constraint in each request and
declare the supplied installed-skill files and hashes for link validation. Those
installed paths are checked consistently in links, prose and code spans; they are
not considered missing merely because they live outside the project snapshot.
Both cases now include a next-day repeat with explicit simulated dates (four model
sessions total). These fixture changes follow the September 28 failure; they do
not change its recorded outcome or alter the installable skill.

The [separately frozen follow-up](../results/2026-09-28-adoption-v013-followup/README.md)
passed all four sessions, including both unchanged next-day repeats. Nine verifier
regression tests cover valid, missing, changed and undeclared installed references
without weakening protected-file or project-link checks. Native Claude Code
loading remains outside these Codex-executed cases.
