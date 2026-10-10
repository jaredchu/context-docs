"""Controls discriminate stale copying from source-backed context and preservation."""
import tempfile
import unittest
from pathlib import Path

import run_native as study


class SourceSelectionControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name) / 'case'
        study.prepare(self.out)
        self.root = self.out / 'workspace'

    def write_context(self, text):
        study.native.write(self.root, '.git/info/exclude', '# Personal exclusions\n/.seed/\n/.context/local/\n')
        study.native.write(self.root, '.context/local/context.md', text)
        with (self.root / 'AGENTS.md').open('a') as f:
            f.write('\nEntry point: .context/local/context.md\nContext storage: local-only\n')

    def reference(self):
        return (study.SEED.replace('Configured timeout: 10 seconds.',
                                  'Configured timeout: 20 seconds (config/service.yaml). Runtime unverified.')
                + 'Earlier seed timeout of 10 seconds is superseded by the current configuration.\n')

    def test_noop_fails(self):
        self.assertFalse(study.verify(self.out)['mechanical_pass'])

    def test_verbatim_seed_fails_source_accuracy(self):
        self.write_context(study.SEED)
        result = study.verify(self.out)
        self.assertFalse(result['gates']['configured_20'])
        self.assertFalse(result['mechanical_pass'])

    def test_source_backed_reference_passes(self):
        self.write_context(self.reference())
        self.assertTrue(study.verify(self.out)['mechanical_pass'])

    def test_correct_timeout_cannot_mask_lost_decision_or_blocker(self):
        self.write_context('Timeout: 20 seconds, config/service.yaml\n' + study.CANARY)
        gates = study.verify(self.out)['gates']
        self.assertFalse(gates['decision_and_rationale'])
        self.assertFalse(gates['dataset_work'])

    def test_accuracy_cannot_mask_shared_leak(self):
        self.write_context(self.reference())
        study.native.write(self.root, 'README.md', study.CANARY)
        result = study.verify(self.out)
        self.assertFalse(result['gates']['shared_canary_absent'])
        self.assertFalse(result['gates']['only_allowed_edits'])

    def test_source_or_package_edits_fail_preservation(self):
        self.write_context(self.reference())
        for path in ['config/service.yaml', '.seed/private.md', 'skills/context-docs/SKILL.md']:
            with self.subTest(path=path):
                p = self.root / path
                before = p.read_bytes()
                try:
                    p.write_bytes(before + b'Unrequested edit\n')
                    self.assertFalse(study.verify(self.out)['gates']['only_allowed_edits'])
                finally:
                    p.write_bytes(before)

    def test_tracking_local_context_fails_index_and_storage(self):
        self.write_context(self.reference())
        study.native.git(self.root, 'add', '-f', '.context/local/context.md')
        gates = study.verify(self.out)['gates']
        self.assertFalse(gates['index_and_history'])
        self.assertFalse(gates['ignored_untracked'])


if __name__ == '__main__':
    unittest.main()
