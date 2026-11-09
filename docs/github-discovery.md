# GitHub discovery

Reviewed November 9, 2026. The repository's topics, About description, homepage
and README introduction describe the supported workflow and help visitors find
the project. Search ranking, traffic gains and indexing latency are not measured.

## Repository metadata

- Repository: [jaredchu/context-docs](https://github.com/jaredchu/context-docs).
- Homepage: <https://context-docs.com/>.
- Description: “Agent skills for Codex and Claude Code that preserve project
  context, decisions and next steps across AI sessions in plain Markdown.”

The previous description was “A reusable agent skill and Markdown standard for
consistent, current project context.” Topics were empty and the homepage unset.
The updated description names the artifact, supported tools, purpose and format.
The README introduction uses the same terms naturally and links to the website;
installation instructions, examples and experimental qualifications are retained.

## Topic selection

| Topics | Relevance |
| --- | --- |
| `agent-skills` | The repository distributes reusable skill packages. |
| `claude-code`, `claude-skills` | Supported client and its skill ecosystem. |
| `codex`, `codex-skills` | Supported client and its skill ecosystem. |
| `context-management`, `context-engineering` | Maintaining useful context across AI sessions. |
| `knowledge-management` | Preserving decisions, reasons, current work and next steps. |
| `documentation`, `markdown` | The workflow maintains human-readable project documents. |
| `developer-tools`, `ai-coding` | The intended coding-agent workflow and audience. |

All twelve selected names were found in GitHub's topic-search API before applying
them. Existing usage establishes vocabulary, not search demand or likely benefit.
`agent-skills`, `claude-code`, `documentation` and `markdown` had curated topic
descriptions at review time; curation is not a ranking guarantee.

This set is a project-specific selection. GitHub permits up to 20 topics; it does
not require filling every slot. Prefer accurate purpose, ecosystem and format
terms over implementation languages used only by helper scripts. Avoid topics
implying unsupported clients, a hosted memory service, retrieval infrastructure
or an MCP server. Reassess topics when supported capabilities change.

## Maintenance and verification

Repository metadata lives on GitHub, independently of commits. Read the current
metadata before updating it, preserve unrelated settings, and read it back after
the update. The topics REST endpoint replaces the entire list, so reconcile any
concurrent additions before writing. Topic names must use lowercase letters,
numbers and hyphens, with at most 50 characters each and 20 topics total.

GitHub repository search normally checks names, descriptions and topics. README
content can be searched with `in:readme`; exact topic classification can be
checked with `topic:agent-skills repo:jaredchu/context-docs`. A metadata read-back
confirms configuration; a matching search result confirms that query at that
time. Neither establishes higher ranking or increased traffic.

On November 9, API read-back matched the twelve topics, description and homepage;
the homepage returned HTTP 200. Repository searches combining this repository
with `topic:agent-skills`, `topic:context-management`, and `"Claude Code"
in:description` each returned the project with complete results. Static checks
and all 34 site tests passed; all 17 generated website files retained identical
hashes, so this change requires no website deployment.

Keep the README useful: explain the problem and workflow early, use descriptive
links, retain setup and examples, and preserve evidence limits. Keyword lists,
repeated synonyms and unrelated trending topics do not help explain this project.

The existing README artwork provides a visual explanation. GitHub's custom
repository social preview is a separate setting for link sharing; an image in
the README does not establish that the custom preview is configured.

## Sources

- [GitHub: classifying repositories with topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics)
  documents their purpose, public visibility and syntax/quantity limits.
- [GitHub: searching repositories](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories)
  documents the default fields, `in:readme` and `topic:` qualifiers.
- [GitHub: searching topics](https://docs.github.com/en/search-github/searching-on-github/searching-topics)
  describes topic exploration and curated/featured filters.
- [GitHub: repository READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
  recommends explaining usefulness, setup and help, and using relative file links.
- [GitHub REST: repository topics](https://docs.github.com/en/rest/repos/repos#replace-all-repository-topics)
  documents replacement of the complete topic list.
- [GitHub: custom social previews](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)
  describes the separate link-sharing image setting.
