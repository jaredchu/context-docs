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

The output contains only nine explicitly named public files: `index.html`,
`styles.css`, `main.js`, `favicon.svg`, `context-docs-overview.png`, `.nojekyll`,
`robots.txt`, `sitemap.xml` and `getting-started/index.html`.
The existing [illustration](../assets/README.md) is copied unchanged. The build
replaces its disposable output directory to prevent stale files being published.
It never copies the repository, context docs, journals, or evaluation exports.

Both pages also show the text tree from the public [progress example](../examples/progress.md),
with clickable source links outside the diagram. The build extracts its canonical
fenced block; it does not read project context or study outputs. The diagram scrolls
within its box on narrow screens to preserve branch alignment.

The v0.2.3 copy explains concise overviews with linked evidence, retaining
meaningful outcomes, decisions, blockers, approval boundaries and existing layouts.
Both pages retain default inline adoption and everyday maintenance, and state the
qualified smoke result: Codex created and removed an extra temporary hash file,
failing strict write scope. Both templates link v0.2.3 notes and previous v0.2.2 notes.
Explicit progress prompts remain optional; installation/upgrade alone changes no
project context.

The [getting-started template](getting-started.html) owns the beginner walkthrough.
Its installation commands, save/resume/progress prompts, synthetic example and versions
come from the same canonical sources as the landing page. The detailed
[installation reference](../docs/getting-started.md) remains in the repository;
the site's local-only setup and auto-logging prompts are extracted from its public
sections. The site links to it for client settings, upgrades and logging details.
Repository context, local notes and journals never become build inputs.

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
relevant pull requests and main-branch pushes. Deployment is manual: after an
approved merge, select **GitHub Actions** as the Pages source in repository
Settings → Pages, then run **Landing page** on `main` with **deploy** selected.
Use the URL returned by the deployment. Branch/PR builds do not publish a site.

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
