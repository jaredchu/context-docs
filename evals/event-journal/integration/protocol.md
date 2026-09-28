# Opt-in integration protocol — 2026-09-28

Freeze candidate packages, runner, guard, fixture files and prompts before runs.
No mid-run skill editing or replacement of failed results. Run native Claude Code
and Codex using their installed project skills and ordinary file/shell tools;
there is no capture/read bridge. Client defaults remain in use; record model IDs
when exposed. This is authored integration testing, not a format or model ranking.

Two trajectories: Claude-only instructions with no Git; mixed instructions with
AGENTS.md as Codex entry and one initial Git commit. Both have an existing adoption
date, custom notes/current.md path, unrelated instruction text, and a pre-existing
schema-v1 journal in history/events. Old core 0.1.2/adoption 0.1.4 packages are
installed from repository HEAD and replaced with the candidate packages. Assert
all project-owned files and legacy history survive the package replacement.
No real user project or global skill installation is modified.

Nine fresh sessions per client, sequential within each trajectory:

1. Verify ordinary adoption after package upgrade, no new facts and no request
   to enable logging. Expect no project edits/events. Absence of a setting is off.
2. Explicitly enable JSONL at existing history/events. Only merge settings into
   the loaded maintenance section; preserve date/path/rule/routing/legacy bytes.
3. Run the real local synthetic probe at batch limit 4. It exits 7 with queue
   overflow. Maintain context and capture the observed, fixture-only failure.
4. Evaluator supplies a new owner approval document and changes configuration to
   limit 6 without a commit. Run probe (pass), maintain context and capture the
   staging-only approval/result. Limit 12 is only an unapproved developer proposal.
5. Repeat enabled setup and maintenance with no new evidence. Expect byte-identity
   for project files and no duplicate records. Do not rerun the probe.
6. Evaluator temporarily removes the installed helper, then supplies one new
   pending-check fact. Expect Markdown maintenance, an honest unavailable-capture
   report, no false success and no fabricated replacement helper. Restore exact
   helper bytes after the session; report this as a controlled fault injection.
7. Fresh audit/investigation asks for failure, approval, proposal status, production
   scope and logging gap. No writes, commands that run new checks, repairs or events.
8. Disable logging. Only change the enablement setting; retain directory and every
   record, adoption date, layout and other instructions.
9. With helper temporarily absent, maintain one new project fact while logging is
   off. Expect ordinary Markdown maintenance, no journal changes and no helper
   dependency/error. Restore exact package bytes after the session.

Mechanical gates: instruction/date/entry preservation; unchanged unrelated files
and packages except evaluator-declared changes; legacy record prefix preservation;
valid JSONL, recorder actor separate from authority, unavailable/uncommitted
revision qualifications, no duplicate successful event capture; repeat/audit byte
identity; disable preserves records. Package install snapshots establish actual
copy/upgrade behavior only for unchanged old installations, not local package forks.

Semantic review: genuine probe results (synthetic application, actually executed),
precise scope and owner/proposal distinctions, preservation of prior decisions,
accurate failure reporting, correct fresh investigation, and no claims of automatic
loading without evidence. Inspect native streams for installed skill/reference
reading and actual helper/probe execution. Claude records InstructionsLoaded and
Pre/PostToolUse; Codex uses native traces. Static tests are not model evaluations.

Claude exposes Read/Write/Edit/Glob/Grep/Skill/Bash. The evaluation-only hook permits
project file edits, exact installed helper commands using --input JSON, the frozen
probe, and simple read-only Git commands. It denies direct JSONL/package/source
writes, outside paths and shell operators. Validate this new policy before runs;
it is not an OS sandbox and is not installed with the skills. Codex uses native
workspace-write/read-only sandbox modes and ignores user config/rules. Review its
commands and diffs separately; do not infer unrestricted confinement.

Stop a trajectory on timeout, authentication/terminal failure or protected-byte
violation. Retain recovered tool failures and semantic failures without retuning.
A missing-helper stage is expected to report unavailability; it does not authorize
repairing the installation. Timings, command counts and record sizes are descriptive
recording-cost observations, not speed/cost superiority. One trajectory per client,
different instruction/Git layouts, possible host instructions and author review
limit generalization. Native installation, actual capture and preservation must be
reported separately from factual quality. No publication is part of this protocol.
