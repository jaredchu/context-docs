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


def render(root):
    readme = (root / 'README.md').read_text(encoding='utf-8')
    example = (root / 'examples/maintenance.md').read_text(encoding='utf-8')
    values = {
        'SITE_URL': SITE_URL,
        'CODEX_INSTALL': fenced_section(readme, '### Install in Codex', 'text'),
        'CLAUDE_INSTALL': fenced_section(readme, '### Install in Claude Code', 'sh'),
        'SAVE_PROMPT': fenced_section(readme, '### 2. Work normally, then save useful changes', 'text'),
        'RESUME_PROMPT': fenced_section(readme, '### 3. Resume with the saved context', 'text'),
        'EXAMPLE_BEFORE': fenced_section(example, '## Before: existing context.md', 'markdown'),
        'EXAMPLE_AFTER': fenced_section(example, '## After: same context.md', 'markdown'),
        'CORE_VERSION': (root / 'skills/context-docs/VERSION').read_text(encoding='utf-8').strip(),
        'ADOPTION_VERSION': (root / 'skills/adopt-context-docs/VERSION').read_text(encoding='utf-8').strip(),
    }
    template = (root / 'site/index.html').read_text(encoding='utf-8')
    for key, value in values.items():
        marker = '{{' + key + '}}'
        if marker not in template:
            raise ValueError(f'Missing template marker: {key}')
        template = template.replace(marker, escape(value))
    if re.search(r'{{[A-Z_]+}}', template):
        raise ValueError('Unresolved template marker')
    return template


def build(root=ROOT, output=OUTPUT):
    # Never copy the repository, docs, journal or a recursive asset directory.
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
    if output.is_symlink():
        raise ValueError('Build destination must not be a symlink')
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    (output / 'index.html').write_text(html, encoding='utf-8')
    (output / '.nojekyll').write_text('', encoding='utf-8')
    # Only public pages belong here, never repository context or evidence exports.
    (output / 'robots.txt').write_text(
        'User-agent: *\nAllow: /\n\nSitemap: ' + SITE_URL + 'sitemap.xml\n',
        encoding='utf-8')
    (output / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        '  <url><loc>' + escape(SITE_URL) + '</loc></url>\n</urlset>\n',
        encoding='utf-8')
    for name, source in sources.items():
        shutil.copyfile(source, output / name)
    return output


if __name__ == '__main__':
    print(build())
