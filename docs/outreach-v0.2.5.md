# Standalone v0.2.5 demo

The illustrative demo is [live on the website](https://context-docs.com/#demo)
as of October 19; its [deployment record](website-demo-deployment-2026-10-19.json)
retains verification and limits.
The demo below is synthetic and illustrative, not an executed session, transcript
or new evaluation result.

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

The draft posting copy was moved to local operator notes on October 23, 2026.
The illustrative demo above remains the website's canonical source.
