# Remove the optional JSONL event journal

## Scope

Retire JSONL event capture, including the auto preference, from the current
Context Docs source packages and user-facing setup. Preserve past journals,
published bundles and evaluation evidence. This work prepares local source.

## Done when

- Current adoption and maintenance use Markdown without the journal helpers or
  logging setup. README, usage guide and generated site agree.
- Existing records remain intact, and earlier adopters can identify and remove
  the obsolete settings while retaining their files.
- Package versions, checks and site tests reflect the removal. An independent
  reviewer assesses the complete change, including removed files.

## Status

Closed on November 25, 2026.

## Outcome

The unreleased skills, adoption flow and site source use Markdown for current
maintenance. The [upgrade note](../getting-started.md#older-jsonl-journal-setups)
covers earlier setups. Saved journal records and frozen evaluation evidence
remain intact. The [decision record](../project-decisions.md#retire-optional-jsonl-event-capture)
owns the retirement scope.

Static checks, 229 automated tests and the 20-file site build passed in a clean
checkout. Independent follow-up review passed after the release history,
evidence overview and legacy settings guidance were corrected. The active
progress link was removed on closure.
