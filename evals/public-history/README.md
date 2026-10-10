# Public-history execution harness

The [plan](../public-history-plan.md) and [evaluator ledger](../public-history-ledger.md)
define this four-session source-inspection study. `build` and `validate` do not run
models. The parent study owner freezes and authorizes the final runtime manifest
before `run`; no retry or resume command exists.

```sh
python3 evals/public-history/test_run.py
python3 evals/public-history/run.py build /private/tmp/context-docs-public-history-20261010
python3 evals/public-history/run.py validate /private/tmp/context-docs-public-history-20261010 --frozen-sha256 HASH
python3 evals/public-history/run.py run /private/tmp/context-docs-public-history-20261010 --frozen-sha256 HASH
python3 evals/public-history/run.py export /private/tmp/context-docs-public-history-20261010 OUTPUT.json
```

Build reads the verified full trees in `.local/public-history-snapshots/` and their
adjacent Git-blob manifests, plus the before files and fix diffs in
`.local/public-history-scout-20261010/`. It retains internal upstream symlinks and
binary files and checks Git blob IDs and executable modes. No upstream code runs.
Build installs only the core package from the `v0.1.6` Git commit in skill arms.

Both arms receive the same neutral `CLAUDE.md`, tools, settings and domain task.
`--disable-slash-commands` disables native/global skills in both arms. The skill
arm's additional instruction requests a complete `Read` of the frozen core file.
Successful returned text must contain every nonempty file line in order. This is
controlled file delivery, not evidence of native discovery or a Skill-tool call.
The launcher requests high effort; actual responder model IDs are checked, while
effort remains a requested setting rather than independently observed behavior.

The guard exposes only Read, Grep, Glob, Write and Edit. Each session can read its
own project and read-only evidence. Writes are restricted to the named handoff and
README; every proposed README write/edit must preserve its original byte prefix.
The hook denies shell, network, delegation, external paths, symlink writes and
ambiguous edits. It reuses the existing hook observer and stream coverage checks.
This restricted-tool harness is not an OS sandbox or a universal Claude isolation
claim. Ancestor/user/managed instruction checks and observed loading guard the
declared inputs; hidden system prompts are not inspected.

The manifest freezes prompts, model/client, 600-second budget, package, source
trees, evidence, hooks, criteria and harness hashes. Run checks drift before each
session and stops on infrastructure failures, retaining attempted logs and output.
Properly denied requests, 600-second timeouts and incomplete skill delivery are
reported as subject outcomes and do not alone stop the remaining sessions. Their
failed completion/delivery checks remain false. Integrity failures still stop.
Exports list planned, attempted and unrun sessions and any stop reason. Diagnostic
errors preserve partial checks; invalid UTF-8 artifacts use replacement decoding
with an explicit validity flag. No final artifact score is inferred by the harness.

Raw streams, hooks and runtime configs remain outside the repository. Export
selects final handoffs, README additions, final messages, byte hashes, scope and
returned-result hashes. It omits upstream source bodies, startup metadata and raw
host paths. Review raw source-read contents locally when assessing semantic claims.
