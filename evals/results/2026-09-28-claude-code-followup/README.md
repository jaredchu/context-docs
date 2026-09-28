# Native audit and discovery follow-up — September 28, 2026

**Audit passes; unnamed discovery selects the skill but fails grounded-content
review and execution checks. Recommendation: hold the merge pending the factual
issues below.** This supersedes the earlier experimental-scope merge recommendation,
not any retained score. The branch is unmerged.

## Frozen setup and outcomes

Protocol frozen in `b8e40b1`, harness `b473c65`, CLI `2.1.234`, requested and
observed model `claude-opus-5`. Core skill `0.1.1` and adoption skill `0.1.3` are
unchanged. The follow-up contains two fresh fixtures, not continuations of prior
model sessions. Requests and rubrics match the corresponding earlier protocol.
The only new preapproved tool rule is read-only `Bash(shasum:*)`; standard input
remains closed, and the parser now handles textual system permission events.

| Session | Skill evidence | Mechanical | Semantic |
| --- | --- | --- | --- |
| Audit-only | Installed core skill read after named invocation | Pass | 2/2 |
| Unnamed discovery | Explicit `Skill(adopt-context-docs)` call | Fail: permission denials | 2/3 |

The [preceding clean run](../2026-09-28-claude-code-clean/README.md) passed four
routing/repeat sessions and completed an audit that encountered a permission
denial and parser crash. Its five sessions and this follow-up's two sessions are
separate conditions; do not describe them as a single six-session pass.

## Findings

1. **Discovery recorded incorrect package versions.** Its final `context.md`
   claims that both installed skills have VERSION `0.1.0`. The frozen protocol
   and installed files identify core `0.1.1` and adoption `0.1.3`. The session read
   the skills and standard, but no recorded call read the VERSION files. The
   incorrect claim survives in the final artifact, failing the rubric's grounded
   context requirement.
2. **Discovery inferred publication history without evidence.** It says that no
   Git remote is configured, "so nothing has been published from this clone."
   Present remote configuration does not establish historical publication. The
   absence should have been recorded without that conclusion.
3. **Audit overclaimed automatic instruction loading.** It asserts that AGENTS.md
   was loaded because it was the only instruction file. The trace shows an explicit
   Read of that file; it does not establish automatic loading. This contradicts
   the repository's caution against inferring client loading solely from names.
   The two frozen audit criteria assess marker interpretation and no edits, so
   both pass; this additional factual issue remains visible rather than changing
   those criteria after execution.

Discovery also omitted a README or documentation index, offering to add one later.
It made context reachable from CLAUDE.md, but that does not complete the core
skill's README/index orientation step. This is recorded separately from the
clear factual failures above.

Three discovery shell commands were denied: one compound converter check, running
a scratchpad verification script, and a Git object-hash check. The final response
acknowledged that its converter checks were not executed. All project-file checks,
including code preservation, installed-package hashes, links, and unnamed skill
selection, passed. `no_execution_error` alone failed mechanically. These permission
failures are execution limitations; they do not excuse the false document claims.

## What worked and how it was reviewed

The audit left the complete project tree byte-identical, distinguished adoption
from a missing marker, and correctly recommended `Adopted: unknown` for an
unrecorded historical date. Discovery selected the adoption skill from an unnamed
request, preserved `convert.py`, and created context.md plus CLAUDE.md with one
dated marker and a maintenance rule valid for this client.

Codex performed author review of snapshots, complete-tree hashes, final responses
and tool calls/results against each frozen rubric item. This was not independent
or blinded. Scope review also observed a client scratchpad script outside the
fixture and an inspection of an absent client memory directory. Thus project-only
checks must not be interpreted as proof of no host filesystem activity.

- [Frozen protocol](protocol.json), [trials and snapshots](trials.json), [explicit reviews](reviews.json)
- [Summary](summary.json), [generated table](table.md), [provenance](provenance.json)
- [Audit transcript](logs/audit-only-pass-1.jsonl), [discovery transcript](logs/discovery-pass-1.jsonl)

Paths in published excerpts are normalized; original streams are retained locally
with SHA-256 provenance. The client/model, small synthetic cases, author review,
local execution without a container, and one attempt per condition limit the
conclusion. Unnamed selection was observed once; general selection reliability,
cross-client equivalence and cross-machine path portability remain unestablished.

## Next step

Address the grounded-content and instruction-loading findings without silently
repairing these outputs or changing their scores. Reuse existing guidance where
possible; avoid adding a universal rule for one isolated example. Then freeze and
run a targeted regression before reconsidering the merge recommendation. Preserve
the [authentication failure](../2026-09-28-claude-code/README.md),
[contaminated attempt](../2026-09-28-claude-code-retry/README.md), and initial
[clean-run permission failure](../2026-09-28-claude-code-clean/README.md).
