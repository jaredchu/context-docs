# Switching between Codex and Claude Code

The [examples index](https://context-docs.com/examples/) has separate authored
walkthroughs for [Codex → Claude Code](https://context-docs.com/examples/switching-codex-claude/)
and [Claude Code → Codex](https://context-docs.com/examples/switching-claude-codex/).
Both reuse the existing [Reading Queue project](https://github.com/jaredchu/context-docs-example-reading-queue),
with no second application, cloud service or deployment needed for the exercise.

## Teaching scenario

Start from the app's `switching-start` tag, based on its original `tutorial-start`
snapshot. The teaching clarification makes the empty export shape explicit:
`{"schema_version":1,"items":[]}`. The starter context limits this exercise to
local implementation and removes historical pending publication from its next
action. It does not change the original tutorial tags or the deployed app.

The outgoing agent implements `GET /api/export` and API tests, then saves its
decisions, rationale, completed work, pending browser integration and actual check
limits in the existing Markdown. The incoming agent receives a fresh session and
reads those files to identify and implement the remaining work. Export covers the
whole active queue because it is a backup, regardless of the UI filter; browser
isolation, expiry and the exclusion of session/database metadata remain required.

The walkthroughs use the same checkout, so saved uncommitted code and notes are
available to the next agent. Different checkouts require transferring both code
and context through the user's authorized workflow; ignored private files need
their own private transfer. Unsaved buffers, chat history, native-memory stores,
processes, credentials and tool connections are not recreated by Markdown.

Each client must load the relevant instructions for continuing maintenance.
The starter's `CLAUDE.md` imports `AGENTS.md`; supported direct loading and settings
also exist. Installation is per client. Reading the entry point explicitly works
with ordinary Markdown even when a skill is unavailable. Follow the
[installation and loading guide](getting-started.md) and the existing
[one-writer rule](getting-started.md#when-sessions-share-a-context-file).

## Observed checks

The November 7, 2026 implementation task includes one bounded native case in each
direction. Results and exact limitations are retained in
[the cross-client record](../evals/handoff/2026-11-07-cross-client/README.md).
The record owns outcomes; authored prompt examples alone establish no successful
handoff. The separate [earlier Git-transfer check](../evals/handoff/2026-11-07-git-transfer/README.md)
used Claude → Claude and does not establish either cross-client result.

The walkthroughs are teaching material, not a controlled comparison, independent
human validation or a promise of reliable switching. Competent ordinary Markdown
and native instructions can support the same workflow. Context Docs supplies
reusable maintenance and adoption guidance; no skill behavior or version change
is needed for these examples.

## Website routes

The Reading Queue walkthrough moves to
[`/examples/reading-queue/`](https://context-docs.com/examples/reading-queue/),
preserving its section IDs. `/reading-queue/` remains a compatibility entry point.
The canonical sitemap lists only the new location and the three example pages
under the examples index. Deployment and redirect verification are recorded in
[the site build guide](../site/README.md#latest-deployment).
