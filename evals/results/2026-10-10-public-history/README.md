# Public-history handoff comparison — October 10, 2026

Four native Claude Opus 5.5 sessions completed the frozen HTTPX/ripgrep comparison.
All four passed execution gates with no denied actions. Required-fact coverage
and additional-claim accuracy are separate outcomes; execution success is not a
factual-accuracy pass. Reviewer results are recorded below.

## Conditions and evidence

The [plan](../../public-history-plan.md), [source ledger](../../public-history-ledger.md)
and [source inventory](../../public-history-sources.json) define the authored tasks.
Inputs were frozen before subjects ran and committed in `87e80d7`:

- [Freeze manifest](freeze.json), [protocol digest](protocol.sha256) and
  [preflight review/resolutions](preflight-review.json).
- [Results](results.json): all handoffs, final responses, README additions,
  per-gate outcomes, source/output hashes and sanitized tool-trace metadata.
- [Astra semantic review](astra-review.json) and
  [Claude semantic review](claude-review.json), with original judgments retained.

The raw runtime protocol SHA-256 is
`407a2c43b2ad4d18f4d8dca48b7fdd721dc560bb3978edd85dcc26dda07fa128`.
The frozen public manifest omits runtime host metadata; it is not byte-identical
to that private protocol. Full pinned after-trees were supplied: HTTPX had 125
files (5,201,175 bytes); ripgrep had 213 entries (3,025,954 bytes), including its
internal `HomebrewFormula` symlink. Git blob identities, bytes and file modes
were checked. Before-helper files and actual fix diffs were read-only evidence;
these were not full before-tag trees. Upstream source bodies are not vendored here.

The subject client was Claude Code **2.1.295**, responding model
**`claude-opus-5-5`**, with High effort requested but not independently observed.
Usage metadata also named `claude-haiku-5-5`; this does not establish its role.
Every observed subject assistant response identified Opus 5.5.
The treatment was released core **0.1.6**, package commit
`b10a3058e43f9af278cbb7a6b2b70d41df16ea7d`, delivered by an explicit complete
`Read` of the frozen skill body. It was **not native Skill-tool invocation or
implicit discovery**. Both native skill catalogs were disabled and observed empty.
Ordinary arms had no skill package. Both arms otherwise received matched inputs.

Only Read, Write, Edit, Glob and Grep were available. Hooks confined file tools;
this was not an operating-system sandbox. Subjects could create one handoff and
append its README link while preserving all original README bytes and every other
upstream entry. They could not run commands, tests, builds, dependency installs,
network tools or delegated agents. Preflight and loading observations constrain
instruction contamination but do not reveal the complete hidden system prompt.

## Execution

| Session, in frozen order | Execution gates | Denials | Duration |
| --- | --- | ---: | ---: |
| HTTPX ordinary | All passed | 0 | 148.7 s |
| HTTPX skill | All passed, complete skill read observed | 0 | 129.8 s |
| ripgrep skill | All passed, complete skill read observed | 0 | 129.2 s |
| ripgrep ordinary | All passed | 0 | 142.4 s |

All four planned sessions were attempted once; none timed out or remained unrun.
No retry, revised skill, replacement artifact or rescoring of earlier studies was
used. README links resolve to the required handoffs in the disposable trees.
Time is an execution diagnostic, not a quality ranking.

## Semantic findings

Both reviewers retained all **26/26** required facts: HTTPX H1–H7 and ripgrep
R1–R6 in both methods. Additional claims still contained material errors.
The following table summarizes Astra's original seven material findings;
it is not a combined finding count or a ranking of methods.

| Artifact | Astra required facts | Astra additional material findings |
| --- | ---: | --- |
| HTTPX ordinary | 7/7 | Incorrect top-level API scope; unsupported historical test-pass claim; unsupported dating of documentation mismatches |
| HTTPX skill | 7/7 | Says intended behavior “has not been decided” when the supplied evidence only leaves the decision unknown |
| ripgrep ordinary | 6/6 | Unsupported unchanged-PCRE2-build claim; final response guarantees upgrading can never remove matching lines |
| ripgrep skill | 6/6 | Extends `avx-accel` compatibility to `globset` and `ignore`, which do not declare that feature |

The top-level HTTPX request API has no `cert` argument or forwarding; the fix's
Client/transport path does not support that broader API claim. Current test source
does not prove a historical successful run, and an unchanged old helper does not
date old documentation that was not supplied. Likewise, current ripgrep manifests
do not prove unchanged historical build compatibility. Its four named library
crates declare `simd-accel`, but only `grep` and `grep-searcher` declare `avx-accel`.
These findings concern unsupported source claims, not assertions that subjects
actually ran the prohibited tests.

Astra records additional wording cautions separately: ripgrep skill says the fix
“touches only” `literal.rs` before accurately describing the same commit's
`tests/util.rs` changes; its matching-section context softens, but does not remove,
the local ambiguity. Qualified source expectations about TLS and matching were
not automatically treated as fabricated runtime verification. An HTTPX skill
API overstatement was corrected during the subject's own permitted editing;
its final artifact is scored, with the trace preserved.

Claude agreed on required-fact coverage and the ordinary handoffs' API, historical
test-pass, PCRE2-build and universal-matching problems. It additionally flagged
unsupported HTTPX maintainer intent (“deliberately left undocumented”), disposable
evidence paths in that handoff, and ripgrep's assertion that nothing in the tree
still requests `simd-accel`, contradicted by historical benchmark/changelog commands.
Source inspection and Astra's focused follow-up accepted these with their scope
qualifications. Historical commands do not establish broken current packaging.

Claude did not flag Astra's no-decision, historical-docs or library-feature
findings; all remain recorded. The reviewers differ on the significance of
exclusive fix-file wording, TLS expectations and a CRLF clause. Their original
judgments are preserved. A proposed documentation correction was not accepted as
fabricated authority. Missing adjacent TLS warnings and MkDocs link portability
remain cautions, with no observed rendered-site failure or missing H6 fact.
The [integration resolutions](review-resolution.json) document each decision,
including a correction to Claude's explanation of ordinary CRLF terminators.
No subject artifact was repaired after scoring.

## Validation and limits

Mechanical validation before the freeze passed **22 public-history harness
controls** and **7 reused guard controls**. Repository static checks are reported
separately from the four actual subject sessions and semantic assessments.
Final static checks passed: **1,074 relative links/anchors**, five published result
tables, two installable packages and two declared versions. `git diff --check`
passed. All 30 frozen evaluator input hashes match commit `87e80d7`; exported
artifact hashes match the artifacts Astra reviewed. These checks do not establish
semantic accuracy.

GPT 6 Astra High authored the plan, ledger and harness and reviewed artifacts.
Claude Opus 5.5 reviewed preparation and the harness, ran the subjects, and reviewed
artifacts. The Claude artifact packet shuffled order and masked condition labels,
but prose could reveal treatment; its source corpus contained the subjects'
actual source reads. This is neither independent nor fully blind review. The
integration owner checked material findings against pinned evidence. Original
reviewer judgments and any resolution remain distinct.

Two public projects have different languages and documentation layouts, but case
selection, prompts, criteria and review were authored for this project. There was
one attempt per project/method, an explicit immutable-source scope override, no
fresh reader, and no longitudinal maintenance. The after-tag changelogs already
state the fixes. These results establish neither a causal accuracy advantage,
reader benefit, equivalence nor general reliability. They do not test native
skill selection, unrestricted editing, actual TLS behavior or executed ripgrep
matching/builds.

The released skills remain unchanged. A reasonable next step is to obtain cases
and review independent of the protocol authors before making broader claims;
any follow-up requires a new freeze and must retain these failures.
