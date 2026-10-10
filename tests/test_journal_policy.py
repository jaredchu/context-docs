"""Real Git topology and conservative error handling for opt-in auto logging."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / 'skills/context-docs/scripts/journal_policy.py'
spec = importlib.util.spec_from_file_location('journal_policy', SOURCE)
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)

IDENTITY = ('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid')


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        # Isolate Git config without changing HOME or touching user config files.
        environ = patch.dict(os.environ, {'GIT_CONFIG_GLOBAL': os.devnull,
                                          'GIT_CONFIG_NOSYSTEM': '1'})
        environ.start()
        self.addCleanup(environ.stop)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        self.env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1')

    def git(self, *args):
        return subprocess.run(['git', *map(str, args)], env=self.env,
                              capture_output=True, text=True, check=True)

    def repo(self, name='repo', ignore=None):
        repo = self.root / name
        self.git('init', repo)
        self.git('-C', repo, *IDENTITY, 'commit', '--allow-empty', '-m', 'Synthetic fixture')
        if ignore is not None:
            (repo / '.gitignore').write_text(ignore)
        return repo

    def commit(self, repo, *paths):
        self.git('-C', repo, 'add', '-f', '--', *paths)
        self.git('-C', repo, *IDENTITY, 'commit', '-m', 'Synthetic tracked file')

    def local(self, project, context=('notes/',), journal='.context/events'):
        return policy.resolve(project, 'auto', storage='local-only',
                              context_paths=None if context is None else list(context),
                              journal_directory=journal)

    def assertEnabled(self, result):
        self.assertEqual(result, {'action': 'enable', 'setting': 'jsonl', 'git': 'present',
                                  'reason': 'local-only', 'errors': []})

    def assertRefused(self, result, fragment=''):
        self.assertEqual((result['action'], result['setting'], result['reason']),
                         ('none', None, 'local-only'), result)
        self.assertTrue(result['errors'], result)
        self.assertTrue(all(isinstance(e, str) and e for e in result['errors']))
        self.assertIn(fragment, ' '.join(result['errors']))

    def snapshot(self, path):
        state = {}
        for root, dirs, files in os.walk(path):
            for name in dirs:
                state[os.path.join(root, name)] = None
            for name in files:
                full = os.path.join(root, name)
                state[full] = os.readlink(full) if os.path.islink(full) else Path(full).read_bytes()
        return state

    # Existing no-Git and shared-Git routes.

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
        self.git('-C', repo, *IDENTITY, 'commit', '--allow-empty', '-m', 'Synthetic fixture')
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

    # Explicit local-only storage inside Git.

    def test_ignored_local_context_and_journal_enable_read_only(self):
        repo = self.repo(ignore='.context/\nnotes/\nlocal.md\n')
        (repo / '.context/events').mkdir(parents=True)
        (repo / '.context/events/2026.jsonl').write_text('{}\n')
        (repo / 'local.md').write_text('synthetic\n')
        head = self.git('-C', repo, 'rev-parse', 'HEAD').stdout
        before = self.snapshot(repo)
        self.assertEnabled(self.local(repo, ('notes/', 'local.md')))
        self.assertEqual(self.snapshot(repo), before)
        self.assertEqual(self.git('-C', repo, 'rev-parse', 'HEAD').stdout, head)
        self.assertFalse((repo / 'notes').exists())

    def test_absent_future_paths_enable(self):
        repo = self.repo(ignore='.context/\nnotes/\n')
        self.assertEnabled(self.local(repo))
        self.assertEqual(sorted(p.name for p in repo.iterdir()), ['.git', '.gitignore'])

    def test_personal_excludes_and_linked_worktree(self):
        repo = self.repo()
        (repo / '.git/info').mkdir(exist_ok=True)
        (repo / '.git/info/exclude').write_text('.context/\nnotes/\n')
        self.assertEnabled(self.local(repo))
        worktree = self.root / 'worktree'
        self.git('-C', repo, 'worktree', 'add', '--detach', worktree)
        self.assertEnabled(self.local(worktree))
        other = self.repo('other')
        personal = self.root / 'personal-excludes'
        personal.write_text('.context/\nnotes/\n')
        self.git('-C', other, 'config', 'core.excludesFile', personal)
        self.assertEnabled(self.local(other))

    def test_settings_and_default_preference_skip_all_probes(self):
        repo = self.repo(ignore='.context/\nnotes/\n')
        with patch.object(policy.subprocess, 'run', side_effect=AssertionError('probe')), \
                patch.object(policy.os, 'walk', side_effect=AssertionError('walk')):
            for setting in ('off', 'jsonl', 'markdown'):
                self.assertEqual(policy.resolve(repo, 'auto', setting, storage='local-only',
                                                context_paths=['../bad'], journal_directory=''),
                                 {'action': 'preserve', 'setting': setting, 'git': 'not_checked'})
            self.assertEqual(policy.resolve(repo, storage='local-only', context_paths=['notes/'],
                                            journal_directory='.context/events'),
                             {'action': 'none', 'setting': None, 'git': 'not_checked'})
            self.assertEqual(policy.resolve(repo, 'auto', 'off', storage='invalid'),
                             {'action': 'preserve', 'setting': 'off', 'git': 'not_checked'})

    def test_shared_git_and_no_git_routes_unchanged(self):
        repo = self.repo(ignore='.context/\nnotes/\n')
        expected = {'action': 'none', 'setting': None, 'git': 'present'}
        self.assertEqual(policy.resolve(repo, 'auto'), expected)
        self.assertEqual(policy.resolve(repo, 'auto', storage='shared', context_paths=['notes/'],
                                        journal_directory='.context/events'), expected)
        plain = self.root / 'plain'
        plain.mkdir()
        self.assertEqual(self.local(plain), {'action': 'enable', 'setting': 'jsonl', 'git': 'absent'})
        self.assertEqual(list(plain.iterdir()), [])

    def test_tracked_files_despite_matching_ignores(self):
        repo = self.repo()
        (repo / 'notes').mkdir()
        (repo / 'notes/old.md').write_text('tracked\n')
        (repo / '.context/events').mkdir(parents=True)
        (repo / '.context/events/old.jsonl').write_text('{}\n')
        self.commit(repo, 'notes/old.md', '.context/events/old.jsonl')
        (repo / '.gitignore').write_text('.context/\nnotes/\n')
        result = self.local(repo)
        self.assertRefused(result, 'tracked')
        self.assertEqual(sum('tracked' in e for e in result['errors']), 2)

    def test_exposed_journal_or_context(self):
        for ignore, fragment in (('', 'not ignored'), ('notes/\n', '.context/events'),
                                 ('.context/\n', 'notes')):
            with self.subTest(ignore=ignore):
                repo = self.repo('repo-%d' % len(ignore), ignore=ignore)
                self.assertRefused(self.local(repo), fragment)

    def test_negated_rules_and_existing_descendants(self):
        repo = self.repo('negated-dir', ignore='.context/*\n!.context/events/\nnotes/\n')
        self.assertRefused(self.local(repo), '.context/events')
        repo = self.repo('negated-file', ignore='.context/events/*\n!.context/events/keep.jsonl\n'
                                                'notes/\n')
        (repo / '.context/events').mkdir(parents=True)
        (repo / '.context/events/keep.jsonl').write_text('{}\n')
        self.assertRefused(self.local(repo), 'keep.jsonl')
        repo = self.repo('negated-context', ignore='.context/\nnotes/*\n!notes/shared.md\n')
        self.assertRefused(self.local(repo, ('notes/shared.md',)), 'notes/shared.md')

    def test_file_only_journal_rule_is_incomplete(self):
        repo = self.repo(ignore='.context/events/*.jsonl\nnotes/\n')
        self.assertRefused(self.local(repo), 'for new files')

    def test_missing_scope(self):
        repo = self.repo(ignore='.context/\nnotes/\n')
        for context, journal in ((None, '.context/events'), ((), '.context/events'),
                                 (('notes/',), None), (('notes/',), ' '), (('',), '.context/events')):
            with self.subTest(context=context, journal=journal):
                self.assertRefused(self.local(repo, context, journal))

    def test_git_errors_missing_git_and_malformed_output(self):
        repo = self.repo(ignore='.context/\nnotes/\n')
        real = subprocess.run

        def fake(result):
            def run(args, **kwargs):
                if 'rev-parse' in args and '--git-dir' in args:
                    return real(args, **kwargs)
                if isinstance(result, BaseException):
                    raise result
                return subprocess.CompletedProcess(args, *result)
            return run
        for result in (FileNotFoundError(), PermissionError(), subprocess.TimeoutExpired('git', 10),
                       (128, b'', b'fatal: synthetic'), (0, 'text not bytes', ''),
                       (0, b'unterminated', b''), (0, b'a\0b\0', b'')):
            with self.subTest(result=result), patch.object(policy.subprocess, 'run',
                                                           side_effect=fake(result)):
                self.assertRefused(self.local(repo))
        with patch.object(policy.subprocess, 'run', side_effect=FileNotFoundError()):
            self.assertEqual(self.local(repo), {'action': 'none', 'setting': None, 'git': 'unknown'})
        (repo / '.context/events/day').mkdir(parents=True)
        with patch.object(policy.os, 'walk', side_effect=PermissionError('denied')):
            self.assertRefused(self.local(repo), 'could not be read')

    def test_bare_repository_refuses_local_only(self):
        self.git('init', '--bare', self.root / 'bare')
        self.assertRefused(self.local(self.root / 'bare'))

    def test_shell_git_redirection_ignored_for_local_only(self):
        repo = self.repo(ignore='.context/\nnotes/\n')
        decoy = self.repo('decoy')
        with patch.dict(os.environ, {'GIT_DIR': str(decoy / '.git'), 'GIT_WORK_TREE': str(decoy),
                                     'GIT_INDEX_FILE': str(decoy / '.git/index'),
                                     'GIT_GLOB_PATHSPECS': '1', 'GIT_ICASE_PATHSPECS': '1'}):
            self.assertEnabled(self.local(repo))
            self.assertRefused(self.local(decoy))

    def test_spaces_and_literal_wildcards(self):
        repo = self.repo()
        (repo / 'ctx1.md').write_text('tracked\n')
        self.commit(repo, 'ctx1.md')
        (repo / '.gitignore').write_text('ctx\\[1\\].md\nlocal events/\nmy notes/\n')
        self.assertEnabled(self.local(repo, ('ctx[1].md', 'my notes/'), 'local events'))
        (repo / '.gitignore').write_text('ctx\\[1\\].md\nctx1.md\nlocal events/\n')
        self.assertRefused(self.local(repo, ('ctx1.md',), 'local events'), 'tracked')

    def test_path_escape_internals_and_symlink_aliases(self):
        repo = self.repo(ignore='.context/\nnotes/\nreal/\nlink\n')
        for bad in ('../outside/', str(repo / 'notes/'), '.git/info/', 'a/../notes/', './notes/',
                    'notes//x.md', '.GIT/x', 'notes\\x.md'):
            with self.subTest(path=bad):
                self.assertRefused(self.local(repo, (bad,)))
        (repo / 'real').mkdir()
        (repo / 'link').symlink_to('real', target_is_directory=True)
        self.assertRefused(self.local(repo, ('link/x.md',)), 'symlink')
        self.assertRefused(self.local(repo, ('notes/',), 'link'), 'symlink')
        (repo / '.context/events').mkdir(parents=True)
        (repo / '.context/events/alias').symlink_to(self.root, target_is_directory=True)
        self.assertRefused(self.local(repo), 'symlink')

    def test_parent_and_nested_repository_topology(self):
        outer = self.repo('outer', ignore='vendor/\n')
        inner = outer / 'vendor/inner'
        inner.mkdir(parents=True)
        self.git('init', inner)
        (inner / '.gitignore').write_text('.context/\nnotes/\n')
        self.assertEnabled(self.local(inner))
        self.assertRefused(self.local(outer, ('vendor/inner/notes/',), 'vendor/events'),
                           'nested repository')
        self.assertRefused(self.local(outer, ('vendor/',), 'vendor/events'), 'nested repository')
        sub = self.repo('sub', ignore='pkg/.context/\npkg/notes/\n') / 'pkg'
        sub.mkdir()
        self.assertEnabled(self.local(sub))

    def test_cli_subprocess(self):
        repo = self.repo(ignore='.context/\nnotes/\n')

        def cli(*args):
            result = subprocess.run([sys.executable, str(SOURCE), '--project', str(repo), *args],
                                    capture_output=True, text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        self.assertEqual(cli('--preference', 'auto'),
                         {'action': 'none', 'setting': None, 'git': 'present'})
        self.assertEqual(cli('--preference', 'auto', '--setting', 'off', '--storage', 'local-only'),
                         {'action': 'preserve', 'setting': 'off', 'git': 'not_checked'})
        self.assertEqual(cli('--preference', 'auto', '--storage', 'local-only', '--context-path',
                             'notes/', '--context-path', 'notes/a b.md', '--journal-directory',
                             '.context/events')['action'], 'enable')
        refused = cli('--preference', 'auto', '--storage', 'local-only')
        self.assertEqual((refused['action'], refused['reason']), ('none', 'local-only'))
        self.assertEqual(len(refused['errors']), 2)
        bad = subprocess.run([sys.executable, str(SOURCE), '--project', str(repo),
                              '--storage', 'private'], capture_output=True, text=True, timeout=60)
        self.assertEqual(bad.returncode, 2)

    def test_effective_global_excludes_are_honored_without_config_edits(self):
        repo = self.repo()
        excludes = self.root / 'global-excludes'
        excludes.write_text('notes/\n.context/\n')
        config = self.root / 'global-config'
        config.write_text('[core]\n\texcludesFile = ' + str(excludes) + '\n')
        before = self.snapshot(self.root)
        with patch.dict(os.environ, {'GIT_CONFIG_GLOBAL': str(config)}):
            self.assertEnabled(self.local(repo))
        self.assertEqual(self.snapshot(self.root), before)

    def test_component_access_error_and_file_parent_refuse(self):
        repo = self.repo(ignore='notes/\n.context/\n')
        actual_lstat = Path.lstat

        def guarded_lstat(path):
            if path == repo / 'notes':
                raise PermissionError('synthetic component access denied')
            return actual_lstat(path)

        with patch.object(Path, 'lstat', guarded_lstat):
            self.assertRefused(self.local(repo), 'could not be inspected')
        (repo / 'notes').write_text('this is a file, not a directory\n')
        self.assertRefused(self.local(repo, ('notes/child.md',)), 'could not be inspected')

    def test_malformed_ignore_response_never_enables(self):
        repo = self.repo(ignore='notes/\n.context/\n')
        actual_run = subprocess.run
        queries = ['notes/' + policy.PROBE, '.context/events/' + policy.PROBE,
                   '.context/events/' + policy.PROBE + '.jsonl',
                   '.context/events/' + policy.PROBE + '.lock']
        outputs = []
        for source, line, pattern, wrong_path in [('.gitignore', 'not-a-line', 'notes/', False),
                                                 ('.gitignore', '1', '', False),
                                                 ('', '', 'notes/', False),
                                                 ('.gitignore', '1', 'notes/', True)]:
            fields = []
            for query in queries:
                fields.extend([source, line, pattern, 'wrong-path' if wrong_path else query])
            outputs.append(('\0'.join(fields) + '\0').encode())
        for output in outputs:
            def altered(args, **kwargs):
                result = actual_run(args, **kwargs)
                if 'check-ignore' in args:
                    return subprocess.CompletedProcess(args, 0, output, b'')
                return result
            with self.subTest(output=output), patch.object(policy.subprocess, 'run', side_effect=altered):
                self.assertRefused(self.local(repo), 'malformed output')

    def test_case_alias_cannot_hide_tracked_context_even_after_deletion(self):
        repo = self.repo(ignore='notes/\n.context/\n')
        (repo / 'Notes').mkdir()
        (repo / 'Notes/old.md').write_text('tracked synthetic context\n')
        self.commit(repo, 'Notes/old.md')
        self.git('-C', repo, 'config', 'core.ignorecase', 'true')
        before = self.snapshot(repo)
        self.assertRefused(self.local(repo, ('notes/',)))
        self.assertEqual(self.snapshot(repo), before)
        (repo / 'Notes/old.md').unlink()
        (repo / 'Notes').rmdir()
        self.assertRefused(self.local(repo, ('notes/',)), 'tracked')

    def test_journal_probe_covers_ordinary_events_and_lock_files(self):
        for index, rule in enumerate(['.context/events/.*\n',
                                      '.context/events/*\n!.context/events/*.jsonl\n',
                                      '.context/events/*\n!.context/events/*.lock\n']):
            repo = self.repo('probe-%s' % index, ignore='notes/\n' + rule)
            with self.subTest(rule=rule):
                self.assertRefused(self.local(repo), 'not ignored')

    def test_invalid_case_config_leaves_auto_unchanged(self):
        repo = self.repo(ignore='notes/\n.context/\n')
        self.git('-C', repo, 'config', 'core.ignorecase', 'not-a-boolean')
        # Git rejects this configuration during repository detection itself.
        self.assertEqual(self.local(repo), {'action': 'none', 'setting': None, 'git': 'unknown'})


if __name__ == '__main__':
    unittest.main()
