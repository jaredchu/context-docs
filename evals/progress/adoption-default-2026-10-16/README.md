# Default inline progress during adoption

October 16, 2026. Development core 0.2.2 / adoption 0.1.11, unreleased.
The owner requests a small inline progress view by default when supported, then
everyday maintenance without duplicate information. Existing layouts, setups,
installed skills and saved studies must remain intact.

## Acceptance cases

1. **Supported context, no view:** explicitly re-adopt an already-adopted project
   without asking for visualization. Use
   the documented goal, checks and missing-fixture blocker to make a small inline
   path within the existing Work section. Keep the original headings and owner
   rationale; make source links clickable. Reuse status lines, not a second task
   list, separate progress file or copied evidence register. Preserve equivalent
   setup rules, marker/date and logging off.
2. **Everyday update:** supply a later retained passing result and finish ordinary
   work under the fixture's maintenance rule, without requesting progress. Refresh
   the same path and canonical facts; remove the obsolete blocker/next action as
   current claims. Preserve the original evidence, owner decisions and layout.
3. **Existing view:** adopt a project with a canonical grouped-bullet or linked-file
   view. Keep its location, format, owner edits and source links; add no inline
   replacement or parallel task list. An explicit visualization may reshape it.
4. **Sparse context:** no documented goal, or insufficient supported work. Keep
   known facts without inventing a goal, progress scaffold or completion conditions.
5. **Explicit preference and local-only storage:** honor no-view/separate-file
   requests and existing ignored/untracked destinations. Keep private facts out of
   shared documents; do not enable logging, move tracked context or rewrite setup.
6. **Repeat and audit:** no new facts means no edits/events; audit-only adoption
   changes nothing, even when a useful view could otherwise be created.

## Observed native checks

Cases 1 and 2 pass in two fresh native Codex CLI sessions on one already-adopted
synthetic Maple CLI project, using copied initial candidate packages. Requested model: `gpt-6.1-sol`,
medium; responding identity unconfirmed. Each has one attempt under 180 seconds,
without retry: adoption completes in 33.99 seconds and the ordinary update in
20.22 seconds. Sol, the change author, scored these outputs; this is not independent validation.

- [Adoption output](adopt/notes/context.md): replaces the original Work status
  paragraph with a nested checklist, its blocker and linked next action. Existing
  headings, owner note/example, decisions and Next move remain; no separate file,
  duplicate status list or setup rewrite. Only the context file changes.
- [Everyday update output](maintain/notes/context.md): a result-recording request
  that never asks for progress refreshes the same checklist and Next move. Both
  checks now pass, the current blocker is removed, earlier dated evidence stays
  retained and deployment still needs owner approval. Only results and context change.
  This checks existing core refresh behavior on the adoption-created view, not
  the effect of newly added maintenance-rule wording. The prompt supplied a
  cross-check summary/next action for the retained result; that output is not
  presented as an ideal evidence-register layout. Its source-linked NEXT label is
  a summary of the canonical Next move, rather than an independent status record.
- Three relative file/anchor links per context resolve; the additional local
  Next move anchor is checked separately. The actual candidate core/guide reads
  are observed. Original fixture instructions, marker/date, logging off, owner
  sentinel and decisions are byte-equal after both sessions.

The [protocol](protocol.json) retains the fixture and exact prompts, with only
the executable path normalized. The [summary](summary.json) retains output and
raw-receipt hashes. Full traces/receipts remain private. Runtime state-db warnings
were retained without repair. No Git fixture or probes were used. These are
guided candidate checks, not evidence of default discovery or future instruction
loading. Fresh adoption that writes a new rule/marker was not run.

After counterpart findings clarified established views and explicit re-adoption,
one further native Codex session runs the clarified candidate on the completed
fixture: **an unchanged re-adoption makes zero edits**. It completes once in
18.79 seconds under 180 seconds, without retry. All fixture bytes remain equal
to the [repeat protocol](repeat-protocol.json). This covers the existing nested
checklist and no-change-repeat branch; linked/nonvisual views, sparse context,
local-only, explicit no-view and audit cases remain unexecuted natively.
The summary pins both candidate package identities: creation and everyday update
precede the wording clarification; repeat uses the clarified candidate.

## Mechanical checks and counterpart review

Packaging/static regression tests pass (18); site tests pass (15); both skill
metadata validators and isolated sibling-package links pass. A nine-file website
build succeeds in private scratch without changing the existing build or deploying.
Repository links/versions and whitespace checks pass separately from native behavior.
The [initial Opus review](review-initial.md) completes in 61.93 seconds under a
180-second cap, requested/reported `claude-opus-5-5`, medium. It uses existing
authenticated Claude Code access with only Read, no MCP, hooks, auto memory or
session persistence; native success has no permission denials. This is counterpart
artifact review, not a Claude subject trial or independent validation.

| Finding | Source-checked disposition |
| --- | --- |
| M1: ordinary status prose versus an existing view is ambiguous | Confirmed. Preserve lists, tables, diagrams and designated progress sections/files; ordinary status sentences may be grouped in place. Retain format if unclear. |
| M2: evidence is re-adoption, not fresh setup; repeat rule is unclear | Confirmed. Explicit adoption may add a missing supported view while preserving existing setup records; later unchanged repeats make no edits. Claims now identify the already-adopted fixture and untested new-rule/marker branch. The extra repeat check changes nothing. |
| M3: changelog describes review before it is recorded | Draft timing issue; the completed review is now recorded here, before closeout. |
| Stale/repeated context actions; doc guarantees | Consolidated the affected current-focus/next-action text and stated untested behavior as guidance. |
| Scoring and maintenance wording attribution | Sol is the change author and scorer. Ordinary update checks existing core refresh behavior, not the new setup-rule wording. |
| NEXT label and summary in retained result | Linked NEXT summarizes canonical Next move; it is not a separate task list. The prompt supplied the evidence summary, so it is retained with that qualification rather than promoted as ideal record layout. |

The [one focused follow-up](review-followup.md) completes in 42.44 seconds under
120 seconds with the same requested/reported Opus model and read-only controls.
It finds no unresolved material finding and flags stale context counts, which
now include the repeat. It also suggests clarifying that adoption's "add only
the missing marker" restriction applies to setup records; that minor scope
clarification is applied after the follow-up, without a third review or another
native run. Documentation distinguishes initial and clarified native candidates;
final source identities are retained separately. No broader approval of untested
branches or installed upgrades is implied.

Preservation checks compare 63,220 pre-change entries across the repository,
installed skill trees and earlier private evidence. Only scoped source/docs and
new synthetic check/journal evidence differ. Existing setups, installed skills,
saved studies and prior evaluation records remain byte/mode equal. Git metadata
and accepted routine native-client bookkeeping are outside this inventory; no
global-state equality claim is made.

## Validation boundary

Use only a synthetic disposable project and copied candidate packages. Native
checks are explicitly guided uses, not implicit-loading proof, installed-version
evaluation or independent validation. Mechanical checks cannot establish that an
agent follows the instructions. Preserve all earlier evaluation artifacts; this
record supplements rather than rescoring the released v0.2.1 smoke evidence.
