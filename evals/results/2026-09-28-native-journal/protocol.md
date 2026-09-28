# Native logging comparison — frozen 2026-09-28

Question: do useful events survive without Git or with infrequent commits, and
what does JSONL add beyond competent Markdown recording? This is an authored,
small development evaluation, not an independent benchmark.

Run six capture sessions: Claude Code and Codex × ordinary Markdown, Markdown
history file, JSONL. Each session handles two synthetic existing adopters: no Git
and Git with one initial commit. Run a fresh read-only investigation session for
each capture. These are 12 sessions, not 24 independent trials. Use client default
models and record the actual model when exposed. No retries after a failed run.

All arms receive identical events and permission to retain useful history.
Ordinary maintenance can add dated history to its existing context. No arm is
required to delete evidence. The capture-only event feed represents ephemeral
messages/check output; it is absent from every fresh reader equally. Outcomes in
that feed are authored facts, not commands actually executed. Source IDs remain
in recorded evidence. The reader also sees the current state and, for sparse Git,
the initial committed state. A separate mechanical Git control demonstrates what
committing a historical observation preserves. No format advantage is presumed.

Installed skill packages remain unchanged. Fixtures preserve pre-existing
AGENTS.md/CLAUDE.md, original date, and custom `notes/state.md` entry. This checks
coexistence and preservation, not a completed skill upgrade or automatic loading.

The evaluation-only bridge exposes `show` and `save JSON`: all writes go to fixed
fixture paths, JSONL saves invoke the actual frozen helper CLI, and audit mode
rejects saving. Claude exposes only Bash with an exact-command PreToolUse guard;
no shell metacharacters, arbitrary Python or redirections are permitted. Validate
that guard before running. Codex uses workspace-write/read-only sandbox modes,
ignores user config/rules, and is instructed to use only that bridge. Inspect its
trace for other commands; this is not an OS confinement claim for Claude. Host
instructions may still influence clients. This constrained interface reduces
manual file/CLI discovery cost; it cannot measure ordinary unassisted usability.

Freeze protocol, runner, bridge, guard and helper hashes before execution. Retain
prompts, tool streams, final files, command outcomes and semantic author review.
Report failed execution separately. Stop that condition if capture fails.

Acceptance, separately per project and client/arm:

- Prior approved retry=3/local-only decision and memory-bound rationale survive.
- E1: staging export check failed at retry=3, exit 7, queue overflow.
- E2: retry=10 was proposed by developer, never approved.
- E3: owner approved retry=5 for staging only, constrained by memory; staging
  export check then passed. No production test/approval may be inferred.
- Facts preserve event/source IDs, authority and scope, and no Git revision is
  invented (no Git = unavailable; sparse Git = current state uncommitted).
- Reader answers all five questions correctly with record locations and does not
  claim those synthetic checks were executed by this evaluation.
- Instruction bytes, adoption date, initial history and installed packages stay
  unchanged; audit leaves all project bytes unchanged. Check journal schema and
  number of records, duplicate event capture, and captured file byte counts.

Capture duration and tool calls are descriptive overhead, not a speed ranking
(one attempt, model differences, constrained interface). JSONL wins no default
status from a tie. If all formats preserve the evidence, keep logging optional;
choose structured records only for demonstrated validation/filtering needs.
