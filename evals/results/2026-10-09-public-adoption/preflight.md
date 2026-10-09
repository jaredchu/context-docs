# Pre-execution review

The four-session [protocol](../../public-adoption/protocol.md) and exact
[manifest](protocol.json) were prepared before subject execution. The candidate
packages come from `3a0c4013962b35c733dc316271f6981aaf5fe9a1`: core 0.1.5 and
unreleased adoption 0.1.7. This record is not a subject result.

Implementation was assigned to GPT 6 Astra with High reasoning. Claude Opus 5.5
reviewed the design and harness in fresh read-only sessions; Codex checked the
findings and final controls. This is author-designed, unblinded development work.

Corrections made before freezing included an explicit README append exception,
precise legacy marker preservation and audit scope, byte-preserving snapshots,
dependent-input drift detection, equivalent links and valid README entry sections,
and rejection of a marker without a separate skill reference. Model verification
uses responding assistant-message fields; auxiliary usage models are recorded
separately. Effort is requested as High, not independently observed. The final
model-evidence correction follows Claude's explicit review recommendation and was
checked against positive, mismatched-responder and usage-only controls.

All 23 new mechanical controls, seven reused guard tests, repository static
checks and diff checks passed before execution. Source fetch, Git blob identities,
answer-key references and frozen-input validation also passed. Earlier disposable
review builds were superseded before any subject session; no scored attempt was
discarded or retried. Local raw peer-review outputs are summarized here rather
than treated as behavioral evaluations.
