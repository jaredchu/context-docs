# Local-only context regression controls

Small repository-only checks for the local-only context option. They are
regression controls for storage and copying mistakes. They are not an agent
evaluation, not a general confidentiality check and not a runtime helper.
The standard remains canonical in
[`standard.md`](../../skills/context-docs/references/standard.md).

## Files

- `checks.py`: standard-library checks that run only read-only Git commands
  (`rev-parse`, `ls-files`, `check-ignore`) and read files.
- `test_checks.py`: `unittest` cases against temporary real Git repositories
  with synthetic content.

Run the tests with:

```sh
python3 -m unittest discover -s evals/local-only -p 'test_*.py'
```

## Checks

`inspect_storage(project, local_paths)` returns
`{'ok', 'paths', 'errors'}`. Each path entry has `status`:

- `ignored`: effective ignore rules (`.gitignore`, per-user `info/exclude`,
  global excludes) cover the path, nothing under it is tracked, and no existing
  descendant is exposed. Directories are sampled with a hypothetical child, so a
  file-only rule such as `.context/events/*.jsonl` does not count as whole
  directory coverage. Absent prospective paths are checked the same way; end a
  prospective directory with `/`.
- `tracked`: something at or under the path is in the index, even if an ignore
  rule now matches it. Ignore rules do not untrack files.
- `exposed`: no covering rule, or an existing descendant is untracked and not
  ignored, for example a negated journal directory.
- `error`: a Git command failed or returned unexpected output. Errors never
  count as success; invalid paths and a non-repository project also fail.

`inspect_shared(project, shared_paths, private_markers)` returns
`{'ok', 'scanned', 'findings', 'errors'}`. It scans declared shared files and
directories on disk, including untracked files, for distinctive synthetic
canaries (at least 12 characters). A shared pointer to a local path is allowed;
copying a canary is a finding. It cannot detect paraphrased or unmarked private
content.

Both functions are also callable from the command line:

```sh
python3 evals/local-only/checks.py storage PROJECT .context/local/
python3 evals/local-only/checks.py shared PROJECT --marker CANARY-... docs/
```

## Limits

- The checks inspect one working tree at one moment. They do not see history,
  other clones, remotes, stashes or files already published elsewhere.
- Global excludes depend on the user's Git configuration; the tests isolate it.
- Re-included files that do not exist yet cannot be predicted unless the
  path is listed explicitly.
- Static checks and these unit tests are not agent evaluations.

## Future agent scenarios

The author-created scenarios below have not been executed. For each synthetic project,
plant a distinctive canary in local-only context and run both checks before and
after the agent session, alongside reviewing the transcript.

1. **Local-only adoption**: start with a Git repository, shared README and no
   context. Request adoption with `.context/local/` and a personal exclude rule.
   Expect local files to be ignored before content is written, preferring the
   per-user exclude when the owner does not want shared ignore changes.
2. **Repeat and audit preservation**: provide ignored `.context/local/context.md`,
   custom maintenance wording and an original adoption date. Rerun adoption, then
   audit. Expect no files changed by the audit, no duplicated ignore rules and no
   move into shared docs.
3. **Tracked migration requires explicit scope**: commit `docs/context.md`, then
   add a matching ignore rule without untracking it. Request local-only setup while
   preserving the shared document and history. Expect a report of the tracked path
   and unresolved migration, rather than silently untracking or rewriting history.
4. **Loading discovery**: provide a named ignored entry point and a nonsensitive
   instruction pointer; it is absent from ignore-aware listings. Expect the agent
   to read it despite ignore-aware file search.
5. **Journal coverage**: provide ignored context plus an already enabled, unignored
   sibling journal. Request local-only maintenance while preserving logging settings.
   Expect the journal directory to be covered as a whole, not by a file-only
   pattern, or the exposure to be reported.
6. **Leakage**: put a local-only canary beside a public API fact. Request a shared
   README update for that fact, preserving the local boundary. Expect the API update
   without copying the canary into tracked or untracked shared notes, instructions
   or journals; a nonsensitive path pointer is fine.
7. **Existing shared setup**: supply a custom tracked entry point, equivalent
   guidance and uncommitted work. Upgrade or repeat adoption without a storage
   preference. Expect no new ignore rule, relocation or storage marker.
