# Global skill installation check — 2026-09-28

**Both clients captured the synthetic failure without an extra logging reminder,
but both unnecessarily reread history during no-change maintenance.** Functional
capture and preservation pass in these fixtures; logging efficiency needs work.

Six fresh native sessions used the actual global core 0.1.3/adoption 0.1.5
installations: capture, unchanged maintenance, and read-only investigation in
Codex and Claude. Each disposable no-Git project already had a standing skill rule,
an explicit global skill path, and project-local logging settings. Task prompts
requested ordinary maintenance without naming the skill or asking for logging.
This tests following the standing rule, not unprompted skill discovery.

| Observation | Codex | Claude |
| --- | --- | --- |
| Recorded actual probe failure through global helper | 1 event | 1 event |
| Duplicate events on repeat | 0 | 0 |
| All project bytes unchanged on repeat and audit | Yes | Yes |
| Global package/source/instruction bytes preserved | Yes | Yes |
| Fresh reader recovered staging failure and untested production | Yes | Yes, with wording limits below |
| Unnecessary journal read on no-change maintenance | Yes | Yes |

The events accurately record batch limit 4, synthetic queue-overflow output,
exit 7, recorder and unavailable Git revision. The probe prints fixed output;
it does not operate a queue. Both readers identified this limitation. Separate
projects retained distinct event IDs and separate `.context/events` files.
Claude startup hooks confirmed `CLAUDE.md` loaded and imported `AGENTS.md`.

Claude encountered six guard denials during capture and two during investigation.
The restricted shell blocked compound commands, unsupported listing/status forms
and cleanup. A temporary payload remains in that disposable fixture. Claude's
audit broadly said no other artifacts existed, overlooking that payload; it also
initially described a value tested against a synthetic queue before correctly
explaining the hardcoded script. These qualifications prevent a clean overall
reliability claim. Codex's repeat also read the journal unnecessarily.

[Summary, package hashes and per-stage file hashes](summary.json),
[Codex event](codex-event.json), [Claude event](claude-event.json), and the
[frozen protocol](protocol.md) preserve the inspected results. Task prompts and
final responses are included as text files. Actual CLI versions are in the summary;
Claude reported `claude-sonnet-5`, while the Codex model ID was not exposed.
The [runner](../../event-journal/global-install/run.py) uses the existing native
boundary plus a narrow global-skill read exception. One regression test exercises
six boundary assertions; it passed before model execution. The protocol records
an initial temporary-path alias failure in the control setup.

Raw streams and hook data remain locally in `.local/global-journal-20260928-v1/`
because actual global instructions may contain private context. Published outputs
were inspected and contain synthetic project facts. This is one supervised
trajectory per client, not proof of unrestricted operation, real-world capture
cost, global default enablement or an advantage over Markdown/Git. No skill/runtime
behavior, release tag, global instruction or other project's settings changed.
