# Existing-skill refresh baseline protocol

Frozen before native execution on October 26, 2026. This is a synthetic,
coordinator-authored diagnostic of the unchanged core **0.2.6**. It asks whether
an explicit refresh request already works before adding skill instructions.
There is no modified-skill comparison or claim of a skill-specific advantage.

## Inputs and execution

The [fixture](fixture/README.md) represents an adopted project with accumulated
drift, canonical decisions, current configuration, a narrow verification report
and an existing progress view. All project content is synthetic. There is no
runnable application or live-system access.

[The runner](run_native.py) creates an isolated project, copies the current core
package into `.agents/skills/context-docs`, and commits that synthetic baseline.
Only tracked package files are copied, after checking the complete file set,
bytes and executable flags against release tag `v0.2.6`; untracked cache files are
excluded. The source revision, dirty-state
listing and release revision are recorded. It then appends a unique uncommitted recovery note and YAML fence to
`docs/current.md`. It freezes the exact prompt, fixture/package/runner/protocol
hashes and command parameters before invoking any model. The runner refuses an
existing output directory. Never change frozen inputs or repair agent outputs.

Run one fresh Codex CLI session per pass, requested `gpt-6.1-sol` at High reasoning,
using existing subscription auth, ephemeral execution and workspace-write sandbox.
Each has a 240-second cap, no API/provider fallback and no retry. Pass two uses the
same prompt, package and evidence in the same project after pass one, with no
additional evidence or coordinator edits. A failed/incomplete first session stops
execution; retain failures rather than silently rerunning them.

The native prompt supplies the refresh task, skill location, allowed write
boundary (`docs/current.md`) and execution restrictions. It supplies neither the expected answers below
nor coordinator findings. It requests no external access, application tests,
delegation, scratch files or changes to source evidence, Git state or setup.

## Acceptance criteria fixed before execution

Review semantics from the actual output and evidence, separately from mechanical
checks. Wording, headings, exact line count and a minimum amount of deletion are
not acceptance targets.

1. Replace the stale configured timeout with 30, supported by configuration.
2. Preserve approval for four retries and its rationale while identifying that
   configuration still sets two; do not claim implementation or retry tests passed.
3. Record the passed local timeout check with its one-job scope. Preserve unknown
   deployed behavior, unrun full-suite/retry/restore checks and deployment approval.
4. Keep the missing-fixture blocker, responsible person and actionable next step.
5. Keep unique uncommitted recovery-note information and its YAML fence intact;
   preserve decision rationale and proposal status in the unchanged decision file.
6. Make current state and the existing progress view consistent. Repetition may
   be consolidated if useful; retaining harmless repetition alone is not a failure.
7. Keep affected source links and anchors valid and preserve the existing layout.
8. Change only `docs/current.md`; preserve all other project/package files, adoption
   marker, original date, logging off and Git HEAD/staging state.
9. After a semantically correct first pass, the second complete pass must leave the entire project file set byte-for-byte
   identical to the first-pass result, including absence of new scratch files.
10. Reports must match what was verified and avoid claims of complete sync, live
    verification or general reliability. Inspect traces for explicit candidate
    reading and any evident scope violations; traces are not a filesystem audit.

The runner records exact file hashes before and after both passes, changed paths,
completion/exit status and Git HEAD/staging checks. It cannot determine content
correctness from equality alone. Runtime/cache bookkeeping outside the isolated
project and `.git` internals are outside the file-set equality claim.

## Decision rule and limits

If baseline passes both repair and no-change criteria, prefer a documented refresh
invocation; a new core operation has no demonstrated necessity from this case.
If it fails, identify the concrete miss before choosing a focused instruction
change and a separately frozen candidate evaluation. Do not retroactively redefine
success or present a corrected output as the original run.

Pass two tests stability of pass one's result; a stable but incorrect first result
does not pass the combined criteria. This is one explicit-invocation, one-layout, author-scored case on one client,
using fresh sessions rather than a resumed chat. It does not establish implicit
selection, instruction auto-loading, Claude behavior, broad preservation or
privacy guarantees, user-effort savings, or general no-change reliability.
