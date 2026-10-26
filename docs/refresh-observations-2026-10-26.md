# Real-repository refresh observations

October 26, 2026. These are retrospective records of maintainer-operated use in
two existing adopted repositories. They are separate from the
[synthetic v0.2.6 evaluation](../evals/refresh/baseline-0.2.6-2026-10-26/README.md)
and add no trials or scores to it.

## What happened

The owner requested a refresh and a repeat in the Context Docs product repository,
then requested the same sequence in the maintainer's private notes repository.
Codex performed all four interactions in a single ongoing chat. The first
refresh in each repository explicitly read the core skill and project instructions;
repeats retained the same conversation context. No separate fresh agent
session or Claude refresh run was launched for these observations.

| Repository and pass | Observed outcome | Checked scope |
| --- | --- | --- |
| Context Docs: first refresh | Corrected one publication-chronology error in the context summary and progress label; appended the correction to the enabled journal | Context entry point and relevant release/version, decision, evaluation and deployment records |
| Context Docs: repeat after committing the correction | No updates; eight directly checked files had equal before/after SHA-256 values, and Git status stayed clean | Same current-state questions, including the corrected chronology, recorded deployment, skill versions and next actions |
| Private notes: first refresh | No updates; 17 directly checked files had equal before/after SHA-256 values, and Git status stayed clean | Context/index, relevant receipts, local setup and deferred-work/feedback records; 69 local links and anchors resolved |
| Private notes: repeat | No updates; the same 17 checked files remained equal, HEAD stayed unchanged and Git status stayed clean | Same bounded receipt/context/link checks |

The product correction distinguishes the walkthrough's first publication at
`b38853d` from its later cleanup at `ee9211e`. At the time of those refreshes,
the recorded website deployment was `6b1c9d6`. The correction and its journal
entry were subsequently
[committed as d0206d2](https://github.com/jaredchu/context-docs/commit/d0206d2c35a7f11f6c3ab7959cb1320ba214a3de).
The repeat checked that committed state. The error had been introduced during
[earlier Codex-assisted maintenance](https://github.com/jaredchu/context-docs/commit/4b1f202eb4bfed013cc323cfff5b0f0ddcd616a1)
in the same chat; its repair is not an
independent test of recovering unfamiliar drift.

The three no-change passes made no documentation edits, journal entries or
bookkeeping commits. Private logging remained disabled. The present report is
being added later at the owner's explicit request; it does not change those
earlier no-change outcomes.

## Evidence and separation from the synthetic case

The correction's exact diff and journal entry are inspectable in the linked
public commit. The no-change outcomes come from the executed read-side checks,
their terminal results and the interaction history in that conversation. Those commands
computed hashes in memory and asserted equality; per-file before/after manifests
and standalone raw session traces were not saved for these real-repository passes.
This report does not reconstruct or present later hashes as earlier measurements.
The private repository's filenames, content, commit identity and operational
details remain private under evidence ID `real-repository-refresh-20261026`.
The aggregate summary here does not provide independent access to that evidence.

The synthetic case has a pre-run protocol, frozen inputs, exported outputs and
two fresh Codex CLI invocations with the same prompt. These real observations
have none of that experimental isolation: the operator was already familiar with
both repositories and had maintained their context in the same conversation.
The product-repeat and private-repeat user requests explicitly asked to avoid
unnecessary changes; the first refresh requests asked whether updates were
needed. The first and repeat requests were not identical. Do not pool their file counts,
passes or outcomes with the synthetic case's 19-file equality result.

## Limits and interpretation

- The two repositories are related maintainer projects, recently maintained in
  the same chat. They are not independent projects, held-out cases or learner trials.
- Before/after hash assertions cover bounded eight- and 17-file sets, not every
  repository file or the whole duration of each interaction. Clean Git status
  adds a tracked/untracked working-tree check; it does not inventory ignored
  runtime/cache state. The checks were read-side commands with no file-write step.
- The refreshes reconciled stored evidence. They did not rerun deployments, app
  tests, native skill evaluations, platform-policy research or live browser checks.
- There was no ordinary-maintenance/no-skill control, randomized assignment,
  independent scoring or measured user effort, token use or cost benefit.
- Refresh actors are identified as Codex. No independent served-model or effective
  reasoning telemetry was retained for these existing chat turns; the model
  configuration of the earlier synthetic CLI runs does not establish it here.
- No ground-truth defect inventory was defined for either repository. A no-change
  result, including the private first refresh, cannot rule out missed drift.
- The observations record one correction and three bounded no-change passes
  consistent with their requests. They establish no general idempotence, completeness, reliability,
  privacy guarantee, automatic skill selection or skill-specific causal advantage.

Core remains **0.2.6** and adoption **0.1.15**. These results change documentation
and evidence records, not either skill package, and require no new skill release.

## Later review of this record

Claude Opus 5.5 (`claude-opus-5-5`), requested High, reviewed the retrospective
report and one focused follow-up. The review tightened outcome wording, prompt
cue coverage and evidence qualifications; the follow-up found no remaining
material issues within that scope. The reviewer read the report, relevant diffs
and coordinator-labeled excerpts, not the original conversation or saved per-file
manifests. This was a later review of presentation, not a refresh rerun or
independent scoring of the four observations. Review originals and metadata remain
private under the same evidence ID. No effective-effort telemetry was independently
exposed. The added review summary was checked locally.

## Later paired no-change check

Later on October 26, after the evidence-page publication and receipt commits,
the owner requested one more refresh of both repositories, explicitly asking
to confirm no unnecessary changes and to avoid website deployment. Codex carried
out this check in the same ongoing conversation. This is a distinct follow-up
to the four observations above, not an additional synthetic evaluation or a
fresh agent session.

| Repository | Latest bounded hash check | Outcome |
| --- | --- | --- |
| Context Docs | 13 selected files | Equal before/after SHA-256 values; no needed update identified; unchanged HEAD and clean Git status |
| Private maintainer notes | 18 selected files | Equal before/after SHA-256 values; no needed update identified; unchanged HEAD and clean Git status |

The read-side command also checked **120 local links and anchors combined**
across selected entry-point/index text. That is neither a per-repository total
nor a repository-wide crawl. The public context's current-focus section was
included; journal paths were skipped. Saved deployment identities and
artifact/live hash manifests, the recorded 24-site-test result and browser
receipts agreed with the current context. This did not rerun those publication
checks or newly verify live service state. The deployed source recorded by both
repositories remained `a97307e`.

This check wrote no files or journal entries, made no commits or pushes, and
performed no deployment. This subsequent entry is being added at the owner's
separate request to record and push the outcome. Detailed private scope stays
under evidence ID `real-repository-refresh-20261026`.

The results are based on the executed command and its terminal report in that
conversation. Hash vectors were compared in memory around the verification
command and were not saved or printed; no standalone raw session trace was
retained. The counts describe selected sets, not all files or the entire
interaction, and clean Git status excludes ignored runtime/cache state. No
ground-truth defect inventory, control or independent scoring established that
unidentified drift was absent. The explicit no-change cue and familiar shared
chat remain limitations; no benefit or general idempotence is established.
Do not pool these 13/18-file counts or the 120-link count with the earlier
8/17-file, 69-link observations or the synthetic 19-file result. The earlier
Opus record review does not cover this later entry; no new independent review
of these outcomes or this entry was performed.
