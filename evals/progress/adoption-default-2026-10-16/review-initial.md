I found **3 material findings** and 6 minor ones. I read only the packet and made no changes.

## Material findings

**M1. The guidance contradicts itself on whether a status paragraph counts as an existing view.**
- `progress.md` (Adoption section, ¶1) says to "Adapt the relevant status lines in place."
- ¶2 of the same section says "An existing progress view, including a nonvisual view … remains canonical: maintain its location and format instead of … reformatting a view just for adoption."
- The Maple `## Work` paragraph (passed check, blocked check, results link) could be either one. Case 1 treated it as status lines and turned it into a checklist. Case 3 treats grouped bullets as a view that must not be reformatted.
- Nothing in the guidance says where the line falls, so an agent could reformat an owner's existing progress prose, which goes against the owner's request to preserve layouts.
- Suggested fix: one sentence defining the difference. For example, a separately structured or labelled progress section counts as a view; inline status sentences inside a broader section count as status lines.

**M2. The tests only cover re-adopting an already-adopted project, but the claims cover adoption in general. That also strains the "existing setups unchanged" claim.**
- The `protocol.json` fixture already has an equivalent rule and the marker `Adopted: 2026-10-01`, and the run still changed `notes/context.md`.
- So the evidence shows that re-running adoption on an existing setup now writes a view. Fresh adoption was never run: no new rule wording, no new marker, no instruction-file write.
- The CHANGELOG ("adoption creates the inline checklist…") and the main README read as general adoption behavior.
- The CHANGELOG also says "existing project setups … are not upgraded or migrated," yet re-adopting an existing setup does change its context.
- Separately, the guidance never says whether re-running adoption on an equivalent setup with no view counts as a no-edit "repeat". It conflicts with adopt SKILL "Existing equivalent setup may require no changes" and case 6 "Repeat … no edits".
- Suggested fix: state the re-adoption rule explicitly, and limit the evidence claims to "re-adoption of an existing equivalent setup; fresh adoption unexecuted".

**M3. The CHANGELOG says the counterpart review is already recorded, but it is still pending.**
- CHANGELOG core 0.2.2: "Validation and counterpart review are recorded in the [check record]."
- The check record README says "Bounded Opus artifact review is pending."
- Reword this, or update it only once this review has actually been recorded.

## Minor qualifications

1. **Stale next action in `docs/project-context.md`.** The bold Next action still says "validate the supported default-adoption path and everyday refresh," but the tree already marks that `DONE [N]` and lists only review and closeout as `NEXT`. The next action now appears in three places (tree NEXT line, the paragraph, the `## Next actions` section), and the unreleased-status note in about four (Current focus, Current state, source N, README). That is the kind of duplication the owner asked to avoid.
2. **Docs present untested behavior as fact.** `getting-started.md` says "Sparse context … gets no new view or empty scaffold" and "adoption does not add a duplicate." The main README says it "keeps it current … without a second task list." Cases 3–6 have not been run, so these should read as what the guidance directs, not as observed behavior (per the core SKILL's "do not turn them into guarantees").
3. **Unclear scoring attribution.** The check record says "Sol scored these outputs," while `protocol.json` says "author-scored." Pick one wording.
4. **Next action written twice in the adopt output.** `**NEXT:** [Obtain the fixture, then run the check](#next-move)` paraphrases the `## Next move` text. A bare link label like `[Next move](#next-move)` would avoid a second version that could drift.
5. **Status summary inside the evidence file.** The maintain run added "Both documented checks have now passed; the next action is maintainer review…" to `results.md`, which mixes a context summary into the retained evidence. The prompt dictated this text, so it isn't a skill defect, but the record shouldn't count it as good preservation practice.
6. **Case 2 doesn't test the new refresh wording.** The fixture's `AGENTS.md` keeps the old rule, and the core sentence "Refresh an existing view when relevant facts change" predates this diff. Case 2 shows the existing core refresh guidance working on an adoption-created view. It does not show the new maintenance wording having any effect.

Everything else checks out: no conflicts with the local-only, logging, audit or publish/install rules; no extra scaffolding; anchors resolve (`#compatibility`, `#interrupted-write`, `#next-move`); and the owner note, decisions and earlier dated evidence stay intact in both outputs.
