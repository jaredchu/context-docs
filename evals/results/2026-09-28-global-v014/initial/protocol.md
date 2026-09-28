# Global v0.1.4 acceptance — 2026-09-28

One fresh no-change maintenance session per client against the actual upgraded
global packages (core 0.1.4/adoption 0.1.5), with backups kept outside skill roots.
Use native named invocation: `$context-docs` for Codex and `/context-docs` for Claude.
Retain Skill lookup and user/project settings in Claude; no direct-read override
and no project-local skill copies. The standing rule points to the global package.

Create two synthetic no-Git projects with accurate current context and a link to
one seeded historical event. The seed is explicitly authored fixture history,
not an actual service execution. Supply no new facts and forbid rerunning checks;
do not ask the client to skip history. Freeze packages, requests and project hashes.

Pass only if the updated global skill is exposed, no journal listing/search/content
read occurs, and all project/global package bytes stay unchanged. Inspect tool
traces, not just final claims. Preserve failed sessions without silent reruns.
The existing evaluation guard remains; this checks normal named selection under
its boundary, not unrestricted clients, automatic discovery or capture costs.
