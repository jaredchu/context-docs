# Context Docs

Preserve project knowledge and maintain accurate, consistent documentation across AI sessions.

Context Docs is an open-source convention and reusable agent skill for maintaining
Markdown project knowledge. It adapts to existing documentation, preserves
decisions and evidence, and keeps current context from becoming a session diary.

**Status: experimental, skill v0.1.1.** The package contains instructions only.
It runs when an agent uses it; there is no background service, automatic scheduler,
cloud account or runtime dependency. Git remains available for history and review.

## Use it

With the skill installed, ask your agent:

```text
Use $context-docs to audit this project's context documents. Report the gaps
without editing files.
```

```text
Use $context-docs to update project context from the work we just completed.
Preserve the existing layout, approved decisions, and unresolved blockers.
```

```text
Use $context-docs to establish a minimal context entry point for this project.
Use existing docs and code as evidence; mark anything you cannot verify.
```

The workflow reads existing context, checks relevant evidence, updates canonical
sections, consolidates duplication, and reviews the resulting diff and links.
An audit stays read-only. Maintenance produces ordinary, reviewable file edits.

## Install in Codex

Ask the built-in installer:

```text
Use $skill-installer to install the context-docs skill from
https://github.com/jaredchu/context-docs/tree/main/skills/context-docs
```

Or clone this repository and copy `skills/context-docs` into your project's
`.agents/skills/` directory. For personal use across repositories, copy it into
`~/.agents/skills/`. Check for an existing `context-docs` folder first and review
changes when upgrading. Copy the whole skill folder, including references and
assets. Codex normally detects changes automatically; restart if it does not.
See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills).

Other agents can use the same instructions when they support `SKILL.md` folders,
or read the [standard](skills/context-docs/references/standard.md) directly.
Client-specific installation and behavior outside Codex have not been tested.

## What is standardized?

| Concern | Convention |
| --- | --- |
| Structure | Shared document roles, mapped to existing files |
| Truth | Distinguish observations, approved decisions, proposals and unknowns |
| Maintenance | Refresh current state after meaningful work; preserve evidence |
| Growth | Consolidate repetition, link to details, retain useful history |
| Portability | Keep canonical content in readable Markdown with source links |

A project with `context.md` and one with `docs/project-context.md` can follow the
same method. No forced directory migration or universal document-size limit.

## Contents

- [Reusable skill](skills/context-docs/SKILL.md)
- [Context standard](skills/context-docs/references/standard.md)
- [Optional context template](skills/context-docs/assets/project-context.md)
- [Optional decision template](skills/context-docs/assets/decision-record.md)
- [Before-and-after example](examples/maintenance.md)
- [Behavioral evaluation scenarios](evals/README.md)
- [Public Harbor suite and results](docs/evaluation-2026-09-27.md)
- [Earlier local-project pilot](docs/evaluation-2026-09-26.md)
- [This project's own context](docs/project-context.md)

## Evaluation results

The primary goal is durable project knowledge: retain useful content, keep claims
accurate, and make decisions and procedures consistent across documents and
sessions. **Shorter files or faster editing do not establish that goal.**

Our next evaluation compares the same project with scattered, stale or missing
context, after ordinary documentation maintenance, and after Context Docs.
Fresh readers will answer the same project questions. Primary measures are
information retention, factual accuracy, cross-document consistency, correct
handling of approvals/unknowns, and agreement with supported answers across
sessions. See the [quality-first protocol](evals/quality-protocol.md).
**That comparison has not run yet.**

Existing studies provide maintenance regression coverage:

- **48 trials, v0.1.0 versus ordinary instructions:** both passed 24/24 under
  mechanical checks and author-reviewed semantic criteria. No correctness
  advantage was observed on these small fixtures. All audits preserved project
  bytes and final no-change passes preserved Markdown.
- **12 trials, v0.1.0 versus concise v0.1.1:** both passed 6/6. The candidate met
  its frozen preservation/concision rule and was adopted. This was a prompt
  refinement test, not evidence of better knowledge retention or reader answers.
- The [earlier local-project pilot](docs/evaluation-2026-09-26.md) includes a
  workflow contradiction the skill missed. Passing synthetic cases does not
  erase that miss.

<!-- evaluation-table:start -->
| Task | Ordinary instructions | With Context Docs |
| --- | ---: | ---: |
| stale-config | 3/3 | 3/3 |
| workflow-conflict | 3/3 | 3/3 |
| decision-status | 3/3 | 3/3 |
| uncommitted-work | 3/3 | 3/3 |
| links-and-fences | 3/3 | 3/3 |
| audit-only | 3/3 | 3/3 |
| initialize | 3/3 | 3/3 |
| repeated-maintenance | 3/3 | 3/3 |
| **Total trials** | **24/24** | **24/24** |
<!-- evaluation-table:end -->

The 48-trial table is generated from recorded trials and explicit reviews. Its
fixtures contain only 19–87 Markdown words; the follow-up fixtures contain
572–676. Both studies use author-created cases and author review, not independent
held-out projects. Global instructions were excluded and recorded inputs checked.

Full results retain all observations, including document growth, slower runs and
resource overhead. These are secondary diagnostics, not the product's success
criteria: [48-trial report](docs/evaluation-2026-09-27.md),
[v0.1.1 comparison](docs/evaluation-2026-09-27-concise.md),
[reproduction commands](evals/suite/README.md), and
[machine-readable results](evals/results/2026-09-27-harbor/trials.json).

## Limits and direction

The skill guides an agent; it cannot guarantee factual correctness, conflict-free
edits or decision preservation. Review consequential changes. It neither captures
every conversation nor grants permission to publish documents or alter systems.

Document quality and downstream reader accuracy on weak-documentation baselines
remain next. Cloud
retrieval can be an optional integration later; no backend is required or included.

Contributions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).
Licensed under [MIT](LICENSE).
