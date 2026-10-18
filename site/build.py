"""Build the public landing page from an explicit file allowlist. Standard library only."""
from html import escape
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / '.local' / 'site-dist'
SITE_URL = 'https://context-docs.com/'


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
            'LOCAL_ONLY_PROMPT': fenced_section(guide, '## Local-only context (excluded from Git)', 'text'),
            'AUTO_LOGGING_PROMPT': fenced_section(guide, '### Auto logging for local-only context', 'text'),
        })
    template = (root / 'site' / template_name).read_text(encoding='utf-8')
    required = {
        'SITE_URL', 'CODEX_INSTALL', 'CLAUDE_INSTALL', 'SAVE_PROMPT',
        'RESUME_PROMPT', 'PROGRESS_PROMPT', 'PROGRESS_EXAMPLE', 'CORE_VERSION', 'ADOPTION_VERSION', 'PACKAGE_STATUS',
    }
    required |= ({'QUICK_EXAMPLE', 'LOCAL_ONLY_PROMPT', 'AUTO_LOGGING_PROMPT'} if template_name == 'getting-started.html'
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
    }
    for source in sources.values():
        if source.is_symlink() or not source.is_file():
            raise ValueError(f'Expected a regular public asset: {source.name}')
    html = render(root)
    guide = render(root, 'getting-started.html')
    if output.is_symlink():
        raise ValueError('Build destination must not be a symlink')
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    (output / 'index.html').write_text(html, encoding='utf-8')
    (output / 'getting-started').mkdir()
    (output / 'getting-started/index.html').write_text(guide, encoding='utf-8')
    (output / '.nojekyll').write_text('', encoding='utf-8')
    # Only public pages belong here, never repository context or evidence exports.
    (output / 'robots.txt').write_text(
        'User-agent: *\nAllow: /\n\nSitemap: ' + SITE_URL + 'sitemap.xml\n',
        encoding='utf-8')
    (output / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        '  <url><loc>' + escape(SITE_URL) + '</loc></url>\n'
        '  <url><loc>' + escape(SITE_URL + 'getting-started/') + '</loc></url>\n</urlset>\n',
        encoding='utf-8')
    for name, source in sources.items():
        shutil.copyfile(source, output / name)
    return output


if __name__ == '__main__':
    print(build())
