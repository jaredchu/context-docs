# Native Claude Code smoke test — September 28, 2026

**Four routing/repeat sessions pass mechanical and semantic checks.** The audit
completed and preserved every project file, but a denied hash command and a parser
crash prevent full execution acceptance. Discovery was not started. This is not a
six-session pass; a [separate targeted follow-up](../2026-09-28-claude-code-followup/README.md)
tests audit and discovery after the harness repair.

## Method and results

Protocol frozen in `e676300`, harness `27ea769`, CLI `2.1.234`, requested and
observed model `claude-opus-5`. Core skill `0.1.1` and adoption skill `0.1.3` were
unchanged. Fixtures ran outside the source repository with standard input closed.
Each pass was a fresh CLI session; repeats inherited the previous project's files.

| Session | Mechanical | Semantic review | Key observation |
| --- | --- | --- | --- |
| Claude-only adoption | Pass | 3/3 | Rule and marker in CLAUDE.md; uncommitted blocker retained |
| Claude-only repeat | Pass | 1/1 | Entire project unchanged; original date retained |
| Mixed-file adoption | Pass | 3/3 | Rule in CLAUDE.md, reference from AGENTS.md, no duplication |
| Mixed-file repeat | Pass | 1/1 | Entire project unchanged; original date retained |
| Audit-only | Fail: execution | 2/2 | No file changes; absent marker distinguished from non-adoption |
| Unnamed discovery | Not run | Not reviewed | Runner stopped after audit parser crash |

Author review inspected final project snapshots, complete-tree SHA-256 maps,
assistant responses and tool calls/results. Installed-core reads were observed in
all five sessions. Named slash invocation need not produce a separate `Skill`
tool call, so package reads are the recorded invocation evidence here.

## Audit failure and recovery

Claude requested `shasum -a 256` to verify the audit's read-only behavior. That
command was outside the frozen preapproved tool rules and was denied. Claude
continued using Git inspection and emitted a completed audit response. The runner
then crashed because a system permission event had a string-valued `message`,
while its parser assumed every message was an object.

The stream and project files survived. After repairing the parser, the audit was
recovered from that original stream, without rerunning the model or changing its
criteria. Before/after snapshots could be reconstructed because the complete final
tree exactly matched the frozen initial hashes. Subprocess metadata lost at the
crash is explicitly null, not inferred. The permission failure remains scored;
semantic success does not turn it into an accepted execution.

The repair also preapproves read-only `shasum` and supports selecting trajectories
when building a new protocol. The follow-up changes those execution conditions;
it does not replace these results.

## Evidence and limits

- [Frozen protocol](protocol.json), [trials](trials.json), [explicit reviews](reviews.json)
- [Summary](summary.json), [generated table](table.md), [provenance and recovery](provenance.json)
- [Claude-only adoption](logs/claude-instructions-pass-1.jsonl) and [repeat](logs/claude-instructions-pass-2.jsonl)
- [Mixed adoption](logs/split-instructions-pass-1.jsonl) and [repeat](logs/split-instructions-pass-2.jsonl)
- [Audit transcript](logs/audit-only-pass-1.jsonl)

These are small synthetic fixtures with author review, one client/model and no
comparison arm. The requests state which instruction file is loaded; they do not
validate all Claude loading configurations or cross-machine paths. Local execution
is not container/network isolation. A repeat inspected its client-provided memory
directory outside the fixture, which was absent; no writes there were observed.

The routing responses sometimes described an unapproved cloud-sync proposal as an
unresolved conflict. Stored documents correctly preserved Approved/Proposed
statuses; the narrow routing rubrics do not establish the quality of every final
prose claim. Passing scores must not be promoted into general correctness claims.

The earlier [authentication failure](../2026-09-28-claude-code/README.md) and
[inherited-input contamination](../2026-09-28-claude-code-retry/README.md) are retained
separately. Neither is included in the five completed sessions above.
