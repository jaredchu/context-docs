"""Build a local plugin candidate without installing it or changing source skills."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

RELEASE = '89c91f424476c8194a89cd38f4f48c5078fa1574'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True,
                        help='New, nonexistent output directory; existing paths are refused')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    template = repo / 'packaging/plugin'
    names = ('context-docs', 'adopt-context-docs')
    tracked = subprocess.check_output(
        ['git', '-C', str(repo), 'ls-tree', '-r', '--name-only', '-z', RELEASE, '--',
         *(f'skills/{name}' for name in names)]).decode().split('\0')
    # This candidate freezes the release, even if source skills are later edited.
    payload = {p: subprocess.check_output(['git', '-C', str(repo), 'show', f'{RELEASE}:{p}'])
               for p in tracked if p}
    for name in names:
        if f'skills/{name}/SKILL.md' not in payload:
            parser.error(f'missing released skill: {name}')
    sources = {}
    for name in ('plugin.json', '.claude-plugin/plugin.json', 'README.md', 'assets/icon.svg'):
        sources[name] = template / name
    sources['LICENSE'] = repo / 'LICENSE'
    # Check all inputs before creating output. Never follow links into local setups.
    for relative, path in sources.items():
        if not path.is_file() or path.is_symlink() or path.resolve() != path.absolute():
            parser.error(f'input must be a regular, non-symlink file: {relative}')
    payload.update({name: path.read_bytes() for name, path in sources.items()})
    payload = dict(sorted(payload.items()))
    output = args.output.absolute()
    if output.exists() or output.is_symlink():
        parser.error('output already exists; choose a new directory')
    output.mkdir(parents=True, mode=0o700)
    package = output / 'context-docs'
    hashes = {}
    archive = output / 'context-docs.zip'
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as zipped:
        for name, content in payload.items():
            target = package / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            target.chmod(0o644)
            entry = zipfile.ZipInfo('context-docs/' + name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.external_attr = 0o100644 << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            zipped.writestr(entry, content)
            hashes[name] = hashlib.sha256(content).hexdigest()
    report = {'package': str(package), 'archive': str(archive), 'skill_source_commit': RELEASE,
              'files': len(payload), 'unpacked_bytes': sum(map(len, payload.values())),
              'archive_bytes': archive.stat().st_size,
              'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
              'sha256': hashes}
    (output / 'build.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
