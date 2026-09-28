# Event journal evaluation — 2026-09-28

Protocol written before the runs in this directory. This is a mechanical test and
author-reviewed synthetic usability replay, not a fresh-agent comparison. No
subagents, external services or model evaluation sessions are required. The
three-real-session trial remains separate.

## Questions and acceptance

1. Does append preserve history and fail clearly on invalid input, corrupt history,
   competing writers and a killed writer? Every acknowledged event must survive
   the tested operations unchanged. Invalid writes must not change prior bytes;
   incomplete history and stale locks must be rejected without automatic deletion.
   CLI errors should have a diagnostic and nonzero status, not an uncaught traceback.
2. Across three authored stages, can the journal retain check scope/revision,
   context-change rationale and unresolved issues? Replay the same authored events
   using the CLI, retain their inputs/outputs and Git revisions, and verify the
   generated records without treating their presence as proof of reader accuracy.
3. What does the journal add when Markdown/Git and original evidence are also
   available? Review both source routes for nine questions (three per stage).
   Record supported answers and exact routes. Do not remove evidence from the
   baseline, manufacture an accuracy advantage or measure author's retrieval speed
   after authoring the answers. A journal-only omitted-event control must remain
   unknown; an old incorrect event must remain inspectable after correction.
4. How does full validation affect append/read latency? Seed 10, 100, 1,000 and
   10,000 synthetic records into one session. Measure three fresh CLI append and
   read processes per size, with a warm filesystem cache. Also measure selecting
   one ten-record session among 100 sessions. Include subprocess startup, parsing,
   validation and output capture. Report every sample and file/output sizes;
   derive medians only as local diagnostics, not a throughput or superiority claim.

## Synthetic history

- Stage 1: configuration-only validation of a timeout change; owner approval
  applies to a local pilot, with deployment unknown. Record the rationale and an
  unresolved production-value discrepancy.
- Stage 2: a limited staging probe fails. The initial journal event overstates
  its scope; append a correction referencing the original event. Production is
  still unknown and a proposed increase is not approved.
- Stage 3: owner approves a staging-only increase after a passing bounded probe.
  Update current context while retaining production uncertainty. Include a raw
  evidence note about a restore check deliberately omitted from the journal to
  demonstrate that storage cannot recover an unrecorded event.

Questions at each cutoff: (1) what check ran, its revision/result/scope;
(2) why context changed and which authority applies; (3) what remains unresolved.
Both source routes have the identical context, Git changes and raw evidence.
The second route additionally has the journal. Review is by the authoring agent,
unblinded and order-dependent; these are worked examples, not observed reader scores.

## Evidence and repair policy

Record tool/test/protocol hashes, Python/platform, base repository revision,
commands and outputs. Retain pre-fix failures and snapshots; make only justified
repairs and rerun affected controls, then the full journal suite and repository
static checks. Distinguish seeded stress data, synthetic check outcomes and actual
executed journal commands. Do not call fictional fixture probes real tests.

Recommend continued optional use only if history/preservation controls pass after
repairs and the replay exposes a concrete retrieval use. Document remaining risks
and setup effort; do not promote this into mandatory skill integration or automatic
cleanup. Nothing here authorizes publication.
