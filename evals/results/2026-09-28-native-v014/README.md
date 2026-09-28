# First unreleased 0.1.2 / 0.1.4 candidate — September 28, 2026

**The original version, publication and automatic-loading errors were corrected
in these samples, but the strengthened regression did not pass.** All six model
sessions completed. Two passed every mechanical check; one passed every semantic
criterion. No session passed both sets. Those counts include stricter final-report
criteria absent from earlier studies, and are not comparable aggregate quality
scores.

Candidate source: `aad4426`, protocol frozen in `866e382`. Packages were unreleased
core `0.1.2` and adoption `0.1.4`; their exact input hashes are retained. CLI
`2.1.234`, model `claude-opus-5`, six fresh sessions, same requests as before.

## What changed and what happened

The candidate tightened exact claim/source scope, final-response checking,
automatic-loading evidence and minimal README navigation. Review criteria were
expanded before execution; [calibration controls](controls.json) show positive and
negative examples. They were not sent to the model.

| Session | Mechanical | Semantic | Remaining finding |
| --- | --- | --- | --- |
| Claude-only adoption | Fail | 3/4 | Denied hash commands; final response misstates a path's parent |
| Claude-only repeat | Fail | 1/2 | Denied hash command; calls unstaged edits staged |
| Mixed adoption | Pass | 3/4 | Final response misstates a path's parent |
| Mixed repeat | Pass | 1/2 | Same path-parent misstatement; all files unchanged |
| Audit-only | Fail | 3/3 | Denied inspection command; loading correctly left unconfirmed |
| Discovery | Fail | 3/5 | Denied commands, directory-link grader defect, CSV overgeneralization |

All preservation, routing and date checks passed. The path-parent error is the
parenthetical claim that `knowledge/state.md` and `CLAUDE.md` are both at repository
root. The former is inside `knowledge/`; the actual relative links remain correct.
The new factual criterion deliberately counts this report error, even though the
stored project files are correct. The repeat's staging claim is contradicted by
the empty Git index and the recorded unstaged diff.

Audit correctly separated the existing maintenance rule from unconfirmed automatic
loading, reported the new versions accurately, and made no edits. Discovery read
the actual VERSION files, omitted the unsupported publication-history claim, and
created the previously missing README link.

Discovery still claimed that every `csv.DictReader` value is a string. Synthetic
[counterexamples](counterexamples.json) reproduced `None` for a missing field and
an overflow list for extra fields. Reading the script's library call does not
support that universal input guarantee.

The link to `.claude/skills/context-docs/` names a real installed directory. The
file-only grader rejected it; a later fix accepts directories containing known
sources while retaining package-integrity checks. The old failed result is
preserved here, not rescored. Optional denied shell commands likewise remain failed
execution checks despite completed final responses.

## Evidence and follow-up

- [Protocol](protocol.json), [trials and snapshots](trials.json), [explicit reviews](reviews.json)
- [Summary](summary.json), [table](table.md), [provenance](provenance.json)
- [Claude-only adoption](logs/claude-instructions-pass-1.jsonl) and [repeat](logs/claude-instructions-pass-2.jsonl)
- [Mixed adoption](logs/split-instructions-pass-1.jsonl) and [repeat](logs/split-instructions-pass-2.jsonl)
- [Audit](logs/audit-only-pass-1.jsonl), [discovery](logs/discovery-pass-1.jsonl)

The [separate follow-up](../2026-09-28-native-v014-followup/README.md) uses a later
unreleased candidate at `dce1a47`, with exact hashes distinguishing the revisions.
It narrows unverified input guarantees, focuses final summaries, aligns the Codex
default prompt with loaded instructions, accepts verified directory links and
preapproves additional hash/inspection commands. Both candidates retain the same
unreleased version numbers; no release tag was published between them.

Author-created fixtures and author review, one model/client, and local execution
without container isolation limit the conclusions. These results do not establish
general correctness or independent reliability. All earlier failed attempts remain
available through the [native harness](../../claude-code/README.md).
