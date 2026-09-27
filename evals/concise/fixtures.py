"""New synthetic projects authored after candidate freeze 136bd31; no private inputs."""
from textwrap import dedent


def md(text):
    return dedent(text).strip() + '\n'


RELEASE = {
    'README.md': md('''
        # Beacon catalogue

        Beacon publishes a searchable catalogue of field equipment manuals for a small
        pilot team. This repository contains the static catalogue and its operating
        documents. It does not own the equipment database or the vendor documents.
        Contributors must preserve that boundary when describing imports or releases.
        A successful local build shows that the catalogue can be assembled; it does
        not establish which version a pilot operator currently sees.

        Begin with [current context](docs/context.md). Detailed [release instructions](docs/release.md)
        and the [design note](docs/design.md) explain the two workflows discussed during
        planning. The [decision register](docs/decisions.md) records owner authority.
        The [handoff](docs/handoff.md) includes questions still awaiting evidence.
    '''),
    'docs/context.md': md('''
        # Current context

        The catalogue pilot is limited to approved sample manuals. No customer uploads
        or public submissions are part of this iteration. The owner wants a reliable
        small release process before adding ingestion or access management. Search
        behavior and the document review process are outside this maintenance task.

        Release on every push to the main branch after CI passes. See the
        [design](design.md) for motivation and the [release guide](release.md) for commands.
        The command in the release guide is also useful for previews. A failed preview
        must not be described as a failed production release without further evidence.

        RESTORE-61 remains blocked because the test volume has not been allocated.
        The next action is for the operator to request a disposable restore volume.
        Keep that work visible even if release documentation is simplified.
    '''),
    'docs/design.md': md('''
        # Release design

        Written September 2, 2026. Automatic publication on pushes to main removes
        repetitive operator steps and makes the artifact traceable to a commit.
        The intended workflow requires CI to pass before publishing. Deploy on every
        main-branch push, with no manual publication step. This design assumes that
        the hosting project is connected to Git and the test job is mandatory.

        Preview links should be recorded with the source revision so reviewers can
        distinguish content changes from stale browser caches. If a preview is
        rebuilt, retain the previous review result as evidence for that revision
        rather than presenting it as a review of the replacement. The rationale for
        automation remains useful even if its implementation is postponed.
    '''),
    'docs/release.md': md('''
        # Pilot release

        ## Publish

        The September 12 owner decision [DEC-61](decisions.md#pilot-workflow) approves
        manual publication during the pilot. Build the catalogue, inspect the local
        artifact, then run `wrangler pages deploy dist`. CI is optional in this phase.
        Record the artifact revision and deployment receipt when the operator actually
        publishes. Documentation maintenance does not itself authorize publication.

        ## Recover

        Keep the last accepted artifact until the replacement has passed the pilot
        review. If the replacement is rejected, use the previously accepted artifact;
        do not silently rebuild it from a newer revision. The restore exercise remains
        separate from this rollback procedure and still needs its own test volume.
    '''),
    'docs/decisions.md': md('''
        # Decision register

        ## Pilot workflow

        DEC-61: Owner Mira approved manual publication on September 12, 2026, to keep
        pilot setup small and permit an operator to review each artifact. Mandatory
        CI and automatic Git publication are deferred proposals. The September 2
        design is not the current release policy. Revisit automation when releases
        become frequent enough for its setup cost to be justified.

        ## Source boundary

        DEC-62: Owner Mira approved sample manuals only. External catalogue ingestion
        remains a proposal because document rights and update ownership have not been
        agreed. Approval of a release process does not approve new content sources.
    '''),
    'docs/handoff.md': md('''
        # Operator handoff

        September 20 contributor note: a hosting dashboard screenshot may indicate
        that a Git integration was enabled during a demonstration. The screenshot
        is not included in this repository, and no deployment receipt or owner
        decision changing DEC-61 is recorded. Confirm the actual integration settings
        before the next release. Do not treat this note as authority to override the
        approved pilot workflow or claim that production was checked.

        Release labels should refer to an artifact revision rather than an informal
        meeting name. The operator still needs to choose where receipts are retained;
        that storage question is unresolved and does not prevent documenting the
        approved manual process. RESTORE-61 remains open until a disposable volume
        is allocated and the restore exercise can be performed.
    '''),
}
RELEASE_ORACLE = {
    'docs/context.md': RELEASE['docs/context.md'].replace(
        'Release on every push to the main branch after CI passes. See the\n[design](design.md) for motivation and the [release guide](release.md) for commands.',
        'Use the approved [manual pilot release](release.md), with optional CI, under\n[DEC-61](decisions.md#pilot-workflow). The [automation design](design.md) is deferred.'),
    'docs/design.md': RELEASE['docs/design.md'].replace(
        'Written September 2, 2026.',
        'September 2, 2026 proposal, superseded for the pilot by [DEC-61](decisions.md#pilot-workflow).\nThe following describes deferred automation, not current release instructions.\nUse the [manual pilot release](release.md), with optional CI.'),
}
INIT = {
    'README.md': md('''
        # Parcel ledger

        Parcel is an offline command-line tool for reconciling two exported warehouse
        ledgers. It reads local CSV files and writes a local discrepancy report. It
        does not contact a warehouse service, upload records, or decide which source
        is financially authoritative. A human reviewer uses the report to investigate
        mismatches. This distinction matters because the same identifier can appear
        in exports taken at different times.

        See [usage](docs/usage.md), [format](docs/format.md), [decisions](docs/decisions.md)
        and [open work](docs/open-work.md). There is no project context entry point yet.
        The documents contain the current supported workflow and its boundaries.
    '''),
    'docs/usage.md': md('''
        # Usage

        Run `parcel compare left.csv right.csv --output report.csv` from a directory
        where both exports are readable. The tool treats the two input files as
        read-only evidence. It refuses to overwrite an input with its output. Keep
        the source exports until a reviewer accepts or rejects the report; rerunning
        against different exports is a different comparison, even when filenames match.

        Review missing identifiers before comparing quantities. A missing identifier
        may mean that an export was filtered, not that an item was deleted. Preserve
        field order from the left export in the discrepancy report so reviewers can
        compare the report with the original spreadsheet without remapping columns.
        Input rows are not deduplicated automatically because duplicate identifiers
        may represent separate warehouse locations. See the format document for the
        composite matching key and the treatment of blank cells.
    '''),
    'docs/format.md': md('''
        # Export format

        The matching key is the pair `item_id` and `location_id`. Identifiers are
        opaque strings: preserve leading zeros and case. Do not convert them to
        numbers or normalize case in an attempt to make matches easier. A blank
        quantity is unknown, not zero. The report keeps that difference visible so
        a reviewer does not mistake missing data for an empty warehouse location.

        The left export determines report column order. A right-side field that does
        not occur on the left is listed after the left-side fields in its original
        order. This keeps comparisons deterministic without hiding fields. Report
        generation does not approve corrections to either ledger. The owner has not
        specified a process for writing corrected values back into an upstream system.
    '''),
    'docs/decisions.md': md('''
        # Decisions

        DEC-71: Owner Lina approved offline operation on September 6, 2026. Keeping
        exports local reduces data movement and allows operators to compare records
        in a disconnected warehouse office. A hosted dashboard was discussed, but
        remains an unapproved proposal pending a concrete need for shared review.
        A working CSV report is sufficient for this iteration.

        DEC-72: Owner Lina approved preserving leading zeros in identifiers and using
        the composite key rather than item identifiers alone. The same item can be
        stored at multiple locations, and numeric coercion can merge distinct records.
        Neither decision establishes accounting policy or grants permission to modify
        the warehouse source system. The tool supplies evidence for human review.
    '''),
    'docs/open-work.md': md('''
        # Open work

        SAMPLE-71 is unresolved: the team needs an approved synthetic export containing
        duplicate item identifiers at different locations. Next action: ask the test
        maintainer to construct that sample without real warehouse records. Until it
        exists, do not claim that the duplicate-location comparison has been verified
        against a representative sample. This is a test coverage gap, not an approved
        change to the matching rule.

        A contributor suggested a browser viewer for discrepancy reports. This is an
        exploratory idea with no owner approval or delivery date. Keep discussion in
        this document until there is a decision worth recording. The existing offline
        boundary still applies. The owner has not requested deployment infrastructure,
        telemetry or a synchronization service as part of the current iteration.
    '''),
}
INIT_ORACLE = {
    'README.md': INIT['README.md'].replace('There is no project context entry point yet.', 'Start with [project context](context.md).'),
    'context.md': md('''
        # Parcel context

        Offline comparison of local warehouse CSV exports for human review; inputs
        remain read-only. [Usage](docs/usage.md) has the command and report workflow.
        [Format](docs/format.md) defines composite identifiers, leading zeros, blank
        quantities and field order. [Decisions](docs/decisions.md) records the approved
        offline scope and matching rationale; a hosted dashboard remains proposed.
        [Open work](docs/open-work.md) tracks SAMPLE-71 and the synthetic sample needed
        before representative duplicate-location coverage can be claimed.
    '''),
}
MAINTAIN = {
    'README.md': md('''
        # Mooring monitor

        Mooring polls a local sensor adapter and stores readings for a pilot operator.
        The repository contains configuration, context and operator guidance. It does
        not contain evidence from the running installation. A configuration change can
        be reviewed here; installation acceptance requires a separate operator check.
        No network service or remote deployment is part of this maintenance request.

        Start with [current context](notes/current.md), then follow [decisions](notes/decisions.md),
        [operations](notes/operations.md) and [open work](notes/open-work.md) as needed.
        The project has an established notes directory. Keep useful historical reasons
        and unresolved work accessible when updating current settings.
    '''),
    'notes/current.md': md('''
        # Current context

        The polling interval is configured to 30 seconds. The value comes from
        [polling configuration](../config/poll.yaml); runtime installation has not
        been verified from this repository. Local storage is the approved pilot
        approach. Read [decisions](decisions.md) for owner authority and rationale.

        The pilot operator reviews gaps rather than treating missing samples as zero
        readings. Sensor identifiers remain strings, including leading zeros, because
        the upstream adapter assigns them. A polling interval change does not authorize
        a change in identifier normalization or the interpretation of missing samples.

        [Open work](open-work.md) tracks restore and calibration blockers. The
        [operations guide](operations.md) contains a hand-maintained restore example
        used by the operator. It should stay canonical so copies do not drift after
        later exercises. Keep this entry point about current state and navigation.
    '''),
    'notes/decisions.md': md('''
        # Decision register

        DEC-81: Owner Sol approved local file storage on September 9, 2026, to avoid
        dependence on a hosted service during the pilot. The pilot site can lose
        network access for hours. Cloud replication remains an unapproved proposal
        until recovery behavior and subscription ownership are decided. A contributor
        demonstration does not change that status.

        DEC-82: Owner Sol approved treating a missing sample as unknown instead of
        zero because zeros would distort later calibration analysis. Operators should
        preserve the gap and investigate its cause. This decision concerns the data
        model, not a promise that the adapter never drops samples. Historical missing
        readings must not be backfilled merely to make a dashboard look complete.
    '''),
    'notes/operations.md': md('''
        # Operations

        ## Restore exercise

        Use the saved source volume for a dry run before touching the pilot data.
        Preserve the directory spelling in the example because the operator's test
        fixture includes a space. An accepted dry run demonstrates only that the
        selected fixture was readable; it does not establish a complete recovery of
        the running installation. Keep the exercise result tied to the source revision
        and volume used, without copying private readings into project documentation.

        ```yaml
        restore:
          retries: 3
          paths:
            - "./data files/pilot.db"
        ```

        Inspect the resulting sample count and identifier preservation before asking
        the owner to accept the exercise. Do not mark RESTORE-81 resolved simply because
        the instructions exist. The blocked volume allocation is tracked in open work.
    '''),
    'notes/open-work.md': md('''
        # Open work

        RESTORE-81 remains blocked on a disposable volume. The operator's next action
        is to request that volume; no restore exercise has been completed. Retain the
        blocker even if the polling interval is updated several times. A configuration
        review does not supply evidence that the volume allocation or recovery happened.

        CAL-82 remains unresolved because the calibration sample lacks a sensor with
        a leading-zero identifier. Next action: ask the test maintainer for an approved
        synthetic sample. Preserve existing samples as evidence rather than rewriting
        identifiers to make the test pass. Neither blocker has an owner-approved due
        date, and no document maintenance request should invent one.
    '''),
    'config/poll.yaml': 'interval_seconds: 60\n',
}
UNCOMMITTED = {'notes/open-work.md': MAINTAIN['notes/open-work.md'] + '\nUncommitted operator note: VOLUME-83 allocation must preserve the sparse-file flag; ask the storage maintainer before reserving the test volume.\n'}
FENCE = '```yaml\nrestore:\n  retries: 3\n  paths:\n    - "./data files/pilot.db"\n```'
CASES = [
    dict(id='wide-release', files=RELEASE, uncommitted={}, protected=['DEC-61', 'DEC-62', 'RESTORE-61', 'wrangler pages deploy dist'], immutable=[], steps=[dict(
        request='Maintain the project context and release guidance so the next operator knows the applicable workflow. Reconcile the supplied sources, preserve useful rationale and unresolved work, and keep the existing layout.',
        updates={}, oracle=RELEASE_ORACLE, rubric=[
            'Both context.md and design.md specifically retire or qualify automatic Git publication and mandatory CI; manual publication with optional CI is current under owner decision DEC-61.',
            'Preserves automation rationale, DEC-62 sample-only content boundary, artifact/rollback constraints and RESTORE-61 volume blocker/next action.',
            'Keeps the September 20 unverified integration note and receipt-storage question unresolved; does not invent runtime checks or treat the newer contributor note as approval.'])]),
    dict(id='mature-init', files=INIT, uncommitted={}, protected=['DEC-71', 'DEC-72', 'SAMPLE-71', 'parcel compare left.csv right.csv --output report.csv'], immutable=[], steps=[dict(
        request='Establish minimal continuity context using the existing project documents, and make it discoverable from the README. Preserve the project layout and supported constraints.',
        updates={}, oracle=INIT_ORACLE, rubric=[
            'Adds a useful README-discoverable entry point or section with supported purpose and navigation to usage, format, decisions and open work; no empty template inventory.',
            'Preserves offline/read-only scope, composite string keys and leading zeros, unknown blank quantities and left-side field order; the relevant details remain reachable.',
            'Preserves owner decision authority/rationale, unapproved hosted/viewer proposals and unresolved SAMPLE-71 with next action; no invented architecture, deployment or verification.'])]),
    dict(id='long-maintenance', files=MAINTAIN, uncommitted=UNCOMMITTED, protected=['DEC-81', 'DEC-82', 'RESTORE-81', 'CAL-82', 'VOLUME-83', FENCE], immutable=['config/poll.yaml'], steps=[]),
]
for i, interval in enumerate([60, 45, 45]):
    CASES[-1]['steps'].append(dict(
        request=('Refresh current context after the polling configuration change. Preserve decisions, rationale, unresolved work and existing uncommitted edits. Do not commit or reset.' if i < 2 else 'No code, configuration, decisions or status have changed since the previous pass. Review current context; edit only for a concrete remaining problem, without bookkeeping-only changes.'),
        updates={'config/poll.yaml': 'interval_seconds: 45\n'} if i == 1 else {},
        oracle={'notes/current.md': MAINTAIN['notes/current.md'].replace('30 seconds', f'{interval} seconds')} if i < 2 else {},
        rubric=[
            f'Current configured interval is {interval} seconds with configuration source; previous values are removed from current state or clearly historical, with no invented runtime verification.',
            'Preserves DEC-81 local storage approval and network rationale, unapproved cloud proposal, DEC-82 unknown-sample semantics, RESTORE-81 and CAL-82 blockers/next actions, and uncommitted VOLUME-83 sparse-file constraint; no commits or resets.',
            'Keeps one coherent current account and the canonical restore YAML/links; no duplicate session diary, speculative new policy or bookkeeping churn.']))
