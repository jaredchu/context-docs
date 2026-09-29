"""Resolve an opt-in logging preference without changing project files."""
import argparse
import json
import os
from pathlib import Path
import subprocess


def git_state(project):
    """Return present, absent, or unknown; only Git's explicit absence enables auto."""
    # Inspect this project, not a repository redirected by the invoking shell.
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(LC_ALL='C', GIT_DISCOVERY_ACROSS_FILESYSTEM='1')
    try:
        result = subprocess.run(
            ['git', '-C', str(Path(project).resolve()), 'rev-parse', '--git-dir'],
            env=env, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return 'unknown'
    if result.returncode == 0 and result.stdout.strip():
        return 'present'
    if (result.returncode == 128 and result.stderr.strip()
            == 'fatal: not a git repository (or any of the parent directories): .git'):
        return 'absent'
    return 'unknown'


def resolve(project, preference='off', setting=None):
    if setting is not None:
        return {'action': 'preserve', 'setting': setting, 'git': 'not_checked'}
    if preference != 'auto':
        return {'action': 'none', 'setting': None, 'git': 'not_checked'}
    state = git_state(project)
    return {'action': 'enable' if state == 'absent' else 'none',
            'setting': 'jsonl' if state == 'absent' else None, 'git': state}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--preference', choices=('off', 'auto'), default='off')
    parser.add_argument('--setting', help='Existing project setting; omit only if absent')
    args = parser.parse_args()
    if args.setting is not None and not args.setting.strip():
        parser.error('--setting must not be blank')
    print(json.dumps(resolve(args.project, args.preference, args.setting)))


if __name__ == '__main__':
    main()
