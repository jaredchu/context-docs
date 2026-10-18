# skills.sh telemetry-enabled installation and visibility

October 18, 2026. **One isolated install passes; both skill pages are available,
but owner-filtered search still returns zero results.**

## Installation

One `skills@1.7.2` invocation installs both siblings from released v0.2.5
(`89c91f424476c8194a89cd38f4f48c5078fa1574`) into a new private project, using
project-scoped default symlink mode for Codex and Claude Code. Core is **0.2.5**;
adoption is **0.1.14**. All 16 released files per client layout match the
[previously pinned hashes](../2026-10-18-skills-sh/summary.json), and the CLI files
match the previously integrity-verified npm package. No installation retry runs.

Telemetry opt-outs are removed only from the child environment. The unchanged CLI
sends one install event naming both skills and their repository paths; its request
receives HTTP 200. A scratch-only fetch observer records the original response
status without modifying responses or replaying requests. The event is explicitly
marked `ci=1` and `agent=codex`; acceptance does not establish a counted install,
completed indexing or popularity. npm caches/configuration and XDG state stay in
scratch; a macOS sandbox confines child filesystem writes there except `/dev/null`.

## Public visibility

| Surface | Immediate check | Approximately 38 seconds later |
| --- | --- | --- |
| [Repository page](https://www.skills.sh/jaredchu/context-docs) | HTTP 200; both skills listed, zero total installs | Same |
| [Core skill](https://www.skills.sh/jaredchu/context-docs/context-docs) | HTTP 200; actual skill content visible | Same |
| [Adoption skill](https://www.skills.sh/jaredchu/context-docs/adopt-context-docs) | HTTP 200; actual skill content visible | Same |
| Owner-filtered search for either skill name | HTTP 200; zero results for both queries | Same |

The skill pages now show content rather than the unavailable/404 text from the
[earlier check](../2026-10-18-skills-sh/README.md). This before/after observation
does not prove causation or establish search-indexing timing. The
[summary](summary.json) records exact URLs, timestamps, telemetry fields and limits;
raw responses and installation receipts remain in the new durable private root.

## Preservation and limits

All 23,511 protected file/symlink entries match before recording these results,
including real installed skills, setup files, saved studies and the prior private
installation evidence. The new result, concise context update and journal event
are separate additions; earlier evidence is unchanged. No global upgrade, adoption,
client/model launch, native behavior test or upstream issue submission occurs.
The next discovery check can be read-only; another installation is unnecessary.
