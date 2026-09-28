"""Regression tests for package portability and current version agreement."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import static_checks as checks


class StaticChecksTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        override = patch.object(checks, 'ROOT', self.root)
        override.start()
        self.addCleanup(override.stop)
        for name, required in checks.SKILLS.items():
            self.write(f'skills/{name}/SKILL.md',
                       f'---\nname: {name}\ndescription: Synthetic test skill.\n---\n')
            for relative in required:
                self.write(f'skills/{name}/{relative}', 'Synthetic fixture.\n')
            self.write(f'skills/{name}/VERSION', '0.1.1\n' if name == 'context-docs' else '0.1.3\n')
        self.write('README.md', '**Status: experimental, core skill v0.1.1; adoption skill v0.1.3.**\n'
                   '\nHistorical adoption releases: 0.1.2 and 0.1.0.\n')
        self.write('CHANGELOG.md', '# Changelog\n\n## adopt-context-docs 0.1.3 — unreleased\n'
                   '\n## adopt-context-docs 0.1.2 — historical\n'
                   '\n## context-docs 0.1.1 — current\n')
        self.add_link('skills/context-docs/SKILL.md', 'references/standard.md')
        self.add_link('skills/context-docs/references/standard.md', '../assets/project-context.md')
        self.add_link('skills/adopt-context-docs/SKILL.md', '../context-docs/SKILL.md')

    def write(self, relative, body):
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body)

    def add_link(self, relative, target):
        source = self.root / relative
        source.write_text(source.read_text() + f'\n[Reference]({target})\n')

    def failures(self, check):
        failures = []
        check(failures)
        return failures

    def test_portable_packages_and_declared_sibling_pass(self):
        self.assertEqual([], self.failures(checks.check_skills))

    def test_repository_only_link_fails(self):
        self.add_link('skills/context-docs/SKILL.md', '../../README.md')
        self.assertTrue(any('../../README.md' in failure for failure in self.failures(checks.check_skills)))

    def test_nested_reference_cannot_escape_package(self):
        self.add_link('skills/context-docs/references/standard.md', '../../../README.md')
        self.assertTrue(any('references/standard.md' in failure for failure in self.failures(checks.check_skills)))

    def test_core_cannot_depend_on_adoption(self):
        self.add_link('skills/context-docs/SKILL.md', '../adopt-context-docs/SKILL.md')
        self.assertTrue(self.failures(checks.check_skills))

    def test_symlink_cannot_escape_package(self):
        (self.root / 'skills/context-docs/escape.md').symlink_to(self.root / 'README.md')
        self.add_link('skills/context-docs/SKILL.md', 'escape.md')
        self.assertTrue(any('escape.md' in failure for failure in self.failures(checks.check_skills)))

    def test_absolute_path_inside_package_is_not_portable(self):
        self.add_link('skills/context-docs/SKILL.md', str(self.root / 'skills/context-docs/LICENSE'))
        self.assertTrue(self.failures(checks.check_skills))

    def test_missing_declared_dependency_target_fails(self):
        (self.root / 'skills/context-docs/SKILL.md').unlink()
        self.assertTrue(any('declared sibling dependency' in failure
                            for failure in self.failures(checks.check_skills)))

    def test_missing_packaged_helper_fails_even_with_fault_fixture_exceptions(self):
        (self.root / 'skills/context-docs/scripts/event_journal.py').unlink()
        self.assertTrue(any('scripts/event_journal.py' in failure
                            for failure in self.failures(checks.check_skills)))

    def test_current_versions_pass(self):
        self.assertEqual([], self.failures(checks.check_versions))

    def test_generated_local_reports_are_excluded_from_repository_links(self):
        self.write('.local/report.md', '[Draft](missing.md)\n')
        self.assertEqual([], self.failures(checks.check_links))
        self.write('docs/report.md', '[Published](missing.md)\n')
        self.assertTrue(any('docs/report.md' in failure for failure in self.failures(checks.check_links)))

    def test_historical_version_does_not_satisfy_current_declarations(self):
        self.write('skills/adopt-context-docs/VERSION', '0.1.2\n')
        failures = self.failures(checks.check_versions)
        self.assertTrue(any('README.md' in failure for failure in failures))
        self.assertTrue(any('CHANGELOG.md' in failure for failure in failures))

    def test_other_skill_version_does_not_satisfy_readme(self):
        readme = self.root / 'README.md'
        readme.write_text(readme.read_text().replace('core skill v0.1.1', 'core skill v0.1.0')
                          .replace('adoption skill v0.1.3', 'adoption skill v0.1.1'))
        self.assertTrue(any('current status for context-docs ' in failure
                            for failure in self.failures(checks.check_versions)))

    def test_missing_changelog_fails(self):
        (self.root / 'CHANGELOG.md').unlink()
        self.assertEqual(2, len(self.failures(checks.check_versions)))


if __name__ == '__main__':
    unittest.main()
