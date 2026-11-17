# Antigravity CLI: longer-timeout follow-up

**LOCAL evidence; setup guidance remains provisional.** Both fresh cases met the
original behavioral criteria: adoption in **160.531 seconds** and search-enabled
refresh in **306.391 seconds**, under a 600-second cap each. These are two
independent fixtures, not a complete adoption-to-refresh workflow. The earlier
failures remain preserved; successful behavior does not establish automatic
instruction loading or general reliability.

| Case | Native result / wall time | Behavioral result | Changed files |
| --- | --- | --- | --- |
| A — adoption | SUCCESS / 160.531 s | PASS: one maintenance rule and correct marker; facts preserved | `AGENTS.md` only |
| R2 — refresh with search | SUCCESS / 306.391 s | PASS: dated access approval recorded; proposal, decision and conflict preserved | `docs/project-context.md` only |

A completed within the former 240-second cap, so its success cannot be attributed
to the longer timeout. R2 used more than 240 seconds in this attempt; the extra
allowance permitted this run to finish. Fresh sessions and variable model behavior
mean that neither result proves a timeout-only causal explanation for prior failures.
The two parent sessions used **466.922 seconds** in total. No timeout, quota/payment
barrier, retry, child delegation or documentation-write denial was observed.

A added one `Method: context-docs` / `Adopted: 2026-11-17` / entry-point marker and
an ongoing maintenance rule, preserving the operational permission note and all
other fixture bytes. Native adoption slash expansion and a direct core `SKILL.md`
read were observed. **No direct adoption `SKILL.md` read occurred in A**, so that
frozen loading criterion remains unmet despite the behavioral pass. Its final
claim of automatic AGENTS injection is **unverified** by the trace.

R2 successfully used the literal-search helper and read both skill files directly.
It removed the stale CDX-4471 blocker from progress/current work and saved the
2026-11-12 approval with the standup's confirmation-email attribution in the next
action. SQLite and its rationale, unapproved Parquet export, station-filter next
step and unresolved UTC/local conflict were retained. The saved page does not
link the standup directly; the final answer does. The seeded broken runbook link
also remains, making the final answer's broad link-verification claim unsupported.
The PASS is for the frozen refresh criteria, not every assertion in that answer.
The adoption-file read during refresh does not retroactively satisfy A's loading
criterion.

## Frozen conditions

This is a separate, owner-authorized local follow-up to the
[240-second scoped attempts](../2026-11-17-scoped-rerun/README.md).
One fresh adoption fixture reproduces A; one fresh refresh fixture reproduces
R2 with bounded literal search. They are independent bases, not a chained workflow.
All fixture bytes match their prior before-manifests except the declared absolute
helper path in the AGENTS evaluation permission note. The prompts, fictional facts,
original criteria, unchanged skill copies, model and effective permissions are retained.
The intended experimental change is the timeout: **240 → 600 seconds per case**,
with a shared 1,200-second budget and bounded termination overhead. Fresh sessions
and nondeterministic behavior prevent a causal or reliability claim from two runs.

The existing CLI is **1.5.9**, with SHA-256
`fad3628ad91fe8613a72f074a1c5fde7cd816517788a5b9be96703f7d256741a`.
No update was performed; the binary version/hash match before and after. Parent
model is `gemini-3.8-flash-medium`.
Session settings retain `agentMode: ""` (Default), `toolPermission:
"request-review"`, `useG1Credits:false`, empty `modelProvider`, and disabled
status/title generation. API override variables are removed by the runner.
Account tier and billing are not independently verified; no paid fallback is selected.
The pre-run built-in usage query reported **45% Gemini weekly allowance remaining**.
The post-run query timed out at 45 seconds and was terminated; its allowance is
**unavailable**, and it was not retried. No task CLI process remained afterward.
The [usage record](usage-check.json) separates this diagnostic failure from the
two completed subject attempts. Neither subject trace contains a quota/payment barrier.
The runner reserves each launch once, checks protocol/settings/fixture/helper/build
hashes, watches quota/rate/payment/model-unavailable barriers, and stops the process
group at the cap. There are no retries, controls or additional subject audits.

Only the fixed-fixture helper command is granted. A permits enumeration and fixed
read-only Git operations; R2 also permits literal search. The native write grants
cover only AGENTS, README and docs; code, tests, data, notes, configuration, copied
skills and Git remain protected. Unknown commands require review and are unavailable
headlessly. Private host evidence, external files, credentials, web and MCP remain
restricted. Helper tests cover outside paths/cwd, symlinks, unsupported operations,
search size/output limits and literal shell-substitution text: **51 passed**
(19 adoption, 32 refresh). These controls are application rules and tested helpers,
not OS isolation or a proof of the native shell parser's boundary.

The new host uses one fixture directory layout. Equivalent evidence-deny paths
were rebuilt; before inference, the former R2 parent-fixture deny was removed
because the flattened layout would otherwise deny its own new fixture. An explicit
sibling-fixture deny remains. This is recorded in the frozen protocol, alongside
raw source hashes. The evaluation permission note is an operational instruction
condition, not the adoption maintenance rule.

## Evidence and interpretation

- [Frozen protocol](protocol.json), [guard tests](guard-tests.json),
  [adoption helper template](A-guard-template.py.txt),
  [refresh helper template](R2-guard-template.py.txt), [runner](runner.py.txt).
- [Results](results.json), [scores](scores.json), [fixture manifests](fixture-manifests.json),
  [preservation](preservation.json), and [provenance](provenance.json).
- Each case's `*-trace-extract.json` preserves completed tool calls and native
  final output; `*-fixture.json` preserves synthetic before/after text;
  `*-settings.json` records its redacted settings; `*-usage.json` records emitted
  token counters. Native success, task completion, direct skill loading and file
  preservation are scored separately.

The original and scoped public evidence and private scoped host remain byte-identical.
Portable derivatives redact host paths and runtime identifiers. Manifest hashes
refer to raw fixture bytes; the portable AGENTS text substitutes helper paths.
Private raw traces are identified by hashes, not made publicly inspectable by them.
Author scoring is by Codex (GPT-6 Astra); source review is separate from native
behavioral evidence. No general App/IDE, interactive or global-placement guarantee
is established, nor reduced effort or compatibility reliability. Skills and package
versions remain unchanged. All work remains local, with no commit, push, deployment
or release.
