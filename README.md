# Context Docs

Keep project context consistent, current and useful across AI sessions.

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

**Latest: concise skill v0.1.1**, tested in 12 trials on three new synthetic
projects of 572–676 words. Original and candidate both passed 6/6 trials under
mechanical checks and author-reviewed semantic criteria. The candidate met the
[predeclared acceptance rule](evals/concise/plan.md) and was adopted.

| Median net Markdown growth | Original v0.1.0 | Concise v0.1.1 |
| --- | ---: | ---: |
| Release guidance | +322.5 words | +184 words |
| Initialization | +211 words | +181 words |
| Repeated maintenance | 0 words | 0 words |

The skill entry point shrank from 645 to 417 words. Initialization was shorter
only on the two-attempt median, not in both attempts. The candidate was slower
(79.8 vs 65.4 seconds median) and used more output tokens. These are small,
author-created cases, not independent evidence of general superiority. Host
global instructions were excluded and recorded inputs checked.
See the [full comparison, variation and limitations](docs/evaluation-2026-09-27-concise.md)
and [reproduction commands](evals/concise/README.md).

The earlier **ordinary instructions versus v0.1.0** study remains below.

**Public custom suite, run with Harbor 0.23.0 on September 27, 2026.** Eight
synthetic tasks × two conditions × three attempts: **48 trials**. Model:
`gpt-6-astra`, low effort; Codex CLI `0.158.0-alpha.2`; unchanged skill v0.1.0.
The repeated-maintenance task has three stages, totaling 60 agent invocations.

Both conditions passed every mechanical check and author-reviewed semantic
criterion. **No correctness advantage was observed; the skill used more time and
tokens in this suite.** This is regression coverage on small fixtures, not proof
of general superiority or an external benchmark score.

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

| Resource metric | Ordinary instructions | With Context Docs |
| --- | ---: | ---: |
| Median agent time per trial | 40.2 s | 45.3 s |
| Uncached input tokens, all trials | 306,778 | 326,395 |
| Output tokens, all trials | 17,436 | 24,525 |

All audit trials preserved project bytes, and all final no-change maintenance
passes left Markdown unchanged. Document growth varied by task: median workflow
additions were +230/+323 words and initialization additions +53/+117 words
(ordinary/skill). These results do not establish general compression or cost savings.

The fixtures start with only 19–87 Markdown words. They are development cases,
not held-out projects, and semantic review was by the authoring assistant rather
than an independent judge. Three repeats do not create three new tasks.

See the [full report and limitations](docs/evaluation-2026-09-27.md),
[reproduction instructions](evals/suite/README.md), and
[machine-readable evidence](evals/results/2026-09-27-harbor/trials.json).
The table is generated from recorded trials and explicit reviews.

The [earlier eight-run private-project pilot](docs/evaluation-2026-09-26.md)
remains documented, including the workflow conflict the skill missed. Passing
the smaller synthetic regression does not erase that result.

## Limits and direction

The skill guides an agent; it cannot guarantee factual correctness, conflict-free
edits or decision preservation. Review consequential changes. It neither captures
every conversation nor grants permission to publish documents or alter systems.

Independent fixtures and downstream reader accuracy remain next. Cloud
retrieval can be an optional integration later; no backend is required or included.

Contributions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).
Licensed under [MIT](LICENSE).
