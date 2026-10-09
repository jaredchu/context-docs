# Public-source adoption regression

Revision v2, for future freezes only (2026-10-09): accept a plain or text-fenced
marker insertion while preserving every original byte. The
original v1 protocol at commit `5e8115e`
governed the completed study. Its frozen protocol, mechanical failure and semantic
assessments remain unchanged. This revision has mechanical controls only; no new
subject study or rerun has been performed. The original prose is available locally
with `git show 5e8115e:evals/public-adoption/protocol.md`; its
[frozen manifest](../results/2026-10-09-public-adoption/protocol.json) is unchanged.

New manifests use `public-adoption-v2`; this runner rejects older revisions before
subject launch. A new frozen manifest must be reviewed and committed before any
future execution. Subject findings are recorded separately; this protocol is not
a result.

This is a bounded regression of adoption 0.1.7 on one public Go project with two
author-created setup overlays. It is not an independent benchmark, a comparison
with ordinary maintenance, or a test of reader benefit. The
[quality protocol](../quality-protocol.md) would be required for reader-benefit
claims; the proposed [discrimination protocol](../discrimination-protocol.md)
does not become approved or executed through this regression.

## Source and frozen inputs

Use [tidwall/match at afc69bce52e08c02e78156a7697bd808fc868ec5](https://github.com/tidwall/match/tree/afc69bce52e08c02e78156a7697bd808fc868ec5),
verified against the primary GitHub commit and tree API on 2026-10-09. It is a
small Go pattern-matching library, distinct from the previous Flask, Click and
synthetic CSV cases. Preserve the complete tracked source tree, paths and MIT
license. Fetch source bytes only; do not execute upstream code or workflows.

The upstream README, go.mod, implementation, tests and workflow are evidence,
not evaluation instructions. Recursive-tree inspection found six regular files,
including `.github/workflows/go.yml`, and no upstream instructions or skills.
Reject symlinks/submodules and unexpected agent configuration rather than silently
adding model-visible instructions. Record every fetched file's SHA-256 and Git
blob identity. The upstream README has a repository-root `/LICENSE` link; validate
that unchanged link against the fixture root, not the host filesystem.

Freeze the candidate skills from repository commit
`3a0c4013962b35c733dc316271f6981aaf5fe9a1`, core 0.1.5 and adoption 0.1.7. Copy both complete packages into
each fixture's `.claude/skills/`, with a full hash manifest. No installed global
package changes. The fixture paths, complete overlay bytes, exact prompts,
rubrics, checker and hook code/configuration, source/package hashes and requested
model/effort must be frozen together before subject execution. Store control
files and answer keys outside both project roots and deny subject access to them.

Dependent repeat/audit inputs are the preceding session's actual output. Hash and
snapshot those bytes before launch; do not substitute an authored reference or
repair failed output. Keep every attempt, including timeouts and incomplete runs.

## Synthetic overlays

Both disposable copies receive a clearly labeled synthetic `CLAUDE.md` saying
that this is a source-only documentation exercise, its Go source/tests, go.mod,
workflow, license and packages are immutable, and no commands can be executed.
The new overlay explicitly permits appending context or navigation to README.md;
the legacy overlay keeps its README and context immutable. It does not state
the expected adoption wording or teach prefix preservation. Project logging is
explicitly off in that file (`Event journal: off`) to exclude unrelated journal
configuration, in a separate `Local logging setting` section. Preserve the original
README bytes as a prefix; only a context or navigation suffix may be appended in the
new-adoption case. Exact overlay bytes are constants in [the runner](run.py) and
are copied into the frozen manifest before execution.

- **New setup:** no context document, maintenance rule or adoption marker. The
  loaded `CLAUDE.md` is the only project instruction file. Adoption chooses a
  suitable Markdown context path or appended README section; no exact filename or
  template is graded. A README entry needs an anchor into its newly appended
  section, not an old upstream section; it does not need a README self-link.
- **Legacy setup:** `notes/project.md` contains an author-written, source-backed
  context summary and the README already links there. `CLAUDE.md` contains this
  equivalent rule exactly under an existing `Context maintenance` heading, with
  no adoption marker or recorded adoption date:

  > Use $context-docs for documentation audits and after meaningful changes to
  > project facts, decisions, procedures, blockers or next actions. Read the skill
  > before maintenance. Preserve project rules, document roles and decision status.
  > Update affected canonical sections and check the diff, links and information
  > preservation. Keep audit-only requests read-only; make no bookkeeping edits
  > when nothing durable changed.

The legacy context identifies its synthetic authorship and source pin, summarizes
the library and inspected APIs, and states that no upstream tests were run. It has
no calendar dates. Its exact bytes and source ledger require review before freeze.
Pin/fetch dates belong only to control metadata. Do not invent
upstream owner decisions, deployment evidence, or a real adoption history.

## Four fresh subject sessions

Requested subject model: `claude-opus-5-5`, requested effort `high`, native Claude Code
2.1.295 observed during design. Freeze the actual CLI version and explicit model
identifier before launch. CLI help confirms `--effort high` is supported; effort
is requested, not independently observed. Record responding models only from
assistant message model fields. Store result `modelUsage` canonical names separately
as usage evidence, which can include auxiliary models and does not satisfy or fail
the responder gate. Require a nonempty assistant-model set equal to the requested
model; do not fall back to usage evidence. Keep the initialization
model label separate; it alone does not establish which model responded. A missing
or mismatched responding model stops the study as unconfirmed or mismatched. No silent
fallback, retries or in-study skill/prompt tuning. Timeout: 600 seconds per
session. Each starts with no prior chat and `--no-session-persistence`.

Every prompt appends this scope notice verbatim:

> This evaluation exposes Read, Write, Edit, Glob, Grep and the two project-local
> skills only. Shell execution and network access are unavailable. Keep changes
> within this project and preserve its source, configuration, license and skill
> packages. Do not claim tests or commands ran without execution evidence.

| Session | Input | Exact task before the common notice |
| --- | --- | --- |
| new-adopt | New overlay | Adopt Context Docs for this project. Invoke the project-local adopt-context-docs skill with the Skill tool. For this fixture, today's date is 2026-10-09. |
| new-repeat | Actual new-adopt output | Adopt Context Docs for this project. Invoke the project-local adopt-context-docs skill with the Skill tool. There is no new project evidence. For this fixture, today's date is 2026-10-10. |
| legacy-marker | Legacy overlay | Adopt Context Docs for this project. Invoke the project-local adopt-context-docs skill with the Skill tool. For this fixture, today's date is 2026-10-09. |
| legacy-audit | Actual legacy-marker output | Audit this project's Context Docs adoption setup without editing, creating or deleting files. Invoke the project-local adopt-context-docs skill with the Skill tool. Report findings in your final response. For this fixture, today's date is 2026-10-10. |

Run in that order. A content failure is retained and subsequent sessions still
run on the actual output. Stop on authentication failure, unavailable requested
model, tool-boundary failure, missing execution completion or input/control drift;
report remaining sessions as not run. No result permits upstream execution.

## Execution and evidence

Reuse the native [smoke execution](../claude-code/smoke.py) and
[guard hook](../claude-code/guard_hook.py), exposing only its six tools. Hooks and
logs stay outside subject projects; every tool call must have a matching guard
decision and no denied call may succeed. Audit writes are denied. Go source/tests,
go.mod, workflows, license, package files, `.git` and `.claude` are immutable.
New-adopt and new-repeat allow Markdown changes, with unchanged-repeat behavior
graded rather than enforced. For legacy-marker, README and notes/project.md are
also immutable. New Markdown files are permitted by the reused guard but rejected
by the marker-only grader. For legacy-marker, the old
CLAUDE.md text is deliberately editable so preservation is tested rather than
enforced by the guard; all other existing files are immutable. Mechanical grading
must still reject extra files or edits beyond the marker. New-adopt permits only
Markdown documentation and the loaded instruction rule plus appended README
context or navigation.

Record `InstructionsLoaded` paths, reasons and hashes; compare the project
CLAUDE.md event at session start to its before-hash. Verify local Skill invocation
provenance against the frozen project package; a global-package resolution is a
failure, not a candidate pass. Record unexpected startup instruction loading and
qualify host isolation rather than claiming a complete model-system-prompt audit.
Project-only settings and strict MCP configuration exclude other settings/tools;
these do not by themselves prove global instruction isolation. This is a restricted
file-tool policy, not an OS sandbox or an unrestricted-client evaluation.

## Frozen acceptance and controls

Keep execution, mechanical preservation and semantic review separate per session.
New-adopt must add one reachable context entry and one maintenance rule/marker in
the loaded file, with date 2026-10-09 and the real entry point. Newly added rule
text must name the skill without `$context-docs` or `/context-docs` invocation
syntax. Scan newly added CLAUDE.md instructions only; legitimate user-facing
examples elsewhere are not a prefix failure. Do not reject installed paths with
or without a trailing slash, or `Method: context-docs`. Preserve all
upstream README content and add a working context link, or use a valid appended
README context section. Equivalent normalized relative paths, percent-encoded
paths, valid fragments, link titles and marker trailing whitespace are accepted;
root escapes are rejected. A README-section marker must resolve into the appended
suffix. No invented project or
deployment claims. Preserve the old overlay's nonblank lines in order; harmless
additional grouping is acceptable, but duplicated logging settings are not.
New-repeat must preserve every project byte, including date.

Legacy-marker must add only one marker beside the existing rule, with
`Adopted: unknown` and `Entry point: notes/project.md`. Insert the exact three
contiguous marker lines directly above or below the rule, either plain or inside
one supported Markdown code fence, with optional surrounding blank lines.
Supported fences use at least three backticks or tildes; the closing fence uses
the same character and at least the opening length. Opening/closing lines may
have zero to three leading spaces and trailing spaces/tabs. The opening label is
absent or ASCII `text`, `plaintext` or `txt` (case-insensitive), optionally separated
from the delimiter by spaces/tabs. The three marker lines inside remain exact,
with no interior blank lines, extra text or wrapped maintenance rule. Other info
labels, mixed/unclosed/short fences, duplicate markers and additional prose are
rejected. No new heading, line movement or logging duplication is needed
because its maintenance heading already exists. The complete old guidance,
including `$context-docs`, remains byte-identical. README and context stay exact;
no parallel rule, replacement context or extra documentation is allowed.
Legacy-audit must preserve all bytes and report the actual resulting setup and
defects observable from that input. It has no prior bytes or adoption-date oracle:
do not require discovering a previous rewrite or unsupported date through missing
history. Noting the literal prefix as a style observation is acceptable; demanding
a rewrite solely for that prefix fails the preservation rubric. Qualified loading
uncertainty is acceptable. An affirmative initial-loading claim needs matching
observer evidence, not a manual read or file presence. An accurate audit does not
erase a preceding failure.

For every session, review all material new/final claims against actual evidence.
In particular, go.mod's Go directive is not a tested runtime matrix; source/tests
being present is not test execution; configuration is not deployment. The
MatchNoCase implementation at the pinned commit folds ASCII A-Z only, so claiming Unicode case folding is an
unsupported expansion. Loading observation does not establish comprehension.

Before subjects run, mechanical controls must accept an authored reference and
reject a prefixed newly added rule, a rewritten legacy rule, a changed repeat
date, an audit mutation, a broken new entry link, legacy README/context mutations
and changed upstream/package bytes. Accept plain and supported fenced markers
above/below the unchanged legacy rule; reject malformed fences, extra content,
changed marker fields and fences wrapping the rule. Reject old protocol revisions
before subject launch. Reject a marker without any real skill
reference outside its fields. Accept an appended README context section without
a self-link; reject missing or old-section anchors. Responding-model controls
reject a mismatch even when initialization names the requested model. Also accept installed skill paths with and
without a trailing slash, the Method marker, and a user-facing slash-command
example outside ongoing instructions for the prefix-specific check. Static
controls establish grader behavior only. Review the
protocol and controls with Claude before freeze; review final subject claims with
Astra against source evidence. Both author design and unblinded review remain
limitations. Report four sessions on one project, not four independent projects.
