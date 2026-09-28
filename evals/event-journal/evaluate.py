"""Run the frozen synthetic replay and local latency diagnostics; no model calls."""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import statistics
import subprocess
import sys
import time
from uuid import uuid4


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / 'skills/context-docs/scripts/event_journal.py'
HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('journal', TOOL)
journal = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(journal)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def invoke(directory, *args, payload=None):
    cmd = [sys.executable, str(TOOL), '--directory', str(directory), *args]
    start = time.perf_counter()
    proc = subprocess.run(cmd, input=json.dumps(payload) if payload is not None else None,
                          text=True, encoding='utf-8', capture_output=True, timeout=30)
    elapsed = (time.perf_counter() - start) * 1000
    result = {'args': list(args), 'returncode': proc.returncode, 'stdout': proc.stdout,
              'stderr': proc.stderr, 'elapsed_ms': elapsed}
    if proc.returncode:
        raise RuntimeError(result)
    return result


def git(repo, *args):
    # Synthetic identity; no hooks, signing, remote or parent repository changes.
    env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_AUTHOR_NAME='Synthetic Evaluation', GIT_AUTHOR_EMAIL='synthetic@example.invalid',
               GIT_COMMITTER_NAME='Synthetic Evaluation', GIT_COMMITTER_EMAIL='synthetic@example.invalid')
    return subprocess.check_output(['git', '-c', 'core.hooksPath=' + os.devnull,
                                    '-c', 'commit.gpgsign=false', '-C', str(repo), *args],
                                   env=env, text=True, stderr=subprocess.PIPE)


def replay(work, output):
    repo = work / 'project'
    repo.mkdir()
    (repo / 'evidence').mkdir()
    git(repo, 'init', '-q')
    (repo / 'context.md').write_text('# Synthetic current context\n\nLocal timeout is 10 seconds; no new approval or check yet.\n')
    (repo / 'config.json').write_text('{"timeout":10}\n')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'Synthetic initial state')
    directory = work / 'journal'
    stages = json.loads((HERE / 'scenario.json').read_text())['stages']
    results = []
    all_records = []
    for stage in stages:
        before = git(repo, 'rev-parse', 'HEAD').strip()
        name = stage['session']
        (repo / 'evidence' / (name + '.md')).write_text(stage['evidence'], encoding='utf-8')
        (repo / 'context.md').write_text(stage['context'], encoding='utf-8')
        (repo / 'config.json').write_text(json.dumps({'timeout': stage['timeout']}) + '\n')
        git(repo, 'add', '.')
        git(repo, 'commit', '-qm', 'Synthetic ' + name)
        after = git(repo, 'rev-parse', 'HEAD').strip()
        snapshots = output / name
        snapshots.mkdir()
        shutil.copytree(repo / 'evidence', snapshots / 'evidence')
        shutil.copy2(repo / 'context.md', snapshots / 'context.md')
        shutil.copy2(repo / 'config.json', snapshots / 'config.json')
        (snapshots / 'git-show.txt').write_text(git(repo, 'show', '--format=fuller', '--no-ext-diff', 'HEAD'))
        prior = {p.name: p.read_bytes() for p in directory.glob('*.jsonl')} if directory.exists() else {}
        commands, inputs, records = [], [], []
        for authored in stage['events']:
            fields = dict(authored)
            correction = fields.pop('supersedes_previous', False)
            payload = dict(fields, actor='synthetic-recorder',
                           sources=['evidence/' + name + '.md', 'context.md'], revision=after)
            if correction:
                payload['supersedes'] = records[-1]['event_id']
            inputs.append(payload)
            result = invoke(directory, 'append', '--session', name, payload=payload)
            commands.append(result)
            record = json.loads(result['stdout'])
            assert all(record[key] == value for key, value in payload.items())
            records.append(record)
        # Verify immutable previous session bytes and selected read-only behavior.
        assert all((directory / name).read_bytes() == data for name, data in prior.items())
        before_read = {p.name: p.read_bytes() for p in directory.glob('*.jsonl')}
        read = invoke(directory, 'read', '--session', name)
        commands.append(read)
        assert [json.loads(line) for line in read['stdout'].splitlines()] == records
        assert before_read == {p.name: p.read_bytes() for p in directory.glob('*.jsonl')}
        shutil.copytree(directory, snapshots / 'journal')
        write_json(snapshots / 'inputs.json', inputs)
        write_json(snapshots / 'commands.json', commands)
        all_records.extend(records)
        results.append({'session': name, 'before_revision': before, 'after_revision': after,
                        'appended_events': len(records), 'prior_session_bytes_preserved': True,
                        'read_roundtrip_and_no_mutation': True,
                        'payload_characters': sum(len(json.dumps(value)) for value in inputs),
                        'journal_bytes_at_cutoff': sum(p.stat().st_size for p in directory.glob('*.jsonl'))})
    full_read = invoke(directory, 'read')
    assert [json.loads(line) for line in full_read['stdout'].splitlines()] == all_records
    write_json(output / 'full-read.json', full_read)
    (output / 'git-history.txt').write_text(git(repo, 'log', '--reverse', '--format=fuller', '--stat'))
    # A portable Git history for inspecting all baseline revisions; no remote.
    git(repo, 'bundle', 'create', str(output / 'synthetic-history.bundle'), '--all')
    write_json(output / 'replay.json', results)
    return results


def latency(work, output):
    payload = dict(type='verification', status='observed', actor='synthetic-recorder',
                   summary='Seeded latency fixture; not an executed project check.',
                   sources=['synthetic:fixture'], revision='synthetic:revision',
                   check=dict(command='synthetic-check', scope='synthetic fixture', result='synthetic:passed'))

    def seed(directory, sessions, count):
        directory.mkdir()
        for index in range(sessions):
            name = f'session-{index:03}'
            with (directory / (name + '.jsonl')).open('w', encoding='utf-8') as stream:
                for _ in range(count):
                    record = dict(payload, schema_version=1, event_id=str(uuid4()), session_id=name,
                                  recorded_at='2026-09-28T00:00:00.000000Z')
                    stream.write(journal.encode(record))

    measurements = []
    for count in (10, 100, 1000, 10000):
        directory = work / ('size-' + str(count))
        seed(directory, 1, count)
        samples = []
        for repeat in range(3):
            before_count = count + repeat
            byte_count = (directory / 'session-000.jsonl').stat().st_size
            read = invoke(directory, 'read')
            assert len(read['stdout'].splitlines()) == before_count
            append = invoke(directory, 'append', '--session', 'session-000', payload=payload)
            samples.append({'records_before': before_count, 'file_bytes_before': byte_count,
                            'read_ms': read['elapsed_ms'], 'append_ms': append['elapsed_ms'],
                            'read_output_bytes': len(read['stdout'].encode('utf-8'))})
        measurements.append({'seeded_records': count, 'sessions': 1, 'samples': samples,
                             'median_read_ms': statistics.median(s['read_ms'] for s in samples),
                             'median_append_ms': statistics.median(s['append_ms'] for s in samples)})
    directory = work / 'many-sessions'
    seed(directory, 100, 10)
    samples = []
    for _ in range(3):
        selected = invoke(directory, 'read', '--session', 'session-000')
        full = invoke(directory, 'read')
        assert len(selected['stdout'].splitlines()) == 10
        assert len(full['stdout'].splitlines()) == 1000
        samples.append({'selected_read_ms': selected['elapsed_ms'], 'full_read_ms': full['elapsed_ms'],
                        'selected_output_bytes': len(selected['stdout'].encode()),
                        'full_output_bytes': len(full['stdout'].encode())})
    result = {'single_session': measurements, 'hundred_sessions': samples,
              'measurement_scope': 'warm-cache fresh CLI processes, including startup and captured output; 3 samples per condition'}
    write_json(output / 'latency.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True, help='new disposable directory')
    parser.add_argument('--output', type=Path, required=True, help='new result directory')
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=False)
    args.output.mkdir(parents=True, exist_ok=False)
    args.work, args.output = args.work.resolve(), args.output.resolve()
    files = [TOOL, HERE / 'protocol.md', HERE / 'scenario.json', Path(__file__).resolve(),
             ROOT / 'tests/test_event_journal.py']
    write_json(args.output / 'provenance.json', {
        'started_at': datetime.now(timezone.utc).isoformat(), 'python': sys.version,
        'platform': platform.platform(),
        'repository_base_revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'uncommitted_pilot': True,
        'sha256': {str(path.relative_to(ROOT)): digest(path) for path in files},
        'scope': 'synthetic CLI replay and local performance diagnostics; no model sessions'})
    replay(args.work, args.output)
    result = latency(args.work, args.output)
    print(json.dumps({'replay': '3 stages, 10 events passed mechanical controls',
                      'latency_medians': [{k: row[k] for k in ('seeded_records', 'median_read_ms', 'median_append_ms')}
                                          for row in result['single_session']]}, indent=2))


if __name__ == '__main__':
    main()
