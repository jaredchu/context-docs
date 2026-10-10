# Local-only context

Local-only means the chosen context files stay outside Git tracking. It is an
explicit storage option, not a confidentiality or encryption guarantee. Agents
can still read these files when instructed; other software can also access them.
They are absent from fresh clones and need the user's own backup or transfer
method. Preserve the existing setup when no storage change is requested.

## Choose the destination and discovery route

Reuse an existing local-only location and equivalent instructions. For a new
setup, respect the user's path; `.context/local/` is an example when none exists,
not a mandatory layout. Keep the entry point, decisions and related local context
there. A project without Git can keep ordinary local files; report Git exclusion
as not applicable rather than initializing a repository.

For a developer-specific choice, use the repository's local exclude file. Locate
it with `git rev-parse --git-path info/exclude` from the project, including in a
worktree; do not assume `.git` is a directory. For a project-wide ignore convention,
use `.gitignore`. Merge only the agreed path pattern, preserving existing rules
and exceptions. Do not change global Git excludes or force-add local files.

Point to the entry file from project guidance that the agent actually loads.
Prefer an existing local instruction location for a developer-specific setup;
verify its loading rather than inventing a client-specific filename. If only
shared instructions are available, resolve whether the user wants a nonsensitive
local-path pointer there, or an explicit session prompt with persistent discovery
left unconfirmed. Do not silently edit shared instructions for a personal choice.
The pointer may name the path and storage policy, but must not copy local content.
Avoid README/index links to a file that will be absent in other clones.

During adoption, record the storage choice beside the adoption marker in the
agreed instruction location; otherwise report the persistent discovery gap.
Core maintenance can reuse equivalent local guidance without requiring a marker.
For example:

```text
Context storage: local-only
Entry point: .context/local/project-context.md
```

Read that exact path directly on subsequent sessions. Git-aware searches may omit
ignored files; an empty search result is not evidence that context is missing and
does not justify creating a competing shared entry point. If the entry file is
missing after a clone or on another machine, report it and follow the user's
restoration or initialization choice without inventing prior decisions.

## Verify storage before writing

Use read-only Git checks from the project, for example for `.context/local/`:

```sh
git ls-files -- .context/local/
git check-ignore -v -- .context/local/project-context.md
```

Check all selected context paths, including directory descendants and any enabled
journal destination. `git ls-files` must return no tracked files in that scope;
an ignore pattern never makes an already tracked file local-only. Verify effective
ignore rules for the actual target files and prospective new files, accounting
for negated patterns: in verbose `check-ignore` output, a pattern beginning with
`!` means the target is NOT ignored. Nonempty verbose output alone is not success.
A rule for one Markdown file does not protect its siblings
or journal. Recheck new targets before writing and review Git status afterward.
Git errors, missing Git, or an unconfirmed ignore rule are unresolved verification,
not success. No-Git projects retain their chosen local layout.

If existing context is tracked, preserve it and its history. Adding an ignore
rule is insufficient. Explain which files are tracked and resolve migration scope
before moving files, removing shared links or untracking anything. A request for
local-only setup does not silently authorize deleting established shared context
or rewriting history. Previously committed content remains in Git history even
after tracking stops; do not claim it has become private retroactively.

## Keep local content within its boundary

Maintain decisions, current work and next steps in the chosen local files. Do not
copy their content into shared docs, tracked agent instructions, shared journals,
commit/PR text or exported artifacts as a fallback for ignored-file discovery.
A request to maintain or summarize context does not change its sharing destination.
Use the standard's [audience guidance](standard.md#audience-and-destination) when
the user explicitly requests a suitable shared derivative; preserve the local
original and omit details outside that derivative's agreed audience.

Logging remains separately opt-in, including the user's `auto` preference. With
`auto` and no existing logging setting, local-only context inside Git can qualify
after verifying all chosen context paths and the journal directory. Explicit
settings, including `off`, always win. If enabled for local-only work, verify that
the configured journal destination is also untracked and ignored before capture.
For a new journal, an `events/` directory under the chosen local root is one option.
Preserve an existing journal, its setting and records; if it is shared or tracked,
resolve the requested storage scope before capturing local-only content there.
Selecting local-only storage alone does not enable logging. Do not relocate old
events or change global settings as a side effect. Follow the
[journal guide](event-journal.md) for any authorized logging change.

Audits never edit ignore rules, markers, files, the index or history. Repeat setup
reuses matching paths, rules and adoption dates, preserving user customizations.
Report the actual entry point, checked storage scope and any discovery or migration
gap. Claim completed local-only setup only when that scope is untracked and its
ignore status is verified; report loading evidence separately.

[Git ignore rules](https://git-scm.com/docs/gitignore) and
[check-ignore output](https://git-scm.com/docs/git-check-ignore) define these checks.
