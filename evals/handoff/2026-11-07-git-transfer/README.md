# Fresh-session handoff through local Git transfer

November 7, 2026. **One synthetic documentation handoff passes all eight frozen
content criteria.** This is an agent check, separate from the anonymous user
feedback and the pending observed participant trial.

## Method and result

Two fresh Claude Code 2.1.319 sessions requested and reported **Claude Opus 5.5**,
configured **High**, through existing subscription authentication. Effective
effort is not independently exposed. Each session had a 180-second limit, no
retries, no session persistence and auto memory disabled through per-session
`autoMemoryEnabled: false` settings. Only guarded file tools
were exposed; MCP, browser and delegation were disabled.

The synthetic already-adopted project used released core **0.2.6** and adoption
**0.1.15** from source commit `d74e69d3268676cf7eab19d241e8b590ddb1c60a`.
It contained project instructions, a README, an initial context entry point and
the copied release packages. Its parser-completion and test-state facts were
fixture inputs, not verified application behavior; there was no application code.
The [protocol](protocol.json) froze prompts, eight semantic criteria, initial
file hashes, command flags and helper/runner hashes before either model ran.

The first session received new synthetic owner decisions and saved only
`docs/current.md`. The coordinator committed that file in the synthetic repository
and ran `git clone --no-local` into a separate local checkout. All 20 project
files matched by hash. No conversation or earlier answer was supplied to the
second session; its prompt requested resumption from saved project files without
restating the decisions or naming a skill.

The second session read the README, transferred context and core skill. It
correctly recovered the goal, whole-queue scope, UTF-8 BOM requirement and reason,
rejected cache and reason, completed/pending work, unresolved malformed-row policy,
test limits and next step. It explicitly qualified the unverified implementation
state and left all files unchanged. Both sessions completed without tool denials
or retries. Hook events match the instruction-file hashes and show CLAUDE.md and
its AGENTS.md import loading before the first tool call in each session.

The [saved context](saved-context.txt), [sender report](sender.txt),
[receiver report](receiver.txt) and [reviewed summary](summary.json) preserve the
synthetic outputs and separate mechanical checks from Codex's semantic review.
Codex authored the case and coordinated and scored it; this is not independent
grading. The summary's seven pre-tool calls total both subject sessions.
Raw streams, hook logs and the runner are retained in local task evidence; hashes
identify the retained artifacts without exposing local paths.

The first summary export failed on a symlink-path alias. Resolving both roots
corrected the export without changing model outputs, hook events or acceptance
criteria; no subject session was rerun.

A separate fresh Opus 5.5 session, configured High, performed a bounded read-only
[report review](review.txt). It found no material overclaims or scoring errors.
Minor wording and metadata clarifications followed. That review inspected the
six report artifacts, not raw logs or the runner; it did not recompute hashes or
add an independent case or grade.

## Limits

This is one coordinator-authored and scored synthetic case, without a comparator
or independent grading. It tests documentation transfer and recovery in an
already-adopted setup. It does not test implementation, fresh adoption, general
implicit selection, unfamiliar-user effort, synchronization software or distinct
physical machines. The two checkouts ran on the same host. File-tool hooks are
not an OS sandbox; host client bookkeeping was outside the project inventory.
Native instruction events support loading in these sessions, not general
compliance or reliability. Neither these results nor the participant self-reports
establish a skill-specific accuracy advantage or measured effort savings.
