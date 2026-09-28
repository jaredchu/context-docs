# Adoption v0.1.3 routing follow-up — September 28, 2026

**Recommendation: ready to merge within the documented experimental scope.**
Both routing trajectories passed all four model sessions, eight semantic rubric
items, and tool-scope review. Both next-day repeats preserved actual project
bytes and the original adoption date. This resolves the
[initial review's validation hold](../2026-09-28-adoption-v013/README.md), without
rescoring its 8/9 result or changing either installable skill.

| Case | Sessions accepted | Outcome |
| --- | ---: | --- |
| CLAUDE.md instructions, then next-day repeat | 2/2 | One rule/marker; original instructions and blocker retained; repeat unchanged |
| Split CLAUDE.md / AGENTS.md, then next-day repeat | 2/2 | One rule/marker in CLAUDE.md and reference from AGENTS.md; protected documents and repeat unchanged |
| **Total** | **4/4** | **2/2 complete trajectories accepted** |

## What was fixed

The initial split-file task silently required `knowledge/state.md` to remain
byte-identical, while its grader rejected a real installed-skill link outside
the project snapshot. The same path in a code span escaped that link check.
These were fixture/verification problems; the initial routing rubrics passed.

The follow-up makes all immutable-file constraints explicit in every generated
request. The verifier accepts only explicitly declared installed-file targets
whose contents still match frozen SHA-256 hashes. References under those supplied
installation roots are checked in Markdown links, code spans and prose. Missing,
changed or undeclared targets fail, as do broken anchors, broken project links
and edits to protected project files. External files never enter the project
snapshot. Existing cases without these optional fields keep project-only checks.

Both routing cases use explicit simulated dates, and the split-file case now
includes a next-day repeat. These changes and all criteria were frozen before
the model sessions. Core v0.1.1 and adoption v0.1.3 are byte-for-byte unchanged.
The original failed observations, review and recommendation remain intact as
dated evidence; this follow-up supersedes that recommendation, not its scores.

## Verification and evidence

Nine new verifier regression tests passed, including controls that ensure valid
external links cannot conceal immutable edits, missing/changed installed files,
undeclared targets or broken local links. The existing 46 core and 66 quality
self-test assertions, 30 adoption-builder controls, 12 static-checker regression
tests, package/link/version checks and published-report regeneration also passed.
These are static checks, separate from the four model sessions above.

Before model execution, four Harbor reference steps passed. Both no-op first
passes failed the required-change check; both permitted no-op repeats passed.
There were no execution errors or automatic retries. Recorded inputs contained
four expected task messages and four environment messages, with no unexpected
user messages or injected host instructions. Frozen package hashes remained
unchanged; every declared installed file matched its hash in every model pass.

- [Frozen protocol and hashes](protocol.json), [manifest](manifest.json) and
  [exact prompts and specifications](inputs.json).
- [All model observations/tool calls](trials.json), [final responses](final-answers.json),
  [rubric packets](review-packets.json) and [explicit author judgments](reviews.json).
- [Summary and repeat comparisons](summary.json), [control outcomes](controls.json),
  [input-isolation audit](isolation.json) and [package verification](package-verification.json).
- Frozen [builder](instructions.txt), [verifier](verify.txt) and
  [verifier regression tests](test_verify.txt).

## Reproduce and interpret

Use this reporting revision and fresh paths. The builder now supplies explicit
dates, visible file constraints and installed-file hashes without manual edits:

```sh
python3 evals/adoption/instructions.py .local/routing-followup/suite
python3 evals/suite/run.py .local/routing-followup/suite .local/routing-followup/jobs --mode oracle --prefix followup
python3 evals/suite/run.py .local/routing-followup/suite .local/routing-followup/jobs --mode nop --prefix followup
python3 evals/suite/run.py .local/routing-followup/suite .local/routing-followup/jobs --mode model --prefix followup
```

Execution used Harbor 0.23.0, Codex CLI 0.158.0-alpha.2, gpt-6-astra with low
reasoning effort, one attempt per trajectory, two concurrent trials and a
240-second per-session limit. See the [runner documentation](../../suite/README.md)
for authentication and isolation. Raw jobs and credentials remain local.

These author-created cases and reviews are not blinded or independent. The
follow-up demonstrates routing and preservation with explicit edit constraints
and valid installed references; it does not establish that every unqualified
adoption request will avoid incidental edits. Absolute skill paths are valid
for this installation, not proven portable across machines. Native Claude Code
loading, automatic selection, broad reliability and accuracy advantages remain
untested. The earlier six marker/audit sessions were not rerun here; their
separate observations remain in the initial review. Do not combine the changed
conditions into a claimed clean 13-session run.
