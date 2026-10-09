# Public-source adoption pilot

Four completed native Claude Opus 5.5 sessions used pinned `tidwall/match` Go source
with two synthetic overlays. See the [protocol](protocol.md). This is a bounded
adoption regression, with no ordinary-maintenance comparison or reader phase.
The [completed report](../results/2026-10-09-public-adoption/README.md) retains the
frozen marker-format failure and separate semantic reviewer assessments.

The [runner](run.py) reuses the native smoke execution, stream parser and six-tool
guard. It never executes upstream source or workflows. Source and license bytes
are preserved; only the new setup permits an appended README context or navigation
section. The legacy
marker pass preserves its existing dollar-prefixed guidance exactly.

Run mechanical controls without credentials or network:

```sh
python3 -m unittest discover -s evals/public-adoption -p 'test_*.py'
python3 -m unittest discover -s evals/claude-code -p 'test_guard.py'
python3 evals/checks/static_checks.py
```

Build into a fresh absolute directory outside this repository. This fetches the
pinned source from GitHub, checks blob identities, copies baseline skill bytes,
and freezes prompts, overlays, rubrics, source references and control hashes:

```sh
python3 evals/public-adoption/run.py build /tmp/context-docs-public-adoption
```

Review the generated `protocol.json` and `protocol.sha256`, then retain a committed
copy before execution. Control files and answer keys live outside subject project
roots. Do not place them in the subject fixtures. Run only after the counterpart
harness review and freeze, passing the reviewed hash literally:

```sh
python3 evals/public-adoption/run.py run /tmp/context-docs-public-adoption --frozen-sha256 REVIEWED_HASH
```

Raw logs and hook events stay local. No retry or prompt tuning belongs to the four
sessions; failed inputs/outputs are preserved. Content failures do not erase a
trajectory, while execution-boundary, model, completion or drift failures stop the
remaining sessions. Byte checks and loading/invocation evidence remain separate
from semantic review. Effort is requested, not independently observed. Responding
model evidence comes only from assistant messages; usage models, which may include
auxiliaries, and the initialization label are recorded separately. Run final claim
review against the frozen rubrics and exact
source references; do not label a mechanical pass as correctness.

Export reviewable summaries to a new file after execution:

```sh
python3 evals/public-adoption/run.py export /tmp/context-docs-public-adoption /tmp/public-adoption-results.json
```

The export omits raw streams, tool arguments and host instruction paths, and
normalizes known local path prefixes. Inspect final responses and artifacts before
publication; the exporter does not decide whether arbitrary model prose is private.
No publication is part of this runner.
