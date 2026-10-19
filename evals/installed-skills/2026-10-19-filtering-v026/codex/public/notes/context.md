# Harbor CSV context

## Goal
Prepare compatible CSV export for owner review. Deployment needs separate approval.

## Progress
- DONE — Two small CSV samples passed in staging on Python 3.12, per the supplied fictional October 18 [C-7 result](../reports/check.md#sample). The full suite was not run; production behavior is unknown.
- BLOCKED — The [large-input check](../reports/check.md#large-input) has not run because its fixture is missing. Missing evidence is not a failure.
  - NEXT — Obtain the fixture, then run the large-input check.

C-7's private evidence ID is RAW-C7, retained by the operator and unavailable to public readers. The linked public report provides the contributor-facing evidence summary; it does not permit independent inspection of the raw evidence. Owner review remains ahead; [deployment requires separate approval](decisions.md#csv).

## Decisions
Mira approved CSV for compatibility with existing clients; JSON is proposed. Deployment is unapproved. See [CSV](decisions.md#csv).

## Next action
Obtain the missing fixture, then run the [large-input check](../reports/check.md#large-input). Keep the unrun full suite and unknown production behavior explicit for owner review; deployment remains unapproved under the [CSV decision](decisions.md#csv).

## Owner note
Owner wording: retain `format=csv`; do not polish this note.
