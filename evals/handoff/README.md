# Fresh-session continuation pilot

This separate synthetic pilot tests whether supplied curated project context plus
an explicit entry-point instruction helps a fresh reader continue a small coding
task. It does not test skill activation or the process that produced the context.
Historical studies and released skills are unchanged.

The two arms have identical starting Python code, tests and raw notes. Only the
curated arm adds a summary, a README entry-point link and a routing sentence in
the task. The baseline can find every underlying fact in ordinary notes. Skills
are disabled in both arms. The frozen manifest contains the exact inputs, prompts,
acceptance criteria, execution bounds and harness hashes; subjects cannot access
it through the guarded file tools.

Build in a new temporary directory outside repositories and ancestor instructions:

```sh
python3 evals/handoff/build.py /private/tmp/context-docs-handoff-NEW
```

Before running, add the SHA-256 of `evals/handoff/run.py` to the manifest's
`harness_hashes` and regenerate `protocol.sha256`. Freeze these inputs before any
agent execution. Review the protocol with:

```sh
python3 evals/handoff/run.py /private/tmp/context-docs-handoff-NEW preflight
```

Inspect that review and record `preflight-verdict.json` with
`accepted_by_coordinator: true` only if the execution and comparison gates pass.
Then run exactly one attempt per arm:

```sh
python3 evals/handoff/run.py /private/tmp/context-docs-handoff-NEW subjects
```

No retry, resume, fallback, paid API credentials or global-setting edits are
permitted. The launcher reuses the native Claude Code smoke runner; the hook
reuses its observation and event recorder, adapting the editable scope to two
Python files and permitting only the fixed fixture test command. Hooks are tool
controls, not an OS sandbox. Python imports may create bytecode caches; those
are execution artifacts, not agent-authored scope changes. A counterpart review
can inspect the coordinator's `assessment.json` with the `review` mode.

Budget: preflight review 180 seconds, curated 420, scattered 420, final review
180; at most 20 minutes of agent execution in total. Fixed order is a limitation.
Use existing Claude.ai subscription authentication and exact `claude-opus-5-5`;
stop if responding model, completion or instruction-isolation gates fail.

Report each criterion as pass, fail or not tested with evidence. Retain raw
streams, hook events, final files, patches and failures. Separate execution
validity, mechanical checks, semantic review and estimated correction need.
No actual human correction is introduced during the run; correction effort is
therefore not directly measured. Time and tool calls describe observed effort,
not subscription allowance savings or statistical significance.

[October 10 artifacts](../results/2026-10-10-handoff/README.md).
