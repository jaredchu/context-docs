# Focused source selection during adoption

This synthetic fixture isolates the stale-source finding from the
[local-only follow-up](../local-only/validation-2026-10-10/README.md). Ignored old
notes report a configured timeout of 10 seconds; `config/service.yaml` sets 20.
The notes also contain an owner-approved SQLite decision and migration rationale,
a dataset blocker and next step, and a private canary. The subject receives the
adoption request and supplied skills, without the expected timeout or suspected
failure. The repository and installed setups are outside the subject workspace.

The focused fixture starts with personal exclusions for both the notes and local
context. This isolates source selection from writing the ignore file. Before
writing, the agent still needs to verify that context is ignored and untracked.
Only the context entry point and the agreed shared instruction marker/rule may
change. Existing files, Git index/history and skill packages must stay intact.

## Checks

Run the mechanical regression controls without model access:

```sh
python3 -m unittest discover -s evals/source-selection -p 'test_*.py'
```

The controls reject no-op output, verbatim stale notes, loss of the SQLite
rationale or dataset work, and a shared canary leak. A source-backed reference
passes while retaining the old value explicitly as superseded evidence. The seven
tests also reject edits to source/configuration/package files and accidental
tracking of local context. The gates are necessary checks, not a semantic grader:
inspect decision authority,
whether 10 is still presented as current, runtime/deployment qualifications,
next actions, link resolution, shared details and pre-write Git checks separately.

For a fresh bounded native attempt, choose an output directory that does not exist:

```sh
python3 evals/source-selection/run_native.py prepare --out /tmp/source-selection-trial
python3 evals/source-selection/run_native.py run --out /tmp/source-selection-trial
```

The runner copies the current packages, creates an independent Git fixture and
freezes its hashes, prompt, criteria and runner/helper identities before execution.
It requests GPT 6.1 Sol with medium effort, rejects API/provider overrides, uses
subscription credentials through an isolated Codex home, bounds execution to 180
seconds, and refuses to overwrite an attempt. Exact Codex responding model
identity is not independently confirmed. An optional `--client claude` requests
Opus 5.5 and checks the returned identity; it was not used for subject trials here.
Claude tool restrictions are prompt constraints rather than an OS sandbox.

## October 10 result

Released core 0.1.8/adoption 0.1.9 reproduced the stale-source issue in one of two
fresh source-selection attempts: the resulting current-state section recorded
10 and did not consult the configuration. The other attempt used 20, reported
the conflicting notes and preserved their decision and pending work. Both
preserved the sharing boundary. An earlier attempt with no context exclusion
could not write the root Git ignore file under the native sandbox; it reported
incomplete adoption and created no context. That blocked attempt and the unused
second original fixture are retained, rather than counted as source outcomes.

The core 0.1.9 candidate adds three lines to the initialization guidance. Both
matched candidate trials record the 20-second configuration, distinguish the old
notes, preserve approved rationale and pending dataset work, and verify storage
before writing. Neither claims runtime verification or future instruction loading.
The [summary](summary.json) records all five attempts, package and fixture hashes,
mechanical gates, semantic inspection and focused counterpart review. Earlier
study artifacts are unchanged. These author-created,
direct-invocation trials establish neither general reliability nor a comparative
accuracy benefit; they do not test implicit skill selection or future-session
instruction loading. Raw traces and frozen workspaces remain local.
