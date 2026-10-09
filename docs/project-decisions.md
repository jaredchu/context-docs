# Project decision history

Historical decisions and their recorded authority, moved from the context entry
point on 2026-10-09. Past release and installation approvals apply to those events;
they do not approve a new release or a different destination. Current direction is
summarized in [project context](project-context.md).

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

On September 29 the owner approved visible README credit for Codex as the primary
AI development contributor, with Jared Chu as creator/maintainer and Claude also
credited. The [commit attribution policy](../CONTRIBUTING.md#commit-attribution)
uses Codex's verified co-author trailer for future assisted commits while preserving
human authorship and existing history. Contributor-graph placement is not established.

On October 9 the owner designated GPT 6 Astra with High reasoning and Claude
Opus 5.5 as the project's ongoing collaborators. The
[project instructions](../AGENTS.md#model-collaboration) record the working rule;
the owner also delegated reasonable task assignment and peer review. Task-fit
assignment, one owner per change and focused counterpart review for substantive
changes implement that preference, with proportionate checks for routine edits.
This records the requested models, not a change to an active chat's
model configuration or a claim that both models reviewed every prior change.


On October 9 the owner requested that Context Docs choose what to retain according
to different project types after reviewing local-development clutter in this
repository. Audience, destination and lasting usefulness are the implementation
criteria; public/private/personal examples guide judgment rather than mandating
new folder layouts. The owner also agreed to cleanup before release. This does
not authorize rewriting published Git history or publishing the new release.

The [September 28 Claude handoff](handoff-2026-09-28-claude-code.md) retains its
then-open harness decisions and recommendations. Later
[native protocols and results](../evals/claude-code/README.md) record the executed
conditions; the handoff's pre-execution status is historical. Cross-machine
installed-path portability remains unestablished.
