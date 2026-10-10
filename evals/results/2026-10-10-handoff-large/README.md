# Larger matched handoff — October 10, 2026

Both fresh Opus 5.5 sessions implemented the continuation correctly, preserved
the owner’s rationale and superseded-proposal status, and retained the unresolved
exporter blocker. Both passed all 16 frozen independent CLI checks. Curated
context reduced file-read calls in this pair, but loaded slightly more text;
neither condition exhausted the retrieval budget. No general correctness,
human-effort or subscription allowance advantage is established.

| Observation | Curated context | Scattered notes |
| --- | --- | --- |
| Frozen semantic criteria | 6/6 pass | 6/6 pass |
| Independent CLI outcomes | 16/16 pass | 16/16 pass |
| Coordinator-run local suite | 14 tests pass | 12 tests pass |
| Full-file reads, maximum 16 | 9 | 13 |
| Charged UTF-8 bytes, maximum 16,000 | 5,842 | 5,721 |
| Filename-search calls, maximum 6 | 0 | 2 |
| All tool calls | 15 | 19 |
| Denied calls | 0 | 0 |
| Subject wall time | 52.6 seconds | 60.8 seconds |
| Code corrections identified | 0 | 0 |

The scattered final answer says it read 14 files. The recorded tools show 13
admitted Read calls to 13 distinct files. This quantitative self-report error is
retained; the curated report’s nine reads matches its events. There were no
actual human corrections during execution. Any report-correction need is a
reviewer estimate, not a measurement of user effort. The literal frozen claims
criterion covers inspected code, invented decisions and verification; the focus
criterion covers denials and unfinished work. Neither clearly requires exact
self-reported retrieval counts. The final six-criterion score therefore does not
expand those clauses after seeing this error. The initial fail score and final
disposition are both retained.

## Frozen design

The [manifest](protocol.json) and [SHA-256](protocol.sha256) freeze both complete
fixtures, exact prompts, expectations, acceptance criteria, budgets, verifier
and harness hashes before either subject started. Unlike the first pilot, the
independent verifier was complete and checked before subject execution.
[Coordinator preflight](preflight.json) records authority, equivalence, budget
feasibility and validation controls.

The ordinary fixture has **54 files / 52,339 bytes**; curated has **55 files /
54,279 bytes**. Both have identical code, baseline tests and underlying notes.
Only curated adds a 1,874-byte summary, a README link and an explicit entry-point
instruction. There are 36 identical benign workshop notes in each arm. The
nondistractor common material is 6,934 bytes across 18 files. Relevant sources
have meaningful filenames and can be found through search; the baseline is not
artificially concealed or deprived of facts.

The code distributes CLI parsing, loading, validation, tenant filtering,
first-occurrence deduplication and rendering across separate modules. The
continuation adds a limit through CLI → service → selection, preserving full
input validation even with zero or an already-satisfied limit. Notes disperse
owner authority and arrival-priority rationale, exact tenant/id identity,
selection sequencing, the rejected sorting/early-stop proposal, and the missing
exporter-v3 sample. The curated summary repeats those supported facts and maps
the code route; it adds no new facts.

Both subjects receive the same neutral continuation task and explicit final
report requirements. That shared guidance asks for owner rationale, superseded
proposal, blocker and honest verification limits; it may reduce reporting
omissions and is not a skill-specific treatment.

Each arm has 16 full-file reads / 16,000 UTF-8 bytes and six filename-search
calls, plus seven minutes. The hook atomically reserves calls and bytes before
allowing retrieval; simultaneous calls cannot bypass the count. Repeated reads
charge again. Read pagination, Grep content-output modes, external paths and unscoped
writes are denied. **Grep still matches file contents** and returns filenames,
revealing match/routing information without a content-byte charge. Both arms can
use at most six such queries; scattered used two and curated none. This is a
file-content-delivery budget with a separate metadata-query cap, not a cap on
all acquired information. Filename-result bytes are not charged. The frozen
preflight’s shorthand “content search denied” was imprecise and is retained
alongside this correction. These are file-byte
counts, not tokens or exact rendered model input sizes.

Both sessions expose only Read, Write, Edit, Glob and Grep; skills and MCP are
disabled and auto-memory is off. This shared tool change from the first pilot
prevents agent-written test code from reading notes outside the budget. Subjects
provide tests but cannot execute them and explicitly disclosed that. Codex runs
the frozen verifier and generated suites after each completed session. Guards
are file-tool controls, not a general OS sandbox guarantee. The custom guard
uses an exact write allowlist rather than supporting every configuration field
of the reused observer; it applies to these fixtures, not generic guard setups. Protected source,
notes, frozen verifier, control and protocol bytes remained intact; normal Python
bytecode caches are excluded from source diffs.

Order is scattered then curated, one attempt each. Identical high effort was
requested but the runtime effort level was not independently exposed. Streams
confirm exact responding model **`claude-opus-5-5`**, the same as the first pilot,
through existing Claude.ai Max authentication. No fallback, paid API access,
global-setting changes, resume or subject retries were used. No external
instruction-loading events were observed; that does not guarantee every hidden
runtime instruction was identical. Codex coordinated in the requested Sol role;
its precise model identifier was not independently exposed in this chat.

## Retained preparation failure and review

The bounded Opus fixture-author assignment timed out after **180 seconds**, with
no fixture or verifier written. [Execution](author-execution.json),
[raw transcript](author.jsonl), [assignment](REQUIREMENTS.md) and
[author prompt](author-prompt.txt) are retained. It was not retried. Codex then
completed the already-specified synthetic fixture and verifier; this change of
preparation responsibility is explicit, not a substituted subject model.

The 20-minute delegated-agent cap allocates 180 seconds to authoring, 420 to each
subject and 180 to counterpart review. Final review covers evaluation design,
budget controls and semantic scoring as well as patches and evidence. Total
delegated execution was **436.8 seconds (7 minutes 16.8 seconds)**, including
the retained 180-second preparation failure and both review sessions. Review
used 143.4 of its 180-second allocation. There was
no counterpart preflight approval after the preparation timeout; the coordinator
preflight and final counterpart findings are distinct evidence.

## Evidence and checks

- [Harness](../../handoff-large/README.md), with exact source snapshots in
  `harness/`; [trial records](trials.json), [assessment](assessment.json),
  [curated patch](curated.patch) and [scattered patch](scattered.patch).
- [Curated checks](curated-checks.json) and [scattered checks](scattered-checks.json)
  retain all 16 independent cases, stdout/stderr/status, input preservation and
  generated-suite execution. Coverage includes cross-tenant identities,
  case-sensitive keys, first duplicate payload, filtering/dedup before cap,
  missing/excess/zero limits, blank/empty input, invalid limits and corrupt late
  input including limit zero.
- [Baseline control](baseline-control.json): all three existing tests pass;
  nine of 16 independent outcomes reject the missing feature.
  [Positive reference control](reference-control.json): all 16 outcomes pass.
  [Reference files](reference-control-files.json) stay outside subject roots.
- [Five guard unit tests](unit-control-output.txt) pass, including concurrent reservations, UTF-8 byte
  charging, call/byte limits, content-search denial and edit/path boundaries.
  These are mechanical controls, separate from the actual agent sessions.
  Captured output and frozen test source were supplied after initial review
  identified that evidence gap; no source was changed or subject rerun. The
  original read-cap tests share a threshold with the byte cap; a separately
  labeled [post-review control](read-cap-control.json) checks the read cap alone.
  [Source hash confirmation](source-hash-confirmation.json) records frozen/source/
  review-material equality and actual hook import resolution.
- [Initial Opus review](review.final.txt), [focused follow-up](followup.final.txt)
  and [disposition](review-disposition.json) retain findings, revisions and
  acceptance. [Initial assessment](assessment-before-review.json) keeps the
  coordinator’s earlier read-count fail score; the final score applies the literal
  rubric and preserves that error separately. The reviewer’s content-output Grep
  was denied; reviewers share that tool restriction without retrieval quotas.
- Raw streams and final answers in `logs/`, retrieval events in `control/`,
  final synthetic trees in `projects/`. Preserve these originals and any
  initial/final assessment disagreement; do not patch subject failures away.

Repository static checks validate packaging, links, version metadata and unchanged
historical result tables. They do not grade agent behavior. Released skills,
previous studies and scores are unchanged. Project context records the bounded
result separately. Nothing was committed or published.

## Interpretation and next step

This is one author-created pair with fixed order and unblinded scoring. Time also
reflects different selected documents, reasoning and test-writing work. More
files increased available volume but the informative raw facts fit well below
the byte cap; neither subject exhausted the read cap. Thus the result observes
selective retrieval, not reliability under budget exhaustion. Curated relied on its author-prepared summary for the superseded proposal and
blocker without opening their raw notes, and disclosed that. This is the intended
supplied-context treatment, not independently maintained context or independent
source verification. The preparation
timeout is an actual failure, not a baseline/control result. No statistical
significance or allowance savings follows from reads, bytes, timing or token data.

For any separately authorized next study, use a dependency graph with more
jointly necessary sources rather than adding benign volume alone. The unused
budgets here show that corpus size did not create substantial retrieval pressure.
No additional attempt or broader evaluation was launched under this request.
