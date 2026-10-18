# Codex test-route diagnostic

October 18, 2026. **The nested sandbox failure is reproduced; active plugin
registration remains unresolved.** No model requests or runtime reruns occur.
The [protocol](protocol.json) bounds this diagnostic to 15 minutes. The frozen
candidate and all [earlier runtime results](../plugin-runtime-2026-10-18/README.md)
remain unchanged. Sol runs and checks the controls; no counterpart review occurs.

## File access

The same synthetic command ([path-normalized source](control.py)) runs through native `command/exec`
under the same outer macOS sandbox with two policies:

| Native command policy | Result |
| --- | --- |
| workspaceWrite | Exit 71: `sandbox-exec: sandbox_apply: Operation not permitted` |
| externalSandbox, restricted network | Exit 0; all boundary controls pass |

A direct outer-sandbox control also passes. The command reads the fictional
README and writes an owned scratch file. Attempts to open the frozen package
and an owned sibling sentinel for writing are denied; reading the real project
is also denied. No real setup or study is used as a write target. The command,
outputs and normalized arguments are in [controls.json](controls.json).

This reproduces the reported nesting error without a model. `externalSandbox`
uses the already enforced outer profile rather than applying a second sandbox.
No filesystem or network permission is added. The existing exact runtime identity
exception is unchanged; identity bytes and checked stat stay equal. This is one
verified non-model command route, not validation of every model tool or plugin.

Two diagnostic CLI errors remain recorded: an obsolete `sandbox macos` syntax
before the freeze, and a later `codex sandbox` invocation requiring an explicit
permission profile. Neither CLI error establishes nesting behavior; the native
command/exec comparison above does. No permission-profile workaround is attempted.

## Skill selection and stop point

In the same non-model session, `plugin/read` returns both namespaced candidate
skills. The plugin summary still says **installed=false, enabled=false**.
`skills/list` returns 11 active entries, none belonging to Context Docs, and no
reported entry errors. Standalone skill reads remain intentionally denied.

The earlier explicit skill input did not establish activation. Missing active
entries are consistent with the uninstalled/disabled state, without proving
all internal selector behavior. No activation, cache seeding, additional skill
root or standalone substitution is attempted. The optional offline prompt render
is skipped because the active catalog already exposes the gap.

[Official packaging guidance](https://developers.openai.com/plugins/build/plugins)
distinguishes discoverable marketplace entries, enablement and installed cache
copies. It does not establish a session-only no-install route for this candidate.
The remaining step is a supported temporary activation route or a separately
approved installation boundary. A model rerun remains outside this diagnostic.
Do not expand permissions or label direct packaged-skill loading as proof of
installed-plugin execution.

## Preservation and qualifications

Network is denied throughout native controls. Only initialize, plugin/read,
skills/list and two command/exec requests occur; there is no thread/turn start,
model request, install/enable operation, real config change or home reassignment.
The old boundary is retained in a new private root; writes to the extracted
candidate are denied. All 21 extracted files equal the frozen ZIP. Existing
runtime identity/configuration are still shared, so this is not a clean profile.
Blocked optional catalog warmers and PATH-alias warnings are retained privately.

Installed skills, setup preferences, earlier studies and raw evidence remain
unchanged. This separate record, current status summaries and one new journal
event retain the new findings. Raw transcripts, controls and receipts remain
private; [summary.json](summary.json) pins their hashes and preservation checks.
No product fix, model review, persistent installation, submission or publication
occurs. Repository static checks are reported separately from these controls.
