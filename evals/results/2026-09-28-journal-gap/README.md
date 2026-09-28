# Durable capture-gap follow-up — 2026-09-28

**Both clients preserved the failed capture's reason in Markdown, and both fresh
readers recovered it after the helper was restored.** All four sessions met the
focused functional and factual acceptance. Existing history/instructions/packages
survived; both investigations left all project-file bytes unchanged and wrote no
events. This resolves the demonstrated lost-reason problem in these fixtures.

The [frozen follow-up](gap-protocol.md) changes only the core journal guide's
failure handling: retain a compact note naming the affected event, observed
failure reason and date/source when requested logging is unavailable. This is
exceptional historical evidence, not a second routine log. The helper/schema and
adoption skill are unchanged. Earlier core v0.1.3 candidate results remain attached
to their own hashes; all revisions are still unreleased.

Four fresh native sessions ran: missing-helper maintenance, then read-only
investigation after restoration, in each client. The fixture enabled logging in
advance; this is not another enablement test. The new fact was a pending restore
check, not an executed verification. Each client updated current Markdown and
recorded that the context update could not be journaled because the installed
helper was absent. Neither fabricated an event or replacement helper. Only the
legacy record remained. Fresh readers recovered that actual historical reason,
kept the check unexecuted, and distinguished restored current availability from
the prior failure. Claude also successfully used the restored helper's read
command; Codex limited its conclusion to current file availability.

Native versions/defaults and boundaries match the lifecycle studies: Claude Code
2.1.234 / claude-sonnet-5; Codex CLI 0.158.0-alpha.2.1, actual model ID unavailable
in the stream. Guard/tool failures are retained separately from semantic outcomes.
This is a focused, author-reviewed test with one trajectory per client, not proof
of general reliability, unrestricted behavior or efficient high-volume logging.

After the model runs, a wording-only refinement expands “unrecorded event” to
“unrecorded or unconfirmed event,” consistent with the existing warning that an
I/O error can follow a completed write. That clarification received static review,
not an extra model run. The 25 existing helper tests include the actual ambiguous
fsync-error behavior; no runtime code changed here.

See [frozen inputs and candidate hashes](frozen.json),
[mechanical summary](mechanical-summary.json), [per-stage table](table.md),
[author review](reviews.json), [Claude transitions](claude-trials.json) and
[Codex transitions](codex-trials.json). Prompts, native streams, final messages,
Claude hook events and project snapshots are retained. The original
[lifecycle failures](../2026-09-28-journal-integration/README.md) and
[Claude follow-up limitations](../2026-09-28-journal-integration-followup/README.md)
remain part of the evidence.
