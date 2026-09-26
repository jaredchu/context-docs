# Contributing

Start with a concrete documentation-maintenance problem and a small proposed
change. Issues and pull requests are welcome. Include a synthetic reproduction;
do not upload private project documents or credentials.

Keep the skill short and its references portable. Preserve existing project
layouts, decision authority and evidence. Favor an instruction change over a new
script unless deterministic tooling provides a clear, repeatable benefit.

For a skill change:

1. Identify the affected [evaluation scenario](evals/README.md), or add one that
   demonstrates the missing behavior without prescribing exact output wording.
2. Run it in a disposable directory and review the resulting diff. Record the
   agent/model, inputs, outcome, verification limits and any lost information.
3. Check relative links and that the skill works when copied without the rest of
   this repository. Use your client's skill validator if available.
4. Describe what changed, why, and what was actually tested in the pull request.

An authored example or static metadata check is not an independent behavioral
evaluation. Keep those claims separate. Contributions are provided under the
repository's MIT license.
