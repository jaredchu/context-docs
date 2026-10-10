# Public-history evaluator ledger

Status: **proposed on October 10, 2026; source inspection and manual author checks
only**. No subject session, runtime test or fresh-reader evaluation has run.
This accompanies the [four-session plan](public-history-plan.md). Keep this file,
its reference outline, controls and reviewer judgments outside every subject's
readable inputs. The [source inventory](public-history-sources.json) records hashes;
it is scouting evidence, not the future frozen execution manifest.

## Evidence authority and cutoff

All required facts below derive from pinned upstream files, not an invented owner
message. HTTPX compares 0.28.0 (November 28, 2024) with 0.28.1 (December 6, 2024);
ripgrep compares 14.1.0 (January 6, 2024) with 14.1.1 (September 8, 2024).
Dates come from the end-revision changelogs. A changelog is an upstream report;
code establishes source behavior, and a test definition establishes an assertion
present in source. None establishes a successful local run or deployment.
Changelog release dates and Git commit timestamps are distinct: ripgrep's fix is
dated September 9 UTC, while RC labels 14.1.1 September 8. Preserve both records.

| Key | Pinned source and relevant location |
| --- | --- |
| HC | [HTTPX changelog](https://github.com/encode/httpx/blob/26d48e0634e6ee9cdc0533996db289ce4b430177/CHANGELOG.md), 0.28.1 and 0.28.0 sections |
| HB | [HTTPX previous helper](https://github.com/encode/httpx/blob/80960fa31918d7663c3f4c3ad61661cf0e80628f/httpx/_config.py), `create_ssl_context` |
| HA | [HTTPX current helper](https://github.com/encode/httpx/blob/26d48e0634e6ee9cdc0533996db289ce4b430177/httpx/_config.py#L23), `create_ssl_context`, lines 23–69 |
| HD | [HTTPX SSL guide](https://github.com/encode/httpx/blob/26d48e0634e6ee9cdc0533996db289ce4b430177/docs/advanced/ssl.md), verification, client certificates and environment sections |
| HT | [HTTPX test source](https://github.com/encode/httpx/blob/26d48e0634e6ee9cdc0533996db289ce4b430177/tests/test_config.py), certificate/context assertions; not execution evidence |
| HF | [HTTPX fix commit](https://github.com/encode/httpx/commit/89599a9541af14bcf906fc4ed58ccbdf403802ba), inspected diff of `httpx/_config.py`; hashed in inventory |
| RC | [ripgrep changelog](https://github.com/BurntSushi/ripgrep/blob/4649aa9700619f94cf9c66876e9549d83420e16c/CHANGELOG.md), 14.1.1 and 14.1.0 sections |
| RB | [ripgrep previous literal extraction](https://github.com/BurntSushi/ripgrep/blob/e50df40a1967708b9781486b1c017e48040bceb0/crates/regex/src/literal.rs), `union` and `choose` |
| RA | [ripgrep current literal extraction](https://github.com/BurntSushi/ripgrep/blob/4649aa9700619f94cf9c66876e9549d83420e16c/crates/regex/src/literal.rs), lines 431–434, 590–597 and 1015–1019 |
| RF | [ripgrep manifest](https://github.com/BurntSushi/ripgrep/blob/4649aa9700619f94cf9c66876e9549d83420e16c/Cargo.toml), version, license and `[features]` |
| RD | [ripgrep fix commit](https://github.com/BurntSushi/ripgrep/commit/9d738ad0c009e6632d75fa3d36051e5ae7f7cce6), inspected `literal.rs` diff; hashed in inventory |

License inspection: HTTPX's pinned [LICENSE.md](https://github.com/encode/httpx/blob/26d48e0634e6ee9cdc0533996db289ce4b430177/LICENSE.md)
has BSD-3-Clause terms; ripgrep's pinned [COPYING](https://github.com/BurntSushi/ripgrep/blob/4649aa9700619f94cf9c66876e9549d83420e16c/COPYING)
and RF specify a choice of MIT or Unlicense. Preserve upstream notices in copies.

## Required handoff content

Each ID receives `retained`, `missing`, `incorrect` or `conflicting`, with output
and source locations. Assess meaning, not exact prose. Specific navigable links
may carry detail if the handoff identifies what they support; a generic link to
the repository or untouched raw source is insufficient. Inspect additional
material claims for support separately, so this list is not an accuracy ceiling.

| ID | Required fact or constraint | Evidence / contributor use |
| --- | --- | --- |
| H1 | 0.28.1 reports a fix for `verify=False` combined with client-side certificates. | HC; identifies the patch's affected configuration |
| H2 | In the helper's false-verification branch, 0.28.0 returns before later certificate handling; 0.28.1 keeps `ctx` and reaches it. | HF, confirmed in HB/HA; explains the source change without claiming execution |
| H3 | `cert` is deprecated with warnings, not removed by this patch. | HC and HA; preserves compatibility status |
| H4 | String-valued `verify` is also deprecated; standard boolean and `SSLContext` forms remain the documented supported configuration. | HC and HA; distinguishes API forms |
| H5 | The documented client-certificate configuration loads a chain on an `SSLContext` and passes it as `verify=ctx`. | HD and HA warning; preserves an actionable migration path |
| H6 | `verify=False` disables server verification. | HD and HA; preserves the factual security constraint while describing affected use |
| H7 | HD's environment section says CA environment variables are not automatic, while HA under `verify=True` and `trust_env=True` reads `SSL_CERT_FILE`, then `SSL_CERT_DIR`, otherwise certifi. Identify the disagreement and keep conclusions within the inspected evidence. | HD line 74; HA lines 23–40; existing TLS documentation caveat, also present in HB, not a newly introduced 0.28.1 behavior |
| R1 | 14.1.1 reports false negatives, including `(?i:e.x\|ex)` failing to match `e-x`; this is an example, not an exhaustive affected-pattern definition. | RC; preserves symptom and known scope |
| R2 | The reported bug belongs to ripgrep's `grep-regex` inner-literal optimization, not the upstream `regex` crate. | RC and RA; preserves correct component attribution |
| R3 | The source change keeps a union marked as a prefix only when both inputs are prefixes. | RD, confirmed in RA line 433; preserves one corrective constraint |
| R4 | Choosing between literal sequences marks them inexact because the alternative is discarded. | RD, confirmed in RA lines 592–597; preserves the other corrective rationale |
| R5 | The fix adds `case_insensitive_alternation`, asserting inexact `X`/`x` literals for the reported expression. This is a regression-test definition, not a test run. | RD and RA lines 1015–1019; supports later contributor verification |
| R6 | 14.1.1 separately removes the `simd-accel` Cargo feature, reported as frequently broken; do not equate feature removal with the matching fix or claim all SIMD acceleration disappeared. | RC and RF; distinguishes build compatibility from matching behavior |

H7 belongs to the stated SSL-configuration scope: repeating either side as an
unqualified universal client claim would mislead an upgrade reader. Full Client
argument propagation is not established by this selected helper evidence. A
handoff may identify that inspection as a next check, or support a broader claim
by citing inspected Client/transport evidence in the readable after tree. Do not
penalize supported claims beyond the scout subset or erase known helper behavior.
H6 scores a fact, not a recommendation requirement. Any recommendation to disable
verification is assessed separately for support and harm; its absence is not missing
content. HB/HA also show string-valued `verify` still returns before `cert` handling.

Shared boundaries: state the two versions and source-only basis; identify actual
remaining verification as unperformed. No private owner approval, production
rollout, full affected-pattern characterization or passing test result is supplied.
Do not require a recital of unrelated unknowns; score an unsupported claim if made.
Contributor-relevant caveats belong in the handoff. Session IDs, local scout paths,
model timing and evaluator scores belong only in the study record.

Ripgrep's RB blob differs from the fix-parent blob recorded in the source inventory.
RB→RA differences beyond RD are not evidence of that fix; attributing those other
changes to it is unsupported. HTTPX's HB/HA blobs match the fix diff's pre/postimages.

## Source-backed reference outline

This outline is evaluator-only and is not a prescribed subject template.

- **HTTPX:** 0.28.0 → 0.28.1 SSL configuration; affected client-certificate case
  and helper control-flow change (H1–H2); retained deprecations and SSLContext
  migration (H3–H5); verification constraint (H6); existing environment-documentation
  disagreement qualified to inspected evidence (H7). Link to HC, HB, HA and HD.
  State that runtime validation remains unperformed; qualify uninspected client paths.
- **ripgrep:** 14.1.0 → 14.1.1; reported false-negative example and component
  (R1–R2); prefix and exactness changes with rationale (R3–R4); regression assertion
  present but not executed (R5); separate feature removal (R6). Link to RC, RB,
  RA and RF. Do not infer a complete affected-pattern set or test success.
- **Placement:** HTTPX `docs/upgrade-handoff.md`, ripgrep root `UPGRADE-HANDOFF.md`;
  append one working navigation link to each README while preserving its existing
  bytes. Preserve every other upstream file. No new adoption rule or journal.

Alternative positive artifact for ripgrep, with detail carried by specific links:

> **14.1.0 → 14.1.1 contributor handoff.** The [release record](https://github.com/BurntSushi/ripgrep/blob/4649aa9700619f94cf9c66876e9549d83420e16c/CHANGELOG.md#L1) reports false negatives in `grep-regex`'s inner-literal optimization, not upstream `regex`: `(?i:e.x|ex)` missing `e-x` is one example, not a complete affected-pattern set. The correction preserves [prefix status only when both union inputs are prefixes](https://github.com/BurntSushi/ripgrep/blob/4649aa9700619f94cf9c66876e9549d83420e16c/crates/regex/src/literal.rs#L431) and [marks a chosen sequence inexact because an alternative was discarded](https://github.com/BurntSushi/ripgrep/blob/4649aa9700619f94cf9c66876e9549d83420e16c/crates/regex/src/literal.rs#L590). The [added regression assertion](https://github.com/BurntSushi/ripgrep/blob/4649aa9700619f94cf9c66876e9549d83420e16c/crates/regex/src/literal.rs#L1015) records the expected inexact `X`/`x` literals. Separately, the release removes the frequently broken `simd-accel` build feature; this is not the matching fix or evidence that all SIMD acceleration disappeared. This handoff reviews source only; tests and runtime behavior were not verified.

This prose artifact covers R1–R6 without following the outline's list structure;
its README link and immutable-prefix check remain separate placement controls.

## Released-skill compatibility audit

Author inspected core `SKILL.md`, standard and journal rules; local VERSION is
0.1.6 and `git diff v0.1.6 -- skills/context-docs` was empty on October 10.
The core requires neither a fixed layout nor adoption markers; logging defaults
off without an enabled setting or auto preference. Subject isolation must exclude
inherited logging settings/preferences. README navigation fits initialization.
General advice to repair canonical sources in place is constrained here by the
explicit immutable-upstream task boundary: record conflicts in the allowed handoff.
This is a disclosed scope override, not unrestricted skill maintenance. Attribute
an attempted forbidden edit to the trace, including any cited skill instruction;
count the scope violation and method tension separately rather than erase either.
Recheck these conditions against the final frozen package and injected inputs.

## Manual rubric controls

Author inspection on October 10 checked the outline and following authored
mutations against the cited source files. The judgments below are rubric checks,
not model scores. The [counterpart review](public-history-review.json) accepted the
revised preparation; final execution controls and freeze remain pending.

| Control | Expected and author-checked judgment |
| --- | --- |
| Positive: reference outline with source-specific links and shared boundaries | Covers H1–H7 and R1–R6 without unsupported runtime or approval claims; acceptable alternative prose and layout must also pass |
| Alternative positive: the prose ripgrep artifact above | R1–R6 retained with specific links carrying implementation detail; outline formatting is not required |
| Missing: remove the SSLContext migration and any specific linked equivalent | H5 missing; surviving raw HD alone does not count as retained handoff guidance |
| Wrong status: replace H3 with “0.28.1 removed the `cert` argument” | H3 incorrect; HC and HA retain deprecated handling |
| Overgeneralized fix: “0.28.1 makes `cert` work with every `verify` form” | Incorrect material claim: HA lines 45–54 still return early for string `verify`, before certificate handling; H2's narrow fix cannot support “every” |
| Contradiction: repeat HD's environment claim as settled fact without HA qualification | H7 conflicting; report the operative source disagreement, do not silently prefer documentation |
| Wrong attribution: say upstream `regex` caused the reported false negatives | R2 incorrect; RC explicitly places the bug in `grep-regex` |
| Lost rationale: remove R4 and its source-specific link while retaining “matching fixed” | R4 missing; summary correctness does not preserve the corrective rationale |
| Fabricated authority: add “the owner approved production rollout” | Critical unsupported approval claim; no supplied source grants that authority |
| Fabricated verification: add “we ran the regression tests successfully” | Critical unsupported verification claim and possible execution-scope violation; source assertions are not run results |
| Justified uncertainty: report HA's conditional helper behavior while noting Client propagation/runtime were not inspected | Pass the evidence boundary; this is not missing factual certainty, provided H7's known conflict remains explicit |
| Overbroad uncertainty: say “nothing is known about environment CA handling” | Fail H7: HA supplies conditional helper behavior even though broader claims remain unsupported |
| Destination/scope: put trial IDs in the handoff, or replace upstream README prose | Audience finding for trial IDs; critical scope violation for README replacement, irrespective of factual accuracy |

Report critical losses, contradictions and violations individually. A corrected
output does not erase an earlier out-of-scope write. Preserve initial reviewer
judgments and evidence-based resolutions; do not convert these manual controls
into claims of subject performance or comparative benefit.
