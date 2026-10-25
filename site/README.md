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
tracking, cookies or application backend are included.

The working build contains only ten explicitly named public files: `index.html`,
`styles.css`, `main.js`, `favicon.svg`, `context-docs-overview.png`, `.nojekyll`,
`robots.txt`, `sitemap.xml`, `getting-started/index.html` and `compare/index.html`.
The existing [illustration](../assets/README.md) is copied unchanged. The build
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
The existing workflow includes this public source in its build path filters;
deployment remains manual and separately authorized.

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
the site's local-only setup and auto-logging prompts are extracted from its public
sections. The site links to it for client settings, upgrades and logging details.
Repository context, local notes and journals never become build inputs.

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

## Latest deployment

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

## GitHub Pages

Live site: [Context Docs](https://context-docs.com/).

The [landing-page workflow](../.github/workflows/site.yml) builds and tests on
relevant pull requests and main-branch pushes. Deployment is manual. When an
authorized change needs publication, select **GitHub Actions** as the Pages source
in repository Settings → Pages, then run **Landing page** on `main` with **deploy**
selected. Use the URL returned by the deployment. Branch/PR builds do not publish
a site. The broad `site/**` path filter can trigger a build for this README;
a successful build or a skipped deploy job does not require manual deployment.

### Deployment checklist

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
  SHA, run the site tests and build, and check relevant CI. Dispatch the manual
  deployment and verify its source SHA and successful build/deploy jobs.
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

This checklist grants no deployment, commit or push authority. Recording evidence
does not create a pending deployment merely because `main` now has a newer SHA.

The custom domain is `context-docs.com`. Cloudflare DNS points its four A and four
AAAA records to GitHub Pages, with `www` pointing to `jaredchu.github.io` by CNAME;
these records are proxied. Cloudflare provides the public certificate with
**Full** SSL mode and **Always Use HTTPS** enabled. Full encrypts the origin
connection without validating the origin certificate; visitor HTTPS does not
depend on GitHub issuing a certificate for this domain. GitHub Pages handles
hosting and the `www` redirect. Domain configuration lives in Pages settings; this Actions-based
deployment does not require a repository CNAME file. The page uses relative asset
links. Do not publish the repository root as the site artifact.

See [GitHub's custom-workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
and [custom-domain guidance](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).
