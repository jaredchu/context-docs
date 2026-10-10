# Local-only behavioral follow-up — 2026-10-10

Core 0.1.8/adoption 0.1.9 were tested in seven synthetic projects per client:
local-only adoption, repeated adoption, tracked migration, ignored-entry discovery,
journal coverage, shared-doc leakage and an existing shared setup. Each client
handled all seven in one session, then audited the repeat case in a fresh session.
These are four bounded native sessions, not fourteen independent trials.

Both clients satisfy all seven mechanical case checks. Both fresh audits preserve
every workspace byte, including Git state. Semantic inspection confirms ignores
were verified before the first local context write, tracked migration remained
unresolved, the requested discovery update retained rationale and blocker, and
the public README update contained only the authorized API fact. Literal canary
checks scan shared files, including untracked files; they do not detect paraphrases.

Codex requested GPT 6.1 Sol with medium effort; its exact responding identity is
not independently confirmed. Claude Code confirmed `claude-opus-5-5`, with medium
effort requested. The [summary](summary.json) records client versions, package and
prompt hashes, acceptance criteria, case gates and execution limits. All fifteen
package files match the released package identities; no skill changed.

## Retained findings and execution failures

- Codex's new adoption context copied the seed's 10-second timeout even though
  the fixture's configuration sets 20. This passes the frozen storage criteria,
  but retains a source-accuracy finding. Claude used 20 and reported the conflicting
  seed value. Both later audits detected the repeat fixture's same stale claim.
- Codex added and verified a whole-directory personal journal exclusion. Claude's
  writes were denied; it reported exposure and captured no event, satisfying the
  fixture's explicitly allowed reporting fallback. This is not a claim that
  Claude completed journal exclusion.
- Opus's harness drafting attempt reached its 240-second bound without a runnable
  patch. Sol prepared the runner; Opus's preflight review found no blocker, with
  timeout wording and journal outcomes reserved for semantic inspection. The
  reviewer compared the assignment's case list, without inspecting the scenario
  README; Sol checked that source separately.
- Claude completed its batch with a successful terminal result, then the runner
  crashed on a string-valued `message` event. Its original CLI exit code was not
  saved. Postprocessing recovered the existing trace; the cases were not rerun.
  A separately frozen parser recovery ran the fresh audit, which exited zero.
  The strict execution aggregate remains false for Claude because the missing
  batch exit code is retained, rather than replaced with an assumed zero. The
  `all_mechanical_pass` aggregate includes that strict execution gate and is also
  false for Claude, despite all seven individual case checks passing.
- The shipped runner now skips non-object message events and saves process
  receipts before parsing. Its regression controls include the observed event
  shape; this runner differs from the original frozen execution source.

## Reproduction and limits

From the repository root, choose a fresh disposable output directory:

```sh
python3 evals/local-only/run_native.py prepare --repo . --out /tmp/local-only-study
python3 evals/local-only/run_native.py run --repo . --out /tmp/local-only-study --client codex
python3 evals/local-only/run_native.py run --repo . --out /tmp/local-only-study --client claude
```

The runner freezes package/fixture hashes, prompts, criteria and checker controls
before execution. It requests subscription-authenticated native CLIs only, rejects
API/provider overrides, uses an isolated Codex home, bounds each batch to 420
seconds and each audit to 120 seconds, and refuses to overwrite a subject attempt.
Claude has prompt/tool constraints rather than an OS sandbox. The commands run a
new study with the repaired runner; they do not recreate the original parser failure.

Sol inspected final artifacts and relevant transcript operations; the Opus
follow-up review is recorded in the summary. Raw traces, initial Git snapshots
and the original frozen runner remain local. This public record is not the complete
executed snapshot. These authored direct-invocation checks establish no general
privacy guarantee, implicit skill selection, automatic instruction loading or
user-effort benefit. Earlier saved studies remain byte-for-byte unchanged.
