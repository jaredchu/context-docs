# Concise skill comparison

Run September 27, 2026. **Adopted as experimental skill v0.1.1.** The shorter
candidate met the [acceptance rule frozen before fixture authoring](../evals/concise/plan.md):
all preservation checks passed, median document growth fell in two of three tasks,
no task exceeded the growth guard, and final no-change passes left Markdown intact.
This supports a concision improvement on these cases, not general superiority.

The entry point shrinks from 645 to 417 whitespace-separated words, including
frontmatter. Supporting references, templates and UI metadata are unchanged.
The candidate consolidates the workflow and discourages repeated generic caveats
and inventories of undocumented features during initialization.

## Results

Three new synthetic projects × two skill variants × two attempts = **12 trials**.
Repeated maintenance has three stages, giving **20 fresh agent sessions**.
Both variants passed 6/6 complete trials, including mechanical checks and all
60 step-level semantic judgments across both variants.

| Task | Initial Markdown words | Original median growth (range) | Candidate median growth (range) | Complete passes, original / candidate |
| --- | ---: | ---: | ---: | ---: |
| Dispersed release guidance | 676 | +322.5 (+274–371) | +184 (+165–203) | 2/2 / 2/2 |
| Initialize from mature docs | 581 | +211 (+133–289) | +181 (+177–185) | 2/2 / 2/2 |
| Three maintenance passes | 572 | 0 (0–0) | 0 (0–0) | 2/2 / 2/2 |

Word growth is final minus initial Markdown across the project, not just the entry
point. Half-word medians are averages of two integer observations. Initialization
was **not consistently shorter**: the candidate added 185 words against 133 in
attempt one, and 177 against 289 in attempt two. A README section and a linked
context file were both accepted when useful and supported; filename choice was
not a scoring criterion. No general compression percentage is claimed.

Release trials qualified the old Git/mandatory-CI instructions in the design
itself, selected the owner-approved manual workflow, and preserved unresolved
integration evidence, receipt-storage questions, rollback constraints and restore
work. All four maintenance trials changed only the polling value, retained the
uncommitted sparse-file note, decisions and YAML, and made no final-pass edits.

| Resource metric | Original v0.1.0 | Concise candidate |
| --- | ---: | ---: |
| Median agent seconds per trial | 65.4 | 79.8 |
| Agent seconds range | 44.4–133.3 | 50.6–142.2 |
| Total agent seconds | 476.8 | 549.3 |
| Total input tokens | 737,604 | 727,237 |
| Cached input tokens | 635,520 | 645,120 |
| Uncached input tokens | 102,084 | 82,117 |
| Output tokens | 11,115 | 12,106 |

The candidate was slower and emitted more total output tokens despite smaller
resulting documentation. Time covers the agent phase, including recovered tool
errors, but excludes container build/setup; three-stage trials sum all sessions.
Cache behavior and server latency were uncontrolled. Token counts are observed
usage, not subscription cost or a prediction of savings.

## Method and controls

- Candidate and acceptance rule frozen in `136bd31`; fixtures and execution
  harness frozen in `1e4caf9`. No scored trial was retried, replaced or discarded.
  All completed without Harbor execution exceptions.
- Harbor 0.23.0, Codex CLI 0.158.0-alpha.2, `gpt-6-astra`, low effort. Two sequential
  blocks, two concurrent trials per block; submitted variant order alternated.
  Each trial used a fresh container. Conditions differed only in `SKILL.md` bytes;
  project inputs, user request, references and graders were identical.
- Three reference controls passed and three no-op controls failed complete trials.
  The repeated no-op control failed both required edits and passed only the final
  no-change mechanical stage. Local controls passed 46 existing-harness assertions
  and 14 new-fixture assertions, including broken links and actual-input behavior.
- The fixed verifier captures actual files before each pass, after configuration
  updates. All eight later-stage Markdown inputs match the preceding actual
  outputs. Original immutable/protected checks remain separate. This fixes the
  reference-input limitation in the older study without silently regrading it.
- The authoring assistant manually reviewed all 20 step outputs against three
  frozen semantic criteria each and inspected tool traces. Review packets omit
  variant labels, but run summaries expose them: **review is neither independent
  nor fully blinded**. Reasons accompany every score.

## Global instructions and limits

The [recorded-input audit](../evals/results/2026-09-27-concise/isolation.json)
found 20 expected task requests and 20 container environment messages, with zero
unexpected user messages or injected `AGENTS.md` messages. The same audit passed
for the older study's 60 sessions. Harbor used a separate Codex home and the
committed test configuration; only the login file was privately copied from the
host. The user's global context-maintenance instructions were not test inputs,
so host instruction changes do not alter these packaged conditions.

Isolation does not eliminate influence on the authoring assistant's skill design,
fixtures or scoring. Both arms also receive explicit scope/preservation rules and
the same default model/CLI instructions. This experiment compares two explicitly
invoked skills; it does not measure automatic activation, ordinary instructions
without a skill, or behavior alongside a user's normal global instructions.

The projects were authored after candidate freeze but by the same assistant.
They are larger development fixtures, **not independently held-out repositories**.
Two repeats do not create additional tasks. Three passes are not evidence of
long-term maintenance quality. Snapshot files are not hardened against malicious
root access; tasks are trusted. Original private projects were not used or edited.

The next useful evaluation is a fresh reader answering project questions after
maintenance, with independent or externally contributed fixtures. Keep the older
[48-trial baseline](evaluation-2026-09-27.md) and [private pilot miss](evaluation-2026-09-26.md)
visible; these new results do not erase either result.

## Reproduce and inspect

- [Commands, packaging and boundaries](../evals/concise/README.md)
- [Frozen plan](../evals/concise/plan.md) and [fixtures/rubrics](../evals/concise/fixtures.py)
- [Trial documents, actual inputs, tool calls and usage](../evals/results/2026-09-27-concise/trials.json)
- [Explicit semantic reviews](../evals/results/2026-09-27-concise/reviews.json)
- [Derived summary and acceptance gate](../evals/results/2026-09-27-concise/summary.json)
- [Control results](../evals/results/2026-09-27-concise/controls.json)
- [Frozen source/package hashes and reporting provenance](../evals/results/2026-09-27-concise/manifest.json)

Raw sessions, system prompts, credentials and private service metadata remain local.
These are custom Harbor tasks, not an external benchmark leaderboard score.
