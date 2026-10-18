# Isolated plugin discovery check

October 18, 2026. **Partial result: Claude Code registers both candidate skills;
Codex loading remains unverified because its isolated initialization fails.**
No model request or skill behavior trial runs.

The [candidate](../../../docs/plugin-candidate.md) is the unchanged 21-file ZIP
with SHA-256 `601ff1f155b78c14cdb3c0e49b777fecdef1b3f2061e51714ef14efa1ae0fbee`.
Separate scratch extractions for both clients match every candidate file hash;
all 21 relative links/anchors resolve in each extraction. The
[summary](summary.json) records client versions, registered metadata and limits.

| Client | Native observation | Limit |
| --- | --- | --- |
| Claude Code 2.1.302 | A session-only `--plugin-dir` plus stream-JSON control initialization registers `context-docs:context-docs` and `context-docs:adopt-context-docs`, with their descriptions and aliases | No user/model prompt, invocation, implicit selection or adoption |
| Codex CLI 0.163.0-alpha.10.2 | First stdio app-server attempt fails initializing its normal SQLite state; one retry with process-local scratch `sqlite_home`/`log_dir` still exits `Operation not permitted` | Neither attempt reaches the requested native plugin discovery responses; the second blocked operation is unidentified |

Codex also reports that the probe's `features.remote_plugins` override is
unrecognized and ignored. That is a harness qualification, not a candidate
finding; the record makes no claim that this override disabled remote catalogs.
Both failed attempts remain retained, and no further retry or workaround runs.

Claude uses a new private configuration directory with hooks, memory, MCP and
Chrome disabled. The scratch Codex project has one private local marketplace
catalog; no catalog is added to the real setup. An OS write sandbox permits
client writes only under the new private evidence root except `/dev/null`.
Neither `HOME` nor `CODEX_HOME` is reassigned. No auth file is copied, and no
native `thread/start`, `turn/start` or Claude user prompt is sent.

This establishes Claude command registration only. It does not establish full
plugin execution, Codex compatibility, sibling reads during adoption, safe
duplicate standalone installs, upgrade behavior or directory acceptance.
The original [candidate checks and Opus review](../plugin-candidate-2026-10-18.json)
remain unchanged; the Claude policy concern remains unresolved. These probes use
native client code, without a Codex or Claude model evaluation/review.

Raw protocol receipts, stderr, the temporary catalog and scratch extractions are
retained in a new durable private root. Installed skills, setup preferences and
saved studies are preserved. Nothing is submitted or published.
