# Quality and fresh-reader study

Status: completed September 27, 2026; see the [results](../../docs/evaluation-2026-09-27-quality.md).
The execution plan below was frozen in `64e059d`; completion links and table
presentation were updated afterward without changing scores. This implements the
[quality-first protocol](../quality-protocol.md). Existing skill v0.1.1 remains
unchanged throughout. No prompt tuning or favorable replacement runs.

## Design fixed before execution

Two new synthetic projects, Kestrel and Oriole, each have three starting conditions:
scattered notes, conflicting current guidance, and no maintained context. Each
condition has the same underlying raw evidence, configuration and uncommitted
notes. Initial documentation defects vary; substantive source facts do not.
These are author-created fixtures, not independently contributed holdouts.

For each of the six scenarios:

- **Unmaintained:** preserve initial documentation and apply only the same raw
  evidence/configuration updates. No agent maintenance call is needed.
- **Ordinary maintenance:** one three-stage trial using a competent common request.
- **Context Docs:** the same trial with explicit invocation of v0.1.1.

Stages are initial maintenance, a new evidence/configuration update, and a final
no-change review. This gives **12 maintenance trials / 36 agent sessions**, with
one maintenance sample per scenario/arm. Each of the **18 final snapshots** then
gets two fresh readers answering equivalent question batches: **36 reader
sessions / 216 answers**. There are six questions per world, covering nine
predeclared evidence-ledger items. Two question wordings test repeated reading of
the same artifact; they are not two independent maintenance attempts.

Harbor 0.23.0, Codex CLI 0.158.0-alpha.2, gpt-6-astra low effort, three concurrent
trials, fresh containers, no automatic retries. Ordinary/skill submitted order
alternates by scenario. Reader submission order is sorted by an opaque hash.
Keep the same committed isolated Codex configuration as earlier studies. Allow
240 seconds per agent session; this is an execution bound, not a speed objective.
Both readers can inspect all project files and common raw evidence. No answer key,
maintenance history, treatment label or skill package is supplied to readers.
All output artifacts are handed off unchanged, even if a maintenance agent fails.

Only final artifacts get reader tests in this first study. Documentation is
reviewed at all three stages. Two projects and one maintenance sample per arm
provide limited generalization; perfect reader scores would indicate a ceiling,
not justify claiming a skill advantage or making the baseline artificially worse.

## Frozen review rules

Mechanical maintenance checks cover actual pre-step inputs, file retention,
non-document scope, links and Git state. Reader checks cover byte-identical
projects, six nonempty structured answers and existing citation paths. Passing
these checks alone is not a semantic success. Raw text evidence stays immutable
for both maintenance arms; a source mutation is a failure, not a repaired input.

Manually review every stage against the nine evidence-ledger items using:

- `correct`: the maintained Markdown contains an accurate account or a specific,
  meaningfully labeled link to the authoritative detail; material status,
  rationale and constraints in that item survive.
- `missing`: the item is absent from the maintained record. Raw-file survival or a
  bare directory/general evidence index does not earn documentation credit.
- `incorrect`: the record makes a materially false or unsupported claim.
- `conflicting`: incompatible operative claims remain without adequate specific
  qualification at their source. Qualified history and explicitly unresolved
  conflicting evidence are valid, not contradictions.

Read all resulting Markdown, not only the entry point. Record sources and reasons
per item or for a clearly explained group. Scan other material claims for invented
facts, lost unique operational detail or unauthorized status transitions, and
record findings outside the fixed ledger as well. Direct links can preserve detail;
an attractive layout or particular filename earns no credit.

Primary document measures:

1. **Required knowledge coverage:** correct ledger items / nine, including material
   rationale and status. Report starting-condition and project breakdowns.
2. **Target-claim accuracy:** correct / (correct + incorrect + conflicting);
   show missing items alongside it. With no assessed target claims, report null,
   not perfect accuracy. This is not an exhaustive count of every factual sentence.
3. **Operative conflicts and critical errors:** enumerate conflicting items,
   unsupported material claims, invented approvals/deployment/authority and lost
   unique constraints. Missing initial documentation is a coverage gap, not an
   invented claim. Loss of a previously captured critical fact is a regression.
4. **Durability:** track item status through updates, counting loss only against
   the stage-appropriate truth. A properly superseded value is not lost knowledge.

For each reader question record two independent Booleans: `correct` and
`supported`. Correctness requires all material requested conclusions, authority,
rationale and uncertainty to match the frozen evidence ledger. Support requires
citations whose actual contents or explicit source chain support those conclusions;
existing paths alone are insufficient. A justified unknown is correct. A fabricated
owner/approval/runtime claim is a critical error. Record specific reasoning and any
critical error per answer; complete success needs both checks and mechanical scope.

**Reader accuracy** is fully correct/supported answers over the fixed question set.
**Consistent correct answers** counts matched questions passing in both fresh reader
sessions. Do not call two equally wrong answers a quality success. Inspect failures
for actual disagreement and publish examples. Report raw counts and per-scenario
results, not significance tests treating 216 answers as independent projects.

Group summaries weight the two projects and three conditions equally; the balanced
question/ledger denominators permit showing counts too. Report untreated document
quality at all stages for matched comparisons. No automatic skill adoption or
quality threshold is inferred from time/size. Resource usage stays in supporting
artifacts; there is no ranking by elapsed time.

The authoring assistant will review condition-hidden packets and inspect traces.
It can still infer treatments or see labels in diagnostics; this is not independent
or fully blinded review. Do not describe it as an external benchmark score.

## Controls and reproduction

Use reference and no-op controls before model phases. Local schema/scope controls
must reject missing answers, unauthorized reader writes and broken links. Manually
review semantic controls that omit a fact, retain a contradiction, invent approval,
answer confidently from a staging receipt, and correctly preserve an unknown.
These controls validate the scoring distinctions, not an independent semantic judge.

Requires Docker, Python 3.9+, uv and an existing Codex login, as described in the
[shared suite](../suite/README.md). Use unused paths/prefixes; raw logs stay local.

```sh
python3 evals/quality/study.py selftest
python3 evals/quality/study.py build-maint .local/quality-maint
python3 evals/quality/study.py run .local/quality-maint .local/harbor-jobs --prefix quality-maint --mode oracle
python3 evals/quality/study.py run .local/quality-maint .local/harbor-jobs --prefix quality-maint --mode nop
python3 evals/quality/study.py run .local/quality-maint .local/harbor-jobs --prefix quality-maint --mode model
python3 evals/quality/study.py collect .local/quality-maint .local/harbor-jobs .local/quality-maint-export --prefix quality-maint
python3 evals/quality/study.py build-readers .local/quality-readers .local/quality-maint-export
python3 evals/quality/study.py run .local/quality-readers .local/harbor-jobs --prefix quality-read --mode oracle
python3 evals/quality/study.py run .local/quality-readers .local/harbor-jobs --prefix quality-read --mode nop
python3 evals/quality/study.py run .local/quality-readers .local/harbor-jobs --prefix quality-read --mode model
python3 evals/quality/study.py collect .local/quality-readers .local/harbor-jobs .local/quality-reader-export --prefix quality-read
```

Both manifests capture frozen source hashes. `snapshots.json` records all 54 stage
artifacts, including untreated inputs. Reader package metadata maps opaque IDs to
snapshot hashes and question variants; those labels are outside the images.
Publication must exclude raw sessions, credentials and private service metadata.
Retain all scored failures and describe infrastructure exceptions explicitly.
