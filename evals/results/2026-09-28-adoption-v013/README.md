# Adoption v0.1.3 merge review — September 28, 2026

**Recommendation: hold merge pending a targeted follow-up.** Five of six
trajectories (eight of nine fresh model sessions) met the frozen acceptance
criteria. The split-instruction case failed two mechanical checks despite
meeting its three routing rubrics. This is neither a full pass nor clean
evidence of a skill regression: the failure mixes an unnecessary document edit
with restrictions the fixture did not state explicitly to the agent.

| Case | Sessions accepted | Reviewed outcome |
| --- | ---: | --- |
| CLAUDE.md instructions, then repeat | 2/2 | One rule and marker; context/blocker preserved; repeat unchanged |
| Split CLAUDE.md / AGENTS.md | 0/1 | Routing correct; immutable context heading changed; external skill link rejected |
| Code-only project, then repeat | 2/2 | Useful source-supported README context; original date and bytes retained |
| Existing layout and blocker, then repeat | 2/2 | Original instructions, decisions and uncommitted blocker preserved |
| Already adopted without marker | 1/1 | Only missing marker added; date remains unknown |
| Audit-only unmarked project | 1/1 | Adoption recognized; all project bytes unchanged |
| **Total** | **8/9** | **5/6 complete trajectories accepted** |

All 21 explicit semantic rubric items passed author review. Overall acceptance
also requires mechanical checks and scope compliance, so that semantic score
does not override the failed case. All three repeat inputs matched the previous
outputs, and their outputs were byte-identical to those inputs. No execution
errors, automatic retries, unexpected user-message injection, or tool-scope
violations were observed. The audit wrote only its requested output report.

## Split-file failure and interpretation

The output put one maintenance rule and marker in `CLAUDE.md`, retained both
instruction files' original text, and added a reference from `AGENTS.md`. Its
final response correctly explained that placement.

Two checks failed:

1. `knowledge/state.md` changed from `# Current context` to
   `# Current context: Offline pilot`. No decision content was lost, but the
   fixture marks this file immutable. The request did not explicitly require
   that file to remain byte-identical. The title edit was unnecessary; it is
   not evidence of factual corruption or a routing failure.
2. The rule linked to `/opt/context-docs/context-docs/SKILL.md`, an installed
   file the agent had read. The project-only verifier treated it as missing
   because it is outside its snapshot. The link exists in this test environment;
   that check does not prove a broken runtime link. The absolute installation
   path does introduce a portability concern. Other passing cases contain the
   same path in code spans, which the Markdown-link grader does not inspect.

Resolve the intended edit constraints and installed-skill reference policy in
the fixture before a separately frozen follow-up. Evaluate equivalent link and
code-span references consistently. Retain this run's failure and do not claim a
full v0.1.3 regression pass. Do not add a universal skill rule merely to fit this
single example. The reviewer recommends holding the combined branch while that
validation gap is unresolved; this is a review recommendation, not an owner
decision to reject the contribution.

## Frozen setup and controls

The skills are unchanged from commit `6597389`: adoption v0.1.3 and core v0.1.1.
Harbor 0.23.0 used Codex CLI 0.158.0-alpha.2, gpt-6-astra, low reasoning effort,
one attempt per trajectory, at most two concurrent trials, and 240 seconds per
session. Only explicit skill use was tested. Container project-instruction
injection and host skill discovery were disabled.

Before any model run, the inherited `AGENTS.md` destination was removed from
the new routing requests, and the CLAUDE-only client condition was restated in
the fresh repeat session. This repairs conflicting test instructions, not the
skill. The initial package received only oracle/no-op controls; its protocol and
manifest are retained. Simulated dates were also made explicit before model
execution, following the earlier marker study's date-ambiguity finding. No
fixture, criterion or skill was changed after the scored sessions began.

The initial routing builder passed ten static controls, the marker builder twelve,
and the corrected routing builder ten. Sixteen separate Harbor control
trajectories covered 24 steps: twelve reference steps passed; all eight required
first-pass no-ops failed, while four permitted repeat no-ops passed. These are
controls, not model evaluations. Package hashes and recorded session inputs were
checked separately. Raw jobs, credentials and service metadata remain local.

## Reproduce

Use this reporting revision, verify the package hashes against the manifests,
and choose a fresh output directory. Build both suites:

```sh
python3 evals/adoption/instructions.py .local/v013-reproduction/instructions-suite-v2
python3 evals/adoption/marker.py .local/v013-reproduction/marker-suite
```

Before running controls or models, replace each date phrase in generated
`instruction.md` files using `pre_execution_date_clarification` in
[protocol.json](protocol.json). Exact final prompts and verifier specifications
are preserved in [inputs.json](inputs.json); compare them before execution.
Run `evals/suite/run.py` with each suite and `--mode oracle`, then `--mode nop`,
then `--mode model`, using prefixes `routing-v2` and `marker` respectively.
Keep all new outcomes separate from these results and review each rubric and
tool trace. The shared [runner documentation](../../suite/README.md) covers
authentication, container setup and export boundaries.

## Evidence and limits

- [Frozen model protocol and hashes](protocol.json), [routing manifest](routing-manifest.json),
  [marker manifest](marker-manifest.json), [frozen routing builder](routing-builder.txt)
  and [final input prompts/specifications](inputs.json).
- [Initial control-only protocol](initial-control-protocol.json) and
  [initial routing manifest](initial-routing-manifest.json), retained before the prompt repair.
- [All model observations and tool calls](trials.json), [final responses](final-answers.json),
  [rubric packets](review-packets.json) and [explicit author judgments](reviews.json).
- [Derived summary and repeat comparisons](summary.json), [control outcomes](controls.json),
  [count-only input-isolation audit](isolation.json) and [package verification](package-verification.json).

These synthetic cases and reviews are author-created, not blinded or independent.
There is no ordinary-maintenance comparison, fresh-reader outcome, automatic
selection test or native Claude Code model run. No cross-client reliability,
accuracy advantage or broad skill regression is established. Frozen failure
counts are retained despite the identified fixture limitations.
