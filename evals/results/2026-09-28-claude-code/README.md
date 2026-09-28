# Native Claude Code attempt — September 28, 2026

**Blocked by authentication. No completed model session or native skill behavior
was observed.** The first of six planned sessions returned:

```text
Failed to authenticate: OAuth session expired and could not be refreshed
```

The repaired harness stopped immediately and retained the failed attempt. Five
sessions were not attempted. This is an execution failure, not evidence that the
skill failed its behavioral criteria. No semantic review was performed.

## Frozen setup

- Harness commit: `bedc176`; protocol committed before execution in `336a414`.
- Client: Claude Code `2.1.234`; requested and initialization-reported model:
  `claude-opus-5`. Authentication failed before any model work.
- Four synthetic trajectories, six planned sessions, one attempt per session.
- Core skill `0.1.1`, adoption skill `0.1.3`, installed in each project's
  `.claude/skills/` and recorded by hash.
- Fixtures ran in a temporary directory outside the source repository. Neither
  user-level instruction file checked by the protocol was present.
- Local execution with project settings, strict MCP configuration, fixed tool
  permission rules and a ten-minute session timeout. This is not a container or
  a network sandbox, and does not establish fully isolated execution.
- Project installation, final-message auditing and the unnamed-selection gate
  were retained as implementation choices. A discovery miss would fail that
  trajectory without by itself establishing a skill-content defect.

## Evidence

- [Frozen protocol and initial hashes](protocol.json)
- [Retained attempt, checks and project snapshots](trials.json)
- [Execution stream excerpt](execution-stream.jsonl)
- [Summary](summary.json) and [generated table](table.md)
- [Provenance and artifact normalization](provenance.json)

The CLI exited with code 1 after 1.8 seconds, with no skill invocation and no
project changes. Its reported cost was zero. The two failed mechanical checks are
`documentation_changed` and `no_execution_error`; neither establishes a model
behavioral failure because authentication prevented the requested work.

All attempt records are retained. Public trial paths replace the temporary root
with `/fixture`; the stream excerpt omits host paths, session identifiers and
local customization metadata. The original local stream is retained outside the
repository, with its SHA-256 in provenance. The protocol is byte-identical to the
file committed before execution.

## Validation and next step

The repaired harness passes 34 original self-test assertions and ten regression
tests covering protocol/model drift, changed initial inputs, complete-tree byte
identity, installed references and execution failures. The repository's other
static checks and report regeneration also pass. These are separate from the
blocked native evaluation; installable skill contents were unchanged.

Refresh Claude Code CLI authentication interactively, then build and freeze a new
destination using the [harness instructions](../../claude-code/README.md). Preserve
this blocked attempt. Complete all six sessions and their explicit semantic
reviews before making a native-behavior claim. This small, author-reviewed smoke
test cannot establish general reliability even if all sessions pass.
