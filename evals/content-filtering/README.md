# Content filtering: offline synthetic checks

Six small [worked examples](cases.json) cover public maintenance, useful personal
paths, an authorized diagnostic derivative, enabled event capture, a no-change
repeat and public adoption. All identities, paths, accounts and events are
synthetic. Each case states its audience, task, source files, proposed writes,
required facts and details to omit. Originals outside the permitted writes stay
unchanged; these examples authorize no changes to real evidence or storage.

Run with Python's standard library:

```sh
python3 -B -m unittest discover -s evals/checks -p 'test_content_filtering.py' -v
```

The [controls](../checks/test_content_filtering.py) run in the existing CI checker
suite without changing its setup. They check retention of decisions, rationale, conditions, uncertainty,
blockers and next actions; source references that survive a moved checkout;
necessary personal/diagnostic paths; and a single meaningful event without routine
bookkeeping. Deliberate negative mutations remove each required fact, restore
incidental details, break links, rewrite protected sources or duplicate events.

These are Sol-authored acceptance examples and offline checker controls. Required
strings express the fixture contracts; they are not a general semantic grader,
secret scanner or implementation of automatic filtering. No native Codex or
Claude skill behavior, automatic loading, privacy guarantee or benefit across
arbitrary projects is established. Existing native audience studies retain their
[original results and limits](../results/2026-10-10-audience/README.md).

## Results — October 19, 2026

- Ten new offline tests pass, including negative mutations for private journal
  sources and plain-text private references, and a journal schema/helper round trip
  in temporary storage. These run alongside the 18 existing static-checker tests:
  28 pass in that CI suite.
- Existing audience controls (19), public-source adoption controls (28), journal
  tests (58), site tests (17), repository metadata/link/version checks and
  whitespace checks pass. No native skill behavior sessions were run.
- The optional skill-creator validator could not start because PyYAML is absent
  from the inspected Python runtimes; nothing was installed to work around it.
  Repository checks independently validate the skill metadata and packaged links.
- Sol authored and checked the examples. Opus 5.5 reviewed the guidance and
  controls with tools disabled. Sol corrected private-reference checker gaps,
  made removal of a retired setup line explicitly authorized in its fixture,
  narrowed an overbroad omission marker and reduced the personal example to a
  next-action edit. The journal fixture now starts with current Markdown already
  reflecting the check, so capturing its event does not leave stale state.
  The one focused follow-up identified missing required fields in the new event
  example. Sol corrected its revision, check provenance and stored timestamp and
  added validation through the actual packaged schema and append/read helper.
  That final correction passed local checks; no further counterpart review was
  requested. There is no claim of counterpart sign-off on the final correction.

Raw counterpart responses and preservation inventories are retained privately
under evidence ID `content-filtering-09afd1f7-ff23-4808-86ee-2d4e6af0a654`.
That identifier does not make the raw evidence publicly accessible or independently
verified. Original studies, installed packages and setup files are outside the
editable scope; this change does not sanitize historical public records.
