# Context Docs plugin candidate

Keep project decisions, current work, blockers and next steps in readable
Markdown. This experimental candidate is for coding agents with access to a
user-selected project workspace. It bundles core **0.2.5** and adoption **0.1.14**
unchanged. It has not been submitted, approved or published in a plugin directory.

## Two workflows, one package

- **adopt-context-docs:** set up the workflow and add or reuse its ongoing
  maintenance rule in the project instructions the coding agent actually loads.
- **context-docs:** audit or maintain the project's existing Markdown and concise
  progress view during normal work.

Both sibling directories are included under `skills/`; adoption needs the core.
Expected Claude Code plugin commands are `/context-docs:adopt-context-docs` and
`/context-docs:context-docs`. Plugin loading and invocation still need a separate
isolated runtime check. Existing standalone installations should not be replaced
or enabled alongside this candidate without reviewing duplicate-skill behavior.
Removing this plugin does not remove maintenance rules previously adopted into
project instructions. Preserve those rules and explicitly review their skill
references when changing installation methods; do not silently delete them.

## Example requests

1. “Adopt Context Docs in this project. Preserve existing instructions and layouts.”
2. “Audit this project's context documents without editing any files.”
3. “Update the current context from this work, retaining decisions, blockers,
   evidence links and the next action.”

## What it reads, writes and runs

The skills guide the host agent to read project instructions, README/context
documents and relevant sources, and to make task-authorized Markdown edits.
Adoption can update project instruction files. Installation alone performs no
adoption, configuration changes or background work. Markdown remains authoritative.

Optional logging is off unless selected by the project's existing settings or
explicitly enabled under the packaged guidance. Python 3.9+ is needed only for
the optional journal/policy helpers. Those helpers perform local file operations
and applicable read-only Git checks; they do not make network requests. The
package declares no MCP server, hooks, package installer or remote data service.
The host agent's own processing and data handling follow the host's settings.

This package does not access built-in chat history or product memory stores.
Its intended use is authorized project-document maintenance, but that does not
resolve Claude's directory policy concerning extraction from user-generated
files or saved conversation summaries, or unnecessary context collection through
logging. Directory eligibility remains unconfirmed. General chat, hosted execution,
Cowork, plugin auto-loading and cross-surface behavior have not been validated.

## Review and support

Review the packaged `SKILL.md` files before use. To troubleshoot missing adoption,
check that both siblings are present and that the project maintenance rule is
actually loaded. Review every resulting diff and preserve local customizations.
The experimental status and existing evaluation qualifications still apply;
packaging checks do not establish reliability or user benefit.

[User guide](https://context-docs.com/getting-started/) ·
[Release qualifications](https://github.com/jaredchu/context-docs/blob/v0.2.5/docs/releases/v0.2.5.md) ·
[Support](https://github.com/jaredchu/context-docs/issues)

MIT licensed; see the included `LICENSE`.
