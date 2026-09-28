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

## Evaluation priority

Retained content, factual accuracy and consistency are primary. The completed
[quality-first study](../docs/evaluation-2026-09-27-quality.md) compares scattered,
conflicting and absent context against ordinary maintenance and Context Docs,
then tests fresh readers. Both maintenance methods capture all required items;
all reader arms reach perfect scores on these small fixtures. No incremental
skill accuracy advantage is established. See the [runnable study](quality/README.md)
and [broader protocol](quality-protocol.md). The scenarios below remain maintenance
regression checks; their pass rates do not establish downstream usefulness.
Speed, tokens and size are supporting diagnostics, not quality substitutes.

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
merge recommendation remains on hold without a claim that the skills caused the
original factual errors. Prior attempts retain their original criteria and scores.
These author-reviewed development cases do not establish cross-client reliability.

## Optional adoption skill

Use the [adoption regression](adoption/README.md) for `adopt-context-docs` changes.
It checks initial adoption and repeated use on projects with no documentation and
with existing rules, a custom layout and uncommitted work. Core maintenance studies
do not establish the adoption wrapper's behavior.
