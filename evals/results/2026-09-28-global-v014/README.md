# Global v0.1.4 acceptance — 2026-09-28

**The final global candidate passes the focused no-history-access check in Codex
and explicit native Claude Skill invocation. Slash-only Claude invocation remains
unreliable in the observed CLI run.** Both clients now have core 0.1.4/adoption
0.1.5 installed globally, with prior copies backed up outside skill directories.

Five fresh sessions tested authored no-Git fixtures with accurate current notes,
one seeded historical event and a direct link to that event. No new work or facts
were supplied. Skill-name lookup remained enabled and there were no local skill
copies, direct-read overrides or task reminders to avoid history.

| Condition | Result |
| --- | --- |
| Initial Codex named invocation | Pass: loaded global skill; no journal access; bytes unchanged. |
| Initial Claude slash-prefixed request | Fail: no Skill invocation or skill-file read observed; listed and read the journal. Bytes unchanged. |
| Explicit native Claude Skill control | Partial: updated body loaded and event contents skipped, but broad `Glob *` enumerated the journal filename. Strict no-access gate failed. |
| Revised known-path guidance, Codex | Pass: direct reads of README, current notes and global skill; no journal access or writes. |
| Revised known-path guidance, Claude native Skill | Pass: exact updated global body observed in stream; direct reads of README/current notes; no journal access or writes. One compound shell command was denied. |

The final candidate adds two sentences directing unchanged maintenance to known
entry-point paths because broad project searches can also enumerate journal
files. The helper/schema/adoption package are unchanged. Candidate hashes differ
from the earlier 0.1.4 studies; [summary and frozen package hashes](summary.json)
keep every condition separate. This tests the targeted behavior under evaluation
boundaries, not reliable automatic/slash-only selection or unrestricted execution.
The [prior capture/investigation study](../2026-09-28-read-gating/README.md) remains
separate evidence on the preceding instruction candidate.

[Final Codex operations](known-paths/codex-repeat-operations.json) and
[final Claude operations](known-paths/claude-repeat-operations.json) show the actual
accesses. Candidate exposure was checked against the full Claude skill body in the
stream, not inferred from package presence. All five sessions preserved project
and global-package bytes. Raw streams remain in ignored `.local/global-v014-*`
folders; inspected prompts, final responses, normalized synthetic paths and raw
stream hashes are retained here. This was author-reviewed, not independent.

The current [official Claude skills guidance](https://code.claude.com/docs/en/skills#skill-not-triggering)
recommends availability checks and rephrasing when selection fails. Neither that
page nor the [headless documentation](https://code.claude.com/docs/en/headless)
establishes the cause of this observed slash-prefixed failure. The explicit-tool
follow-up must not be treated as rescoring it.

Local validation passed all 90 regression tests plus core/quality/Claude/adoption
controls. Metadata and repository packaging/link/version checks passed separately
from these model results. Release remains experimental; no claim of measured
logging cost reduction or general reliability is made.
