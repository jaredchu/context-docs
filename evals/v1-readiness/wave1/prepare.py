"""Materialize review fixtures in a NEW external directory; no client launch."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

from checker import digest, git, git_environment, inventory, relative

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BASELINE = '14acc74dc7b51c3a4c512d1e555daac94c955216'
CUSTOMIZATION = b'\n<!-- SYNTHETIC LOCAL CUSTOMIZATION: keep fixture terminology. -->\n'
LOCAL_NOTE = b'Synthetic compatible local note; preserve across upgrade.\n'


def write(root, name, data):
    relative(name)
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data.encode() if isinstance(data, str) else data)
    path.chmod(0o644)


def package_files(released=False):
    """Read source packages only; never reads installed packages or credentials."""
    if released:
        r = git(REPO, 'ls-tree', '-r', '--name-only', BASELINE, '--', 'skills')
        if r.returncode:
            raise ValueError('Pinned release is unavailable locally')
        names = r.stdout.decode().splitlines()
        result = {}
        for name in names:
            r = git(REPO, 'show', BASELINE + ':' + name)
            if r.returncode:
                raise ValueError('Cannot read pinned package')
            result[name] = r.stdout
        return result
    listed = git(REPO, 'ls-files', '-z', '--cached', '--others', '--exclude-standard', '--', 'skills')
    if listed.returncode:
        raise ValueError('Cannot enumerate candidate source package files')
    result = {}
    for name in listed.stdout.decode().split('\0'):
        if not name:
            continue
        p = REPO / name
        if p.is_symlink() or REPO not in p.resolve().parents or not p.is_file():
            raise ValueError('Candidate source file is missing or escapes its package')
        result[name] = p.read_bytes()
    return result


def make_project(root, spec):
    root.mkdir(parents=True)
    for name, data in spec['files'].items():
        write(root, name, data)
    write(root, 'saved-study.bin', b'SYNTHETIC STUDY\x00original\xff\n')
    write(root, 'owner-work.txt', 'Synthetic owner baseline\n')
    if spec['git']:
        env = dict(git_environment(),
                   GIT_AUTHOR_NAME='Synthetic Fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                   GIT_COMMITTER_NAME='Synthetic Fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid',
                   GIT_AUTHOR_DATE='2026-10-01T00:00:00+00:00',
                   GIT_COMMITTER_DATE='2026-10-01T00:00:00+00:00')
        for args in [('init', '-q'), ('add', '.'),
                     ('-c', 'core.hooksPath=' + os.devnull, 'commit', '-qm', 'Synthetic baseline')]:
            subprocess.run(['git', '-c', 'core.excludesFile=' + os.devnull, *args], cwd=root, env=env, check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Different staged and working values catch accidental resets or adds.
        write(root, 'owner-work.txt', 'Synthetic staged owner work\n')
        subprocess.run(['git', '-c', 'core.excludesFile=' + os.devnull,
                        'add', 'owner-work.txt'], cwd=root, env=env, check=True)
        write(root, 'owner-work.txt', 'Synthetic unstaged owner work\n')


def prepare(destination):
    destination = Path(destination).absolute()
    resolved = destination.resolve()
    temp_roots = {Path(tempfile.gettempdir()).resolve(), Path('/tmp').resolve()}
    if not any(p in resolved.parents for p in temp_roots):
        raise ValueError('Review fixtures must be in a new temporary directory')
    # Refuse the checkout and installed package locations, including symlink aliases.
    protected = [REPO, Path.home() / '.agents', Path.home() / '.claude',
                 Path.home() / '.codex']
    for p in protected:
        p = p.resolve()
        if resolved == p or p in resolved.parents or resolved in p.parents:
            raise ValueError('Output overlaps a protected location')
    if destination.exists() or destination.is_symlink():
        raise ValueError('Output must not exist; no reset or overwrite is supported')
    recipes = json.loads((HERE / 'fixtures.json').read_text())
    cases = json.loads((HERE / 'cases.json').read_text())
    candidate, released = package_files(), package_files(True)
    destination.mkdir(parents=True, mode=0o700)
    write(destination, '.wave1-preparation-root.json', json.dumps({
        'status': 'review-only', 'model_trials': 0, 'source': 'synthetic recipes'}) + '\n')
    coordinator = destination / 'coordinator'
    for label, files in [('candidate', candidate), ('v0.1.9', released)]:
        for name, data in files.items():
            write(coordinator, 'packages/' + label + '/' + name, data)
    for name in ('cases.json', 'fixtures.json', 'ledger.json', 'isolation.json'):
        write(coordinator, name, (HERE / name).read_bytes())
    for client in ('codex', 'claude'):
        for group in ('journey', 'upgrade-clean', 'upgrade-custom', 'core-only', 'boundaries'):
            environment = destination / 'subjects' / client / group
            for name in recipes['groups'][group]:
                make_project(environment / name, recipes['projects'][name])
            files = released if group.startswith('upgrade') else candidate
            for name, data in files.items():
                if group == 'core-only' and name.startswith('skills/adopt-context-docs/'):
                    continue
                # Staging area, NOT an installed or authenticated client profile.
                write(environment, 'package-state/' + name, data)
            if group == 'upgrade-custom':
                p = environment / 'package-state/skills/context-docs/SKILL.md'
                with p.open('ab') as stream:
                    stream.write(CUSTOMIZATION)
                write(environment, 'package-state/skills/context-docs/references/local-note.md',
                      LOCAL_NOTE)
            state = inventory(environment, (group + '/.context/events/old.jsonl',))
            write(coordinator, 'baselines/' + client + '-' + group + '.json',
                  json.dumps(state, indent=2, sort_keys=True) + '\n')
    delta = sorted(name for name in set(candidate) | set(released)
                   if candidate.get(name) != released.get(name))
    manifests = {label: {n: digest(b) for n, b in files.items()}
                 for label, files in [('candidate', candidate), ('v0.1.9', released)]}
    source = git(REPO, 'rev-parse', 'HEAD')
    result = {'status': 'prepared-for-review', 'execution_ready': False,
              'model_trials': 0, 'sessions': len(cases['sessions']),
              'subject_seconds': sum(c['seconds'] for c in cases['sessions']),
              'baseline_revision': BASELINE, 'candidate_revision': source.stdout.decode().strip(),
              'candidate_versions': {n: candidate['skills/' + n + '/VERSION'].decode().strip()
                                     for n in ('context-docs', 'adopt-context-docs')},
              'plan_sha256': digest((REPO / 'docs/v1.0.0-validation-plan.md').read_bytes()),
              'candidate_approved': False, 'package_delta_from_v0.1.9': delta,
              'packages': manifests,
              'upgrade_expected': {'clean': manifests['candidate'],
                  'custom': {**manifests['candidate'],
                      'skills/context-docs/SKILL.md': digest(candidate['skills/context-docs/SKILL.md'] + CUSTOMIZATION),
                      'skills/context-docs/references/local-note.md': digest(LOCAL_NOTE)}},
              'recipe_sha256': {p.name: digest(p.read_bytes()) for p in HERE.iterdir()
                                if p.is_file() and p.name not in ('preparation.json',)},
              'blockers': ['Native user-scope, credential and memory isolation unverified',
                           'Maintainer scope/budget and trial execution not authorized',
                           'Per-phase inputs after actual J1/J2 outputs not frozen',
                           'Counterpart checker review pending']}
    if not delta:
        result['blockers'].append('Candidate equals v0.1.9; no distinct upgrade can be certified')
    write(coordinator, 'preparation.json', json.dumps(result, indent=2, sort_keys=True) + '\n')
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('destination', type=Path)
    args = p.parse_args()
    result = prepare(args.destination)
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('packages', 'upgrade_expected', 'recipe_sha256')}, indent=2))


if __name__ == '__main__':
    main()
