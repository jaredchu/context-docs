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

Make the context entry point discoverable: link it from the project README or
documentation index. For a fresh session, ask the agent to start there and read
the linked context before working. A context file's presence alone does not ensure
that an agent will read it. This routing is already part of the skill's
initialization workflow.

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
- [Quality and fresh-reader study](docs/evaluation-2026-09-27-quality.md)
- [Larger public-source handoff pilot](docs/evaluation-2026-09-27-public.md)
- [README routing and verified reading](docs/evaluation-2026-09-27-routing.md)
- [Decision histories across four maintenance passes](docs/evaluation-2026-09-27-history.md)
- [Public Harbor suite and results](docs/evaluation-2026-09-27.md)
- [Earlier local-project pilot](docs/evaluation-2026-09-26.md)
- [This project's own context](docs/project-context.md)

## Evaluation results

The primary goal is durable project knowledge: retain useful content, keep claims
accurate, and make decisions and procedures consistent across documents and
sessions. **Shorter files or faster editing do not establish that goal.**

The [quality-first study](docs/evaluation-2026-09-27-quality.md) compared two
synthetic projects with scattered, conflicting or absent context. It ran 12
three-stage maintenance trials, followed by 36 fresh-reader sessions: **72 model
sessions and 216 reader answers**, plus reference/no-op controls.

<!-- quality-table:start -->
| Final-artifact measure | Unmaintained | Ordinary maintenance | Context Docs v0.1.1 |
| --- | ---: | ---: | ---: |
| Required knowledge recorded | 12/54 | 54/54 | 54/54 |
| Correct, supported reader answers | 72/72 | 72/72 | 72/72 |
| Correct in both reader sessions | 36/36 | 36/36 | 36/36 |
| Target-claim accuracy | 37.5% | 100.0% | 100.0% |
| Missing required items | 22 | 0 | 0 |
| Incorrect required items | 20 | 0 | 0 |
| Critical document findings | 11 | 0 | 0 |
| Conflicting required items | 0 | 0 | 0 |
<!-- quality-table:end -->

Both maintenance methods improved the stored record. **Context Docs did not
outperform ordinary maintenance on these quality measures.** Readers could inspect
the same small raw evidence set in every arm and all answered correctly, including
with unmaintained docs. This reader ceiling establishes no accuracy advantage or
general equivalence. Both maintenance arms retained all required items through an
evidence update and made no edits in the final no-change pass.

Coverage counts required knowledge captured accurately in maintained Markdown;
raw-file survival alone does not count. Target-claim accuracy excludes missing
items, which are shown separately. Incorrect current claims and unresolved
operative conflicts are separate categories. The two projects contain only
514–656 total input words, are author-created and author-reviewed, and have one
maintenance trial per scenario/arm. This is a reproducible development study,
not an independent benchmark. See the [method, per-project results and limits](docs/evaluation-2026-09-27-quality.md),
[execution commands](evals/quality/README.md), and
[snapshots and scored evidence](evals/results/2026-09-27-quality/README.md).

A [larger public-source pilot](docs/evaluation-2026-09-27-public.md) used pinned
Flask and Click releases containing 143,604 and 102,647 source/test/doc words.
It completed four handoffs and 12 fresh readers: **16 sessions, 72 answers**.
Existing upstream documentation stayed intact; this complements the weak-docs
comparison above.

<!-- public-table:start -->
| Reader outcome | Upstream docs/code | Ordinary handoff | Context Docs v0.1.1 |
| --- | ---: | ---: | ---: |
| Flask | 12/12 | 11/12 | 12/12 |
| Click | 12/12 | 12/12 | 12/12 |
| **Total** | 24/24 | 23/24 | 24/24 |
| Correct in both phrasings | 12/12 | 11/12 | 12/12 |
<!-- public-table:end -->

Both handoff methods covered 24/24 required items. The one ordinary-reader miss
omitted a required cleanup guard. **No skill-specific accuracy advantage is
established:** recorded traces show that none of the eight readers given handoffs
opened their content; they answered from upstream sources. The ordinary handoff
already contained the omitted guard. The protocol also prohibited adding a link
from the upstream README, limiting discovery. This tests handoff availability,
not the effect of confirmed handoff consumption.

Sources were externally authored, but questions and reviews were not independent.
There was one maintenance attempt per method/project, and both projects belong
to the same ecosystem. See [the discovery finding, exact miss and limits](docs/evaluation-2026-09-27-public.md)
and [all outputs and judgments](evals/results/2026-09-27-public/README.md).

A [routing follow-up](docs/evaluation-2026-09-27-routing.md) then reused those
handoffs unchanged, added equivalent orientation links to temporary READMEs,
and compared README-first discovery with explicitly directed reading. It ran
**12 fresh sessions and 72 answers**, using one previously tested phrasing.

<!-- routing-table:start -->
| Reader mode and outcome | Upstream orientation | Ordinary handoff | Context Docs handoff |
| --- | ---: | ---: | ---: |
| README-first discovery: supported answers | 12/12 | 12/12 | 12/12 |
| README-first discovery: full orientation text exposed | 1/2 | 2/2 | 2/2 |
| Directed reading: supported answers | 12/12 | 12/12 | 12/12 |
| Directed reading: full orientation text exposed | 2/2 | 2/2 | 2/2 |
<!-- routing-table:end -->

All eight handoff readers received the complete document before answer-writing,
verified from model-visible tool output. All 12 readers saw the complete README.
**Accuracy remains tied:** the original sources also support every answer. This
checks reading under the new routing/instructions; it does not establish a skill
advantage, unguided discovery or equivalence. The earlier omitted cleanup guard
is present in the repeated answers. See [the unchanged criteria, exposure method
and limitations](docs/evaluation-2026-09-27-routing.md) and
[reproducible evidence](evals/results/2026-09-27-routing/README.md).

A [decision-history follow-up](docs/evaluation-2026-09-27-history.md) replayed two
externally authored Python policy histories through four maintenance passes:
**28 model sessions and 96 reader answers**. It tests evolving requirements,
authority, rationale and authentic source contradictions; both histories come
from one project and the questions/review remain author-created.

<!-- history-table:start -->
| Outcome | Unmaintained | Ordinary maintenance | Context Docs v0.1.1 |
| --- | ---: | ---: | ---: |
| Required knowledge in final context | 0/16 | 16/16 | 16/16 |
| Required knowledge across all stages | 0/63 | 63/63 | 63/63 |
| Correct, supported reader answers | 32/32 | 32/32 | 32/32 |
| Correct in both reader sessions | 16/16 | 16/16 | 16/16 |
| Readers exposed to all Markdown | 4/4 | 4/4 | 4/4 |
| Critical document findings across stages | 0 | 0 | 0 |
<!-- history-table:end -->

Both methods retained every assessed item and made no Markdown changes in the
final no-new-evidence pass. **Reader accuracy tied**, including readers of raw
history alone; those original PEPs remain accessible in every arm. Zero in the
unmaintained column measures absent context summaries, not absent source facts.
One skill session briefly wrote a backup outside the allowed directories, then
corrected it; the project-file grader did not catch that. See the
[scope finding and limits](docs/evaluation-2026-09-27-history.md) and
[all artifacts and explicit judgments](evals/results/2026-09-27-history/README.md).

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

Next evaluations should prioritize independently contributed histories from other
projects and condition-blind review, with verified context reading. Current results
do not establish a skill-specific correctness advantage. Cloud
retrieval can be an optional integration later; no backend is required or included.

Contributions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md).
Licensed under [MIT](LICENSE).
