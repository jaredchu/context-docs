# Owner decisions (synthetic fixture)

## Earlier rationale — superseded
The earlier multi-worker design selected Redis for cross-worker cache sharing.
Keep that rationale as history; it is no longer the current architecture.

## Approved replacement — 2026-11-07
Remove Redis and its client dependency. Use a process-local in-memory dictionary:
the tool now runs as one process and must work offline without a background
service. Cache entries are intentionally ephemeral; do not reintroduce Redis or
promise persistence. Preserve the earlier cross-worker rationale as history.

## Unresolved acceptance check
The restart acceptance fixture is unavailable. Restart/end-to-end verification
remains blocked until that fixture is supplied; unit checks cannot clear it.
