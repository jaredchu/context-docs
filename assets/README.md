# Brand and README artwork

The November 7, 2026 UI reboot uses original, code-authored SVG artwork:

- [Abstract C mark](context-docs-mark.svg): a solid angular graphite C with a
  detached cobalt terminal, suggesting context carried forward. Filled geometry
  stays readable at favicon size; the white backplate supports light or dark
  browser chrome. This original vector is the current brand mark.
- [Wordmark export](context-docs-logo.svg): the same mark and Context Docs name.
  Website headers use the mark with accessible real text. The wordmark export
  uses system fonts and is intended for light surfaces.
- [Workflow illustration source](context-docs-overview.svg): a technical minimalist
  light diagram showing work, saved project context and a new session reading it.
- [PNG export](context-docs-overview.png): the 1600×840 browser-rendered SVG export
  used by the README and social preview. It is not edited from the prior raster.

The build exposes the canonical mark as `logo.svg`. The tracked site favicon
uses the same exact SVG bytes. No third-party logo, remote font or stock asset
is used. SVG sources remain editable; the PNG preserves compatibility with
GitHub Markdown and social preview consumers.

The workflow is illustrative, not a screenshot or an observed agent recording.
It adds no claim of automatic synchronization, unlimited memory or guaranteed
updates. The agent acts during active sessions and changes need review.

The previous illustration remains available in the
[v0.2.7 release snapshot](https://github.com/jaredchu/context-docs/blob/v0.2.7/assets/context-docs-overview.png).
Its original generation provenance is retained below; it does not describe the
current artwork.

## Earlier illustration (superseded)

The earlier `context-docs-overview.png` was an original conceptual illustration generated with
the built-in image-generation tool on October 10, 2026. It shows work becoming
readable Markdown context that a later session can consult. It is not a product
screenshot or a claim of automatic capture. The README includes equivalent text
and descriptive alt text. The generated image was copied into this repository
without visual edits.

### Original generation prompt

Use case: illustration-story. Asset type: wide hero illustration for the GitHub README of Context Docs, an open-source reusable instruction skill for people who don't know how to save useful project context. Primary request: visitors should understand in seconds that they can ask their coding agent to organize important project knowledge into readable Markdown, then use that document when continuing in a new session. Create a polished, restrained editorial software illustration with three clearly connected stages left to right. Stage 1: a small cluster of chat bubbles, code snippets and decision notes from ongoing work, slightly scattered but not chaotic. Stage 2: one prominent tidy document with a folded corner and a subtle Markdown symbol, three neatly separated rows reading exactly 'Decisions', 'Current state', 'Next steps'. Stage 3: a fresh chat/workspace window visibly consulting that same document, with a simple continuation arrow. Large stage captions exactly 'Work', 'Save context', 'Resume'. Thin directional arrows link stages; same document colors carry through to stage 3. Visual emphasis on human-readable project knowledge and continuity, not a memory database. Style: high quality contemporary editorial illustration, gently dimensional paper and interface cards, precise typography, soft shadows, generous whitespace, calm light background, dark readable labels and restrained teal/blue accent. Wide landscape banner around 1800 by 720, balanced at README width, no tiny text necessary to understand it. No robot mascots, brain icons, cloud servers, company logos, badges, fake terminal commands, guaranteed-correctness checkmarks, automatic-sync symbols, infinite memory claims, photo, or decorative clutter. No extra text other than the exact six labels above. This is a conceptual illustration, not a screenshot of a product UI.

### Historical presentation references

The README organization drew on the workflow introduction and platform-specific
setup in [Superpowers](https://github.com/obra/superpowers), concrete use cases in
[Vercel Agent Skills](https://github.com/vercel-labs/agent-skills), and the concise
skill explanation/examples in [Anthropic Skills](https://github.com/anthropics/skills).
These informed structure; their artwork and prose were not copied. No affiliation
or endorsement is implied.
