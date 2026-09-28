# Changelog

Each installable skill under `skills/` carries its own version in a `VERSION`
file and moves independently. The repository tags `v0.1.0` and `v0.1.1` name core
skill releases only; later entries identify the package they change. Versions are
reconstructed here from the commits and dated reports they were published with,
so the history is auditable without reading every evaluation document.

Every entry states what was actually tested. A static check or an authored example
is not a behavioral evaluation, and adopting a version is an implementation choice,
not a demonstrated accuracy gain.

## Repository checks and installation guidance — unreleased

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
  evaluations. Installable skill contents and versions are unchanged.

## adopt-context-docs 0.1.3 — unreleased

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
