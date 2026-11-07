# Stale dependency note check

November 7, 2026. **Pass in one synthetic case; no skill change needed.**
A normal adopted-project refresh corrected a stale dependency note while keeping
historical rationale and an unresolved verification blocker. The reported user
miss was not reproduced in this case.

## Method

The [fixture](fixture/README.md) contains working standard-library cache code,
an empty runtime dependency list, an approved Redis-removal decision and a stale
context file still requiring Redis and its server. The decision explains both
the former cross-worker rationale and the replacement's offline, single-process
purpose. A missing restart acceptance fixture remains an explicit blocker.

The coordinator ran `python3 -m unittest discover -s tests` before the model
session; its two unit checks passed. The [receipt](fixture/checks/unit.txt) makes
clear that restart and end-to-end checks did not run. This verifies the small
fixture, not Context Docs' effectiveness.

The [protocol](protocol.json) froze the generic refresh prompt, six criteria,
source/fixture hashes, model flags and runner/helper hashes before execution.
The prompt did not name Redis, identify the stale note or explicitly invoke a
skill. Loaded project instructions direct the agent to read the copied core
skill and consult current sources. This is an ordinary explicit refresh under
an existing rule, not a test of spontaneous maintenance after a code edit.

The subject used unreleased source core **0.2.7**, not the published or installed
core 0.2.6 package. Claude Code **2.1.319** requested and reported **Opus 5.5**,
configured **High**, through existing first-party subscription authentication.
Effective effort was not independently exposed. The run had a 180-second bound,
no retries, no session persistence, auto memory off, and guarded file tools only.
Browser, MCP and delegation were disabled. The file-tool guard permitted edits
only to `docs/current.md`.

## Result and evidence

Codex authored and scored the case against the frozen criteria. All six pass:

- Current backend and dependencies match the code and manifest.
- Current setup and next steps no longer require provisioning Redis.
- Replacement rationale and superseded cross-worker rationale remain.
- The missing restart fixture and verification blocker remain.
- Two passing unit checks are reported with their limits; no new tests are claimed.
- Only the context file changed; all other inventoried fixture files and the source skill
  remained byte-identical.

The [after-context](after.txt), exact [subject report](refresh.txt) and
[reviewed summary](summary.json) retain the result and separate semantic review
from hash checks. Ten file-tool calls completed with no denials or retries.
Instruction-event hashes match the fixture's CLAUDE.md and imported AGENTS.md;
both loaded before the first tool call. Raw streams, hooks and the runner remain
in local task evidence; the protocol and summary retain their hashes.

A separate fresh Opus 5.5 session, configured High, performed a bounded read-only
[report review](review.txt) and found no material issues. Minor guard wording and
source-hash evidence clarifications followed; no subject session was rerun.
The reviewer inspected the supplied artifacts, not raw logs or the runner, and
did not execute commands or recompute hashes. This adds no independent case
selection or grading.

## Limits

This is one coordinator-authored synthetic case, not a reproduction of a private
participant project or a comparison with ordinary maintenance. It adds no
cross-client, fresh-installation, spontaneous-maintenance or general reliability
claim. File-tool hooks are not an OS sandbox; client bookkeeping outside the
fixture is not inventoried. No original participant trace was supplied, so the
cause of that reported miss remains unknown. Passing this case does not justify
a speculative instruction change or establish effort savings.
