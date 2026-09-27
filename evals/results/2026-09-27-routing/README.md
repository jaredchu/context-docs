# Routing follow-up evidence

The [frozen protocol](../../routing/README.md) defines the comparison and exposure
measurement. See the [report](../../../docs/evaluation-2026-09-27-routing.md).
Freeze commit: `a02cade`. Earlier study data and handoffs were not edited.

- `manifest.json`: input/source hashes, upstream provenance, exact README prefixes,
  orientation targets, opaque task mappings, shared settings and freeze commit.
- `trials.json`: all 12 actual reader outputs, checks and timing/token diagnostics.
- `reviews.json`: 72 explicit per-answer judgments, with notes and any omissions.
- `exposure.json`: pre-answer model-visible exposure of README and target, matched
  line counts, missing-line indices and tool-response hashes, plus source-call text.
  This measures displayed text, not comprehension or a trusted system-call trace.
- `summary.json` and [table.md](table.md): derived per-question and aggregate scores.
  Accuracy and exposure are separate. Readers who skip documents stay in scores.
- `controls.json`: two successful reference and two correctly failing no-op runs.
- `control-equivalence.json`: all 2300 generated task-package files were identical
  between control and scored packages. New pre-freeze decoder/report self-tests
  do not alter the container prompts, inputs or verifier.
- `isolation.json`: recorded-input audit for 12 model sessions.

Handoffs and their prior provenance/reviews remain in the
[public-source evidence](../2026-09-27-public/README.md). Upstream BSD attribution
is preserved in the manifest and [third-party notices](../2026-09-27-public/THIRD-PARTY-NOTICES.txt).
The original source trees are fetched by revision, not vendored. Raw model
sessions remain local because they may contain service metadata. The exposure
decoder can be rerun against those sessions; published line/hash evidence is not
a cryptographic proof of what a model understood.

Reproduce the table from the repository root:

```sh
python3 - <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, 'evals/routing')
from report import summarize
root = Path('evals/results/2026-09-27-routing')
load = lambda name: json.loads((root / name).read_text())
summary, table = summarize(load('trials.json'), load('reviews.json'), load('exposure.json'))
assert summary == load('summary.json')
assert table == (root / 'table.md').read_text()
print(table)
PY
```

Independent reviewers can inspect the unchanged
[required criteria](../../public/cases.json), answers and citations, replace the
explicit booleans/notes, and regenerate scores. These are author judgments,
not an independent benchmark or hidden automatic semantic judge.
