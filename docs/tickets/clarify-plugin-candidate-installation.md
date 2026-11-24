# Clarify the plugin candidate's installation guidance

## Scope

Clarify the introduction of the [October 18 plugin candidate](../plugin-candidate.md).
Its opening presented standalone v0.2.5 as the everyday install. The
[installation guide](../../README.md#get-started) now points to a later published
bundle. The candidate itself still uses its original versions.

## Done when

- The introduction identifies core 0.2.5 and adoption 0.1.14 as the frozen
  candidate versions and links to current standalone installation guidance.
- The [Codex plugin runtime deferral](../project-decisions.md#codex-plugin-runtime-deferral)
  and the rest of the candidate record are preserved.
- Repository static checks and `git diff --check` pass.

## Status

Closed on November 25, 2026.

## Outcome

The [candidate introduction](../plugin-candidate.md) now dates the frozen bundle
and points to the current standalone install instructions. Static checks and
`git diff --check` passed. The runtime-deferral sentence and the content below
the introduction matched the baseline byte for byte.

## Handoff check

Before the edit, a fresh read-only Codex CLI session started at the
[project entry point](../project-context.md#current-focus), followed its progress
link to this ticket, and recovered the recorded status, exact next action,
completion checks and scope boundary without a follow-up prompt. The coordinator
then made the edit and removed the active progress link. This was one observed
handoff on a documentation task.
