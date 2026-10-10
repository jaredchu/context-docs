# Small public-history maintenance plan

Status: **preparation on October 10, 2026; not frozen, accepted or executed.**
The next proposed step is four maintenance sessions using two public projects.
Selecting sources and preparing this plan do not authorize model execution or
publication. No completed study, skill or score changes with this proposal.

## Question and boundary

Can the released core skill create a supported, useful contributor upgrade handoff
from actual public changes, in two documentation layouts? Compare its
outputs with competent ordinary maintenance on the same evidence. Assess stored
knowledge, factual accuracy, consistency, audience and permitted scope.

This is a bounded maintenance comparison informed by the artifact criteria in
the [quality protocol](quality-protocol.md), not its full reader-benefit study.
The [discrimination protocol](discrimination-protocol.md) remains a separate,
unapproved proposal. Its explanations for earlier ties are hypotheses; neither a
tie nor a difference in four sessions establishes a general causal effect.

## Cases to freeze

Use new public histories rather than copies of existing evaluation fixtures.
Keep upstream facts separate from the evaluator-authored maintenance request.

| Case | Public project and layout | Source event and cutoff | Status |
| --- | --- | --- | --- |
| A | [encode/httpx](https://github.com/encode/httpx), Python package with `docs/`, BSD-3-Clause | [0.28.0](https://github.com/encode/httpx/tree/80960fa31918d7663c3f4c3ad61661cf0e80628f) → [0.28.1](https://github.com/encode/httpx/tree/26d48e0634e6ee9cdc0533996db289ce4b430177); [SSL client-certificate fix](https://github.com/encode/httpx/commit/89599a9541af14bcf906fc4ed58ccbdf403802ba) | Proposed; source hashes recorded, freeze pending |
| B | [BurntSushi/ripgrep](https://github.com/BurntSushi/ripgrep), Rust workspace with root Markdown docs, MIT OR Unlicense | [14.1.0](https://github.com/BurntSushi/ripgrep/tree/e50df40a1967708b9781486b1c017e48040bceb0) → [14.1.1](https://github.com/BurntSushi/ripgrep/tree/4649aa9700619f94cf9c66876e9549d83420e16c); [inner-literal fix](https://github.com/BurntSushi/ripgrep/commit/9d738ad0c009e6632d75fa3d36051e5ae7f7cce6) | Proposed; source hashes recorded, freeze pending |

Candidate distinctions: HTTPX certificate handling versus retained deprecations;
ripgrep's `grep-regex` optimization versus the upstream `regex` dependency and a
separate feature removal. These are source-backed case leads, not scored results.
Use pinned Git files and objects for historical claims. A release page fetched
today may have been edited since release and is not a historical snapshot.

[Source inventory](public-history-sources.json) records pinned locations and hashes;
the [evaluator ledger](public-history-ledger.md) gives source-backed required facts.
The task is explicitly evaluator-authored: add an upgrade handoff, not repair an
asserted upstream defect. Do not invent decisions or corrupt upstream documents.
These cases exercise different layouts, languages and change mechanisms. Public source authors
are independent of this project; case selection, task boundaries and scoring are
authored here and are not independent benchmark design.

Use the full after-tag tree as each disposable editable copy. Supply identical
before-revision files and fix-commit diffs as read-only evidence outside that tree,
with pinned URLs and hashes. The full after tree is readable; do not expose later
resolutions or current web search. No discussion excerpts are supplied. This is
handoff creation from existing history, not repair from evidence newer than the docs.
The end-revision changelogs already describe fixes, so a ceiling remains plausible.
This tests artifact feasibility and retention, not incremental causal benefit.

## Four sessions

Run one ordinary-maintenance and one explicit-skill session per project: **four
sessions, 600 seconds maximum each, no retries or readers**. Retain an untouched
starting copy for artifact comparison; it requires no agent session.

Both arms receive: "Prepare a contributor upgrade handoff for [case scope] from
the supplied evidence, and link it from the README." Case scope is HTTPX SSL
configuration guidance and its consistency with source, 0.28.0 → 0.28.1;
or ripgrep matching behavior and build-feature compatibility,
14.1.0 → 14.1.1. Append identical
editable paths, audience, source cutoff, tool limits and task boundaries. The
skill arm additionally invokes the frozen released **context-docs v0.1.6**.
Do not install or invoke the adoption skill. Freeze complete prompts verbatim.

Proposed executor: **Claude Opus 5.5, high reasoning**, using identical tools in
both arms. Local Claude CLI is currently 2.1.295; freeze exact client/model IDs,
reasoning configuration and tool/resource limits before execution. Give each session a
fresh isolated context. Verify that the ordinary arm cannot read the skill and
that neither arm inherits this repository's maintenance instructions, evidence
ledger, reviewer notes or other outputs. Preserve applicable upstream instructions
identically and audit any method guidance they already contain. Verify explicit
skill exposure from the recorded trace rather than assuming invocation succeeded.
Order: HTTPX ordinary, HTTPX skill, ripgrep skill, ripgrep ordinary.

Outputs: HTTPX `docs/upgrade-handoff.md`; ripgrep root `UPGRADE-HANDOFF.md`, each
with an appended README navigation link. Preserve
the entire existing README as a byte-identical prefix and all other upstream files.
These shared scope controls do not impose a handoff structure on either arm.
Project inspection is limited to reading the frozen source and history. Do not
execute upstream code, install dependencies, access live environments, contact
upstream maintainers or publish changes. Allow writes only to the frozen document
allowlist in each disposable copy. Keep study artifacts outside both subjects.
Do not enable logging, migrate layout or create an adoption marker as part of the
task. Preserve both arms' complete outputs and actual writes, including failures.
The ledger records the released-skill compatibility audit and override attribution.

## Evidence and review

The proposed evaluator-only ledger remains outside subject access and records
atomic required facts, source locations, source authority and date, supported
status, existing constraints/rationale to preserve, and justified unknowns.
Record expected destinations or acceptable canonical links without mandating
wording or a new directory structure. Include the source basis for deciding that
a fact is useful to contributors. A merged change proves repository state at its
revision; it does not independently prove runtime behavior or private approval.

Assess each output against these frozen criteria:

| Measure | Required reporting |
| --- | --- |
| Retention | Required facts and unique constraints/rationale retained accurately in maintained docs or navigable canonical links; raw-source survival alone earns no documentation credit |
| Accuracy and authority | Supported material claims, missing required items, incorrect claims, invented approvals and unqualified unknowns; inspect new claims beyond the target ledger |
| Consistency | Current instructions reconciled with supplied evidence; superseded history qualified; unresolved source conflicts accurately preserved |
| Audience and destination | Useful contributor information in the mandated handoff, reachable from README and linked to canonical sources; evaluator/session bookkeeping excluded; useful historical evidence retained or linked |
| Scope and execution | Actual writes within allowlist, source integrity, successful output capture and verified skill exposure; disclose any violation even if corrected |

Keep critical failures visible individually: lost unique constraints or decisions,
fabricated approval or runtime verification, unreported operative contradictions,
destruction of supplied work, and out-of-scope writes. Do not average them into a
single passing score. Word count, editing time and tokens are secondary diagnostics.

The ledger includes a reference outline and manual negative/uncertainty controls;
counterpart review must check them before freeze. These are rubric checks, not
additional agent sessions or a new test framework.

GPT 6 Astra High authored the plan/ledger and will score outputs; Claude Opus 5.5
reviews preparation and outputs and is also the proposed executor model. These are
author and same-model overlaps, not independent review. Record actual roles and
mask arm labels where feasible without claiming style is unrecognizable. Preserve
the [initial Claude review](public-history-review.json), disagreements and resolutions.

## Acceptance, freeze and reporting

Before asking to execute, complete both case rows and provide the exact sources,
task boundaries, four-session budget, model configuration and ledger/rubric for
review. Execution requires acceptance of that concrete scope. Snapshot assembly,
input isolation and write-boundary enforcement remain unimplemented. Freeze hashes of
the full skill package, project/source snapshots, prompts, ledger, criteria and
controls in a new manifest before starting any subject session.
Enumerate the read-only evidence exactly: HTTPX's before-tag `httpx/_config.py`
(HB), ripgrep's before-tag `crates/regex/src/literal.rs` (RB), and both fix diffs.
Any additional evidence must be declared and supplied identically before freeze.

Reuse existing capture tooling where applicable. Retain failed runs, timeouts,
traces, before/after snapshots and reviewer evidence. A repaired configuration or
new attempt needs a separately identified freeze and scope; never replace an
original result. Run repository static checks and report them separately from
actual agent execution and semantic review. Leave all earlier frozen studies
unchanged. Publication remains a separate authorized action.

Report results per case and arm, with evidence for every failure and material
disagreement. Four sessions across two selected public histories cannot establish
general reliability, longitudinal durability, natural invocation or reader benefit.
If reader benefit becomes the question, propose a separate extension under the
quality protocol with unmaintained/ordinary/skill arms, fresh isolated readers,
frozen questions, equal source access and declared budgets. Do not quietly add it
to these four sessions or infer its outcomes from document quality.
