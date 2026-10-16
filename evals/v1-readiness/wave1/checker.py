"""Read-only Wave 1 mechanics. Never launches agents or declares native success."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess


def digest(data):
    return hashlib.sha256(data).hexdigest()


def relative(value):
    p = PurePosixPath(value)
    if not value or p.is_absolute() or '..' in p.parts or str(p) != value:
        raise ValueError('Expected a normalized relative path')
    return p


def git_environment():
    # Inherited GIT_DIR/WORK_TREE/INDEX_FILE must not redirect fixture writes or reads.
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_OPTIONAL_LOCKS='0', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_CONFIG_NOSYSTEM='1')
    return env


def git(root, *args):
    env = git_environment()
    return subprocess.run(['git', '-c', 'core.fsmonitor=false',
                           '-c', 'core.hooksPath=' + os.devnull,
                           '-c', 'core.excludesFile=' + os.devnull, *args],
                          cwd=root, env=env, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)


def inventory(root, append_paths=()):
    """Includes ignored files and Git bytes; never traverses symlinks."""
    root = Path(root)
    if not root.is_dir() or root.is_symlink():
        raise ValueError('Inventory root must be an existing regular directory')
    entries = {}
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in sorted(dirs + files):
            p = Path(directory) / name
            key = p.relative_to(root).as_posix()
            info = p.lstat()
            entry = {'mode': stat.S_IMODE(info.st_mode)}
            if p.is_symlink():
                entry.update(kind='symlink', target=os.readlink(p))
            elif p.is_dir():
                entry.update(kind='directory')
            elif p.is_file():
                data = p.read_bytes()
                entry.update(kind='file', sha256=digest(data), size=len(data))
                if key in append_paths:
                    entry['prefix_b64'] = base64.b64encode(data).decode('ascii')
            else:
                entry.update(kind='special')
            entries[key] = entry
    repos = {}
    for key, entry in entries.items():
        if (key == '.git' or key.endswith('/.git')) and entry['kind'] == 'directory':
            project_key = key[:-5] if key != '.git' else '.'
            repos[project_key] = git_state(root / project_key)
    return {'entries': entries, 'git': repos,
            'root_mode': stat.S_IMODE(root.stat().st_mode)}


def git_state(root):
    result = {}
    for label, args in [('head', ('rev-parse', 'HEAD')),
                        ('refs', ('show-ref',)),
                        ('staged', ('ls-files', '--stage', '-z'))]:
        r = git(root, *args)
        if r.returncode:
            raise ValueError('Cannot inspect synthetic Git ' + label)
        result[label] = digest(r.stdout)
    return result


def compare(root, before, policy):
    """Exact preservation except explicitly named regular files or appends.

    No Git index/cache exception is implemented: accepting one needs a reviewed
    new policy/checker, never an after-the-fact waiver.
    """
    allowed = set(policy.get('writes', []))
    append = set(policy.get('appends', []))
    for p in allowed | append:
        relative(p)
        if '/.git/' in '/' + p or p.endswith('/.git'):
            raise ValueError('Git writes cannot be allowed')
    current = inventory(root, append)
    failures = []
    if before['root_mode'] != current['root_mode']:
        failures.append({'path': '.', 'reason': 'root mode changed'})
    old, new = before['entries'], current['entries']
    for p in sorted(set(old) | set(new)):
        a, b = old.get(p), new.get(p)
        if a == b:
            continue
        if a is not None and b is None:
            failures.append({'path': p, 'reason': 'deletion'})
        elif p in append and a and b and a['kind'] == b['kind'] == 'file':
            prefix = base64.b64decode(a['prefix_b64'], validate=True)
            data = (Path(root) / p).read_bytes()
            if b['mode'] != a['mode'] or not data.startswith(prefix):
                failures.append({'path': p, 'reason': 'journal prefix/mode changed'})
            elif data != prefix:
                try:
                    rows = [json.loads(line) for line in data.splitlines()]
                    ids = [r['event_id'] for r in rows]
                    if not data.endswith(b'\n') or len(ids) != len(set(ids)):
                        raise ValueError('Incomplete or duplicate event')
                except (ValueError, TypeError, KeyError):
                    failures.append({'path': p, 'reason': 'invalid JSONL append'})
        elif p in allowed and b and b['kind'] == 'file':
            if (a and (a['kind'] != 'file' or b['mode'] != a['mode'])) or (
                    not a and b['mode'] != 0o644):
                failures.append({'path': p, 'reason': 'file type/mode changed'})
        elif (a is None and b and b['kind'] == 'directory' and b['mode'] == 0o755
              and any(x.startswith(p + '/') for x in allowed | append)):
            continue
        else:
            failures.append({'path': p, 'reason': 'outside allowed writes'})
    if before['git'] != current['git']:
        failures.append({'path': '(Git)', 'reason': 'head/refs/staged content changed'})
    for p in policy.get('required_files', []):
        relative(p)
        if current['entries'].get(p, {}).get('kind') != 'file':
            failures.append({'path': p, 'reason': 'required regular file missing'})
    for p, expected in policy.get('expected_json', {}).items():
        relative(p)
        try:
            if current['entries'].get(p, {}).get('kind') != 'file':
                raise ValueError('Missing regular file')
            if json.loads((Path(root) / p).read_text()) != expected:
                raise ValueError('Unexpected configuration')
        except (ValueError, OSError):
            failures.append({'path': p, 'reason': 'configuration does not match frozen task'})
    return {'mechanical_pass': not failures, 'failures': failures,
            'native_pass': None, 'semantic_review': 'required',
            'loading_evidence': 'required'}


def storage(root, paths):
    """Check descendants, not only directory patterns; Git failures fail closed."""
    result = {}
    for value in paths:
        relative(value)
        p = Path(root) / value
        if any((Path(root) / parent).is_symlink()
               for parent in [PurePosixPath(value), *PurePosixPath(value).parents]
               if str(parent) != '.'):
            result[value] = {'safe': False, 'reason': 'symlink'}
            continue
        tracked = git(root, 'ls-files', '-z', '--', value)
        ignored = git(root, 'check-ignore', '--no-index', '--', value)
        result[value] = {'safe': tracked.returncode == 0 and not tracked.stdout
                        and ignored.returncode == 0,
                         'untracked': tracked.returncode == 0 and not tracked.stdout,
                         'ignored': ignored.returncode == 0,
                         'git_error': tracked.returncode != 0 or ignored.returncode not in (0, 1)}
    return result


def screen(text, ledger):
    """Literal diagnostics only: missing/rephrased facts need semantic review.

    Present words cannot prove truthful propositions, authority or non-leakage.
    Canonical linked preservation and paraphrases are graded by a human reviewer.
    """
    normalized = text.casefold()
    missing = [item['id'] for item in ledger['items']
               if not all(word.casefold() in normalized for word in item['screen_terms'])]
    flags = [item['id'] for item in ledger['red_flags']
             if re.search(item['pattern'], text, re.IGNORECASE)]
    return {'missing_or_rephrased': missing, 'literal_red_flags': flags,
            'semantic_pass': None, 'review_required': True}


def canaries(root, shared_paths, canaries):
    leaks = []
    for value in shared_paths:
        relative(value)
        p = Path(root) / value
        if any((Path(root) / parent).is_symlink()
               for parent in [PurePosixPath(value), *PurePosixPath(value).parents]
               if str(parent) != '.'):
            leaks.append({'path': value, 'reason': 'shared symlink'})
        elif p.is_file():
            data = p.read_bytes()
            for token in canaries:
                if token.encode() in data:
                    leaks.append({'path': value, 'reason': 'literal private canary'})
    return {'literal_leak_free': not leaks, 'leaks': leaks,
            'paraphrase_review': 'required', 'privacy_guarantee': False}


def phase_policy(session, candidate_manifest):
    policy = json.loads(json.dumps(session['policy']))
    if policy.pop('package_upgrade', False):
        policy['writes'].extend('package-state/' + p for p in candidate_manifest)
    return policy


def check_packages(root, expected):
    """Exact frozen package match; does not prove native selection or upgrade."""
    observed = inventory(Path(root) / 'package-state')['entries']
    actual = {p: e['sha256'] for p, e in observed.items() if e['kind'] == 'file'}
    safe = all(e['kind'] in ('file', 'directory') for e in observed.values())
    return {'bundle_match': safe and actual == expected,
            'native_selection': None, 'upgrade_proven': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='operation', required=True)
    snap = sub.add_parser('snapshot')
    snap.add_argument('root', type=Path)
    snap.add_argument('--append', action='append', default=[])
    check = sub.add_parser('compare')
    check.add_argument('root', type=Path)
    check.add_argument('baseline', type=Path)
    check.add_argument('policy', type=Path)
    args = p.parse_args()
    if args.operation == 'snapshot':
        result = inventory(args.root, args.append)
    else:
        result = compare(args.root, json.loads(args.baseline.read_text()),
                         json.loads(args.policy.read_text()))
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.operation == 'compare' and not result['mechanical_pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
