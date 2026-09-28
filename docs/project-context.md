# Project context

Last reviewed: 2026-09-28.

## Purpose and scope

Context Docs provides a reusable skill and Markdown convention for project
continuity across AI sessions. Its primary goal is retaining useful content and
improving documentation accuracy and consistency. It addresses inconsistent
structures and maintenance drift while adapting to existing project layouts.

The public package contains instructions, references, templates and synthetic
examples. A hosted memory service, automatic scheduler and retrieval backend are
outside the first version's scope.

## Decisions

Approved by the project owner in the founding request on September 26, 2026:

- Publish an open-source project under `jaredchu` named `context-docs`.
- Begin with a reusable context standard and maintenance skill.
- Keep Markdown/Git authoritative and cloud integrations optional for later.

Initial implementation choices: MIT license; skill at `skills/context-docs`;
experimental version 0.1.0 at launch; no runtime dependencies. These are choices
made while implementing the authorized first version, not additional attributed
owner quotes.

On September 27 the owner accepted the proposed eight-task, two-condition,
three-attempt evaluation. Harbor is the selected execution framework; evaluation
dependencies are separate from the instruction-only skill package.

On September 27 the owner clarified that retained content, documentation accuracy
and consistency are the product goals. Speed and concision are secondary diagnostics.
Future comparisons should include scattered, stale or missing documentation and
measure the resulting record and fresh readers' supported answers. This clarification
does not change the already executed studies or their frozen acceptance criteria.

On September 28 the owner delegated authority to contribute changes to this
repository directly, including commits and pushes to branches. That delegation
covers contribution mechanics; it does not approve new product claims. Changes
made under it are recorded as ordinary implementation choices, and proposals
still need owner acceptance.

On September 28 the owner accepted a bounded paired native comparison: fresh
CSV/state-update cases, identical requests with and without the skills, and two
attempts per condition. The [frozen design](../evals/claude-code/paired-protocol.md)
records the implementation choices and decision rule. It does not authorize a merge.

## Current state

- Core skill supports audit, initialize and maintain operations.
- Optional [adoption skill](../skills/adopt-context-docs/SKILL.md), experimental
  v0.1.4, applies the core method and merges ongoing maintenance into the project's
  loaded agent instruction file. Install it alongside `context-docs`; it is not standalone.
  Completed setup now records a small adoption marker with the original date and
  actual entry point. Missing markers do not imply non-adoption; unrecorded dates
  remain unknown, and audit-only requests never create markers.
  New sections prefer a `Context maintenance` heading, marker, then instructions;
  existing equivalent layouts stay intact. This v0.1.2 presentation preference
  received static validation only at introduction; later model results appear below.
  v0.1.3 places the rule and marker in the instruction file the client actually
  loads, rather than assuming `AGENTS.md`, and states the rule without a
  client-specific invocation prefix. Claude Code loading depends on version,
  configuration and local instruction files; the [installation guidance](../README.md#install-in-claude-code)
  records the documented defaults and exceptions checked on 2026-09-28.
  Its [instruction-file cases](../evals/adoption/instructions.py) pass ten static
  grader controls. The [v0.1.3 merge review](../evals/results/2026-09-28-adoption-v013/README.md)
  ran nine model sessions across routing and older marker cases: eight met frozen
  acceptance. All repeats and the audit preserved bytes. Split-file routing passed
  semantic review but failed immutable-heading and installed-link checks. A
  [separate follow-up](../evals/results/2026-09-28-adoption-v013-followup/README.md)
  passed four routing/repeat sessions after making constraints explicit and
  validating declared installed references by hash across links, code spans and
  prose. Both repeats preserved bytes and dates. Skills and the original failed
  result remain unchanged. That review recommended merging within the experimental
  scope; the later native review below now recommends holding the merge.
  The earlier v0.1.0 [adoption regression](../evals/results/2026-09-27-adoption/README.md): two synthetic
  projects passed adoption and unchanged repeat passes across four fresh sessions.
  These author-reviewed cases do not establish automatic selection or general reliability.
  The [marker regression](../evals/results/2026-09-27-adoption-marker/README.md)
  retains an initial equivalent-guidance rewrite and ambiguous test dates. Ten
  sessions include targeted follow-ups; the final revision passed marker-only
  adoption and read-only auditing on the two affected unmarked cases.
- The [standard](../skills/context-docs/references/standard.md) defines document
  roles, evidence/decision distinctions and maintenance behavior.
- Two templates, an authored example and five behavioral evaluation scenarios
  are included. Templates are optional.
- Packaging, links, published-table agreement and the container-free study
  self-tests run as [static repository checks](../evals/checks/static_checks.py)
  in GitHub Actions since 2026-09-28. Package checks enforce boundaries including
  nested references and the adoption skill's declared sibling dependency; version
  checks compare current README status and latest per-skill changelog entries.
  Regression controls cover escaped package links and stale version declarations.
  These mechanical repository checks establish nothing about agent behavior.
- A [native Claude Code smoke test](../evals/claude-code/README.md) exists for skill
  discovery and invocation, rule placement in Claude-only and mixed instruction
  projects, repeat preservation and audit-only read-only behavior. It reuses the
  shared adoption fixtures. Review found and repaired three harness defects:
  ignoring frozen requests/model, excluding `.claude/` from read-only checks, and
  rejecting valid absolute installed links. Live execution then exposed inherited
  standard-input contamination and a crash on textual permission events; both are
  repaired, and read-only hash/inspection checks are preapproved. The 34 self-test
  assertions and 13 smoke-runner regression tests pass. Five paired-runner tests
  cover matched inputs, the executable CSV oracle, failure controls and frozen execution. Twelve shared-verifier tests
  include directory links containing known sources, unknown directories and
  directory anchors. Protocols freeze inputs and requests; completed responses
  with denied commands retain execution failures but allow later sessions to run.
  Authentication, nonzero exits and incomplete streams still stop the run.
  The [clean native run](../evals/results/2026-09-28-claude-code-clean/README.md)
  and [audit/discovery follow-up](../evals/results/2026-09-28-claude-code-followup/README.md)
  retain earlier factual, permission and harness failures without rescoring.
  Core v0.1.2 now tightens claim scope, decision attribution, final-report and
  resulting-state checks, and minimal README navigation. Adoption v0.1.4 requires
  evidence for automatic loading and aligns Codex metadata with the loaded file.
  Four new frozen native runs distinguish successive unreleased candidates:
  [first](../evals/results/2026-09-28-native-v014/README.md), 1/6 semantic passes;
  [second](../evals/results/2026-09-28-native-v014-followup/README.md), 5/6;
  [attribution follow-up](../evals/results/2026-09-28-native-discovery-final/README.md), 0/1;
  [final-state follow-up](../evals/results/2026-09-28-native-state-followup/README.md), 0/1.
  The second candidate passes routing, repeats and audit. The latest discovery
  preserves code/packages, creates navigation, qualifies loading and attributes
  choices correctly, but overclaims CSV value types and retains a stale no-README
  claim in its final response. All its file checks pass; a denied compound command
  fails the separate execution check. **Current recommendation: hold the merge.**
  These are different development conditions, not a pooled benchmark. Exact
  commits/hashes distinguish candidates sharing unreleased package versions.
- Installation and native behavior have been tested on Claude Code 2.1.234 with
  Claude Opus 5, with mixed results. Other clients remain unevaluated.
- Public repository: [jaredchu/context-docs](https://github.com/jaredchu/context-docs).
- Current package: experimental core skill v0.1.2; standard/resources remain v0.1.0.
  The package is instructions only, with no background maintenance or sync.
- Completed studies cover initialization, stale/conflicting guidance, decision
  preservation, uncommitted work, links, audit-only behavior and repeated maintenance.
  The [dated evaluation summary](evaluation-summary-2026-09-27.md) preserves all
  prior study summaries, frozen versions, outcomes and validation details.
- Reviewed results support supervised use, but establish no general accuracy,
  speed, cost or correctness advantage over competent ordinary maintenance.
  Reader results often tie because common source evidence remains available.
- Retain the [private-pilot deployment-conflict miss](evaluation-2026-09-26.md)
  and [history-study temporary out-of-scope backup](evaluation-2026-09-27-history.md)
  when assessing reliability; perfect content scores do not prove full compliance.
- Unnamed selection was observed in native discovery runs; reliable automatic selection,
  general cross-client behavior and long-term maintenance remain unestablished.
  Prior controlled Codex runs excluded host/global instructions; native smoke tests
  have weaker local isolation. Authoring and review were not independent or blinded.

## Next actions

1. Use the recorded native failures to guide review before further prompt tuning.
   Avoid adding rules for isolated examples. Cloud adapters still need a concrete
   retrieval or cross-machine use case.
2. Seek independently contributed histories from other projects and condition-blind
   review before expanding correctness claims. Keep common raw-evidence access,
   verified context reading, a competent ordinary baseline and frozen criteria.
   Repeating the current searchable questions is unlikely to distinguish accuracy.
   Include command-scope review alongside project-file checks; the temporary backup
   violation shows those mechanical rewards do not establish full task compliance.
   Preserve all earlier results and the original private-project miss.
3. Evaluate selection reliability, other models, normal global-instruction setups
   and longer maintenance sequences when relevant. Native evidence now includes
   unnamed selection but does not establish reliable cross-client behavior.
4. Proposed, not yet approved: address the three conditions that hold reader and
   document scores at a ceiling before running further comparisons. The shared
   task prompts already state much of the skill's guidance to both arms, the
   fixture evidence labels its own approval and observation status, and the
   question sets stay answerable from small raw inputs. Until those change, a tie
   is the expected result and cannot distinguish the methods. See the
   [discrimination protocol](../evals/discrimination-protocol.md).
5. Preserve the initial v0.1.3 failure, passing Codex follow-up and mixed native
   results as separate evidence. Installed-path portability across machines remains
   untested. Do not promote these small studies into reliable-support claims.
6. Keep the current branch unmerged while discovery factual consistency remains
   unresolved. Further changes need concrete claim evidence and independently
   contributed cases, rather than more prompt tuning on this single fixture.
   Retain all attempts and separate execution failures from factual errors; do not
   silently repair scored artifacts. Native coverage does not make the new core
   revision a full rerun of the earlier Codex maintenance studies.

## Canonical references

- [README and installation](../README.md)
- [Skill entry point](../skills/context-docs/SKILL.md)
- [Evaluation scenarios](../evals/README.md)
- [Completed quality and fresh-reader study](evaluation-2026-09-27-quality.md)
- [Larger public-source pilot](evaluation-2026-09-27-public.md)
- [README routing and verified reading](evaluation-2026-09-27-routing.md)
- [Public decision histories across sessions](evaluation-2026-09-27-history.md)
- [Quality-first comparison protocol](../evals/quality-protocol.md)
- [September 26 local-project benchmark](evaluation-2026-09-26.md)
- [September 27 public Harbor evaluation](evaluation-2026-09-27.md)
- [Concision comparison and v0.1.1 adoption](evaluation-2026-09-27-concise.md)
- [Contribution guidance](../CONTRIBUTING.md)
- [Per-version changelog](../CHANGELOG.md)
- [Proposed discrimination protocol](../evals/discrimination-protocol.md)
- [Native Claude Code smoke test](../evals/claude-code/README.md)
- [September 28 Claude Code handoff and open decisions](handoff-2026-09-28-claude-code.md)
