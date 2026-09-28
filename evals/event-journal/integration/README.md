# Native opt-in integration evaluation

The [protocol](protocol.md) tests actual upgraded project-local skill packages,
ordinary file tools and direct helper invocations. It uses real execution of a
small synthetic probe, followed by fresh sessions for capture, repeat setup,
missing-helper handling, investigation, disabling and disabled maintenance.
There is no capture/read bridge.

```sh
python3 -m unittest discover -s evals/event-journal/integration -p 'test_*.py'
python3 evals/event-journal/integration/run.py build --output .local/optin-new
python3 evals/event-journal/integration/run.py run --output .local/optin-new --client claude
python3 evals/event-journal/integration/run.py run --output .local/optin-new --client codex
python3 evals/event-journal/integration/report.py .local/optin-new
```

Independent client trajectories can run concurrently, but each client's stages
are sequential. Existing output directories/logs are refused. Requires already
installed/authenticated CLIs; tests of the guard require neither. The runner
uses old packages from repository HEAD, so check the frozen `old_versions` before
interpreting a later run as the same upgrade. Source copies and hashes freeze the
candidate, fixture construction, requests and evaluation policy.

The [separate Claude invocation follow-up](followup-protocol.md) retains the
initial failure and puts the actual task first with native /skill-name invocation:

```sh
python3 evals/event-journal/integration/followup.py .local/optin-claude-followup
python3 evals/event-journal/integration/run.py run --output .local/optin-claude-followup --client claude
python3 evals/event-journal/integration/report.py .local/optin-claude-followup
```

Read native streams and author semantic reviews alongside mechanical reports.
Unchanged files are not proof that a skipped requested action passed. The initial
runner continues after semantic misses; dependent stages are invalid as evidence
if enablement was skipped. Process exit zero does not establish task completion.

Claude's hook permits file tools, direct helper commands with JSON input files,
the probe, and limited Git commands. It is not an OS sandbox. Its exclusion of
shell cleanup/operators creates evaluation-specific failures and means these
runs cannot establish unrestricted CLI usability. Codex uses its native sandbox;
inspect its trace and diffs separately. Global instruction influence, one case per
client, and author review limit generalization. Fault snapshots intentionally lack
a helper and retain that state; the repository checker exempts only their exact
missing links, while requiring the helper in the shipped core package.

The [durable capture-gap follow-up](gap-protocol.md) tests the demonstrated loss
of the failure reason between sessions. Use `gap.py build --output NEW_PATH`,
then `gap.py run --output NEW_PATH --client claude` and the corresponding Codex
command. Its two sessions per client use fixture-enabled logging and do not
replace the earlier lifecycle scores.
