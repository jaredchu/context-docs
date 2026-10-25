"""Boundary and canonical-content checks for the public website artifact."""
import importlib.util
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
from html import unescape
from html.parser import HTMLParser
import urllib.robotparser
import xml.etree.ElementTree as ET

SPEC = importlib.util.spec_from_file_location('landing_build', Path(__file__).with_name('build.py'))
landing = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(landing)


class LandingBuildTests(unittest.TestCase):
    def test_artifact_contains_only_allowlisted_files_even_after_dirty_build(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'public'
            output.mkdir()
            (output / 'private-note.txt').write_text('Must not survive a rebuild')
            landing.build(output=output)
            self.assertEqual({p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}, {
                'index.html', 'styles.css', 'main.js', 'favicon.svg',
                'context-docs-overview.png', '.nojekyll', 'robots.txt', 'sitemap.xml',
                'getting-started/index.html', 'compare/index.html', 'reading-queue/index.html'})
            self.assertFalse(any(p.is_symlink() for p in output.rglob('*')))
            self.assertEqual((output / 'context-docs-overview.png').read_bytes(),
                             (landing.ROOT / 'assets/context-docs-overview.png').read_bytes())

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
            self.assertEqual([item.text for item in sitemap.findall('.//{*}loc')],
                             ['https://context-docs.com/', 'https://context-docs.com/getting-started/',
                              'https://context-docs.com/compare/', 'https://context-docs.com/reading-queue/'])
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
            self.assertEqual(path, landing.ROOT / 'site/compare.html')
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
            self.assertEqual(path, landing.ROOT / 'site/reading-queue.html')
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
