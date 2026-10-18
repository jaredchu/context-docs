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
                'getting-started/index.html'})
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
                             ['https://context-docs.com/', 'https://context-docs.com/getting-started/'])
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
