# Runnable worked example: Reading Queue

The owner selected a separate public Reading Queue project on October 25, 2026,
and authorized its Cloudflare demo and publication of the website walkthrough
after validation. The [decision](project-decisions.md#runnable-worked-example)
retains scope and authority.

- [Example repository](https://github.com/jaredchu/context-docs-example-reading-queue)
- [Demo](https://context-docs-example-reading-queue.viweb.workers.dev)
- [Website walkthrough source](../site/reading-queue.html)
- [Example's current context](https://github.com/jaredchu/context-docs-example-reading-queue/blob/main/docs/project-context.md)

## Scope and status

The app uses Workers static assets and D1 for temporary browser-isolated queues.
It supports adding links, read/unread status, filters, deletion and JSON export.
The team omitted R2 because URL records do not need object storage. This app
does not add a hosted runtime or cloud requirement to Context Docs itself.

The starter and completed Git tags preserve a real export change and its context
update. The walkthrough provides copyable prompts, expected results and checks.
Only adoption names a skill; later work requests are ordinary prompts. Check
actual instruction loading and resulting Markdown rather than assuming that
prompt text establishes automatic behavior.

Local validation passed: 18 app integration tests against workerd/D1, actual
headless Chrome downloads and failure handling, desktop/mobile checks, and 22
site build tests. This is an authored teaching example with application checks;
it is not independent evidence of improved handoffs, reliability or savings.
A [focused native continuation](https://github.com/jaredchu/context-docs-example-reading-queue/blob/main/docs/evidence/README.md)
observed Claude Code / Opus 5.5 High invoking the installed skill and updating
three context documents from an ordinary implementation prompt with no skill
name or documentation-update request. The disposable fixture passed 20 API
tests on the coordinator rerun and retained browser checks as pending. It is
separate from the integrated app, not a Codex run or general implicit-selection
claim; the preserved decision diff also has an explicitly recorded wording
qualification. Two configuration-limited attempts are retained in private notes.

A subsequent maintainer-operated Codex CLI / GPT 6.1 Sol High trial used
preinstalled skills and the starter's adopted AGENTS.md maintenance rule. All
eight local website prompts ran unchanged, with a separate fresh implementation
thread; the invocation ignored user configuration and execution-policy rules.
It read the skill and updated context without another reminder; 23 fixture tests
passed. Native browser launch failed, while separate coordinator Chrome
checks passed after recorded helper corrections. Verification also downloaded
BrowserAct support despite the no-install constraint, then removed it. This is
qualified evidence of maintenance, **not a clean walkthrough pass** or independent
learner validation. Detailed records and the prepared learner-feedback packet
remain in private notes under evidence ID `reading-queue-codex-2026-10-25`.

The [app workflow](https://github.com/jaredchu/context-docs-example-reading-queue/actions/runs/40158636168)
automatically tested and deployed `0f68893`. All four served static assets match
the source by SHA-256, the live health endpoint reports that full commit, and
live browser checks passed for CRUD, isolated queues and export success/failure.
The [companion walkthrough](https://context-docs.com/reading-queue/) was
[initially deployed from b38853d](https://github.com/jaredchu/context-docs/actions/runs/40158912040).
All ten served website files match the pinned build and uploaded artifact; live
desktop/mobile checks, including all nine prompt copy buttons, pass. Later
record commits do not replace either deployed source. Gather concrete learner
feedback next. Detailed operator evidence belongs in private notes under evidence ID
`reading-queue-example-2026-10-25`. Skill versions and prior studies are unchanged.


## October 26 review follow-up preview

The owner requested retaining the independent Astra/Fable reviews in private
notes, applying targeted cleanup and preparing a local preview. Both reviews
were configured at High and assessed the same coordinator desktop/mobile captures;
this is independent model judgment, not separate browser reproduction or human
validation. Detailed originals and verified disposition belong in private notes
under evidence ID `website-review-2026-10-26`.

The cleanup improves the comparison-to-example route, audit verification
instructions, dated evidence notes and optional-deployment wording. Main-branch
example documents align ordinary prompts and clarify the existing export shape
and implementation-team rationale. Historical case records and published tags
retain their original scope. No app behavior, skill version or installed package
changes are selected.

The local preview passes all 22 site tests, repository static checks and
desktop/mobile rendering and navigation checks, including copy feedback with
clipboard writes stubbed inside temporary contexts. Only the comparison and
walkthrough HTML outputs changed relative to the committed build. The owner
subsequently authorized website-only deployment from `main` at
`ee9211e`, completed on October 26 by the
[Pages workflow](https://github.com/jaredchu/context-docs/actions/runs/40258260595).
All ten served files match that pinned build and uploaded artifact; canonical
metadata, sitemap/robots and live desktop/mobile checks pass. Detailed receipts
are retained privately under evidence ID `website-deployment-2026-10-26-ee9211e`.
The original preview and review records retain their earlier scope.

The app remains at `0f68893` and was not redeployed. Broader mobile-table
restructuring and guide-length changes remain proposals for learner feedback.
The owner plans to share the existing learner packet; no new human results or
native agent evaluation were collected by this publication. Record-only follow-up
commits do not require another deployment.
