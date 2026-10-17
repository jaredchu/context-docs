# Cedar working context

## Goal
Prepare profile import for owner review. Completion requires format compatibility and duplicate-name checks to pass. Deployment is separate and requires owner approval.

## Work
```text
Goal: profile import ready for owner review (incomplete) [G]
|-- DONE     Format compatibility check passed [A]
`-- BLOCKED  Duplicate-name check not run: representative fixture missing [B]
    `-- NEXT Obtain the fixture, then run the check [B]

Outside completion path: deployment (owner approval not given),
export support (undecided), PROPOSED binary format (not approved) [D]
```

Sources: G [goal](#goal); A [format result](evidence.md#format-compatibility); B [duplicate-name status](evidence.md#duplicate-names); D [decisions](decisions.md). See [retained evidence](evidence.md).

Owner note: keep the `mode=plain` example here.

Example: older profiles containing `mode=plain` must remain accepted.

## Decisions
The owner approved keeping the existing profile format for older clients. A proposed binary format is not approved. Whether to add export support is undecided and outside the import-review goal. See [decision rationale](decisions.md).

## Next move
Obtain the duplicate-name fixture, then run the check. Deployment is not approved.
