# Evaluation results

The [September 27 study summary](evaluation-summary-2026-09-27.md) provides the
earlier study map; the sections below retain subsequent evidence and limitations.

Success means helping the intended users preserve useful, accurate project
knowledge with minimal setup and ongoing manual effort. Relevant effort includes
learning the workflow, deciding what to save, organizing documents, prompting the
agent and correcting its output. **Shorter files or faster model runs alone do
not establish that goal.**

Comparisons with competent ordinary maintenance help assess output quality; beating
an expert workflow is not a requirement for serving users who lack one. The studies
below retain their original findings and limits. They do not yet establish how much
effort Context Docs saves its intended users; factual errors still matter.

The [October 10 local-only follow-up](../evals/local-only/validation-2026-10-10/README.md)
executes seven cases per native client and two fresh read-only audits. Storage and
preservation checks pass, with stale-source selection, denied journal writes and
a recovered postprocessing failure retained separately. These direct-invocation
fixtures do not establish implicit selection or automatic instruction loading.

The [quality-first study](evaluation-2026-09-27-quality.md) compared two
synthetic projects with scattered, conflicting or absent context. It ran 12
three-stage maintenance trials, followed by 36 fresh-reader sessions: **72 model
sessions and 216 reader answers**, plus reference/no-op controls.

<!-- quality-table:start -->
| Final-artifact measure | Unmaintained | Ordinary maintenance | Context Docs v0.1.1 |
| --- | ---: | ---: | ---: |
| Required knowledge recorded | 12/54 | 54/54 | 54/54 |
| Correct, supported reader answers | 72/72 | 72/72 | 72/72 |
| Correct in both reader sessions | 36/36 | 36/36 | 36/36 |
| Target-claim accuracy | 37.5% | 100.0% | 100.0% |
| Missing required items | 22 | 0 | 0 |
| Incorrect required items | 20 | 0 | 0 |
| Critical document findings | 11 | 0 | 0 |
| Conflicting required items | 0 | 0 | 0 |
<!-- quality-table:end -->

Both maintenance methods improved the stored record. **Context Docs did not
outperform ordinary maintenance on these quality measures.** Readers could inspect
the same small raw evidence set in every arm and all answered correctly, including
with unmaintained docs. This reader ceiling establishes no accuracy advantage or
general equivalence. Both maintenance arms retained all required items through an
evidence update and made no edits in the final no-change pass.

Coverage counts required knowledge captured accurately in maintained Markdown;
raw-file survival alone does not count. Target-claim accuracy excludes missing
items, which are shown separately. Incorrect current claims and unresolved
operative conflicts are separate categories. The two projects contain only
514–656 total input words, are author-created and author-reviewed, and have one
maintenance trial per scenario/arm. This is a reproducible development study,
not an independent benchmark. See the [method, per-project results and limits](evaluation-2026-09-27-quality.md),
[execution commands](../evals/quality/README.md), and
[snapshots and scored evidence](../evals/results/2026-09-27-quality/README.md).

A [larger public-source pilot](evaluation-2026-09-27-public.md) used pinned
Flask and Click releases containing 143,604 and 102,647 source/test/doc words.
It completed four handoffs and 12 fresh readers: **16 sessions, 72 answers**.
Existing upstream documentation stayed intact; this complements the weak-docs
comparison above.

<!-- public-table:start -->
| Reader outcome | Upstream docs/code | Ordinary handoff | Context Docs v0.1.1 |
| --- | ---: | ---: | ---: |
| Flask | 12/12 | 11/12 | 12/12 |
| Click | 12/12 | 12/12 | 12/12 |
| **Total** | 24/24 | 23/24 | 24/24 |
| Correct in both phrasings | 12/12 | 11/12 | 12/12 |
<!-- public-table:end -->

Both handoff methods covered 24/24 required items. The one ordinary-reader miss
omitted a required cleanup guard. **No skill-specific accuracy advantage is
established:** recorded traces show that none of the eight readers given handoffs
opened their content; they answered from upstream sources. The ordinary handoff
already contained the omitted guard. The protocol also prohibited adding a link
from the upstream README, limiting discovery. This tests handoff availability,
not the effect of confirmed handoff consumption.

Sources were externally authored, but questions and reviews were not independent.
There was one maintenance attempt per method/project, and both projects belong
to the same ecosystem. See [the discovery finding, exact miss and limits](evaluation-2026-09-27-public.md)
and [all outputs and judgments](../evals/results/2026-09-27-public/README.md).

A [routing follow-up](evaluation-2026-09-27-routing.md) then reused those
handoffs unchanged, added equivalent orientation links to temporary READMEs,
and compared README-first discovery with explicitly directed reading. It ran
**12 fresh sessions and 72 answers**, using one previously tested phrasing.

<!-- routing-table:start -->
| Reader mode and outcome | Upstream orientation | Ordinary handoff | Context Docs handoff |
| --- | ---: | ---: | ---: |
| README-first discovery: supported answers | 12/12 | 12/12 | 12/12 |
| README-first discovery: full orientation text exposed | 1/2 | 2/2 | 2/2 |
| Directed reading: supported answers | 12/12 | 12/12 | 12/12 |
| Directed reading: full orientation text exposed | 2/2 | 2/2 | 2/2 |
<!-- routing-table:end -->

All eight handoff readers received the complete document before answer-writing,
verified from model-visible tool output. All 12 readers saw the complete README.
**Accuracy remains tied:** the original sources also support every answer. This
checks reading under the new routing/instructions; it does not establish a skill
advantage, unguided discovery or equivalence. The earlier omitted cleanup guard
is present in the repeated answers. See [the unchanged criteria, exposure method
and limitations](evaluation-2026-09-27-routing.md) and
[reproducible evidence](../evals/results/2026-09-27-routing/README.md).

A [decision-history follow-up](evaluation-2026-09-27-history.md) replayed two
externally authored Python policy histories through four maintenance passes:
**28 model sessions and 96 reader answers**. It tests evolving requirements,
authority, rationale and authentic source contradictions; both histories come
from one project and the questions/review remain author-created.

<!-- history-table:start -->
| Outcome | Unmaintained | Ordinary maintenance | Context Docs v0.1.1 |
| --- | ---: | ---: | ---: |
| Required knowledge in final context | 0/16 | 16/16 | 16/16 |
| Required knowledge across all stages | 0/63 | 63/63 | 63/63 |
| Correct, supported reader answers | 32/32 | 32/32 | 32/32 |
| Correct in both reader sessions | 16/16 | 16/16 | 16/16 |
| Readers exposed to all Markdown | 4/4 | 4/4 | 4/4 |
| Critical document findings across stages | 0 | 0 | 0 |
<!-- history-table:end -->

Both methods retained every assessed item and made no Markdown changes in the
final no-new-evidence pass. **Reader accuracy tied**, including readers of raw
history alone; those original PEPs remain accessible in every arm. Zero in the
unmaintained column measures absent context summaries, not absent source facts.
One skill session briefly wrote a backup outside the allowed directories, then
corrected it; the project-file grader did not catch that. See the
[scope finding and limits](evaluation-2026-09-27-history.md) and
[all artifacts and explicit judgments](../evals/results/2026-09-27-history/README.md).

Existing studies provide maintenance regression coverage:

- **48 trials, v0.1.0 versus ordinary instructions:** both passed 24/24 under
  mechanical checks and author-reviewed semantic criteria. No correctness
  advantage was observed on these small fixtures. All audits preserved project
  bytes and final no-change passes preserved Markdown.
- **12 trials, v0.1.0 versus concise v0.1.1:** both passed 6/6. The candidate met
  its frozen preservation/concision rule and was adopted. This was a prompt
  refinement test, not evidence of better knowledge retention or reader answers.
- The [earlier local-project pilot](evaluation-2026-09-26.md) includes a
  workflow contradiction the skill missed. Passing synthetic cases does not
  erase that miss.

<!-- evaluation-table:start -->
| Task | Ordinary instructions | With Context Docs |
| --- | ---: | ---: |
| stale-config | 3/3 | 3/3 |
| workflow-conflict | 3/3 | 3/3 |
| decision-status | 3/3 | 3/3 |
| uncommitted-work | 3/3 | 3/3 |
| links-and-fences | 3/3 | 3/3 |
| audit-only | 3/3 | 3/3 |
| initialize | 3/3 | 3/3 |
| repeated-maintenance | 3/3 | 3/3 |
| **Total trials** | **24/24** | **24/24** |
<!-- evaluation-table:end -->

The 48-trial table is generated from recorded trials and explicit reviews. Its
fixtures contain only 19–87 Markdown words; the follow-up fixtures contain
572–676. Both studies use author-created cases and author review, not independent
held-out projects. Global instructions were excluded and recorded inputs checked.

Full results retain all observations, including document growth, slower runs and
resource overhead. These are secondary diagnostics, not the product's success
criteria: [48-trial report](evaluation-2026-09-27.md),
[v0.1.1 comparison](evaluation-2026-09-27-concise.md),
[reproduction commands](../evals/suite/README.md), and
[machine-readable results](../evals/results/2026-09-27-harbor/trials.json).

## Adoption regression history

Adoption v0.1.0 passed [two adoption-and-repeat regression cases](../evals/results/2026-09-27-adoption/README.md)
(four model sessions). Both repeat passes left project files unchanged. These are
small author-reviewed checks, not evidence of general reliability.
The [v0.1.1 marker regression](../evals/results/2026-09-27-adoption-marker/README.md)
retains an initial guidance-rewrite failure and date-test ambiguity. Targeted
follow-ups passed marker-only adoption, read-only auditing and explicit-date
preservation. Ten sessions across initial and revised conditions are reported
separately; the final revision was tested on the two affected unmarked cases.
Adoption v0.1.2 adds only the preferred layout for new sections. Metadata, package
links and existing static controls were checked; no new model evaluation was run.
Adoption v0.1.3 routes the rule and marker to the instruction file a client loads
and drops client-specific invocation wording. Its
[instruction-file cases](../evals/adoption/instructions.py) pass ten static grader
controls. The [v0.1.3 merge review](../evals/results/2026-09-28-adoption-v013/README.md)
ran nine model sessions: eight met frozen acceptance, with a split-file failure
involving an immutable heading and an installed-skill link. Routing rubrics passed,
but the original result is not a full regression pass. A
[separately frozen follow-up](../evals/results/2026-09-28-adoption-v013-followup/README.md)
passed four routing/repeat sessions after making file constraints explicit and
validating installed references consistently. That follow-up left the skills
unchanged; the initial failure remains recorded.
The [v0.1.7 public-source regression](../evals/results/2026-10-09-public-adoption/README.md)
ran four native Claude Opus 5.5 sessions. Target preservation behavior passed both
reviews; a frozen marker-format failure, unsupported verification claim and
semantic scoring disagreement remain recorded. This bounded study establishes
neither comparative benefit nor general reliability.
Per-version history is in the [changelog](../CHANGELOG.md).

## Native integration evidence

**Native support remains experimental.** The
[guarded follow-up](../evals/results/2026-09-28-native-guarded/README.md) passes four
loading/boundary checks, including a denied outside-project write and a fresh
read-only session loading the newly added maintenance rule. This clears those
integration gates and supports an experimental merge recommendation. The guard
is evaluation tooling with a restricted tool set; installing the skills does not
install a sandbox or enforce write confinement.

Factual limitations remain: the CSV response still overclaims value types. The
[eight-session paired study](../evals/results/2026-09-28-native-paired/README.md)
reproduced that error with and without the skills, while both conditions corrected
stale documentation. These author-reviewed runs on Claude Code 2.1.234 with Claude
Opus 5 establish neither a skill-specific accuracy advantage nor general reliability.
Earlier failures and scores remain recorded; file checks, execution and semantic
review are reported separately.

## Optional journal evidence

The [initial evaluation](../evals/results/2026-09-28-event-journal/README.md) covers
mechanical controls and a synthetic history replay; real-work benefit remains
unestablished.

The journal's goal is [efficient event capture for later investigation](event-journal-pilot.md#efficient-logging-goals).
Capture significant history when it happens and consult it when needed. Current
context improvement or savings are not its success criteria. The earlier
[same-chat handoff trial](event-journal-live-trial.md) tested a narrower question;
its findings do not establish whether historical logging earns its cost.
Before broader integration, the [journal requirements](event-journal-pilot.md#requirements-before-broader-integration)
call for comparison against Markdown/Git, native Claude and Codex evaluation, and
compatible updates for existing adopters. A [12-session native comparison](../evals/results/2026-09-28-native-journal/README.md)
now covers no-Git and sparse-commit histories: all three formats retained the
requested facts, with Claude factual overstatements and capture errors preserved.
JSONL remains optional. The [installed-skill lifecycle evaluation](../evals/results/2026-09-28-journal-integration/README.md)
now covers upgrades, direct capture, repeat setup, audits, helper absence and
logging disablement. Codex passed its functional stages; Claude required a
separately frozen explicit-invocation follow-up, with earlier failures retained.
A [targeted capture-gap fix](../evals/results/2026-09-28-journal-gap/README.md) preserves
failed-capture reasons for later readers. Natural recording-cost advantages and
general reliability remain unestablished. Installing or updating skills installs
the helper but does not enable logging.

The [auto-preference evaluation](../evals/results/2026-09-29-auto-preference/README.md)
records setting precedence and no-Git enablement outcomes, including retained
failures and the limits of its restricted sessions.

## More recent studies

The [audience/destination pilot](../evals/results/2026-10-10-audience/README.md) and
[public-history comparison](../evals/results/2026-10-10-public-history/README.md)
retain their individual outcomes, errors and review disagreements. These authored
studies do not establish effort savings for users new to context management.

The v0.2.x records cover [Markdown progress](../evals/progress/smoke-2026-10-16/README.md),
[visual paths](../evals/progress/smoke-0.2.1-2026-10-16/README.md) and
[default inline adoption](../evals/progress/adoption-default-2026-10-16/README.md).
Later focused smokes retain these qualifications:

- [Concise progress, v0.2.3](../evals/progress/smoke-0.2.3-2026-10-17/README.md):
  both clients pass the progress checks; Codex violates the permitted write scope
  by creating and removing a temporary hash file whose prior state is unknown.
- [Clarity, v0.2.4](../evals/clarity/smoke-0.2.4-2026-10-17/README.md):
  saved-Markdown checks pass in both clients; Claude's final chat report adds an
  unsupported gendered pronoun. No comprehension gain is established.
- [Shared-file coordination, v0.2.5](../evals/concurrency/smoke-0.2.5-2026-10-17/README.md):
  both respect ownership and handoff and recover from the forced stale edit;
  Claude retries its own second mismatch without rereading, and Codex corrects a
  read-only checking error. The separate
  [installed smoke](../evals/installed-skills/2026-10-18-concurrency-v025/README.md)
  passes one forced mismatch per client; it does not retest or clear those earlier
  qualifications. The [offline diagnostic](../evals/concurrency/offline-2026-10-17/README.md)
  records forced filesystem/tool outcomes separately from native sessions.

These guided, author-scored cases do not establish implicit loading, automatic
everyday reliability or user benefit. The concurrency checks do not establish
simultaneous-writer safety or general conflict prevention. Original outputs and
their study-specific limits remain authoritative in the linked records.

Current work prioritizes daily use and focused fixes when concrete issues arise.
Broader claims would need independently contributed cases or histories, independent
review with condition labels concealed, and evidence of the intended users' effort
and outcomes. Claims about downstream reader benefit also need verified context
reading. These are requirements for stronger evidence, not prerequisites for
ordinary use. See the [contribution packet](../evals/external-validation/README.md).

Return to the [project overview](../README.md) or browse the [evaluation scenarios](../evals/README.md).
