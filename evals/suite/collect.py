"""Export allowlisted synthetic evidence and metrics, never raw Harbor logs/configs."""
import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from cases import CASES


def seconds(timing):
    if not timing or not timing.get('finished_at'):
        return None
    return (datetime.fromisoformat(timing['finished_at']) - datetime.fromisoformat(timing['started_at'])).total_seconds()


def collect(jobs, prefix):
    cases = {c['id']: c for c in CASES}
    trials, packets = [], []
    for job in sorted(jobs.glob(prefix + '-model-*')):
        if not job.is_dir():
            continue
        for result_path in sorted(job.glob('*/result.json')):
            data = json.loads(result_path.read_text())
            task, arm = data['task_name'].rsplit('-', 1)
            if task not in cases or arm not in {'baseline', 'skill'}:
                raise ValueError('Unexpected task: ' + data['task_name'])
            trial_id = hashlib.sha256((job.name + '/' + data['trial_name']).encode()).hexdigest()[:12]
            steps = []
            for i, step in enumerate(data.get('step_results') or [data]):
                folder = result_path.parent / 'steps' / step['step_name'] if 'step_name' in step else result_path.parent
                observed_path = folder / 'verifier/observed.json'
                observed = json.loads(observed_path.read_text()) if observed_path.exists() else None
                review_id = trial_id + f'-{i+1}'
                error = step.get('exception_info') or data.get('exception_info')
                steps.append(dict(review_id=review_id, mechanical_pass=observed['mechanical_pass'] if observed else False,
                                  execution_seconds=seconds(step.get('agent_execution')),
                                  execution_error=error.get('exception_type', 'unknown') if error else None,
                                  observed=observed))
                packets.append(dict(review_id=review_id, task=task, step=i+1,
                                    rubric=cases[task]['steps'][i]['rubric'], observed=observed))
            usage_parts = [s.get('agent_result') or {} for s in (data.get('step_results') or [data])]
            usage = {k: sum(p[k] for p in usage_parts) if all(p.get(k) is not None for p in usage_parts) else None
                     for k in ['n_input_tokens', 'n_cache_tokens', 'n_output_tokens']}
            trials.append(dict(id=trial_id, task=task, arm=arm, attempt=int(job.name.rsplit('-', 1)[1]),
                               task_checksum=data['task_checksum'], agent_info=data.get('agent_info'),
                               expected_steps=len(cases[task]['steps']),
                               usage={k: usage.get(k) for k in ['n_input_tokens', 'n_cache_tokens', 'n_output_tokens']},
                               steps=steps, total_trial_seconds=seconds(data)))
    return trials, sorted(packets, key=lambda p: p['review_id'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('jobs', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--prefix', required=True)
    args = parser.parse_args()
    trials, packets = collect(args.jobs, args.prefix)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'trials.json').write_text(json.dumps(trials, indent=2) + '\n')
    (args.output / 'review-packets.json').write_text(json.dumps(packets, indent=2) + '\n')
    print(f'Exported {len(trials)} trials and {len(packets)} step review packets. Review before publication.')
