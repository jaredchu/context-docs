"""Evaluation-only fixed-path interface; not shipped in the skills."""
import json
import os
from pathlib import Path
import subprocess
import sys


def execute(config, action, payload=None):
    root = Path(config['workspace'])
    if action == 'show':
        result = {}
        for case in ('no-git', 'sparse-git'):
            project = root / case
            files = {str(p.relative_to(project)): p.read_text() for p in project.rglob('*')
                     if p.is_file() and '.git' not in p.parts}
            result[case] = {'files': files}
            if case == 'sparse-git':
                result[case]['initial_committed_context'] = subprocess.check_output(
                    ['git', 'show', 'HEAD:notes/state.md'], cwd=project, text=True)
        if not config['read_only']:
            result['synthetic_events'] = config['feed']
        return result
    if action != 'save' or config['read_only']:
        raise ValueError('Save unavailable in this session')
    if not isinstance(payload, dict) or set(payload) != {'case', 'context', 'history', 'events'}:
        raise ValueError('Use case, context (string), history (string), events (array)')
    if payload['case'] not in ('no-git', 'sparse-git'):
        raise ValueError('Unknown case')
    if not isinstance(payload['context'], str) or not isinstance(payload['history'], str) or not isinstance(payload['events'], list):
        raise ValueError('Invalid payload types')
    if config['arm'] != 'jsonl' and payload['events']:
        raise ValueError('Only JSONL arm accepts events')
    if config['arm'] != 'markdown-log' and payload['history']:
        raise ValueError('Only Markdown-log arm accepts history')
    project = root / payload['case']
    # Helper is outside the model-write root and frozen by the runner.
    results = []
    for event in payload['events']:
        command = [sys.executable, config['helper'], '--directory', str(project / 'events'),
                   'append', '--session', 'capture']
        run = subprocess.run(command, input=json.dumps(event), text=True, capture_output=True)
        results.append({'command': command, 'exit_code': run.returncode,
                        'stdout': run.stdout, 'stderr': run.stderr})
        with Path(config['helper_calls']).open('a') as stream:
            stream.write(json.dumps(results[-1]) + '\n')
        if run.returncode:
            raise ValueError('Helper rejected event: ' + run.stderr)
    (project / 'notes/state.md').write_text(payload['context'])
    if payload['history']:
        (project / 'notes/history.md').write_text(payload['history'])
    return {'saved': payload['case'], 'appended': len(results)}


if __name__ == '__main__':
    try:
        config = json.loads(Path(sys.argv[1]).read_text())
        value = execute(config, sys.argv[2], json.loads(sys.argv[3]) if len(sys.argv) == 4 else None)
        print(json.dumps(value))
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
