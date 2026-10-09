# Public evidence metadata cleanup — 2026-10-09

The owner requested cleanup of unnecessary local-development data before the next
release. This repository now contains sanitized derivatives of 43 tracked files,
mostly earlier evaluation streams and diagnostic outputs. The
[hash ledger](../evals/results/redactions-2026-10-09.json) identifies every changed
file, its prior SHA-256, public-copy SHA-256 and transformation categories.

The transformation normalizes the developer's home and repository prefixes to
`/user-home` and `/context-docs-repo`. Host-specific Claude cache project roots use
stable identifiers; distinct roots remain distinct. Unrelated startup
skill, agent and command inventory names use explicit placeholders, preserving
list lengths and the two Context Docs skill names. Model identities, tool catalogs,
client versions, call identifiers and tool-result relationships are retained.
No evaluation score, acceptance criterion or reported failure was changed.

Original bytes were copied to an ignored local evidence backup before modification.
The backup and public-copy hashes were verified. Every original also matches
its ledger hash at the recorded base commit `c9aa810`; there were no uncommitted
originals in this set. That commit is local until published. The backup is not
part of the public package. Existing raw hashes, original protocol freezes and prior source revisions
still identify their historical bytes; they must not be presented as hashes of
these derivatives. Use the ledger's public hashes for the current copies. This
cleanup does not rerun or retrospectively regrade any study.

The transformation excluded `.context/events/` and installable `skills/` files;
non-UTF-8 or unreadable files would be skipped. A separate targeted scan of tracked
text found no remaining personal home/storage prefixes. This is not a comprehensive
privacy or credential audit, and journal contents were not rewritten. Historical Git commits and already published releases are unchanged, so
old copies can still contain the original metadata. Rewriting shared history is a
separate action and was not part of this cleanup.

Current context was also condensed into durable direction, present state, limits
and next actions. The [decision history](project-decisions.md) preserves recorded
authority and rationale; detailed results remain in their existing reports.

Validation compared each derivative against its original, permitting only the
listed path transformations and startup inventory placeholders. JSON structure,
numeric/boolean values and all other strings matched. All 20 local CI-equivalent
check groups passed, including 127 unit tests and regeneration of the quality,
history, routing and guarded report outputs without changes. No replaced inventory entry contained a namespaced or decorated `context-docs`
name. Startup events retained their other fields apart from the declared path
normalizations. No new agent behavioral evaluation was performed.
