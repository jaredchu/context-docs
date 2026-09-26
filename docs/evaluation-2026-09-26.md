# Local documentation benchmark

Date: 2026-09-26. Skill: v0.1.0, commit
`7517367a7fda2d452f914d724064881012a28b50`.

**Outcome:** useful maintenance guidance, with smaller additions in this pilot,
but no demonstrated accuracy advantage or general cost saving. The skill missed
one specific contradiction that the natural-cleanup baseline resolved. Retain
human/agent diff review and explicit conflict checks before applying results.

## Scope and method

This is a small paired maintenance pilot on temporary documentation snapshots
from three owner-authorized local projects. It is not a full-repository,
production, retrieval-quality or statistical benchmark. The original projects
were not edited. Private documents, prompts containing them, and raw model
outputs remain outside this repository.

- Project A: portfolio governance, 54 original Markdown documents.
- Project B: a web SaaS product, 16 original Markdown documents.
- Project C: an educational web product, 21 original Markdown documents.

Snapshots included the relevant Markdown, available root package metadata and
license files, including current uncommitted document content. They excluded
source code, credentials, build artifacts, original Git history and live access.
The controlled tasks added a synthetic pilot document and configuration to each
copy. A second pair used Project B's original documentation without injections.

Each pair received identical bytes and the same maintenance request. Both arms
could read the project's existing instructions and conventions. The treatment
additionally received the unchanged skill and its references. This is a comparison
against a competent ordinary prompt, not an unstructured or deliberately weak
baseline.

Fresh ephemeral Codex CLI processes used `gpt-6-astra`, low reasoning effort,
CLI `0.155.0-alpha.16.4`, and the existing ChatGPT subscription login. User config,
automatic host skill discovery, hooks, plugins, apps, browsing, memory and
delegation were disabled. Writes used the workspace-write sandbox, with sandbox
network access disabled; prompts limited inspection to the temporary workspace.
Read scope was checked in command traces, not enforced by a fully isolated
filesystem. Project instructions remained available as files for
both arms to read. Explicit skill loading was tested, not automatic selection.

There was one run per arm/task, without tuning the skill between runs. Order was
baseline then skill for A and C, skill then baseline for B; the natural cleanup
used baseline then skill. Server caching was not controlled. The startup probe,
snapshot preparation and author review are outside the run metrics.

## Controlled maintenance results

Each copy contained a known stale configuration claim, repeated diary notes,
an approved choice with rationale and authority, an unapproved proposal, an
uncommitted blocker/next action and a hand-edited YAML example. Configuration
established the new value; no execution/deployment evidence was supplied.

Ten criteria per project covered the corrected fact/source, verification limits,
approval/rationale, proposal status, blocker/next action, exact YAML preservation,
decision-link reachability, preselected real-project constraints, edit scope and
consolidation. Diff/semantic review was by the authoring assistant, not an
independent blinded judge. Mechanical checks supplemented that review.

**Both arms met all 30 controlled criteria.** No measured accuracy advantage was
established. No new local-link diagnostics appeared, and the supplied evidence
and skill files were unchanged. Missing implementation files already caused
some unresolved links in the limited snapshots; these were not new regressions.

| Project | Baseline time | Skill time | Baseline input tokens | Skill input tokens | Baseline total-doc word change | Skill total-doc word change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 60.7 s | 57.1 s | 108,895 | 100,602 | +103 | +42 |
| B | 47.4 s | 39.7 s | 56,190 | 61,054 | +62 | +27 |
| C | 51.2 s | 40.6 s | 70,722 | 61,802 | +45 | +13 |
| Total | 159.3 s | 137.4 s | 235,807 | 223,458 | +210 | +82 |

| Additional metric | Baseline | Skill |
| --- | ---: | ---: |
| Uncached input tokens | 60,447 | 64,098 |
| Output tokens | 3,578 | 2,974 |
| Shell command batches | 15 | 13 |
| Combined entry-point word change | +31 | -29 |

The skill runs took 13.7% less wall time and processed 5.2% fewer total input
tokens in this sample, but used 6.0% more uncached input. The experiments do not
establish monetary savings. Token counters are CLI-reported cumulative usage,
including repeated context/tool output; they are not the size of the final docs.
Wall time includes startup and service latency, not just model computation.

The skill introduced 61.0% fewer additional documentation words, but both arms
grew the total corpus while improving evidence and handoffs. This is evidence of
smaller additions in this task, not proof that the skill automatically shrinks
documentation. Two controlled runs had a nonfatal shell failure from trying to
read a nonexistent `AGENTS.md` (one in each arm); both completed successfully.

## Original-document cleanup

The second pair used Project B's original documents without synthetic additions.
The task was to make existing context easier to use, consolidate repetition,
correct only evidence-supported stale guidance, and preserve unique details and
unresolved work. This is a broader task than the controlled update.

| Metric | Before | Baseline | Skill |
| --- | ---: | ---: | ---: |
| Entry-point words | 1,251 | 973 | 1,011 |
| Entry-point lines | 220 | 128 | 127 |
| Whole Markdown corpus words | 12,526 | 12,667 | 12,598 |
| Markdown files changed | — | 10 | 7 |
| Wall time | — | 147.3 s | 107.8 s |
| Total input tokens | — | 251,715 | 239,807 |
| Uncached input tokens | — | 45,379 | 44,479 |
| Output tokens | — | 3,896 | 2,791 |

Both moved repeated commands and recorded measurements into existing focused
documents and replaced repetition with links. They retained checked operational
identifiers, command lines, launch boundaries, unresolved actions and the
rationale for a disabled noisy alert. Neither introduced new link diagnostics
or claimed live production verification. The skill files and non-Markdown inputs
remained unchanged. Full diffs were reviewed, with identifier and command-line
checks as supplementary diagnostics, not proof of complete semantic equivalence.

The skill's entry point shrank by 19.2% in words; the baseline shrank it by 22.2%.
The skill used fewer edits and took 26.8% less time, but both increased total
documentation because they added provenance and verification limits. Line count
alone would misleadingly suggest a larger improvement than word count.

One meaningful difference favored the baseline: it explicitly reconciled an
older design section proposing Git-connected deployments/CI with a later manual
release workflow. The skill added a general warning that design documentation
mixes intent and implementation, but left those conflicting deployment bullets
in place without specifically marking or resolving them. Fewer edits therefore
did not mean more complete maintenance. This is a post-run qualitative finding,
not an additional pre-registered accuracy score.

Both outputs include statements about the disposable snapshot's missing code and
access. These are appropriate experimental handoffs, but should not be copied
blindly into a full production repository. The tested edits have not been applied
to the original projects.

Final checks found all 94 sampled original files byte-for-byte unchanged and
the original three Git status snapshots unchanged. All eight model runs completed;
none was silently dropped or replaced with a retry. The skill was not modified
in response to this sample.

## Limits and next evaluation

The controlled tasks are easy, explicit and share the same injected scenario.
The original projects already have substantial context conventions. Results do
not establish benefits for weakly documented projects, every model, repeated
maintenance over time or downstream answer accuracy. Counts and diff review do
not prove preservation of every possible interpretation of a document.

This pilot exercises maintenance. Audit-only behavior, initialization and
automatic activation remain separate tests. A useful next study would repeat
held-out tasks, include genuinely conflicting evidence and meaningful concurrent
edits, and evaluate whether a new reader can answer project questions after
maintenance. Any changes based on these results should be tested on new inputs,
not silently substituted into this baseline.

## Local evidence

The git-ignored `.local/benchmark-location.json` records the temporary artifact
root for the owner. It contains paired before/after trees, prompts, model events,
diffs, source hashes/statuses, the fixed rubrics, usage measurements and local
runner/measurement scripts. Those artifacts include private project documents
and must not be added to this public repository. Temporary directories may be
removed by the operating system; retain them privately if longer-term replay is
needed. The aggregate report alone is not a publicly reproducible dataset.
