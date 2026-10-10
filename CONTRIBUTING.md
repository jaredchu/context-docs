# Contributing

Start with a concrete documentation-maintenance problem and a small proposed
change. Issues and pull requests are welcome. Include a synthetic reproduction;
do not upload private project documents or credentials.

Keep the skill short and its references portable. Preserve existing project
layouts, decision authority and evidence. Favor an instruction change over a new
script unless deterministic tooling provides a clear, repeatable benefit.

Design for people who do not yet know how to save and maintain project context.
Reduce the setup, organization, prompting and correction work users must do while
preserving useful knowledge, accuracy and consistency. Model speed and file size
alone do not measure that benefit; outperforming an expert workflow is not required.
For claims about reader benefit, use the [quality-first protocol](evals/quality-protocol.md)
with matched weak-documentation baselines. Maintenance pass rates alone do not
establish better downstream answers.

For a skill change:

1. Identify the affected [evaluation scenario](evals/README.md), or add one that
   demonstrates the missing behavior without prescribing exact output wording.
2. Use the [public Harbor suite](evals/suite/README.md) for repeatable comparisons,
   or run the scenario in a disposable directory. Validate reference and failing
   controls before model runs. Record the agent/model, inputs, outcome,
   verification limits and any lost information. Report semantic review separately
   from mechanical checks, and retain failed trials.
3. Run `python3 evals/checks/static_checks.py` for packaging, links, declared
   versions and agreement between evidence-page tables and published results. GitHub
   Actions runs it with the container-free study self-tests on every push. Also
   check that the skill works when copied without the rest of this repository, and
   use your client's skill validator if available.
4. Describe what changed, why, and what was actually tested in the pull request.

An authored example or static metadata check is not an independent behavioral
evaluation. Keep those claims separate, including in the
[changelog](CHANGELOG.md): record the version a change lands in and what was
actually executed for it. A version whose only evidence is static checks says so. Contributions are provided under the
repository's MIT license.

## Contribute validation evidence

You can [propose a public case or review a handoff](evals/external-validation/README.md)
without running models or installing tools. Case selection and artifact review
are separate contributions; disclose prior involvement and model assistance.
Original study results remain intact when supplemental reviews are added.
Maintainer and regular-user feedback is welcome too: record the task, version,
expected behavior and observed result. Label maintainer cases as field validation,
with public source evidence or a clearly labeled synthetic reproduction of private
work, rather than independent review.

## Commit attribution

Keep the contributor's normal Git author identity. For work assisted by Codex,
include this trailer exactly once, separated from the commit body by a blank line:

```text
Co-authored-by: Codex <noreply@openai.com>
```

This is the format used in [OpenAI's Codex attribution implementation](https://github.com/openai/codex/blob/9946da9af1829410271f6b76f9159961f7281e0a/codex-rs/ext/git-attribution/src/world_state.rs),
verified on September 29, 2026. Preserve existing co-author trailers and credit
only actual assistance. Apply this to new commits; do not rewrite published history
solely for attribution. The README acknowledgment describes project roles and does
not promise a particular position in GitHub's Contributors graph.
