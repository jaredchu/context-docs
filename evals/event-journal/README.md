# Event journal mechanical evaluation

This evaluation follows the [frozen protocol](protocol.md): expanded failure
controls, a synthetic three-stage history replay and bounded local latency probes.
It makes no model calls and does not complete the real-session usability trial.

Run from the repository root with Python 3.9+ and Git:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 evals/event-journal/evaluate.py \
  --work .local/journal-eval-new \
  --output .local/journal-results-new
```

Both directories must be new. The runner only commits inside its newly created
synthetic repository; it disables hooks/signing and performs no network operation.
It records inputs, command outputs, snapshots, revisions, latency samples and
provenance hashes. It does not automatically grade the correctness of prose claims.

The [scenario](scenario.json) contains fictional approvals and check outcomes.
Actual executed operations are journal CLI calls and Git snapshot operations.
Authored source-route reviews are retained separately from automatic assertions.

The [September 28 result](../results/2026-09-28-event-journal/README.md) preserves
two pre-fix failures, a small decoding repair, 25 passing tests, replay artifacts
and local timings. Continued optional use is recommended; real-work usefulness
and agent reader benefits remain unestablished.

## Native history comparison

The [separate native protocol](native/protocol.md) covers Claude and Codex, ordinary
Markdown and two logging formats, with no-Git and sparse-commit fixtures.
See the [runner and limitations](native/README.md). It does not rescore this
earlier mechanical/synthetic study.

## Opt-in package integration

The [native lifecycle protocol and runner](integration/README.md) test project-local
upgrades, direct CLI use and sequential events with the full candidate skills.
These runs are separate from the bridge comparison and retain its limitations.
