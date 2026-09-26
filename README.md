# Context Docs

Keep project context consistent, current and useful across AI sessions.

Context Docs is an open-source convention and reusable agent skill for maintaining
Markdown project knowledge. It adapts to existing documentation, preserves
decisions and evidence, and keeps current context from becoming a session diary.

**Status: experimental, v0.1.0.** The first version is an instruction-only skill.
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
- [This project's own context](docs/project-context.md)

## Limits and direction

The skill guides an agent; it cannot guarantee factual correctness, conflict-free
edits or decision preservation. Review consequential changes. It neither captures
every conversation nor grants permission to publish documents or alter systems.

The next step is to evaluate the workflow on varied project layouts and measure
accuracy, information preservation and maintenance effort. Cloud retrieval can
be an optional integration later. No retrieval backend is required or included.

Contributions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).
Licensed under [MIT](LICENSE).
