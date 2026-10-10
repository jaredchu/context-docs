# Project context

Add --limit N to the offline formatter; preserve the current default behavior.
N is a nonnegative integer, absent means unlimited, zero emits nothing, and
excess N emits all selected records. CLI invalid limits use argparse errors.

## Constraints and authority
[Owner Mira's reply](../notes/owner/2026-09-24-preview-reply.md) requires arrival
order because downstream consumers treat it as priority. The input stays untouched.
Load and validate every record before selection, including limit zero or an
already satisfied limit: corrupt later rows must still be detected. The sorting
and early-stop parts of [Dev's design](../notes/design/2026-09-21-preview.md),
proposed for screenshots and latency, were superseded by that reply. Queue
merging and pagination are outside this continuation.

[Identity decision](../notes/contracts/2026-09-15-identity.md): deduplicate by the
exact case-sensitive (tenant,id), keeping the first payload, to avoid dropping
independent jobs across tenants. [Selection contract](../notes/contracts/2026-09-25-selection.md):
apply the cap AFTER tenant filtering and deduplication, not to raw lines.

## Code route
CLI parsing in parcel/cli.py calls parcel/service.py, which fully loads and
validates through parcel/loader.py and parcel/validation.py before calling
parcel/selection.py. Pass the optional limit along this route; preserve render
behavior in parcel/render.py. [README](../README.md) has invocation and tests.
The [local test note](../notes/testing/2026-09-28-local.md) and
[UI review](../notes/ui/2026-09-27-preview.md) require no new dependency or UI work.

## Open blocker
[Operations](../notes/ops/2026-09-26-exporter.md): production exporter v3 lacks
a sample. Synthetic tests cannot clear compatibility; request a sanitized v3
sample from its owner, then check separately. Production rollout is unverified.
