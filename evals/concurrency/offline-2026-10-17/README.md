# Offline concurrent-context diagnostic

Run October 17, 2026; retained artifacts inspected October 18. This is a
Sol-authored and assessed filesystem/tool diagnostic, not a native Codex or
Claude trial. No diagnostic process, patch or model session was rerun for this record.

| Forced case | Retained outcome |
| --- | --- |
| Both processes read the original; A writes, then B | B removes A's decision, compatibility rationale and approval boundary. Both writes exit 0. |
| Both processes read the original; B writes, then A | A removes B's sample result and evidence link. Both writes exit 0. |
| Available `apply_patch`, disjoint replacements | Both updates survive; the unrelated next action stays unchanged. |
| Available `apply_patch`, overlapping original line | The first update survives; the stale second patch is rejected. No retry or repair. |

The [protocol](protocol.json) records the synthetic inputs and forced schedules;
[patches](patches.json) records the exact replacements. The
[whole-file results](whole-file-results.json) retain read hashes, write order,
exit codes and output hashes. The [patch results](patch-results.json) retain
the reported patch outcomes and stale-text error.

These four files are byte-exact copies of the retained private records. Inspection
matched the original input hash and all four whole-file output snapshots to their
recorded hashes, and matched the disjoint/overlap final snapshots to the frozen
replacements. The original snapshots, records and preservation manifest remain
unchanged privately. This public record includes no runnable harness or raw
execution transcript; inspecting recorded outcomes is not an independent reproduction.

| Retained artifact | SHA-256 |
| --- | --- |
| [protocol.json](protocol.json) | `41ce2cb788512fd0d65e211a2d8b045b9f9d5b788828d98e2a3a5ea2a195f1e2` |
| [patches.json](patches.json) | `f30b7e75db420370cc3522ae7f43491bd878e606879aaf287f587220ff1a89c2` |
| [whole-file-results.json](whole-file-results.json) | `0c2cb2b470d1f40a5377cecd7aa9d222d13e32dc09f1905180cd8bb7731d7994` |
| [patch-results.json](patch-results.json) | `14d6d6f58a58849e0a3d596098aa61d25a82b10695cd3c5d4059b253e6eca139` |

The deliberately forced schedules establish possible loss, not its frequency in
agent use. Patch results apply to the available `apply_patch` operations only;
disjoint success does not establish semantic consistency, general concurrent
safety or protection from other editing methods. No locking, atomic-replace
behavior or Git/worktree merging was tested. Later
[candidate](../smoke-0.2.5-2026-10-17/README.md) and
[installed](../../installed-skills/2026-10-18-concurrency-v025/README.md) native
smokes are separate evidence with their own qualifications.
