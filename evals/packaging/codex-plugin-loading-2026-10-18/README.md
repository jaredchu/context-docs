# Codex plugin metadata follow-up

October 18, 2026. **Native metadata parsing passes; runtime behavior remains untested.**
Codex `0.163.0-alpha.10.2` reads the unchanged `0.2.5-candidate.1` package from a
private local catalog and returns both entries:

- `context-docs:context-docs`
- `context-docs:adopt-context-docs`

Both entries include their packaged paths, descriptions and Codex interfaces.
The missing-plugin control returns the expected `-32600` error. The enclosing
plugin remains **uninstalled and disabled**; skill-level `enabled: true` metadata
does not override those flags. The final app-server exits zero in 0.21 seconds.
The [summary](summary.json) pins the candidate hash, attempt ledger and limits.
The [earlier partial check](../plugin-loading-2026-10-18/README.md) and all its failed
receipts remain unchanged.

## Startup diagnosis and minimal route

The original failures precede plugin parsing. Redirecting SQLite and logs alone
was insufficient: a kernel sandbox log identifies denied `file-write-data` access
to Codex's existing runtime `installation_id` file. A synthetic timestamp-only
permission test also remains denied; no actual identity timestamp refresh is established.
CLI catalog discovery works, but provides no skill detail. Existing-server proxy,
remote-control-disabled startup and offline prompt rendering do not solve the block.
All failed attempts remain retained, rather than being replaced by the final success.

The successful route uses process-only `sqlite_home` and `log_dir` paths plus a
scratch marketplace. It sends only initialize/initialized and two `plugin/read`
requests over stdio. Its macOS sandbox allows writes to scratch and `/dev/null`,
with one exact canonical-file exception for runtime identity access; network is
denied. It does not reassign HOME/CODEX_HOME or change real configuration. This is
a scratch metadata check sharing existing runtime identity, not a clean account
or fully isolated runtime.

The exception permits `file-write-data` and `file-write-times`; it is **not
metadata-only enforcement**. Beforehand the identity was checked as a regular file
with one hard link, and its bytes and stat were retained privately. Contents,
size, mode, owner/group, inode, link count, mtime and ctime match afterward.
No create, rename, unlink, mode or owner permission was added for that file.
Optional remote catalog warmers attempted network access, which the sandbox blocked;
the PATH-alias write warning also remains nonfatal. No broader exception was added.

Sol investigated and checked the route. One tools-disabled, subscription-authenticated
Claude Opus 5.5 review assessed the narrow identity exception. It also recommended
a whole runtime-home manifest and stopping on any network attempt or new denial.
Those recommendations were not fully adopted: named static setup/skill/study roots
were hashed, and blocked optional requests/warnings were allowed to coexist with
local parsing. The review is qualified accordingly; it is not an unconditional
approval of every final observation. Native probes send **zero model requests**;
the separate counterpart review sends one.

## Preservation and limits

Installed skills, setup preferences, saved studies, the original candidate and
previous loading evidence are preserved. The existing progress/decision sections
and setup rules remain unchanged. One ordinary Claude feature-cache timestamp
refresh is left alone; no whole-runtime byte-identity claim is made. Raw transcripts,
sandbox denial evidence, identity checks and review receipts are retained privately.
The candidate remains the [same frozen build](../plugin-candidate-2026-10-18.json).

This completes native metadata discovery alongside the earlier Claude command
registration result. It does not test installed/enabled session loading, skill
execution, sibling reads, implicit selection, duplicate skills or upgrades.
[Directory policy and submission questions](../../../docs/plugin-candidate.md)
remain unresolved. No persistent install, package/dependency installation,
submission, publication or policy inquiry occurred.

Repository static and whitespace checks are recorded separately in the summary;
they do not establish agent behavior.
