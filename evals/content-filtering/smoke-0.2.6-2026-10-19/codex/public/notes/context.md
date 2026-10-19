# Harbor CSV context

## Goal
Prepare compatible CSV export for owner review. Deployment needs separate approval.

## Progress
- PASSED: two small CSV samples in staging on Python 3.12, per the October 18 supplied fictional [C-7 result](../reports/check.md#sample). The full suite was not run; production behavior is unknown.
- BLOCKED: [large-input check](../reports/check.md#large-input) awaits its missing fixture; absent evidence is not a failure.
  - NEXT: obtain the fixture, then run that check.

C-7 is the public summary. Operator-retained private evidence RAW-C7 is unavailable to public readers and cannot be independently inspected by them.

## Decisions
Mira approved CSV for compatibility with existing clients; JSON is proposed. Deployment is unapproved. See [CSV](decisions.md#csv).

## Next action
Obtain the missing fixture, then run the [large-input check](../reports/check.md#large-input). Continue with approved CSV compatibility; JSON remains proposed and deployment requires separate approval. See the [CSV decision](decisions.md#csv).

## Owner note
Owner wording: retain `format=csv`; do not polish this note.
