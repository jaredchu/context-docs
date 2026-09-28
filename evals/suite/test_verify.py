"""Check bounded installed references without weakening project preservation."""
import hashlib
import tempfile
import unittest
from pathlib import Path

from verify import grade, link_errors


class ExternalReferenceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        base = Path(temporary.name)
        self.root, self.output = base / 'project', base / 'output'
        self.root.mkdir()
        self.output.mkdir()
        self.installed = base / 'installed'
        self.installed.mkdir()
        self.skill = self.installed / 'SKILL.md'
        self.skill.write_text('# Context Docs\n\nInstalled fixture.\n')
        self.before = {'README.md': '# Context\n', 'AGENTS.md': '# Instructions\n'}
        for name, body in self.before.items():
            (self.root / name).write_text(body)
        self.spec = dict(id='installed-reference', before=self.before, protected=[],
                         immutable=['README.md'], entry='README.md', allow_noop=False,
                         external_references={str(self.skill): hashlib.sha256(self.skill.read_bytes()).hexdigest()},
                         external_reference_roots=[str(self.installed)])

    def use(self, reference):
        (self.root / 'AGENTS.md').write_text('# Instructions\n\nUse ' + reference + '.\n')
        return grade(self.spec, self.root, self.output)

    def forms(self, target):
        return [f'[skill]({target})', f'`{target}`', target]

    def test_existing_declared_reference_passes_in_each_form(self):
        for reference in self.forms(str(self.skill)):
            with self.subTest(reference=reference):
                result = self.use(reference)
                self.assertTrue(result['mechanical_pass'], result)
                self.assertEqual({'README.md', 'AGENTS.md'}, set(result['documents']))

    def test_missing_reference_fails_in_each_form(self):
        for reference in self.forms(str(self.installed / 'absent.md')):
            with self.subTest(reference=reference):
                result = self.use(reference)
                self.assertFalse(result['checks']['local_links_and_anchors'])
                self.assertTrue(result['link_errors'])

    def test_undeclared_existing_file_fails_in_each_form(self):
        other = self.installed / 'other.md'
        other.write_text('# Not supplied by this fixture\n')
        for reference in self.forms(str(other)):
            with self.subTest(reference=reference):
                self.assertFalse(self.use(reference)['mechanical_pass'])

    def test_external_anchors_are_checked_in_each_form(self):
        for reference in self.forms(str(self.skill) + '#context-docs'):
            self.assertTrue(self.use(reference)['mechanical_pass'])
        for reference in self.forms(str(self.skill) + '#absent'):
            self.assertFalse(self.use(reference)['mechanical_pass'])

    def test_changed_installed_file_fails_integrity(self):
        self.skill.write_text('# Changed skill\n')
        result = self.use(f'`{self.skill}`')
        self.assertFalse(result['checks']['external_reference:' + str(self.skill)])
        self.assertFalse(result['mechanical_pass'])

    def test_missing_installed_file_fails_integrity(self):
        self.skill.unlink()
        result = self.use(f'[skill]({self.skill})')
        self.assertFalse(result['checks']['external_reference:' + str(self.skill)])
        self.assertFalse(result['mechanical_pass'])

    def test_valid_external_link_does_not_hide_immutable_edit(self):
        (self.root / 'README.md').write_text('# Renamed context\n')
        result = self.use(f'[skill]({self.skill})')
        self.assertTrue(result['checks']['local_links_and_anchors'])
        self.assertFalse(result['checks']['immutable:README.md'])
        self.assertFalse(result['mechanical_pass'])

    def test_valid_external_link_does_not_hide_broken_local_link(self):
        result = self.use(f'[skill]({self.skill}) and [missing](absent.md)')
        self.assertFalse(result['mechanical_pass'])
        self.assertEqual(['AGENTS.md: missing absent.md'], result['link_errors'])

    def test_external_files_are_not_assumed_without_declaration(self):
        self.assertTrue(link_errors({'AGENTS.md': f'[skill]({self.skill})'}))

    def test_declared_installed_directory_is_valid_but_integrity_still_required(self):
        self.assertTrue(self.use(f'[package]({self.installed}/)')['mechanical_pass'])
        self.skill.write_text('tampered\n')
        result = self.use(f'[package]({self.installed}/)')
        self.assertFalse(result['mechanical_pass'])
        self.assertFalse(result['checks']['external_reference:' + str(self.skill)])

    def test_project_directory_links_require_known_contents(self):
        files = {'README.md': '[Docs](docs/)\n', 'docs/context.md': '# Context\n'}
        self.assertEqual([], link_errors(files))
        files['README.md'] = '[Missing](missing/)\n'
        self.assertTrue(link_errors(files))

    def test_directory_anchor_is_not_assumed(self):
        result = self.use(f'[package]({self.installed}/#context-docs)')
        self.assertFalse(result['checks']['local_links_and_anchors'])


if __name__ == '__main__':
    unittest.main()
