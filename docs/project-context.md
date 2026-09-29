# Project context

Last reviewed: 2026-09-29.

## Purpose and scope

Context Docs provides a reusable skill and Markdown convention for project
continuity across AI sessions. Its primary goal is retaining useful content and
improving documentation accuracy and consistency. It addresses inconsistent
structures and maintenance drift while adapting to existing project layouts.

The package contains instructions, references, templates and an optional Python
journal helper. Ordinary Markdown maintenance needs no runtime. A hosted memory service, automatic scheduler and retrieval backend are
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
dependencies were separate from the then instruction-only skill package.

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

On September 28 the owner approved merging PR #1 after reviewing the guarded
follow-up and its experimental-support recommendation. The merge retains the
documented factual limitations and does not establish general reliability.

On September 28 the owner authorized implementing an optional JSONL event-journal
pilot, keeping Markdown as curated context and evaluating usefulness during real
work. Its CLI, schema and three-session trial procedure are implementation choices,
not an approved universal logging requirement.

The owner subsequently authorized proceeding with the three-session live trial
in this repository. The temporary project instruction and tracking layout are
implementation choices; this does not mandate logging for skill adopters.

The owner then clarified the logging objective: record events efficiently so their
history is available when needed. Better current context, routine handoff speed
and context savings are not acceptance criteria for logging. This supersedes the
assistant's inference that the context-retrieval trial justified ending useful
event capture; it does not rescore earlier tests or prove logging reliability.

The owner added three logging requirements: include actual Claude testing and
evaluation, make updates compatible with already adopted Context Docs projects,
and establish whether additional logging is necessary alongside Markdown/Git.
The third question takes priority over assuming a separate JSONL store is needed.
The owner also identified projects without Git or with infrequent commits as
logging use cases. Evaluate event preservation there without assuming JSONL is
necessary: Markdown history can also survive independently of commits.
Concrete comparison and upgrade criteria are recorded in the
[journal requirements](event-journal-pilot.md#requirements-before-broader-integration).

The owner then authorized the minimal opt-in integration: package the helper with
the owning skill, leave logging off by default, exercise real incremental capture
in Claude and Codex, and verify upgrade/repeat/audit/disable preservation. The
settings and version increments are implementation choices within that scope.

On September 28 the owner authorized publishing the experimental v0.1.3 release,
including the merged Claude work, upgrading local global skills and enabling
logging. This repository opts in through its existing AGENTS.md section, with
CLAUDE.md importing that file; other projects keep their existing settings.

On September 29 the owner approved an opt-in auto preference: enable logging only
when no explicit project setting exists and Git confirms the project is outside
a repository. Explicit off/on settings win; unknown Git status leaves settings
unchanged. Save enablement in project instructions and preserve it if Git is later
added. This is setup convenience, not a decision that every non-Git project needs
logging. The preference line and read-only policy helper are implementation choices.

## Current state

- Unreleased core 0.1.5/adoption 0.1.6 implement the optional
  [auto preference](../skills/context-docs/references/event-journal.md#optional-auto-preference).
  [Native checks](../evals/results/2026-09-29-auto-preference/README.md) retain two
  Codex harness blocks and four functional passes. Both clients preserve explicit
  settings, custom paths and history; repeat after Git and audits write nothing.
  Claude still enumerated journal filenames and retained guard denials. Eight new
  policy tests and affected mechanical checks pass separately. Local global skills
  remain core 0.1.4/adoption 0.1.5; this project's explicit setting is unchanged.
- Core skill supports audit, initialize and maintain operations.
- Core 0.1.4 adds an explicit journal read decision: no-change
  maintenance stops after current context and supplied evidence unless new work,
  a contradiction or an uncertain write needs history. Enabled settings and history
  links alone do not trigger journal access. The helper/schema and adoption 0.1.5
  remain unchanged. A [twelve-session follow-up](../evals/results/2026-09-28-read-gating/README.md)
  found Codex and Claude direct-read trajectories preserve capture/investigation
  while avoiding history on repeat. Earlier Claude path/selection failures remain
  recorded; a native Skill call selected the released global copy. The final Claude
  condition disables that lookup and verifies candidate file reads. These are
  narrow behavior checks with execution/factual qualifications, not general
  reliability or cost evidence. Global packages stayed at released versions during
  that isolated study; the later authorized upgrade is recorded below.
- Local global Codex and Claude skills now contain core 0.1.4/adoption 0.1.5;
  prior copies are backed up. The [global acceptance check](../evals/results/2026-09-28-global-v014/README.md)
  retains five sessions: initial Claude slash-only loading failed, and an explicit
  Skill control loaded the body but enumerated history. A two-sentence known-path
  clarification then passed no-history-access in both Codex and explicit native
  Claude Skill invocation. All project/package bytes were preserved. Native
  slash-only and automatic selection reliability remain unestablished. The
  [v0.1.4 release notes](releases/v0.1.4.md) retain those limits. The owner-authorized
  [experimental prerelease](https://github.com/jaredchu/context-docs/releases/tag/v0.1.4)
  is published at `bf292ef4fd74`, whose [complete CI suite](https://github.com/jaredchu/context-docs/actions/runs/36442131106)
  passed. Both local global installations match the tagged packages; logging
  remains enabled only for this repository, with existing records preserved.
- A [six-session global-installation check](../evals/results/2026-09-28-global-journal/README.md)
  used the released packages in fresh Codex and Claude sessions. Both captured a
  synthetic failure without an extra logging reminder; repeats and audits preserved
  all project bytes, with no duplicate events or global package changes. Claude's
  fixture loaded CLAUDE.md and its AGENTS.md import. However, both clients reread
  history during no-change maintenance; Claude also retained guard denials, a
  temporary payload and qualified audit wording. Functional passes do not establish
  efficient or unrestricted behavior. That evaluation tested only project opt-in;
  the later optional auto preference is described above.
- Core v0.1.3 packages the optional [schema-v1 journal](event-journal-pilot.md)
  and its portable guide; adoption v0.1.5 merges explicit project settings.
  Logging defaults off, including existing adopters. It has no background capture,
  cleanup or mandatory runtime; the optional helper requires Python 3.9+.
  The repository command remains a compatibility entry point to that one helper.
  [Earlier mechanical tests and replay](../evals/results/2026-09-28-event-journal/README.md)
  and the [same-chat trial](event-journal-live-trial.md) remain historical evidence.
  The [12-session native format comparison](../evals/results/2026-09-28-native-journal/README.md)
  found requested facts retained in all formats, with factual/execution errors;
  it establishes no JSONL necessity or speed advantage.
- The [native integration study](../evals/results/2026-09-28-journal-integration/README.md)
  tests actual old-package replacement and direct installed-helper use. Codex's
  nine-stage lifecycle passed functional capture/preservation. Claude's original
  nine sessions skipped setup and remain failures; a separately frozen task-first
  native-invocation follow-up passed functional stages with semantic and guard
  qualifications. Original dates, custom paths, instruction wording and legacy
  history survived; repeat/audits wrote nothing; disabling retained all records.
  Normal maintenance continued with the helper absent.
- A [four-session capture-gap follow-up](../evals/results/2026-09-28-journal-gap/README.md)
  addresses failure reasons previously retained only in chat. Both clients now
  preserve a concise gap note in existing Markdown; fresh readers recovered the
  actual historical cause after helper restoration without writing/backfilling.
  Frozen hashes identify the unreleased core candidates. A final clarification
  covers unconfirmed writes and received static review only. General accuracy,
  unrestricted-client reliability, implicit selection and a recording-cost
  advantage remain unestablished. These evaluations used isolated installations
  and synthetic adopters; they did not change global skills or real adopter projects.
- Optional [adoption skill](../skills/adopt-context-docs/SKILL.md), experimental
  v0.1.5, applies the core method and merges ongoing maintenance into the project's
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
  scope; a later native review held the merge until the guarded follow-up below.
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
  cover matched inputs, the executable CSV oracle, failure controls and frozen
  execution. Seven observer/guard tests cover path escapes, protected writes, loading
  event hashes and call/decision correlation. Twelve shared-verifier tests
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
  The second candidate passes routing, repeats and audit. The final targeted discovery
  preserves code/packages, creates navigation, qualifies loading and attributes
  choices correctly, but overclaims CSV value types and retains a stale no-README
  claim in its final response. All its file checks pass; a denied compound command
  fails the separate execution check. That development review held the merge.
  These are different development conditions, not a pooled benchmark. Exact
  commits/hashes distinguish candidates sharing unreleased package versions.
  The subsequent [paired study](../evals/results/2026-09-28-native-paired/README.md)
  completed eight fresh sessions with identical requests, ordinary/skills conditions
  and two attempts per case. Skills were unchanged. CSV target accuracy is 0/2
  ordinary versus 1/2 skills; stale-state reconciliation passes in both conditions.
  All eight sessions pass project-file checks. Strict semantic acceptance is 2/4 ordinary
  versus 1/4 skills, but two skills failures are solely unverified loading
  confirmations, not demonstrated false assertions. The missing early check phrase
  cannot prove non-loading. Scope review finds scratch writes in two ordinary and
  one skills session. That study retained the hold for verification evidence and
  scope limits without establishing a skill-specific cause of the original errors.
  The owner then requested the next integration step; this is a separately frozen
  condition, not extra retries of the paired study.
  The [guarded follow-up](../evals/results/2026-09-28-native-guarded/README.md) passes
  all four integration sessions. Native InstructionsLoaded events confirm startup
  loading with matching hashes, including the newly adopted rule in a fresh audit.
  The outside write probe is denied, the inside probe succeeds, and every tool call
  is covered by the guard. The audit preserves all bytes. CSV semantic review still
  fails on the universal string-value claim; the other three reviews pass, including
  the boundary control. **Current recommendation: experimental merge, with factual
  limits and no unrestricted-client reliability claim.** The evaluation-only guard
  exposes six file/skill tools, excludes shell execution, and is not an OS sandbox.
  That evaluated instruction-only candidate did not install the guard. No skill
  revision or merge was performed during that follow-up.
- Installation and native behavior have been tested on Claude Code 2.1.234 with
  Claude Opus 5, with mixed results. Clients beyond Codex and Claude Code remain unevaluated.
- Public repository: [jaredchu/context-docs](https://github.com/jaredchu/context-docs).
- Experimental Claude Code changes were merged into `main` on September 28 in
  [PR #1](https://github.com/jaredchu/context-docs/pull/1), merge commit `998ff774eec9`.
- Current working package: unreleased core skill v0.1.5 and adoption v0.1.6; standard
  remains v0.1.0. The core includes the optional schema-v1 helper; normal Markdown
  maintenance needs no runtime. There is no background maintenance or sync.
- The owner-authorized [v0.1.3 prerelease](https://github.com/jaredchu/context-docs/releases/tag/v0.1.3)
  is published at `b4233576db78`, including the merged Claude work. The
  [release notes](releases/v0.1.3.md) retain evaluation limits and the initial CI
  failure; the repaired commit passed the complete GitHub Actions suite.
  At publication, local global copies matched core 0.1.3/adoption 0.1.5;
  previous Codex copies were backed up. Both installed helpers passed a read-only
  journal check. No other project's logging settings were changed.
  Logging is enabled for this repository in `.context/events`, preserving the
  original adoption date, entry point and historical records. CLAUDE.md imports
  AGENTS.md so both clients can share the settings; live automatic loading in
  a new Claude session has not been verified during release preparation.
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

Keep logging optional and preserve the [integration findings and limits](../evals/results/2026-09-28-journal-integration/README.md).
The bounded upgrade/capture/repeat/audit/disable checks are complete, including a
focused durable-gap repair. Use explicit native skill invocation for Claude when
evaluating the released skills; initial skipped requests remain evidence. Further
expansion needs a concrete use case and varied real-project histories, not more
format comparisons on these fixtures. Customized package merges, other platforms,
high event volumes and natural recording effort remain outside the completed tests.
The v0.1.4 read-gating guidance addresses unnecessary journal reads in the focused
conditions above, now including explicit native selection of the updated global
Claude skill. Retain the failed slash-only request and broader invocation limits
when reviewing the prerelease; varied-project efficiency remains unmeasured.

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
6. The paired study and guarded follow-up are complete. The restricted integration
   gates pass, and PR #1 is merged with its factual limitations retained.
   Preserve earlier scores and avoid further tuning
   on these fixtures. Use the observer and boundary checks for future native
   evaluations; adding executable tools requires a new confinement design and
   validation. General reliability still needs varied projects and independent review.

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
