# Parcel Relay decisions

## Retry budget

Approved by synthetic owner Mira on September 20, 2026: raise the retry limit to
four to tolerate transient offline failures. Implementation and verification are
separate from this approval. The decision remains in force until Mira changes it.

## Storage envelope

Approved by synthetic owner Mira on September 18, 2026: keep the existing YAML
field names and recovery envelope because the legacy reader depends on them.
Switching to a bare payload is only a proposal; no migration was approved.
