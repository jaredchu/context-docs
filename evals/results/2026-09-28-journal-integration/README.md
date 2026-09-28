# Opt-in journal integration — 2026-09-28

**The optional integration is implemented, with logging off by default.** Core
v0.1.3 packages the helper and its guide; adoption v0.1.5 merges explicit settings
without replacing existing adoption. The helper/schema are unchanged, with the
old repository command retained as a compatibility entry point.

Native evidence is mixed and retained separately: Codex passed the nine-stage
functional lifecycle here; Claude skipped enablement and other requests. A
[separately frozen Claude invocation follow-up](../2026-09-28-journal-integration-followup/README.md)
then passed those functional stages using the identical skills and task-first
native invocation. Neither result establishes general reliability or clean
unrestricted execution. A subsequent [four-session capture-gap follow-up](../2026-09-28-journal-gap/README.md)
tested a narrow guidance repair after discovering that capture-failure reasons
were lost outside the final chat response.

## What was installed and tested

The [frozen protocol](protocol.md) covers two upgraded, already adopted projects:
Claude-only CLAUDE.md with no Git, and mixed instructions with AGENTS.md as the
Codex entry and one initial commit. The runner copied the old core 0.1.2/adoption
0.1.4 packages from HEAD, replaced them with candidate packages, and verified
project-owned files and pre-existing schema-v1 history stayed byte-identical.
It preserved the September 1 adoption date, custom notes/current.md entry,
unrelated release checklist and instruction routing. No global installation or
real user project was modified.

Each client then ran nine fresh sessions: ordinary default-off adoption, explicit
enablement, real failing synthetic probe, new approval plus passing probe, repeat
setup/maintenance, missing-helper injection, fresh read-only investigation,
disabling, and disabled maintenance with the helper absent. These were actual
file tools and direct packaged-helper invocations, not the earlier bridge. The
probe really ran and returned exits 7 and 0; its behavior is a local synthetic
fixture, not a real infrastructure incident or production test.

Clients: Claude Code 2.1.234, stream model claude-sonnet-5; Codex CLI
0.158.0-alpha.2.1, client default with user config ignored. Codex does not expose
a model identifier in these retained streams. The two instruction/Git layouts
and defaults differ, so these runs are not a model comparison.

## Original outcomes

Codex passed all functional stages. Only requested enable/disable settings changed
in its instructions. It appended three new events: the real fixture failure,
owner approval and later passing check. Recorder (`Codex`), authority/source,
uncommitted revision qualification and scope were correct. The existing legacy
record survived unchanged. Repeat setup and the audit preserved all project-file
bytes. Missing-helper and disabled maintenance updated Markdown without adding
records; the former accurately reported capture unavailability.

Claude's original condition **failed**. Several responses said there was no actual
request, although the retained prompt contained one. Enablement was skipped and
logging stayed absent/off for the entire trajectory. Some Markdown maintenance
and the first probe did run, but no new journal record was written. The runner
continued after semantic misses, so later unchanged logs do not validate enabled
repeat, missing-helper or disabling behavior. The follow-up is a separate condition,
not a replacement score. Startup InstructionsLoaded hashes match CLAUDE.md in all
nine original sessions; this does not identify why requests were skipped.

All original project/package protection checks passed, as did legacy preservation.
These checks constrain damage; they do not establish task completion or factual
quality. [Author reviews](reviews.json) distinguish those outcomes. Native guard
denials, stdout, final responses and other errors remain in their original files.

## Evidence and limits

- [Frozen inputs, versions, hashes and requests](frozen.json); exact source/package
  copies under `source/` and project snapshots after each stage.
- [Mechanical summary](mechanical-summary.json), [per-stage table](table.md),
  [loading checks](loading-checks.json), [Claude transitions](claude-trials.json)
  and [Codex transitions](codex-trials.json).
- Per-session prompts, native streams, final responses, stderr and Claude hook
  events are retained beside the snapshots. Read these together with the reviews;
  a zero process exit or unchanged files cannot prove semantic success.

Claude's evaluation hook exposed file tools and a limited set of direct commands;
it is not an OS sandbox and is not part of the installed skills. Codex used its
native sandbox. File protection is enforced in parts of this test, not evidence
that unrestricted agents never make out-of-scope attempts. Codex file reads do
not provide the same startup-loading proof as Claude's hook. Host instructions,
one trajectory per client and non-independent author review limit generalization.

The targeted helper-absence snapshots deliberately retain a missing file. Only
those exact frozen links are exempted from repository link validation; package
validation still requires the helper in the shipped core. Python itself was not
uninstalled. Clean old packages were upgraded; customized package merges,
other platforms, older journal schemas and long-running operational capture were
not evaluated. Timings and tool counts are descriptive, not a speed/cost advantage.
No universal need for JSONL is established; earlier Markdown comparisons stand.
