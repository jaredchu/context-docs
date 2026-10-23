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

## Release checklist

For future authorized releases, include this skills.sh refresh and verification
after the released skill files are available on GitHub's default branch. Keep
release preparation, website deployment and installed upgrades within their
separately authorized scope. This checklist grants no publication permission.

- [ ] Record the published commit and both skill versions. Fetch both public
  [core](https://www.skills.sh/jaredchu/context-docs/context-docs) and
  [adoption](https://www.skills.sh/jaredchu/context-docs/adopt-context-docs) pages
  before the refresh to establish their current content.
- [ ] Snapshot existing installed skill files and symlinks, including resolved
  targets. Create a temporary project and temporary HOME; keep npm configuration,
  caches, temporary files and agent state there. Enforce filesystem writes within
  that temporary tree.
  Disable npm lifecycle scripts and verify the selected CLI package's integrity.
- [ ] In that isolated environment, run one install with the recorded CLI version:

  ```sh
  skills add jaredchu/context-docs --skill context-docs adopt-context-docs --agent codex --yes --json
  ```

  Enable telemetry only in the child environment, preserving the user's existing
  settings. Mark an automated run truthfully (`CI=1`; preserve agent detection).
  Use project scope; do not run a global install or `skills update`. Compare all
  installed package files with the release's tracked files, including both
  `VERSION` files, excluding generated files such as Python bytecode.
- [ ] Observe the original install telemetry response without replaying the event
  or changing its payload. HTTP 200 establishes request acceptance only.
- [ ] Fetch both public pages again and compare their full rendered `SKILL.md`
  text with the published release, including collapsed content. Account for
  Markdown rendering and omitted frontmatter; infer versions from matched content
  when the pages do not display them. Page availability, an unchanged introduction
  or telemetry acceptance alone does not verify the refresh. If content remains
  stale, allow a bounded processing/cache interval and recheck without repeating
  the install; record the observed wait and any unresolved mismatch.
- [ ] Verify that the existing installed files and symlinks match the saved
  snapshot. Record the source commit, CLI version, isolated package comparisons,
  telemetry outcome, page URLs, check times, content comparisons and preservation
  result in a detailed operator receipt retained in local notes. Keep a concise
  verified result and its material limits in the product release notes, and link
  that result from current project context. The
  [v0.2.6 result](docs/releases/v0.2.6.md#discovery-verification) is an example.
  Distinguish verified page text from unverified supporting-file snapshots, audit
  reruns, counted installs and future refresh reliability. Report static checks
  separately from actual agent evaluations.

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
verified on September 29, 2026.

For every commit Claude helps implement, validate or review, include this
project's Claude attribution trailer exactly once:

```text
Co-authored-by: Claude <noreply@anthropic.com>
```

Credit completed validation and review even when Claude does not edit the files.
When both Codex and Claude assist the work in a commit, include both trailers,
each exactly once, separated from the commit body by a blank line. Keep the
normal human author identity and preserve existing co-author trailers. Credit
only actual assistance. Apply this to new commits; do not rewrite published history
solely for attribution. The README acknowledgment describes project roles and does
not promise a particular position in GitHub's Contributors graph.

## Landing page

See the [site build guide](site/README.md) for local preview and GitHub Pages setup.
Installation commands, the example and package versions come from their canonical
repository sources. Keep the public build allowlist explicit; do not deploy the
repository root.
