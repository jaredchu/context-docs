# Native event-history comparison

Read the [frozen protocol](protocol.md) before running. This compares recording
and fresh investigation in native Claude Code and Codex, using ordinary Markdown,
a Markdown history file, and the repository's JSONL helper. It includes no-Git
and sparse-commit projects, plus a mechanical regularly committed Git control.

```sh
python3 -m unittest discover -s evals/event-journal/native -p 'test_*.py' -v
python3 evals/event-journal/native/run.py --output .local/native-journal-new-run
```

Both CLIs must already be installed and authenticated. The runner uses client
default models, permits at most 300 seconds per session, and refuses an existing
output directory. Each run retains its frozen inputs/hashes, prompts, native
streams, file snapshots and outcomes. Temporary projects live outside this repo
so the no-Git cases cannot accidentally discover the parent repository.

This invokes real model sessions. Do not count the boundary unit tests or
mechanical Git control as agent evaluations. Review native streams and final
artifacts for evidence preservation, command scope and unsupported claims before
reporting semantic outcomes. A zero process exit alone does not prove task success.

The evaluation bridge deliberately narrows the interface. It is not a proposed
product API, skill upgrade, automatic logger, or measurement of natural CLI
usability. Claude's hook validates exact quoted bridge commands, and Codex uses
its native sandbox. Neither a prompt restriction nor this hook should be described
as operating-system confinement. Existing adopter markers and layouts are
fixtures; real package installation, automatic instruction loading, repeated
upgrade/no-change maintenance and disabling still require separate coverage.
