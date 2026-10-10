# Project context

## Authorized continuation
Add --limit N to the JSONL formatter. N is a nonnegative integer; zero emits
nothing, excess N emits all records, negative values use argparse exit 2.
Default output stays unchanged.

## Approved constraint and rationale
Owner Mira requires retaining input order and leaving the source untouched:
downstream consumers interpret arrival order as priority. See
[owner reply](../notes/2026-10-04-owner.md).

## Superseded proposal
The sorting part of the [October 2 design](../notes/2026-10-02-design.md),
intended to stabilize previews across exporter versions, was superseded by Mira's
October 4 reply. The limit feature remains authorized.

## Open blocker
Production exporter v3 compatibility lacks a sample. Local synthetic tests cannot
resolve it. Request a sanitized sample from the exporter owner; production rollout
is unverified. See [operations](../notes/2026-10-05-ops.md).

## Other current facts
The [UI review](../notes/2026-10-06-ui.md) requests no formatter changes.
Code and local tests are described in [README](../README.md).
