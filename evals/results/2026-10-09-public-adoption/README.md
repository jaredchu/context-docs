# Public-source adoption regression — 2026-10-09

Four native Claude Opus 5.5 sessions completed on pinned public Go source with
two synthetic setup overlays. All execution checks passed; three of four sessions
passed the frozen mechanical checks. The legacy adoption session preserved its
existing rule and all other files, but its code-fenced marker failed the narrower
frozen marker-format check. That failure is retained, not rescored.

Both semantic reviewers accepted all four session-specific adoption/preservation
goals. Full factual/verification acceptance differs: Astra accepts 1/4 sessions;
Claude accepts 3/4. Both reject the repeat session’s unsupported verification claim.
The assessments are retained separately; this is not a clean correctness pass.

| Session | Frozen mechanical result | Execution checks | Observed change |
| --- | --- | --- | --- |
| New adoption | Pass | Pass | Added neutral maintenance wording, marker and context; appended README navigation |
| Unchanged repeat | Pass | Pass | Every project byte preserved; original date retained |
| Legacy marker | Fail: `marker_only` | Pass | Added the three marker lines inside a `text` code fence; original `$context-docs` rule preserved |
| Legacy audit | Pass | Pass | Every project byte preserved; audit used the actual preceding output |

## Semantic review and disposition

GPT 6 Astra (requested High reasoning) implemented the harness and reviewed all
21 frozen rubric judgments. Claude Opus 5.5 reviewed the design, controls and
then the disputed semantic judgments in fresh read-only sessions. Codex integrated
the results. These are unblinded author/counterpart reviews, not independent scores.

| Session | Target behavior, both reviewers | Astra full-claim acceptance | Claude full-claim acceptance |
| --- | --- | --- | --- |
| New adoption | Pass | Fail | Pass with qualification |
| Unchanged repeat | Pass | Fail | Fail |
| Legacy marker | Pass | Fail | Pass with qualification |
| Legacy audit | Pass | Pass with qualifications | Pass with qualifications |

The [Astra review](reviews.json) retains each rubric judgment and trace evidence;
the [Claude review and integration decision](peer-review.json) retain the differing
assessment. The target subtotal concerns setup/preservation, not every general
semantic criterion. No aggregate consensus score replaces these assessments.

- **Agreed verification failure:** the repeat said it compared the documented
  `tolower` behavior against source, but its only source search returned that
  function’s declaration without the body. The documented ASCII behavior is true;
  the claimed fresh verification was unsupported.
- **Disputed severity:** the new context omits that a negative `maxcomp` disables
  the limit, and the repeat endorses that summary. Astra scores the unconditional
  API summary as too broad; Claude treats it as an edge-case omission from a
  summary supported by the upstream comment. Both see the same source guard.
- **Disputed severity:** legacy adoption incorrectly describes `notes/project.md`
  and `CLAUDE.md` as both at the root. The written path is correct. Astra counts
  this as a strict factual failure; Claude treats it as minor final-prose error.
- **Audit qualifications:** a version search returned two journal-guide lines,
  though the full guide was never opened and no history was accessed. Its
  “did not open” wording is ambiguous. The peer also notes an inaccurate marker
  line citation. Package-version compatibility was reported as uncertainty,
  not demonstrated incompatibility.

The legacy marker’s code fence preserves all existing guidance. Both reviewers
accept its meaning; the skill itself presents a fenced example. The frozen
plain-line check still fails. Before reusing the evaluator, reconcile that
constraint with acceptable presentation in a newly frozen protocol. This result
does not justify rewriting the skill around one formatting example or repairing
and rerunning these subjects.

## Evidence and frozen scope

- Source: [tidwall/match at afc69bce52e08c02e78156a7697bd808fc868ec5](https://github.com/tidwall/match/tree/afc69bce52e08c02e78156a7697bd808fc868ec5),
  six regular source/configuration/license files. No upstream code or tests ran.
- Candidate: core 0.1.5 and unreleased adoption 0.1.7 from
  `3a0c4013962b35c733dc316271f6981aaf5fe9a1`.
- Freeze commit: `5e8115e`, before subject execution. Exact prompts, source and
  package bytes, overlays, rubrics and control hashes are in [protocol.json](protocol.json),
  with its [SHA-256](protocol.sha256). The [design](../../public-adoption/protocol.md)
  and [pre-execution review](preflight.md) describe the scope and repaired controls.
- CLI: Claude Code 2.1.295; requested effort High, not independently observed.
  Responding assistant messages identify `claude-opus-5-5` in every session.
  Usage metadata also lists auxiliary `claude-haiku-5-5`; it is kept separate
  from responding-model evidence.
- Matching project `CLAUDE.md` startup-loading events, local candidate skill
  delivery and complete guard coverage were observed in all four sessions.
  There were no denied tool calls. No retries, prompt changes or artifact repairs
  occurred during the frozen study.
- [Results and artifact snapshots](results.json) preserve every session's checks,
  final reply, before/after file hashes and sanitized public/synthetic documents.
  Raw streams and hook events remain local; host paths and raw tool arguments
  are not published here.

## Limits

This is one public project, two author-created overlays and four fresh sessions,
not four independent projects. It tests explicit native invocation in a restricted
six-tool configuration. There is no ordinary-maintenance comparison, reader phase,
upstream execution, automatic-selection test or general reliability conclusion.
Author design and review are unblinded. The frozen marker checker accepts only
three bare lines with optional blank lines, so its rejection of code-fence markup
must be considered separately from whether the skill's preservation goal was met.

Before execution, 23 new mechanical controls, seven reused guard tests and
repository static checks passed. Those checks are separate from the four native
subject sessions and the later semantic review.
