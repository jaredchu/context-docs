# Minimal plugin candidate

Prepared October 18, 2026. **Local packaging candidate, not a directory submission.**
Both released skills remain unchanged: core **0.2.5**, adoption **0.1.14**. Keep
adoption as the setup workflow and core as the maintenance/audit workflow; this
candidate bundles their existing sibling dependency rather than merging them.

## Contents and reproduction

Run from the repository root, choosing a new output directory:

```sh
python3 -B scripts/build_plugin.py --output .local/plugin-candidate-review
```

The [builder](../scripts/build_plugin.py) reads the two canonical `skills/`
directories from pinned release commit `89c91f4`, the current root license and four explicit
[packaging templates](../packaging/plugin/README.md). It produces a folder, ZIP
and SHA-256 inventory. Existing output paths are refused. No installation or
configuration change is performed. Generated copies stay outside the tracked
source tree; make later skill changes under `skills/`, not in a generated copy.
This candidate deliberately uses the pinned release even when working-tree skills
are edited; a later candidate needs an explicit source/version update.

The candidate contains **21 regular files** and a ZIP of approximately **38 KB**.
The check record below pins exact bytes for the final build.
It includes both skills' references, assets, helpers, licenses,
versions and Codex metadata, plus a short README, MIT license, original SVG icon
and two manifests. All 16 skill files match the released source bytes. No study
results, project context, setup files, credentials or history enter the package.
The [check record](../evals/packaging/plugin-candidate-2026-10-18.json) pins the build
and records validation and review limits.

The portable [OpenAI manifest](../packaging/plugin/plugin.json) marks local execution
as required. The [Claude manifest](../packaging/plugin/.claude-plugin/plugin.json)
uses the default sibling `skills/` layout. There is no marketplace catalog, MCP
server, hook, auto-installer, telemetry endpoint or background service in the bundle.
These are packaging drafts, not a new skill release or a change to existing setups.

## Claude policy assessment

**Eligibility is unresolved. Local operation and user authorization are not a
documented exception to the directory policy.** This is a source-based engineering
assessment; only Anthropic can resolve its directory interpretation and acceptance.

The [Software Directory Policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy)
section 1.F broadly restricts extraction from product memory, chat history,
conversation summaries and user-generated or uploaded files. Context Docs does not access built-in product
memory or chat-history stores, but its normal purpose includes reading and
summarizing user-authored project Markdown. That is a direct overlap requiring
clarification, rather than a claim we can clear by renaming the feature. A saved
context document can itself include session-derived summaries; the policy concern
therefore applies even without opening a built-in history store. The text does not
separately establish a blanket prohibition on creating a new summary, and this
assessment does not invent one.

| Area | Observed workflow | Assessment |
| --- | --- | --- |
| Project files, section 1.F | Read and maintain selected README, context, decisions and potentially saved conversation summaries | Unresolved policy overlap, including local coding use |
| Context collection, section 1.D | Select durable task-relevant information; omit secrets and unnecessary personal/customer data | Intent is to avoid excess collection; actual necessity and directory interpretation remain unverified |
| Optional journal, sections 1.D/F | Explicit project settings control selected local events; no transcript store or background capture | Logging is not categorically forbidden by 1.D, but unnecessary context collection is; enabling it does not resolve either policy question |
| External instructions, section 2.F | Core's references and adoption's sibling are bundled, not remotely fetched | No declared dynamic instruction-download mechanism; project instructions still remain subject to the host's instruction hierarchy |
| Safeguards, sections 1.B and 2.D–E | Preserve project rules and authorization; no hooks or permission-setting changes | No deliberate bypass or unrelated tool coercion identified in the inspected instructions |
| Standing project instructions | Adoption adds or reuses a maintenance rule in loaded AGENTS.md/CLAUDE.md | An authorized persistent edit, requiring disclosure and instruction-hierarchy review; uninstalling a plugin leaves the project rule in place |

The canonical [core skill](../skills/context-docs/SKILL.md),
[adoption skill](../skills/adopt-context-docs/SKILL.md) and
[audience/destination guidance](../skills/context-docs/references/standard.md#audience-and-destination)
establish those workflow boundaries. They do not override Anthropic policy.
The host agent may process content through its own service; absence of a separate
plugin endpoint is not a promise that project data never leaves the machine.

Proposed clarification to Anthropic, **not sent**:

> Do sections 1.D/F permit a coding plugin that reads and edits user-selected
> project Markdown, including saved session summaries, for authorized documentation
> maintenance, without accessing built-in memory or chat-history stores? Adoption
> can add a standing maintenance rule to project instructions, and explicitly
> enabled logging appends selected task-relevant local events. What scope and
> disclosures would be required for these operations and supported surfaces?

Do not submit until that interpretation is resolved. Do not claim Claude approval
or make silent skill changes to evade review. Removing adoption would not resolve
the overlap: core maintenance itself reads and summarizes project documents.

## What is checked and what remains

Claude Code's local strict manifest validation passes, with non-blocking advice
to add a marketplace install line. The advice is retained; no working marketplace
exists, so the candidate README does not advertise an unverified install command.
Local validation does not establish directory-policy compliance or runtime behavior.
The [Claude pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist)
adds portal validation, safety scanning, name availability and review. Its size
rules apply to the plugin folder and, for some checks, the containing repository.
Future GitHub publication would need a selected plugin folder or dedicated source;
the local ZIP is not a GitHub-hosted Claude submission.

OpenAI documents [portable packaging](https://developers.openai.com/plugins/build/plugins),
[local-executor requirements](https://developers.openai.com/plugins/deploy/desktop-only)
and [submission requirements](https://developers.openai.com/plugins/deploy/submission).
The candidate sets `requires_local_executor: true`; this is no approval or proof
of account eligibility. Its root JSON has been inspected against the documented
fields, not validated by OpenAI's complete manifest schema or portal. The separate
OpenAI skill quick validator was unavailable because PyYAML is absent; existing
Node YAML parsing and repository skill/link checks were used without installing
dependencies. Publisher verification, portal checks, listing fields and
category values still need confirmation in the actual submission account.

Claude Opus 5.5 reviewed the initial candidate with tools disabled. Verified
findings were corrected or dispositioned in the check record: the builder now
pins released Git objects, and the policy/README clarify saved summaries,
selective logging, persistent project rules and unverified invocation. Final
corrections received local packaging checks, not a second counterpart review.

The later [isolated loading check](../evals/packaging/plugin-loading-2026-10-18/README.md)
registers both namespaced Claude Code commands without a model prompt. Its Codex
startup failures remain retained. A separate [Codex follow-up](../evals/packaging/codex-plugin-loading-2026-10-18/README.md)
now parses both skill entries natively using scratch SQLite/logs and an exact
runtime-identity file exception, with network denied. Identity bytes and checked
metadata remain unchanged; this shares existing runtime identity rather than
providing a clean profile. The plugin remains uninstalled and disabled. Neither
native check sends a model prompt; a separate Opus review of the diagnostic route
retains its qualifications. Original evidence is unchanged.
No plugin has been persistently installed. Sibling reads during adoption,
namespaced invocation, implicit selection, duplicate standalone
skills and preservation during a plugin upgrade need a small isolated runtime
check before any supported-plugin claim. In particular, do not enable this candidate
beside existing standalone skills until their selection and project-rule references
are tested. General chat, hosted execution and Cowork
remain unvalidated; the existing standalone evidence retains its qualifications.
The checks use a private scratch catalog and process-only configuration; no
existing setup was reconfigured. No package/dependency installation, submission,
publication, policy inquiry or maintainer message occurred.
