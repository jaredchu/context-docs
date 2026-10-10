# Context Docs standard

Version: 0.1.1 (experimental).

This is a convention for project knowledge, not a required directory tree or file
format beyond readable Markdown. Use the project's established terms and map
them to these meanings. Do not introduce metadata fields that nobody will use.

## Document roles

| Role | Answers | What belongs here |
| --- | --- | --- |
| Entry point | Where should a new reader start? | Purpose, scope, canonical links and reading order |
| Current state | What is true now? | Verified state, active work, blockers and next actions |
| Decisions | What was chosen, by whom, and why? | Status, authority, rationale, consequences and sources |
| Open questions | What still needs an answer? | Uncertainty, impact and the evidence or decision needed |
| Procedures | How is work performed? | Applicable steps, prerequisites and relevant verification |
| Historical evidence | What happened, and what supports it? | Dated observations, evaluations and superseded rationale |
| Local working state | What helps this workspace's operator? | Useful machine setup, temporary diagnostics or installation state with an appropriate local destination |

A small project may keep the first four roles in one `context.md`. An established
project may use `docs/README.md`, several registers, and runbooks. Neither is more
compliant by filename. Create a separate file when it improves navigation or
ownership, not to fill every row of this table.

The entry point should identify the project and its boundaries and link to
canonical details. Prefer repository-relative links for portable project docs.
Do not copy facts between unrelated projects to simulate continuity.

## Audience and destination

Choose content from the user's intent, intended readers and actual sharing
destination before relying on labels such as public, private or personal. One
project can have public contributor docs, restricted operations notes and local
working state. Use the request and available project guidance to understand that
boundary; ordinary maintenance does not require a new permissions audit or broad
file inventory.

For each detail, consider its use to the next reader, how long it remains useful,
and whether this destination is appropriate for it. The following are examples,
not required layouts or permission grants:

| Audience and destination | Useful project knowledge | Where more specific detail belongs |
| --- | --- | --- |
| Public contributors or users | Purpose, supported behavior, decisions, reproducible setup, environment constraints and known failures | Shared procedures and source-backed reports; incidental developer installations, backup locations and scratch state stay with the operator unless needed to explain a project issue |
| Private team with a suitable restricted destination | Shared architecture, current blockers, decisions and necessary operational information | Existing restricted runbooks or incident records for internal endpoints, recovery steps and relevant diagnostic detail; a private-project label does not make every document an appropriate recipient |
| Personal project or private workspace | Durable preferences, local paths, machine constraints or workflows that the owner actually needs | Reuse the owner's chosen notes and procedures; local detail can be essential, while expired temporary state need not fill current context |
| Unknown or mixed visibility | Supported facts and decisions appropriate to the established destination | Continue harmless maintenance without assuming the whole project is public or private; ask only when unresolved audience or destination ambiguity materially changes what may be recorded or shared |

Keep current state, active constraints and next actions in current context.
Put repeatable instructions in procedures and dated investigations, reproduction
conditions and evaluation outcomes in their existing historical records. Link
from current context to the detail that explains a present limitation. Keep
incidental machine state local when it has no wider purpose; do not move all
technical detail to ignored files or require Git, a new folder tree or a new store.
An absolute diagnostic path or exact environment version may be necessary evidence,
including for a public failure report; retain its relevant meaning instead of
discarding it merely because it originated on one machine.

When preparing a public copy from restricted evidence, include only the needed
detail and sanitize identifiers that do not belong in that destination. Preserve
diagnostic relationships, source provenance and the transformation's limits.
Keep the original evidence in its appropriate existing destination; resolve an
unsuitable or unknown destination before moving it. Cleanup does not authorize
silently discarding raw evidence or rewriting frozen inputs, historical scores
or failed evaluations. A sanitized derivative is distinct from its source.

Apply the same audience and destination choices to optional journal payloads.
This does not enable logging or justify scanning history; follow the skill's
existing capture and read triggers. Keep credentials out of context and refer to
existing approved secret storage when a procedure needs them. Retain personal or
customer details only when necessary for the authorized task and suitable for
the intended destination.

## Statements and authority

Keep these distinctions explicit when ambiguity could change what the next
person or agent does:

- **Observed:** supported by identified evidence, with an observation date when
  freshness matters. Say whether the evidence is code, configuration, a test or
  live state; those are different claims.
- **Approved:** a decision made by someone with authority for that project.
  Retain the authority/source and rationale. An assistant suggestion is not
  approval, and implementation alone need not establish owner approval.
- **Proposed:** a suggested future action or decision, not current policy.
- **Unknown:** unresolved information or conflicting sources, with the next
  useful check when known.
- **Superseded:** earlier guidance replaced by identified newer guidance.
  Preserve rationale or historical evidence that remains useful.

These are semantic categories, not compulsory labels on every sentence. Preserve
an existing equivalent status vocabulary. Implementation state and decision
status are separate: an approved change can remain unimplemented, and deployed
behavior can disagree with an approved decision.

When code and docs differ, correct claims about what the code does while keeping
the decision discrepancy visible. Do not silently rewrite approved intent to
match implementation, or declare runtime behavior from code alone. If a needed
source is inaccessible, state the verification limit instead of inventing it.

## A maintenance cycle

Maintain context after meaningful changes to behavior, configuration, decisions,
procedures or project status, or when the user requests a review. Routine work
that adds no durable information needs no new note.

1. Read the entry point and affected canonical sections.
2. Identify the new evidence and which claims it changes.
3. Update current state and preserve decision status and source references.
4. Consolidate duplication and move details only where that helps navigation.
5. Check the diff, links, pending work and information preservation.

Treat dates as evidence boundaries. Updating one configuration fact does not
justify stamping an entire unreviewed runbook as current. Record a command's
scope and result when useful; omit repetitive command logs.

## Controlling growth

Keep current context focused on the next reader's decisions. Replace resolved
status items rather than appending a daily diary. Keep detailed evidence in one
canonical location and link from summaries.

Word counts are signals, not deletion quotas. Split an entry point when unrelated
detail makes it hard to navigate. Consolidate repeated facts only after checking
that their qualifications agree. A short file that loses a constraint is worse
than a longer accurate file.

Use Git for edit history where available. Retain important decision rationale,
evaluation evidence and unresolved work in readable documents even when Git
exists. Mark archived guidance as historical and keep inbound links useful.
Never delete uncommitted material on the assumption that Git can recover it.

## Minimal adoption

For an existing project, map its files to roles and fix the most consequential
gaps in place. Do not migrate directories just to match an example. For a new
project, start with [one context document](../assets/project-context.md) linked
from the README. Add a [decision record](../assets/decision-record.md) only when a
decision warrants its own rationale. No manifest, database or index is required.

## What this standard does not provide

Markdown/Git does not automatically resolve concurrent edits, enforce access
permissions, verify facts, or run maintenance. Agents must inspect edits and use
available evidence; Git helps review and recovery. Cross-device synchronization
uses the user's existing repository workflow. Any future search service should
preserve source paths and revisions and remain separable from the originals.
