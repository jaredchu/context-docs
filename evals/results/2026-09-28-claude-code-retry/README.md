# Native retry with inherited-input contamination — September 28, 2026

**Invalid for acceptance.** Authentication succeeded after the owner refreshed
the CLI login, but the first session received the Python launch script through
inherited standard input in addition to its frozen request. Its final response
explicitly identifies that extra script and its repository paths. The first
session completed and passed mechanical checks; the second was stopped by the
reviewer when the contamination was identified. Four sessions were not started.

The runner previously left standard input inherited. Claude's print mode consumed
the heredoc used by the parent Python launcher and appended it to the request.
This is a harness defect, not a skill failure. The repair supplies
`stdin=subprocess.DEVNULL`, and the CLI-launch regression test now asserts that
contract. Fresh fixtures and a separately frozen protocol are required for the
next attempt. These scores must not be used as native acceptance evidence.

## Retained evidence

- [Protocol](protocol.json), committed in `9540074` before execution, with harness
  `bedc176`, CLI `2.1.234` and requested model `claude-opus-5`.
- [Trials and project snapshots](trials.json), [summary](summary.json) and
  [generated table](table.md). No semantic acceptance review was performed.
- [First session transcript excerpt](logs/claude-instructions-pass-1.jsonl) and
  [interrupted second session](logs/claude-instructions-pass-2.jsonl).
- [Provenance](provenance.json), including raw-stream hashes and normalization.

The first response added the rule and marker to `CLAUDE.md` and preserved the
pre-existing uncommitted blocker. It also inspected nonexistent `.local` and
`evals` directories from the appended launch script. The transcript retains that
unexpected activity. The reviewer terminated the second CLI process; its negative
exit code and missing terminal result reflect that interruption.

Transcript excerpts preserve tool calls/results and assistant text, with fixture
paths normalized. Host customization metadata and session identifiers are omitted.
Original streams remain available locally. The earlier
[authentication-blocked attempt](../2026-09-28-claude-code/README.md) is unchanged.
