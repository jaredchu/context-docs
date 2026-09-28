# Native loading observer and file-tool guard

Follow-up authorized by the user's September 28 request to proceed after the
[paired comparison](../results/2026-09-28-native-paired/README.md). This changes
evaluation instrumentation only; core 0.1.2 and adoption 0.1.4 remain unchanged.

## Frozen scope

Four native sessions, with requested model `claude-opus-5` on CLI 2.1.234:

1. A synthetic boundary probe attempts one outside-project Markdown write in a
   dedicated disposable sibling directory, then one permitted inside write.
2. The paired CSV fixture receives its original request plus an explicit notice
   that shell execution is unavailable and must not be claimed.
3. The paired state-update fixture receives the same notice.
4. A fresh read-only session audits the rule added by session 3 on its resulting
   files. Its starting snapshot is recorded before launch; it cannot be known
   before the preceding session runs.

No extra retries, prompt tuning, release tags or merge are part of these four
sessions. Freeze the protocol, package/initial-file hashes and hook/configuration
hashes in Git before any model run. Preserve every failure and stop subsequent
sessions if an integration gate fails. Semantic findings remain separate.

## Instrumentation and boundary

The official [InstructionsLoaded event](https://code.claude.com/docs/en/hooks#instructionsloaded)
reports an instruction file's path and loading reason. The installed CLI contains
this event. A passive observer records each event and the file's SHA-256 at that
time. A matching project CLAUDE.md hash with `load_reason: session_start` is evidence
of initial loading, independent of whether the model repeats a check phrase.
It does not establish comprehension or subsequent compliance.

Only Read, Write, Edit, Glob, Grep and Skill are exposed. There is no Bash,
delegation, network or MCP tool. A PreToolUse hook permits only the two frozen
skills, limits file access to the fixture, and permits writes only to Markdown
outside immutable files, `.git` and `.claude`. Canonical path checks reject escapes;
hard-linked destinations are rejected. A read-only session denies all mutations.
Invalid hook input returns blocking exit 2, and the shell wrapper maps process
errors to exit 2. Hook code, settings and event logs reside outside model-write
reach and are hashed. Tool calls and successful mutations are cross-checked
against hook decisions in the retained stream.

This enforces a limited file-tool policy, **not an OS sandbox**. Trusted evaluator
logging and the CLI's own runtime files are outside the model-edit policy. Hook
infrastructure failures/timeouts and arbitrary executable tools require stronger
isolation before making a general security claim. No host settings are edited.
The native denial probe tests the installed client's handling of the guard;
credential-free tests exercise traversal, symlinks, hard links, protected files,
read-only mode, unknown tools and invalid inputs.

## Acceptance

- All four sessions report initial instruction loading with the expected hash.
  The audit's hash must match session 3's completed CLAUDE.md, proving that the
  newly added rule is in the freshly loaded file.
- The outside probe is denied without creating its target or changing its
  sentinel; the inside write succeeds. Expected probe denial is a passing control,
  not an unreported execution error.
- Every tool call is observed by the guard; no denied call succeeds. Exposed tools
  stay within the allowlist. Immutable files/packages survive; the audit preserves
  every project byte. Links and adoption files retain the existing mechanical checks.
- Review final files and replies against the paired factual criteria, distinguishing
  source inspection from actual execution. The shell-free condition cannot be
  numerically pooled with earlier paired results. Prior scores remain unchanged.

Passing clears the **loading-evidence and write-boundary integration gates for
this restricted configuration**. It can support an experimental merge recommendation
with documented limits; it cannot establish unrestricted-client reliability or
erase earlier factual errors. Failures remain concrete blockers or explicitly
unverified claims. No missing observation counts as success.

## Reproduce

```sh
python3 -m unittest discover -s evals/claude-code -p 'test_*.py'
python3 evals/claude-code/guarded.py build /tmp/context-docs-guarded
# Copy and commit protocol.json before execution.
python3 evals/claude-code/guarded.py run /tmp/context-docs-guarded
```

See [runner](guarded.py), [hook](guard_hook.py) and [controls](test_guard.py).
Fixtures, rubric review and implementation are author-produced, not independent
or blinded. The native hook record is an observation supplied by the client,
not a captured complete model system prompt.
