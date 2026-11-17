# Antigravity CLI: blocker diagnosis and scoped follow-up

**LOCAL evidence; provisional setup guidance remains appropriate.** The original
failures involved denied shell listings and parent sessions ending with wait-only
responses. Scoped enumeration worked in the follow-up, but did not ensure task
completion. The denied-shell adoption control succeeded; scoped adoption timed
out; initial scoped refresh ended blank after a denied search; audit completed.
The separate search-capability refresh attempt also timed out without edits,
after permitted literal searches succeeded. Refresh completion remains unresolved
within these bounded conditions.

## Outcomes

Each row is a fresh, independent fixture, with the original task prompt and rubric.
Task completion is scored separately from native exit status and file preservation.

| Case | Condition | Native result / wall time | Behavioral task result |
| --- | --- | --- | --- |
| B | Adoption on B0, shell denied, omitted execution-mode setting, no added permission note | SUCCESS / 195.036 s | PASS: one maintenance rule and marker; project facts preserved |
| A | Adoption on B0, explicit Default mode, scoped helper and permission note | interrupted at 240 s cap / 240.423 s including termination | INCOMPLETE: no edits or final answer |
| R | Refresh on original C0 plus original standup, scoped helper | SUCCESS with empty response / 103.035 s | INCOMPLETE: no edits; stale blocker remains |
| U | Audit on original completed S3, scoped helper, all writes denied | SUCCESS / 128.725 s | PASS: missing runbook link identified with location; every byte unchanged |
| R2 | Fresh refresh fixture, added guarded literal search | interrupted at 240 s cap / 240.313 s including termination | INCOMPLETE: search worked, but no edits or final answer |

The control preserves the SQLite decision and rationale, proposed/unapproved
Parquet export, CDX-4471 blocker, station-filter next action and unresolved timezone
conflict. Its final response claims automatic AGENTS loading, but the trace does
not substantiate that claim; automatic loading remains **unverified**.

A completed 13 direct file reads and 11 helper calls, including relevant project
sources and extra skill references. One unsupported multi-root `find` returned
exit 64; subsequent single-root calls worked. Its last tool activity was successful
root enumeration at step 48, followed by no further completed tool events before
the cap. No editing attempt or child delegation was observed. This is a bounded
timeout, not evidence that the helper failed or that adoption is incompatible.

R read the new standup and current context successfully. Its last requested shell
operation was `grep -rn "Blockers" <workspace>/.agents/skills`, outside the frozen
allowlist. Headless review soft-denied it; the session then returned an empty
SUCCESS result. The missing search capability motivated the separately frozen R2
condition; R remains an incomplete result regardless of R2's outcome.

R2 successfully searched documents and copied skills through the added helper.
Its last successful tool call was `search "blocker" .agents/skills` at step 42;
it then reached the time cap with no edits or final answer. A missing-runbook
inspection returned a normal missing-file error, not a search permission denial.
No requested documentation write was denied in these new cases: B's edits
succeeded, while A/R/R2 did not reach a documentation write request. Thus broader
permissions alone are not shown to solve the remaining completion problem.

U reported the seeded broken `docs/runbook.md` link at
`docs/project-context.md:42`. It also described missing cache-work tracking,
unimplemented configuration/timezone handling and combined-station semantics.
The pass rests on the verified concrete broken-link finding and unchanged bytes,
not on treating every suggested improvement as an approved requirement.

## Why the original cases did not complete

The [original record](../2026-11-17/README.md) remains byte-identical. In S1, S2
and S5, the core skill was read successfully; S1 also received native adoption
slash expansion. The blanket `command(*)` deny blocked the chosen `ls`, `find`,
Git and Python commands. Advertised native enumeration tools existed, but the
observed strategy used research children that repeated blocked commands and
then guessed paths. The parents ended with wait-for-child text rather than the
requested result, despite SUCCESS/exit zero.

Thus the direct permission barrier is established, as is an unsuccessful
parent/child strategy. The internal cause of premature wait-only completion is
unknown. The successful denied-shell control on the later build shows that shell
access was not necessary for that adoption attempt. It does not identify why the
older attempt failed.

## Permissions and controls

- Unchanged skill packages: core 0.2.7 and adoption 0.1.16, in `.agents/skills/`.
- Session-only fixture reads and documentation writes; copied skill, code,
  configuration, data and Git writes protected. U explicitly denies `write_file(*)`.
  Web/MCP, credentials, private host evidence and outside writes remain restricted.
- A/R/U explicitly configure `agentMode: ""` (Default) with `toolPermission:
  "request-review"`. This was a safety amendment before those cases began,
  after discovering that omitted mode can select Auto. B retained omitted mode
  plus blanket shell deny. Init reports request-review, not execution mode;
  R's ungranted search was observed soft-denied.
- Only an absolute, fixed-fixture helper is granted as a command. It implements
  enumeration without shell evaluation and narrowly invokes read-only Git with
  fixed arguments/environment. A fixture AGENTS note explains this capability;
  it is a declared instruction condition, separate from adoption's maintenance rule.
  All 57 initial guard checks passed; actual helper invocations succeeded.
- R2 adds literal substring search only, with validated root/cwd/realpaths,
  symlink refusal, 256 KiB file and 160-match output caps. All 32 second-phase
  checks passed, including no evaluation of shell-substitution text. Plain grep,
  interpreters and arbitrary shell commands remain ungranted.
- These are application permissions plus tested helper controls, **not OS
  isolation**. Prefix grants and surrounding shell syntax have separate risks;
  shell-control deny patterns are defense in depth, not an independently proved
  native parser boundary. File rules are not claimed to sandbox commands.

The original phase-one protocol and pre-scoped-mode amendment are preserved.
After R exposed the search gap, the coordinator explicitly expanded the internal
four-session limit to five for **R2 only**, retaining the original 960-second
aggregate cap and 240-second per-case cap. No timeout-driven A repeat, successful
U repeat, permission widening within an attempt or hidden retry occurred.
The five parent sessions used **907.532 seconds** in total. A/R2 wall times
include less than half a second of termination overhead each after their caps.
All attempts and failures are retained; no further subject runs followed R2.

## Loading, preservation and limits

Completed direct core `SKILL.md` reads were observed in every case. R2 also
read the adoption `SKILL.md` directly during the implicit refresh attempt; that
read did not yield a completed refresh.
Adoption slash expansion in B/A is reported separately from a direct adoption
skill file read. Neither B nor A completed a direct read of the adoption
`SKILL.md`, so that frozen loading criterion remains unmet in both. B's pass
records behavioral completion and preservation, not an adoption-loading pass.
No native child events were observed in the new runs; the
original child-model qualifications remain in the original record. Parent model
was fixed to `gemini-3.8-flash-medium`. Automatic instruction injection is not
independently confirmed by these traces.

Original public evidence, original private host evidence, repository/selected
installed skill trees and selected global settings are unchanged. Phase-one
fixture code, configuration, data, copied skills and Git metadata are unchanged;
only B's AGENTS/context documents changed. R2's complete fixture and Git
metadata also remained unchanged, and the frozen phase-one evidence was preserved. U's complete fixture, index and HEAD
state remained identical (the fixture has no commits). Native conversation/log
state was created separately and is not claimed unchanged.

The CLI was already **1.5.9**, versus **1.5.7** in the original trial; no update was
performed by this task and the reason for the earlier change is unknown. Its
binary hash was stable during the checks. Google's [CLI changelog](https://antigravity.google/docs/changelog)
describes a v1.5.8 queued-message/subagent-reply fix and v1.5.9 workflow/MCP changes.
No corrupt original queue was observed, so those notes are alternative context,
not a proven causal diagnosis. Build, execution mode, permission note, helper
capabilities and stochastic behavior confound comparisons. A/R/U are independent
bases, not an adoption-to-refresh-to-audit chain. One attempt per declared
condition does not establish reliability, effort savings or general compatibility.
App, IDE, interactive use and global skill placement remain untested.

Existing included account access was used, with `useG1Credits:false` and empty
`modelProvider` on every invocation. No API-key override, paid fallback or
quota/payment barrier was observed. Account tier and billing were not independently
verified. No commits, pushes, deployments, releases or skill/version changes are
part of this local task.

## Inspectable evidence

- [Phase-one protocol](protocol.json), [explicit-mode amendment](protocol-amended.json),
  [results](results.json), [author scores](scores.json),
  [fixture manifests](fixture-manifests.json), [preservation](phase1-preservation.json).
- Per-case `*-trace-extract.json`, `*-settings.json` and `*-fixture.json` retain
  successful/error tool calls, native finals and before/after synthetic text.
  [B's diff](B-changes.diff) shows the only phase-one edits.
- [Guard source template](guard-template.py.txt) and [57 checks](guard-tests.json)
  describe the task-specific control; it is not an installable product adapter.
- [R2 protocol](phase2/protocol.json), [R2 results](phase2/results.json),
  [search guard](phase2/guard-template.py.txt), [32 checks](phase2/guard-tests.json).
- [Provenance and final preservation](provenance.json) identifies private raw
  evidence by hashes. Paths/runtime identifiers are removed or replaced in these
  derivatives; hashes do not make private traces independently inspectable.

Author-scored by Codex (GPT-6 Astra). Source review is separate from these native
behavioral observations. Current [permission documentation](https://antigravity.google/docs/permissions?tab=cli),
[headless behavior](https://antigravity.google/docs/cli/headless/) and
[session settings](https://antigravity.google/docs/settings?tab=cli) informed the
controls; actual emitted events and file manifests determine the reported results.
