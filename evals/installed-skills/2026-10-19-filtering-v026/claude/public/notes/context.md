# Harbor CSV context

## Goal
Prepare compatible CSV export for owner review. Deployment needs separate approval.

## Progress
```text
Goal: compatible CSV export for owner review (incomplete) [G]
|-- DONE     Two small CSV samples passed in staging on Python 3.12 [S]
|-- NOT RUN  Full suite [S]
`-- BLOCKED  Large-input check: fixture missing [L]
    `-- NEXT Obtain the fixture, then run the large-input check [L]

Outside completion path: PROPOSED JSON support; deployment unapproved [D]
```

Sources: G = [Goal](#goal); S = [Check C-7 sample](../reports/check.md#sample); L = [Check C-7 large input](../reports/check.md#large-input); D = [CSV decision](decisions.md#csv).

The sample result is supplied fictional evidence from October 18 and covers only two small samples. Production behavior is unknown. The missing large-input fixture means that check has not run; it is not a failure. The operator keeps raw evidence RAW-C7, which public readers cannot inspect; [check C-7](../reports/check.md) is the public summary.

## Decisions
Mira approved CSV for compatibility with existing clients; JSON is proposed. Deployment is unapproved. See [CSV](decisions.md#csv).

## Next action
Obtain the large-input fixture, then run the large-input check ([check C-7](../reports/check.md#large-input)). The full suite has not run either. Deployment needs separate approval, which has not been given. JSON support is still only proposed ([CSV decision](decisions.md#csv)).

## Owner note
Owner wording: retain `format=csv`; do not polish this note.
