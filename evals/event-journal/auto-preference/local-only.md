# Local-only auto logging checks — 2026-10-10

Candidate: core 0.1.8/adoption 0.1.9, unreleased. The owner requested extending an
already selected auto preference to explicitly local-only context inside Git,
preserving settings and verifying ignored, untracked context and journal paths.
This is setup-policy validation, not evidence that JSONL is necessary or that
logging improves handoffs or saves effort.

## Mechanical checks

All 156 relevant tests pass: 31 policy, 27 event-journal, 21 local-only controls,
17 static-checker, 19 audience, 28 public-adoption, 1 original auto-guard and
12 website tests. Repository static checks, both skill metadata validators,
independent sibling-package links/helper execution and the site build pass.

The first drafted helper ran 25 tests with 13 failing assertions: Git rejected its
NUL-output `check-ignore` call without `--stdin`. Codex corrected the invocation
and removed the inappropriate literal-pathspec flag from that command. Real Git
checks then passed. Additional controls cover access failures, malformed output
and effective Git exclusions without editing personal configuration. A new invalid
case-config test initially expected a detailed local-only error; actual Git fails
earlier in detection, returning unchanged logging with `git: unknown`. Its expected
result was corrected and all 31 final policy tests pass.

## Bounded native sessions

Each client received isolated synthetic projects, copied candidate packages and
instructions to read the skills directly. Acceptance and all starting file hashes
(including Git files, instructions, context and legacy journal bytes) were frozen
before execution. Only a legitimately eligible project's `AGENTS.md` could gain
`Event journal: jsonl`; all existing lines, paths, dates and records had to survive.
No setup event, journal migration, new log or ignore-rule edit was permitted.

| Candidate stage | Client/model | Execution and preservation |
| --- | --- | --- |
| Before review fixes: setup in seven projects | Claude Code 2.1.296 / confirmed Opus 5.5 | Passed; only eligible instructions gained one setting |
| Before review fixes: setup in seven projects | Codex CLI 0.162.0-alpha.17.2 / requested GPT 6.1 Sol | Passed; only eligible instructions gained one setting |
| Before review fixes: repeat/no-change maintenance and separate audit | Same Claude client/model | Passed; no file changes |
| Before review fixes: repeat/no-change maintenance and separate audit | Same Codex client/model request | Passed; no file changes |
| Final packages: fresh setup in nine projects | Same Claude client/model | Passed; only eligible instructions gained one setting |
| Final packages: fresh setup in nine projects | Same Codex client/model request | Passed; only eligible instructions gained one setting |

Setup cases: eligible ignored local-only storage, explicit off, explicit jsonl,
unignored journal, tracked context despite ignore rules, shared Git context and
no selected preference. A separate audit project remained untouched. Final setup
also included a tracked case alias and an empty journal whose future JSONL files
were re-included by a negated rule. Both clients refused auto for those two cases.
Relevant helper output and final summaries were inspected separately from the
byte-preservation gate. Storage checks can enumerate names; no journal content
was needed. The repeat/audit result is for the earlier package snapshot; final
helper fixes received fresh setup sessions and separate regression tests.

## Review and limits

Exact Opus 5.5 drafted the helper/tests within a 240-second bound; Codex integrated
and validated them. One separate 120-second diff review found a real macOS case
alias gap and missing site unreleased/version labeling. Codex reproduced the gap:
tracked `Notes/old.md` was missed when `notes/` was selected. The fix rejects
existing spelling/normalization aliases and uses case-insensitive literal index
queries when Git's `core.ignorecase` is true. Controls include deleted tracked
targets. Ordinary, JSONL and lock probes address dot-only and suffix-negated rules.
One focused 90-second follow-up found the findings resolved and no remaining
blocker. Its minor status-fallback concern was fixed and locally tested.

These are authored, constrained direct-invocation fixtures. They do not establish
implicit skill selection, automatic instruction loading, independent user benefit,
privacy guarantees or behavior across all platforms/layouts. Known new targets
still need explicit checks; sampled future paths cannot predict every negation.
Git's handling of absent Unicode-normalization aliases is not exhaustively tested.
Arbitrary shell `GIT_CONFIG_COUNT`/`PARAMETERS` overrides are intentionally removed;
normal global/system config locators are honored. Large directory walks are unbounded.
Raw transcripts, frozen fixtures and runners remain outside the repository; this
public summary is not a complete executable reproducer. Existing saved study files
and project setup are preserved separately against their pre-change hashes.

## Final native package identities

Paths are relative to `skills/`; both final native clients used these bytes.

| File | SHA-256 |
| --- | --- |
| `context-docs/SKILL.md` | `d71abe3ac4a88185fcaee666899e568a7797d16a086ecc0564ca5366dd24dfb3` |
| `context-docs/VERSION` | `76f81f64ece28d0bcfe39dd35f6d14f3c87fe000b77aee11561e18d1919f607e` |
| `context-docs/references/event-journal.md` | `e721c1ca877c039dedcb2ca3e032f353b229c808c0d99e33948ba20fbf7ee254` |
| `context-docs/references/local-only.md` | `5ce5e7064e4f24ec084dd80298b3a2b20b28f5005fc8ede0774ad0dd5c504b43` |
| `context-docs/scripts/journal_policy.py` | `b6b390ec4ae6958252e1899fb42fe1f20bac947325675754a7707ac8f9cde445` |
| `adopt-context-docs/SKILL.md` | `73d9520415566b26027337305274f5b95533825168cdd2444084d840f85d713d` |
| `adopt-context-docs/VERSION` | `e358d84552808a5c0bd6679d690c283b938ebe15c2bd843c898681d093213107` |
