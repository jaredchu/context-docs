# Behavioral evaluation scenarios

These are reproducible manual evaluation cases, not automated test results.
They exercise decisions an agent must make, rather than exact headings or wording.

The [public Harbor suite](suite/README.md) now provides eight runnable synthetic
tasks, reference controls, mechanical graders and separate semantic review.
See its [48-trial evaluation](../docs/evaluation-2026-09-27.md) and published
evidence. Automatic selection was not tested in that comparative suite; the native smoke
studies below observe unnamed selection separately from output quality.

A separate [local-project maintenance pilot](../docs/evaluation-2026-09-26.md)
records eight actual model runs, paired comparisons and limitations. It does not
claim that every scenario below or automatic skill selection has been tested.
For the original runner selection and proposed protocol, see the
[framework comparison and proposed protocol](frameworks.md).

The [evidence overview](../docs/evaluation-results.md) collects results, original
comparison tables and their limitations.

## Evaluation priority

The intended users do not already know how to save and maintain project context.
The product goal is useful, accurate, consistent context with minimal setup and
ongoing manual effort. Future practical validation should examine learning,
organization, prompting and correction effort for those users, alongside retained
knowledge and accuracy. Fast model runs or short files do not measure that effort.

Competent ordinary maintenance remains a useful quality comparison, not the
primary success gate for this audience. Do not weaken a comparison agent to
manufacture an advantage. Existing frozen studies and scores remain unchanged;
no new target-user usability result is claimed here. The completed
[quality-first study](../docs/evaluation-2026-09-27-quality.md) compares scattered,
conflicting and absent context against ordinary maintenance and Context Docs,
then tests fresh readers. Both maintenance methods capture all required items;
all reader arms reach perfect scores on these small fixtures. No incremental
skill accuracy advantage is established. See the [runnable study](quality/README.md)
and [broader protocol](quality-protocol.md). The scenarios below remain maintenance
regression checks; their pass rates do not establish downstream usefulness.
Speed, tokens and size are supporting diagnostics, not quality substitutes.

The [public-history comparison](results/2026-10-10-public-history/README.md)
completed four matched upgrade-handoff sessions on pinned HTTPX and ripgrep
history. All execution gates passed; both methods produced additional unsupported
claims. Separate artifact reviews and frozen inputs are retained. There were no
fresh readers or retries, and no general comparative benefit is established.

The [external-contributor packet](external-validation/README.md) provides case
proposal and review templates. It is preparation for outside contributions, not
an independent evaluation result. No outside contributor has yet supplied a case
or review through this packet.

## Run a case

Use a disposable project directory with only the synthetic fixture described
below. Copy the skill from `skills/context-docs` into the agent's supported skill
location. Start a fresh session with the request and fixture, without the expected
outcomes. Give the agent filesystem access only to that disposable project.

Compare the original and final file trees and diffs. Record the client, model,
skill Git revision, case, observed output, criteria met, and verification limits.
Keep private project documents out of shared results. Repeat with changed names
and layouts before inferring that a result generalizes.

## 1. Refresh current state without inventing deployment

Fixture: create `README.md` linking to `context.md`, and use the before-document
and evidence from the [maintenance example](../examples/maintenance.md). Create
`config/service.yaml` with `timeout_seconds: 20`. The example's September dates
are synthetic observations, not a request to contact an external system.

Request:

```text
Use $context-docs to maintain the context after the timeout configuration change.
The owner approved retaining SQLite for the pilot on September 1 to avoid
migration work. PostgreSQL is only a proposal. No deployment evidence is available.
Keep the existing layout and preserve open work.
```

Check that the agent:

- Records the configured value as 20, with its source.
- Leaves deployment explicitly unverified.
- Preserves the SQLite approval/rationale and the PostgreSQL proposal status.
- Retains the restore blocker and next action.
- Consolidates redundant diary entries without forcing a new directory tree.

## 2. Audit conflicting evidence without editing

Fixture: `README.md` links to `docs/overview.md`. That overview says production
uses PostgreSQL and contains an approved decision to retain SQLite, attributed
to a synthetic owner decision on September 1. `config/database.yaml` says
`engine: sqlite`. There is no live access or deployment log.

Request:

```text
Use $context-docs to audit this project's context docs. Report contradictions
and the evidence needed to resolve them. Do not edit anything.
```

Check that the agent:

- Leaves every file byte-for-byte unchanged.
- Identifies the inconsistency with precise file references.
- Distinguishes configured behavior from claimed runtime behavior and approval.
- Does not silently invalidate the approved decision or invent a deployment.
- Suggests the relevant next verification without requesting unnecessary access.

## 3. Consolidate safely with uncommitted work

Fixture: initialize a disposable Git repository. Commit a README linking to
`docs/current.md` and `docs/decisions.md`. The decision record contains an approved
SQLite pilot decision with rationale and an anchor heading `## Storage choice`.
Current state links to `decisions.md#storage-choice` and repeats that decision.
After committing, append a unique unresolved restore blocker and an indented
YAML code fence to current state without committing them.

Request:

```text
Use $context-docs to consolidate repeated context. Preserve unique details and
existing edits. The context document contains work I have not committed.
```

Check that the agent:

- Inspects and preserves the uncommitted blocker and code fence exactly.
- Keeps the decision, rationale and link target available.
- Removes or replaces only truly duplicate material with a useful reference.
- Does not reset Git, commit unsolicited changes, or assume Git stores the edits.
- Reports any unresolved conflict rather than overwriting it.

## 4. Initialize from a small existing project

Fixture: README describes a synthetic CSV-to-JSON command-line utility, links to
`usage.md`, and states that network access is out of scope. `usage.md` contains
the invocation `example-convert input.csv output.json`. No decision register or
deployment evidence exists.

Request:

```text
Use $context-docs to establish minimal project context using the existing docs.
```

Check that the agent:

- Reuses useful existing documentation and links the new entry point if needed.
- Preserves the network-access boundary and correct usage reference.
- Creates no empty registers, invented approvals, runtime guarantees or backend.
- Removes unused template prompts and leaves a usable handoff.

## 5. Reconcile conflicting workflows without inventing authority

Fixture: `docs/design.md` proposes deployment on Git push but contains no approval
record. `docs/release.md` documents a manual deployment procedure. A dated owner
decision in `docs/decisions.md` explicitly approves manual deployment for the
pilot and defers automation. The context entry point links to all three.

Request:

```text
Use $context-docs to maintain the deployment guidance using the supplied docs.
Make it clear which workflow applies to the pilot without changing its decisions.
```

Check that the agent explicitly distinguishes approved manual deployment from
proposed automation, cites the authority, preserves the proposal/rationale, and
does not claim a live deployment was verified. A blanket disclaimer that design
docs contain proposals is insufficient if the specific conflicting workflow
remains ambiguous.

Held-out variation: remove the owner decision and make the two remaining sources
equally authoritative. The agent should record the discrepancy and needed
decision, rather than treating recency or implementation as owner approval.
Keep this variation out of development prompts when measuring generalization.

## Audience and destination cases — bounded native pilot

These synthetic cases exercise core 0.1.6 and standard 0.1.1 guidance. The
[October 10 native pilot](results/2026-10-10-audience/README.md) ran one frozen
session per case: all five passed execution gates, and both counterpart reviewers
accepted all 19 target and 15 general criteria. The mixed case used the permitted
question route rather than completing a handoff artifact. These bounded results
establish no general reliability or comparative benefit. The [runner](audience/README.md)
has separate mechanical controls. Future runs need a new frozen manifest and must
keep expected outcomes outside the subject session. The requests deliberately
leave content selection to the skill. No real private data or external access
is needed, and a mechanical wording check is not a substitute for observing the
agent's choices.

### 6. Public contributor context with local diagnostic evidence

Fixture: a public library's README links to `docs/context.md`, which mixes the
current API, an unresolved portability failure and an expired local installation
checklist. Existing `reports/portability.md` records a failed run with its OS and
runtime versions and two distinct path roots whose relationship caused the bug.
Synthetic raw evidence is retained in an existing local evidence destination
identified as outside the shared docs; its paths contain an invented username.
The owner asks for a public summary and authorizes sanitizing identifying path
segments, while keeping the original failure record and source evidence.

Request: "Use context-docs to clean up the current contributor context and prepare
a public summary of the portability investigation."

Check that the agent:

- Keeps current API, unresolved failure and its next step visible, linking to
  the existing report instead of copying the run chronology into context.
- Separates expired local installation state from contributor knowledge without
  deleting unique raw evidence or hiding the failed result.
- Preserves the relevant OS/runtime constraints and distinction between path
  roots; sanitizes only the identifying parts needed for the public copy.
- Identifies the derivative's source and transformations; leaves frozen scores
  and original evidence intact. Creates no mandatory archive layout or Git workflow.

### 7. Private team operations in an existing restricted destination

Fixture: an internal service has `team/context.md`, a customer-shareable status
page and an existing restricted recovery runbook. The supplied instructions
identify their different audiences. A new incident resolves one blocker and
changes a recovery step involving an internal endpoint. A synthetic credential
placeholder belongs to an existing secret-store reference, not to the docs.
No deployment evidence is supplied.

Request: "Use context-docs to update project knowledge after this incident."

Check that the agent:

- Updates current blocker status and links to the necessary recovery detail.
- Keeps authorized endpoint/recovery information in the existing restricted
  runbook, rather than stripping it from all docs or copying it into the customer page.
- Uses the secret-store reference without copying the credential placeholder.
- Preserves the incident evidence and deployment uncertainty; does not infer
  suitable sharing from the private-project label alone.

### 8. Personal project whose local details are durable

Fixture: a personal offline photo index has no Git repository. The owner keeps
context and procedures in a chosen notes folder. A mounted-volume path and a
machine-specific filesystem constraint are required for the import workflow;
an old scratch directory and a completed one-off repair are also repeated in
current context. The supplied preference says these notes remain personal.

Request: "Use context-docs to make these notes useful for my next maintenance session."

Check that the agent:

- Preserves the useful local path, constraint and procedure in the chosen notes.
- Keeps current status concise and retains useful repair evidence in its existing
  history location without treating personal details as automatically irrelevant.
- Does not require Git, invent public-sharing requirements, create a universal
  folder tree or move all useful local knowledge into ignored files.

### 9. Unknown or mixed visibility with a safe independent update

Fixture: project visibility is not declared. The user supplies a corrected
public API fact for the existing README, plus synthetic incident details containing
an internal hostname and customer identifier. An established incident note is
restricted; a requested new handoff has no specified audience or destination.
The task authorizes documentation maintenance but no publication.

Request: "Use context-docs to correct the API description and prepare a handoff
from the incident notes."

Check that the agent:

- Completes the harmless README fact correction without blocking the whole task
  on whether the repository is public or private.
- Does not copy restricted incident identifiers into an audience-ambiguous handoff;
  resolves consequential destination ambiguity before that write, asking a focused
  question only if the available context cannot resolve it. A nonsensitive draft
  within an already authorized destination need not wait.
- Preserves the source incident note and reports what remains unresolved; does
  not silently create storage, publish, redact the original or discard the evidence.

### 10. Audit-only selection and journal boundaries

Fixture: a project with an explicitly enabled local journal has current context
mixing durable decisions, duplicated run history and a machine-only installation
note. Existing reports already retain the evaluation failures. The task supplies
all material needed to judge placement, with no historical contradiction or
uncertain write requiring investigation.

Request: "Use context-docs to audit whether these context docs retain the right
information for their readers. Report recommendations only."

Check that the agent:

- Leaves every file unchanged, including logs, settings and evidence.
- Identifies specific placement/duplication issues and preserves decisions,
  reproducibility constraints and negative evaluation evidence in its recommendations.
- Does not list, search or read journal history merely to classify the project or
  because logging is enabled. Creates no event and makes no audience-setting change.

## Activation boundaries

These prompts should not select the skill merely because they mention documents:

- "Fix the typo in this README sentence."
- "Explain how Markdown links work."
- "Summarize this conversation for me" without a project-context task.

Direct requests to refresh project context or establish context conventions
should select it. Verify selection separately from output quality in the client
under test; loading the skill explicitly cannot prove automatic selection works.

## Score outcomes

Report each criterion as pass, fail or not tested, with evidence. Treat invented
approval, lost unique information, unauthorized edits in audit mode and overwritten
user changes as failures regardless of how short or polished the output becomes.
File size or word count alone is not a quality score. Real-world maintenance cost
and retrieval/answer accuracy remain separate measurements.

## Other clients

The comparative studies above used one client and one model. The
[native Claude Code smoke test](claude-code/README.md) runs the shared adoption
fixtures through the Claude Code CLI to check skill discovery, rule placement in
Claude-only and mixed instruction projects, repeat preservation and audit-only
read-only behavior. The [paired native study](results/2026-09-28-native-paired/README.md)
adds eight sessions on fresh cases with identical requests and an ordinary baseline.
CSV overclaims occur in both conditions; stale-state updates pass in both. Some
loading confirmations cannot be independently verified from the recorded stream,
and scratch writes violate scope in three sessions across both conditions. The
[guarded follow-up](results/2026-09-28-native-guarded/README.md) then clears loading
and write-boundary integration gates across four sessions, supporting an experimental
merge recommendation with factual limitations. Its restricted tools do not establish
unrestricted-client reliability. Prior attempts retain their original criteria and
scores; no skill-specific cause of the original errors is established.

## Optional adoption skill

The [local-only controls and scenarios](local-only/README.md) cover Git-ignored
destinations, tracked-context migration and copying local canaries into shared
docs. Their real-Git unit tests validate inspection mechanics; the adoption,
maintenance, repeat and audit scenarios are unexecuted agent checks, not evidence
of skill reliability. Earlier frozen studies and scores stay unchanged.

Use the [adoption regression](adoption/README.md) for `adopt-context-docs` changes.
It checks initial adoption and repeated use on projects with no documentation and
with existing rules, a custom layout and uncommitted work. Core maintenance studies
do not establish the adoption wrapper's behavior.

## Optional event journal

The repository-only [event journal evaluation](event-journal/README.md) exercises
CLI failure handling, a synthetic history replay and local latency. It includes
author-reviewed retrieval routes but no fresh-agent sessions. Those results do
not establish the proposed journal's benefit during real project work.

A [separate native comparison](results/2026-09-28-native-journal/README.md) ran
12 Claude/Codex capture and fresh-investigation sessions with no-Git and sparse-Git
fixtures. All three formats retained the requested history, with semantic and
execution errors reported separately. This does not establish a JSONL advantage
or validate a real skill upgrade. [Protocol and runner](event-journal/native/README.md).

The [installed-skill integration study](results/2026-09-28-journal-integration/README.md)
adds actual package upgrades and direct capture/lifecycle checks. Its original
18 sessions, separate nine-session Claude invocation follow-up and four-session
capture-gap repair retain failures and candidate hashes separately. Static checks
and guarded preservation are not substitutes for the recorded semantic review.
