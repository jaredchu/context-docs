# Harbor CSV context

## Goal
Prepare compatible CSV export for owner review. Deployment needs separate approval.

## Progress
```text
Goal: compatible CSV export ready for owner review (incomplete) [G]
|-- PASSED   Small-sample check: two CSV samples, staging, Python 3.12 [C7a]
|            Full suite not run; production behavior unknown.
`-- BLOCKED  Large-input check: fixture missing, so not run (not a failure) [C7b]
    `-- NEXT Obtain the fixture, then run the large-input check [C7b]

Outside completion path:
  PROPOSED JSON support [D]
  Deployment needs separate approval, not given [D]
```

Sources: [G] Goal above; [C7a](../reports/check.md#sample) (supplied result, October 18); [C7b](../reports/check.md#large-input); [D](decisions.md#csv).

## Decisions
Mira approved CSV for compatibility with existing clients; JSON is proposed. Deployment is unapproved. See [CSV](decisions.md#csv).

## Next action
Obtain the large-input fixture, then run the large-input check from [C-7](../reports/check.md#large-input). A pass would still leave the full suite unrun and production behavior unknown. Do not deploy without separate approval ([CSV decision](decisions.md#csv)).

## Owner note
Owner wording: retain `format=csv`; do not polish this note.
