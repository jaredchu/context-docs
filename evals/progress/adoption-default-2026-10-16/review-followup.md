**No material findings remain unresolved.** M1, M2 and M3 are addressed. I found one factual regression that should be fixed before closeout, plus a few precise qualifications. I read only the packet and made no edits.

## Material findings

**M1 is resolved.** `progress.md` (Adoption, ¶2) now draws the line itself. Task lists, status tables, diagrams and designated progress sections or files are kept as they are. Ordinary status sentences in broader context may be grouped in place. When it's unclear which applies, the existing format is kept. Case 1, where the Maple Work paragraph became a checklist, fits this rule. `getting-started.md` says the same thing.
- Small leftover: case 3 calls a "canonical grouped-bullet" view one to preserve. Grouped bullets that aren't a task list or a designated section fall only under the "if unclear, retain" fallback. That still gives the right result.

**M2 is resolved.** `progress.md` ¶4 now states the re-adoption rule: explicit adoption may add a missing view, keeping the existing rule and marker, and a later unchanged repeat makes no edits. This fits case 6 and adopt's "may require no changes." The claims now name the already-adopted fixture and say fresh new-rule/marker adoption wasn't tested. The CHANGELOG now says "setup rules … not upgraded or rewritten" instead of the broader wording.
- **Qualification:** adopt `SKILL.md` still says "If equivalent maintenance guidance and context already exist, add only the missing marker." Read on its own, that conflicts with re-adoption adding a view. It sits in the marker paragraph, so it's most likely scoped to marker handling, but a phrase like "for setup records" would remove the ambiguity.
- **Qualification:** the adopt 0.1.11 CHANGELOG line "does not … change existing setups" is accurate about installation. However, an explicit re-adoption under the new guidance does write to an existing project's context. Consider "does not change existing setups unless adoption is explicitly re-run."

**M3 is resolved.** The initial review is now recorded in the check record, so "counterpart review is recorded" is accurate. The record correctly says this follow-up is pending. Once this follow-up's result is recorded, update the line "One focused follow-up … is pending" there.

## Regression from the fixes (should fix)

**`docs/project-context.md` source N is out of date after the repeat run.** It says "Existing-view, sparse, local-only, **repeat** and audit cases are authored but not executed natively" and "pass two guided native Codex phases." The check record now reports a third session: a clarified-candidate unchanged repeat that made zero edits. The tree line "DONE Guidance, two guided native phases" has the same problem.
- Suggested wording: three sessions, made up of two initial-candidate phases plus one clarified-candidate no-change repeat (nested-checklist branch only). The audit part of case 6 and cases 3–5 remain unexecuted.

## Other qualifications

1. **Mechanical checks have to be rerun before closeout.** The CHANGELOG and check record say in the present tense that packaging/site (18 + 15), validator, link and build checks pass. Per the packet, those ran before the wording clarification and will be rerun. Either keep that timing visible or update the claims after the rerun.
2. **The CHANGELOG doesn't say which candidate the native phases used.** It says "two guided native Codex phases … pass" without mentioning that both ran the version before the clarification, or the later repeat run. The check record does say this. A short "(initial candidate; see record)" would keep the summary from overstating.
3. **The next action is still repeated** in the tree NEXT line and in `## Next actions`, and the bold paragraph now links to them. That's acceptable as summary plus canonical location. The unreleased status still appears in Current focus, source N and the README, which is minor.

Everything else checks out. The scoring attribution is consistent: Sol is named as author and scorer, and nothing calls it independent. The docs describe untested behavior as guidance. The native-evidence qualification in the packet matches the check record.
