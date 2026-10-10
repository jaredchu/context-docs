# Audience/destination pilot — 2026-10-10

All five native sessions passed execution gates. GPT 6 Astra High and Claude Opus
5.5 each accepted **19/19 target criteria** and **15/15 general criteria**, with no
material findings. This is a bounded synthetic regression, not evidence of general
reliability or an advantage over ordinary documentation maintenance.

| Case | Execution | Target criteria, each reviewer | General criteria, each reviewer | Observed outcome |
| --- | --- | --- | --- | --- |
| Public | Pass | 4/4 | 3/3 | Removed expired setup detail; preserved failed evidence and distinct roots in a sanitized derivative. |
| Private team | Pass | 4/4 | 3/3 | Updated the restricted recovery procedure, kept the vault reference and retained production uncertainty. |
| Personal | Pass | 3/3 | 3/3 | Kept useful local paths and offline constraints; consolidated completed repair detail in existing history. |
| Mixed | Pass | 4/4 | 3/3 | Corrected the public API text; asked who should receive the restricted handoff. |
| Audit | Pass | 4/4 | 3/3 | Reported retention issues without writes, searches, journal reads or new events. |

The mixed case **did not produce a handoff artifact**. Its focused audience and
destination question satisfies the pre-frozen criterion; the harmless README
correction was completed first. This is not a claim that the whole hypothetical
handoff task was completed. The personal case retained existing repair history
while disclosing that its thumbnail wording was not corroborated by the raw record.

## Conditions and evidence

- Candidate packages: core **0.1.6**, adoption **0.1.7**, from commit
  `53be1a2fc99c9d9885eff3a7002eea6b1b022c79`. Standard **0.1.1**.
- Harness and exact [manifest](protocol.json) were committed in `af41564` before
  subjects ran. [Manifest SHA-256](protocol.sha256):
  `aff1bdc7e7c49f1c9ec848f449a0af5dd7385eec69dddbbc551602cbaa02654a`.
- Five independent no-Git projects, one attempt each, explicit core Skill
  invocation, Claude Code **2.1.295**, six exposed file/skill tools, no shell,
  network, delegation or publication. No retries or post-run fixture repairs.
- Each responding assistant model was **claude-opus-5-5**, observed from assistant
  message fields. Auxiliary usage also listed **claude-haiku-5-5**; it is not
  treated as the responding model. High effort was requested, not independently
  observed. Auto memory was disabled in per-session settings.
- Execution gates covered actual core delivery, model identity, hook coverage,
  instruction loading, protected bytes and authorized writes. All passed. Across
  47 exposed tool calls there were no denied or out-of-scope write attempts.
  Audit used only Skill and Read on the skill/reference and current project sources.

The [frozen protocol](../../audience/protocol.md), [preflight record](../../audience/preflight.md)
and [counterpart review text](preflight-reviews.json) document pre-run corrections.
Nineteen audience controls and seven reused guard tests passed, along with static
repository and diff checks. These mechanical checks are separate from the native
behavioral results above. Shared helpers, historical studies and skill packages
were not changed during this pilot.

[Results](results.json) retain synthetic before/after files and hashes, final
responses, selected tool results, invocation/model gates and destination scope.
[Astra review](astra-review.json) and [Claude review](claude-review.json) retain
every criterion assessment. They reviewed separately without receiving each
other's conclusions. Astra's trajectory indices are one-based; Claude's are
zero-based. Codex integrated the results and checked counts and evidence.

The exact manifest retains a neutral temporary root for byte verification and
contains no personal host paths. Result copies normalize host/runtime paths and
omit startup inventories, session IDs and raw Skill delivery text. Raw streams,
control settings and original project snapshots remain outside the repository;
the exported evidence does not rewrite those originals.

## Limits and review qualifications

These are five author-created, unblinded cases on one client and responding model,
with explicit invocation and restricted tools. Astra authored some harness changes;
Claude reviewed preflight and is the same model as the subjects. The two
assessments are counterpart review, not external independent validation. There is
no baseline, reader study, implicit-selection test or general reliability estimate.
The guard is not an operating-system sandbox and passing observed instruction
loading does not establish complete system-prompt isolation.

The audit voluntarily avoided writes and history, but therefore did not exercise
native journal search-result discrimination. That distinction has mechanical
controls; future behavioral cases would need a new freeze. Search flags are
heuristics, and retained actual results remain decisive.

One limitation in the preserved Claude review says Grep results are omitted.
The exporter retains permitted in-project search results; these five subjects
made no Grep calls. Package-reference and raw Skill text are omitted from the
trajectory export, while package bodies remain in the manifest. This corrects
review metadata, not a subject verdict or historical score.
