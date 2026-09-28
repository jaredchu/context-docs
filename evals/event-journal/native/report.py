"""Mechanical summary only. Semantic judgments live separately in reviews.json."""
import json
import shlex
import guard
from pathlib import Path
import sys


def main():
    root = Path(sys.argv[1])
    trials = json.loads((root/'trials.json').read_text())
    summary = []
    for trial in trials:
        name = trial['name']
        rows = [json.loads(line) for line in (root/(name+'-stream.jsonl')).read_text().splitlines()]
        commands, result, model, errors, tool_failures = [], None, None, [], []
        for row in rows:
            if row.get('type') == 'system' and row.get('subtype') == 'init':
                model = row.get('model')
            if row.get('type') == 'assistant':
                for item in row.get('message', {}).get('content', []):
                    if item.get('type') == 'tool_use':
                        commands.append({'tool': item.get('name'), 'input': item.get('input')})
            if row.get('type') == 'user':
                for item in row.get('message', {}).get('content', []):
                    if item.get('type') == 'tool_result' and item.get('is_error'):
                        tool_failures.append(item)
            if row.get('type') == 'result':
                result = row
                if row.get('is_error') or row.get('permission_denials'):
                    errors.append({'is_error': row.get('is_error'), 'permission_denials': row.get('permission_denials')})
                (root/(name+'-final.txt')).write_text(row.get('result', ''))
            if row.get('type') == 'item.completed':
                item = row.get('item', {})
                if item.get('type') == 'command_execution':
                    commands.append({'tool': 'command_execution', 'command': item.get('command'), 'exit_code': item.get('exit_code')})
            if row.get('type') in ('error', 'turn.failed'):
                errors.append(row)
        prompt = (root/(name+'-prompt.txt')).read_text()
        prefix = shlex.split(prompt.split('commands: ', 1)[1].split(' show;', 1)[0])
        command_policy = []
        for call in commands:
            if call['tool'] == 'Bash':
                event = {'tool_name': 'Bash', 'tool_input': call['input']}
            else:
                shell = shlex.split(call['command'])
                inner = shell[2] if len(shell) == 3 and shell[1] in ('-lc', '-c') else call['command']
                event = {'tool_name': 'Bash', 'tool_input': {'command': inner}}
            command_policy.append(guard.allowed(event, {'prefix': prefix, 'read_only': name.endswith('investigate')}))
        hookfile = root/(name+'-hooks.jsonl')
        hooks = [json.loads(l) for l in hookfile.read_text().splitlines()] if hookfile.exists() else []
        journalfiles = list((root/name).glob('*/events/*.jsonl'))
        records = [json.loads(l) for p in journalfiles for l in p.read_text().splitlines()]
        sizes = {str(p.relative_to(root/name)): p.stat().st_size for p in (root/name).glob('*/notes/*.md')}
        sizes.update({str(p.relative_to(root/name)): p.stat().st_size for p in journalfiles})
        allowed_new = {'helper-calls.jsonl'} | {f'{case}/{path}' for case in ('no-git', 'sparse-git') for path in ('notes/history.md', 'events/capture.jsonl')}
        unexpected = sorted(set(trial['after']) - set(trial['before']) - allowed_new)
        summary.append({'name': name, 'unexpected_new_files': unexpected, 'exit_code': trial['exit_code'], 'seconds': trial['seconds'],
                        'model_from_stream': model, 'protected_unchanged': trial['protected_unchanged'],
                        'audit_unchanged': trial['audit_unchanged'], 'commands': commands,
                        'command_policy': command_policy, 'hooks': len(hooks), 'denied': sum(not h['allowed'] for h in hooks),
                        'errors': errors, 'tool_failures': tool_failures, 'journal_records': len(records), 'record_file_bytes': sizes,
                        'terminal_result': result is not None if name.startswith('claude') else any(r.get('type')=='turn.completed' for r in rows)})
    (root/'mechanical-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    lines = ['| Client / capture format | Capture seconds | Capture calls | Stored context + history bytes (both projects) | Fresh audit unchanged |',
             '| --- | ---: | ---: | ---: | --- |']
    for row in summary:
        if row['name'].endswith('-capture'):
            readers = [r for r in summary if r['name'] == row['name'].replace('-capture', '-investigate')]
            unchanged = readers[0]['audit_unchanged'] if readers else 'pending'
            lines.append(f"| {row['name'].removesuffix('-capture')} | {row['seconds']} | {len(row['commands'])} | {sum(row['record_file_bytes'].values())} | {unchanged} |")
    (root/'table.md').write_text('\n'.join(lines)+'\n')
    for row in summary:
        print(row['name'], row['exit_code'], row['seconds'], 'commands',len(row['commands']),
              'protected',row['protected_unchanged'], 'audit',row['audit_unchanged'], 'errors',len(row['errors']))


if __name__ == '__main__':
    main()
