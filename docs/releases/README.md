# Release history

[Overview](../../README.md) · [User guide](../getting-started.md) · [Changelog](../../CHANGELOG.md)

Use the main guide for current instructions. Release notes and the changelog own
historical changes; the linked preparation, publication and study records retain
their original scope, failures and qualifications. Publication does not upgrade
installed skills or change existing project setups.

For future releases, follow the [release checklist](../../CONTRIBUTING.md#release-checklist),
including an isolated skills.sh refresh and full page-content verification.

## v0.2.x

- **[v0.2.6](v0.2.6.md):**
  [preparation](v0.2.6-validation.json), [publication](v0.2.6-publication.json),
  [installed upgrade](../../.context/events/installed-v026-upgrade-20261019.jsonl),
  [installed smoke](../../evals/installed-skills/2026-10-19-filtering-v026/README.md),
  [qualified candidate smoke](../../evals/content-filtering/smoke-0.2.6-2026-10-19/README.md)
  and [offline controls](../../evals/content-filtering/README.md).
- **[v0.2.5](v0.2.5.md):** [preparation](v0.2.5-validation.json),
  [publication](v0.2.5-publication.json),
  [installed upgrade](../../.context/events/installed-v025-upgrade-20261018.jsonl),
  [installed smoke](../../evals/installed-skills/2026-10-18-concurrency-v025/README.md),
  [candidate smoke](../../evals/concurrency/smoke-0.2.5-2026-10-17/README.md) and
  [offline diagnostic](../../evals/concurrency/offline-2026-10-17/README.md).
- **[v0.2.4](v0.2.4.md):** [preparation](v0.2.4-validation.json),
  [publication](v0.2.4-publication.json)
  ([deployment run](https://github.com/jaredchu/context-docs/actions/runs/39021889853)),
  [installed upgrade](../../.context/events/installed-v024-upgrade-20261017.jsonl),
  [installed smoke](../../evals/installed-skills/2026-10-17-clarity-v024/README.md) and
  [candidate smoke](../../evals/clarity/smoke-0.2.4-2026-10-17/README.md).
- **[v0.2.3](v0.2.3.md):** [preparation](v0.2.3-validation.json),
  [publication](v0.2.3-publication.json),
  [installed smoke](../../evals/installed-skills/2026-10-17-progress-v023/README.md) and
  [candidate smoke](../../evals/progress/smoke-0.2.3-2026-10-17/README.md).
- **[v0.2.2](v0.2.2.md):** [preparation](v0.2.2-validation.json),
  [publication](v0.2.2-publication.json),
  [installed smoke](../../evals/installed-skills/2026-10-17-progress-v022/README.md) and
  [default-adoption checks](../../evals/progress/adoption-default-2026-10-16/README.md).
- **[v0.2.1](v0.2.1.md):** [preparation](v0.2.1-validation.json),
  [publication](v0.2.1-publication.json),
  [installed smoke](../../evals/installed-skills/2026-10-16-progress-v021/README.md),
  [candidate smoke](../../evals/progress/smoke-0.2.1-2026-10-16/README.md) and
  [visual-path review](../../evals/progress/visual-path-review-2026-10-16.md).
- **[v0.2.0](v0.2.0.md):** [preparation](v0.2.0-validation.json),
  [publication](v0.2.0-publication.json),
  [installed smoke](../../evals/installed-skills/2026-10-16-progress/README.md) and
  [candidate smoke](../../evals/progress/smoke-2026-10-16/README.md).

## Earlier releases

- **[v0.1.9](v0.1.9.md):** [preparation](v0.1.9-validation.json),
  [upgrade notes](v0.1.9.md#installation-and-upgrade),
  [website verification](../website-deployment-2026-10-11.json),
  [installed smoke](../../evals/installed-skills/2026-10-11/README.md) and
  [source-selection checks](../../evals/source-selection/README.md).
- **[v0.1.8](v0.1.8.md):** [preparation](v0.1.8-validation.json),
  [local-only follow-up](../../evals/local-only/validation-2026-10-10/README.md) and
  [auto-logging checks](../../evals/event-journal/auto-preference/local-only.md).
- **[v0.1.6](v0.1.6.md), [v0.1.5](v0.1.5.md), [v0.1.4](v0.1.4.md) and
  [v0.1.3](v0.1.3.md):** see their notes and the [changelog](../../CHANGELOG.md)
  for package identities, validation and earlier releases.
- [October 10 website verification](../website-deployment-2026-10-10.json)
  remains a separate historical record.

## Feature boundaries for older installations

Current source includes these features; the linked notes distinguish unpublished
candidates from releases. Older installed packages keep their own guidance until
separately upgraded; use the linked notes for exact scope.
Core and adoption have separate versions, so retain both complete sibling packages.

| Feature | Introduced core / adoption | Bundle notes |
| --- | --- | --- |
| Basic optional JSONL logging | 0.1.3 / 0.1.5 | [v0.1.3](v0.1.3.md) |
| Auto logging outside Git | 0.1.5 / 0.1.6 | [v0.1.5](v0.1.5.md) |
| Local-only context and its auto-logging extension | 0.1.8 / 0.1.9 | [v0.1.8](v0.1.8.md) |
| Explicit source checks when initializing from notes | 0.1.9 / 0.1.9 | [v0.1.9](v0.1.9.md) |
| Markdown progress | 0.2.0 / 0.1.10 | [v0.2.0](v0.2.0.md) |
| Visual paths, dependencies and blockers | 0.2.1 / 0.1.10 | [v0.2.1](v0.2.1.md) |
| Default inline progress adoption | 0.2.2 / 0.1.11 | [v0.2.2](v0.2.2.md) |
| Concise progress views | 0.2.3 / 0.1.12 | [v0.2.3](v0.2.3.md) |
| Clarity preference | 0.2.4 / 0.1.13 | [v0.2.4](v0.2.4.md) |
| Shared-file coordination | 0.2.5 / 0.1.14 | [v0.2.5](v0.2.5.md) |
| Metadata filtering and portable references | 0.2.6 / 0.1.15 | [v0.2.6](v0.2.6.md) |
