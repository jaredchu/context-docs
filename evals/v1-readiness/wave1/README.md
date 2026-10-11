# Wave 1 preparation for review

Status: **prepared synthetic inputs and mechanical checker; execution blocked**.
October 11, 2026. No model trial, client login, account/profile provisioning or
installed-skill change was performed. This implements the preparation portion of
the [bounded plan](../../../docs/v1.0.0-validation-plan.md), not its execution or
the [graduation gates](../../../docs/v1.0.0-readiness.md).

## Review materials

- [Cases and exact prompt sequences](cases.json): V1 Codex CLI and V6 Claude CLI,
  11 sessions each, **22 total / 4,080 seconds (68 minutes)**. Five journey phases,
  two upgrade variants with U1/U2, one core-only boundary session and one B2–B4
  batch per client. Failed launches consume slots; no retries or background runs.
- [Fixture recipes](fixtures.json): seven project states per client. Journey
  phases carry actual output forward; later phases are not replaced by an authored
  reference. Each upgrade variant has independent package staging and project
  files. The core-only environment has no adoption sibling. The boundary batch
  has separate tracked-context, ignored-private-context and explicit-off projects.
- [Evaluator ledger](ledger.json): approved API/rationale, retry proposal, source
  conflict, current configuration, incomplete export work, dataset blocker/next
  step and unknown runtime. Its reference is a checker control, not agent output.
- [Checker](checker.py) and [controls](test_wave1.py): ignored files, file sets,
  modes/symlinks, saved sentinels, Git index/staged state/refs, journal prefixes,
  tracked/negated-ignore targets, literal leakage and semantic screening limits.
- [Isolation evidence](isolation.json): version/help observations, official
  sources, unverified store/access boundaries and route blockers.
- [Preparation receipt](preparation.json): package and recipe hashes, actual local
  checks, preservation counts and remaining decisions. No execution freeze exists.
- [Counterpart review packet](review-packet.md): bounded pending review; no
  completed Claude review of this implementation is claimed.

## Synthetic fixture boundaries

The tiny offline CSV project has a current timeout of 45 seconds and an earlier
note saying 10. Owner evidence approves API compatibility, leaves five retries
as a proposal, and retains a missing-sample blocker. J2 requests a timeout of 60
and its regression test without naming Context Docs or requesting documentation.
J3 reads the saved context and continues empty-input testing; its final ledger
depends on what was actually implemented and verified. Neither proves deployment.

Upgrade inputs retain the October 1 adoption date, an existing `notes/state.md`
entry point, equivalent guidance, storage and logging choices. The clean variant
has explicit off plus auto; the customized variant has explicit JSONL, historical
synthetic records, a local skill comment and an extra local reference. A staged
owner edit differs from the working version; both and a binary study sentinel
must survive. Subjects may not inspect historical records as routine context.

B2's context is already tracked. B3's ignored context has a literal canary and
private synthetic pricing intent, while a separate public endpoint is available.
B4's ignored context coexists with an exposed journal descendant and explicit off.
The controls verify those Git states rather than assuming folder patterns suffice.
No fixture contains real private project information.

## Materialize and check without models

From the repository root, choose an output path that does not exist in the OS
temporary directory (or `/tmp`). The preparer refuses existing destinations,
checkout/installation overlap and non-temporary destinations. It has no reset,
client-launch or authentication command.

These commands need Python 3.9+, Git and the pinned release commit already present
in this local checkout. They need no model credentials, container or installed
skills. Missing release objects stop preparation; the script never fetches them.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s evals/v1-readiness/wave1 -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 evals/v1-readiness/wave1/prepare.py \
  /tmp/context-docs-wave1-review-new
```

Generated `subjects/<client>/<group>/` contains synthetic projects and independent
`package-state/` copies. These are **staging directories**, not native user-scope
installations or authenticated profiles. `coordinator/` retains package archives,
recipes, ledgers, initial baselines and hashes. All generated inputs stay outside
the repository. The owner setup is never an output destination.

Before trials, an accepted isolation mechanism must make only the appropriate
project and selected native packages accessible to the subject. Deny access to
the coordinator tree, sibling fixtures, owner files and prior-chat memory.
Sibling directories alone do not enforce that boundary.

The checker prints JSON to stdout; retain it outside subject access. For example,
use `snapshot ROOT` before a phase and `compare ROOT BASELINE_JSON POLICY_JSON`
after it. `phase_policy()` expands U1 writes from the pinned candidate manifest;
`check_packages()` checks the exact clean/customized expected bundle. The extra
local reference remains protected and the customized expected hash includes the
original local comment. Later-phase baselines/policies must be frozen after the
preceding actual output and declared coordinator evidence, before launch.

Comparison is read-only and preserves exact Git bytes. No stat-cache exception
has been accepted or implemented. Allowed ordinary writes do not allow deletions,
symlinks, mode changes or Git edits. JSONL checks cover original-byte prefix,
syntax, completed lines and distinct event IDs; full schema/capture validation
remains separate experimental evidence. Audit/no-change policies allow no writes.

## Scoring limits

Mechanical success leaves `native_pass: null`. Review actual invocation/selected
package, loaded instructions, fresh-session and source/context-read evidence,
terminal outcome and executed task tests separately. A placeholder test file,
installed copy or client's self-report cannot complete those gates.

Literal content screening flags lost/maybe-rephrased propositions and specific
stale/fabricated controls. It intentionally never assigns semantic success.
Paraphrases, canonical links, negation, operative contradictions, missing facts
and the public/private meaning boundary require source-backed review using the
[quality protocol](../../quality-protocol.md). Canary absence cannot certify
non-leakage. Inspect retained decisions, authority, blockers and next steps rather
than averaging away a critical loss. All authored references and corrupted
controls remain distinct from native evidence.

## Isolation evidence and blockers

Non-inference help/version commands establish that the installed binaries advertise
the recorded options; they establish no native catalog, loading, authentication
or write-isolation result.

The owner-file inventory detected drift in Codex configuration and Claude global
state during preparation. A subsequent read-only audit reconstructed the exact
Codex baseline with a matching SHA-256: four trust entries for unrelated local
workspaces were added, with no other configuration changes. Claude's recovered
before/retained-after pair differs only in cached feature data and its timestamp;
the audited live file also has a refreshed usage cache. All other Claude fields
and its separate settings file were unchanged. The writer remains unproved.
No rollback was attempted and further owner-client invocations stopped. Saved
study artifacts, installed skills and existing project setup files passed their
hash checks, but broader global-state preservation did not. Treat metadata
commands as potentially stateful on this installation; the proposed isolated
route remains blocked. Local raw evidence stays outside public artifacts; no
unrelated workspace details are copied here.

Codex documents state under `CODEX_HOME`, while user skills are under
`$HOME/.agents/skills` and admin/system roots are additional inputs. A config
profile layers settings; it does not isolate user skill selection.
[Advanced configuration](https://learn.chatgpt.com/docs/config-file/config-advanced),
[skill locations](https://learn.chatgpt.com/docs/build-skills).
Credentials may be file- or OS-store-backed and can refresh during use; do not
symlink writable credentials into tests.
[Authentication](https://learn.chatgpt.com/docs/auth).

Claude documents separate settings/history/plugins with `CLAUDE_CONFIG_DIR` and
configuration-directory-specific macOS Keychain entries or credential-file
fallback. That makes directory isolation a possible route, not a verified
authenticated profile on this machine.
[Settings](https://code.claude.com/docs/en/settings),
[authentication](https://code.claude.com/docs/en/authentication).
Auto memory also needs explicit supported suppression in the test profile, and
history/resume must not carry answers between phases.
[Memory](https://code.claude.com/docs/en/memory).

Before execution, resolve:

1. An existing isolated subscription-authenticated account/profile, all effective
   native package/instruction roots, credential/global store preservation and
   enforced subject access. No such executable environment is established here.
2. The accepted candidate and supported scope. Current source package bytes equal
   v0.1.9; rehearsing the checker with them cannot establish an actual upgrade.
   Do not invent a version bump merely to obtain a passing upgrade receipt.
3. Counterpart checker review and any material corrections, exact native evidence
   requirements, prompts/allowed writes and explicit trial authorization. The
   [project collaboration rule](../../../AGENTS.md#model-collaboration) requires
   the other model's review of consequential evaluation changes. Sol implemented
   and validated these preparations; Opus was not launched because an isolated
   authenticated development-review store has not been established. No substitute
   model, credential export or API fallback was used.

The pinned current-source snapshot is for review, not an approved v1.0.0 candidate.
Wave 2, external validation, publication and real installed upgrades remain
separate decisions. Existing studies and their scores are unchanged.
