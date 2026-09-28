# Final-state discovery follow-up — September 28, 2026

**Discovery still fails factual review; hold the merge.** The context now accounts
for the README it creates, but its final response still says no README exists.
Both the context and final response also assert string-only CSV output without
the necessary qualification. No further model run followed this result.

Candidate `269e260`, frozen protocol `cdb4cee`, unreleased core `0.1.2` / adoption
`0.1.4`, CLI `2.1.234`, model `claude-opus-5`. One fresh discovery session uses the
same unnamed request and five review criteria as the
[preceding targeted run](../2026-09-28-native-discovery-final/README.md).
The only subsequent skill refinement asks review to reconcile claims with the
resulting project and label retained pre-change observations.

| Check | Outcome |
| --- | --- |
| Unnamed selection | Pass: explicit adoption Skill call |
| Grounded context and factual report | Fail: universal CSV claim and stale final README statement |
| Maintenance rule and code preservation | Pass |
| README/index navigation | Pass |
| All project-file mechanical checks | Pass |
| Strict execution check | Fail: denied compound verification command |

Semantic result: **3/5 criteria, failed overall**. Mechanical result: **0/1 sessions**;
only `no_execution_error` fails. The denied command combines diff/status checks
and shell link checks; its denial is preserved separately from the factual failures.
The agent recovered with other checks. Immutable code, installed packages, links,
and no unsolicited staging/commits pass the grader.

The context correctly distinguishes package versions from the standard version,
attributes the layout to the assistant, leaves automatic loading unconfirmed and
avoids the earlier unsupported publication claim. Its no-README observation now
explicitly excludes the new README. Those improvements do not establish reliability:
the final response loses that temporal qualification, and the universal type claim
is false for irregular rows. The retained [synthetic counterexamples](../2026-09-28-native-v014/counterexamples.json)
show missing fields becoming `None` (JSON null) and extra fields becoming a list.
The evaluated files and responses remain unchanged.

## Evidence and limits

- [Protocol](protocol.json), [controls](controls.json), [trials](trials.json), [reviews](reviews.json)
- [Summary](summary.json), [table](table.md), [provenance](provenance.json)
- [Transcript excerpt](logs/discovery-pass-1.jsonl)

The [second six-session candidate](../2026-09-28-native-v014-followup/README.md)
passed five semantic sessions (routing, repeats and audit); discovery failed.
This targeted run tests a later candidate, not those five sessions again. Exact
commits and protocol hashes distinguish candidates sharing unreleased versions.
The [first candidate](../2026-09-28-native-v014/README.md) and all intermediate
failures are retained without rescoring.

These are author-created synthetic fixtures and author review, not independent or
blinded validation. Repeated development on one discovery fixture cannot establish
a general accuracy gain. Keep the branch unmerged; before further prompt tuning,
seek independent cases and review that checks claims against concrete evidence.
No release tag or merge was performed.
