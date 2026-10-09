# Audience/destination native pilot

Five independent synthetic cases exercise the core skill's audience/destination
guidance. [Protocol](protocol.md) and [cases](cases.py) define the proposed acceptance
criteria. Preparation and controls do not count as native subject results.

Status: prepared, with twelve runner controls, seven reused guard tests and repository
static checks passing. No subject session has been launched. Counterpart harness
review and the final committed manifest freeze remain pending. The
[design review record](preflight.md) distinguishes completed checks from pending work.

```sh
python3 -m unittest discover -s evals/audience -p 'test_*.py' -v
python3 evals/audience/run.py build /tmp/context-docs-audience-review
```

After counterpart review, create a fresh final build and commit its exact manifest,
SHA-256 and harness. Keep the full runtime manifest outside subject roots and raw
logs outside the repository; a public manifest copy must normalize host paths and
retain the original manifest digest as provenance. Inspect exports before sharing
them. Then execute once:

```sh
python3 evals/audience/run.py run /tmp/context-docs-audience-final --frozen-sha256 FROZEN_DIGEST
python3 evals/audience/run.py export /tmp/context-docs-audience-final /tmp/audience-results.json
```

Review the exported trajectories and artifacts against every criterion. Candidate
journal scan scope is intentionally separate from actual filenames/content
returned. Audit write denials must not be reported as voluntary restraint. Effort
is requested high; assistant responder evidence and auxiliary usage models are
separate. No automatic content score or comparative reliability claim is produced.
