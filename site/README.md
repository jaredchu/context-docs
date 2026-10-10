# Landing page

A static introduction for prospective Context Docs users. The Python standard-library
build reads installation commands and save/resume prompts from the root [README](../README.md), before/after
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

The output contains only six explicitly named public files: `index.html`,
`styles.css`, `main.js`, `favicon.svg`, `context-docs-overview.png` and `.nojekyll`.
The existing [illustration](../assets/README.md) is copied unchanged. The build
replaces its disposable output directory to prevent stale files being published.
It never copies the repository, context docs, journals, or evaluation exports.

## GitHub Pages

Live site: [Context Docs](https://jaredchu.github.io/context-docs/).

The [landing-page workflow](../.github/workflows/site.yml) builds and tests on
relevant pull requests and main-branch pushes. Deployment is manual: after an
approved merge, select **GitHub Actions** as the Pages source in repository
Settings → Pages, then run **Landing page** on `main` with **deploy** selected.
Use the URL returned by the deployment. Branch/PR builds do not publish a site.

The page uses relative asset links so it supports a repository subpath or a future
custom domain. No domain is configured or assumed; the owner plans to purchase
`context-docs.com` separately. Connect and verify it in GitHub Pages only when
requested. Do not publish the repository root as the site artifact.

See [GitHub's custom-workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
and [custom-domain guidance](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).
