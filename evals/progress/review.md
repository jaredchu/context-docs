# Markdown progress validation and review

Development core 0.2.0 / adoption 0.1.10, October 16, 2026. Standard remains 0.1.1.
This is an instruction feature, not a runtime viewer. Installed skills, existing
setups and saved studies are preserved. The earlier webview was a proposal;
this branch began at `5433e47` and introduces no progress web app or server.

## Mechanical validation

- Repository static checks pass after closeout: 1,250 relative links/anchors,
  packaged metadata/versions and five published evidence tables.
- Packaging/static regression suite: 18 tests pass, including omission of the
  progress reference from a standalone package even if its routing link is lost.
- Site regression suite: 12 tests pass.
- Skill-creator validation: both packages pass using the existing
  `.local/validation/bin/python -B`; default/bundled interpreters lacked PyYAML.
  No dependency was installed or existing environment changed.

The [seven progress scenarios](README.md) and [example](../../examples/progress.md)
are authored cases, not executed native behavioral evaluations. These checks do
not establish automatic selection, usability benefits or reliable stall detection.

## Counterpart review and scope

One five-minute Opus 5.5 artifact review via BrowserAct Chrome Direct completed
in about 74 operator seconds, based on retained pre-Send UTC and clock-tool UTC
at capture. Cross-command process-relative monotonic readings were not used as
elapsed time. One Send, no follow-up. The exact 51,179-byte composer readback
matched SHA-256 `9d2dc9375b59aa04113a60065ad5dd43d29d1e57b100d78fdd70c62c7afb881e`.
The UI showed Opus 5.5 High, incognito and Research/Web search off; those observations
are not backend identity or universal tool-enforcement proof. The owned session
closed. No native agent trial ran.

The packet contained the complete core/adoption instructions, progress guide,
synthetic example, original five scenarios, user guide and static-check tests,
plus requirements and a local-check summary. It did not include full README,
changelog or final project-context edits; final static checks cover repository
mechanics only. The complete response and delivery records are retained privately;
the response is reproduced below. This is counterpart artifact review, not an
independent native evaluation.

## Sol dispositions after source inspection

1. **Accepted:** retained dated attempt notes are legitimate history. Added them
   alongside Git/journal sources so the example and instructions agree.
2. **Qualified:** the review's enabled-only journal premise came from Sol's packet
   wording, not the owner's original “existing optional event journal” requirement.
   Existing journal rules preserve records when capture is off and allow reading
   for historical questions. Aligned the guide and progress reference: relevant
   retained records may be read without enabling capture or changing off settings.
3. **Accepted:** user guidance now describes requested/instructed behavior, with
   a validation boundary and review of output rather than guarantees.
4. **Accepted:** adoption now explicitly refreshes the view through core while
   preserving layout/evidence.
5. **Accepted:** preserve findability in existing layouts; write a new view on
   request and refresh an existing view. No universal progress restructuring.
6. **Accepted:** relationships need documented evidence or a clearly labeled,
   cited inference; unsupported dependencies stay out.
7. **Accepted:** an audit asking about repetition may read relevant history;
   every audit remains free of writes/events/settings changes.
8. **Accepted:** clarified absent history, included non-table maintenance, and
   added Git/journal audit and adoption-preservation scenarios. Seven authored
   scenarios are not seven executed tests.
9. **Accepted:** final checks are rerun after closeout. Earlier check counts were
   explicitly pre-closeout, not evidence for later edits.
10. **Scope limit retained:** no old progress webview was implemented in this
    baseline. README/guide now advertise the Markdown feature as unreleased;
    no removal of a previously shipped webview is claimed.

Sol checked and corrected the returned findings. There was no second model review
of the revised text, and no claim that Claude accepted the final revision.

## Complete initial review response

Context Docs progress view: artifact review

This is a static review of the packet. It is not a behavioral validation, and it is not evidence of native skill use.

Material findings

1. The stall-evidence source conflicts with the example and Scenario 1.

Where: references/progress.md § “Assess possible stalls only with history” versus examples/progress.md and evals/progress/README.md §1.
Problem: The guide names only Git history or the optional journal, and says a “current snapshot… cannot by itself establish a loop.” The example and Scenario 1 instead derive a possible stall from retained, dated attempt notes inside the saved context.
Consequence: An agent following the guide literally would report repetition as “unknown” and fail Scenario 1. Alternatively, it might treat dated context notes inconsistently.
Fix: Add “retained dated attempt records in existing context” as an accepted history source, under the same limits.

2. The journal-eligibility wording is inconsistent, which blurs a privacy boundary.

Where: progress.md says “the existing optional journal.” docs/getting-started.md says “an already enabled journal.” The owner requirement says “enabled journal.”
Consequence: A disabled journal keeps its records (per the logging docs). Under the guide’s wording, those retained records could still be read for stall analysis, against the owner’s boundary.
Fix: Change progress.md to “an enabled journal,” or explicitly state the rule for disabled journals with retained records.

3. User docs state unverified behavior as guarantees.

Where: docs/getting-started.md § “Progress in Markdown”. Examples: “No completion percentage, missing goal or live activity is invented,” “It summarizes… rather than introducing a second task tracker,” and “An audit still writes nothing.”
Consequence: The scenarios are authored but not executed. These sentences contradict the skill’s own rule against turning inspected operations into guarantees.
Fix: Reword as instructions, for example “The guidance directs the agent not to…”, and link to the evals’ validation boundary.

4. The adoption skill’s “preserve” conflicts with the core skill’s “refresh.”

Where: adopt-context-docs/SKILL.md says to “preserve an existing view during ongoing maintenance.” The core skill says to “refresh an existing view when relevant facts change.”
Consequence: An agent could read “preserve” as “do not modify,” leaving the view stale.
Fix: Change to “preserve and refresh an existing view through the core skill.”

5. The visualize section’s opening sentence over-scopes the feature.

Where: context-docs/SKILL.md § “Visualize progress in Markdown”, first sentence (“…easy to find during initialization and maintenance”).
Consequence: This can be read as mandating progress restructuring on every initialization or maintenance pass. That risks layout churn and conflicts with “preserve existing layouts” and “no bookkeeping edits.”
Fix: Qualify it: “when documented, keep… findable; write a view only when requested or one already exists.”

6. The guide is ambiguous about inferred dependencies.

Where: progress.md says both “Do not invent… dependencies” and “Label inferred relationships.” The owner requirement asks for dependencies to be shown.
Fix: State that dependencies may appear only when sourced, or as an inference from cited sources and labeled as inferred.

7. The audit-history rule is ambiguous.

Where: The last line of progress.md: “Audit requests remain read-only, including history and settings.”
Problem: The sentence does not say whether an audit asked about looping may read Git or journal history. Scenario 5 only covers the case where no comparison is requested.
Fix: Add one sentence stating whether audits may read history when explicitly asked, and that they write nothing.

8. Several scenarios are missing or underspecified.

Where: evals/progress/README.md.
Gaps:
No scenario performs stall comparison from Git history or an enabled journal.
Scenario 3 does not say whether a Git repository exists, so “repetition remains unknown” may not be the expected outcome.
Nothing exercises the adoption v0.1.10 routing, or an existing non-table progress section, which is the “no rigid layout” requirement.
Fix: State that the Scenario 3 fixture has no Git history and no journal. Add one Git or enabled-journal stall case and one adoption-preservation case.

9. The validation evidence is time-scoped.

Where: The Sol checks report “1241 links/anchors before context closeout.”
Consequence: The link and anchor pass predates the final context edits, so it does not cover the final state.
Fix: Re-run the checks after closeout, or report them as pre-closeout. The remaining claims (18 regression tests, which matches the test file; skill-creator validation needing the project interpreter; scenarios not executed) are appropriately bounded.

10. Webview replacement is not evidenced.

Problem: The owner says Markdown replaces a webview. The packet does not show whether earlier webview docs or code were removed or marked as superseded.
Consequence: I cannot verify this from the packet.
Fix: Confirm in the changelog that no webview remnant is still advertised.
No material issue found
The packaging test for references/progress.md and the portability of the shipped files.
The disclosure of unreleased versions in the guide.
The example’s separation of proposal status from implementation status.
The local-only canary coverage in Scenario 4.
