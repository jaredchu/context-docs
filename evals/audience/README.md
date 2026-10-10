# Audience/destination native pilot

Five independent synthetic cases exercise the core skill's audience/destination
guidance. [Protocol](protocol.md) and [cases](cases.py) define the proposed acceptance
criteria. Preparation and controls do not count as native subject results.

Status: counterpart design and harness review completed; nineteen runner controls,
seven reused guard tests and repository static checks pass. See the
[preflight record](preflight.md). The [October 10 pilot](../results/2026-10-10-audience/README.md)
records the completed five-session run and both semantic assessments.

```sh
python3 -m unittest discover -s evals/audience -p 'test_*.py' -v
python3 evals/audience/run.py build /tmp/context-docs-audience-review
```

After counterpart review, create a fresh final build and commit its exact manifest,
SHA-256 and harness. Keep the full runtime manifest outside subject roots and raw
logs outside the repository; the exact public manifest may retain a neutral temporary root, but must contain
no personal host paths. Preserve its exact bytes and digest. Inspect exports before sharing
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
