# Second unreleased 0.1.2 / 0.1.4 candidate — September 28, 2026

**Five of six sessions pass semantic review; four pass all mechanical checks.**
Routing, repeats and auditing meet their factual and preservation criteria.
Discovery still overattributes implementation choices to the user and strengthens
a qualified CSV description in its final summary. It remains a failure; the
[targeted discovery regression](../2026-09-28-native-discovery-final/README.md)
tests a subsequent refinement separately.

Candidate `dce1a47`, protocol frozen in `1024fa5`, CLI `2.1.234`, model
`claude-opus-5`. These are six fresh sessions with the same requests and strengthened
rubrics as the [first candidate](../2026-09-28-native-v014/README.md).

## Changes and results

The core guidance now avoids unverified guarantees for every input and focuses
final reports. The adoption metadata no longer hardcodes AGENTS.md. The shared
grader accepts directories containing known sources while retaining integrity
checks. Additional hash/inspection commands are preapproved. These changes mean
this is a separate condition, not a rescore of the first candidate.

| Session | Mechanical | Semantic | Observation |
| --- | --- | --- | --- |
| Claude-only adoption | Fail: permission | 4/4 | Correct rule/marker and factual summary |
| Claude-only repeat | Pass | 2/2 | All bytes/date preserved; no staged/unstaged misstatement |
| Mixed adoption | Pass | 4/4 | One rule with a reference; loading grounded in explicit request |
| Mixed repeat | Pass | 2/2 | All bytes/date preserved; accurate path and status report |
| Audit-only | Pass | 3/3 | Read-only; missing marker and unconfirmed loading kept separate |
| Discovery | Fail: permissions | 3/5 | Selection/navigation pass; decision attribution and summary fail |

Every project-file check passes, including relative links, package hashes,
immutable files, no staging/commits and whole-tree identity for no-op cases. The
Claude-only first pass encountered a denied `git -C <fixture> diff` command and
recovered with permitted `git diff`; the strict execution check remains failed.
Discovery's denied compound commands likewise remain visible.

Discovery records correct versions, avoids the absent-remote publication claim,
qualifies loading and creates README navigation. However, its context labels the
chosen Context Docs method and file layout as `Approved (user request)`. The
unnamed request authorizes ongoing documentation maintenance, not those specific
agent-chosen details as an explicit owner decision. Its final response also says
"all values left as strings," losing the document's irregular-CSV caveat. The
next refinement preserves decision attribution and qualifications in summaries.

## Evidence and limits

- [Frozen protocol](protocol.json), [controls](controls.json), [trials](trials.json), [reviews](reviews.json)
- [Summary](summary.json), [table](table.md), [provenance](provenance.json)
- [Claude-only adoption](logs/claude-instructions-pass-1.jsonl) and [repeat](logs/claude-instructions-pass-2.jsonl)
- [Mixed adoption](logs/split-instructions-pass-1.jsonl) and [repeat](logs/split-instructions-pass-2.jsonl)
- [Audit](logs/audit-only-pass-1.jsonl), [discovery](logs/discovery-pass-1.jsonl)

Author review inspected snapshots, hashes and tool traces against each frozen
criterion. Neither review nor fixtures are independent or blinded. One client/model,
local execution, and one attempt per condition do not establish general reliability.
Both candidates use the same unreleased package version numbers; exact commits
and package hashes distinguish them. No release tag or merge was performed.
