"""Run Harbor controls or the three paired blocks. Raw jobs stay local."""
import argparse
import json
import os
import subprocess
from pathlib import Path
from build import CLI_VERSION, HERE
from cases import CASES


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('suite', type=Path)
    parser.add_argument('jobs', type=Path)
    parser.add_argument('--mode', choices=['oracle', 'nop', 'model'], required=True)
    parser.add_argument('--prefix', required=True)
    args = parser.parse_args()
    manifest = json.loads((args.suite.parent / (args.suite.name + '-manifest.json')).read_text())
    case_ids = list(dict.fromkeys(p['task'] for p in manifest['packages']))
    conditions = manifest['conditions']
    args.jobs.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    if args.mode == 'model':
        auth = Path(env.get('CODEX_AUTH_JSON_PATH', str(Path(env.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'auth.json')))
        if not auth.is_file():
            raise SystemExit('A Codex auth.json is required; set CODEX_AUTH_JSON_PATH to an existing login file.')
        env['CODEX_AUTH_JSON_PATH'] = str(auth.resolve())
        for key in ['OPENAI_API_KEY', 'CODEX_API_KEY', 'OPENAI_BASE_URL']:
            env.pop(key, None)
        agent = dict(name='codex', model_name='openai/gpt-6-astra', kwargs=dict(
            version=CLI_VERSION, reasoning_effort='low', web_search='disabled',
            config=str(HERE / 'codex.toml')))
    else:
        agent = dict(name=args.mode)
    for repeat in range(manifest['attempts'] if args.mode == 'model' else 1):
        name = f'{args.prefix}-{args.mode}-{repeat+1}'
        if (args.jobs / name).exists():
            raise SystemExit(f'Refusing to overwrite existing job {name}. Choose a new prefix; do not discard failed attempts.')
        tasks = []
        for index, case_id in enumerate(case_ids):
            arms = conditions if (repeat + index) % 2 == 0 else conditions[::-1]
            if args.mode != 'model':
                arms = [conditions[0]]
            tasks += [dict(path=str((args.suite / (case_id + '-' + arm)).resolve())) for arm in arms]
        config = dict(job_name=name, jobs_dir=str(args.jobs.resolve()), agents=[agent], tasks=tasks,
                      n_attempts=1, n_concurrent_trials=2, retry=dict(max_retries=0))
        path = args.jobs / (name + '.json')
        path.write_text(json.dumps(config, indent=2) + '\n')
        print(f'Starting {name}: {len(tasks)} trials', flush=True)
        subprocess.run(['uv', 'tool', 'run', '--from', 'harbor==0.23.0', 'harbor', 'run', '--config', str(path)], env=env, check=True)
        result = json.loads((args.jobs / name / 'result.json').read_text())
        if result['stats']['n_errored_trials']:
            raise SystemExit(f'Infrastructure errors recorded in {name}; inspect before starting another block.')
        if args.mode != 'model':
            for trial in (args.jobs / name).glob('*/result.json'):
                data = json.loads(trial.read_text())
                reward = data['verifier_result']['rewards']['mechanical']
                if (args.mode == 'oracle' and reward != 1) or (args.mode == 'nop' and reward == 1):
                    raise SystemExit(f'Control failed in {trial}; fix the harness before model runs.')


if __name__ == '__main__':
    main()
