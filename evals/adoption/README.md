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
