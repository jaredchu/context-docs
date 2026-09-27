"""Audit recorded user messages against generated task prompts; export counts only.

This detects unexpected injected user instructions, not malicious hidden channels.
Raw sessions can contain private service metadata and must remain local.
"""
import argparse
import json
from pathlib import Path


def audit(jobs, suite, prefix):
    result = dict(trials=0, sessions=0, expected_task_messages=0,
                  environment_messages=0, unexpected_user_messages=0,
                  injected_agents_messages=0, missing_sessions=0)
    for job in sorted(jobs.glob(prefix + '-model-*')):
        if not job.is_dir():
            continue
        for path in sorted(job.glob('*/result.json')):
            trial = json.loads(path.read_text())
            result['trials'] += 1
            for step in trial.get('step_results') or [trial]:
                rel = Path('steps') / step['step_name'] if 'step_name' in step else Path()
                expected = (suite / trial['task_name'] / rel / 'instruction.md').read_text().strip()
                sessions = list((path.parent / rel / 'agent/sessions').rglob('*.jsonl'))
                if len(sessions) != 1:
                    result['missing_sessions'] += 1
                for session in sessions:
                    result['sessions'] += 1
                    for line in session.read_text().splitlines():
                        event = json.loads(line)
                        payload = event.get('payload', {})
                        if event.get('type') != 'response_item' or payload.get('role') != 'user':
                            continue
                        text = '\n'.join(c.get('text', '') for c in payload.get('content', []))
                        if text.strip() == expected:
                            result['expected_task_messages'] += 1
                        elif text.startswith('<environment_context>') and '<cwd>/workspace</cwd>' in text:
                            result['environment_messages'] += 1
                        else:
                            result['unexpected_user_messages'] += 1
                        result['injected_agents_messages'] += int('# AGENTS.md instructions for' in text)
    result['passed'] = (result['sessions'] > 0 and result['expected_task_messages'] == result['sessions']
                        and result['environment_messages'] == result['sessions']
                        and not result['unexpected_user_messages'] and not result['injected_agents_messages']
                        and not result['missing_sessions'])
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('jobs', type=Path)
    parser.add_argument('suite', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--prefix', required=True)
    args = parser.parse_args()
    result = audit(args.jobs, args.suite, args.prefix)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    if not result['passed']:
        raise SystemExit('Unexpected or missing recorded input; inspect locally before claiming isolation.')
