# JSONL event journal evaluation — September 28, 2026

Recommendation: continue the optional local pilot. The tested preservation controls
pass after one error-handling repair. The journal offers a structured route to
history, but this evaluation establishes no reader-accuracy advantage or net time
saving over well-maintained Markdown/Git and raw evidence. Keep automatic capture,
cleanup and mandatory skill integration out of scope pending real use.

## Mechanical results

| Check | Initial implementation | Repaired implementation |
| --- | --- | --- |
| Journal unit/integration tests | 23 passed, 2 failed | 25 passed |
| Deeply nested JSON input/history | Uncaught `RecursionError` traceback | Clean failure with diagnostic; no append to invalid history |
| Killed writer with partial tail | Passed | Passed |
| 12 concurrent independent session writers | Passed | Passed |
| Existing per-session lock blocks competing writer | Passed | Passed |
| Synthetic three-stage replay | Not run | 10 events retained; prior session bytes and read-only checks passed |

The two failing tests exercise one defect: JSON decoding can raise `RecursionError`
outside the existing error handler. The repair catches it at decoding and reports
the nesting limit. No schema or skill version changed. Retain
[initial test output](tests-before.txt), [pre-fix source](before-fix.py),
[passing test output](tests-after.txt) and the
[executed repaired source](after-fix.py). The
[test snapshot](tested-tests.py) preserves the 25 controls used in both runs.

The killed-writer test starts a child process, waits until it holds the session
lock and has flushed an incomplete record, then kills it. Append first refuses
the leftover lock. After the test confirms child exit and removes the lock,
append refuses the incomplete record without altering it. Moving the damaged
artifact outside the read directory permits a new session while preserving the
original. This is process interruption testing, not filesystem or power-loss testing.

The prior `fsync` error control also confirms that an error may follow a completed
write. Retry is not deduplicated; inspect history first. Structural validation
accepts an approval claim with a nonexistent evidence reference, as documented:
the CLI validates neither truth nor reference resolution.

Repository static validation is recorded in [static-checks.txt](static-checks.txt),
separately from the 25 executable journal tests. Neither is an agent evaluation.

## Synthetic usability replay

The [protocol](../../event-journal/protocol.md) was written before execution.
The [authored fixture](../../event-journal/scenario.json) provides a local timeout
approval, a staging failure and correction, and a later staging-only approval.
Probe results in that fixture are fictional evidence; only journal commands, Git
snapshot operations and mechanical checks were actually executed.

Both source routes have the same current Markdown, Git history and raw evidence.
One additionally has JSONL. The author reviewed nine questions (three per cutoff)
and retained supported answers and source routes in [reviews.json](reviews.json).
These are worked examples, not fresh-reader answers or a 9/9 agent score.

| Question | What the journal offers | What the baseline already provides |
| --- | --- | --- |
| What check ran, with what scope/revision/result? | Named fields and a verification filter | Raw check note, Git revision and context qualification |
| Why did context change and whose decision was it? | Context-update and decision events with source references | Context, source decision and Git diff |
| What remains unresolved? | Retained contradiction plus later qualifications | Current context and raw evidence |

All nine questions are answerable from the shared evidence. There is no additional
verified fact introduced by JSONL. Potential value is organization and retrieval;
neither reader effort nor net logging effort was measured here.

Three boundary findings matter:

- The incorrect production-failure event survives beside its staging-only
  correction. The actual [verification query](queries.json) returns both; the
  reader must follow `supersedes`. The CLI does not resolve current truth.
- A decision query returns both the earlier proposal and later approval. Filtering
  is not an authoritative current-state view.
- The raw stage-3 note contains a failed restore drill deliberately omitted from
  the journal. Shared evidence supports that answer; journal-only reading cannot.
  Reliable capture is still a workflow responsibility.

The replay required ten authored payloads totaling 3,899 serialized input
characters, producing 5,117 bytes of final journal history. This is a description
of this fixture, not a token count or time measurement. It adds material to maintain
alongside the original evidence. The journal still needs a real-work benefit test.

Inspect [per-stage results](run/replay.json),
[stage 1](run/stage-1/context.md), [stage 2](run/stage-2/context.md),
[stage 3](run/stage-3/context.md), [full read output](run/full-read.json),
[Git history](run/git-history.txt) and the portable
[synthetic Git bundle](run/synthetic-history.bundle). Each stage directory retains
the raw evidence, JSON inputs, stored journal and command outputs. The
[provenance](run/provenance.json) records hashes, Python, platform and base revision.

## Local latency diagnostics

Three samples per condition, Python 3.9.6 on this macOS host. Timings include a fresh
CLI process, startup, validation, and captured JSONL output, with a warm filesystem
cache. Each row starts with the listed seeded count; consecutive samples add one
record each. These are local diagnostics, not comparative performance claims.

| Seeded records in one session | Median read | Median append |
| --- | ---: | ---: |
| 10 | 24.0 ms | 24.6 ms |
| 100 | 28.5 ms | 28.7 ms |
| 1,000 | 48.6 ms | 46.7 ms |
| 10,000 | 249.3 ms | 217.2 ms |

At 10,000 records the file starts at 4,380,000 bytes. Each append scans and validates
the existing session, so the cost grows with session history. This supports keeping
sessions bounded; it does not establish a safe universal size threshold.

Across 100 files with ten events each, selecting one session returned 4,380 bytes
in a median 24.4 ms, versus 438,000 bytes and 51.0 ms for a full read. Explicit
session selection limits output and work; a type filter still validates the
selected history. See [all samples](run/latency.json).

## Reproduce and limits

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 evals/event-journal/evaluate.py \
  --work .local/event-journal-evaluation-repeat \
  --output .local/event-journal-results-repeat
python3 evals/checks/static_checks.py
```

Use new output/work directories; the runner refuses existing ones. Replays generate
new UUIDs, recording times and Git commit IDs; behavioral checks are reproducible,
not byte-identical reruns. Latency can vary by machine and cache state. The retained
hashes identify the version actually measured.

There were **zero fresh-agent sessions**. The fixture, answers and review were
authored together, with no blindness or independent reviewer. This did not complete
the proposed three-real-session trial, measure human/agent logging effort, compare
SQLite performance, validate Windows/network filesystems, or prove crash durability.
One repaired decoding edge case and the passing controls justify continued bounded
testing, not general reliability or a claim that JSONL is superior to Markdown.
