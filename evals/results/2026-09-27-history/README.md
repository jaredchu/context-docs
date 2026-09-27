# Public decision-history evidence

Protocol and scoring freeze: `85936ea`. See the
[report](../../../docs/evaluation-2026-09-27-history.md),
[protocol](../../history/README.md), [source pins](../../history/provenance.json),
[criteria/questions](../../history/cases.json), and
[third-party attribution](../../history/THIRD-PARTY-NOTICES.md).

Artifacts:

- `maintenance-manifest.json` / `reader-manifest.json`: frozen source/skill hashes,
  exact task mappings, execution settings and input provenance.
- `maintenance-trials.json`: all four trajectories, including all 16 actual
  before/after observations and secondary timing/token diagnostics.
- `snapshots.json`: all 24 project artifacts, including the unmaintained arm,
  source bytes and four successive stages. Actual outputs carry forward.
- `reader-trials.json`: all 12 actual reader outputs and mechanical checks.
- `document-reviews.json`: explicit knowledge-item judgments for every snapshot,
  including omissions, unsupported claims and critical/minor findings.
- `reader-reviews.json`: 96 explicit correctness, source-support and critical-error
  judgments; these are author reviews, not an automatic or independent judge.
- `exposure.json`: every Markdown document's model-visible line coverage before
  answer-writing; exposure does not establish comprehension or causal use.
- `maintenance-controls.json` / `reader-controls.json`: all eight reference/no-op
  control trials. Maintenance no-op correctly fails the first three stages and
  passes the final stage, where no edit is required.
- `reader-control-equivalence.json`: 28 files identical between the two reader
  control packages and corresponding scored packages.
- `maintenance-isolation.json` / `reader-isolation.json`: recorded-input audits.
- `trace-review.json`: supplementary manual scope findings from command traces;
  these are separate from the frozen mechanical and semantic scores.
- `summary.json` / [table.md](table.md): derived scores, loss transitions,
  final-pass byte stability and Markdown word counts.

Raw sessions remain local because they may contain service metadata. All project
inputs are public policy snapshots or authored benchmark workspace text. The
original PEP source declarations remain in each snapshot; the project MIT license
does not replace their public-domain/CC0 declarations.

Reproduce the summary and table from these explicit judgments:

```sh
python3 evals/history/report.py evals/results/2026-09-27-history
```

Independent reviewers can change review fields/notes in a copy and regenerate the
scores. Preserve the original judgments when comparing alternate reviews. The
Harbor reward measures mechanics, not semantic correctness or full filesystem
confinement; consult the separate trace findings before claiming scope compliance.
