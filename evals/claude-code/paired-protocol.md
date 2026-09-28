# Bounded native paired comparison

Approved by the user on September 28, 2026, after the retained discovery failures.
This tests the current, unchanged core 0.1.2 / adoption 0.1.4 against ordinary
Claude Code on two newly authored cases. They are development fixtures, not
independent or held-out validation.

## Design frozen before execution

Eight fresh sessions: two cases × two conditions × two attempts. Both conditions
receive identical requests, project files and tool permissions. Order within each
case is ordinary, skills, skills, ordinary. This counterbalances order without
pretending that repeated model responses are deterministic paired observations.

- `delimited-records`: a semicolon-delimited reader with normal, missing and
  surplus fields in one sample. Initialize context, README and maintenance rules.
- `front-door-refresh`: preserve existing scope/unknowns while creating a README,
  extracting usage and adding a maintenance rule. Current notes initially describe
  those features as absent. The agent must reconcile the resulting state.

The skills condition installs both complete packages under `.claude/skills/` and
leaves native selection enabled. Ordinary has neither package and uses
`--disable-slash-commands` to prevent host skill selection. That flag and installed
package availability are the intended treatment; user requests are identical.
Record actual calls/reads. Missing skill exposure or baseline contamination makes
the affected comparison inconclusive, not evidence about the skill's content.

Both use Claude Code 2.1.234 and requested model `claude-opus-5`, project settings,
strict MCP configuration, empty stdin, fresh sessions and no session persistence.
The available tool set excludes delegation and network tools; fixed permissions
include source/sample execution via `python3`. These local tool rules are not a
sandbox. Inspect tool traces for scope violations and retain permission denials.
User/global instruction presence is recorded; no host instructions are edited.

Each initial CLAUDE.md contains an innocuous first-reply check phrase. Its
appearance before any file-reading tool supports initial instruction exposure.
Appearance only after an explicit read does not establish automatic loading.
Do not score a later read as loading evidence. Also review unsupported loading
claims in documents and final responses. This probes initial instructions, not
fresh-session loading of the newly added maintenance rule.

## Scoring and decision rule

`protocol.json` freezes all initial file hashes, exact requests, criteria, model,
permissions, ordering and package hashes. Commit it before running. The runner
checks hashes before any model call, consumes frozen requests and never overwrites
a run. Authentication/incomplete execution stops the remaining run; a completed
permission denial remains failed but permits later sessions. No automatic retries.

Five semantic criteria per case cover useful navigation/content, target accuracy
or retained decisions, resulting-state consistency, factual/authority scope, and
maintenance/preservation. Review all artifacts and final replies, plus traces
supporting verification claims. Mechanical file/link/byte checks and execution
failures remain separate. Reference/failing controls run before model sessions;
actual synthetic code output supplies the CSV oracle. Review is author-conducted,
not independent or blinded. Ordinary does not need a Context Docs marker or name.

A same-case semantic criterion failing in both skills attempts while passing in
both ordinary attempts is a repeatable adverse association requiring investigation,
not proof of causality. Shared or inconsistent failures are inconclusive. With no
observed skill-specific regression and no preservation/scope blocker, experimental
merge may be considered with explicit limitations; this small study cannot prove
reliability, equivalence or a skill advantage. Incomplete or contaminated pairs
cannot clear a hold. Keep all earlier failures and do not tune prompts or add model
runs within this bounded study. Any follow-up requires its own frozen protocol.

## Commands

```sh
python3 -m unittest discover -s evals/claude-code -p 'test_*.py'
python3 evals/claude-code/paired.py build /tmp/context-docs-paired --model claude-opus-5
# Copy and commit protocol.json before execution.
python3 evals/claude-code/paired.py run /tmp/context-docs-paired
python3 evals/claude-code/paired.py report /tmp/context-docs-paired --reviews reviews.json
```

The cases, runner and report generator are in [paired.py](paired.py); mechanical
controls are in [test_paired.py](test_paired.py). The existing [smoke runner](smoke.py)
provides stream parsing, client execution and installed-reference validation.
