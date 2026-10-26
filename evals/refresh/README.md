# Refresh existing context: baseline first

The owner asked whether a refresh workflow needed new skill instructions or was
already handled by core maintenance. The [pre-run protocol](protocol.md) tests
unchanged published **0.2.6** before selecting a skill change.

The [October 26 result](baseline-0.2.6-2026-10-26/README.md) passes the focused
repair criteria and the second-run no-change check. This supports a documented
refresh invocation without changing either installable skill or its version.
It does not prove that existing instructions cover every drift case.

The later [real-repository observations](../../docs/refresh-observations-2026-10-26.md)
record one correction and an unchanged repeat in Context Docs, plus two unchanged
passes in private maintainer notes. These were bounded interactions in the same
ongoing chat, documented retrospectively with evidence limits. They are not
additional synthetic trials, independent evaluations or a general idempotence claim.

The [synthetic fixture](fixture/README.md) separates configuration, approved
intent and narrow local verification. The [runner](run_native.py) adds an
uncommitted note, verifies the complete copied package against release `v0.2.6`,
freezes inputs and runs two fresh Codex sessions with the same prompt/evidence.
Semantic review remains separate from mechanical equality checks.

For a separately authorized rerun, use a new output directory:

```sh
python3 evals/refresh/run_native.py --out .local/refresh-baseline-new
```

This invokes the configured Codex model through existing subscription access;
it is not an offline test. Preserve earlier results and freeze any changed case
or candidate separately rather than rewriting this baseline.
