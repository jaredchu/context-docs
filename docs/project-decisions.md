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
The October 10 responsibility split below supersedes this model assignment.


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

On October 10, 2026, the owner clarified the intended audience: people who do not know
how to save project context and want to maintain it better with the least effort
possible, rather than people who already manage context well. This establishes
accessible setup and low ongoing manual effort as product goals alongside useful,
accurate retained knowledge. For implementation and evaluation, distinguish user
learning, organization, prompting and correction effort from model runtime, token
use or document length. Comparisons with competent ordinary maintenance remain
quality diagnostics, not a requirement to outperform an expert workflow. Existing
frozen criteria, scores and factual failures remain unchanged; no reduction in
intended users' effort has been demonstrated by this clarification alone.

On October 10, 2026, the owner replaced the Astra/Opus assignment with Sol 6.1
coordinating scope, task breakdown and integration, handling small changes alone,
and maintaining context with actual tests and accepted decisions. Opus 5.5 takes
bounded substantial implementation or sustained investigation; the other model
reviews consequential changes against specific risks. The owner emphasized that
Sol should send a compact task, receive a patch plus evidence and inspect important
boundaries without redoing all of Opus's work, to preserve the ChatGPT allowance.
In the fuller policy supplied afterward, the owner required clear editable scope
and a usage/time bound for Opus assignments, one writer per change, findings-only
reviewers and owner-validated resolutions. Review is limited to one initial pass
and one focused follow-up for material fixes; unresolved issues must be reported
rather than triggering a loop. Roles may change when warranted; small changes
remain Sol-only unless project rules require independent review. Use existing
subscription-authenticated access; Astra, API fallback and additional spending
require an explicit owner request. Apply the policy only to this project, preserve
existing safeguards and leave global settings unchanged. Useful completed work
from both subscriptions, better quality and reduced ChatGPT allowance pressure
are objectives to verify, not demonstrated outcomes.
The [project instructions](../AGENTS.md#model-collaboration) own the working rules.
This records the owner's requested responsibilities, not a runtime model change
or evidence that either model participated in a particular task.

On October 10, 2026, the owner requested an explicit local-only context option in
both skills and the user guide, with checks for ignored files, already tracked
context and copying into shared docs. Existing setups and saved studies must be
preserved. Local-only is opt-in Git exclusion; it does not retroactively remove
tracked history or establish confidentiality. Example paths and verification
procedures are implementation choices documented in the
[packaged guide](../skills/context-docs/references/local-only.md).

The owner then identified Git-ignored context as a clearer use case for logging:
retaining history while current context changes without commits. This clarifies
the optional journal's purpose, without enabling it or changing existing setups.
It is a proposed use case, not a newly measured benefit or a claim that selected
event records preserve complete document versions.

The owner then requested implementing auto logging for local-only context inside
Git projects, respecting explicit settings and verifying ignored, untracked
context and journal paths. Update both skills and the guide, add regression tests,
and preserve saved study artifacts. This extends an already opted-in preference;
it does not enable logging for all local-only setups or authorize moving records,
changing global settings or publishing a release.

On October 10, 2026, the owner requested crediting Claude on every commit it
helps implement, validate or review, while preserving the existing Codex
attribution rule. Completed validation and review count even without file edits;
only actual assistance is credited, preserving human authorship, existing
co-author trailers and published history. The
[commit attribution policy](../CONTRIBUTING.md#commit-attribution) owns the exact
trailers; the stable Claude trailer name is a project implementation choice.

## Codex plugin runtime deferral

On October 18, 2026, the owner requested: "Record the Codex plugin runtime deferral
and keep standalone v0.2.5 as the everyday-use path."

Defer Codex plugin activation and runtime validation. Keep using installed
standalone experimental v0.2.5 (core 0.2.5, adoption 0.1.14). Preserve the frozen
candidate, [qualified runtime results](../evals/packaging/plugin-runtime-2026-10-18/README.md)
and [non-model diagnostic](../evals/packaging/codex-route-diagnostic-2026-10-18/README.md).
Claude's focused journey passed; Codex discovery and one command route were
verified, while active plugin registration and execution remain unverified.
The bounded read-only follow-up did not establish a supported disposable
activation route under the preservation constraints. This is a verification
limit, not proof that such a route cannot exist.

This decision authorizes recording the deferral only. Preserve installed skills,
setups, credentials and saved studies. No activation, model reruns, installation,
submission or publication is selected; reopening the work needs a new owner request.

## Cursor compatibility review

On October 23, 2026, the owner requested independent Astra and Fable reviews at
High reasoning, then asked to retain both reviews and a proposed testing plan in
private notes. The owner explicitly instructed not to install or launch Cursor yet.

Keep Cursor **not evaluated** and defer advertised support pending native evidence.
Both reviewers recommend a bounded synthetic probe using the unchanged standalone
skills, with separate claims for CLI and desktop. Cursor documents
[Agent Skills](https://cursor.com/docs/skills) and
[AGENTS.md](https://cursor.com/docs/rules) compatibility; that does not establish
Context Docs discovery, instruction loading or runtime behavior. No skill change,
plugin, release or native Cursor test is selected by this record.

The private review and plan record has evidence ID
`cursor-compatibility-2026-10-23`. It retains both original reviews, model provenance,
dated sources, machine requirements and a proposed seven-session journey. Private
details are not public evaluation evidence. This recording request authorizes no
installation, launch, authentication, spending or test execution.

## Deployment record commits

On October 23, 2026, the owner requested updating the deployment checklist and
both repositories' context so verification-record commits do not require another
deployment. Keep the actual deployed SHA and receipt when later commits only
record evidence or context. The [deployment checklist](../site/README.md#deployment-checklist)
owns the output/behavior change check, verification steps and explicit-rerun
exception. CI can still build documentation-only commits without publishing.
This request authorizes documentation changes, not a deployment or Cursor launch.

## Cursor support postponement

On October 24, 2026, the owner postponed Cursor support and redirected work to
independent Astra/Fable research into context-management skills and tools compared
with Context Docs. Preserve the earlier reviews and proposed testing plan as
historical evidence; no local or remote native test, installation or launch is
selected. Cursor remains not evaluated.

The owner selected **prepare a preview first** when asked about publishing the
research. The public [comparison summary](context-management-comparison.md)
records scope, method and limits; detailed original reports remain privately
retained under evidence ID `context-management-landscape-2026-10-24`. The owner's
follow-ups make the central questions explicit: why Context Docs when native
features already exist, its advantages/disadvantages, intended users, project
types and appropriate workflows. This task grants no website publication.
