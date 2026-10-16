# Visual-path correction: checks and artifact review

October 16, 2026. **Unreleased core 0.2.1; adoption 0.1.10 and standard 0.1.1
unchanged.** The owner requested a clear visual path, dependencies and blockers
in Markdown. Sol made the correction; Claude Opus 5.5 reviewed the artifacts.
No installed upgrade, publication, deployment or new native behavior trial ran.

## What changes

The [packaged guide](../../skills/context-docs/references/progress.md) now asks for
an explicit visual path, preserves unknowns and parallel conditions, and puts
prerequisites beside blocked work. Source keys in text diagrams map to real
Markdown links outside the fence. The [example](../../examples/progress.md) shows
that shape. [Visual acceptance criteria](README.md#visual-acceptance-criteria-core-021-candidate)
reject a flat status table alone and check the relationships and source mapping.
Ordinary maintenance keeps an existing format; an explicit visualization request
may reshape the same section/file while preserving owner edits and record locations.

## Bounded counterpart review

Both read-only CLI reviews used existing authenticated access, requested and
reported `claude-opus-5-5`, medium effort, with only the Read tool, no MCP, hooks,
auto memory or session persistence. No API-key environment fallback. The initial
review completed in 48.48 seconds under a 120-second cap; its one focused follow-up
completed in 26.65 seconds under a 90-second cap. No further review or subject run.
Raw packets, responses, commands and receipts are retained in a durable private folder.

| Finding | Verified disposition |
| --- | --- |
| B1: refresh scenario expected an undefined two-check goal, blocker and next action | Confirmed. Scenario 2 now supplies the initial facts and a later dated sample-provided/passing result. The follow-up accepts the fix. |
| B2: unclear whether maintenance must reformat an existing view | Confirmed. Guide and criteria distinguish ordinary maintenance, explicit visualization and maintenance of an existing visual view. The follow-up accepts the fix. |
| S1: released version should head README status | Keep the checkout version so README, changelog and VERSION agree under existing checks. The latest published bundle is explicitly v0.2.0 immediately below it; the follow-up accepts this distinction. |
| S2/S3/S4: unevaluated behavior, hard-coded site version and released/candidate ambiguity | Clarified the user guide, made website copy version-neutral and scoped the criteria to the unreleased candidate. |
| Optional guide source-map illustration | The guide explains replacing illustrative keys with real links; the authored example demonstrates the concrete map. No second fixture was added inside the guide. |
| Follow-up cosmetic README concern | The actual status line has balanced bold markers; the review packet excerpt had removed its opening marker. No source defect. |
| Follow-up minor scenario ambiguity | Clarified after follow-up that the visualization variants start from the initial blocked fixture and that the maintenance case updates a next-action bullet. No third review. |

The follow-up found no remaining material blocker, subject to final checks.
This is artifact review by the other model, not an independent behavioral study
or evidence that a native client produces a useful visual from the new guidance.

## Checks and limits

Final checks pass after the corrections: 18 packaging/static regression tests,
14 site tests, both skill validators, 20 isolated sibling-package links, repository
static checks and the nine-file site build. The exact
canonical visual prompt and unreleased status are present on both built pages;
the existing site test checks prompt equality. The whitespace check also passes.
These are mechanical checks, separate from native behavior and visual usefulness.

Candidate file identities (the scenario file includes the noted post-review
clarification):

```json
{
  "skills/context-docs/SKILL.md": "4773a1c9849438fe320fc5d80059999ab9a91b9ce8b1e8da2d029ddf83b1d67c",
  "skills/context-docs/references/progress.md": "f86942ce1eb3581c75d4aee6fead87613f9e1262dabbfe773eb7de2b311fe59c",
  "skills/context-docs/VERSION": "71015c979ccb0fc8a0be7ca0ae83046ab045cdc2c8faa09fb2f0f7e440f9b4a6",
  "examples/progress.md": "85ae7e83da3d11e0f01d6375f6d2eaa587d6f8cb7e0a4d1a6514e5fc7c4e913a",
  "evals/progress/README.md": "e9fd427f0e5609d8001021ef69aeb9620bf9f045d42a62b5b66e4b5a83704f37"
}
```

The revised visual criteria are authored and unexecuted. Earlier
[copied-development smoke](smoke-2026-10-16/README.md),
[installed v0.2.0 smoke](../installed-skills/2026-10-16-progress/README.md) and the
[initial artifact review](review.md) are unchanged, with their original limits.
Passing their status/source criteria does not establish this visual criterion,
general reliability, privacy, stall-detection accuracy or target-user benefit.

Preservation closeout compares 62,748 pre-change entries across the repository,
installed packages and retained private evidence. Only scoped guidance/docs and
new review/journal evidence differ; existing setups, saved studies, installed
packages and the earlier uncommitted journal event are unchanged. Git metadata
and routine client caches are outside this comparison; no global client-state
equality claim is made.
