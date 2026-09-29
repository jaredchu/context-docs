"""Real Git topology and conservative error handling for opt-in auto logging."""
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / 'skills/context-docs/scripts/journal_policy.py'
spec = importlib.util.spec_from_file_location('journal_policy', SOURCE)
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        self.env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1')

    def git(self, *args):
        return subprocess.run(['git', *map(str, args)], env=self.env,
                              capture_output=True, text=True, check=True)

    def test_no_git_enables_without_writing(self):
        self.assertEqual(policy.resolve(self.root, 'auto'),
                         {'action': 'enable', 'setting': 'jsonl', 'git': 'absent'})
        self.assertEqual(list(self.root.iterdir()), [])

    def test_default_and_explicit_settings_skip_detection(self):
        with patch.object(policy, 'git_state', side_effect=AssertionError('unexpected Git probe')):
            self.assertEqual(policy.resolve(self.root)['action'], 'none')
            for setting in ('off', 'jsonl', 'markdown'):
                self.assertEqual(policy.resolve(self.root, 'auto', setting),
                                 {'action': 'preserve', 'setting': setting, 'git': 'not_checked'})

    def test_git_root_parent_and_worktree(self):
        repo = self.root / 'repo'
        self.git('init', repo)
        self.git('-C', repo, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '--allow-empty', '-m', 'Synthetic fixture')
        nested = repo / 'nested'
        nested.mkdir()
        worktree = self.root / 'worktree'
        self.git('-C', repo, 'worktree', 'add', '--detach', worktree)
        for path in (repo, nested, worktree):
            with self.subTest(path=path):
                self.assertEqual(policy.resolve(path, 'auto')['git'], 'present')
                self.assertEqual(policy.resolve(path, 'auto')['action'], 'none')

    def test_bare_repository_is_not_absent(self):
        self.git('init', '--bare', self.root / 'bare')
        self.assertEqual(policy.git_state(self.root / 'bare'), 'present')

    def test_invalid_directory_and_broken_git_pointer_are_unknown(self):
        self.assertEqual(policy.git_state(self.root / 'missing'), 'unknown')
        (self.root / '.git').write_text('gitdir: missing-directory\n')
        self.assertEqual(policy.resolve(self.root, 'auto')['git'], 'unknown')
        self.assertEqual(policy.resolve(self.root, 'auto')['action'], 'none')

    def test_detection_errors_do_not_enable(self):
        for error in (FileNotFoundError(), PermissionError(), subprocess.TimeoutExpired('git', 10)):
            with self.subTest(error=error), patch.object(policy.subprocess, 'run', side_effect=error):
                self.assertEqual(policy.resolve(self.root, 'auto')['git'], 'unknown')
                self.assertEqual(policy.resolve(self.root, 'auto')['action'], 'none')
        for message in ('fatal: detected dubious ownership', 'fatal: permission denied', ''):
            with patch.object(policy.subprocess, 'run', return_value=subprocess.CompletedProcess(
                    [], 128, '', message)):
                self.assertEqual(policy.resolve(self.root, 'auto')['action'], 'none')

    def test_shell_git_redirection_does_not_hide_real_project(self):
        repo = self.root / 'repo'
        self.git('init', repo)
        outside = self.root / 'outside'
        outside.mkdir()
        with patch.dict(os.environ, {'GIT_DIR': str(repo / '.git'),
                                     'GIT_CEILING_DIRECTORIES': str(repo)}):
            self.assertEqual(policy.git_state(outside), 'absent')
            self.assertEqual(policy.git_state(repo), 'present')

    def test_added_git_does_not_override_saved_setting(self):
        self.assertEqual(policy.resolve(self.root, 'auto')['setting'], 'jsonl')
        self.git('init', self.root)
        self.assertEqual(policy.resolve(self.root, 'auto', 'jsonl')['action'], 'preserve')


if __name__ == '__main__':
    unittest.main()
