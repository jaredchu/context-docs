#!/usr/bin/env python3
"""Read-only repository checks for the local-only context option.

These are regression controls, not a runtime helper and not an agent
evaluation. They only run read-only Git commands and read files.
"""
import json
import os
import subprocess
import sys
from pathlib import Path, PurePosixPath

# Name of a hypothetical future file used to ask Git whether a directory's
# rules cover a prospective child. It is never created; explicit targets still
# need checking because a future exception can override this sample.
PROBE = 'context-docs-probe'
MIN_MARKER = 12


def _git(project, *args, input=None):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    for name in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_COMMON_DIR',
                 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES', 'GIT_PREFIX',
                 'GIT_LITERAL_PATHSPECS', 'GIT_GLOB_PATHSPECS', 'GIT_NOGLOB_PATHSPECS',
                 'GIT_ICASE_PATHSPECS'):
        env.pop(name, None)
    literal = ['--literal-pathspecs'] if args[0] == 'ls-files' else []
    command = ['git', *literal, '-C', str(project), *args]
    try:
        return subprocess.run(command, input=input, capture_output=True, env=env, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as error:
        return subprocess.CompletedProcess(command, 128, b'', str(error).encode())


def _fail(result, what):
    detail = result.stderr.decode(errors='replace').strip()
    return f'{what}: git exited {result.returncode}: {detail}'


def _split(output):
    return [p for p in output.decode(errors='surrogateescape').split('\0') if p]


def _bad_path(path):
    parts = PurePosixPath(path).parts
    if not path or PurePosixPath(path).is_absolute() or '..' in parts:
        return f'{path!r}: use a relative path inside the project'
    return None


def _check_repo(project):
    if not Path(project).is_dir():
        return f'{project}: not a directory'
    result = _git(project, 'rev-parse', '--is-inside-work-tree')
    if result.returncode != 0:
        return _fail(result, f'{project}: not a Git work tree')
    if result.stdout.strip() != b'true':
        return f'{project}: not inside a Git work tree'
    return None


def _ignore_rule(project, path):
    """Return (rule or None, error or None) from effective ignore rules."""
    result = _git(project, 'check-ignore', '--no-index', '-v', '-z', '--stdin',
                  input=(path + '\0').encode())
    if result.returncode not in (0, 1):
        return None, _fail(result, f'{path}: check-ignore')
    fields = _split(result.stdout)
    if result.returncode == 1 and not fields:
        return None, None
    if len(fields) != 4:
        return None, f'{path}: unexpected check-ignore output {fields!r}'
    source, line, pattern, _ = fields
    if pattern.startswith('!'):
        return None, None
    return f'{source}:{line}:{pattern}', None


def _storage_entry(project, path):
    entry = {'path': path, 'exists': False, 'kind': None, 'status': None,
             'rule': None, 'tracked': [], 'exposed_descendants': [], 'errors': []}
    bad = _bad_path(path)
    if bad:
        entry['errors'].append(bad)
        return entry
    full = Path(project) / path
    if not full.resolve().is_relative_to(Path(project).resolve()):
        entry['status'] = 'error'
        entry['errors'].append(f'{path}: resolved path is outside the project')
        return entry
    entry['exists'] = full.exists()
    is_dir = full.is_dir() or path.endswith('/')
    entry['kind'] = 'directory' if is_dir else 'file'
    clean = path.rstrip('/')

    tracked = _git(project, 'ls-files', '-z', '--cached', '--', clean)
    if tracked.returncode != 0:
        entry['errors'].append(_fail(tracked, f'{path}: ls-files --cached'))
    entry['tracked'] = _split(tracked.stdout)

    # A directory is covered only if a future descendant would be ignored;
    # file-only rules such as dir/*.jsonl do not cover the whole directory.
    target = f'{clean}/{PROBE}' if is_dir else clean
    entry['rule'], error = _ignore_rule(project, target)
    if error:
        entry['errors'].append(error)

    if is_dir and entry['exists']:
        others = _git(project, 'ls-files', '-z', '--others', '--exclude-standard', '--', clean)
        if others.returncode != 0:
            entry['errors'].append(_fail(others, f'{path}: ls-files --others'))
        entry['exposed_descendants'] = _split(others.stdout)

    if entry['errors']:
        entry['status'] = 'error'
    elif entry['tracked']:
        entry['status'] = 'tracked'
    elif entry['rule'] and not entry['exposed_descendants']:
        entry['status'] = 'ignored'
    else:
        entry['status'] = 'exposed'
    return entry


def inspect_storage(project, local_paths):
    """Classify declared local-only paths as tracked, ignored, exposed or error.

    ok is True only when every path is ignored by effective rules, nothing under
    it is tracked or exposed, and every Git command succeeded.
    """
    errors = []
    repo_error = _check_repo(project)
    if repo_error:
        return {'ok': False, 'paths': [], 'errors': [repo_error]}
    if not local_paths:
        errors.append('no local paths declared')
    paths = [_storage_entry(project, p) for p in local_paths]
    ok = not errors and all(e['status'] == 'ignored' for e in paths)
    return {'ok': ok, 'paths': paths, 'errors': errors}


def _shared_files(project, path):
    full = Path(project) / path
    if full.is_file():
        return [full], []
    files, errors = [], []
    for root, dirs, names in os.walk(full, onerror=lambda error: errors.append(str(error))):
        dirs[:] = sorted(d for d in dirs if d != '.git')
        for name in list(dirs):
            if (Path(root) / name).is_symlink():
                errors.append(f'{Path(root) / name}: directory symlink not scanned')
                dirs.remove(name)
        files.extend(Path(root) / n for n in sorted(names))
    return files, errors


def inspect_shared(project, shared_paths, private_markers):
    """Report distinctive synthetic canaries copied into declared shared docs.

    Scans files on disk, including untracked ones. This detects copying of the
    given markers only; it is not a general confidentiality check.
    """
    for marker in private_markers:
        if len(marker.strip()) < MIN_MARKER:
            raise ValueError(f'marker {marker!r} is not distinctive enough')
    result = {'ok': False, 'scanned': [], 'findings': [], 'errors': []}
    if not private_markers:
        result['errors'].append('no private markers given')
    if not shared_paths:
        result['errors'].append('no shared paths declared')
    encoded = [(m, m.encode()) for m in private_markers]
    for path in shared_paths:
        bad = _bad_path(path)
        if bad or not (Path(project) / path).exists():
            result['errors'].append(bad or f'{path}: declared shared path is missing')
            continue
        if not (Path(project) / path).resolve().is_relative_to(Path(project).resolve()):
            result['errors'].append(f'{path}: resolved path is outside the project')
            continue
        files, errors = _shared_files(project, path)
        result['errors'].extend(errors)
        for file in files:
            rel = file.relative_to(project).as_posix()
            if not file.resolve().is_relative_to(Path(project).resolve()):
                result['errors'].append(f'{rel}: resolved path is outside the project')
                continue
            try:
                data = file.read_bytes()
            except OSError as error:
                result['errors'].append(f'{rel}: {error}')
                continue
            result['scanned'].append(rel)
            result['findings'].extend({'path': rel, 'marker': m}
                                      for m, raw in encoded if raw in data)
    result['ok'] = not result['errors'] and not result['findings']
    return result


def main(argv):
    usage = ('usage: checks.py storage PROJECT PATH...\n'
             '       checks.py shared PROJECT --marker M [--marker M] PATH...')
    if len(argv) < 3 or argv[0] not in ('storage', 'shared'):
        print(usage, file=sys.stderr)
        return 2
    command, project, rest = argv[0], argv[1], argv[2:]
    if command == 'storage':
        report = inspect_storage(project, rest)
    else:
        markers, paths = [], []
        while rest:
            item = rest.pop(0)
            if item == '--marker' and rest:
                markers.append(rest.pop(0))
            else:
                paths.append(item)
        report = inspect_shared(project, paths, markers)
    print(json.dumps(report, indent=2))
    return 0 if report['ok'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
