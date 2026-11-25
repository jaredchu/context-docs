# Prepare the v0.2.9 prerelease

## Scope

Prepare an experimental bundle of core 0.2.9 and adoption 0.1.17 for the
[JSONL retirement](../project-decisions.md#retire-optional-jsonl-event-capture).

## Done when

- Disposable project installs upgrade from v0.2.8 in the Codex and Claude Code
  layouts with the retired files absent and existing JSONL and context preserved.
- Release notes describe the evidence, upgrade steps and verification limits.
- Repository checks and independent review pass for the selected source.

## Status

Completed 2026-11-25. Both disposable layouts passed the clean replacement
check. Repository static checks and independent release-preparation review
passed. The [release notes](../releases/v0.2.9.md) record the package and
verification limits. The checked package files come from `45557cf`.

## Handoff

The [publication ticket](publish-v029-prerelease.md) records the remaining work.
