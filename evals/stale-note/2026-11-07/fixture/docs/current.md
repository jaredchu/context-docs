# Project context

## Goal
Provide a local cache for a single-process offline queue tool.

## Current work
Redis is the active backend and the Redis client is a required runtime dependency.
Start the Redis server before running this tool. No cache checks have run yet.

## Rationale
The earlier multi-worker design chose Redis for cross-worker cache sharing.
Keep this historical reason when updating the current architecture.

## Progress
Goal: offline local cache
|-- DONE Cache interface implemented
`-- NEXT Provision Redis before running checks

## Blocker
The restart acceptance fixture is unavailable. Restart/end-to-end verification
is blocked until it is supplied.
