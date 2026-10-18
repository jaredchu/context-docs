# Standalone v0.2.5 demo and outreach draft

**Outreach post drafted October 18, 2026; not posted or submitted.**
The illustrative demo is [live on the website](https://context-docs.com/#demo)
as of October 19; its [deployment record](website-demo-deployment-2026-10-19.json)
retains verification and limits. The outreach post below remains a draft.
The demo below is synthetic and illustrative, not an executed session, transcript
or new evaluation result. The post is ready to copy after owner approval.

## Short demo: resume without reconstructing the conversation

Suggested length: 60–90 seconds. Show a Markdown diff and a fresh-session prompt.
Use a disposable fictional project; no private project material is needed.

**Starting point:** both standalone skills are installed from the
[experimental v0.2.5 release](https://github.com/jaredchu/context-docs/releases/tag/v0.2.5).
Adopt once with `$adopt-context-docs` in Codex or `/adopt-context-docs` in Claude
Code. Confirm the maintenance rule is loaded and note its context entry point.
The fictional project below uses `docs/context.md`; existing projects keep their
own paths and layouts. See the [installation and usage guide](getting-started.md).

### 1. Show the fictional work notes

These are the demo's supplied facts, not results from this repository:

<a id="synthetic-source-notes"></a>

```text
Goal: validate CSV export, including empty input, before calling it complete.
Maintainer-approved decision: keep the existing export API for compatibility.
Result: two sample export checks passed; full validation has not run.
Blocker: the empty-input fixture is missing, so that check cannot run yet.
Next action: add the empty-input fixture, then run that check.
```

### 2. Show the saved Markdown

After meaningful work, the loaded maintenance rule guides the agent to update
the existing context. No repeated skill invocation should be needed. For example,
an ordinary task prompt could be: “Review the supplied export-check notes and
identify the next test to add.” Inspect whether the context update also happens;
do not present a missed update as a pass. An explicit update request is a recovery
option, not evidence of automatic maintenance.

Illustrative saved view, derived only from the notes above:

```text
Goal: validate CSV export, including empty input [S]
|-- DONE     Two sample checks passed [S]
`-- BLOCKED  Empty-input check: fixture missing [S]
    `-- NEXT Add the fixture, then run the check [S]

Decision: keep the existing API for compatibility [S].
Limit: full validation has not run [S].
```

Source S: [synthetic source notes](#synthetic-source-notes).
In a real project's saved view, link to its actual decision and check records.
Review the diff: the two sample passes must not become “export complete.”

### 3. Resume in a fresh session

```text
Read docs/context.md and its relevant linked sources.
Explain the next task and the decision we need to preserve. Do not edit yet.
```

Look for: add the missing fixture before running the empty-input check, retain
the compatibility decision, and keep full validation pending. This is a check
to make when recording the demo, not an observed outcome. Saved Markdown is the
handoff; an old context update does not imply live agent activity.

## Outreach post

**Context Docs: keep decisions and next steps across Codex and Claude Code sessions**

Starting a fresh coding-agent session often means explaining what you decided,
what is blocked and what to do next. I'm building Context Docs for people who
want a small, readable workflow for saving that knowledge in their project's
existing Markdown.

Standalone **v0.2.5 is experimental**, and I'd like Codex and Claude Code users
to try it. Two skills handle setup and ongoing maintenance. Once adopted with
its maintenance rule loaded, the workflow guides the agent to keep context and
a concise progress path current during meaningful work, without naming the
skill in every prompt. You review ordinary Markdown diffs; a fresh session reads
the saved context and relevant sources.

For example: two export checks passed, but empty-input validation is blocked by
a missing fixture. Save that blocker, the compatibility decision and the next
action, so the next session can resume without calling the feature complete.
This example is illustrative.

Focused checks in both clients are guided and author-scored, with retained
failures and qualifications. Broad reliability, automatic everyday compliance
and user-effort savings are not established. It provides no background service
or file locking; shared context files still need one writer at a time.

[Get v0.2.5](https://github.com/jaredchu/context-docs/releases/tag/v0.2.5) ·
[Install and use](https://github.com/jaredchu/context-docs/blob/v0.2.5/docs/getting-started.md) ·
[Evidence and limits](https://github.com/jaredchu/context-docs/blob/main/docs/evaluation-results.md)

If you try it, [open an issue](https://github.com/jaredchu/context-docs/issues):
what helped, what needed a reminder, or what became inaccurate or too verbose?
Include your client and skill version if known. Public examples or synthetic
reproductions are welcome; please keep private context and credentials out.
No formal evaluation is needed to give feedback.
