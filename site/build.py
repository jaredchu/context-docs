"""Build the public website from an explicit page and file allowlist. Standard library only."""
from html import escape
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '.local' / 'site-dist'
SITE_URL = 'https://context-docs.com/'
ICONS = frozenset({'arrow-right', 'arrow-down', 'arrow-up-right', 'file-text',
                   'plus', 'minus', 'copy', 'check'})


def expand_icons(root, template):
    """Embed selected, locally vendored SVGs before inserting escaped source text."""
    def substitute(match):
        name = match[1]
        if name not in ICONS:
            raise ValueError(f'Unknown UI icon: {name}')
        source = root / 'site/vendor/tabler' / (name + '.svg')
        if source.is_symlink() or not source.is_file():
            raise ValueError(f'Expected a regular icon source: {name}')
        svg = source.read_text(encoding='utf-8').strip()
        svg = svg.replace('<svg', '<svg aria-hidden="true" focusable="false"', 1)
        svg = svg.replace('class="icon ', 'class="ui-icon icon ', 1)
        return re.sub(r'>\s+<', '><', svg)

    rendered = re.sub(r'\[\[icon:([a-z-]+)\]\]', substitute, template)
    if '[[icon:' in rendered:
        raise ValueError('Malformed UI icon marker')
    return rendered


# Public routes listed in the sitemap, in order. The legacy redirect is deliberately absent.
CANONICAL_ROUTES = ('', 'getting-started/', 'compare/', 'examples/', 'examples/reading-queue/',
                    'examples/switching-codex-claude/', 'examples/switching-claude-codex/')

# Client-side fallback for the former /reading-queue/ URL. GitHub Pages cannot send an
# HTTP 301 from this build; this page uses a canonical link, a script that keeps the
# query and fragment, a meta refresh for browsers without scripts and a visible link.
READING_QUEUE_REDIRECT = '''<!doctype html>
<html lang="en"><head>
<!-- UI icons: Tabler Icons 3.50.0 (MIT). License: ../tabler-icons-LICENSE.txt -->
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moved: Reading Queue example</title>
<link rel="canonical" href="{{SITE_URL}}examples/reading-queue/">
<script>(function () {
  var target = new URL('../examples/reading-queue/', window.location.href);
  target.search = window.location.search;
  target.hash = window.location.hash;
  window.location.replace(target.href);
}());</script>
<meta http-equiv="refresh" content="0; url=../examples/reading-queue/">
<meta name="theme-color" content="#fafbfc"><link rel="icon" href="../favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../styles.css">
</head>
<body class="guide-page redirect-page">
<main id="main" class="wrap"><header class="guide-hero"><a class="brand" href="../"><img class="brand-mark" src="../logo.svg" width="26" height="26" alt=""><span>Context Docs</span></a><p class="eyebrow">PAGE MOVED</p><h1>The Reading Queue example<br><span>has moved.</span></h1><p class="guide-lead">It now lives with the other examples. If you are not taken there automatically, use the link below.</p><p><a class="button primary" href="../examples/reading-queue/">Open the Reading Queue example <span aria-hidden="true">[[icon:arrow-right]]</span></a></p></header></main>
</body></html>
'''


def render_site_url_only(root, template, label):
    """Render a static page whose only marker is SITE_URL; fail on anything else."""
    template = expand_icons(root, template)
    if set(re.findall(r'{{([A-Z_]+)}}', template)) != {'SITE_URL'}:
        raise ValueError(f'{label} must contain only the SITE_URL marker')
    rendered = template.replace('{{SITE_URL}}', escape(SITE_URL))
    if '{{' in rendered:
        raise ValueError(f'{label} contains an unknown or malformed marker')
    return rendered


def render_page(root, template_name, label):
    return render_site_url_only(root, (root / 'site' / template_name).read_text(encoding='utf-8'), label)


def render_comparison(root):
    return render_page(root, 'compare.html', 'Comparison page')


def render_reading_queue(root):
    template = (root / 'site/reading-queue.html').read_text(encoding='utf-8')
    if 'DEMO_URL_PENDING' in template:
        raise ValueError('Reading Queue demo URL is still a placeholder')
    return render_site_url_only(root, template, 'Reading Queue page')


def render_reading_queue_redirect(root):
    return render_site_url_only(root, READING_QUEUE_REDIRECT, 'Reading Queue redirect')


def fenced_section(text, heading, language):
    section = text.split(heading + '\n', 1)
    if len(section) != 2:
        raise ValueError(f'Missing canonical section: {heading}')
    # Headings inside the fenced Markdown example are content, not boundaries.
    content = []
    inside = False
    for line in section[1].splitlines():
        if inside:
            if line == '```':
                return '\n'.join(content)
            content.append(line)
        elif line == '```' + language:
            inside = True
        elif re.match(r'^#{1,3} ', line):
            break
    raise ValueError(f'Missing or unclosed {language} block in {heading}')


def render(root, template_name='index.html'):
    readme = (root / 'README.md').read_text(encoding='utf-8')
    status = re.search(r'^\*\*Status: (.*?)\*\*$', readme, re.M)
    if status is None:
        raise ValueError('Missing canonical package status in README.md')
    example = (root / 'examples/maintenance.md').read_text(encoding='utf-8')
    values = {
        'SITE_URL': SITE_URL,
        'QUICK_EXAMPLE': fenced_section(readme, '## What you get', 'markdown'),
        'CODEX_INSTALL': fenced_section(readme, '### Install in Codex', 'text'),
        'CLAUDE_INSTALL': fenced_section(readme, '### Install in Claude Code', 'sh'),
        'SAVE_PROMPT': fenced_section(readme, '### 2. Save decisions, current work and next steps', 'text'),
        'RESUME_PROMPT': fenced_section(readme, '### 3. Resume with the saved context', 'text'),
        'PROGRESS_PROMPT': fenced_section(readme, '### 4. Visualize progress in Markdown', 'text'),
        'PROGRESS_EXAMPLE': fenced_section((root / 'examples/progress.md').read_text(encoding='utf-8'),
                                           '## Example Markdown view', 'text'),
        'EXAMPLE_BEFORE': fenced_section(example, '## Before: existing context.md', 'markdown'),
        'EXAMPLE_AFTER': fenced_section(example, '## After: same context.md', 'markdown'),
        'CORE_VERSION': (root / 'skills/context-docs/VERSION').read_text(encoding='utf-8').strip(),
        'ADOPTION_VERSION': (root / 'skills/adopt-context-docs/VERSION').read_text(encoding='utf-8').strip(),
        'PACKAGE_STATUS': 'Unreleased' if re.search(r'\bunreleased\b', status[1], re.I) else 'Released',
    }
    if template_name == 'index.html':
        demo = (root / 'docs/outreach-v0.2.5.md').read_text(encoding='utf-8')
        values.update({
            'DEMO_NOTES': fenced_section(demo, '### 1. Show the fictional work notes', 'text'),
            'DEMO_CONTEXT': fenced_section(demo, '### 2. Show the saved Markdown', 'text'),
            'DEMO_RESUME': fenced_section(demo, '### 3. Resume in a fresh session', 'text'),
        })
    if template_name == 'getting-started.html':
        guide = (root / 'docs/getting-started.md').read_text(encoding='utf-8')
        values.update({
            'REFRESH_PROMPT': fenced_section(guide, '### Refresh after outside work', 'text'),
            'LOCAL_ONLY_PROMPT': fenced_section(guide, '## Local-only context (excluded from Git)', 'text'),
            'AUTO_LOGGING_PROMPT': fenced_section(guide, '### Auto logging for local-only context', 'text'),
            'VERIFY_RESUME_PROMPT': fenced_section(guide, '### Verify a resumed session', 'text'),
            'TROUBLESHOOT_PROMPT': fenced_section(guide, '### Troubleshoot setup and saved context', 'text'),
        })
    template = expand_icons(root, (root / 'site' / template_name).read_text(encoding='utf-8'))
    required = {
        'SITE_URL', 'CODEX_INSTALL', 'CLAUDE_INSTALL', 'SAVE_PROMPT',
        'RESUME_PROMPT', 'PROGRESS_PROMPT', 'PROGRESS_EXAMPLE', 'CORE_VERSION', 'ADOPTION_VERSION', 'PACKAGE_STATUS',
    }
    required |= ({'QUICK_EXAMPLE', 'REFRESH_PROMPT', 'LOCAL_ONLY_PROMPT', 'AUTO_LOGGING_PROMPT',
                  'VERIFY_RESUME_PROMPT', 'TROUBLESHOOT_PROMPT'}
                 if template_name == 'getting-started.html'
                 else {'EXAMPLE_BEFORE', 'EXAMPLE_AFTER', 'DEMO_NOTES', 'DEMO_CONTEXT', 'DEMO_RESUME'})
    present = set(re.findall(r'{{([A-Z_]+)}}', template))
    if required - present:
        raise ValueError(f'Missing template markers: {sorted(required - present)}')

    def substitute(match):
        key = match[1]
        if key not in values:
            raise ValueError(f'Unknown template marker: {key}')
        return escape(values[key])

    return re.sub(r'{{([A-Z_]+)}}', substitute, template)


def build(root=ROOT, output=OUTPUT):
    # Render selected public prompts; never copy context, journals or a recursive directory.
    sources = {
        'styles.css': root / 'site/styles.css',
        'main.js': root / 'site/main.js',
        'context-docs-overview.png': root / 'assets/context-docs-overview.png',
        'favicon.svg': root / 'site/favicon.svg',
        'logo.svg': root / 'assets/context-docs-mark.svg',
        'tabler-icons-LICENSE.txt': root / 'site/vendor/tabler/LICENSE',
    }
    for source in sources.values():
        if source.is_symlink() or not source.is_file():
            raise ValueError(f'Expected a regular public asset: {source.name}')
    # Render every page before touching the destination so invalid content keeps the prior build.
    pages = {
        'index.html': render(root),
        'getting-started/index.html': render(root, 'getting-started.html'),
        'compare/index.html': render_comparison(root),
        'examples/index.html': render_page(root, 'examples.html', 'Examples page'),
        'examples/reading-queue/index.html': render_reading_queue(root),
        'examples/switching-codex-claude/index.html':
            render_page(root, 'switching-codex-claude.html', 'Codex to Claude Code page'),
        'examples/switching-claude-codex/index.html':
            render_page(root, 'switching-claude-codex.html', 'Claude Code to Codex page'),
        'reading-queue/index.html': render_reading_queue_redirect(root),
    }
    if set(pages) - {'reading-queue/index.html'} != {route + 'index.html' for route in CANONICAL_ROUTES}:
        raise ValueError('Canonical routes and rendered pages disagree')
    if output.is_symlink():
        raise ValueError('Build destination must not be a symlink')
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    for name, html in pages.items():
        (output / name).parent.mkdir(parents=True, exist_ok=True)
        (output / name).write_text(html, encoding='utf-8')
    (output / '.nojekyll').write_text('', encoding='utf-8')
    # Only public pages belong here, never repository context or evidence exports.
    (output / 'robots.txt').write_text(
        'User-agent: *\nAllow: /\n\nSitemap: ' + SITE_URL + 'sitemap.xml\n',
        encoding='utf-8')
    (output / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + ''.join('  <url><loc>' + escape(SITE_URL + route) + '</loc></url>\n' for route in CANONICAL_ROUTES)
        + '</urlset>\n',
        encoding='utf-8')
    for name, source in sources.items():
        shutil.copyfile(source, output / name)
    return output


if __name__ == '__main__':
    print(build())
