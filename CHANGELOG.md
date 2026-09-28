# Changelog

Each installable skill under `skills/` carries its own version in a `VERSION`
file and moves independently. The repository tags `v0.1.0` and `v0.1.1` name core
skill releases only; `v0.1.3` bundles core 0.1.3 and adoption 0.1.5, including
the previously merged Claude changes. Later entries identify the package they change. Versions are
reconstructed here from the commits and dated reports they were published with,
so the history is auditable without reading every evaluation document.

Every entry states what was actually tested. A static check or an authored example
is not a behavioral evaluation, and adopting a version is an implementation choice,
not a demonstrated accuracy gain.

Release contents and validation are summarized in the [v0.1.3 release notes](docs/releases/v0.1.3.md).

## context-docs 0.1.4 — unreleased

- Decide whether historical evidence is needed before accessing the journal.
  No-change maintenance checks current context and supplied evidence, then stops
  without listing, searching or reading journal files unless a contradiction or
  uncertain write requires it. An enabled setting or history link alone is not a
  read trigger. Preserve new-event capture and targeted historical investigations.
- Clarify that the helper's own append validation still runs and a successful
  append returns its record; extra history reads need a concrete reason.
  Helper/schema and adoption version are unchanged.
- The [read-gating follow-up](evals/results/2026-09-28-read-gating/README.md)
  retained twelve native sessions. Codex's initial trajectory and Claude's final
  direct-read trajectory capture one event, avoid all journal access on repeat,
  and investigate history without writing. Earlier Claude helper-path and global
  skill-selection failures remain separate evidence; candidate bytes were unchanged.
  Claude guard/cleanup and audit wording limits remain. Both metadata validators,
  thirteen checker regressions, six guard assertions and static checks pass.
  Global installations and released tags are unchanged; this is not a cost study.
- A later [five-session global acceptance check](evals/results/2026-09-28-global-v014/README.md)
  upgrades both global installations with backups. Codex passes; Claude's initial
  slash-only request does not load the skill. Explicit native Skill loading skips
  event contents but still enumerates history through a broad search. Add two
  sentences directing unchanged maintenance to known entry-point paths. The final
  Codex and explicit native Claude checks then avoid all journal access and writes.
  Preserve the earlier failures and distinct candidate hashes. All 90 local
  regression tests, study controls, metadata and static checks pass separately.
  The [v0.1.4 draft notes](docs/releases/v0.1.4.md) retain invocation limits.

## Global installation evaluation — 2026-09-28 (after v0.1.3)

- Run six fresh native sessions against the actual global Codex/Claude skills.
  Both capture one synthetic failure without a task-level logging reminder;
  repeats/audits preserve bytes and create no duplicates. Both unnecessarily read
  history on unchanged maintenance. Retain Claude guard denials, its leftover
  payload and audit qualifications in the [report](evals/results/2026-09-28-global-journal/README.md).
- Add the bounded evaluator and one regression with six global-read/project-write
  boundary assertions to CI. Boundary and static checks pass separately from native
  findings. Skills, versions, released tag and global settings are unchanged.

## context-docs 0.1.3 — 2026-09-28 (tag `v0.1.3`)

Release validation found a generated-bytecode fixture-copy failure in the first
Linux CI run. Exclude Python cache files from native Claude fixture installations
and their manifests, with a regression checking that executable helper sources
remain included. This evaluation-harness repair does not change either skill or
rescore frozen model runs.

- Package the unchanged schema-v1 journal helper and a self-contained optional
  guide with the core skill. Keep logging off by default; ordinary Markdown
  maintenance has no runtime dependency. Enable capture only for project opt-in;
  no events for setup, no-change maintenance or audits. Preserve history on disable.
- Define recorder versus approving authority, unavailable/uncommitted revisions,
  capture failure reporting, and use of the installed helper. Keep the repository
  command as a compatibility entry point to one canonical implementation.
- The existing 25 helper tests and two portable-package/wrapper tests pass.
  Five new native execution-boundary controls, thirteen repository checker tests,
  skill metadata validators and repository static checks pass separately from
  actual model evaluation.
- The [native lifecycle study](evals/results/2026-09-28-journal-integration/README.md)
  ran eighteen sessions: Codex passed functional stages; Claude skipped setup.
  A separately frozen nine-session Claude follow-up passed functional preservation
  and capture under task-first native invocation. Retain semantic overstatements
  and guard denials; these are not clean unrestricted-client passes.
- Both original lifecycle readers lacked durable evidence for why a requested
  event was not captured. Add a concise Markdown capture-gap note on failure.
  Four [targeted native sessions](evals/results/2026-09-28-journal-gap/README.md)
  then preserved and recovered the actual reason, with audits unchanged. The final
  wording also covers unconfirmed writes after I/O errors; that wording-only
  clarification received static review, not another model run. Frozen hashes
  distinguish these unreleased 0.1.3 candidates; helper/schema remain unchanged.

## adopt-context-docs 0.1.5 — 2026-09-28 (bundled in `v0.1.3`)

- Merge optional journal settings only on explicit enable/disable requests.
  Preserve existing adoption date, context path, maintenance wording and routing;
  installing or updating a skill does not enable logging. Repeat setup is a no-op.
- Delegates journal behavior to the sibling core's packaged guide. Actual native
  old-package replacements preserve original project files. Codex's nine-stage
  lifecycle and Claude's separate nine-stage invocation follow-up preserve dates,
  paths, rule wording and legacy records; default-off/repeat/audit make no edits
  and disabling preserves history. Retain the original Claude setup failure,
  execution restrictions and factual limits. No global installation or publication.

## Optional event journal pilot — included in `v0.1.3` (2026-09-28)

- Add no-Git and infrequent-commit cases to the owner's logging requirements.
  Document explicit unavailable/uncommitted revisions; Git is not required by the
  helper. Run a [12-session native comparison](evals/results/2026-09-28-native-journal/README.md)
  across Claude/Codex and three recording formats. All requested facts survived;
  retain Claude overstatements, rejected/corrected capture attempts and metadata
  limitations separately from mechanical success. Twenty-two actual appends
  succeeded and all six fresh investigations preserved project-file bytes.
  Six new execution-boundary tests and repository static checks passed. No helper,
  skill or version change. Existing dates/paths/instructions were preserved in
  fixtures; actual package upgrade and natural capture-effort benefits remain
  untested. Keep JSONL optional rather than adding a default requirement.

- Record the owner's requirements for native Claude evaluation, compatibility
  with existing adopters and establishing necessity beyond Markdown/Git. Define
  a proposed comparison that includes a Markdown event log, and explicit upgrade
  acceptance criteria. Verified local Claude CLI version only; documentation and
  repository static checks do not establish authentication or logger behavior.
  No new model run, helper change, migration or skill version change in this step.
- Owner clarification: logging should efficiently preserve events for later need;
  current-context improvement and savings are not acceptance criteria. Update
  active guidance and qualify the earlier stop-logging recommendation as based
  on the narrower handoff trial. Preserve original results and journal entries.
  Documentation and repository static checks only; no runtime or skill version
  changes and no new investigation-benefit evaluation.
- Add a repository-only Python JSONL append/read command, schema version 1,
  with evidence and authority fields, verification scope/results, per-session
  writer exclusion, correction references and validation of existing history.
- Add a synthetic example and a three-session usability protocol. Markdown stays
  curated context; capture, retention and skill integration remain manual/optional.
- Eighteen synthetic journal tests and repository static checks passed. These
  include CLI round trips, interrupted history, competing writers, UTF-8 validation
  and a simulated `fsync` failure. No actual agent evaluation or real-session
  benefit trial was run.
  Installable skills and their versions are unchanged by this pilot.
- A [follow-up evaluation](evals/results/2026-09-28-event-journal/README.md)
  expanded coverage to 25 tests. Two initially failed on uncaught deep-JSON
  decoding; a targeted handler repair makes all 25 pass. Preserve the failures.
  Actual controls include a killed writer and 12 independent concurrent writers.
  Ten events passed a three-stage synthetic replay, with nine author-reviewed
  source-route questions and bounded local latency measurements. No fresh-agent
  sessions or real-work benefit trial were run; skill versions remain unchanged.
- Begin the owner-authorized [live trial](docs/event-journal-live-trial.md) in this
  repository with a bounded temporary instruction, source snapshots and actual
  journal events. Session 1 covers setup/verification; two later maintenance
  sessions remain pending. This is not a completed usefulness evaluation and does
  not change the installable skills or their versions.
- Live-trial session 2 reviewed the setup handoff in the same authoring chat:
  all three questions were answerable before the current-turn journal read;
  the journal added grouping but no missing fact. Correct stale project-context
  wording to distinguish the repository's temporary agent instruction from the
  unchanged installable skills. Static checks passed; independent retrieval and
  logging-effort benefits remain unmeasured, with session 3 pending.
- Close the live trial after three maintenance tasks in one authoring chat.
  Both handoff reviews found grouping but no missing fact recovered beyond the
  baseline evidence. Recommend ending routine logging and retain the optional
  tool and all evidence. Remove the temporary repository instruction as planned.
  Writer/test hashes still match the prior 25-test run; fresh static checks cover
  closure documentation. No fresh-agent, independent effort or accuracy result
  is claimed; installable skills remain unchanged.

## Repository checks and installation guidance — included in `v0.1.3` (2026-09-28)

- Enforce package boundaries for skill links and nested references, allowing the
  adoption package's declared dependency on its sibling core. Reject repository-only,
  absolute and escaping symlink targets. Exclude gitignored `.local/` study output
  from repository link checks.
- Compare `VERSION` files against the current README status and latest changelog
  entry for each skill, so historical mentions cannot hide a stale declaration.
- Correct Claude Code installation guidance for version requirements, local
  instruction files and configurable loading behavior; keep that detail canonical
  in the README.
- Twelve checker regression tests passed. These are static checks, not model
  evaluations. These repository-only changes do not alter installable skills;
  separate skill changes are recorded below.

## Native loading observer and file-tool guard — 2026-09-28

- Add evaluation-only InstructionsLoaded observation and a PreToolUse guard for
  six file/skill tools. Record loading hashes and correlate tool calls with guard
  decisions; exclude shell/delegation/network tools. No packaged skill changed.
- Seven new guard/observer controls join the eighteen existing native tests;
  twenty-five credential-free tests pass. CI also regenerates the new result summary.
- [Four actual native sessions](evals/results/2026-09-28-native-guarded/README.md)
  pass all loading/boundary gates, including a blocked outside write and fresh
  read-only loading of the newly installed rule. Three semantic reviews pass;
  the CSV response retains the known universal string-value error.
- Recommend experimental merge with factual limits. This clears the restricted
  integration gates only, not unrestricted-client reliability. The guard is not
  installed with the skills and is not an OS sandbox. Earlier scores are unchanged.

## Native paired evaluation — 2026-09-28

- Add a bounded ordinary-versus-skills comparison with matched requests, fresh
  cases, two attempts per condition and frozen inputs/criteria. Five new runner
  tests and the existing thirteen native smoke tests pass; these are static checks.
- [Eight actual native sessions](evals/results/2026-09-28-native-paired/README.md)
  use the unchanged core 0.1.2 / adoption 0.1.4. CSV overclaims appear in both
  conditions; stale-state reconciliation passes in both. No skill-specific cause
  of the earlier errors is established.
- Retain unverified loading confirmations, scratch-directory scope violations and
  optional command denials separately. The hold remains; conservative acceptance
  totals are not an accuracy ranking. No new skill revision or extra retry follows.

## context-docs 0.1.2 — included in `v0.1.3` (2026-09-28)

- Tighten the existing evidence check: verify the exact claim and retain the
  source's scope in both documents and final reports. Distinguish installed
  package versions from reference versions, and local configuration from runtime
  behavior or publication history. Omit unverified incidental details.
- Clarify that creating a minimal README link does not require inventing project
  intent when a project has no README or index.
- The second unreleased candidate also avoids unverified guarantees about every
  input and keeps final reports focused instead of restating unchanged context.
- A targeted refinement attributes agent-chosen methods/layouts to their actual
  decision maker and preserves document qualifications in final summaries.
- Final review reconciles statements with the resulting project, including facts
  made stale by the agent's own edits.
- Addresses the retained [native discovery failures](evals/results/2026-09-28-claude-code-followup/README.md).
  Four separately frozen native runs retain all candidates: the
  [first six-session run](evals/results/2026-09-28-native-v014/README.md) passes
  one semantic session, the [second](evals/results/2026-09-28-native-v014-followup/README.md)
  passes five, and two targeted discovery runs still fail. The
  [latest result](evals/results/2026-09-28-native-state-followup/README.md) retains
  an unsupported universal CSV claim and a stale final README statement.
  Hold the merge; this is author-reviewed development evidence, not a reliability
  claim. Exact commits distinguish candidates with the same unreleased versions.

## adopt-context-docs 0.1.4 — included in `v0.1.3` (2026-09-28)

- Require evidence for automatic instruction loading rather than inferring it
  from file presence or an explicit file read. Keep existing workflow adoption
  distinct from verified loading, including during audits.
- Align the Codex default prompt with the loaded instruction file instead of
  hardcoding AGENTS.md. This metadata change is statically validated.
- Addresses the unsupported loading claim in the
  [native audit](evals/results/2026-09-28-claude-code-followup/README.md).
  The [second native candidate](evals/results/2026-09-28-native-v014-followup/README.md)
  passes routing, repeat and audit semantic criteria, including qualified loading.
  Discovery remains factually unreliable in the
  [latest targeted run](evals/results/2026-09-28-native-state-followup/README.md).
  Permission denials remain separate execution failures; the branch stays on hold.

## adopt-context-docs 0.1.3 — included in `v0.1.3` (2026-09-28)

- Route the ongoing maintenance rule and adoption marker to the instruction file
  the client actually loads, instead of assuming `AGENTS.md`. Both `AGENTS.md` and
  `CLAUDE.md` are common, and a client may load only one of them; a rule written to
  an unloaded file silently does nothing. When a project keeps several, the rule
  belongs in the one in effect and stays reachable from the others by reference or
  import rather than being duplicated.
- State the maintenance rule without a client-specific invocation prefix, so the
  wording written into a project is valid wherever the skill is installed.
- Add [instruction-file routing cases](evals/adoption/instructions.py) with ten
  static grader controls. Before model evaluation, remove their inherited AGENTS.md
  destination and restate the client condition in the fresh repeat session.
- [September 28 merge review](evals/results/2026-09-28-adoption-v013/README.md):
  nine model sessions, eight accepted; all three repeats and the audit preserved
  bytes. The split-file case passed routing rubrics but failed frozen immutable-file
  and external-link checks. Fixture limitations are retained with that failure;
  the review recommends holding merge for a targeted follow-up. No native Claude
  Code evaluation was run, and the skill contents were not tuned after this result.
- [Separately frozen routing follow-up](evals/results/2026-09-28-adoption-v013-followup/README.md):
  four sessions passed after exposing immutable-file constraints in requests and
  checking declared installed references by hash in links, code spans and prose.
  Both next-day repeats preserved bytes and dates. Nine new verifier regression
  tests and existing static checks passed. The reviewer now considers the branch
  ready to merge within its experimental scope. The original failure is retained;
  neither skill changed, and native Claude Code behavior remains untested.

## adopt-context-docs 0.1.2 — 2026-09-27 (`eed23ed`)

- Prefer a `Context maintenance` heading, then the marker, then instructions when
  creating a new maintenance section; preserve existing equivalent layouts.
- Metadata, package links and existing static controls were checked. No new model
  evaluation was run for this version.

## adopt-context-docs 0.1.1 — 2026-09-27 (`9a5211a`)

- When equivalent context and maintenance guidance already exist, add only the
  missing marker and preserve the guidance's wording.
- [Marker regression](evals/results/2026-09-27-adoption-marker/README.md): ten
  sessions across initial and revised conditions. The initial run's guidance
  rewrite failure and date-test ambiguity are retained, not erased. The final
  revision was tested on the two affected unmarked cases only.

## adopt-context-docs 0.1.0 — 2026-09-27 (`d0febcf`)

- First adoption wrapper: applies the core method and merges a maintenance rule
  into the project's instructions. Requires `context-docs` as a sibling package.
- [Adoption and repeat regression](evals/results/2026-09-27-adoption/README.md):
  two cases, four sessions. Both repeat passes left project files unchanged.

## context-docs 0.1.1 — 2026-09-27 (`6c96d2a`, tag `v0.1.1`)

- Shorter entry point, 645 to 417 words, with the frozen preservation and concision
  rule met.
- [Concision comparison](docs/evaluation-2026-09-27-concise.md): 12 trials, both
  the original and the candidate passed 6/6. This was a prompt refinement test; it
  established no better knowledge retention or reader accuracy. The candidate was
  slower and emitted more output tokens.
- Later studies exercised this version without changing it: the
  [quality and fresh-reader study](docs/evaluation-2026-09-27-quality.md), the
  [public-source handoff pilot](docs/evaluation-2026-09-27-public.md), the
  [routing follow-up](docs/evaluation-2026-09-27-routing.md) and the
  [decision-history study](docs/evaluation-2026-09-27-history.md). None of them
  found an accuracy advantage over competent ordinary maintenance.

## context-docs 0.1.0 — 2026-09-26 (`7517367`, tag `v0.1.0`)

- First published skill, [standard](skills/context-docs/references/standard.md)
  0.1.0, templates and evaluation scenarios. Instructions only: no runtime
  dependency, background service or scheduler.
- [Local-project pilot](docs/evaluation-2026-09-26.md): eight runs. All 30
  controlled checks met, and a specific workflow contradiction was missed that the
  ordinary cleanup baseline resolved. That miss stands as part of the record.
- [48-trial public suite](docs/evaluation-2026-09-27.md): both arms passed 24/24
  under mechanical checks and author-reviewed criteria. No correctness advantage
  was observed. The skill used more time and tokens.
