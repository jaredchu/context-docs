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

The latest bundle is described in the [v0.2.5 release notes](docs/releases/v0.2.5.md).
Previous [v0.2.4 release notes](docs/releases/v0.2.4.md) are retained.
Previous [v0.2.3 release notes](docs/releases/v0.2.3.md) are retained.
Previous [v0.2.2 release notes](docs/releases/v0.2.2.md) are retained.
Previous [v0.2.1 release notes](docs/releases/v0.2.1.md) are retained.
Previous [v0.2.0 release notes](docs/releases/v0.2.0.md) are retained.
Previous [v0.1.9 release notes](docs/releases/v0.1.9.md) are retained.
Earlier [v0.1.6 release notes](docs/releases/v0.1.6.md) are retained.
Earlier contents and validation are summarized in the [v0.1.5 release notes](docs/releases/v0.1.5.md),
with earlier [v0.1.4](docs/releases/v0.1.4.md) and [v0.1.3](docs/releases/v0.1.3.md) notes retained.

## Installed v0.2.5 concurrency smoke — 2026-10-18

- Run one fresh native session per client using installed core 0.2.5/adoption
  0.1.14 directly. Both respect writer ownership and explicit handoff, reread
  after the forced stale edit, and preserve newer content, decisions, blockers
  and all seven final context links per client. Only Progress and Next action
  in the handed-over file change. The [record](evals/installed-skills/2026-10-18-concurrency-v025/README.md)
  retains the reused fixture, protocol, exact outputs, trace ordering and limits.
- Each session has only the forced mismatch; no additional mismatch path is
  exercised. This does not clear Claude's earlier second-mismatch reread failure
  or erase Codex's earlier corrected read-only checker error. These guided,
  author-scored cases with explicit installed paths establish no simultaneous
  writer safety, implicit loading or general conflict-prevention guarantee.
  Installed skills, existing setups, saved studies, prior evidence and the
  uncommitted upgrade event remain unchanged. No output repair or model rerun.

## v0.2.5 publication — 2026-10-18

- Publish the [experimental prerelease](https://github.com/jaredchu/context-docs/releases/tag/v0.2.5)
  from `89c91f4` after all three release-commit Actions runs pass. Deploy from
  the same revision; all eight checked live resources return HTTP 200 and match
  the build, including released labels, both smoke qualifications and SEO titles
  without em dashes. The [publication record](docs/releases/v0.2.5-publication.json)
  owns identities, hashes, preservation and limits; the original preparation
  record and all earlier native/review evidence remain unchanged.
- Publication and verification are Codex-assisted. Earlier Claude contributions
  remain credited in the guidance and smoke commits. No new native model trial,
  counterpart review or installed upgrade is performed. Existing setups,
  installed packages and saved studies are preserved.

## v0.2.5 release preparation — 2026-10-17 (prepublication checks)

- Prepare [draft release notes](docs/releases/v0.2.5.md) for core 0.2.5/adoption
  0.1.14 and update both website pages, the guide and current context. Keep draft
  labels distinct from published v0.2.4. Describe writer assignment, explicit
  handoff, narrow edits and reread/reconcile without locking or merge guarantees.
- Retain the native smoke qualifications: Claude retries its own second mismatch
  without rereading despite preserved final content; Codex corrects a read-only
  anchor-check error. Guided cases do not test simultaneous writers or establish
  general conflict prevention. Original smoke/review evidence remains unchanged.
- Local static/package checks, 18 checker tests and 15 site tests pass. The
  [preparation record](docs/releases/v0.2.5-validation.json) separates these checks,
  the nine-file public build, desktop/mobile previews and preservation from the
  earlier native evidence. No new model trial, counterpart review, publication,
  deployment or installed upgrade is performed. Skill source files, installed
  packages, setup rules and saved studies are preserved.

## context-docs 0.2.5 — 2026-10-18 (bundled in v0.2.5)

- When agents or sessions work concurrently on the same context file, coordinate
  one writer per file before concurrent edits begin, hand off ownership explicitly,
  and pass other participants' findings to that writer.
  Prefer narrow edits; after conflicts or stale-text failures, reread and reconcile
  current contributions before retrying. Preserve newer work instead of replacing
  it from a stale snapshot. This adds guidance, with no locking infrastructure.
- The earlier [offline diagnostic](evals/concurrency/offline-2026-10-17/README.md)
  forced two processes to read the same snapshot:
  either whole-file write order lost an update. Available-tool patches
  preserved disjoint edits and rejected a stale overlapping patch. These are
  mechanism checks, not native trials or an incident-rate estimate. At the
  guidance commit, the new rule had not been behavior-tested in native sessions.
  Original evidence is unchanged; the separate candidate smoke below adds native
  observations with its own qualifications.
- Validation: repository static checks, 18 evaluation-check unit tests, 15 site
  unit tests, standalone checks of both packaged skills and whitespace checks pass.
  Sol integrated and checked the change; Opus 5.5 reviewed the diff, requested
  explicit writer assignment/handoff in the skills, and approved the correction
  in one focused follow-up. This was artifact review, not a native behavior trial.
  Installed skills, existing setup rules, prior evidence and saved studies remain
  unchanged.
- A [focused native candidate smoke](evals/concurrency/smoke-0.2.5-2026-10-17/README.md)
  runs once per client with copied core 0.2.5/adoption 0.1.14. Both respect assigned
  writers and explicit handoff, reread after the deliberately stale queued edit,
  and preserve newer content and source links. Claude's own second edit mismatch
  is retried without another reread: a procedural failure despite preserved final
  Markdown. Codex's first read-only self-check has an anchor-case error; its
  corrected check passes. All original traces and outputs are retained without
  repair or rerun. These guided, author-scored cases do not test simultaneous
  writers, installed behavior or general conflict prevention.

## adopt-context-docs 0.1.14 — 2026-10-18 (bundled in v0.2.5)

- Follow sibling core's conditional shared-file coordination during adoption and
  re-adoption: one writer, narrow edits and reread/reconcile after conflicts.
  Existing setup-preservation rules remain in place. Validation and limitations
  are shared with core 0.2.5 above.

## Installed v0.2.4 clarity smoke — 2026-10-17

- Run one fresh native session per client with installed core 0.2.4/adoption
  0.1.13, each covering two synthetic clarity tasks. Both preserve conditions,
  uncertainty, rationale, evidence and the permitted edit scope; 10 Codex and
  eight Claude context links resolve. The [installed smoke record](evals/installed-skills/2026-10-17-clarity-v024/README.md)
  retains exact outputs, operation checks and limits separately from the unchanged
  copied-candidate pronoun qualification. Installed skills, setups and saved studies
  remain unchanged. Guided, author-scored and explicitly routed; no comprehension
  gain, automatic everyday application or independent loading proof is established.

## v0.2.4 publication — 2026-10-17

- Finalize owner-authorized experimental release labels for core 0.2.4, adoption
  0.1.13 and unchanged standard 0.1.1. Retain the report-only Claude pronoun
  qualification, unchanged original evidence and limits on comprehension benefit
  and automatic everyday application. The [publication record](docs/releases/v0.2.4-publication.json)
  confirms passing release-commit checks and deployment from `73b15ac`. All eight
  checked live public resources match the build, including released labels, clarity
  guidance and the qualification. Installed upgrades remain separate; source packages,
  installed skills, setups, earlier evidence and saved studies are preserved.

## v0.2.4 release preparation — 2026-10-17 (unpublished)

- Prepare draft notes and both website pages for the small clarity preference,
  preserving conditions, uncertainty, rationale, evidence and existing layouts
  without requiring ASD-STE100 compliance. Distinguish unreleased source versions
  from the published v0.2.3 bundle; keep SEO titles without em dashes.
- Retain the smoke qualification: both clients pass the saved-Markdown checks,
  while Claude's final chat report adds an unsupported pronoun absent from the
  saved context. The guided checks do not establish comprehension gains or
  automatic everyday application. Earlier evidence is unchanged.
- The [preparation record](docs/releases/v0.2.4-validation.json) owns new local
  checks, package identities, previews and preservation separately from earlier
  native results and review. No new model trial, counterpart review, installed
  upgrade, release or deployment is part of preparation.

## context-docs 0.2.4 — 2026-10-17 (bundled in v0.2.4)

- Prefer clear, direct sentences and consistent project terminology within
  authorized context edits. Preserve conditions, uncertainty, rationale and
  evidence. The preference requires no ASD-STE100 compliance and grants no scope
  to change existing layouts or unrelated owner text.
- Earlier tiny text comparison: two fictional notes and 12 shared questions,
  with a fresh Claude Opus 5.5 reader per condition. Original and clarity-rewritten
  notes both score 12/12; no information loss or comprehension gain is observed.
  Codex authored and scored the examples. This is not a native evaluation of the
  updated skills or a measure of human reading effort; original evidence is unchanged.
- Package/metadata/link/version checks, 18 static-check regression tests and 15 site
  tests pass. Opus artifact review and one focused follow-up close owner-text
  wording and preservation-evidence findings. Byte/mode comparisons verify installed
  skills, setup rules and saved studies unchanged. This is not a release or upgrade.
- A [small copied-candidate smoke](evals/clarity/smoke-0.2.4-2026-10-17/README.md)
  now runs one native session per client, each covering re-adoption and maintenance
  of synthetic prose. Both preserve conditions, uncertainty, rationale and all eight
  source links, changing only permitted sections of two context files. Claude's final chat
  report adds an unsupported gendered pronoun for Noor; saved Markdown is unaffected.
  No correction or retry. These guided, author-scored writing cases do not establish
  comprehension gain, automatic everyday application or general reliability.

## adopt-context-docs 0.1.13 — 2026-10-17 (bundled in v0.2.4)

- Follow sibling core's clarity preference within adoption's existing edit scope,
  preserving conditions, uncertainty, rationale and evidence without requiring
  ASD-STE100 compliance. Existing setup and layout preservation rules remain in place.
- Validation shares core 0.2.4's checks and limitations above.

## v0.2.3 publication — 2026-10-17

- Finalize owner-authorized experimental release labels for core 0.2.3, adoption
  0.1.12 and unchanged standard 0.1.1. Retain the Codex temporary-file scope failure,
  unknown prior path state and original native/review qualifications.
- The [publication record](docs/releases/v0.2.3-publication.json) records the
  experimental prerelease, passing release-commit checks and successful Pages
  deployment from pinned source `0c053d6`. All eight checked live responses match
  the build, including released labels, concise guidance and the smoke qualification.
  Package files, installed skills, setup rules and saved studies are preserved;
  no new model trial, counterpart review or installed upgrade.

## v0.2.3 release preparation — 2026-10-17 (unpublished)

- Prepare draft notes and both website pages for concise progress views with
  linked evidence, preserving decisions, blockers and existing layouts. Keep
  unreleased candidate labels separate from the published v0.2.2 bundle.
- Retain the focused smoke's Codex temporary-file write/delete scope failure and
  unknown prior temporary-path state. Earlier smoke outputs and review records
  remain unchanged; no new model trial, review, installed upgrade or deployment.
- The [preparation record](docs/releases/v0.2.3-validation.json) owns local checks,
  package identities, previews and preservation separately from earlier native evidence.
  All 33 local regression tests, both metadata validators, isolated package links
  and the nine-file build pass. Both pages pass desktop/mobile preview checks;
  this is not live-site verification or a new native model evaluation.

## context-docs 0.2.3 — 2026-10-17 (bundled in v0.2.3)

- Favor concise progress overviews with links to canonical evidence. Keep the goal,
  meaningful outcomes, dependencies, blockers and next action visible, retaining
  decisions, approval boundaries and qualifications without a fixed line limit.
  Preserve existing formats and unique information; do not create a new evidence
  store merely to shorten a view.
- Validation: repository/package/link checks, 18 static-check regression tests,
  15 site tests and both metadata validators pass. Initial Opus artifact review
  finds a missing authorization condition in the context summary; corrected with
  one focused follow-up finding no unresolved material issue. The
  [check/review record](evals/progress/concise-view-review-2026-10-17.md) distinguishes
  artifact review and its original pre-smoke scope. Installed skills, setup rules
  and saved studies remain unchanged.
- A [focused copied-candidate smoke](evals/progress/smoke-0.2.3-2026-10-17/README.md)
  runs re-adoption and linked-table maintenance in one session per native client.
  Both produce concise, source-linked views and preserve decisions, blockers and
  existing layouts. Codex creates/removes an extra fixed temporary hash file,
  failing the strict write boundary; the qualified result is retained without
  correction or retry. The full suite and general benefit remain unestablished.

## adopt-context-docs 0.1.12 — 2026-10-17 (bundled in v0.2.3)

- Follow sibling core's concise-overview guidance during adoption. Link detailed
  evidence rather than expanding a view into test/review history, preserving
  established views, owner edits, decisions and setup records.
- Validation shares the core 0.2.3 checks above; no installed upgrade or release.

## v0.2.2 publication — 2026-10-17

- Finalize the owner-authorized experimental release labels and website links
  for core 0.2.2, adoption 0.1.11 and unchanged standard 0.1.1. Preserve all package
  files, preparation evidence, earlier native results, installed skills and setups.
- The [publication record](docs/releases/v0.2.2-publication.json) owns release-commit
  checks, prerelease identity, deployment and live verification. Publish from
  `7aa2d5d` after both main-branch checks pass and deploy the same revision.
  All eight checked live resources return HTTP 200 and match its build, including
  default-adoption copy, source maps, released labels and SEO titles without em dashes.
  No new model trial, review or installed upgrade is part of publication.

## v0.2.2 release preparation — 2026-10-17 (unpublished)

- Prepare [draft bundle notes](docs/releases/v0.2.2.md) for core 0.2.2, adoption
  0.1.11 and unchanged standard 0.1.1. Retain all three earlier native Codex
  sessions, the Opus reviews and their exact candidate/final-wording qualifications.
- Explain default inline creation during supported adoption and everyday
  maintenance on both website pages. Keep explicit visualization prompts optional,
  existing views canonical, sparse context free of scaffolding and upgrades
  separate from project changes. Retain draft/unreleased labels, the published
  v0.2.1 link, the canonical visual example and SEO titles without em dashes.
- The [preparation record](docs/releases/v0.2.2-validation.json) owns current local
  checks and previews separately from unchanged earlier behavior evidence. Skill
  packages, installed skills, setups and saved studies are preserved; this work
  performs no new native trial, model review, publication, deployment or upgrade.
  Local checks pass: 18 packaging/static and 15 site tests, both metadata
  validators, isolated package links and the nine-file public build. Both pages
  pass desktop/mobile previews with inspected progress screenshots and no page
  overflow, script errors or remote requests.

## context-docs 0.2.2 — 2026-10-16 (bundled in v0.2.2)

- Add the core guide for adoption's default inline progress path when a documented
  goal and supported work make one useful. Adapt existing status lines in place,
  preserve existing views and layouts, and keep detailed facts authoritative in
  one place. Sparse context, explicit preferences and read-only audits retain
  their boundaries. Everyday maintenance refreshes the view without another request.
- Validation and counterpart review are recorded in the
  [default-adoption check record](evals/progress/adoption-default-2026-10-16/README.md).
  Two guided native Codex phases on an already-adopted fixture pass with the initial candidate: explicit
  re-adoption adds the missing inline checklist without a progress request;
  ordinary work refreshes it from a new result under the existing rule.
  A third session checks the clarified candidate's unchanged re-adoption and
  makes no edits. Opus artifact review and one focused follow-up resolve the
  material findings; a minor marker-scope clarification follows without another review.
  Only scoped fixture Markdown changes. Packaging/site checks pass (18 + 15),
  as do metadata validators, isolated package links and a private website build.
  Earlier smoke results retain their original request-based scope. Installed
  skills, setup rules and saved studies are not upgraded or rewritten. Fresh
  adoption with a new instruction rule/marker is not tested.

## adopt-context-docs 0.1.11 — 2026-10-16 (bundled in v0.2.2)

- Start the supported inline view by default during adoption through sibling core
  0.2.2; reuse existing views and equivalent maintenance rules. New maintenance
  wording includes keeping the view current without duplicate tracking. Preserve
  original markers/dates, storage, owner edits and logging settings.
- The [check record](evals/progress/adoption-default-2026-10-16/README.md) distinguishes
  mechanical checks, guided native behavior and artifact review. This development
  change does not install skills or publish a release. Explicit re-adoption may
  update project context; existing setup rules and markers are preserved.

## Installed v0.2.1 visual progress smoke — 2026-10-16

- Run one fresh synthetic create case per native client using the installed
  core 0.2.1: Codex requests Sol 6.1, Claude Code requests/reports Opus 5.5.
  Both show the visual path, dependencies, blocker and sourced next action;
  all 17 Codex and 15 Claude view/context links resolve. Claude adds one
  unsupported prerequisite in Unknowns prose; retain that qualification and
  both exact outputs in the [smoke record](evals/installed-skills/2026-10-16-progress-v021/README.md).
- Each completes within 180 seconds without retry; only the two permitted fixture
  Markdown files change. These author-scored cases do not establish general
  usability or flawless source grounding. Installed skills, setups, earlier
  evidence and saved studies are preserved; no package or version change.

## v0.2.1 publication — 2026-10-16

- Finalize the approved experimental release labels and website links for core
  0.2.1, unchanged adoption 0.1.10 and standard 0.1.1. Keep preparation evidence,
  earlier native outcomes, installed packages, setups and saved studies unchanged.
- Publish the experimental prerelease and deploy from `0c897c0` after both
  release-commit Actions pass. All eight checked live resources return HTTP 200
  and match the build, including the visual example/source maps and released
  labels. The [publication record](docs/releases/v0.2.1-publication.json) preserves
  hashes, Actions and limits separately from unchanged preparation evidence.
  No new model trial or installed upgrade is part of this work.

## v0.2.1 release preparation — 2026-10-16 (unpublished)

- Prepare [draft notes](docs/releases/v0.2.1.md) for core 0.2.1, unchanged adoption
  0.1.10 and standard 0.1.1, retaining the bounded artifact review and two guided
  native smoke outcomes with their original limits.
- Show the canonical synthetic text tree on both website pages, with clickable
  source maps outside the diagram and horizontal scrolling to preserve branch
  alignment on narrow screens. Retain experimental/unreleased labels, the latest
  published v0.2.0 link and SEO titles without em dashes.
  Include the canonical progress example in the website CI input filters.
- The [preparation record](docs/releases/v0.2.1-validation.json) separates current
  mechanical checks and local previews from earlier native evidence. Skill packages,
  installed skills, setups and saved studies are unchanged. No new native trial,
  release or deployment is performed.

## context-docs 0.2.1 — 2026-10-16 (bundled in v0.2.1)

- Require an explicit progress visualization to show a compact visual path with
  completion branches, dependencies, blockers and the next action. Keep proposals
  separate, unknown relationships unknown and links clickable outside text diagrams.
  A flat status table alone no longer meets visual acceptance.
- Replace the authored example's status table with a source-keyed text tree and
  revise the manual acceptance criteria, README prompt and user/website guide.
  Adoption inherits the sibling core guide; its 0.1.10 package is unchanged.
  Earlier smoke outputs and scores retain their original scope: they did not
  validate this stricter visual criterion. No installed upgrade, setup migration
  or new native behavior trial is performed by this correction.
- Final validation passes 18 packaging/static tests, 14 site tests, both metadata
  validators, 20 isolated package links, repository static checks and the nine-file
  website build. Opus 5.5's initial review and one focused follow-up resolve the
  fixture/format findings; a final minor fixture clarification is recorded without
  another review. See the [checks and dispositions](evals/progress/visual-path-review-2026-10-16.md).
- Subsequently run one small synthetic copied-candidate create case in each of
  native Codex and Claude Code. Both show parallel completion branches, the
  missing-sample dependency, blocker and next action, with clickable source maps;
  all 18 Codex and 14 Claude view/context links resolve. Only the two permitted
  fixture Markdown files change. The [smoke record](evals/progress/smoke-0.2.1-2026-10-16/README.md)
  retains exact outputs, model qualifications and author-scored limits. No retry,
  installed upgrade or full-suite run; existing setups and saved studies are preserved.

## Installed v0.2.0 progress smoke — 2026-10-16

- Run one fresh native Codex session and one Claude Code session using installed
  core 0.2.0 to create a linked Markdown view from the same synthetic fixture.
  Both observe installed guidance, preserve incomplete goals, blockers and
  approval boundaries, distinguish learning from outcomes and qualify possible
  stalls. All 17 view/context links per client resolve; only the two permitted
  Markdown files change. Retain the [outputs and limits](evals/installed-skills/2026-10-16-progress/README.md).
- Each session completes within its 180-second cap, with no retry, product change
  or new test infrastructure. These guided author-scored cases add no general reliability,
  user-benefit or implicit-loading claim. Existing setups, installed packages and
  saved studies are preserved; earlier smoke gaps and records remain unchanged.

## v0.2.0 publication — 2026-10-16

- Publish core 0.2.0/adoption 0.1.10 as an experimental prerelease with unchanged
  standard 0.1.1. Finalize release labels and website links without changing skill
  packages or upgrading installations. Retain the initial review, guided smoke
  and known source-link gap; no new native trial is performed.
- Preserve the earlier main-branch v1.0 planning documents and fixtures as deferred
  history, without making them release gates. The
  [publication record](docs/releases/v0.2.0-publication.json) records passing
  release-commit Actions and deployment from `d341695`. Eight live responses match
  the build; both pages show progress guidance and released status. Existing
  setups, installed skills and saved studies are unchanged. Preparation and
  historical evidence remain intact.

## v0.2.0 release preparation — 2026-10-16 (prepublication checks)

- Prepare [draft release notes](docs/releases/v0.2.0.md) for core 0.2.0,
  adoption 0.1.10 and unchanged standard 0.1.1. Add Markdown progress guidance
  and the canonical prompt to both website pages, retaining unreleased labels,
  the latest published v0.1.9 link and SEO titles without em dashes.
- Pass 14 site tests, 18 packaging/static regression tests, repository static
  checks, the nine-file public build and desktop/mobile previews. The
  [preparation record](docs/releases/v0.2.0-validation.json) separates these
  checks from earlier native smoke evidence and its source-link gap. No new
  model trial, release, deployment or installed upgrade is performed; skill
  packages, existing setups and saved studies are preserved.

## context-docs 0.2.0 — 2026-10-16 (bundled in `v0.2.0`)

- Add Markdown progress visualization to initialization and maintenance: a view
  in existing context or a linked Markdown file, grounded in source links and
  documented goals, outcomes, blockers and next actions. Distinguish useful
  learning from completed outcomes; history can support a possible stall, not
  prove a loop. Preserve local-only boundaries and read-only audits; no web app,
  duplicate tracker, invented percentages or claim of live agent activity.
- Package the progress guide with core; add a synthetic example and seven manual
  regression scenarios. Validation covers 18 packaging/static regression tests,
  12 site tests, both skill validators and static repository checks. A focused
  Opus 5.5 artifact review is retained with Sol's source-checked dispositions;
  the revised text has no second model review. See the
  [validation and review record](evals/progress/review.md).
  Installed skills, existing project setups and saved studies are unchanged.
- A [focused synthetic smoke check](evals/progress/smoke-2026-10-16/README.md)
  runs two fresh Claude Code sessions with an explicit copied development skill:
  create a linked Markdown view, then refresh it from a new retained result.
  Core status/approval/history behavior and write boundaries pass; 37 link
  occurrences resolve. Two advances bullets lack direct inline source links,
  although their sources are linked elsewhere. The remaining scenarios, native
  Codex behavior, default loading and user benefit are untested.

## adopt-context-docs 0.1.10 — 2026-10-16 (bundled in `v0.2.0`)

- Route progress requests to the sibling core's Markdown guide while preserving
  existing layouts, storage, markers and equivalent setup rules. Packaging,
  version/link checks and skill validation pass; authored adoption behavior cases
  are not executed. This development update does not upgrade installed skills.

## v0.1.9 publication — 2026-10-11

- Publish the [experimental prerelease](https://github.com/jaredchu/context-docs/releases/tag/v0.1.9)
  from `14acc74` after its static and landing-page Actions passed, retaining both
  Codex and Claude credits. Bundle core 0.1.9, adoption 0.1.9 and standard 0.1.1.
- Deploy the website from that commit. All eight checked live public responses
  match the nine-file build; both pages show released status and SEO titles omit
  em dashes. Retain [publication evidence](docs/website-deployment-2026-10-11.json)
  separately from preparation/native checks. Local static checks, 12 site tests
  and build pass; no new agent study or installed-skill update is performed.
- Verify original package, installed skill, setup, saved study and existing journal
  bytes against the pre-publication baseline. Preserve preparation hashes and
  historical release/review records; append publication facts to current records.

## context-docs 0.1.9 — 2026-10-11 (bundled in `v0.1.9`)

- Prepared [v0.1.9 release notes](docs/releases/v0.1.9.md) on October 11 and update
  the website's setup guidance and draft-release links. Preparation kept both
  pages marked unreleased, SEO titles without em dashes and the nine-file public
  build boundary. Publication switches those labels to released.
  The [preparation record](docs/releases/v0.1.9-validation.json) separates earlier
  fix-commit CI/native evidence from current local preparation checks. No new
  agent study, publication, installation or setup change was performed by preparation.
- Clarify initialization from earlier notes: check relevant project sources before
  importing current implementation/configuration claims, while retaining decisions
  and unresolved work. Adoption inherits the core rule; its package is unchanged.
- Add a focused stale-source adoption fixture and regression controls. The released
  core reproduced the stale 10-second claim in one of two source-selection trials;
  the other correctly read the 20-second configuration. An earlier attempt was
  blocked by the sandbox's ignore-file write restriction and produced no context.
  Validation details are recorded in the [focused case](evals/source-selection/README.md).
- Both matched candidate source-selection trials use the 20-second configuration,
  distinguish the earlier claim and preserve rationale, blocker, next step and
  local sharing boundaries. This small mixed-baseline check establishes no general
  reliability or causal accuracy advantage. Local checks: seven focused controls,
  23 local-only controls, 17 static-checker tests, 12 site tests, repository static
  checks and site build. Existing installations, adoption setup and saved study
  artifacts were preserved; the focused fix did not update installed skills.
- Claude Opus 5.5 reviewed the focused change and evidence; Sol integrated and
  validated it. Both package metadata validators pass using a disposable PyYAML
  environment; the initial system/bundled Python attempts lacked that dependency.

## Documentation and validation follow-up — 2026-10-10

- Clarify that adopted projects use their loaded maintenance rule during normal
  work; naming the skill in every prompt is optional. Align README, guide,
  illustrative example and website source. Describe Codex's initial contribution
  and the current Sol/Opus collaboration roles; record owner-reported search setup.
- Extend commit attribution to every commit Claude helps implement, validate or
  review, including review-only assistance. Preserve the Codex trailer rule,
  human author identity, existing co-author trailers and published history.
- Execute seven local-only cases per client plus fresh audits on released core
  0.1.8/adoption 0.1.9. Record passing storage/preservation gates alongside the
  stale-source finding, journal write denial, preparation timeout and recovered
  parser failure in the [follow-up](evals/local-only/validation-2026-10-10/README.md).
  No subject cases were retried. Ship the runner with a mixed-event parser fix
  and early process receipts; it differs from the frozen execution source.
- Local checks: 23 local-only/stream controls, 17 static-checker tests and 12 site
  tests; repository static checks and public site build. These mechanics are
  separate from the native evaluations. Skill packages and versions are unchanged;
  the previous 1,881 saved study files are preserved.
- Publish the prepared follow-up as `a8e1e36` with Codex and Claude co-author
  trailers. Both push workflows and manual Pages deployment pass; both live HTML
  pages and five public resources match the build. Retain the
  [deployment verification](docs/website-deployment-2026-10-10.json), including
  optional-prompt guidance and SEO titles without em dashes. No new skill release.

## v0.1.8 publication — 2026-10-10

- Publish the [experimental prerelease](https://github.com/jaredchu/context-docs/releases/tag/v0.1.8)
  from `8bda86ce8e23d14874dcb22e0af7b2e581717ee7`, after release-commit
  [static checks](https://github.com/jaredchu/context-docs/actions/runs/38062411488) and
  [landing-page checks](https://github.com/jaredchu/context-docs/actions/runs/38062411476) passed.
  Bundle core 0.1.8/adoption 0.1.9 and unchanged standard 0.1.1. The release-note
  Opus 5.5 review findings were resolved before publication; package behavior,
  existing setups and saved studies are unchanged by release preparation.

## v0.1.8 release preparation — 2026-10-10 (prepublication checks)

- Prepare [release notes](docs/releases/v0.1.8.md) for core 0.1.8/adoption 0.1.9
  and unchanged standard 0.1.1. Record all 15 packaged file hashes; all seven
  published final-native identities match the candidate. The candidate's static
  and landing-page GitHub Actions runs passed.
- Release preparation passes 12 site tests, repository static checks and the
  site build. Site status tests now cover released/unreleased states independently
  of the README's current state. Saved study artifacts and existing setups remain
  unchanged. These checks add no native agent evaluation; release-note review
  and publication status are recorded in the linked notes and records.

## context-docs 0.1.8 — 2026-10-10 (bundled in `v0.1.8`)

- Extend the opted-in `auto` preference to explicitly selected local-only context
  inside Git. Preserve all existing logging settings before detection; require
  both context and journal paths to be untracked and effectively ignored. Missing
  scope, tracked/exposed paths, negation, symlinks, nested repositories and probe
  errors leave settings unchanged. Shared-Git and no-Git defaults are preserved.
- Update both skills' routing and the packaged/user guides. The website now
  extracts local-only setup and auto prompts from the public guide; remove em
  dashes from page/Open Graph SEO titles. No existing setup, ignore rule or saved
  study is migrated.
- Mechanical validation: 156 relevant tests pass, including 31 policy tests,
  21 local-only controls, 17 static-checker, 19 audience, 28 public-adoption,
  1 original auto-guard and 12 site tests; the remaining 27 tests exercise the
  event journal. Static checks, both skill validators, isolated package links/helper
  execution and the site build pass. All 1,881 saved study files are unchanged.
- Exact Opus 5.5 drafted the helper and policy tests within a 240-second bound;
  Codex integrated them, corrected a Git `check-ignore` invocation defect found
  in the initial failing run, and strengthened access/error/config handling.
- Six bounded native Claude Code/Codex sessions pass their execution/preservation
  gates: four before review fixes (setup and repeat/audit per client), then two
  fresh final-package setup sessions including case aliases and prospective
  journal exceptions. One Opus review and one focused follow-up resolved the
  tracking and site-status findings. The [validation record](evals/event-journal/auto-preference/local-only.md)
  retains failures, candidate identities and limits; no broad behavioral or
  JSONL-necessity claim is made.

## adopt-context-docs 0.1.9 — 2026-10-10 (bundled in `v0.1.8`)

- Resolve the extended opt-in auto policy during authorized adoption, preserving
  explicit settings, agreed instruction locations, original adoption dates,
  existing directories and event history. Selecting local-only storage alone,
  skill installation, upgrades and audits do not enable logging. Validation is
  shared with core 0.1.8 above.

## context-docs 0.1.7 — 2026-10-10 (bundled in `v0.1.8`)

- Add opt-in local-only context guidance: check effective ignore rules separately
  from Git tracking, read ignored entry points directly, and keep local content
  out of shared destinations. Preserve existing layouts, tracked history and
  logging settings; resolve migration scope before changing established context.
- Clarify the journal's optional role in retaining selected events as Git-ignored
  context changes. It does not capture complete document versions or enable
  logging implicitly; existing logging settings and auto rules are preserved.
- Add repository-only storage/leakage regression controls and synthetic scenarios.
  All 21 new real-Git/canary controls pass, along with 17 static-checker, 19 audience,
  28 public-adoption and 8 site tests (93 total), repository static checks, the site
  build, both skill validators and isolated sibling-package link checks. Seven
  agent scenarios are authored but unexecuted; no new native agent evaluation or
  confidentiality guarantee is claimed. Saved studies remain unchanged; standard
  remains 0.1.1.
- Codex implemented skill/docs guidance and integrated controls drafted by exact
  Claude Opus 5.5. The bounded implementation reached its 180-second limit after
  writing three files; Codex corrected Git invocation issues and validated them.
  A separate Opus review found no hard blocker; its routing, marker and ignore-rule
  clarifications were applied. One focused follow-up accepted the fixes; version
  files and the guide's unreleased wording were verified independently.

## adopt-context-docs 0.1.8 — 2026-10-10 (bundled in `v0.1.8`)

- Apply the core local-only procedure during explicit adoption and record the
  storage choice in the agreed instruction location. Keep upgrades and repeat
  adoption from selecting or migrating storage implicitly; separate verified Git
  exclusion from instruction-loading evidence. Update the user guide with setup
  and fresh-session prompts. The same 93 mechanical tests, static checks, skill
  validators and sibling-package checks pass; native local-only adoption remains
  untested. The focused Opus review and its clarifications are recorded above.

## v0.1.6 publication — 2026-10-10

- Publish the [experimental prerelease](https://github.com/jaredchu/context-docs/releases/tag/v0.1.6)
  from `b10a3058e43f9af278cbb7a6b2b70d41df16ea7d`, after reviewed
  [PR #2](https://github.com/jaredchu/context-docs/pull/2) merged and the exact
  [release-commit CI run](https://github.com/jaredchu/context-docs/actions/runs/38024377561)
  passed. Bundle core 0.1.6/adoption 0.1.7 and standard 0.1.1; retain the recorded
  experimental limits and earlier failed evaluation results.

## v0.1.6 release preparation — 2026-10-10 (prepublication checks)

- Prepare [release notes](docs/releases/v0.1.6.md) for core 0.1.6/adoption 0.1.7.
  All 21 local CI command groups pass with Python 3.12 on macOS: 146 unit tests,
  study/grader controls and four unchanged regenerated reports. Isolated package
  metadata and links pass; all 14 package files match the evaluated candidate.
- GPT 6 Astra High drafted the notes; Claude Opus 5.5 found no blocking issue.
  Its package-identity evidence gap was resolved with exact hash comparisons.
  Validation and review records distinguish local checks, native study outcomes
  and publication status. No package behavior or version changed in preparation.

## Audience/destination native evaluation — 2026-10-10 (included in v0.1.6)

- Complete the [five-case pilot](evals/results/2026-10-10-audience/README.md) on
  core 0.1.6/adoption 0.1.7: execution gates pass 5/5; GPT 6 Astra High and Claude
  Opus 5.5 each accept 19/19 target and 15/15 general criteria. No retries or
  material findings. The mixed case completes the API edit and asks for handoff
  readers/destination; it does not produce the handoff artifact. Audit attempts
  no writes, searches or journal reads. No comparative or general reliability claim.
- Before freezing, correct journal search-content observation, verify denied
  writes do not halt valid execution, disable subject auto memory and record
  unique build identity and destination scope. Claude's focused re-review found
  no blocking issues. Nineteen audience controls, seven reused guard tests and
  static checks pass separately. Historical studies and packages are unchanged.

## Audience/destination evaluation preparation — 2026-10-09 (included in v0.1.6)

- Prepare five isolated synthetic cases with a restricted native runner, pinned
  candidate skills, exact input/control hashes, invocation provenance and selected
  trajectory export. Separate audit write attempts and journal scan scope from
  actual changes or returned evidence.
- Twelve new runner controls, seven reused guard tests and repository static checks
  pass; a disposable build passed manifest and input validation. Claude Opus 5.5
  reviewed fixture design; its material ambiguities were addressed before any run.
  At this preparation stage, counterpart harness review and final freeze remained
  pending and no subject session was launched. The October 10 entry records the
  later evaluation. Installable packages were unchanged.

## context-docs 0.1.6 — 2026-10-09 (bundled in `v0.1.6`)

- Select retained information by audience, sharing destination and lasting
  usefulness, using public, private-team and personal-project examples. Keep
  portable current context separate from detailed evidence and local state;
  preserve relevant operational constraints and failed results. Standard advances
  to 0.1.1. Adoption remains 0.1.7.
- Apply the guidance to this repository: shorten current context, preserve decision
  history, and normalize incidental host metadata in public evidence copies with
  a hash ledger and local originals. Historical scores and Git history remain
  unchanged. See the [redaction record](docs/evidence-redaction-2026-10-09.md).
- Skill metadata validation and all 20 local CI-equivalent check groups pass,
  including 127 unit tests, static checks, grader controls and four unchanged
  regenerated reports. The 43 redacted copies were verified against local originals
  for declared transformations and unchanged scores. Five new audience/destination
  scenarios were synthetic and unexecuted at that stage; the October 10 entry
  records their subsequent native evaluation.
- GPT 6 Astra High implemented the guidance; Claude Opus 5.5 found no blocking
  skill issue. Its documentation findings were resolved with validation details,
  per-study redaction notices and restored historical navigation. Codex integrated
  cleanup and verified the declared transformations against original bytes.

## Public-adoption evaluator marker handling — 2026-10-09 (included in v0.1.6)

- Accept a marker-only insertion as bare lines or a bounded Markdown fenced
  block while preserving the exact existing rule, date uncertainty and entry path.
  Version the revised protocol for future freezes; retain the completed study's
  original files and scores. This changes evaluation tooling only; skill packages
  and versions remain unchanged.
- GPT 6 Astra High implemented the change; Claude Opus 5.5 found no blocking
  issues in a read-only review. Applied its ASCII-label restriction and additional
  boundary controls. All 28 evaluator controls, seven reused guard tests and static
  checks pass. These are mechanical checks, not new agent evaluations.

## adopt-context-docs 0.1.7 — 2026-10-09 (bundled in `v0.1.6`)

- Clarify that newly added maintenance wording may adapt to local terminology
  without client-specific invocation syntax, consistent with v0.1.3. Preserve
  existing equivalent guidance as written.
  Correct the stale current adoption version in project context; core then remained 0.1.5.
- Repository static checks, 13 checker regressions and 30 existing adoption,
  routing and marker controls pass. These are mechanical checks.
- A [bounded public-source regression](evals/results/2026-10-09-public-adoption/README.md)
  ran four native Claude Opus 5.5 sessions on one pinned Go project with two
  synthetic overlays. Execution passed 4/4; frozen mechanical checks passed 3/4,
  retaining a fenced-marker failure. Both reviewers accepted target preservation
  behavior in all four, but full-claim semantic scores differ (Astra 1/4, Claude
  3/4); both found an unsupported verification claim in the repeat. No retries,
  comparative benefit or general reliability claim. Twenty-three new harness
  controls, seven reused guard tests and static checks passed separately.

## context-docs 0.1.5 — 2026-09-29 (tag `v0.1.5`)

- Add an opt-in auto preference for projects outside Git. A read-only policy helper
  distinguishes confirmed absence from detection errors and recognizes parent
  repositories, worktrees and bare repositories. Explicit project settings win;
  saved enablement survives adding Git. Audits and default adoption remain unchanged.
- Eight new policy tests, 35 total journal/policy tests, 13 checker regressions,
  one native guard regression, both metadata validators and static checks pass.
  The [native evaluation](evals/results/2026-09-29-auto-preference/README.md) retains
  six sessions: two Codex harness blocks and four functional passes after correcting
  its shell-read boundary. Claude guard denials and journal filename enumeration
  remain qualifications. Writer/schema and global installations are unchanged.

## adopt-context-docs 0.1.6 — 2026-09-29 (bundled in `v0.1.5`)

- Route user-selected auto preferences through the core 0.1.5 journal guide while
  preserving explicit settings, custom paths, adoption dates and existing history.
  The same native evaluation verifies one-line enablement, unchanged default/off/
  Git/error projects and read-only audits. Installation alone does not enable logging.

## context-docs 0.1.4 — 2026-09-28 (tag `v0.1.4`)

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
  The [v0.1.4 release notes](docs/releases/v0.1.4.md) retain invocation limits.

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
