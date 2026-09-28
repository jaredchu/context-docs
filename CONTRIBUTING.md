# Contributing

Start with a concrete documentation-maintenance problem and a small proposed
change. Issues and pull requests are welcome. Include a synthetic reproduction;
do not upload private project documents or credentials.

Keep the skill short and its references portable. Preserve existing project
layouts, decision authority and evidence. Favor an instruction change over a new
script unless deterministic tooling provides a clear, repeatable benefit.

Evaluate knowledge retention, accuracy and consistency before speed or file size.
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
   versions and agreement between README tables and published results. GitHub
   Actions runs it with the container-free study self-tests on every push. Also
   check that the skill works when copied without the rest of this repository, and
   use your client's skill validator if available.
4. Describe what changed, why, and what was actually tested in the pull request.

An authored example or static metadata check is not an independent behavioral
evaluation. Keep those claims separate, including in the
[changelog](CHANGELOG.md): record the version a change lands in and what was
actually executed for it. A version whose only evidence is static checks says so. Contributions are provided under the
repository's MIT license.
