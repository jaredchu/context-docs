#!/usr/bin/env python3
"""Tests for local-only checks against temporary real Git repositories."""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import checks  # noqa: E402

CANARY = 'CANARY-local-only-7f3a9c2e'


def git(cwd, *args):
    return subprocess.run(['git', '-C', str(cwd), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def write(path, text=''):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def snapshot(root):
    """Content, size and mtime of every file, including .git, plus all paths."""
    state = {}
    for current, dirs, files in os.walk(root):
        for name in dirs + files:
            path = Path(current) / name
            stat = path.lstat()
            digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
            state[path.relative_to(root).as_posix()] = (stat.st_mtime_ns, stat.st_size, digest)
    return state


@unittest.skipUnless(shutil.which('git'), 'git is required')
class GitCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, self.tmp)
        env = {'GIT_CONFIG_GLOBAL': os.devnull,
               'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CEILING_DIRECTORIES': str(self.tmp),
               'GIT_AUTHOR_NAME': 'Test', 'GIT_AUTHOR_EMAIL': 'test@example.invalid',
               'GIT_COMMITTER_NAME': 'Test', 'GIT_COMMITTER_EMAIL': 'test@example.invalid'}
        patcher = mock.patch.dict(os.environ, env)
        patcher.start()
        self.addCleanup(patcher.stop)
        for name in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_COMMON_DIR'):
            os.environ.pop(name, None)
        self.repo = self.tmp / 'repo'
        self.repo.mkdir()
        git(self.repo, 'init', '-q')
        write(self.repo / 'README.md', '# Synthetic project\n')
        git(self.repo, 'add', 'README.md')
        git(self.repo, 'commit', '-q', '-m', 'init')

    def storage(self, project, paths):
        """Run inspect_storage and assert it changed nothing on disk."""
        before = snapshot(self.tmp)
        report = checks.inspect_storage(project, paths)
        self.assertEqual(before, snapshot(self.tmp))
        return report

    def shared(self, project, paths, markers):
        before = snapshot(self.tmp)
        report = checks.inspect_shared(project, paths, markers)
        self.assertEqual(before, snapshot(self.tmp))
        return report

    def entry(self, report, path):
        return next(e for e in report['paths'] if e['path'] == path)


class StorageTests(GitCase):
    def test_gitignore_covers_existing_and_future_files(self):
        write(self.repo / '.gitignore', '.context/local/\n')
        write(self.repo / '.context/local/project-context.md', 'local notes\n')
        report = self.storage(self.repo, ['.context/local/', '.context/local/future.md'])
        self.assertTrue(report['ok'], report)
        existing = self.entry(report, '.context/local/')
        future = self.entry(report, '.context/local/future.md')
        self.assertEqual((existing['status'], existing['exists']), ('ignored', True))
        self.assertEqual((future['status'], future['exists']), ('ignored', False))
        self.assertIn('.gitignore:1:.context/local/', existing['rule'])

    def test_info_exclude_in_linked_worktree(self):
        worktree = self.tmp / 'worktree'
        git(self.repo, 'worktree', 'add', '-q', str(worktree))
        exclude = worktree / git(worktree, 'rev-parse', '--git-path', 'info/exclude')
        write(exclude, '.context/local/\n')
        write(worktree / '.context/local/project-context.md', 'local notes\n')
        report = self.storage(worktree, ['.context/local/'])
        self.assertTrue(report['ok'], report)
        self.assertIn('info/exclude', self.entry(report, '.context/local/')['rule'])
        # Per-user rules are not shared through the repository's .gitignore.
        self.assertFalse((worktree / '.gitignore').exists())

    def test_tracked_despite_matching_ignore_rule(self):
        write(self.repo / '.context/local/project-context.md', 'was committed\n')
        git(self.repo, 'add', '.context/local/project-context.md')
        git(self.repo, 'commit', '-q', '-m', 'tracked context')
        write(self.repo / '.gitignore', '.context/local/\n')
        report = self.storage(self.repo, ['.context/local/'])
        self.assertFalse(report['ok'])
        entry = self.entry(report, '.context/local/')
        self.assertEqual(entry['status'], 'tracked')
        self.assertEqual(entry['tracked'], ['.context/local/project-context.md'])
        self.assertIsNotNone(entry['rule'])

    def test_unignored_sibling_journal_is_exposed(self):
        write(self.repo / '.gitignore', '.context/local/\n')
        write(self.repo / '.context/local/project-context.md', 'local\n')
        write(self.repo / '.context/events/2026-10.jsonl', '{}\n')
        report = self.storage(self.repo, ['.context/local/', '.context/events/'])
        self.assertFalse(report['ok'])
        self.assertEqual(self.entry(report, '.context/local/')['status'], 'ignored')
        events = self.entry(report, '.context/events/')
        self.assertEqual(events['status'], 'exposed')
        self.assertEqual(events['exposed_descendants'], ['.context/events/2026-10.jsonl'])

    def test_negated_journal_inside_ignored_pattern_is_exposed(self):
        write(self.repo / '.gitignore', '.context/*\n!.context/events/\n')
        write(self.repo / '.context/events/2026-10.jsonl', '{}\n')
        report = self.storage(self.repo, ['.context/', '.context/events/2026-10.jsonl'])
        self.assertFalse(report['ok'])
        self.assertEqual(self.entry(report, '.context/')['exposed_descendants'],
                         ['.context/events/2026-10.jsonl'])
        self.assertEqual(self.entry(report, '.context/events/2026-10.jsonl')['status'], 'exposed')

    def test_ignored_entry_point_is_readable_by_explicit_path(self):
        write(self.repo / '.gitignore', '.context/local/\n')
        entry_point = self.repo / '.context/local/project-context.md'
        write(entry_point, '# Local project context\n')
        report = self.storage(self.repo, ['.context/local/project-context.md'])
        self.assertTrue(report['ok'], report)
        # Ignore-aware discovery omits it, so loading needs an explicit path.
        listed = git(self.repo, 'ls-files', '--others', '--exclude-standard')
        self.assertNotIn('project-context.md', listed)
        self.assertEqual(entry_point.read_text(), '# Local project context\n')

    def test_file_only_rule_does_not_cover_directory(self):
        write(self.repo / '.gitignore', '.context/events/*.jsonl\n')
        write(self.repo / '.context/events/2026-10.jsonl', '{}\n')
        report = self.storage(self.repo, ['.context/events/', '.context/events/2026-10.jsonl'])
        self.assertFalse(report['ok'])
        self.assertEqual(self.entry(report, '.context/events/')['status'], 'exposed')
        self.assertEqual(self.entry(report, '.context/events/2026-10.jsonl')['status'], 'ignored')

    def test_absent_prospective_paths(self):
        write(self.repo / '.gitignore', '.context/local/\n')
        report = self.storage(self.repo, ['.context/local/new/', '.context/other.md'])
        self.assertFalse(report['ok'])
        self.assertEqual(self.entry(report, '.context/local/new/')['status'], 'ignored')
        other = self.entry(report, '.context/other.md')
        self.assertEqual((other['status'], other['exists']), ('exposed', False))

    def test_not_a_repository_fails(self):
        plain = self.tmp / 'plain'
        plain.mkdir()
        report = self.storage(plain, ['.context/local/'])
        self.assertFalse(report['ok'])
        self.assertTrue(report['errors'])

    def test_unknown_git_failure_is_not_success(self):
        write(self.repo / '.gitignore', '.context/local/\n')
        real = checks._git

        def failing(project, *args, **kwargs):
            if 'check-ignore' in args:
                return subprocess.CompletedProcess(args, 128, b'', b'fatal: injected')
            return real(project, *args, **kwargs)

        with mock.patch.object(checks, '_git', failing):
            report = self.storage(self.repo, ['.context/local/'])
        self.assertFalse(report['ok'])
        entry = self.entry(report, '.context/local/')
        self.assertEqual(entry['status'], 'error')
        self.assertIn('injected', entry['errors'][0])

    def test_missing_git_is_reported_as_unverified(self):
        with mock.patch.object(checks.subprocess, 'run', side_effect=FileNotFoundError('git unavailable')):
            report = self.storage(self.repo, ['.context/local/'])
        self.assertFalse(report['ok'])
        self.assertIn('git unavailable', report['errors'][0])

    def test_git_redirection_does_not_inspect_another_repository(self):
        write(self.repo / '.gitignore', '.context/local/\n')
        with mock.patch.dict(os.environ, {'GIT_DIR': str(self.tmp / 'missing.git'),
                                         'GIT_WORK_TREE': str(self.tmp / 'other')}):
            report = self.storage(self.repo, ['.context/local/'])
        self.assertTrue(report['ok'], report)

    def test_paths_with_spaces_and_future_exception(self):
        write(self.repo / '.gitignore', 'local notes/*\n!local notes/public.md\n')
        write(self.repo / 'local notes/context.md', 'local notes\n')
        report = self.storage(self.repo, ['local notes/', 'local notes/public.md'])
        self.assertFalse(report['ok'])
        self.assertEqual(self.entry(report, 'local notes/')['status'], 'ignored')
        self.assertEqual(self.entry(report, 'local notes/public.md')['status'], 'exposed')

    def test_symlink_outside_project_is_not_local_storage(self):
        outside = self.tmp / 'outside.md'
        write(outside, 'outside scope\n')
        (self.repo / 'context.md').symlink_to(outside)
        write(self.repo / '.gitignore', 'context.md\n')
        report = self.storage(self.repo, ['context.md'])
        self.assertFalse(report['ok'])
        self.assertEqual(self.entry(report, 'context.md')['status'], 'error')

    def test_invalid_and_empty_paths_fail(self):
        report = self.storage(self.repo, ['../outside', '/abs'])
        self.assertFalse(report['ok'])
        self.assertTrue(all(e['status'] is None and e['errors'] for e in report['paths']))
        self.assertFalse(self.storage(self.repo, [])['ok'])


class SharedTests(GitCase):
    def setUp(self):
        super().setUp()
        write(self.repo / '.context/local/private.md', f'Synthetic secret {CANARY}\n')
        write(self.repo / 'docs/project-context.md',
              '# Context\n\nLocal-only notes: `.context/local/project-context.md`\n')
        git(self.repo, 'add', 'docs')
        git(self.repo, 'commit', '-q', '-m', 'shared docs')

    def test_pointer_without_canary_is_allowed(self):
        report = self.shared(self.repo, ['docs/', 'README.md'], [CANARY])
        self.assertTrue(report['ok'], report)
        self.assertIn('docs/project-context.md', report['scanned'])

    def test_canary_in_tracked_shared_doc_is_detected(self):
        write(self.repo / 'docs/project-context.md', f'Copied: {CANARY}\n')
        report = self.shared(self.repo, ['docs/'], [CANARY])
        self.assertFalse(report['ok'])
        self.assertEqual(report['findings'],
                         [{'path': 'docs/project-context.md', 'marker': CANARY}])

    def test_canary_in_untracked_shared_doc_is_detected(self):
        write(self.repo / 'docs/new-notes.md', f'Draft {CANARY}\n')
        report = self.shared(self.repo, ['docs/'], [CANARY])
        self.assertFalse(report['ok'])
        self.assertEqual([f['path'] for f in report['findings']], ['docs/new-notes.md'])

    def test_missing_shared_path_and_weak_marker_fail(self):
        self.assertFalse(self.shared(self.repo, ['docs/missing.md'], [CANARY])['ok'])
        self.assertFalse(self.shared(self.repo, ['docs/'], [])['ok'])
        with self.assertRaises(ValueError):
            checks.inspect_shared(self.repo, ['docs/'], ['secret'])

    def test_shared_symlink_outside_scope_is_not_silently_skipped(self):
        outside = self.tmp / 'outside.md'
        write(outside, CANARY)
        (self.repo / 'docs/link.md').symlink_to(outside)
        report = self.shared(self.repo, ['docs/'], [CANARY])
        self.assertFalse(report['ok'])
        self.assertTrue(report['errors'])

    def test_shared_directory_read_error_is_not_a_clean_scan(self):
        def unreadable(path, **kwargs):
            kwargs['onerror'](PermissionError('shared directory unreadable'))
            return iter(())

        with mock.patch.object(checks.os, 'walk', side_effect=unreadable):
            report = checks.inspect_shared(self.repo, ['docs/'], [CANARY])
        self.assertFalse(report['ok'])
        self.assertIn('unreadable', report['errors'][0])


if __name__ == '__main__':
    unittest.main()
