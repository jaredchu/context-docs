"""Resolve an opt-in logging preference without changing project files."""
import argparse
import json
import os
from pathlib import Path
import stat
import subprocess

# Prospective child used to confirm that a directory rule covers new files.
PROBE = 'context-docs-coverage-probe'


class ProbeError(Exception):
    """A scope or Git check could not establish safe local-only coverage."""


def git_env(**extra):
    # Inspect this project, not a repository redirected by the invoking shell.
    # Keep configuration locators so exclusions match the user's effective Git rules.
    config = {'GIT_CONFIG_GLOBAL', 'GIT_CONFIG_SYSTEM', 'GIT_CONFIG_NOSYSTEM'}
    env = {k: v for k, v in os.environ.items()
           if not k.startswith('GIT_') or k in config}
    env.update(LC_ALL='C', GIT_DISCOVERY_ACROSS_FILESYSTEM='1', **extra)
    return env


def git_state(project):
    """Return present, absent, or unknown before resolving storage eligibility."""
    try:
        result = subprocess.run(
            ['git', '-C', str(Path(project).resolve()), 'rev-parse', '--git-dir'],
            env=git_env(), capture_output=True, text=True, timeout=10)
    except (OSError, RuntimeError, subprocess.TimeoutExpired):
        return 'unknown'
    if result.returncode == 0 and result.stdout.strip():
        return 'present'
    if (result.returncode == 128 and result.stderr.strip()
            == 'fatal: not a git repository (or any of the parent directories): .git'):
        return 'absent'
    return 'unknown'


def run_git(project, args, ok=(0,), input=None):
    """Run a read-only Git query and return NUL-separated fields; fail closed."""
    try:
        result = subprocess.run(['git', '-C', str(project), *args],
                                env=git_env(GIT_OPTIONAL_LOCKS='0'), input=input,
                                capture_output=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ProbeError('git %s could not run: %s' % (args[0], error))
    if not isinstance(result.stdout, bytes) or not isinstance(result.stderr, bytes):
        raise ProbeError('git %s returned malformed output' % args[0])
    if result.returncode not in ok:
        detail = result.stderr.decode('utf-8', 'replace').strip().splitlines()
        raise ProbeError('git %s failed (%s)%s' % (
            args[0], result.returncode, ': ' + detail[0] if detail else ''))
    return result.stdout


def split_nul(data, what):
    if not data:
        return []
    if not data.endswith(b'\0'):
        raise ProbeError('git %s returned malformed output' % what)
    return [os.fsdecode(field) for field in data[:-1].split(b'\0')]


def clean_path(raw, label):
    """Return a normalized project-relative path and whether it names a directory."""
    if not isinstance(raw, str) or not raw.strip():
        raise ProbeError('%s is empty' % label)
    if any(char in raw for char in '\0\n\r\\'):
        raise ProbeError('%s %r contains an unsupported character' % (label, raw))
    if raw.startswith('/') or os.path.isabs(raw):
        raise ProbeError('%s %r must be relative to the project' % (label, raw))
    parts = raw.rstrip('/').split('/')
    if any(part in ('', '.', '..') for part in parts):
        raise ProbeError('%s %r must be a normalized path inside the project' % (label, raw))
    if any(part.lower() == '.git' for part in parts):
        raise ProbeError('%s %r points into Git internals' % (label, raw))
    return '/'.join(parts), raw.endswith('/')


def check_components(project, rel, label):
    """Reject symlink aliases and nested repositories; return whether the target exists."""
    current = project
    try:
        for part in rel.split('/'):
            if current != project and os.path.lexists(current / '.git'):
                raise ProbeError('%s %r is inside a nested repository' % (label, rel))
            current = current / part
            try:
                metadata = current.lstat()
            except FileNotFoundError:
                return False
            if stat.S_ISLNK(metadata.st_mode):
                raise ProbeError('%s %r has a symlink component' % (label, rel))
            if part not in os.listdir(current.parent):
                raise ProbeError('%s %r uses a case or Unicode normalization alias' % (label, rel))
        if current.is_dir() and os.path.lexists(current / '.git'):
            raise ProbeError('%s %r is a nested repository' % (label, rel))
        return True
    except OSError as error:
        raise ProbeError('%s %r could not be inspected: %s' % (label, rel, error))


def check_descendants(path, label, rel):
    """Fail on unreadable entries, symlinks or nested repositories below a directory."""
    def fail(error):
        raise error
    try:
        for root, dirs, files in os.walk(path, onerror=fail):
            if '.git' in dirs or '.git' in files:
                raise ProbeError('%s %r contains a nested repository' % (label, rel))
            for name in dirs + files:
                if os.path.islink(os.path.join(root, name)):
                    raise ProbeError('%s %r contains a symlink' % (label, rel))
    except OSError as error:
        raise ProbeError('%s %r could not be read: %s' % (label, rel, error))


def local_only_errors(project, context_paths, journal_directory):
    """Return errors; empty only when every chosen path is untracked and ignored."""
    project = Path(project).resolve()
    errors, targets = [], []
    if isinstance(context_paths, str):
        context_paths = [context_paths]
    if not context_paths:
        errors.append('local-only storage requires at least one context path')
    if journal_directory is None or not str(journal_directory).strip():
        errors.append('local-only storage requires a journal directory')
    entries = [('context path', raw, False) for raw in context_paths or ()]
    if journal_directory is not None and str(journal_directory).strip():
        entries.append(('journal directory', journal_directory, True))
    for label, raw, directory in entries:
        try:
            rel, slash = clean_path(raw, label)
            exists = check_components(project, rel, label)
            full = project / rel
            directory = directory or slash or (exists and full.is_dir())
            if exists and directory and not full.is_dir():
                raise ProbeError('%s %r exists but is not a directory' % (label, rel))
            if exists and directory:
                check_descendants(full, label, rel)
            targets.append((label, rel, directory))
            if label == 'journal directory':
                # Cover real event and lock suffixes as well as a generic child.
                targets.extend((label, rel + '/' + PROBE + suffix, False)
                               for suffix in ('.jsonl', '.lock'))
        except ProbeError as error:
            errors.append(str(error))
    if errors:
        return errors
    try:
        if run_git(project, ['rev-parse', '--is-inside-work-tree']) != b'true\n':
            return ['project is not inside a Git work tree']
        ignorecase = run_git(project, ['config', '--type=bool', '--get', 'core.ignorecase'], ok=(0, 1))
        if ignorecase not in (b'', b'true\n', b'false\n'):
            raise ProbeError('git config core.ignorecase returned malformed output')
        literal = ':(literal,icase)' if ignorecase == b'true\n' else ':(literal)'
        queries = [rel + '/' + PROBE if directory else rel for _, rel, directory in targets]
        fields = split_nul(run_git(
            project, ['check-ignore', '--no-index', '--verbose', '--non-matching', '-z',
                      '--stdin'], ok=(0, 1),
            input=b'\0'.join(os.fsencode(path) for path in queries) + b'\0'), 'check-ignore')
        if len(fields) != 4 * len(queries):
            raise ProbeError('git check-ignore returned malformed output')
        for index, (label, rel, directory) in enumerate(targets):
            source, line, pattern, path = fields[4 * index:4 * index + 4]
            if (path != queries[index] or
                    (source and (not line.isdigit() or not pattern)) or
                    (not source and (line or pattern))):
                raise ProbeError('git check-ignore returned malformed output')
            if not source or pattern.startswith('!'):
                errors.append('%s %r is not ignored%s' % (
                    label, rel, ' for new files' if directory else ''))
            tracked = split_nul(run_git(
                project, ['ls-files', '-z', '--', literal + rel]), 'ls-files')
            if tracked:
                errors.append('%s %r has tracked files: %s' % (label, rel, ', '.join(tracked[:3])))
            exposed = split_nul(run_git(
                project, ['ls-files', '-z', '--others', '--exclude-standard', '--',
                          literal + rel]), 'ls-files')
            if exposed:
                errors.append('%s %r has files that are not ignored: %s' % (
                    label, rel, ', '.join(exposed[:3])))
    except ProbeError as error:
        errors.append(str(error))
    return errors


def resolve(project, preference='off', setting=None, *, storage='shared',
            context_paths=None, journal_directory=None):
    if setting is not None:
        return {'action': 'preserve', 'setting': setting, 'git': 'not_checked'}
    if preference != 'auto':
        return {'action': 'none', 'setting': None, 'git': 'not_checked'}
    if storage not in ('shared', 'local-only'):
        raise ValueError('storage must be shared or local-only')
    state = git_state(project)
    if storage == 'local-only' and state == 'present':
        errors = local_only_errors(project, context_paths, journal_directory)
        return {'action': 'none' if errors else 'enable',
                'setting': None if errors else 'jsonl', 'git': state,
                'reason': 'local-only', 'errors': errors}
    return {'action': 'enable' if state == 'absent' else 'none',
            'setting': 'jsonl' if state == 'absent' else None, 'git': state}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--preference', choices=('off', 'auto'), default='off')
    parser.add_argument('--setting', help='Existing project setting; omit only if absent')
    parser.add_argument('--storage', choices=('shared', 'local-only'), default='shared')
    parser.add_argument('--context-path', action='append', dest='context_paths',
                        help='Project-relative local-only context path; end directories with /')
    parser.add_argument('--journal-directory', help='Project-relative local-only journal directory')
    args = parser.parse_args()
    if args.setting is not None and not args.setting.strip():
        parser.error('--setting must not be blank')
    print(json.dumps(resolve(args.project, args.preference, args.setting, storage=args.storage,
                             context_paths=args.context_paths,
                             journal_directory=args.journal_directory)))


if __name__ == '__main__':
    main()
