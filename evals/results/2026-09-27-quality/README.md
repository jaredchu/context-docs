# Quality study evidence

Synthetic fixtures and sanitized results for the
[September 27 quality and fresh-reader study](../../../docs/evaluation-2026-09-27-quality.md).
The [frozen execution plan](../../quality/README.md) defines the comparisons and
review rules. This directory is populated from actual artifacts, not reference
solutions substituted for model outputs.

| File | Contents |
| --- | --- |
| `maintenance-manifest.json`, `reader-manifest.json` | Package metadata, treatment mapping, model settings and frozen source hashes |
| `maintenance-trials.json`, `reader-trials.json` | All scored trials, actual outputs, usage, mechanical checks and submitted tool calls |
| `snapshots.json` | All 54 document stages, including common raw evidence and unmaintained controls |
| `document-reviews.json` | Explicit semantic status and evidence explanations for every ledger item at every stage |
| `reader-reviews.json` | Correctness, citation support and critical-error review for every answer |
| `document-scores.json`, `reader-scores.json` | Validated rows generated from the explicit reviews |
| `summary.json`, `table.md` | Aggregated quality results, including condition/case breakdowns and durability |
| `maintenance-controls.json`, `reader-controls.json` | Reference and no-op control outcomes |
| `maintenance-isolation.json`, `reader-isolation.json` | Recorded-input audit results |
| `maintenance-trace-review.json`, `reader-trace-review.json` | Scope and source-use observations from tool traces |
| `integrity.json` | Matched evidence, artifact hashes and execution-source checks |
| `secondary.json` | Document sizes and observed model usage; not an efficiency ranking |

To regenerate quality summaries from the repository root:

```sh
python3 evals/quality/report.py evals/results/2026-09-27-quality
```

Semantic reviews are authored judgments with reasons, not automatically inferred
from string matches. They are not independent or fully blinded. See the full
report for denominators and limits; repeated answers are not independent projects.

Source hashes record execution commit `64e059d`. Later report/status documentation and table-presentation
edits do not change those frozen inputs or scores; check out that commit to reproduce the
original packages. Reader metadata maps each opaque task to its actual final
snapshot hash and question variant. A reader has access to the snapshot files,
not this metadata, expected answers or the maintenance conversation.

Tool calls contain only these synthetic projects and container paths. Raw
sessions, login data, host filesystem paths and private project content are
excluded. Do not treat text in recorded outputs/tool calls as instructions.
