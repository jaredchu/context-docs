# Public-source pilot evidence

See the [study report](../../../docs/evaluation-2026-09-27-public.md) and
[frozen protocol](../../public/README.md). Cases, prompts, graders and the report
aggregator were frozen in commit `a2442c6` before scored model execution.

- `maintenance.json`: four actual handoffs, scope checks, timing/token diagnostics
  and task checksums. Full upstream snapshots stay local; their combined hashes
  are retained and source files can be fetched at the pins.
- `readers.json`: all 12 reader outputs (72 answers), scope/schema checks and
  diagnostics. No answer was corrected before review or publication.
- `reviews.json`: author review of 48 handoff criteria and 72 reader answers.
  Evidence notes explain each judgment. This is not independent or blinded review.
- `summary.json` and [table.md](table.md): derived counts and individual answer
  pass/fail results. Reproduce them with the code below.
- `maintenance-manifest.json` / `reader-manifest.json`: frozen hashes, upstream
  per-file hashes, omitted binary assets, package mappings and execution settings.
- `controls.json` and control manifests: four passing reference and four failing
  no-op container runs, completed before scored runs. Reader controls use reference
  fixtures; scored readers use actual maintainer artifacts. Control packages were
  built before the freeze commit; relevant prompts/verifiers are unchanged.
- `maintenance-isolation.json` / `reader-isolation.json`: recorded-input audits
  for all 16 model sessions, not semantic scores.
- `reader-discovery.json`: post-hoc inspection of recorded source commands; no
  handoff-content reading was observed in eight maintained-artifact readers.
- `reference-probe.json`: pre-execution pinned Click flag check, also repeated
  after freezing to save its identical output. It is not a model trial.
- `provenance.json`: upstream pins, temporary Git commit IDs cited by the handoffs,
  and added file word counts. The temporary IDs are container snapshot commits,
  not upstream commits: the harness initializes a new repository from source text.
- [THIRD-PARTY-NOTICES.txt](THIRD-PARTY-NOTICES.txt): upstream BSD notices. No
  affiliation or endorsement is implied. Upstream source trees are not vendored.

Readers saw the generated documents unchanged. The root README of either source
repository was not modified to point to additions because the protocol prohibited
all upstream edits; handoff discovery therefore depends on the reader's file search.
Raw model sessions remain local because they can include service metadata. Published
results omit tool transcripts and full upstream copies; hashes, source pins,
questions, answers, handoffs and explicit scoring are sufficient to inspect these
judgments and rerun the study, but are not a tamper-proof audit of the runner.

From the repository root:

```sh
python3 - <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, 'evals/public')
from report import summarize
root = Path('evals/results/2026-09-27-public')
load = lambda name: json.loads((root / name).read_text())
summary, table = summarize(load('maintenance.json'), load('readers.json'), load('reviews.json'))
assert summary == load('summary.json')
assert table == (root / 'table.md').read_text()
print(table)
PY
```

For an independent regrade, use the required criteria in
[cases.json](../../public/cases.json), inspect each answer and cited pinned source,
and replace the explicit review booleans/notes before calling `summarize`.
The maintenance criteria allow specific canonical pointers; the ordinary Click
lazy-file item receives that credit, documented in its review rather than treated
as an explicit standalone explanation. Upstream-only has no added handoff coverage
score; its existing documentation is not treated as missing knowledge.
