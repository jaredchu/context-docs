# Landing page

A static introduction for prospective Context Docs users. The Python standard-library
build reads installation commands and save/resume/progress prompts from the root [README](../README.md), before/after
content from the [maintenance example](../examples/maintenance.md), and package
versions from their `VERSION` files. Edit those sources for shared content; edit
[index.html](index.html), [styles.css](styles.css) and [main.js](main.js) for presentation.

## Build and preview

From the repository root:

```sh
python3 -m unittest discover -s site -p 'test_*.py'
python3 site/build.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory .local/site-dist
```

Open `http://localhost:8000`. Both installation sections remain available without
JavaScript; JavaScript adds agent selection and copy buttons. Clipboard failure
selects the text and gives manual-copy instructions. No external fonts, analytics,
tracking, cookies or application backend are included in the repository build.
Live delivery also has the owner-retained Cloudflare analytics injection described
in [Latest deployment](#latest-deployment).

The working build contains seventeen explicitly allowed public files: eight HTML
pages (seven canonical routes plus the old Reading Queue redirect fallback), six
assets, `robots.txt`, `sitemap.xml` and the empty `.nojekyll` marker. The canonical
routes are `/`, `/getting-started/`, `/compare/`, `/examples/`,
`/examples/reading-queue/`, `/examples/switching-codex-claude/` and
`/examples/switching-claude-codex/`. The old `/reading-queue/` is excluded from the
sitemap. The `.nojekyll` marker dates from GitHub Pages hosting; artifact upload
omits it, so sixteen files are deployed. `build.py` renders every page before replacing the output, so a missing
or invalid new template leaves the previous artifact intact.
The [brand artwork](../assets/README.md) provides the canonical logo mark,
same-byte favicon and the SVG-authored workflow illustration. Selected asset
bytes are copied without transformation. The build
replaces its disposable output directory to prevent stale files being published.
It never copies the repository, context docs, journals, or evaluation exports.

The [comparison page](compare.html) is the canonical copy for the October 24
[research and fit preview](../docs/context-management-comparison.md). It uses the
shared stylesheet, requires no JavaScript, and links primary sources. The
sitemap includes `/compare/`; the landing page and guide link to it. The owner
authorized publication after preview preparation; the page is now
[live](https://context-docs.com/compare/) from the deployment recorded below.

Near “What you get,” the landing page also shows the three fenced blocks from
the [public demo source](../docs/outreach-v0.2.5.md): fictional work notes,
saved context and a fresh-session prompt. Edit that source to change the example;
the build escapes its text and publishes only the selected demo blocks. Draft
posting copy is retained in local operator notes.
The page labels it illustrative rather than an executed session or evaluation,
retains the experimental limits, and links to installation and evidence.
The workflow includes this public source in its build path filters. When this
was published, deployment was manual; see [Deployment](#deployment) for the
current main-branch auto-deploy.

The demo was deployed from `d8c624c` on October 19, 2026. The
[deployment record](../docs/website-demo-deployment-2026-10-19.json) verifies all
eight served files against the build and desktop/mobile rendering with JavaScript
disabled. No installed upgrade or new agent evaluation was part of deployment.

Both pages also show the text tree from the public [progress example](../examples/progress.md),
with clickable source links outside the diagram. The build extracts its canonical
fenced block; it does not read project context or study outputs. The diagram scrolls
within its box on narrow screens to preserve branch alignment.

The v0.2.3 copy explains concise overviews with linked evidence, retaining
meaningful outcomes, decisions, blockers, approval boundaries and existing layouts.
Both pages retain default inline adoption and everyday maintenance, and state the
qualified smoke result: Codex created and removed an extra temporary hash file,
failing strict write scope. Published v0.2.3 notes retain that qualification.
Explicit progress prompts remain optional; installation/upgrade alone changes no
project context.

The v0.2.4 release adds clear, direct sentences and consistent project terms within
authorized context edits, preserving conditions, uncertainty, rationale, evidence,
layouts and unrelated owner text without ASD-STE100 compliance. Both pages link
the release notes and previous v0.2.3 notes. They retain
the clarity smoke qualification: saved Markdown passes in both clients, while
Claude's final chat report adds an unsupported pronoun. These guided checks do
not establish comprehension gains or automatic everyday application. The
[preparation record](../docs/releases/v0.2.4-validation.json) records local checks
and previews with its original draft scope. The [publication record](../docs/releases/v0.2.4-publication.json)
confirms deployment from `73b15ac` and eight matching live public resources,
including released labels and the smoke qualification. Live verification checks
response bytes and metadata, not new browser rendering or user benefit.

The v0.2.5 release adds conditional shared-file coordination to both pages: assign
one writer before concurrent edits, hand ownership over explicitly, prefer narrow
edits and reread/reconcile after conflicts. It provides no locking or automatic
merge guarantee. Both pages retain Claude's second-mismatch reread failure and
Codex's corrected read-only checking error, without claiming simultaneous-write
safety. The [release notes](../docs/releases/v0.2.5.md) retain both qualifications.
The [preparation record](../docs/releases/v0.2.5-validation.json) keeps its original
draft scope and local previews. The [publication record](../docs/releases/v0.2.5-publication.json)
confirms deployment from `89c91f4` and eight matching live resources on October 18.
The uploaded artifact omits the empty `.nojekyll` marker; all eight served files
match the release build. Publication adds no installed upgrade or new native trial.

The v0.2.6 website update adds metadata selection, portable references and
less routine bookkeeping while preserving useful local knowledge and diagnostic
conditions. Both pages link the [release notes](../docs/releases/v0.2.6.md), retain
the previous v0.2.5 link, and show released experimental labels. The
[qualified smoke](../evals/content-filtering/smoke-0.2.6-2026-10-19/README.md)
passes visible saved-Markdown checks; Claude could not locate the unlinked private
note, so its incoming-note filtering remains untested. No automatic redaction,
secret scanner or general privacy guarantee is claimed. The
[preparation record](../docs/releases/v0.2.6-validation.json) owns local build and
preview checks with their original unpublished scope. The
[publication record](../docs/releases/v0.2.6-publication.json) verifies release and
deployment from `d74e69d`; all eight live public files match that build. Verification
checks HTTPS bytes and metadata, not a new live-browser rendering or agent trial.

The [getting-started template](getting-started.html) owns the beginner walkthrough.
Its installation commands, save/resume/progress prompts, synthetic example and versions
come from the same canonical sources as the landing page. The detailed
[installation reference](../docs/getting-started.md) remains in the repository;
the site's refresh, local-only setup and auto-logging prompts are extracted from its public
sections. The site links to it for client settings, upgrades and logging details.
Repository context, local notes and journals never become build inputs.

## Examples collection and directed switching

The [examples index](examples.html) introduces three walkthroughs. The existing
[Reading Queue source](reading-queue.html) is served at `/examples/reading-queue/`
with its original IDs and prompts. New, separate templates serve
[Codex → Claude Code](switching-codex-claude.html) and
[Claude Code → Codex](switching-claude-codex.html). They reuse the Reading Queue
application and its dedicated `switching-start` teaching snapshot; no new hosted
application or dependency is required.

The [example record](../docs/switching-agents-examples.md) owns teaching scope;
the [cross-client record](../evals/handoff/2026-11-07-cross-client/README.md) owns
actual native outcomes and limits. Static/build/browser checks are separate from
those native sessions. The public build never copies the evidence tree.

The old route builds a canonicalized script/meta-refresh/link fallback. Its
script preserves query and fragment. A true HTTP 301 requires the separately
managed Cloudflare Single Redirect: the build emits no `_redirects` file, which
the former GitHub Pages host did not interpret either. The edge rule stays in
place with the Workers Static Assets host. The requested edge rule matches only `/reading-queue` and
`/reading-queue/` on the canonical host, targets the new URL with status 301 and
preserves the query string; the browser retains a fragment when Location supplies
none. Apply it only after the new destination is live. The latest deployment
record owns whether that rule is actually applied and verified.

## Runnable Reading Queue example

The [Reading Queue template](reading-queue.html) is the canonical website
walkthrough for the [separate runnable example](../docs/reading-queue-example.md).
It includes nine copyable prompts with expected results and checks. Adoption
names the skill; later prompts are ordinary work requests. The guide links to
the actual starter/completed Git snapshots, app source and demo, distinguishes
application checks from agent evidence, and keeps cloud deployment optional for
learners. Workers and D1 belong to that app, not to Context Docs.

The public build serves the walkthrough at `/examples/reading-queue/` and lists
that canonical URL in the sitemap. The old `/reading-queue/` URL returns HTTP 301
on the public site; its static fallback remains in the artifact and outside the
sitemap. The build reads only the authored public template for this page, never
the example workspace, private operator notes, project context or native-run logs.
Both existing entry pages link to the moved walkthrough. The owner authorized
its original publication after validation; the walkthrough is now
[live](https://context-docs.com/examples/reading-queue/) from the
[latest verified deployment](#latest-deployment).

## Targeted cleanup preview

The October 25 working-tree cleanup follows the
[comparison and UI/UX review follow-up](../docs/context-management-comparison.md#review-follow-up-preview).
It keeps the existing visual system, fixes guide navigation and mobile heading
spacing, clarifies comparison overlap/operating limits, and makes detailed
release qualifications optional during first use. Synthetic inputs, historical
evidence, installation commands and skill versions stay authoritative in their
existing sources. The owner subsequently authorized deployment from `c2414d4`;
the cleanup is now live. The preview checks below retain their original scope.

All 20 site tests and repository static checks pass. Desktop/mobile Chromium
checks cover the three pages, keyboard disclosure/fragment access, separate guide
links, copy feedback and no-JavaScript installation. No page-wide overflow or
JavaScript errors were observed at 1440×1000 and 390×844. These are local
mechanical/rendering checks, not an accessibility certification or user study.
Detailed review originals, disposition and before/after evidence are retained in
private notes under evidence ID `website-review-2026-10-25`. The later deployment
is recorded below; Cursor support and native testing remain postponed.

## October 26 comparison and example preview

The [review follow-up](../docs/reading-queue-example.md#october-26-review-follow-up-preview)
selects a local preview of targeted content, navigation and tutorial clarifications.
The comparison links directly to the runnable example, and the guide preserves
ordinary prompts while clarifying audit checks, native-memory conditions, historical
case scope and optional deployment. Existing visual design and the mobile table
remain; broader restructuring awaits learner feedback.

All 22 site tests and repository static checks pass. Local Chromium checks pass
at 1440×1000 and 390×844 for the new routes, all nine prompt copy handlers
(clipboard stubbed), step anchors, no page-wide overflow and no observed JavaScript
errors. The walkthrough and direct example link remain accessible without
JavaScript. Only the comparison and walkthrough HTML build outputs changed.
Original reviews, before/after browser evidence and preview receipts belong in
private notes under evidence ID
`website-review-2026-10-26`. The owner subsequently authorized website-only
deployment from `ee9211e`,
completed and verified below. The preview record retains its original scope;
installed skills and the example app are unchanged.

## Local evidence consolidation preview

The owner requested consolidating refresh evidence and adding a no-change stop
rule after independent commit reviews identified repetitive recording/publication.
The guide now has a compact summary linking the separate, unchanged synthetic
study and retrospective maintainer record. Existing evidence fragment URLs still
resolve. The homepage no longer promotes the latest unchanged check. Navigation
and public-source checks replace tests that required observation counts, exact
qualifier text and separate bookkeeping sections.

This was prepared and validated locally before the owner authorized deployment
from `e8ace0c`, now verified below. Original study records, historical receipts,
private evidence and skill packages remain intact. The project
[refresh boundary](../docs/project-decisions.md#refresh-recording-and-publication-boundary)
owns the stop rule.

## Technical minimalist UI reboot

The owner requested a full website UI/UX and identity reboot, including the logo,
favicon and README visual, using a technical minimalist light theme. The redesign
uses a cohesive near-white/white, graphite and cobalt system across
all four routes: sharp typography, thin rules, light code panels, an abstract C mark and responsive navigation. The earlier approachable story, simpler
steps, earlier setup and optional detailed examples are retained.

The [brand assets](../assets/README.md) include editable original SVG sources and
a 1600×840 PNG export for the README/social image. The canonical mark and favicon
match byte-for-byte. The build serves only thirteen explicit public files. The banner/wordmark SVG
masters, project context, journals and private review material are not copied.
Copy-button clearance uses a class applied during enhancement and preserves the
no-JavaScript baseline. The site workflow includes the new canonical mark in
both pull-request and push path filters, so later logo changes receive build checks.

The initial reboot passed static checks and 25 site tests. Local Chrome checks cover four routes
at 1440×1000, 900×1000, 390×844 and 375×812: logo loading, light theme, no page-wide
overflow or observed JavaScript errors, installation/copy behavior, disclosures,
reduced motion and no-JavaScript setup. All nine Reading Queue prompt controls
also pass pointer/copy checks at desktop and mobile sizes, with a stubbed
clipboard. The SVG banner, wordmark and 16/32px icon renders were inspected.
These are local functional/visual checks, not full accessibility conformance,
cross-browser certification or measured comprehension/conversion gains.

A counterpart review of brand/build integration found no blocker. Minor diagram
path and label refinements were applied and checked locally afterward. Detailed
implementation/review receipts are retained privately under evidence ID
`ui-reboot-2026-11-07`. The earlier review originals and artifact provenance
remain preserved in their original records.

The owner authorized committing, pushing and deploying this UI reboot on
November 7, 2026. The redesign is now deployed from `92042e9`; the
[latest deployment](#latest-deployment) retains its source and verification.
Skills, package versions and canonical examples are unchanged.

## Consistent SVG icons

The current brand uses an abstract C in the header, favicon, wordmark and
README illustration: a solid angular graphite shape with a detached cobalt terminal.
UI arrows, document
icons, disclosure controls and copy/success states use **Tabler outline 3.50.0**.
Eight original SVGs and their MIT license are [vendored locally](vendor/tabler/README.md).
The build embeds selected SVGs with `currentColor`, decorative accessibility
attributes and text labels; it ships `tabler-icons-LICENSE.txt` as the thirteenth
explicit artifact. Canonical code, prompts and Markdown diagrams retain their symbols.
There is no icon font, CDN, runtime library or package-install step.

The selection considered [Lucide](https://lucide.dev/),
[Heroicons](https://heroicons.com/), [Tabler](https://tabler.io/icons),
[Phosphor](https://github.com/phosphor-icons/core),
[Material Symbols](https://developers.google.com/fonts/docs/material_symbols) and
[Font Awesome](https://docs.fontawesome.com/web/). All offer SVG delivery.
Tabler's consistent 24px grid, outline strokes and broad catalog fit this site's
technical light theme; Phosphor's multiple weights and Material's variable axes
are not needed here. This is a project design choice, not a universal ranking.
The original package archive's SHA-512 integrity was checked before extracting
only the selected files. Updates require deliberately changing the pinned sources.

The refresh passes static checks and all 27 site tests. Local Chrome checks cover
all four routes at four viewport sizes, mobile navigation/keyboard interactions,
all nine walkthrough copy controls, and copy/disclosure icon states without an
icon runtime. A focused review caught a tablet arrow-direction mismatch; its fix
was confirmed by a focused source follow-up and browser assertions at
1440, 981, 980, 900, 800 and 390px. The arrow rules now share the card-stacking
media block. These checks do not establish cross-browser certification.

The icon refresh is part of the owner-authorized redesign deployment and does
not change the published skill release. Evidence ID:
`icon-refresh-2026-11-07`.

## Approachable homepage preview

This narrower preview is now incorporated into the broader
[technical minimalist UI reboot](#technical-minimalist-ui-reboot).

The owner requested a live/project currency check and fewer technical barriers,
especially on the homepage, with a lively attractive presentation. Fresh checks
on November 7 confirm that the existing live site matches committed source
`ede9d67` (deployed build `00c4b51`), apart from the retained edge analytics script.
This is presentation work, not a repair of missing release deployment.

The local preview puts a readable fictional handoff before short workflow steps
and earlier setup. Longer code examples stay available in native disclosures;
canonical prompts, examples, evidence links, old anchors and no-JavaScript setup
remain. The guide gets a direct setup action. The comparison adds a current-release
bridge while preserving its dated reviewed versions and research limits. Existing
visual identity and assets stay; there are no new dependencies or runtime services.

Static checks and all 24 site tests pass. Fresh local Chrome checks cover all four
routes at 1440×1000 and 390×844, entry-page controls, stubbed copy feedback,
no-JavaScript installation and reduced motion. A focused check confirms keyboard
Space toggling, automatic reveal of a previously closed demo through its source
fragment, and no page-wide overflow when expanded. New label contrast ratios
exceed 4.5:1; this is not a full accessibility audit. No measured comprehension
or conversion improvement is established. Two independent model reviews and one
focused counterpart review are retained privately under evidence ID
`website-review-2026-11-07`.

The initial preview was local and uncommitted; subsequent publication authorization
covers the broader redesign above. Skills, versions, frozen examples and
historical evidence are unchanged.

## Workers Static Assets migration (prepared)

On November 9, 2026, the owner authorized moving `context-docs.com` from GitHub
Pages to Cloudflare Workers Static Assets with automatic deployment from `main`.
The repository now contains the asset-only Worker configuration
([wrangler.jsonc](../wrangler.jsonc)) and the updated
[landing-page workflow](../.github/workflows/site.yml); see [Deployment](#deployment).

**Status: prepared, not yet live.** No Worker deployment, DNS change or live check
has been recorded here. The coordinator owns credentials, the cutover and live
verification of canonical HTTPS, the `www` redirect, the retained Reading Queue
301 and analytics. Until a verified receipt replaces this note, the
[latest deployment](#latest-deployment) below is the last served release, from
GitHub Pages.

## Latest deployment

The creator attribution correction is live from **`c8bc929`**, published
November 9, 2026 by [Pages run 42559064156](https://github.com/jaredchu/context-docs/actions/runs/42559064156).
All seven canonical page footers link Jared Chu to his canonical CV at
<https://cv.jaredchu.com/>, matching his other project websites. Project-source
links, contribution credits, public copy and installable packages are unchanged.

All 34 site tests and static repository checks pass; both source CI workflows
and the manual build/deploy jobs succeeded. The sixteen uploaded files match the
pinned seventeen-file build (empty `.nojekyll` omitted). All fifteen canonical
live resources match exactly, and the legacy Reading Queue 301 preserves its
query. This verifies the URL correction and served files, not a new agent study
or browser-layout audit. Private evidence ID: `context-docs-creator-link-2026-11-09`.

### Earlier examples collection deployment

The examples collection is live from **`e38fede`**, published November 7, 2026 by
[Pages run 42375161164](https://github.com/jaredchu/context-docs/actions/runs/42375161164).
Both source CI workflows and the manual build/deploy jobs passed. The seven
canonical routes include the examples index, moved Reading Queue and two directed
switching walkthroughs; the old URL is a compatibility route.

All **sixteen uploaded files** match the pinned seventeen-file build by SHA-256
(the empty `.nojekyll` marker is omitted by upload). Eight non-HTML live resources
match exactly. Seven canonical HTML pages and the legacy fallback, checked before
the edge rule, match after removing only the previously approved Cloudflare
analytics beacon and inserted newline. The analytics configuration is retained.

Using the authenticated **cf CLI**, one Cloudflare Single Redirect was added after
the new destination was live. `/reading-queue/` and `/reading-queue` now return
**HTTP 301** to `/examples/reading-queue/`; query preservation passes three HTTP
checks, and Chrome verifies the original `#resume` fragment remains usable.
No DNS or unrelated Cloudflare setting was changed. The static compatibility page
remains in the artifact for direct-origin/fallback access.

Fresh local and live Chrome checks pass at 1440px and 390px across all seven
canonical routes, plus legacy-query/fragment and no-JavaScript index checks
(**sixteen checks per site run**). Branding/assets, canonical links, navigation,
no page-wide overflow and all copy controls are checked; clipboard writes were
stubbed. Static checks and **34 site tests** pass. The separate
[native case record](../evals/handoff/2026-11-07-cross-client/README.md) owns the two
implementation continuations and their qualifications; website checks do not add
agent outcomes or establish comparative benefit.

Reading Queue's `switching-start` tag is public at `ed3a02a`; its main documentation
is updated at `50ad018`. Original tutorial tags, live app deployment, skills and
installed packages are unchanged. Detailed private receipt/evidence ID:
`examples-implementation-2026-11-07`. A following record-only commit does not replace
the deployed SHA or require another deployment.

### Earlier website redesign deployment


On November 7, 2026, the owner authorized committing and deploying the full
website redesign and logo changes. The
[Pages workflow](https://github.com/jaredchu/context-docs/actions/runs/42356590439)
built and deployed `main` at **`92042e9`**. Both source CI workflows and the
manual build/deploy jobs passed. The commit retains normal human authorship
and credits Codex and Claude for implementation, validation and review.

The technical light theme, simpler introduction/setup, abstract C identity,
consistent Tabler SVG icons and README artwork are live. All **twelve uploaded
files** match the pinned thirteen-file build by SHA-256; upload omits the empty
`.nojekyll` marker. Eight non-HTML live resources match exactly, including
`logo.svg`, `favicon.svg`, the README PNG and Tabler's MIT license. Each of four
HTML pages matches exactly after removing only the previously approved
Cloudflare analytics beacon and its inserted newline. The owner chose to keep
that edge injection; no Cloudflare setting was changed.

Fresh Chrome checks at 1440×1000 and 390×844 pass on all four routes: light theme,
loaded branding, canonical URLs, no page-wide overflow or observed JavaScript
errors. Homepage/guide checks also cover published v0.2.7 install pins, client
selection, stubbed copy feedback, native disclosures and no-JavaScript setup.
The repository passes static checks and 27 site tests. These are publication and
rendering checks, not OS clipboard validation, cross-browser certification or
new agent evaluations. Detailed receipt: private evidence ID
`website-redesign-deployment-2026-11-07`.

The deployment source stays `92042e9` when a later record-only commit advances
`main`. Final public artifact paths and hashes are unchanged by the record update,
so no second deployment is required.

### Earlier v0.2.7 release deployment


On November 7, 2026, the owner separately authorized website deployment for the
v0.2.7 release and required the site to be current with the repository. The
[Pages workflow](https://github.com/jaredchu/context-docs/actions/runs/42348936504)
built and deployed `main` at `00c4b51`; both jobs passed. All ten uploaded public
files match the eleven-file repository build, which includes an empty `.nojekyll`
marker omitted by artifact upload. The live release labels and install commands
select core 0.2.7/adoption 0.1.16 at tag v0.2.7.

Six non-HTML resources match live bytes exactly. Each of four live HTML pages
adds exactly one Cloudflare Web Analytics beacon outside the repository; the
remaining HTML matches the build exactly. The owner chose to **keep it and record
the difference**, so no Cloudflare setting was changed. The repository adds no
analytics code, but live delivery includes this edge-injected script. This
qualification supersedes any blanket claim that the deployed site has no analytics.

Fresh Chrome checks pass on all four routes at 1440×1000 and 390×844: no page-wide
overflow or observed JavaScript errors, correct canonical URLs, released versions
and tag pins. Homepage/guide checks cover client selection, stubbed clipboard
feedback, evidence disclosure and installation with JavaScript disabled. These
checks do not validate the OS clipboard or agent behavior. The
[publication record](../docs/releases/v0.2.7-publication.json) owns hashes, exact
source and limits. Private evidence ID: `publish-v0.2.7-2026-11-07`.
Record/context commits do not replace this deployed SHA or require another
publication when the resulting public output is unchanged.

### Earlier deployment: October 26, 2026

On October 26, 2026, the owner-authorized [Pages workflow](https://github.com/jaredchu/context-docs/actions/runs/40277604859)
built and deployed `main` at `e8ace0c`, publishing the evidence consolidation
and routine no-change stop guidance. Both jobs succeed; all 24 pinned site tests
pass. All ten uploaded and served public files match the pinned build by SHA-256;
the upload omits the empty `.nojekyll` marker as before. Canonical/Open Graph,
sitemap and robots metadata match. Only the homepage and getting-started output
changed from the previous deployment.

Fresh live Chrome checks at 1440×1000 and 390×844 pass for homepage navigation,
the compact qualified summary and separate source links, stop guidance, three
legacy fragment URLs, canonical prompt and stubbed copy feedback. No page-wide
overflow or JavaScript errors were observed; evidence and prompt remain accessible
without JavaScript. These are publication/rendering checks, not new refresh
outcome scoring or user-benefit evidence. Detailed receipt: private evidence ID
`website-deployment-2026-10-26-e8ace0c`. The requested task ends after the receipt and
context updates; no additional refresh or publication cycle is selected.

## October 26 paired-refresh evidence deployment

On October 26, 2026, the owner-authorized [Pages workflow](https://github.com/jaredchu/context-docs/actions/runs/40270565743)
built and deployed `main` at `a0e636c`. The homepage links to the guide's
[latest paired no-change check](https://context-docs.com/getting-started/#paired-no-change-refresh-results).
Its 13/18 selected-file checks and 120 combined links remain separate from the
earlier 8/17-file, 69-link observations and the synthetic 19-file evaluation.
Visible limits retain the familiar same-chat setup, explicit no-change cue,
bounded selected sets, missing saved hash vectors/raw traces, ignored-state
exclusion and lack of ground truth/control/independent scoring. No general
idempotence or benefit is established. Private filenames/content remain unpublished;
skill packages and original refresh/study records are unchanged.

Both build and deploy jobs succeed, and all 24 pinned site tests pass.
All ten uploaded and served public files match the pinned build by SHA-256;
the upload omits the empty `.nojekyll` marker as before. Only the homepage and
getting-started HTML outputs change from `a97307e`. Four canonical URLs,
existing Open Graph URLs, sitemap URLs and the robots sitemap reference match.

Fresh live Chrome checks at 1440×1000 and 390×844 pass for both homepage evidence
links, all three sibling evidence sections and source links, visible scopes and
limits, private-scope exclusion, canonical refresh prompt and stubbed copy feedback.
No page-wide overflow or JavaScript errors were observed. The prompt and all
three evidence sections remain accessible without JavaScript; no host clipboard
write occurs. Opus 5.5, requested High, reviewed website presentation against the
written public records. One overstatement was corrected to say 120 links were
checked; final wording, tests and rendering were checked locally without another
reviewer run. This is separate from review of the original refresh outcomes or
retrospective entry, which was not performed.

Detailed evidence is retained privately under ID
`website-deployment-2026-10-26-a0e636c`. These are publication/rendering checks,
not a new refresh run, independent scoring or user study. Later record-only commits
retain this deployed SHA and need no further deployment when output is unchanged.

## October 26 earlier real-repository evidence deployment

On October 26, 2026, the owner-authorized [Pages workflow](https://github.com/jaredchu/context-docs/actions/runs/40268041794)
built and deployed `main` at `a97307e`. The homepage links to the guide's separate
synthetic and real-repository refresh evidence sections. Visible real-use limits
retain the same-chat setup, explicit repeat cues, bounded checks, missing saved
manifests/traces, lack of ground truth/control and possibility of missed drift.
Private content and filenames stay unpublished. Skills and original study records
are unchanged.

Both workflow jobs succeed, and the pinned build passes all 24 site tests.
All ten uploaded and served public files match the pinned build by SHA-256;
the empty `.nojekyll` marker is omitted by upload as before. Only the homepage
and getting-started HTML outputs change from `6b1c9d6`. Four canonical URLs,
existing Open Graph URLs, sitemap URLs and the robots sitemap reference match.

Fresh live Chrome checks at 1440×1000 and 390×844 pass for the homepage evidence
link, distinct sections and their source links, visible limits, aggregate-only
private results, canonical refresh prompt and stubbed copy feedback. No page-wide
overflow or JavaScript errors were observed. The prompt, both evidence sections
and limits remain accessible without JavaScript; no host clipboard write occurs.
Opus 5.5, requested High, reviewed presentation against the public records;
suggested wording fixes were checked locally with no second reviewer run.

Detailed evidence is retained privately under ID
`website-deployment-2026-10-26-a97307e`. These are publication/rendering checks,
not new refresh subjects, independent scoring or a user study. Later record-only
commits retain this deployed SHA and need no additional deployment when output
is unchanged.

## October 26 refresh-guidance deployment

On October 26, 2026, the owner-authorized [Pages workflow](https://github.com/jaredchu/context-docs/actions/runs/40262515843)
built and deployed `main` at `6b1c9d6`, publishing the canonical refresh prompt in
the beginner guide and a homepage link to that section. Existing skill versions
and the synthetic baseline's qualifications are preserved. The pinned source and
workflow pass all 23 site tests; both build and deploy jobs succeed. All ten
served public files match the pinned build and uploaded artifact by SHA-256;
the empty `.nojekyll` marker is omitted by upload as before. Only the homepage
and getting-started HTML outputs differ from the previous deployment.

Four canonical URLs, existing Open Graph URLs, sitemap URLs and the robots
sitemap reference match. Live Chrome checks at 1440×1000 and 390×844 pass for
the homepage-to-refresh link, fragment, canonical prompt, copy feedback, no
page-wide overflow and no observed JavaScript errors. The prompt is accessible
without JavaScript. Clipboard writes were stubbed in fresh contexts; no host
clipboard write occurred. An initial Python HTTP client received 403; successful
canonical byte checks used Node fetch, complemented by the Chrome checks.

Detailed evidence is retained privately under ID
`website-deployment-2026-10-26-6b1c9d6`. These are deployment/rendering checks,
not a new native evaluation or user study. Later record/context commits do not
replace this deployed SHA or require another deployment when output is unchanged.

## October 26 comparison and example deployment

On October 26, 2026, the owner-authorized [Pages workflow](https://github.com/jaredchu/context-docs/actions/runs/40258260595)
built and deployed `main` at `ee9211e`. The pinned source passed all 22 site tests;
both workflow build and deploy jobs succeeded. All ten served files match the
pinned build and uploaded artifact by SHA-256. The local eleven-file build's
empty `.nojekyll` marker is omitted by artifact upload as before.

Four canonical URLs, existing Open Graph URLs, sitemap URLs and the robots sitemap
reference match. Live Chrome checks pass at 1440×1000 and 390×844 for the new
comparison-to-example routes, all nine copy handlers, step anchors, no page-wide
overflow, no observed JavaScript errors and the no-JavaScript path. Clipboard
writes were stubbed inside fresh contexts; no host clipboard write. These are
publication/rendering checks, not a new native evaluation or user study.

The example was not redeployed: its only Actions run remains the October 25
`0f68893` deployment, and read-only health checks before/after still report that
full revision. The receipt is retained privately under evidence ID
`website-deployment-2026-10-26-ee9211e`. Later record/context commits do not replace
this deployed source or require another deployment when output is unchanged.

## Initial Reading Queue publication

On October 25, 2026, the [workflow](https://github.com/jaredchu/context-docs/actions/runs/40158912040)
built and deployed `main` at `b38853d`, publishing the runnable Reading Queue
walkthrough. All 22 site tests passed in the pinned source and workflow. All ten
served files match the pinned build and uploaded artifact by SHA-256; the local
eleven-file build includes an empty `.nojekyll` omitted from upload. Four HTML
canonical links, sitemap URLs and the robots sitemap reference match. Existing
Open Graph URLs, where present, match their canonical links.

Live Chrome checks pass at 1440×1000 and 390×844, including all nine prompt copy
buttons, step anchors, navigation from both entry pages, no page-wide horizontal
overflow and no uncaught JavaScript errors. These are application/rendering
checks, not accessibility certification or a user-benefit study. The
[separate app](../docs/reading-queue-example.md) and focused ordinary-prompt
observation have their own evidence and limits. The detailed receipt remains in
private notes under evidence ID `website-deployment-2026-10-25-b38853d`.

Later record/context commits do not replace this deployed source or require
another deployment if output and deployment behavior are unchanged.

## Previous cleanup deployment

On October 25, 2026, the [deployment workflow](https://github.com/jaredchu/context-docs/actions/runs/40155726392)
successfully built and deployed `main` at `c2414d4`, publishing the targeted
website cleanup. All 20 site tests passed in a clean pinned source snapshot and
the deployment workflow. All nine served public files matched both the pinned
local build and uploaded artifact by SHA-256 over canonical HTTPS responses.
All three HTML canonical links, sitemap URLs and the robots sitemap reference
matched. The ten-file local build includes an empty `.nojekyll` marker omitted
by the upload.

Every build file also matches the previously verified local cleanup preview.
This deployment verification covers response bytes and metadata; the earlier
local browser checks retain their original scope. No new live-browser rendering
or agent evaluation ran. The detailed receipt is retained in private operator
notes under evidence ID `website-deployment-2026-10-25-c2414d4`.
The previous `9b6ee38` deployment and its receipt remain historical evidence.
Later record/context commits do not supersede this deployed source or require
another deployment when website output and deployment behavior are unchanged.

## Search discovery

`SITE_URL` in [build.py](build.py) owns the canonical HTTPS origin. The build uses
it for the canonical link, Open Graph URLs, robots sitemap location and sitemap.
The sitemap lists only public HTML pages; it has no invented modification dates.
The crawler policy permits crawling the public artifact and introduces no
training-specific restrictions. Search access and model-training preferences are
separate; this policy is not a guarantee of indexing, citations or recommendations.

After deploying these files:

1. Check the live `robots.txt`, sitemap, canonical links and redirects. Cloudflare
   can modify robots responses or challenge requests separately from repository
   rules. Check the actual response and verified crawler traffic; a spoofed
   user-agent request alone does not prove a real crawler has access.
2. Verify the domain in [Google Search Console](https://search.google.com/search-console/about)
   and [Bing Webmaster Tools](https://www.bing.com/webmasters/about), then submit
   `https://context-docs.com/sitemap.xml`. These account registrations and
   submissions are not performed by the build or deployment workflow.
3. Inspect indexing and referral traffic before claiming discovery. Keep crawler
   access controls separate from any decision about training reuse.

See [OpenAI crawler guidance](https://developers.openai.com/api/docs/bots),
[Anthropic crawler guidance](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
and [Google's AI search guidance](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide).

## Deployment

Live site: [Context Docs](https://context-docs.com/).

The site is prepared for an **asset-only Cloudflare Worker** using Workers Static
Assets ([migration status](#workers-static-assets-migration-prepared)). The root
[wrangler.jsonc](../wrangler.jsonc) names the Worker `context-docs-site` and
serves `.local/site-dist` with no Worker script. Its settings are:
`html_handling: auto-trailing-slash`, `not_found_handling: none`, custom-domain
routes for `context-docs.com` and `www.context-docs.com`, with `workers_dev`
and preview URLs disabled. Pre-cutover checks use a separate temporary configuration.

The [landing-page workflow](../.github/workflows/site.yml) works as follows:

- **Pull requests validate only.** The build job runs
  repository static checks (`evals/checks/static_checks.py`) and the site tests,
  then builds and prints a SHA-256 manifest. It runs `wrangler deploy --dry-run`
  without credentials and uploads `.local/site-dist` as the `site-dist` artifact.
- **Pushes to `main` deploy automatically** once the build job passes, if they
  touch a build input. Build inputs are the site templates, styles, script,
  favicon, build/test code and vendored icons; the selected root assets; the root
  README; the getting-started and demo sources; both examples; skill `VERSION`
  files; `wrangler.jsonc` and the workflow itself. This README and deployment
  records are excluded, so record-only commits do not start a build or deployment.
- **Manual reruns** use **Landing page** → *Run workflow* on `main` with
  **deploy** selected. On other refs, the deploy job is skipped.
- The deploy job downloads the same `site-dist` artifact, prints its manifest
  and runs `wrangler deploy`. It does not rebuild. Wrangler is pinned to
  **4.113.0** (via `npx`) on Node 24. Only this job receives the
  `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` repository secrets. It runs in
  the `production` environment, and the `context-docs-production` concurrency
  group serializes it. A freshness check skips superseded site output or deployment
  configuration; record-only commits that leave both unchanged do not prevent a
  pending deployment. Deployed versions are tagged with their source SHA.

Artifact upload excludes hidden files, so the empty `.nojekyll` marker is not
deployed, as it was not on GitHub Pages either. The Reading Queue 301, canonical
`www` redirect and Cloudflare Web Analytics are zone-level rules outside this
repository. The coordinator manages them, not Wrangler.

Because pushes to `main` now publish, authority to push a site-input change to
`main` is also authority to deploy it. Keep unreviewed site changes on branches
or pull requests.

### Deployment checklist

Apply the [refresh recording and publication boundary](../docs/project-decisions.md#refresh-recording-and-publication-boundary)
before this checklist. A routine unchanged refresh is not a reason to create
website content; publication still needs useful new information and task authority.

- [ ] Determine whether the change affects public website output or deployment
  behavior. Verification receipts, journals, project context and this README do
  not become website content. Some Markdown does: the root README, selected
  guide/demo sections and examples feed [build.py](build.py). Judge the actual
  inputs rather than treating every documentation change as deployable content.
- [ ] If only records or context changed, retain the existing deployed SHA and
  receipt and stop without deploying again. `main` may advance beyond the
  deployed commit. If output impact is uncertain, build locally and compare
  public file paths and per-file SHA-256 hashes with the last deployment's
  retained manifest, artifact or a build from its exact source SHA. Compare file
  contents rather than archive digests, and account for the documented omission
  of the empty `.nojekyll` marker. Identical output needs no routine redeployment;
  deployment-behavior changes or an explicit owner-requested rerun are separate
  reasons to deploy.
- [ ] When deployment is needed and authorized, record the exact selected `main`
  SHA, run the site tests and build, and check relevant CI. A push of build inputs
  to `main` deploys automatically. Otherwise, dispatch **Landing page** on `main`
  with **deploy** selected. Verify the run's source SHA and successful build/deploy
  jobs, and compare the two printed manifests.
- [ ] Compare the uploaded artifact and canonical live HTTPS responses with that
  pinned build, including public file paths/hashes and HTML/robots/sitemap
  metadata. Record failures and verification limits; byte checks do not establish
  browser rendering or agent behavior.
- [ ] Save one deployment receipt in the appropriate operator notes and update
  the concise public summary and context. Keep the SHA actually deployed and
  workflow identity; do not replace them with a later record-commit SHA. Commit
  and push those records when authorized, check their applicable CI, then stop.
  That follow-up commit does not start another deployment/receipt cycle unless
  it also changes website output or deployment behavior, or the owner requests
  another run. Preserve historical receipts.

This checklist grants no deployment, commit or push authority. Pushing build
inputs to `main` deploys them, so treat that push as publication. Recording evidence
does not create a pending deployment merely because `main` now has a newer SHA.
Path filters exclude record-only commits.

## Historical GitHub Pages configuration

<a id="github-pages"></a>
*Historical:* this describes hosting before the
[Workers Static Assets migration](#workers-static-assets-migration-prepared). The
DNS and Pages settings below still serve the site until the coordinator completes
and verifies the cutover. Earlier deployment records above refer to this setup.

Under that setup, deployment was manual: select **GitHub Actions** as the Pages source in
repository Settings → Pages, then run **Landing page** on `main` with **deploy**
selected. The GitHub Pages deploy job has been removed from the workflow.

The custom domain is `context-docs.com`. Cloudflare DNS points its four A and four
AAAA records to GitHub Pages, with `www` pointing to `jaredchu.github.io` by CNAME;
these records are proxied. Cloudflare provides the public certificate with
**Full** SSL mode and **Always Use HTTPS** enabled. Full encrypts the origin
connection without validating the origin certificate; visitor HTTPS does not
depend on GitHub issuing a certificate for this domain. GitHub Pages handles
hosting and the `www` redirect. Domain configuration lives in Pages settings; this Actions-based
deployment does not require a repository CNAME file. The page uses relative asset
links. Do not publish the repository root as the site artifact.

Cutover notes for the coordinator (not yet verified in this repository):
- Worker custom domains create their own DNS records. The existing apex A/AAAA
  and `www` CNAME records probably need removing or replacing first, otherwise
  the first `wrangler deploy` may fail on the conflict.
- GitHub Pages no longer provides the `www` redirect once DNS moves. The planned
  canonical `www` rule replaces it.
- Check Full SSL, Always Use HTTPS, the Reading Queue 301 and analytics against
  the Worker origin after cutover.
- Unset the Pages custom domain only after the Worker serves both hostnames.

See [GitHub's custom-workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
and [custom-domain guidance](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).
