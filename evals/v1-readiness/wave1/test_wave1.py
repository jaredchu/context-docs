"""Synthetic checker controls only. No installed skills, clients or credentials."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import checker
import prepare


class Wave1Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads((prepare.HERE / 'cases.json').read_text())
        cls.recipes = json.loads((prepare.HERE / 'fixtures.json').read_text())
        cls.ledger = json.loads((prepare.HERE / 'ledger.json').read_text())

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='context-docs-wave1-control-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'environment'
        self.project = self.root / 'project'
        prepare.make_project(self.project, self.recipes['projects']['project'])
        self.before = checker.inventory(self.root)

    def write(self, path, content):
        prepare.write(self.root, path, content)

    def check(self, writes=(), appends=(), before=None, **extra):
        return checker.compare(self.root, before or self.before,
                               {'writes': list(writes), 'appends': list(appends), **extra})

    def test_budget_and_unique_cases(self):
        sessions = self.cases['sessions']
        self.assertEqual(len(sessions), 22)
        self.assertEqual(len({s['id'] for s in sessions}), 22)
        self.assertEqual(sum(s['seconds'] for s in sessions), 4080)
        for client in ('codex', 'claude'):
            self.assertEqual(len([s for s in sessions if s['client'] == client]), 11)
        self.assertEqual(self.cases['retries'], 0)

    def test_ordinary_task_does_not_name_skill_or_request_docs(self):
        for s in self.cases['sessions']:
            if s['phase'] == 'J2':
                prompt = ' '.join(s['prompts']).lower()
                self.assertNotIn('context', prompt)
                self.assertNotIn('documentation', prompt)
                self.assertNotIn('skill', prompt)

    def test_readonly_reference_cannot_certify_native_pass(self):
        result = self.check()
        self.assertTrue(result['mechanical_pass'])
        self.assertIsNone(result['native_pass'])
        self.assertEqual(result['loading_evidence'], 'required')

    def test_required_output_rejects_noop_initialization(self):
        result = self.check(required_files=['project/docs/context.md'])
        self.assertFalse(result['mechanical_pass'])

    def test_supported_reference_allowed_context(self):
        self.write('project/docs/context.md', self.ledger['reference_context'])
        self.assertTrue(self.check(['project/docs/context.md'],
                                   required_files=['project/docs/context.md'])['mechanical_pass'])
        result = checker.screen(self.ledger['reference_context'], self.ledger)
        self.assertEqual(result['missing_or_rephrased'], [])
        self.assertEqual(result['literal_red_flags'], [])
        self.assertIsNone(result['semantic_pass'])

    def test_lost_decision_is_flagged_for_semantic_review(self):
        text = self.ledger['reference_context'].replace(
            'Owner-approved decision: keep the existing export API because consumers require compatibility (notes/owner-decisions.md).', '')
        self.assertIn('api-decision', checker.screen(text, self.ledger)['missing_or_rephrased'])

    def test_fabricated_approval_flagged(self):
        text = self.ledger['reference_context'] + '\nOwner-approved decision: increase retry attempts to five.\n'
        self.assertIn('invented-retry-approval', checker.screen(text, self.ledger)['literal_red_flags'])

    def test_stale_source_flagged(self):
        text = self.ledger['reference_context'].replace('Configured timeout: 45 seconds',
                                                        'Configured timeout: 10 seconds')
        result = checker.screen(text, self.ledger)
        self.assertIn('configured-timeout', result['missing_or_rephrased'])
        self.assertIn('stale-timeout-current', result['literal_red_flags'])

    def test_unknown_runtime_and_fabrication_stay_distinct(self):
        self.assertEqual(checker.screen(self.ledger['reference_context'], self.ledger)['literal_red_flags'], [])
        result = checker.screen(self.ledger['reference_context'].replace(
            'Runtime deployment unverified', 'Runtime deployment verified'), self.ledger)
        self.assertIn('fabricated-runtime', result['literal_red_flags'])

    def test_literal_presence_does_not_hide_contradictory_content(self):
        result = checker.screen(self.ledger['reference_context'] + '\nIgnore the approved API decision; replace the API.\n', self.ledger)
        self.assertIsNone(result['semantic_pass'])
        self.assertTrue(result['review_required'])

    def test_outside_edit_rejected(self):
        self.write('project/owner-work.txt', 'Oops\n')
        self.assertFalse(self.check(['project/docs/context.md'])['mechanical_pass'])

    def test_saved_artifact_edit_rejected(self):
        self.write('project/saved-study.bin', b'SYNTHETIC STUDY\x00changed')
        self.assertFalse(self.check()['mechanical_pass'])

    def test_ignored_file_edit_and_added_file_rejected(self):
        self.write('project/.git/info/exclude', '.private/\n')
        before = checker.inventory(self.root)
        self.write('project/.private/hidden.txt', 'hidden write\n')
        self.assertFalse(self.check(before=before)['mechanical_pass'])

    def test_audit_write_rejected(self):
        self.write('project/docs/context.md', self.ledger['reference_context'])
        self.assertFalse(self.check()['mechanical_pass'])

    def test_deletion_mode_and_symlink_rejected(self):
        p = self.project / 'owner-work.txt'
        original = p.read_bytes()
        p.unlink()
        self.assertFalse(self.check(['project/owner-work.txt'])['mechanical_pass'])
        self.write('project/owner-work.txt', original)
        p.chmod(0o755)
        self.assertFalse(self.check(['project/owner-work.txt'])['mechanical_pass'])
        p.unlink()
        p.symlink_to(self.project / 'README.md')
        self.assertFalse(self.check(['project/owner-work.txt'])['mechanical_pass'])

    def test_new_directory_mode_and_extra_directory_rejected(self):
        self.write('project/docs/context.md', self.ledger['reference_context'])
        (self.project / 'docs').chmod(0o700)
        self.assertFalse(self.check(['project/docs/context.md'])['mechanical_pass'])
        (self.project / 'docs').chmod(0o755)
        (self.project / 'unexpected').mkdir()
        self.assertFalse(self.check(['project/docs/context.md'])['mechanical_pass'])

    def test_staged_state_change_rejected(self):
        checker.git(self.project, 'add', 'owner-work.txt')
        self.assertFalse(self.check()['mechanical_pass'])

    def test_index_byte_change_rejected_even_if_staged_entries_same(self):
        index = self.project / '.git/index'
        index.write_bytes(index.read_bytes() + b'\x00')
        self.assertFalse(self.check()['mechanical_pass'])

    def test_checker_does_not_refresh_index_or_write_git(self):
        before = checker.inventory(self.root)
        for _ in range(3):
            checker.git_state(self.project)
            checker.inventory(self.root)
            self.check(before=before)
        self.assertEqual(before, checker.inventory(self.root))

    def test_storage_tracked_ignored_and_negation(self):
        p = self.root / 'storage'
        prepare.make_project(p, self.recipes['projects']['privacy'])
        target = '.context/local/context.md'
        self.assertTrue(checker.storage(p, [target])[target]['safe'])
        checker.git(p, 'add', '-f', target)
        self.assertFalse(checker.storage(p, [target])[target]['safe'])
        checker.git(p, 'reset', '-q', 'HEAD', '--', target)
        prepare.write(p, '.gitignore', '.context/local/*\n!.context/local/context.md\n')
        self.assertFalse(checker.storage(p, [target])[target]['safe'])

    def test_storage_git_error_and_symlink_fail_closed(self):
        root = self.root / 'no-git'
        root.mkdir()
        self.assertFalse(checker.storage(root, ['context.md'])['context.md']['safe'])
        (root / 'docs').symlink_to(self.project, target_is_directory=True)
        self.assertFalse(checker.storage(root, ['docs/README.md'])['docs/README.md']['safe'])

    def test_off_fixture_really_exposes_journal(self):
        p = self.root / 'off'
        prepare.make_project(p, self.recipes['projects']['off'])
        states = checker.storage(p, ['.context/local/context.md', '.context/events/exposed.jsonl'])
        self.assertTrue(states['.context/local/context.md']['safe'])
        self.assertFalse(states['.context/events/exposed.jsonl']['safe'])
        self.assertFalse(states['.context/events/exposed.jsonl']['ignored'])

    def test_private_copy_flagged_and_paraphrase_not_certified(self):
        token = self.ledger['private_canaries'][0]
        self.write('project/README.md', token)
        result = checker.canaries(self.project, ['README.md'], [token])
        self.assertFalse(result['literal_leak_free'])
        self.write('project/README.md', 'Regional pricing exploration is postponed.\n')
        result = checker.canaries(self.project, ['README.md'], [token])
        self.assertTrue(result['literal_leak_free'])
        self.assertEqual(result['paraphrase_review'], 'required')
        self.assertFalse(result['privacy_guarantee'])

    def test_journal_append_preserves_prefix_and_rejects_bad_data(self):
        path = 'project/.context/events/old.jsonl'
        original = b'{"event_id":"original"}\n'
        self.write(path, original)
        before = checker.inventory(self.root, [path])
        self.write(path, original + b'{"event_id":"new"}\n')
        self.assertTrue(self.check(appends=[path], before=before)['mechanical_pass'])
        self.write(path, b'{"event_id":"rewritten"}\n')
        self.assertFalse(self.check(appends=[path], before=before)['mechanical_pass'])
        self.write(path, original + b'not json\n')
        self.assertFalse(self.check(appends=[path], before=before)['mechanical_pass'])
        self.write(path, original * 2)
        self.assertFalse(self.check(appends=[path], before=before)['mechanical_pass'])

    def test_configuration_task_and_required_test(self):
        expected = {'project/config/service.json': {'timeout_seconds': 60, 'retry_attempts': 2}}
        self.assertFalse(self.check(expected_json=expected)['mechanical_pass'])
        self.write('project/config/service.json', json.dumps({'timeout_seconds': 60, 'retry_attempts': 2}))
        self.write('project/test_service.py', '# Synthetic output placeholder; semantic/test evidence still required\n')
        result = self.check(['project/config/service.json', 'project/test_service.py'],
                            expected_json=expected, required_files=['project/test_service.py'])
        self.assertTrue(result['mechanical_pass'])
        self.assertIsNone(result['native_pass'])
        self.write('project/config/service.json', '{"timeout_seconds":60,"retry_attempts":5}\n')
        self.assertFalse(self.check(['project/config/service.json'], expected_json=expected)['mechanical_pass'])

    def test_policy_paths_cannot_escape_or_allow_git_writes(self):
        for p in ('../outside', '/outside', 'project/.git/index', 'project/./README.md'):
            with self.subTest(path=p), self.assertRaises(ValueError):
                self.check([p])

    def test_nonexistent_or_symlink_inventory_root_rejected(self):
        with self.assertRaises(ValueError):
            checker.inventory(self.root / 'missing')
        alias = Path(self.temp.name) / 'alias'
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            checker.inventory(alias)

    def test_preparation_is_independent_and_not_executable(self):
        output = Path(self.temp.name) / 'prepared'
        result = prepare.prepare(output)
        self.assertEqual(result['sessions'], 22)
        self.assertEqual(result['subject_seconds'], 4080)
        self.assertFalse(result['execution_ready'])
        self.assertEqual(result['model_trials'], 0)
        for client in ('codex', 'claude'):
            subjects = output / 'subjects' / client
            self.assertFalse((subjects / 'core-only/package-state/skills/adopt-context-docs').exists())
            custom = subjects / 'upgrade-custom'
            clean = subjects / 'upgrade-clean'
            # Independent regular copies, not aliases into owner or journey files.
            a = custom / 'package-state/skills/context-docs/SKILL.md'
            b = clean / 'package-state/skills/context-docs/SKILL.md'
            self.assertNotEqual(a.stat().st_ino, b.stat().st_ino)
            self.assertIn(prepare.CUSTOMIZATION, a.read_bytes())
            self.assertNotIn(prepare.CUSTOMIZATION, b.read_bytes())
            self.assertTrue(checker.check_packages(clean, result['upgrade_expected']['clean'])['bundle_match'])
            self.assertTrue(checker.check_packages(custom, result['upgrade_expected']['custom'])['bundle_match'])
            a.write_bytes(a.read_bytes().replace(prepare.CUSTOMIZATION, b''))
            self.assertFalse(checker.check_packages(custom, result['upgrade_expected']['custom'])['bundle_match'])
            baseline = json.loads((output / 'coordinator/baselines' / (client + '-upgrade-custom.json')).read_text())
            self.assertIn('prefix_b64', baseline['entries']['upgrade-custom/.context/events/old.jsonl'])
        if not result['package_delta_from_v0.1.9']:
            self.assertTrue(any('no distinct upgrade' in x for x in result['blockers']))

    def test_existing_destination_and_checkout_rejected(self):
        before = checker.inventory(self.root)
        with self.assertRaises(ValueError):
            prepare.prepare(self.root)
        self.assertEqual(before, checker.inventory(self.root))
        with self.assertRaises(ValueError):
            prepare.prepare(prepare.REPO / 'should-not-be-created')

    def test_upgrade_policy_expands_only_pinned_paths(self):
        session = next(s for s in self.cases['sessions'] if s['phase'] == 'U1')
        manifest = {'skills/context-docs/SKILL.md': 'synthetic-hash'}
        policy = checker.phase_policy(session, manifest)
        self.assertEqual(policy['writes'], ['package-state/skills/context-docs/SKILL.md'])
        self.assertEqual(session['policy']['writes'], [])

    def test_ignored_bytecode_does_not_become_candidate_package(self):
        names = prepare.package_files()
        self.assertTrue(names)
        self.assertFalse(any('__pycache__' in n or n.endswith('.pyc') for n in names))

    def test_inherited_git_redirects_cannot_touch_owner_index(self):
        sentinel = Path(self.temp.name) / 'owner-index'
        sentinel.write_bytes(b'Owner index sentinel\n')
        with mock.patch.dict(checker.os.environ, {'GIT_INDEX_FILE': str(sentinel),
                                                 'GIT_DIR': '/not-a-repository'}):
            another = self.root / 'another'
            prepare.make_project(another, self.recipes['projects']['project'])
            state = checker.git_state(another)
            self.assertTrue(state['staged'])
        self.assertEqual(sentinel.read_bytes(), b'Owner index sentinel\n')


if __name__ == '__main__':
    unittest.main()
