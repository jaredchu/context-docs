"""Boundary and canonical-content checks for the public website artifact."""
import importlib.util
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
from html import unescape
from html.parser import HTMLParser
import urllib.parse
import urllib.robotparser
import xml.etree.ElementTree as ET

SPEC = importlib.util.spec_from_file_location('landing_build', Path(__file__).with_name('build.py'))
landing = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(landing)

SCHEME = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.-]*:')
READING_QUEUE_STEPS = ('run', 'adopt', 'read', 'scope', 'save', 'resume', 'verify', 'compare', 'deploy')
# Fragment targets published at /reading-queue/ before the move; incoming links must keep working.
READING_QUEUE_IDS = ({'main', 'try', 'takeaways'} | set(READING_QUEUE_STEPS)
                     | {'prompt-' + step for step in READING_QUEUE_STEPS}
                     | {'status-' + step for step in READING_QUEUE_STEPS})


class PageParser(HTMLParser):
    """Collect ids, links, assets, metadata, inline scripts and copyable code from one page."""

    def __init__(self):
        super().__init__()
        self.id_list = []
        self.links = []
        self.assets = []
        self.canonical = []
        self.refresh = []
        self.scripts = []
        self.code = {}
        self.buttons = []
        self._in_nav = False
        self._link = None
        self._script = False
        self._code = None

    @property
    def ids(self):
        return set(self.id_list)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.id_list.append(attrs['id'])
        if tag == 'nav':
            self._in_nav = 'site-nav' in (attrs.get('class') or '').split()
        if tag == 'a' and 'href' in attrs:
            self._link = {'attrs': attrs, 'text': '', 'nav': self._in_nav}
            self.links.append(self._link)
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs['href'])
        if tag == 'link' and attrs.get('rel') in ('stylesheet', 'icon'):
            self.assets.append(attrs['href'])
        if tag in ('script', 'img') and 'src' in attrs:
            self.assets.append(attrs['src'])
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'refresh':
            self.refresh.append(attrs['content'])
        if tag == 'script' and 'src' not in attrs:
            self._script = True
            self.scripts.append('')
        if tag == 'code' and 'id' in attrs:
            self._code = attrs['id']
            self.code[self._code] = ''
        if tag == 'button' and 'data-copy' in attrs:
            self.buttons.append(attrs)

    def handle_endtag(self, tag):
        if tag == 'nav':
            self._in_nav = False
        if tag == 'a':
            self._link = None
        if tag == 'script':
            self._script = False
        if tag == 'code':
            self._code = None

    def handle_data(self, data):
        if self._link is not None:
            self._link['text'] += data
        if self._script:
            self.scripts[-1] += data
        if self._code:
            self.code[self._code] += data


def parse(html):
    page = PageParser()
    page.feed(html)
    return page


class LandingBuildTests(unittest.TestCase):
    def test_artifact_contains_only_allowlisted_files_even_after_dirty_build(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'public'
            output.mkdir()
            (output / 'private-note.txt').write_text('Must not survive a rebuild')
            landing.build(output=output)
            self.assertEqual({p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}, {
                'index.html', 'styles.css', 'main.js', 'favicon.svg', 'logo.svg',
                'context-docs-overview.png', '.nojekyll', 'robots.txt', 'sitemap.xml',
                'tabler-icons-LICENSE.txt',
                'getting-started/index.html', 'compare/index.html', 'examples/index.html',
                'examples/reading-queue/index.html', 'examples/switching-codex-claude/index.html',
                'examples/switching-claude-codex/index.html', 'reading-queue/index.html',
                'experiments/index.html', 'experiments/markdown-maintenance/index.html',
                'experiments/public-project-docs/index.html'})
            self.assertFalse(any(p.is_symlink() for p in output.rglob('*')))
            self.assertEqual((output / 'context-docs-overview.png').read_bytes(),
                             (landing.ROOT / 'assets/context-docs-overview.png').read_bytes())

    def test_brand_assets_are_consistent_and_resolve_on_every_public_route(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = landing.build(output=Path(temporary) / 'public')
            mark = (landing.ROOT / 'assets/context-docs-mark.svg').read_bytes()
            self.assertEqual((output / 'logo.svg').read_bytes(), mark)
            self.assertEqual((output / 'favicon.svg').read_bytes(), mark)
            self.assertEqual(ET.fromstring(mark).attrib['viewBox'], '0 0 32 32')

            class Images(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.sources = []

                def handle_starttag(self, tag, attrs):
                    attrs = dict(attrs)
                    if tag == 'img':
                        self.sources.append(attrs.get('src', ''))

            for path in output.rglob('*.html'):
                images = Images()
                images.feed(path.read_text())
                logos = [src for src in images.sources if src.endswith('logo.svg')]
                self.assertTrue(logos, path.relative_to(output).as_posix())
                for src in logos:
                    self.assertEqual((path.parent / src).resolve(), (output / 'logo.svg').resolve())

    def test_commands_and_example_are_canonical(self):
        rendered = unescape(landing.render(landing.ROOT))
        for path, heading, language in [
            ('README.md', '### Install in Codex', 'text'),
            ('README.md', '### Install in Claude Code', 'sh'),
            ('README.md', '### 2. Save decisions, current work and next steps', 'text'),
            ('README.md', '### 3. Resume with the saved context', 'text'),
            ('examples/maintenance.md', '## Before: existing context.md', 'markdown'),
            ('examples/maintenance.md', '## After: same context.md', 'markdown'),
        ]:
            block = landing.fenced_section((landing.ROOT / path).read_text(), heading, language)
            self.assertIn(block, rendered)
        self.assertNotIn('{{', rendered)

    def test_inline_icons_are_decorative_local_and_licensed_on_all_routes(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = landing.build(output=Path(temporary) / 'public')
            self.assertEqual((output / 'tabler-icons-LICENSE.txt').read_bytes(),
                             (landing.ROOT / 'site/vendor/tabler/LICENSE').read_bytes())
            for path in output.rglob('*.html'):
                html = path.read_text()
                self.assertNotIn('[[icon:', html)
                icons = re.findall(r'<svg\b[^>]*class="ui-icon [^"]*"[^>]*>', html)
                self.assertTrue(icons, path)
                for icon in icons:
                    self.assertIn('aria-hidden="true"', icon)
                    self.assertIn('focusable="false"', icon)
                    self.assertIn('stroke="currentColor"', icon)
                self.assertNotRegex(html, r'<(?:script|link)[^>]*(?:tabler|fontawesome|lucide)')

    def test_icon_markers_fail_closed_and_canonical_text_is_not_expanded(self):
        with self.assertRaisesRegex(ValueError, 'Unknown UI icon'):
            landing.expand_icons(landing.ROOT, '[[icon:not-bundled]]')
        with self.assertRaisesRegex(ValueError, 'Malformed UI icon'):
            landing.expand_icons(landing.ROOT, '[[icon:../file]]')
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, 'Expected a regular icon source'):
                landing.expand_icons(Path(temporary), '[[icon:check]]')
        original = Path.read_text
        def canonical_marker(path, *args, **kwargs):
            text = original(path, *args, **kwargs)
            if path == landing.ROOT / 'README.md':
                return text.replace('CSV export is implemented;', '[[icon:check]] is literal;')
            return text
        with patch.object(Path, 'read_text', canonical_marker):
            self.assertIn('[[icon:check]] is literal;', landing.render(landing.ROOT, 'getting-started.html'))

    def test_refresh_prompt_tracks_canonical_updates_without_publishing_other_notes(self):
        source = landing.ROOT / 'docs/getting-started.md'
        original_read = Path.read_text
        prompt = landing.fenced_section(source.read_text(), '### Refresh after outside work', 'text')

        def changed_source(path, *args, **kwargs):
            text = original_read(path, *args, **kwargs)
            if path == source:
                return text.replace(prompt, prompt + '\n<refresh-update>&', 1) + '\nUNSELECTED-REFRESH-NOTE'
            return text

        with patch.object(Path, 'read_text', changed_source):
            guide = landing.render(landing.ROOT, 'getting-started.html')
        self.assertIn(prompt + '\n<refresh-update>&', unescape(guide))
        self.assertIn('&lt;refresh-update&gt;&amp;', guide)
        self.assertNotIn('UNSELECTED-REFRESH-NOTE', guide)
        self.assertIn('id="refresh-after-outside-work"', guide)
        self.assertIn('data-copy="refresh-prompt"', guide)
        self.assertIn('getting-started/#refresh-after-outside-work', landing.render(landing.ROOT))

    def test_public_navigation_source_links_and_storage_boundaries(self):
        class Links(HTMLParser):
            def __init__(self):
                super().__init__()
                self.ids = set()
                self.hrefs = []

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if 'id' in attrs:
                    self.ids.add(attrs['id'])
                if tag == 'a' and 'href' in attrs:
                    self.hrefs.append(attrs['href'])

        with tempfile.TemporaryDirectory() as temporary:
            output = landing.build(output=Path(temporary) / 'public')
            pages = {}
            for path in output.rglob('*.html'):
                page = Links()
                html = path.read_text()
                page.feed(html)
                pages[path.resolve()] = page
                for private_detail in ('context-docs-notes', '/Users/', '/Volumes/', 'pi-git:'):
                    self.assertNotIn(private_detail, html, path.name)
            guide = (output / 'getting-started/index.html').resolve()
            # Preserve incoming URLs from the published evidence sections.
            for fragment in ('synthetic-refresh-evaluation', 'real-repository-refresh-results',
                             'paired-no-change-refresh-results'):
                self.assertIn(fragment, pages[guide].ids)
            prefix = 'https://github.com/jaredchu/context-docs/blob/main/'
            for path, page in pages.items():
                for href in page.hrefs:
                    with self.subTest(page=path.name, href=href):
                        if href.startswith(prefix):
                            source = href[len(prefix):].partition('#')[0]
                            self.assertTrue((landing.ROOT / source).is_file(), href)
                        elif not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', href):
                            relative, _, fragment = href.partition('#')
                            target = (path.parent / relative).resolve() if relative else path
                            if target.is_dir():
                                target /= 'index.html'
                            self.assertIn(target, pages, href)
                            if fragment:
                                self.assertIn(fragment, pages[target].ids, href)

    def test_demo_reuses_only_selected_blocks_and_escapes_source_updates(self):
        source = landing.ROOT / 'docs/outreach-v0.2.5.md'
        text = source.read_text()
        original_read = Path.read_text
        headings = ['### 1. Show the fictional work notes',
                    '### 2. Show the saved Markdown',
                    '### 3. Resume in a fresh session']
        for heading in headings:
            block = landing.fenced_section(text, heading, 'text')

            def changed_source(path, *args, **kwargs):
                content = original_read(path, *args, **kwargs)
                if path == source:
                    return content.replace(block, block + '\n<demo-update>&', 1) + '\nPRIVATE-DRAFT-SENTINEL'
                return content

            with self.subTest(heading=heading), patch.object(Path, 'read_text', changed_source):
                rendered = landing.render(landing.ROOT)
                self.assertIn(block, unescape(rendered))
                self.assertIn('&lt;demo-update&gt;&amp;', rendered)
                self.assertNotIn('<demo-update>', rendered)
                self.assertNotIn('PRIVATE-DRAFT-SENTINEL', rendered)
                self.assertNotIn('If you try it,', rendered)
                self.assertIn('href="#demo-source-notes"', rendered)
                self.assertIn('id="demo-source-notes"', rendered)

    def test_missing_demo_source_preserves_previous_public_artifact(self):
        original_read = Path.read_text
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'public'
            output.mkdir()
            previous = output / 'previous-build.txt'
            previous.write_text('Preserve until all content renders.')

            def missing_demo(path, *args, **kwargs):
                if path == landing.ROOT / 'docs/outreach-v0.2.5.md':
                    return 'No canonical demo blocks.'
                return original_read(path, *args, **kwargs)

            with patch.object(Path, 'read_text', missing_demo):
                with self.assertRaisesRegex(ValueError, 'Missing canonical section'):
                    landing.build(output=output)
            self.assertEqual(previous.read_text(), 'Preserve until all content renders.')

    def test_discovery_points_only_to_the_public_canonical_site(self):
        class Metadata(HTMLParser):
            def __init__(self):
                super().__init__()
                self.canonical = []
                self.open_graph = {}

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == 'link' and attrs.get('rel') == 'canonical':
                    self.canonical.append(attrs['href'])
                if tag == 'meta' and attrs.get('property', '').startswith('og:'):
                    self.open_graph[attrs['property']] = attrs['content']

        with tempfile.TemporaryDirectory() as temporary:
            output = landing.build(output=Path(temporary) / 'public')
            metadata = Metadata()
            metadata.feed((output / 'index.html').read_text(encoding='utf-8'))
            self.assertEqual(metadata.canonical, ['https://context-docs.com/'])
            self.assertEqual(metadata.open_graph['og:url'], metadata.canonical[0])
            self.assertEqual(metadata.open_graph['og:image'],
                             'https://context-docs.com/context-docs-overview.png')
            sitemap = ET.parse(output / 'sitemap.xml')
            # Every canonical route, in order; the legacy /reading-queue/ redirect is excluded.
            self.assertEqual([item.text for item in sitemap.findall('.//{*}loc')],
                             ['https://context-docs.com/', 'https://context-docs.com/getting-started/',
                              'https://context-docs.com/compare/', 'https://context-docs.com/examples/',
                              'https://context-docs.com/examples/reading-queue/',
                              'https://context-docs.com/examples/switching-codex-claude/',
                              'https://context-docs.com/examples/switching-claude-codex/',
                              'https://context-docs.com/experiments/',
                              'https://context-docs.com/experiments/markdown-maintenance/',
                              'https://context-docs.com/experiments/public-project-docs/'])
            # Each listed route is a built page whose canonical and og:url name that route.
            for route in landing.CANONICAL_ROUTES:
                page = Metadata()
                page.feed((output / route / 'index.html').read_text(encoding='utf-8'))
                self.assertEqual(page.canonical, [landing.SITE_URL + route], route)
                if 'og:url' in page.open_graph:
                    self.assertEqual(page.open_graph['og:url'], landing.SITE_URL + route, route)
            guide_metadata = Metadata()
            guide_metadata.feed((output / 'getting-started/index.html').read_text(encoding='utf-8'))
            self.assertEqual(guide_metadata.canonical, ['https://context-docs.com/getting-started/'])
            self.assertEqual(guide_metadata.open_graph['og:url'], guide_metadata.canonical[0])
            robots = urllib.robotparser.RobotFileParser()
            robots.parse((output / 'robots.txt').read_text(encoding='utf-8').splitlines())
            for bot in ['Googlebot', 'bingbot', 'OAI-SearchBot', 'Claude-SearchBot']:
                self.assertTrue(robots.can_fetch(bot, landing.SITE_URL))
            self.assertEqual(robots.site_maps(), [landing.SITE_URL + 'sitemap.xml'])

    def test_guide_reuses_canonical_instructions_and_example(self):
        rendered = unescape(landing.render(landing.ROOT, 'getting-started.html'))
        readme = (landing.ROOT / 'README.md').read_text(encoding='utf-8')
        for heading, language in [
            ('### Install in Codex', 'text'),
            ('### Install in Claude Code', 'sh'),
            ('### 2. Save decisions, current work and next steps', 'text'),
            ('### 3. Resume with the saved context', 'text'),
            ('## What you get', 'markdown'),
        ]:
            self.assertIn(landing.fenced_section(readme, heading, language), rendered)
        self.assertNotIn('{{', rendered)

    def test_comparison_has_native_baselines_fit_limits_and_resolving_navigation(self):
        class Links(HTMLParser):
            def __init__(self):
                super().__init__()
                self.hrefs = []
                self.canonical = []

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == 'a':
                    self.hrefs.append(attrs.get('href', ''))
                if tag == 'link' and attrs.get('rel') == 'canonical':
                    self.canonical.append(attrs['href'])

        original_read = Path.read_text

        def comparison_source_only(path, *args, **kwargs):
            self.assertIn(path, {landing.ROOT / 'site/compare.html'} |
                          {landing.ROOT / 'site/vendor/tabler' / (name + '.svg') for name in landing.ICONS})
            return original_read(path, *args, **kwargs)

        with patch.object(Path, 'read_text', comparison_source_only):
            rendered = landing.render_comparison(landing.ROOT)
        self.assertNotIn('{{', rendered)
        parser = Links()
        parser.feed(rendered)
        self.assertEqual(parser.canonical, ['https://context-docs.com/compare/'])
        for source in ['https://learn.chatgpt.com/docs/customization/memories',
                       'https://code.claude.com/docs/en/memory',
                       'https://docs.cline.bot/best-practices/memory-bank',
                       'https://oraios.github.io/serena/02-usage/045_memories.html#cli-subcommands',
                       'https://github.com/jaredchu/context-docs/blob/main/docs/project-decisions.md'
                       '#cursor-support-postponement']:
            self.assertIn(source, parser.hrefs)
        for text in ['Who it is for', 'What projects fit', 'What workflow fits',
                     'Skip it when', 'have not been demonstrated', '2026-10-24',
                     # Operating expectations must not imply implicit loading or concurrent safety.
                     'Operating expectations', 'dependable implicit loading',
                     'one writer per document', 'no safety guarantee for simultaneous writers']:
            self.assertIn(text, rendered)
        with tempfile.TemporaryDirectory() as temporary:
            output = landing.build(output=Path(temporary) / 'public')
            for name in ['index.html', 'getting-started/index.html']:
                nav = Links()
                nav.feed((output / name).read_text())
                links = [href for href in nav.hrefs if href.endswith('/compare/')]
                self.assertTrue(links, name)
                for href in links:
                    target = (output / name).parent / href / 'index.html'
                    self.assertTrue(target.is_file(), (name, href))

    def test_release_history_is_collapsed_after_actions_and_toc_links_are_list_items(self):
        class Structure(HTMLParser):
            void = {'br', 'img', 'meta', 'link', 'input'}

            def __init__(self):
                super().__init__()
                self.stack = []
                self.ids = {}
                self.toc_links = []

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                ancestors = list(self.stack)
                if 'id' in attrs:
                    self.ids.setdefault(attrs['id'], []).append(ancestors)
                if tag == 'a' and any('guide-toc' in (a.get('class') or '').split() for _, a in ancestors):
                    self.toc_links.append((attrs['href'], ancestors[-1][0]))
                if tag not in self.void:
                    self.stack.append((tag, attrs))

            def handle_endtag(self, tag):
                for index in range(len(self.stack) - 1, -1, -1):
                    if self.stack[index][0] == tag:
                        del self.stack[index:]
                        break

        for name in ['index.html', 'getting-started.html']:
            with self.subTest(page=name):
                rendered = landing.render(landing.ROOT, name)
                page = Structure()
                page.feed(rendered)
                # Fragment destinations survive once, inside a default-collapsed disclosure.
                for fragment in ['clarity', 'concurrency', 'metadata-filtering']:
                    self.assertEqual(len(page.ids.get(fragment, [])), 1, fragment)
                    details = [attrs for tag, attrs in page.ids[fragment][0] if tag == 'details']
                    self.assertEqual(len(details), 1, fragment)
                    self.assertNotIn('open', details[0])
                for smoke in ['clarity/smoke-0.2.4-2026-10-17', 'concurrency/smoke-0.2.5-2026-10-17',
                              'content-filtering/smoke-0.2.6-2026-10-19', 'progress/smoke-0.2.3-2026-10-17']:
                    self.assertEqual(rendered.count('evals/' + smoke + '/README.md'), 1, smoke)
                self.assertLess(rendered.index('id="save-prompt"'), rendered.index('id="release-details"'))
                main_path = re.sub(r'<details\b.*?</details>', '', rendered, flags=re.S)
                for text in ['do not establish broad reliability, privacy guarantees or effort savings',
                             'no automatic redaction', 'file locking']:
                    self.assertIn(text, main_path)
        guide = Structure()
        guide.feed(landing.render(landing.ROOT, 'getting-started.html'))
        self.assertEqual([href for href, _ in guide.toc_links][-3:], ['#progress', '#local-only', '#questions'])
        for href, parent in guide.toc_links:
            self.assertEqual(parent, 'li', href)
            self.assertEqual(len(guide.ids.get(href[1:], [])), 1, href)

    def test_reading_queue_is_an_explicit_public_source_and_fails_closed(self):
        original_read = Path.read_text

        def only_public_template(path, *args, **kwargs):
            self.assertIn(path, {landing.ROOT / 'site/reading-queue.html'} |
                          {landing.ROOT / 'site/vendor/tabler' / (name + '.svg') for name in landing.ICONS})
            return original_read(path, *args, **kwargs)

        with patch.object(Path, 'read_text', only_public_template):
            rendered = landing.render_reading_queue(landing.ROOT)
        self.assertNotIn('{{', rendered)
        for text in ['tutorial-start', 'tutorial-complete', 'Leave files unchanged',
                     'no controlled fresh-session performance study',
                     'not account-authenticated private storage',
                     'Documentation-only record commits']:
            self.assertIn(text, rendered)
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'public'
            output.mkdir()
            previous = output / 'previous-build.txt'
            previous.write_text('Preserve last valid output')

            def pending_demo(path, *args, **kwargs):
                if path == landing.ROOT / 'site/reading-queue.html':
                    return '{{SITE_URL}} DEMO_URL_PENDING'
                return original_read(path, *args, **kwargs)

            with patch.object(Path, 'read_text', pending_demo):
                with self.assertRaisesRegex(ValueError, 'demo URL'):
                    landing.build(output=output)
            self.assertEqual(previous.read_text(), 'Preserve last valid output')

    def test_worked_example_prompts_name_the_skill_only_at_adoption(self):
        class Prompts(HTMLParser):
            def __init__(self):
                super().__init__()
                self.active = None
                self.prompts = {}
                self.buttons = []
                self.ids = set()

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if 'id' in attrs:
                    self.ids.add(attrs['id'])
                if tag == 'code' and attrs.get('id', '').startswith('prompt-'):
                    self.active = attrs['id']
                    self.prompts[self.active] = ''
                if tag == 'button' and 'data-copy' in attrs:
                    self.buttons.append(attrs)

            def handle_endtag(self, tag):
                if tag == 'code':
                    self.active = None

            def handle_data(self, data):
                if self.active:
                    self.prompts[self.active] += data

        page = Prompts()
        page.feed(landing.render_reading_queue(landing.ROOT))
        self.assertEqual(len(page.prompts), 9)
        for name, prompt in page.prompts.items():
            if name == 'prompt-adopt':
                self.assertIn('adopt-context-docs', prompt)
            else:
                self.assertNotIn('context-docs', prompt.lower())
        self.assertNotIn('context', page.prompts['prompt-resume'].lower())
        for button in page.buttons:
            self.assertIn(button['data-copy'], page.prompts)
            self.assertIn(button['data-status'], page.ids)

    def test_invalid_comparison_preserves_previous_artifact(self):
        original_read = Path.read_text

        def invalid_comparison(path, *args, **kwargs):
            if path == landing.ROOT / 'site/compare.html':
                return '{{PRIVATE_NOTES}}'
            return original_read(path, *args, **kwargs)

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'public'
            output.mkdir()
            previous = output / 'previous-build.txt'
            previous.write_text('Keep previous build until all pages render.')
            with patch.object(Path, 'read_text', invalid_comparison):
                with self.assertRaisesRegex(ValueError, 'Comparison page'):
                    landing.build(output=output)
            self.assertEqual(previous.read_text(), 'Keep previous build until all pages render.')

    def test_local_only_guide_uses_only_canonical_public_prompts(self):
        rendered = unescape(landing.render(landing.ROOT, 'getting-started.html'))
        guide = (landing.ROOT / 'docs/getting-started.md').read_text(encoding='utf-8')
        for heading in ['## Local-only context (excluded from Git)',
                        '### Auto logging for local-only context']:
            self.assertIn(landing.fenced_section(guide, heading, 'text'), rendered)
        original_read = Path.read_text

        def forbid_private_sources(path, *args, **kwargs):
            relative = path.relative_to(landing.ROOT).as_posix()
            self.assertNotIn(relative, ['docs/project-context.md', 'docs/project-decisions.md'])
            self.assertFalse(relative.startswith('.context/'))
            return original_read(path, *args, **kwargs)

        with patch.object(Path, 'read_text', forbid_private_sources):
            landing.render(landing.ROOT, 'getting-started.html')

    def test_progress_prompt_uses_canonical_public_sources_on_both_pages(self):
        readme = (landing.ROOT / 'README.md').read_text()
        prompt = landing.fenced_section(readme, '### 4. Visualize progress in Markdown', 'text')
        original_read = Path.read_text
        public_inputs = {
            'README.md', 'examples/maintenance.md', 'examples/progress.md', 'docs/getting-started.md',
            'docs/outreach-v0.2.5.md',
            'skills/context-docs/VERSION', 'skills/adopt-context-docs/VERSION',
            'site/index.html', 'site/getting-started.html',
        }
        public_inputs |= {'site/vendor/tabler/' + name + '.svg' for name in landing.ICONS}

        def public_sources_only(path, *args, **kwargs):
            self.assertIn(path.relative_to(landing.ROOT).as_posix(), public_inputs)
            return original_read(path, *args, **kwargs)

        with patch.object(Path, 'read_text', public_sources_only):
            for name in ['index.html', 'getting-started.html']:
                rendered = landing.render(landing.ROOT, name)
                self.assertIn(prompt, unescape(rendered))
                self.assertIn('id="progress"', rendered)

    def test_both_pages_show_the_canonical_visual_with_clickable_source_map(self):
        example = landing.fenced_section((landing.ROOT / 'examples/progress.md').read_text(),
                                         '## Example Markdown view', 'text')
        for name in ['index.html', 'getting-started.html']:
            rendered = landing.render(landing.ROOT, name)
            self.assertIn(example, unescape(rendered))
            # Source links must be usable outside the preformatted diagram.
            outside_diagrams = re.sub(r'<pre\b[^>]*>.*?</pre>', '', rendered, flags=re.S)
            for anchor in ['source-goal-and-decisions', 'source-checks-and-open-work']:
                self.assertIn('href="https://github.com/jaredchu/context-docs/blob/main/examples/progress.md#'
                              + anchor + '"', outside_diagrams)

    def test_missing_required_examples_preserve_previous_public_artifact(self):
        original_read = Path.read_text
        cases = [(name, marker) for name in ['index.html', 'getting-started.html']
                 for marker in ['PROGRESS_PROMPT', 'PROGRESS_EXAMPLE']]
        cases += [('index.html', marker) for marker in ['DEMO_NOTES', 'DEMO_CONTEXT', 'DEMO_RESUME']]
        cases += [('getting-started.html', marker) for marker in
                  ['REFRESH_PROMPT', 'VERIFY_RESUME_PROMPT', 'TROUBLESHOOT_PROMPT']]
        for name, marker in cases:
            with self.subTest(template=name, marker=marker), tempfile.TemporaryDirectory() as temporary:
                output = Path(temporary) / 'public'
                output.mkdir()
                previous = output / 'previous-build.txt'
                previous.write_text('Preserve until all content renders.')

                def missing_progress(path, *args, **kwargs):
                    text = original_read(path, *args, **kwargs)
                    if path == landing.ROOT / 'site' / name:
                        return text.replace('{{' + marker + '}}', '')
                    return text

                with patch.object(Path, 'read_text', missing_progress):
                    with self.assertRaisesRegex(ValueError, 'Missing template markers'):
                        landing.build(output=output)
                self.assertEqual(previous.read_text(), 'Preserve until all content renders.')

    def test_seo_titles_have_no_em_dash(self):
        class Titles(HTMLParser):
            def __init__(self):
                super().__init__()
                self.inside_title = False
                self.values = []

            def handle_starttag(self, tag, attrs):
                self.inside_title = tag == 'title'
                attrs = dict(attrs)
                if tag == 'meta' and (attrs.get('property') == 'og:title' or
                                      attrs.get('name') == 'twitter:title'):
                    self.values.append(attrs['content'])

            def handle_endtag(self, tag):
                if tag == 'title':
                    self.inside_title = False

            def handle_data(self, text):
                if self.inside_title:
                    self.values.append(text)

        for page in ['index.html', 'getting-started.html']:
            titles = Titles()
            titles.feed(landing.render(landing.ROOT, page))
            self.assertGreaterEqual(len(titles.values), 2)
            for value in titles.values:
                self.assertNotIn('\u2014', value)

    def test_package_release_status_follows_readme(self):
        original_read = Path.read_text
        for released, capitalized in [(False, False), (False, True), (True, False)]:
            def status_source(path, *args, **kwargs):
                text = original_read(path, *args, **kwargs)
                if path == landing.ROOT / 'README.md':
                    # Exercise both states independently of the current release status.
                    text = text.replace(' (unreleased)', '').replace(' (Unreleased)', '')
                    if not released:
                        suffix = ' (Unreleased)' if capitalized else ' (unreleased)'
                        text, count = re.subn(r'^(\*\*Status: .*?)(\*\*)$',
                                      lambda match: match[1] + suffix + match[2], text, flags=re.M)
                        self.assertEqual(count, 1)
                    return text
                return text

            with self.subTest(released=released), patch.object(Path, 'read_text', status_source):
                for page in ['index.html', 'getting-started.html']:
                    self.assertIn('Experimental · ' + ('Released' if released else 'Unreleased'),
                                  landing.render(landing.ROOT, page))

    def test_missing_package_status_does_not_claim_a_release(self):
        original_read = Path.read_text

        def missing_status(path, *args, **kwargs):
            text = original_read(path, *args, **kwargs)
            if path == landing.ROOT / 'README.md':
                return '\n'.join(line for line in text.splitlines() if not line.startswith('**Status:'))
            return text

        with patch.object(Path, 'read_text', missing_status):
            for page in ['index.html', 'getting-started.html']:
                with self.assertRaisesRegex(ValueError, 'Missing canonical package status'):
                    landing.render(landing.ROOT, page)

    def test_each_page_fails_closed_when_required_content_is_removed(self):
        original_read = Path.read_text
        for name in ['index.html', 'getting-started.html']:
            with self.subTest(template=name):
                def missing_prompt(path, *args, **kwargs):
                    content = original_read(path, *args, **kwargs)
                    if path == landing.ROOT / 'site' / name:
                        return content.replace('{{SAVE_PROMPT}}', '')
                    return content
                with patch.object(Path, 'read_text', missing_prompt):
                    with self.assertRaisesRegex(ValueError, 'Missing template markers'):
                        landing.render(landing.ROOT, name)

    def test_missing_block_does_not_steal_next_sections_command(self):
        with self.assertRaises(ValueError):
            landing.fenced_section('## First\nNo command\n## Second\n```sh\necho wrong\n```', '## First', 'sh')
        with self.assertRaises(ValueError):
            landing.fenced_section('## First\n```sh\nunclosed', '## First', 'sh')

    def test_markdown_headings_inside_example_survive(self):
        text = '## Example\n```markdown\n# Context\n\n## Decision\nApproved.\n```\n## Next'
        self.assertEqual('# Context\n\n## Decision\nApproved.', landing.fenced_section(text, '## Example', 'markdown'))

    def test_verify_resume_prompt_is_canonical_read_only_and_available_without_scripts(self):
        guide = (landing.ROOT / 'docs/getting-started.md').read_text(encoding='utf-8')
        heading = '### Verify a resumed session\n'
        # The former deep link stays a small alias directly at the short check.
        self.assertIn('<a id="first-handoff-check"></a>\n\n' + heading, guide)
        section = guide.split(heading, 1)[1].split('\n### ', 1)[0]
        expected = re.findall(r'^```text\n(.*?)\n```$', section, re.S | re.M)
        self.assertEqual(len(expected), 1)
        prompt = expected[0]
        for text in ['read-only', 'Cite the file and', 'missing rather than guessing',
                     'do not change files or continue implementation']:
            self.assertIn(text, prompt)

        html = landing.render(landing.ROOT, 'getting-started.html')
        page = parse(html)
        self.assertEqual(page.code['verify-resume-prompt'], prompt)
        button = next(b for b in page.buttons if b['data-copy'] == 'verify-resume-prompt')
        self.assertIn(button['data-status'], page.ids)
        self.assertIn('hidden', button)
        self.assertNotEqual(button['data-status'], 'resume-status')
        # Both anchors resolve inside Resume; neither is a separate section or TOC entry.
        start = html.index('<section id="resume"')
        resume = html[start:html.index('<section', start + 1)]
        for anchor in ['verify-a-resumed-session', 'first-handoff-check']:
            self.assertIn('id="' + anchor + '"', resume)
            self.assertNotIn('<section id="' + anchor + '"', html)
        self.assertIn('id="verify-resume-prompt"', resume)
        self.assertNotIn('<details', resume)
        toc = re.search(r'<nav class="guide-toc".*?</nav>', html, re.S)[0]
        self.assertNotIn('handoff', toc)
        self.assertNotIn('verify', toc)
        self.assertIn('href="#troubleshoot-setup-and-saved-context"', toc)
        for text in ['not automatic loading', 'href="../examples/reading-queue/"',
                     '#moving-shared-context-to-another-checkout']:
            self.assertIn(text, resume)
        # The disposable synthetic exercise is gone from the guide, the page and the README.
        readme = (landing.ROOT / 'README.md').read_text(encoding='utf-8')
        for removed in ['Handoff practice', 'disposable practice', 'SQLite for the pilot', 'handoff-save',
                        'handoff-receive', 'handoff-checklist']:
            self.assertNotIn(removed, html)
            self.assertNotIn(removed, guide)
        self.assertNotIn('#first-handoff-check', readme)
        # The README offers the check only within its Resume step.
        resume_step = readme.split('### 3. Resume with the saved context\n', 1)[1].split('\n### ', 1)[0]
        self.assertIn('docs/getting-started.md#verify-a-resumed-session', resume_step)
        self.assertEqual(readme.count('#verify-a-resumed-session'), 1)

    def test_verify_resume_prompt_updates_are_escaped_and_missing_source_fails_closed(self):
        source = landing.ROOT / 'docs/getting-started.md'
        original_read = Path.read_text
        prompt = landing.fenced_section(source.read_text(encoding='utf-8'), '### Verify a resumed session', 'text')

        def updated(path, *args, **kwargs):
            text = original_read(path, *args, **kwargs)
            if path == source:
                return text.replace(prompt, prompt + '\n<verify-update>&', 1) + '\nUNSELECTED-VERIFY-NOTE\n'
            return text

        with patch.object(Path, 'read_text', updated):
            html = landing.render(landing.ROOT, 'getting-started.html')
        self.assertEqual(parse(html).code['verify-resume-prompt'], prompt + '\n<verify-update>&')
        self.assertIn('&lt;verify-update&gt;&amp;', html)
        self.assertNotIn('<verify-update>', html)
        self.assertNotIn('UNSELECTED-VERIFY-NOTE', html)

        def missing_section(path, *args, **kwargs):
            text = original_read(path, *args, **kwargs)
            if path == source:
                return text.replace('### Verify a resumed session\n', '### Renamed check\n', 1)
            return text

        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'public'
            output.mkdir()
            previous = output / 'previous-build.txt'
            previous.write_text('Preserve until all content renders.')
            with patch.object(Path, 'read_text', missing_section):
                with self.assertRaisesRegex(ValueError, 'Missing canonical section'):
                    landing.build(output=output)
            self.assertEqual(previous.read_text(), 'Preserve until all content renders.')

    def test_troubleshooting_prompt_is_canonical_collapsed_and_qualified(self):
        guide = (landing.ROOT / 'docs/getting-started.md').read_text(encoding='utf-8')
        heading = '### Troubleshoot setup and saved context'
        prompt = landing.fenced_section(guide, heading, 'text')
        self.assertTrue(prompt.startswith('Troubleshoot Context Docs setup and saved context'))
        self.assertTrue(prompt.endswith('Do not certify accuracy, freshness or successful loading.'))
        for constraint in ['This is read-only.', 'Do not\nenumerate, search or read event journals',
                           'Report loading as "not verified by this check".',
                           'Suggest repairs without executing them.']:
            self.assertIn(constraint, prompt)
        # The guide suggests the ordinary audit first and this prompt as the fallback.
        intro = guide.split(heading + '\n', 1)[1].split('```text', 1)[0]
        for text in ['audit', 'unavailable', 'without invoking a skill']:
            self.assertIn(text, intro)
        html = landing.render(landing.ROOT, 'getting-started.html')
        page = parse(html)
        self.assertEqual(page.code['troubleshoot-prompt'], prompt)
        section = html[html.index('id="troubleshoot-setup-and-saved-context"'):html.index('id="progress"')]
        disclosure = re.search(r'<details id="troubleshoot-prompt-details"[^>]*>.*?</details>', section, re.S)[0]
        self.assertNotRegex(disclosure.split('>', 1)[0], r'\bopen\b')
        self.assertIn('id="troubleshoot-prompt"', disclosure)
        self.assertIn('data-copy="troubleshoot-prompt"', disclosure)
        # The long prompt is collapsed; its read-only scope and loading limit stay visible.
        visible = unescape(section.replace(disclosure, ''))
        for text in ['audit prompt', 'unavailable', 'without invoking a skill', 'read-only',
                     'not verified by this check', 'Behavior in a newly opened client and newcomer usability remain untested',
                     '#install-in-codex', '#install-in-claude-code']:
            self.assertIn(text, visible)

    def test_every_canonical_page_has_the_same_main_menu_and_correct_current_marker(self):
        menu = ['Overview', 'Guide', 'Examples', 'Experiments', 'GitHub']
        local_targets = {'Overview': '', 'Guide': 'getting-started', 'Examples': 'examples',
                         'Experiments': 'experiments'}
        github = 'https://github.com/jaredchu/context-docs'
        with tempfile.TemporaryDirectory() as temporary:
            output = landing.build(output=Path(temporary) / 'public')
            self.assertEqual(len(landing.CANONICAL_ROUTES), 10)
            for route in landing.CANONICAL_ROUTES:
                name = route + 'index.html'
                with self.subTest(page=name):
                    html = (output / name).read_text(encoding='utf-8')
                    page = parse(html)
                    nav = [link for link in page.links if link['nav']]
                    self.assertEqual([link['text'].strip() for link in nav], menu)
                    self.assertEqual(html.count('class="site-nav"'), 1)
                    for link in nav:
                        label, href = link['text'].strip(), link['attrs']['href']
                        if label == 'GitHub':
                            self.assertEqual(href, github)
                            continue
                        self.assertFalse(SCHEME.match(href), href)
                        target = ((output / name).parent / href).resolve()
                        expected = (output / local_targets[label]).resolve()
                        self.assertEqual(target, expected, label)
                        self.assertTrue((target / 'index.html').is_file(), label)
                    if route == '':
                        expected_current = ('Overview', 'page')
                    elif route == 'getting-started/':
                        expected_current = ('Guide', 'page')
                    elif route in ('examples/', 'experiments/'):
                        expected_current = (route[:-1].capitalize(), 'page')
                    elif route.startswith(('examples/', 'experiments/')):
                        expected_current = (route.split('/')[0].capitalize(), 'true')
                    else:
                        self.assertEqual(route, 'compare/')
                        expected_current = None
                    marked = [(link['text'].strip(), link['attrs']['aria-current'])
                              for link in nav if 'aria-current' in link['attrs']]
                    self.assertEqual(marked, [expected_current] if expected_current else [])
                    # Compare stays reachable from page content or the footer, not the main menu.
                    if route != 'compare/':
                        compare = [link for link in page.links if not link['nav']
                                   and ((output / name).parent / link['attrs']['href'].partition('#')[0]).resolve()
                                   == (output / 'compare').resolve()]
                        self.assertTrue(compare, name)
                    # The logo returns home.
                    brand = re.search(r'<a class="brand" href="([^"]+)"', html)[1]
                    self.assertEqual(((output / name).parent / brand).resolve(), output.resolve())
                    # Only the redirect page itself may point at the legacy location.
                    self.assertNotIn('context-docs.com/reading-queue', html)
                    for link in page.links:
                        relative = link['attrs']['href'].partition('#')[0]
                        if relative and not SCHEME.match(relative):
                            self.assertNotEqual(((output / name).parent / relative).resolve(),
                                                (output / 'reading-queue').resolve(), link['attrs']['href'])

    def test_assets_resolve_and_ids_are_unique_at_every_page_depth(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = landing.build(output=Path(temporary) / 'public')
            root = output.resolve()
            for path in output.rglob('*.html'):
                with self.subTest(page=path.relative_to(output).as_posix()):
                    page = parse(path.read_text(encoding='utf-8'))
                    self.assertTrue(any(ref.endswith('styles.css') for ref in page.assets))
                    for ref in page.assets:
                        self.assertFalse(SCHEME.match(ref), ref)
                        target = (path.parent / ref).resolve()
                        self.assertTrue(target.is_file(), ref)
                        self.assertIn(root, target.parents, ref)
                    self.assertEqual(len(page.id_list), len(page.ids))

    def test_legacy_reading_queue_route_redirects_with_query_and_fragment(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = landing.build(output=Path(temporary) / 'public')
            html = (output / 'reading-queue/index.html').read_text(encoding='utf-8')
            page = parse(html)
            moved = parse((output / 'examples/reading-queue/index.html').read_text(encoding='utf-8'))
            sitemap = (output / 'sitemap.xml').read_text(encoding='utf-8')
        relative = '../examples/reading-queue/'
        self.assertEqual(page.canonical, [landing.SITE_URL + 'examples/reading-queue/'])
        self.assertEqual(page.refresh, ['0; url=' + relative])
        self.assertIn(relative, [link['attrs']['href'] for link in page.links])
        script = ''.join(page.scripts)
        target = re.search(r"new URL\('([^']+)', window\.location\.href\)", script)
        self.assertIsNotNone(target)
        # A relative target keeps preview hosts and the live site on their own origin.
        self.assertEqual(target[1], relative)
        self.assertIn('target.search = window.location.search;', script)
        self.assertIn('target.hash = window.location.hash;', script)
        self.assertIn('window.location.replace(target.href);', script)
        self.assertLess(html.index('location.replace'), html.index('http-equiv="refresh"'))
        self.assertNotIn(landing.SITE_URL + 'reading-queue/', sitemap)
        # Reproduce the script's URL arithmetic; fragments must exist on the moved page.
        for old, expected in [
            ('https://context-docs.com/reading-queue/?ref=post&x=1#verify',
             'https://context-docs.com/examples/reading-queue/?ref=post&x=1#verify'),
            ('https://context-docs.com/reading-queue/index.html#prompt-resume',
             'https://context-docs.com/examples/reading-queue/#prompt-resume'),
            ('https://context-docs.com/reading-queue/',
             'https://context-docs.com/examples/reading-queue/'),
        ]:
            with self.subTest(old=old):
                parts = urllib.parse.urlsplit(old)
                joined = urllib.parse.urlsplit(urllib.parse.urljoin(old, target[1]))
                self.assertEqual(joined._replace(query=parts.query, fragment=parts.fragment).geturl(), expected)
                if parts.fragment:
                    self.assertIn(parts.fragment, moved.ids)

    def test_moved_reading_queue_keeps_anchors_prompts_and_external_urls(self):
        rendered = landing.render_reading_queue(landing.ROOT)
        page = parse(rendered)
        self.assertLessEqual(READING_QUEUE_IDS, page.ids)
        self.assertEqual(set(page.code), {'prompt-' + step for step in READING_QUEUE_STEPS})
        self.assertEqual(page.canonical, [landing.SITE_URL + 'examples/reading-queue/'])
        self.assertIn('property="og:url" content="https://context-docs.com/examples/reading-queue/"', rendered)
        hrefs = [link['attrs']['href'] for link in page.links]
        for url in ['https://context-docs-example-reading-queue.viweb.workers.dev',
                    'https://github.com/jaredchu/context-docs-example-reading-queue',
                    'https://github.com/jaredchu/context-docs-example-reading-queue/tree/tutorial-complete',
                    'https://developers.cloudflare.com/d1/reference/migrations/']:
            self.assertIn(url, hrefs)
        for href in hrefs:
            if SCHEME.match(href):
                self.assertNotIn('../', href)
        self.assertIn('../switching-codex-claude/', hrefs)
        self.assertIn('../switching-claude-codex/', hrefs)

    def test_switching_walkthroughs_have_direction_specific_prompts_and_copy_controls(self):
        skills = {'codex': '$adopt-context-docs', 'claude': '/adopt-context-docs'}
        names = {'codex': 'Codex', 'claude': 'Claude Code'}
        evidence = 'https://github.com/jaredchu/context-docs/blob/main/docs/switching-agents-examples.md'
        starts, continues = [], []
        for outgoing, incoming in [('codex', 'claude'), ('claude', 'codex')]:
            direction = outgoing + '-' + incoming
            template = 'switching-' + direction + '.html'
            with self.subTest(direction=direction):
                html = landing.render_page(landing.ROOT, template, template)
                page = parse(html)
                expected = {'setup-' + direction, f'prompt-{outgoing}-adopt', f'prompt-{incoming}-adopt',
                            f'prompt-{outgoing}-start', f'prompt-{incoming}-continue'}
                self.assertEqual(set(page.code), expected)
                self.assertEqual({button['data-copy'] for button in page.buttons}, expected)
                for button in page.buttons:
                    self.assertIn(button['data-status'], page.ids)
                    copy_id = button['data-copy']
                    expected_destination = (names[copy_id.split('-')[1]] if copy_id.startswith('prompt-')
                                            else 'your terminal')
                    self.assertEqual(button['data-destination'], expected_destination, copy_id)
                setup = page.code['setup-' + direction]
                for command in ['https://github.com/jaredchu/context-docs-example-reading-queue.git',
                                'git switch -c try-' + direction + ' switching-start', 'npm ci', 'npm test']:
                    self.assertIn(command, setup)
                for client, skill in skills.items():
                    self.assertTrue(page.code[f'prompt-{client}-adopt'].startswith(skill + ' '))
                self.assertLess(html.index(f'id="prompt-{outgoing}-adopt"'), html.index(f'id="prompt-{incoming}-adopt"'))
                start = page.code[f'prompt-{outgoing}-start']
                for text in ['GET /api/export', '{"schema_version":1,"items":[]}', 'title, url and read',
                             'entire active queue', 'regardless of any UI filter', 'isolation and expiry',
                             'no identifiers, cookie values or database metadata', 'do not change any data',
                             'exercise clarification', 'do not rewrite the requirement',
                             'backup of the whole queue', 'no schema or cloud changes',
                             'Stop before the browser Export JSON button', 'docs/project-context.md',
                             'docs/decisions.md', 'browser integration is pending', 'Do not deploy']:
                    self.assertIn(text, start)
                resume = page.code[f'prompt-{incoming}-continue']
                # The receiver must recover the feature from saved files, not from the prompt.
                for leaked in ['export', 'schema', 'button', '/api', 'browser', 'filter', 'backup', 'json']:
                    self.assertNotIn(leaked, resume.lower())
                for text in ['context entry point', 'complete', 'pending and why', 'current files',
                             'next authorized task', 'actually ran', 'blockers', 'existing notes', 'Do not deploy']:
                    self.assertIn(text, resume)
                starts.append(start)
                continues.append(resume)
                hrefs = [link['attrs']['href'] for link in page.links]
                self.assertIn('../switching-' + incoming + '-' + outgoing + '/', hrefs)
                self.assertIn('../', hrefs)
                self.assertIn(evidence, hrefs)
                figure = re.search(r'<figure class="guide-example">.*?</figure>', html, re.S)[0]
                self.assertIn('not recorded agent output', figure)
                self.assertIn('&lt;your actual result&gt;', figure)
                for claim in ['API tests do not cover', 'not a study', 'no sync, file locking',
                              'Ignored or private files do not travel with Git', 'you do not need to commit']:
                    self.assertIn(claim, html)
        # Both directions run the same task; only the clients differ.
        self.assertEqual(starts[0], starts[1])
        self.assertEqual(continues[0], continues[1])

    def test_examples_hub_offers_three_cards_and_home_links_switching_through_it(self):
        hub = landing.render_page(landing.ROOT, 'examples.html', 'Examples page')
        page = parse(hub)
        self.assertEqual(hub.count('<li class="example-card'), 3)
        hrefs = [link['attrs']['href'] for link in page.links]
        for target in ['reading-queue/', 'switching-codex-claude/', 'switching-claude-codex/']:
            self.assertIn(target, hrefs)
        self.assertIn('switching', page.ids)
        home = landing.render(landing.ROOT)
        resume = home[home.index('id="resume-prompt"'):home.index('id="release-details"')]
        self.assertIn('href="./examples/#switching"', resume)
        self.assertIn('Your next session.<br><span>Less starting over.</span>', home)

    def test_experiments_index_lists_both_reports_newest_first_with_qualified_summaries(self):
        repo = 'https://github.com/jaredchu/context-docs/blob/main/'
        expected = [
            ('public-project-docs', '2026-11-14', 'docs/evaluation-2026-11-14-public-project-docs.md',
             'evals/results/2026-11-14-public-project-docs/README.md',
             ['agent-only', 'did not outperform ordinary Markdown', 'disputes remain unresolved',
              'unreconciled', 'not measured']),
            ('markdown-maintenance', '2026-11-13', 'docs/evaluation-2026-11-13-markdown-maintenance.md',
             'evals/results/2026-11-13-markdown-maintenance/README.md',
             ['agent-only', 'favored ordinary Markdown', 'no clean three-pair average',
              'neither a Context Docs advantage nor general equivalence', 'not measured']),
        ]
        with tempfile.TemporaryDirectory() as temporary:
            output = landing.build(output=Path(temporary) / 'public')
            index = output / 'experiments/index.html'
            html = index.read_text(encoding='utf-8')
            cards = re.findall(r'<li id="([^"]+)" class="[^"]*\bexperiment-card\b[^"]*">(.*?)</li>\s*(?=<li id=|</ol>)',
                               html, re.S)
            self.assertEqual([card_id for card_id, _ in cards], [slug for slug, *_ in expected])
            dates = [re.search(r'<time datetime="([^"]+)">', body)[1] for _, body in cards]
            self.assertEqual(dates, sorted(dates, reverse=True))
            for (card_id, body), (slug, date, report, evidence, phrases) in zip(cards, expected):
                with self.subTest(card=card_id):
                    markdown = (landing.ROOT / report).read_text(encoding='utf-8').splitlines()
                    # Titles and dates come from the canonical reports.
                    self.assertEqual(unescape(re.search(r'<h3>(.*?)</h3>', body, re.S)[1]), markdown[0][2:])
                    self.assertEqual(dates[[c for c, _ in cards].index(card_id)], date)
                    shown_date = re.search(r'<time datetime="[^"]+">([^<]+)</time>', body)[1]
                    self.assertTrue(markdown[2].startswith('**' + shown_date + ' · '), markdown[2])
                    for heading in ['What was tested', 'Observed result', 'Qualifications']:
                        self.assertIn('<h4>' + heading + '</h4>', body)
                    text = unescape(re.sub(r'<[^>]+>', ' ', body))
                    text = re.sub(r'\s+', ' ', text)
                    for phrase in phrases:
                        self.assertIn(phrase, text)
                    hrefs = re.findall(r'<a\b[^>]*href="([^"]+)"', body)
                    self.assertEqual(hrefs, [slug + '/', repo + report, repo + evidence])
                    self.assertTrue((index.parent / slug / 'index.html').is_file())
                    for source in (report, evidence):
                        self.assertTrue((landing.ROOT / source).is_file(), source)
            # Summaries stay qualified: no advantage, speed, effort-saving or benchmark claims.
            visible = re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', html))).lower()
            self.assertNotRegex(visible, r'\b(?:outperformed|outperforms|superior|better than|faster|'
                                         r'saves? (?:time|effort)|time savings|effort savings|benchmark|proves?)\b')
            for text in ['exploratory', 'agent-only', 'does not copy evaluation files',
                         'not public evidence', 'read the full report before relying on a number']:
                self.assertIn(text, visible)
            self.assertIn('href="' + repo + 'docs/evaluation-results.md"', html)
            self.assertIn('href="../compare/"', html)

    def test_experiment_artifact_copies_no_evidence_or_private_paths(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = landing.build(output=Path(temporary) / 'public')
            experiment_files = {p.relative_to(output).as_posix()
                                for p in (output / 'experiments').rglob('*') if p.is_file()}
            self.assertEqual(experiment_files, {'experiments/index.html',
                                                'experiments/markdown-maintenance/index.html',
                                                'experiments/public-project-docs/index.html'})
            self.assertFalse(list(output.rglob('*.json')))
            self.assertFalse(list(output.rglob('*.md')))
            for path in (output / 'experiments').rglob('*.html'):
                html = path.read_text(encoding='utf-8')
                self.assertNotRegex(html, r'/Users/|/Volumes/|<script|\.context/|operator-notes')

    def test_report_pages_link_back_to_the_index_outside_the_canonical_article(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = landing.build(output=Path(temporary) / 'public')
            for slug in ['markdown-maintenance', 'public-project-docs']:
                with self.subTest(report=slug):
                    path = output / 'experiments' / slug / 'index.html'
                    html = path.read_text(encoding='utf-8')
                    start, end = html.index('<article id="experiment-report">'), html.index('</article>')
                    outside = html[:start] + html[end:]
                    backs = re.findall(r'<p class="report-back[^"]*"><a class="text-link" href="([^"]+)">', outside)
                    self.assertEqual(len(backs), 2)
                    for href in backs:
                        self.assertEqual((path.parent / href).resolve(), (output / 'experiments').resolve())
                    self.assertNotIn('report-back', html[start:end])
            home = (output / 'index.html').read_text(encoding='utf-8')
            # Homepage discovery adds the index while keeping both direct report links.
            for href in ['experiments/', 'experiments/public-project-docs/', 'experiments/markdown-maintenance/']:
                self.assertIn('href="' + href + '"', home)
            self.assertIn('<a href="./experiments/">Experiments</a>', home.split('class="site-footer"', 1)[1])

    def test_invalid_new_pages_preserve_previous_artifact_and_unknown_markers_fail(self):
        original_read = Path.read_text
        for template in ['examples.html', 'switching-codex-claude.html', 'switching-claude-codex.html',
                         'reading-queue.html', 'experiments.html', 'experiment.html',
                         'public-project-experiment.html']:
            with self.subTest(template=template), tempfile.TemporaryDirectory() as temporary:
                output = Path(temporary) / 'public'
                output.mkdir()
                previous = output / 'previous-build.txt'
                previous.write_text('Keep previous build until all pages render.')

                def invalid_page(path, *args, **kwargs):
                    text = original_read(path, *args, **kwargs)
                    if path == landing.ROOT / 'site' / template:
                        return text + '{{PRIVATE_NOTES}}'
                    return text

                with patch.object(Path, 'read_text', invalid_page):
                    with self.assertRaisesRegex(ValueError, 'only the SITE_URL marker'):
                        landing.build(output=output)
                self.assertEqual(previous.read_text(), 'Keep previous build until all pages render.')
        with self.assertRaisesRegex(ValueError, 'unknown or malformed marker'):
            landing.render_site_url_only(landing.ROOT, '{{SITE_URL}} {{lower_case}}', 'Test page')
        with self.assertRaisesRegex(ValueError, 'only the SITE_URL marker'):
            landing.render_site_url_only(landing.ROOT, 'No canonical marker', 'Test page')

    def test_symlink_destination_cannot_overwrite_other_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / 'keep'
            target.mkdir()
            (target / 'note').write_text('keep')
            link = base / 'output'
            link.symlink_to(target, target_is_directory=True)
            with self.assertRaises(ValueError):
                landing.build(output=link)
            self.assertEqual('keep', (target / 'note').read_text())


if __name__ == '__main__':
    unittest.main()
