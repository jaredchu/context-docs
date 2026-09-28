# Decision-attribution discovery regression — September 28, 2026

**The attribution and summary defects improved, but this session still fails.**
It creates README.md, then retains unqualified statements in context.md and the
final response that no README exists. Initial-state observations were not reconciled
with the resulting project.

Candidate `6772889`, frozen protocol `a8481f1`, unreleased core `0.1.2` / adoption
`0.1.4`, CLI `2.1.234`, model `claude-opus-5`. This is one fresh discovery session
with the same unnamed request and five review criteria as the preceding run.

| Check | Outcome |
| --- | --- |
| Unnamed selection | Pass: explicit adoption Skill call |
| Grounded context and factual report | Fail: stale no-README statements |
| Maintenance rule and code preservation | Pass |
| README/index navigation | Pass |
| All project-file mechanical checks | Pass |
| Strict execution check | Fail: denied verification commands |

Semantic result: 3/5 criteria, failed overall. The context now attributes the
chosen layout to the assistant, and the final summary preserves the source-based
verification limit rather than repeating the previous universal string-value
claim. Those improvements do not erase the stale-state failure.

The next [final-state follow-up](../2026-09-28-native-state-followup/README.md)
adds a narrow review step for facts made stale by the agent's own edits. Its input
hashes distinguish another unreleased candidate; these artifacts remain unchanged.

- [Protocol](protocol.json), [controls](controls.json), [trials](trials.json), [reviews](reviews.json)
- [Summary](summary.json), [table](table.md), [provenance](provenance.json)
- [Transcript excerpt](logs/discovery-pass-1.jsonl)

Review was author-conducted, not independent or blinded. One local native session
on a synthetic case establishes neither general reliability nor a causal advantage
for the prompt change. See the [preceding six-session follow-up](../2026-09-28-native-v014-followup/README.md)
for the separate routing, repeat and audit evidence.
