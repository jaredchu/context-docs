# Adoption marker regression

Four cases exercise adoption v0.1.1: new adoption on a code-only project, adoption
with existing project rules and an uncommitted blocker, already-adopted guidance
without a marker or recorded date, and an audit-only request on unmarked guidance.
The first two cases run again in fresh sessions on a later supplied date: six
model sessions in total, one attempt per case.

The original adoption v0.1.0 cases/results remain unchanged. `marker.py` reuses
those cases and the core Harbor builder/verifier, with additional marker criteria.
No new benchmark comparison or automatic-selection claim is intended.

```sh
python3 evals/adoption/marker.py .local/adoption-marker-suite
python3 evals/suite/run.py .local/adoption-marker-suite .local/adoption-marker-jobs --mode oracle --prefix marker
python3 evals/suite/run.py .local/adoption-marker-suite .local/adoption-marker-jobs --mode model --prefix marker
```

Use new paths/prefixes for later runs. The builder executes twelve static controls:
a passing reference, rejected incomplete no-op and rejected invalid change for each
case. For audit-only, the invalid change adds a marker, which must fail the
byte-preservation check. Harbor oracle trials check container/grader integration
before scored model runs. Execution settings are those of the [core suite](../suite/README.md).

Review the semantic criteria in `marker.py` separately from mechanical scores.
Confirm exactly one marker with the actual entry point after completed setup,
preservation of the original date on a later-day repeat, and no reinitialization
or duplicate rules when existing instructions already implement the method.
The unrecorded adoption date must remain unknown. Audit-only must report existing
adoption without writing any project file. A missing marker alone must not cause
a non-adopted classification; a marker alone must not imply accurate/current docs.

Compare actual first-pass output with second-pass input/output. The generic
mechanical verifier permits a no-op repeat but does not enforce unchanged output
or interpret marker meaning. These checks therefore also require explicit review.
Cases and reviews are author-created, not blinded or independent. External source
truth, missing-dependency behavior, concurrent maintenance and long-term reliability
remain outside this check.

## Targeted follow-ups

The initial run exposed ambiguous date wording and unnecessary rewriting of
equivalent guidance. Results retain both findings. The date follow-up uses the
same skill candidate with an explicit simulated current date:

```sh
python3 evals/adoption/explicit_dates.py .local/adoption-marker-dates-suite
python3 evals/suite/run.py .local/adoption-marker-dates-suite .local/adoption-marker-dates-jobs --mode oracle --prefix marker-dates
python3 evals/suite/run.py .local/adoption-marker-dates-suite .local/adoption-marker-dates-jobs --mode model --prefix marker-dates
```

After tightening the skill to preserve equivalent guidance when adding a marker,
the targeted rerun covers editable and audit-only unmarked projects:

```sh
python3 - .local/adoption-marker-unmarked-suite <<'PY'
import sys
sys.path.insert(0, 'evals/adoption')
import marker
marker.CASES = [c for c in marker.CASES if c['id'] in {'adopt-unmarked', 'audit-only'}]
marker.main()
PY
python3 evals/suite/run.py .local/adoption-marker-unmarked-suite .local/adoption-marker-unmarked-jobs --mode oracle --prefix marker-unmarked
python3 evals/suite/run.py .local/adoption-marker-unmarked-suite .local/adoption-marker-unmarked-jobs --mode model --prefix marker-unmarked
```

The selected suite's manifest records two trials/two sessions and six static
controls; the builder's fixed console summary describes the full original suite.
Each build uses current skill files. To reproduce an initial candidate exactly,
use the archived candidate and hashes in the
[results](../results/2026-09-27-adoption-marker/README.md).
