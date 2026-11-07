# Try Context Docs with Reading Queue

This is a short local trial for people who have not used Context Docs before.
We want to learn where the workflow helps and where it is confusing. There is
no pass/fail judgment of you. Ask for help or stop at any point; plan for up to
45 minutes, and it is fine to leave the work incomplete.

Use your existing Codex or Claude Code access. You will need Git, Node.js 22 or
later and npm for the example app. You do not need a Cloudflare account or to
publish anything. Use public example URLs, not private reading data.

1. Tell the coordinator whether you already use saved project notes or memory
   across AI chats, and whether these skills are already installed. The
   coordinator will supply the selected v0.2.6 packages and walkthrough. Preserve
   any existing customized installation; ask for help rather than overwriting it.
2. Work in a disposable checkout of the
   [Reading Queue example](https://github.com/jaredchu/context-docs-example-reading-queue),
   starting from commit `238d1d3c0921d304edc8770ced18355972cb7d64`
   (`tutorial-start`). The coordinator can help verify it. The starter already
   has saved context and a maintenance rule.

   If installation is needed, ask your agent:

   > Install context-docs and adopt-context-docs from jaredchu/context-docs at
   > commit d74e69d3268676cf7eab19d241e8b590ddb1c60a for this example project only.
   > Keep the complete folders side by side in this client's supported project
   > skill directory. Preserve existing installations and customizations; if
   > another version would conflict, report it instead of overwriting or adding
   > a duplicate. Do not change global instructions or settings.

3. Follow the supplied copy of the [local walkthrough](https://context-docs.com/reading-queue/)
   from “Run the starter locally” through “Verify behavior and the saved state.”
   Use its prompts as written where possible. Note any wording you change or
   extra prompts you need. Open the fresh implementation chat when the guide
   asks; do not paste the earlier conversation into it.
4. After verification, before looking at the completed example, open another new
   chat in the same checkout. Send this prompt without the earlier conversation:

   > Read this project's context entry point and its relevant linked sources.
   > State the current goal, what remains unfinished, any blocker and the next
   > useful action. Explain which verification results are established and which
   > remain unknown. Do not edit files or run checks.

5. Tell the coordinator what was unclear, where you needed help, whether the saved
   context was useful and what you would do differently next time. There is no
   need to finish every app check within the time available.

Keep optional logging off. Skip deployment and do not change account settings.
Share only the evidence you agree to share: a redacted prompt, small diff or error
can be enough. Do not send credentials, cookies, account identifiers, private URLs
or unreviewed full chat logs. The coordinator will ask separately before using
identifying information or quotations publicly.
