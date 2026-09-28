# Journal read-gating follow-up — 2026-09-28

**Codex and Claude, when reading the candidate instructions, skipped journal
access on no-change maintenance while retaining capture and investigation.**
The unreleased core 0.1.4 changes the read decision in SKILL.md and the journal
guide; the helper, schema and adoption 0.1.5 are unchanged.

The [prior released-package evaluation](../2026-09-28-global-journal/README.md)
found both clients rereading history on repeat maintenance. This follow-up uses
the same task prompts, without a reminder to skip logs. Candidate packages are
installed in isolated synthetic projects; actual global installations remain at
released core 0.1.3/adoption 0.1.5. Installation/selection conditions differ from
the baseline, so this is a focused behavioral check, not a causal performance study.

| Condition | Sessions | Observed result |
| --- | --- | --- |
| Initial Codex | 3 | One accurate capture; repeat reads only README, current notes and candidate SKILL.md; audit reads history and preserves bytes. |
| Initial Claude | 3 | Guard rejected the candidate helper because `/var` and resolved `/private/var` paths differed. No event; downstream stages do not validate a successful capture. |
| Claude path follow-up | 3 | Capture succeeds. Repeat invokes released global skill, then lists and reads history. Candidate exposure failed; do not count this as a pass for the new guidance. |
| Claude direct-read follow-up | 3 | With Skill/slash lookup disabled, reads the candidate file directly. One accurate capture; repeat reads only current notes, README and candidate SKILL.md; audit reads history and preserves bytes. |

All twelve sessions are retained in [per-stage results and hashes](summary.json).
The exact candidate instruction/helper hashes are identical across conditions.
The passing no-change traces are inspectable for
[Codex](initial/codex-repeat-operations.json) and
[Claude](direct-read/claude-repeat-operations.json): no journal listing, search,
content read, append or project write. Capture records the synthetic probe's
fixed output (batch limit 4, queue overflow, exit 7); fresh readers identify that
it does not exercise a real queue and that production remains untested.

These results support the narrow read-gating change, not reliable native selection
or unrestricted operation. Claude's guard denials and leftover temporary payload
remain. Its final audit calls the input payload a field-for-field match to the
stored event, overlooking helper-generated metadata; the requested historical
facts are correct, but that extra claim is too broad. Earlier failures remain
separate evidence and were not silently rescored or combined into a clean run.

The [final protocol](direct-read/protocol.md), [candidate source snapshot](source/skills/context-docs/SKILL.md),
requests, final responses and normalized operation traces are included. Trace
normalization replaces known synthetic project roots with `<project>`; original
stream hashes are retained. Raw streams remain in ignored `.local/read-gating-20260928*`
directories because host/global instructions may contain private context.
The [runner](../../event-journal/read-gating/run.py) freezes its packages and
conditions before execution. Candidate paths are now resolved before the guard
comparison; absolute and relative helper commands passed preflight in both fixtures.

Separate mechanical validation: both skill metadata validators, 13 repository
checker regressions, one guard regression containing six boundary assertions,
and repository packaging/link/version checks passed. No logging-cost reduction,
real-project benefit or general reliability is established by these small tests.
