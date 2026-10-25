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

The [app workflow](https://github.com/jaredchu/context-docs-example-reading-queue/actions/runs/40158636168)
automatically tested and deployed `0f68893`. All four served static assets match
the source by SHA-256, the live health endpoint reports that full commit, and
live browser checks passed for CRUD, isolated queues and export success/failure.
The companion website walkthrough is validated locally; publication is pending. Detailed operator evidence belongs in private notes under evidence ID
`reading-queue-example-2026-10-25`. Skill versions and prior studies are unchanged.
