# Public-source handoff pilot

Frozen before model execution. This complements the [weak-documentation study](../quality/README.md): it does not describe upstream documentation as poor or remove it to make a weak baseline.

## Question and design

Does an added project handoff improve supported continuation answers when readers
can access a much larger, externally authored repository? Compare upstream as
supplied, ordinary handoff maintenance, and Context Docs v0.1.1 maintenance.
Keep the skill unchanged. No claim of independent benchmark design or judging.

- Flask 3.1.1 at `7fff56f5172c48b6f3aedf17ee14ef5c2533dfd1`.
- Click 8.2.1 at `fd183b2ced1cb5857784fe7fb22f4982f671f098`.
- Include every tracked UTF-8 text file unchanged; exclude binary assets and
  symlinks, recording every omission and source hash in the manifest. These are
  reading tasks, not runnable replicas. Preserve upstream license notices.
- Two projects × two maintenance arms × one attempt = **four maintainers**.
  One additive initialization pass; upstream files and Git state are immutable.
  Only new Markdown handoff documents may be added, with any suitable layout.
- Two projects × three artifacts × two question variants = **12 fresh readers**,
  each answering six questions: **72 answers and 16 model sessions total**.
- Both maintainers receive identical six topic areas and a competent request to
  check sources, preserve information, distinguish uncertainty and verify links.
  The skill arm additionally receives explicit skill invocation and its package.
  Neither sees the exact questions, expected answers or grading ledger.
- Readers receive the actual complete final artifact, including any maintainer
  mistake. All can inspect the same upstream code, tests and documentation.
  Readers see no skill, earlier conversation, arm labels or scoring key.
- Do not run upstream code/tests or install dependencies during model sessions;
  inspect source. No external search/services. Host/global instructions excluded.

## Frozen questions and scoring

[cases.json](cases.json) contains two natural phrasings of each question, two
required semantic criteria and source paths. The author derived these questions
from upstream material; they are not a separately authored held-out benchmark.
Click's flag question also draws on [upstream issue 2746](https://github.com/pallets/click/issues/2746).
The topics are intentionally supplied to maintainers; this is a focused handoff,
not a test of discovering every important fact in a repository.

Primary outcome: an answer passes only when both required criteria are satisfied,
its cited files support the material claims, and it makes no material false claim
or invented deployment assumption. Equivalent valid solutions count. Omission of
unasked trivia does not fail an answer. Report numerator/denominator by project,
arm and question; retain missing answers and execution failures as failures.
Also report pairs correct in both variants. Variants share a maintained artifact
and are not independent project samples; no significance or equivalence claim.

Secondary document review: assess the 12 required criteria per maintained
handoff as accurate, missing, incorrect or conflicting. A meaningful, specific
pointer to canonical evidence can satisfy an item; a generic documentation link
cannot. Record material additional errors. **Upstream-only has no added handoff,
so this coverage metric is not applicable, not zero knowledge.** All its original
knowledge remains accessible and its reader results are the primary comparator.

Mechanical checks are separate from semantics: upstream byte preservation,
Markdown-only additions, local inline link target existence, answer schema,
existing citation paths, unchanged reader project bytes and Git state. Anchors,
reference-style links and claim support require author review. Review by the
same authoring agent is not blinded or independent. Publish explicit evidence
notes, all answers, added documents and per-item scores; do not publish raw
sessions or credential/service metadata. Source corpora are fetched by pin,
not vendored into the repository.

## Execution and controls

Harbor 0.23.0, Codex CLI 0.158.0-alpha.2, gpt-6-astra, low effort, shared isolated
[configuration](../suite/codex.toml), pinned Node image inherited from the shared
builder. Allow 480 seconds per model session, concurrency three, no retries.
Maintenance order alternates arms across projects; readers use sorted opaque IDs.
Wall time and tokens are secondary diagnostics, not product success criteria.

Before scored runs: validate reference/no-op behavior on both projects and both
stages, plus local controls for source edits, non-Markdown additions, broken
paths, missing answers, invalid citations and reader edits. These controls test
harness mechanics, not whether a semantic judge can reliably grade arbitrary
answers. Confirm the version-sensitive Click flag example from pinned local
source with [probe.py](probe.py) before freezing; model sessions remain read-only
source inspection. Flask's config documentation includes a mistyped per-request
property link; implementation exposes `max_form_memory_size`. Score the actual
property correctly, without requiring the reader to discuss the typo explicitly.

Freeze cases, prompts, criteria and harness in Git before model execution. Build
packages after that commit and retain hashes. Never repair generated documents
before readers see them. Keep failures/timeouts and stop to inspect infrastructure
errors; any later rerun must be separately disclosed, never silently substituted.
Recorded-input audits check unexpected user messages and global AGENTS injection.

## Reproduce

From the repository root, with Docker, Python 3, uv and an existing Codex login:

```sh
python3 evals/public/study.py selftest
python3 evals/public/probe.py
python3 evals/public/study.py build-maint .local/public-maint
python3 evals/public/study.py run .local/public-maint .local/public-jobs --prefix public-maint --mode oracle
python3 evals/public/study.py run .local/public-maint .local/public-jobs --prefix public-maint --mode nop
python3 evals/public/study.py run .local/public-maint .local/public-jobs --prefix public-maint --mode model
python3 evals/public/study.py collect .local/public-maint .local/public-jobs .local/public-maint-export --prefix public-maint
python3 evals/public/study.py build-readers .local/public-readers .local/public-maint-export
python3 evals/public/study.py run .local/public-readers .local/public-jobs --prefix public-read --mode oracle
python3 evals/public/study.py run .local/public-readers .local/public-jobs --prefix public-read --mode nop
python3 evals/public/study.py run .local/public-readers .local/public-jobs --prefix public-read --mode model
python3 evals/public/study.py collect .local/public-readers .local/public-jobs .local/public-read-export --prefix public-read
python3 evals/suite/audit_isolation.py .local/public-jobs .local/public-maint .local/public-maint-audit.json --prefix public-maint
python3 evals/suite/audit_isolation.py .local/public-jobs .local/public-readers .local/public-read-audit.json --prefix public-read
```

The source probe requires Python 3.10+ (upstream Click's requirement); the harness
can run on Python 3.9+. New output directories are required to preserve prior runs.
Prepare explicit author reviews after execution; do not treat mechanical reward
as answer correctness.

## Limits

Only two familiar projects, both in the Pallets/Python ecosystem; model prior
knowledge may help. One maintainer sample per arm/project, two phrasings per
question, no maintenance update sequence, one model/effort and one agent client.
Questions, ordinary prompt, source selection and scoring share author influence.
No model superiority, general equivalence, production reliability or longitudinal
retention claim is justified by this pilot. Larger source size may still produce
a reader ceiling. Retain the earlier private-project miss and completed studies.
