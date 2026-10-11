# Installed v0.1.9 fresh-session smoke checks

October 11, 2026. These author-created synthetic checks use the actual user-scope
installed core/adoption v0.1.9 packages, without supplied skill copies or paths.
They are narrow native observations, separate from repository static checks.

## Outcomes

- **Codex:** explicit adoption read both installed skills and initialized context
  from configuration (45-second timeout value), distinguishing the historical 15-second claim.
  A separate maintenance task omitted the skill name; it read installed core and
  updated context to 60. Decisions, authority, rationale, proposal status, dataset
  blocker and next step remain. Runtime/deployment stay unverified. Original
  fixture bytes outside permitted docs/instructions, Git index and history pass.
- **Claude with project-only setting sources:** installed user skills were absent
  from the startup catalog. Adoption's `Skill` call returned `Unknown skill`; the
  agent read installed packages by path and initialized source-backed context.
  A separate maintenance session updated to 60 without reading the installed core.
  This is a loading/use limitation in the isolated invocation, **not a passing
  installed-skill maintenance check**. Both original attempts are retained.
- **Additional Claude probes with user,project setting sources:** a tool-free
  startup probe listed both installed skills. A separately frozen follow-up on a
  copied synthetic project successfully invoked `context-docs` without naming it
  in the task prompt and read configuration before updating context to 75.
  Decisions and pending work remain; runtime is unverified. The fixture Git index
  bytes refreshed, while staged contents/history stayed unchanged. This fails the
  strict index-byte gate; it does not replace the original failed use observation.

## Preservation and limits

Original saved studies, repository packages, installed skills and project setup
files retain their hashes. Claude's user settings file is unchanged. Two trust entries for other workspaces (not the fixtures) appeared in Codex
config during the run; their origin is not established and they were left intact. Claude's CLI-managed global state changed; nearby backups differ in a
feature-cache timestamp, but exact original global-state bytes were not recovered.
Neither global file is claimed byte-for-byte preserved. No configuration repair
or skill change is inferred from these observations.

All six native subject/diagnostic executions completed within their caps:
180 seconds each, except the 60-second tool-free catalog probe. Claude per-message fields confirm `claude-opus-5-5`; Codex requested
`gpt-6.1-sol` with medium effort, with responding identity unconfirmed. Automatic
instruction loading lacks independent native startup evidence; self-reports and
reads are insufficient. The maintenance prompts omit the skill name, while the
existing project rule names it: this is a guided smoke check, not general implicit
selection. The settings-isolated CLI runs are not full default interactive UI tests.
Claude boundaries are prompt constraints rather than a general OS sandbox.

[Protocol](protocol.json) retains pre-session criteria, freezes and separately
frozen amendments. [Synthetic inputs](fixtures.json) and [assessment](summary.json)
retain outputs and narrow semantic observations. Raw traces and machine/account
configuration stay local. The [counterpart review](review.json) retains the initial
protocol review and one focused follow-up; Codex resolved the required reporting
corrections by fixture inspection, with no third review or subject rerun. These few
unblinded cases establish no general
reliability, privacy, user-effort savings or causal advantage.
