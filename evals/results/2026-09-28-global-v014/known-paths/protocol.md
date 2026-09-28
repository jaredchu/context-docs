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

The initial Claude slash-prefixed request did not invoke Skill or read SKILL.md,
and it listed/read history. Retain this failure. One separately frozen diagnostic
control asks explicitly to invoke context-docs using the native Skill tool before
the same maintenance request. No file-path injection, disabled skill lookup or
logging reminder is added. This can establish native loading of the updated global
package; it cannot establish reliable slash-only or automatic invocation.
The current official skills documentation recommends checking availability and
rephrasing when a skill does not trigger: https://code.claude.com/docs/en/skills#skill-not-triggering
It does not establish the cause of this observed CLI failure.

The explicit-tool control loaded global 0.1.4 and skipped event contents, but its
broad `Glob *` result included the journal filename. Retain this strict-gate
failure. A new candidate adds two sentences directing no-change maintenance to
known entry-point paths because broad project searches can enumerate history.
Freeze the revised candidate separately and test Codex named invocation and
Claude explicit native Skill invocation once each. This does not rescore the
slash-only failure or establish automatic selection reliability.
