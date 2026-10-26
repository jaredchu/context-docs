# Installation and usage

[Back to Context Docs](../README.md) · [Evaluation evidence](evaluation-results.md) · [Release history](releases/README.md)

Install both skills once, adopt them in a project, and let its maintenance rule keep
context current after meaningful work. No background service is installed.

## Install in Codex

Ask the built-in installer:

```text
Use $skill-installer to install both skills from jaredchu/context-docs:
- skills/context-docs
- skills/adopt-context-docs
Install them together in ~/.agents/skills/.
Preserve existing installations and local customizations; report version
mismatches before upgrading.
```

The adoption skill requires `context-docs` as a sibling folder. It is a small
setup wrapper, not a standalone replacement for the core skill. The core skill
can be installed and used by itself.

Alternatively, clone this repository and copy both complete folders from `skills/`
into `~/.agents/skills/`. For a repository-scoped installation, copy both into
`.agents/skills/` at the project root instead. Use one scope to avoid duplicate
skill entries. Check existing folders and review changes before upgrading; retain
references, assets, metadata and licenses. Codex normally detects changes
automatically; restart if they do not appear.
See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills).

## Install in Claude Code

Copy both folders into a skills directory Claude Code reads: `~/.claude/skills/`
for every project, or `.claude/skills/` inside one repository. Use one scope.
If either skill is already installed, [review the upgrade guidance](#upgrading)
before copying files. For a first installation:

```sh
git clone https://github.com/jaredchu/context-docs.git
cd context-docs
mkdir -p ~/.claude/skills
cp -r skills/context-docs skills/adopt-context-docs ~/.claude/skills/
```

Keep both folders side by side: the adoption skill reads its sibling core skill.
Invoke a skill as `/context-docs` or `/adopt-context-docs`, or describe the task
and let Claude select it. The packaged `agents/openai.yaml` is Codex metadata and
is ignored here.

Direct `AGENTS.md` loading requires Claude Code v2.1.277 or later with its built-in
`agents-md` plugin enabled. By default, it loads `AGENTS.md` only when no
`CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` exists in the working directory
or its ancestors; user-level `~/.claude/CLAUDE.md` and managed instructions do not
disable that fallback. The Project instructions setting can instead load both
file types, only Claude files, or only managed instructions at launch. Older or
otherwise unsupported sessions can import `AGENTS.md` from `CLAUDE.md`.

Adoption targets the instructions actually loaded in the session. Confirm
the result: the rule should be in a loaded file, or included through that file's
supported import. Check `/context` and the Project instructions setting rather
than inferring loading solely from filenames. See the
[Claude Code skill](https://code.claude.com/docs/en/skills) and
[memory](https://code.claude.com/docs/en/memory) documentation.

Other agents can use the same instructions when they support `SKILL.md` folders,
or read the [standard](../skills/context-docs/references/standard.md) directly.
Behavior on clients other than Codex and Claude Code has not been evaluated.

## Use it

With both skills installed, adopt a new or existing project with:

| Codex | Claude Code |
| --- | --- |
| `$adopt-context-docs` | `/adopt-context-docs` |

This applies the core method and adds or merges a maintenance rule in the
instruction file the project's agent actually loads, such as `AGENTS.md` or
`CLAUDE.md`. After checking the setup, it records a small marker beside that rule:

```text
Method: context-docs
Adopted: YYYY-MM-DD
Entry point: path/to/context.md
```

New maintenance sections preferably use a `Context maintenance` heading, then the
marker, then maintenance instructions. Existing equivalent layouts are preserved.

The path reflects the project's actual entry point. Repeat runs preserve the
original adoption date and reuse equivalent guidance. When retrofitting a marker,
an undocumented original adoption date stays `unknown`. Audit-only runs do not
write markers. The marker records workflow adoption; it is not an accuracy or
freshness certificate, and its absence alone does not prove non-adoption.

After adoption, a loaded project maintenance rule tells the agent to maintain
context after meaningful changes during normal work. You do not need to mention
Context Docs in every prompt. Check that the agent loads the rule and review its
edits; skill installation alone does not establish ongoing project maintenance.

You can also ask directly, for example if an update was missed:

```text
Update this project's context from the work we just completed.
Preserve the existing layout, approved decisions, and unresolved blockers.
```

Explicit skill prompts are optional ways to request a focused audit, update or
initialization. The following examples use Codex syntax; replace `$context-docs`
with `/context-docs` for Claude Code:

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

Select information by audience and destination, using the public, private-team
and personal-project examples in the
[standard](../skills/context-docs/references/standard.md#audience-and-destination).

The workflow reads existing context, checks relevant evidence, updates canonical
sections, consolidates duplication, and reviews the resulting diff and links.
An audit stays read-only. Maintenance produces ordinary, reviewable file edits.

### Refresh after outside work

When context has drifted after work in another session or tool, ask the existing
skill to reconcile it with current project evidence:

```text
Use $context-docs to refresh this project's context against current project evidence.
```

Name relevant changed files, reports or a known revision range when useful. The
existing maintenance guidance covers supported updates, safe consolidation,
preserving decisions and unresolved work, and leaving files unchanged when no
durable update is needed. Review the resulting diff and verification limits.
Refresh here means maintaining the project's documents during the active session.

The [focused v0.2.6 baseline](../evals/refresh/baseline-0.2.6-2026-10-26/README.md)
repaired synthetic accumulated drift and made no changes on a second fresh run.
That case supported documenting the invocation without changing the skill or its
version. It used an explicit skill path on one client; it does not establish
automatic selection or general reliability. Existing adoption rules and storage
choices still apply; no skill upgrade or re-adoption is needed for this prompt.

### Sharing and portable references

Before saving context or an enabled journal event, the agent reviews its additions
for the intended readers. Shared project context should omit incidental usernames,
private evidence locations, account identifiers and personal installation state.
Summarize the relevant tool finding instead of copying raw output. Keep secrets
out of both shared and local context. An enabled journal can be tracked and shared;
logging does not make its contents private.

Use repository-relative links to project files. For privately retained evidence,
cite a suitable public summary, stable evidence ID or hash and state access limits;
a hash alone does not let another reader inspect the evidence. Useful machine
paths can remain in appropriate local notes. If paths or environment versions
explain a failure, retain the necessary conditions and relationships in an
authorized public derivative, with provenance and limits. Preserve originals.

Record meaningful outcomes once and link to their canonical detail. Avoid repeated
installation/preservation assurances unless they establish a relevant condition
or requested check. Keep decisions, rationale, uncertainty, blockers and the next
action clear. This is guidance for selecting new content, not automatic redaction,
a guarantee against disclosure, or permission to rewrite history or move records.
Existing layouts, storage choices and logging settings remain in effect.

In the [v0.2.6 candidate smoke](../evals/content-filtering/smoke-0.2.6-2026-10-19/README.md),
both clients pass visible saved-Markdown checks. Claude could not locate an
unlinked private operator note with its restricted tools; filtering incoming
content from that note remains untested. These guided checks establish no general
privacy guarantee or automatic everyday application.

Make shared context discoverable: link it from the project README or
documentation index. For a fresh session, ask the agent to start there and read
the linked context before working. A context file's presence alone does not ensure
that an agent will read it. This routing is already part of the skill's
initialization workflow.

### Clarity during context updates

Prefer clear, direct sentences and consistent project terms within authorized edits. Preserve
conditions, uncertainty, rationale and evidence; keep existing layouts and unrelated
owner text. No ASD-STE100 compliance or special invocation is required.

The [qualified clarity checks](../evals/clarity/smoke-0.2.4-2026-10-17/README.md)
retain Claude's unsupported pronoun in its chat report, with saved Markdown
unaffected. They do not establish comprehension gains or automatic everyday application.

### When sessions share a context file

When multiple agents or sessions work on the same context file concurrently,
coordinate one writer at a time for that file. Other participants pass their
findings to the writer. Prefer narrow edits. If an edit conflicts or reports stale text,
reread the current file and reconcile everyone's changes before retrying;
do not replace newer contributions with an old snapshot.

Installing the skill in both Codex and Claude Code does not coordinate sessions.
Concurrent sessions in a shared checkout can still target the same context file.
When splitting work across models, assign context maintenance to one participant
before parallel work begins; others return context findings instead of editing
that file independently. Change writers through an explicit handoff.

This rule guides coordination and provides no file locking or automatic merge
guarantee. Existing project setups stay unchanged unless separately updated.
See the [core rule](../skills/context-docs/SKILL.md#make-the-smallest-useful-update).

The [qualified candidate smoke](../evals/concurrency/smoke-0.2.5-2026-10-17/README.md)
retains Claude's second mismatch without a reread and Codex's corrected checking error.
These guided cases do not test simultaneous writers or establish general
conflict prevention. Publication alone does not upgrade installed skills.

### Progress in Markdown

Show a clear visual path rather than a flat status table alone. During adoption,
start a small inline path by default when the documented goal and supported work
make one useful. Group ordinary status sentences in place,
keeping details authoritative and linked to evidence. Existing lists, tables,
diagrams and designated progress sections/files keep their format and location;
do not add a duplicate. When the goal or supporting work is too sparse, skip the
new view rather than creating empty scaffolding. Explicit requests to omit the
view or use another destination take precedence. An explicit adoption run may
add a missing supported view to an already-adopted project, preserving its rule
and original marker/date; subsequent unchanged repeats should make no edits.
Installation or upgrade alone does not change project setups.

Favor a concise overview: goal, meaningful outcomes, dependencies/blockers and next action.
Link detailed test/review evidence instead of repeating its chronology. Keep
decisions, rationale, approval boundaries and relevant qualifications visible;
preserve existing formats and unique information. Detail can grow with project
complexity or an explicit request; there is no fixed length limit or new evidence store.
The [qualified concise-progress smoke](../evals/progress/smoke-0.2.3-2026-10-17/README.md) retains its scope failure:
both clients pass progress checks, but Codex creates/removes an extra temporary
hash file outside its allowed paths. Earlier installed packages keep their own
guidance until separately upgraded; [release history](releases/README.md#feature-boundaries-for-older-installations)
records feature boundaries and the original validation limits.

Once a view exists, the loaded maintenance rule directs the agent to update it
after meaningful changes during everyday work; you need not ask each time.
This is session-time guidance, not background tracking. Review the resulting edits.

You can request a view directly, or ask to reshape an existing view, using the
same skill syntax as other requests:

```text
Use $context-docs to visualize this project's progress in Markdown.
Show its documented goal and completion conditions, milestones when available,
completed, active, blocked and proposed work, and the next action.
Use a compact tree, arrow path or nested checklist. Show dependencies and
put each blocker beside the affected work, with its prerequisite and next step.
Link items to evidence, distinguish useful learning from completed outcomes,
and mark unknowns. Preserve existing layouts and local-only storage boundaries.
```

The progress guidance asks for a small visual path in existing context, or a
linked Markdown file if requested or easier to navigate. Branch parallel
conditions; show ordering only when supported. Keep proposals outside required
completion conditions unless approved there. Link items and relationships to
their sources; keys in a fenced text diagram need clickable Markdown links
outside the fence. Keep unknown paths unknown. A table can support the visual;
the same authoritative documents remain the source of truth.
It directs the agent to refresh an existing view during authorized context
maintenance, without a special invocation for each update. Audits are instructed
to remain read-only. Review the edits and source links.

For a historical question, ask which attempts produced new results or useful
findings. Relevant Git history, retained dated attempt notes or an existing
journal can support that comparison. Reading retained journal records for a
historical question does not enable capture or change an explicit off setting.
Repeated activity may suggest a stall, but does not prove a loop.
Without suitable history, repetition remains unknown; this does not enable
logging. The guidance forbids inventing completion percentages, missing goals
or live activity; the [validation boundary](../evals/progress/README.md#validation-boundary)
distinguishes the documented workflow from actual behavioral evidence.
See the [synthetic example](../examples/progress.md) and the packaged
[progress guidance](../skills/context-docs/references/progress.md).

### Starting from earlier notes

During initialization, the agent should check current implementation or configuration claims against
relevant project sources before carrying them into the new context. It should preserve approved
decisions, their rationale and unfinished work. For example, old notes may report
a 10-second timeout while configuration sets 20; record the configured value and
distinguish the older claim. Configuration alone does not verify runtime behavior.
This is part of the skill's setup guidance and needs no additional invocation.

## Local-only context (excluded from Git)

Local-only context is an explicit storage option. Existing
projects keep their storage, paths and instructions unless you request a change;
installing or upgrading the skills does not make context local-only.

For a new setup, ask:

```text
Use $adopt-context-docs to set up local-only context, excluded from Git.
Reuse my existing local context and instruction locations if present;
otherwise use .context/local/ for context files. Use repository-local excludes
for my personal setup. Keep private content out of shared docs and instructions.
Verify both tracking and ignore status, including the journal if already enabled.
Preserve existing tracked context and resolve migration scope before changing it.
Record how a fresh session should find the local entry point, and report whether
the guidance actually loads. Leave logging settings unchanged.
```

In Claude Code, replace `$adopt-context-docs` with `/adopt-context-docs`.
The directory above is an example; use your own existing path. For a project-wide
ignore convention, request `.gitignore` instead of a developer-local exclude rule.
The [packaged local-only guide](../skills/context-docs/references/local-only.md)
owns the storage checks, discovery and migration procedure.

The agent should confirm that every chosen context path is untracked and ignored.
Ignored files may be absent from searches, so a new session should read the named
entry point directly, for example:

```text
Read .context/local/project-context.md and its relevant linked documents directly.
Keep this context local-only and use it to continue the next task.
```

Use local agent guidance that actually loads, or an agreed nonsensitive path
pointer in shared instructions. Avoid public README links to files missing from
other clones. A pointer does not authorize copying the local content into shared
docs, tracked instructions, shared journals or exports.

An ignore rule does not stop tracking existing files or erase old commits. The
agent should report tracked context and preserve it until migration scope is
clear, rather than silently moving or untracking it. Enabled journals need the
same storage checks; existing records and logging settings remain intact.

For local-only context, [optional logging](#optional-logging) can retain significant
decisions, checks and corrections as current context changes without Git history.
Enable it explicitly with an untracked, ignored journal destination; selecting
local-only storage alone does not enable it. A selected `auto` preference can also
enable it after the same checks, unless an existing setting takes precedence. The
[journal guide](../skills/context-docs/references/event-journal.md) explains capture
and preservation; complete document versions still need snapshots or backups.

Git exclusion is not encryption or a promise that an agent cannot read the files.
Local files do not travel with clones, other worktrees or other machines; arrange
your own backup or transfer if needed. A missing local entry point requires
restoration or fresh initialization, not invented history. Audits remain read-only,
and repeat adoption preserves matching rules, paths and the original adoption date.

## Optional logging

Preserve existing logging settings. With no setting, logging stays off unless
explicitly enabled or a user-selected auto preference applies. Before enabling,
check that the installed packages include the journal guide and helper; see
[older-package boundaries](releases/README.md#feature-boundaries-for-older-installations).
Preserve locally customized package files when reviewing an upgrade.
To enable it explicitly, ask the adoption skill to enable JSONL in the project's
existing maintenance section, optionally naming a directory. For example:

```text
Codex: $adopt-context-docs Enable optional JSONL logging in history/events.
Claude Code: /adopt-context-docs Enable optional JSONL logging in history/events.
Preserve the existing adoption date, context path and maintenance instructions.
```

The [packaged journal guide](../skills/context-docs/references/event-journal.md)
defines settings, capture, investigation and failure handling. It works without
Git; uncommitted state must not be attributed solely to an old commit. Ask the
same skill to disable logging to stop capture while retaining the directory
setting and all history. No project migration or background service is required.
Setup, no-change maintenance and audits create no events. The
[journal pilot and requirements](event-journal-pilot.md) explain when logging may
be useful and what remains unestablished.

### Auto logging

To opt into automatic enablement, include this preference in your request
or the personal instructions your agent loads:

```text
Context Docs logging preference: auto
```

During adoption or authorized maintenance, an existing project logging setting
wins, including `off`, `jsonl` or another logging method. With no setting, auto
enables JSONL outside Git, or for explicitly selected local-only context inside Git.
For the latter, every chosen context path and the journal directory must be
verified untracked and ignored, including existing descendants and prospective
new paths. A tracked file still fails even if an ignore rule matches it.

### Auto logging for local-only context

For example, after choosing local-only storage, ask:

```text
Use adopt-context-docs to apply my auto logging preference to this local-only setup.
Context Docs logging preference: auto
Use the existing context at .context/local/ and journal directory
.context/local/events. Verify that both are ignored and untracked before enabling.
Preserve explicit logging settings, adoption dates, paths and existing records.
Do not move files, change ignore rules or create a log for setup.
```

These paths are examples; reuse yours. Shared context inside Git does not qualify.
Parent repositories and worktrees count as Git; missing Git, failed detection or
unverified exclusion leaves logging unchanged and the gap is reported. The setting
is saved only in the agreed instruction location that the client loads. Existing
paths and records stay intact; auto does not grant permission to change ignore
rules or relocate a journal to make it qualify. Adding Git later preserves a saved
setting and history. Audits never enable logging. See the
[auto preference rules](../skills/context-docs/references/event-journal.md#optional-auto-preference).
This preference does not automatically commit logs or install a background service.

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

## Upgrading

Review installed files before copying an update. Preserve local customizations
and install both complete sibling packages together. Existing projects keep their
maintenance rules, adoption dates, context paths and logging settings; no document
migration is required. Installing an update does not enable logging. See the
[v0.2.6 upgrade notes](releases/v0.2.6.md#existing-projects-and-upgrades) and
[release history](releases/README.md) for feature boundaries and retained evidence.
The v0.2.6 experimental prerelease does not upgrade existing installations.
