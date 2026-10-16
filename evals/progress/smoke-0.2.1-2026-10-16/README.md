# Core 0.2.1 candidate: focused visual-path smoke

October 16, 2026. **Both native create cases pass this fixture's visual and source gates.**
These use copies of the unreleased candidate, not the installed v0.2.0 packages.

| Client | Requested model / effort | Elapsed | Resolving links, view + context | Result |
| --- | --- | --- | --- | --- |
| Codex CLI 0.162.0-alpha.17.2 | gpt-6.1-sol / medium | 48.75 s | 18 | Pass |
| Claude Code 2.1.296 | claude-opus-5-5 / medium | 38.04 s | 14 | Pass |

Each client had one fresh session, a 180-second cap and no retry. Claude's native
messages and terminal usage report Opus 5.5; Codex's responding identity is not
exposed, so its model is requested rather than independently confirmed.
Sol inspected both exact outputs and scored them against the frozen criteria;
Claude participated as a native skill subject, not an independent reviewer.

## Inspect the visuals

- [Codex progress view](codex/notes/progress.md) and [entry point](codex/docs/context.md).
- [Claude progress view](claude/notes/progress.md) and [entry point](claude/docs/context.md).

Both text trees show the documented incomplete goal and parallel completion
checks. DONE column compatibility is separate from BLOCKED, unrun empty-input
testing. The blocked branch contains the missing-sample prerequisite and NEXT
obtain sample, then run the check. Neither makes one check depend on the other.
Claude writes an explicit `depends on` line; Codex includes the prerequisite in
its nested NEXT line. Both remain readable as plain text.

Both place deployment and the unapproved, unimplemented retry proposal outside
the required completion path. Diagram keys resolve through real clickable links
outside their fences. Meaningful advances have their own source links. Both
separate useful path discovery from completion and qualify repeated attempts as
a possible stall, with the compared dates and source evidence. They date the
saved snapshot and leave later state unknown, without percentages or live-agent
claims. No material visual/source gap was found in these two outputs.

## Inputs, boundaries and evidence

The [frozen protocol](protocol.json) retains every synthetic input, exact prompt,
criteria, invocation and candidate package hash. The repository's authored
example view was withheld; the candidate's packaged guide was available. Each
fixture reused the earlier Reed Export facts, with instructions changed to read
the copied candidate directly. The [summary](summary.json) records model identity
limits, exact output/transcript hashes, link checks and the author assessment.
The source evidence is fictional; no export implementation or application test
was run.

Trace inspection confirms both read the copied core and packaged progress guide.
Codex used local shell reads and Markdown edits with user config ignored,
workspace-write sandbox, memories/multi-agent disabled and an ephemeral session.
Claude used safe/restricted mode with Read/Write/Edit only, no MCP, hooks or auto
memory and no session persistence; its init reports no API-key source. API/provider
override variables were removed only from child environments; existing subscription
authentication was reused. These controls differ from ordinary interactive sessions
and do not establish general isolation. Codex emitted state-db fallback warnings;
the successful result and raw stderr are retained without changing client state.

Only `docs/context.md` and `notes/progress.md` changed in each fixture. Every
other fixture entry, including owner work, instructions, source evidence and the
copied core, retained its bytes and mode. Generated documents here are byte-exact,
with their source files copied beside them so relative links remain usable.
New raw transcripts, receipts and preservation manifests are retained privately
under a durable evidence root, outside the repository.

## Scope limits

This is two explicit copied-candidate create cases, scored by the implementation
coordinator. It checks the visual requirement on this fixture, not general
visual usefulness, user benefit or reliable loop detection. No refresh, identical
repeat, adoption, read-only audit, local-only storage, implicit discovery, Git or
journal-history scenario was run. The [full manual suite](../README.md) remains
unexecuted. Earlier studies and their findings retain their original scope.
Installed v0.2.0 skills were not upgraded, and core 0.2.1 remains unreleased.

Repository static checks are reported separately from these native outcomes.

Preservation hashes and modes match for all four installed skill packages, prior
durable evidence, saved studies, existing setups and every pre-existing repository
entry except the three authorized current documentation updates. The check excludes
repository `.git` and the new private evidence root; it makes no byte-for-byte
global client-state claim. Original v0.2.1 skill/example files and earlier review
packets/events are unchanged by this smoke task.

Closeout: `python3 -B evals/checks/static_checks.py` passes (1,493 relative links
and anchors, five published result tables, two skill packages and two declared
versions). `git diff --check` passes. These are mechanical checks, separate from
the two native visual-path outcomes.
