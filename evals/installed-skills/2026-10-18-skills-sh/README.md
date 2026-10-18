# skills.sh discovery and isolated installation check

October 18, 2026. **Direct GitHub discovery and one isolated installation pass.**
The public skills.sh catalog does not surface these skills at check time.
This checks packaging, not native agent behavior.

## Discovery

`skills@1.7.2` lists exactly `context-docs` and `adopt-context-docs` from both
`jaredchu/context-docs` and the pinned v0.2.5 `skills/` path. The public search
request for `context-docs`, owner `jaredchu`, returns HTTP 200 with zero results.
The repository page returns 404. Each individual skill page returns HTTP 200 but
renders a “404 / isn't available in this repository” message; HTTP success alone
does not establish a listing.

An initial `--list --json` request is rejected by the CLI before installation.
Corrected plain `--list` succeeds. Both receipts remain retained; the actual
installation runs once, with no retry.

## Installation and verification

One project-scoped invocation installs both sibling packages from released commit
`89c91f424476c8194a89cd38f4f48c5078fa1574` (core **0.2.5**, adoption **0.1.14**),
using the default symlink mode. Codex reads canonical files in `.agents/skills/`;
Claude Code receives links under `.claude/skills/`, all within the new scratch tree.

| Check | Codex layout | Claude Code layout |
| --- | --- | --- |
| All released package files accessible and byte-equal | 16 | 16 |
| Packaged links/anchors resolve, including the adoption sibling dependency | 21 | 21 |
| `event_journal.py --help` | Exit 0 | Exit 0 |
| `journal_policy.py --help` | Exit 0 | Exit 0 |

This includes both `SKILL.md` files, every reference, asset and Python helper,
Codex metadata, licenses and version files. The [summary](summary.json) retains
all 16 release-file hashes, normalized commands, outcomes and limits. The npm CLI
files match an archive verified against npm's published SHA-512 integrity value.

Npm cache/configuration, temporary clones and XDG state are confined to the private
scratch root. A macOS sandbox denies filesystem writes outside that root except
`/dev/null`. Telemetry, package lifecycle scripts and Node compile caching are
disabled. The original project files, installed skill trees, setup files and saved
studies match their pre-check bytes/modes. Only this new public result record,
current context and one journal event are added or updated afterward.

## Limits

This validates a pinned, project-scoped symlink installation, not global installs,
upgrades or copy mode. Helper help checks establish startup only. No native client,
model session, adoption, skill invocation or functional journal test runs; there
is no implicit-loading, preservation-during-maintenance or everyday-reliability
claim. Existing [installed native smoke](../2026-10-18-concurrency-v025/README.md)
and [release qualifications](../../../docs/releases/v0.2.5.md) remain unchanged.

Public directory visibility is a dated observation, separate from direct GitHub
installation. Telemetry is disabled, so this check makes no registration or
listing claim. No marketplace submission is performed. Raw receipts, page bodies,
isolation settings and the installed scratch fixture are retained privately.
