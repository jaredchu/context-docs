# Context Docs standard

Version: 0.1.0 (experimental).

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

A small project may keep the first four roles in one `context.md`. An established
project may use `docs/README.md`, several registers, and runbooks. Neither is more
compliant by filename. Create a separate file when it improves navigation or
ownership, not to fill every row of this table.

The entry point should identify the project and its boundaries and link to
canonical details. Prefer repository-relative links for portable project docs.
Do not copy facts between unrelated projects to simulate continuity.

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
