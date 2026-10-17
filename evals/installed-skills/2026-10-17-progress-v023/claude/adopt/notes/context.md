# Cedar working context

## Goal
Prepare profile import for owner review. Completion requires format compatibility and duplicate-name checks to pass. Deployment is separate and requires owner approval.

## Work
```text
Goal: profile import ready for owner review (incomplete) [G]
|-- DONE     Format compatibility check passed [F]
`-- BLOCKED  Duplicate-name check not run: representative fixture missing [U]
    `-- NEXT Obtain the fixture, then run the check (outcome unknown) [N]

Outside completion path: deployment (owner approval not given),
export support (undecided), PROPOSED binary format (not approved) [D]
```

Sources: G [goal](#goal); F [format result](evidence.md#format-compatibility); U [duplicate-name status](evidence.md#duplicate-names); N [next move](#next-move); D [decision rationale](decisions.md). Full [retained evidence](evidence.md).

Owner note: keep the `mode=plain` example here.

Example: older profiles containing `mode=plain` must remain accepted.

## Decisions
The owner approved keeping the existing profile format for older clients. A proposed binary format is not approved. Whether to add export support is undecided and outside the import-review goal. See [decision rationale](decisions.md).

## Next move
Obtain the duplicate-name fixture, then run the check. Deployment is not approved.
