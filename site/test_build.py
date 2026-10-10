"""Boundary and canonical-content checks for the public website artifact."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from html import unescape

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
            self.assertEqual({p.name for p in output.iterdir()}, {
                'index.html', 'styles.css', 'main.js', 'favicon.svg',
                'context-docs-overview.png', '.nojekyll'})
            self.assertFalse(any(p.is_dir() or p.is_symlink() for p in output.iterdir()))
            self.assertEqual((output / 'context-docs-overview.png').read_bytes(),
                             (landing.ROOT / 'assets/context-docs-overview.png').read_bytes())

    def test_commands_and_example_are_canonical(self):
        rendered = unescape(landing.render(landing.ROOT))
        for path, heading, language in [
            ('README.md', '### Install in Codex', 'text'),
            ('README.md', '### Install in Claude Code', 'sh'),
            ('README.md', '### 2. Work normally, then save useful changes', 'text'),
            ('README.md', '### 3. Resume with the saved context', 'text'),
            ('examples/maintenance.md', '## Before: existing context.md', 'markdown'),
            ('examples/maintenance.md', '## After: same context.md', 'markdown'),
        ]:
            block = landing.fenced_section((landing.ROOT / path).read_text(), heading, language)
            self.assertIn(block, rendered)
        self.assertNotIn('{{', rendered)

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
