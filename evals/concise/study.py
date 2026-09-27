"""Build and report the frozen, two-variant concision study using the shared harness."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / 'suite'))
from build import build, spec_for
from collect import collect
from report import summarize
from verify import grade, snapshot
from selftest import put
from fixtures import CASES

CONDITIONS = ('original', 'candidate')


def hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()}


def build_study(destination):
    packages = destination.parent / (destination.name + '-skills')
    packages.mkdir(parents=True, exist_ok=False)
    files = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', 'v0.1.0', '--', 'skills/context-docs'], cwd=ROOT, text=True).splitlines()
    variants = {}
    for arm in CONDITIONS:
        target = packages / arm / 'context-docs'
        for name in files:
            p = target / Path(name).relative_to('skills/context-docs')
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(subprocess.check_output(['git', 'show', 'v0.1.0:' + name], cwd=ROOT))
        if arm == 'original':
            assert (target / 'SKILL.md').read_bytes() == (HERE / 'original-SKILL.md').read_bytes()
        else:
            shutil.copy2(HERE / 'candidate-SKILL.md', target / 'SKILL.md')
        variants[arm] = target
    manifest = build(destination, CASES, variants, attempts=2)
    manifest['candidate_freeze_commit'] = '136bd31'
    manifest['execution_commit'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    manifest['variant_files'] = {arm: hashes(path) for arm, path in variants.items()}
    manifest['study_files'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.iterdir() if p.is_file()}
    manifest['initial_words'] = {c['id']: sum(len(s.split()) for p, s in {**c['files'], **c['uncommitted']}.items() if p.endswith('.md')) for c in CASES}
    (destination.parent / (destination.name + '-manifest.json')).write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(manifest['initial_words']))


def selftest():
    n = 0
    for c in CASES:
        with tempfile.TemporaryDirectory() as temp:
            root, output = Path(temp) / 'project', Path(temp) / 'output'
            root.mkdir(); output.mkdir()
            put(root, {**c['files'], **c['uncommitted']})
            assert sum(len(v.split()) for p, v in snapshot(root).items() if p.endswith('.md')) >= 500
            for i, step in enumerate(c['steps']):
                put(root, step['updates'])
                before = snapshot(root)
                spec = spec_for(c, i, before)
                if not spec['allow_noop']:
                    assert not grade(spec, root, output, before)['mechanical_pass'], c['id']
                    n += 1
                put(root, step['oracle'])
                assert grade(spec, root, output, before)['mechanical_pass'], (c['id'], grade(spec, root, output, before)['checks'])
                n += 1
                saved = (root / 'README.md').read_text()
                (root / 'README.md').write_text(saved + '\n[Broken](absent.md)\n')
                assert not grade(spec, root, output, before)['mechanical_pass']
                (root / 'README.md').write_text(saved)
                n += 1
    print(f'{n} new-fixture control assertions passed.')


def control_results(jobs, prefix):
    controls = []
    for mode in ('oracle', 'nop'):
        job = jobs / f'{prefix}-{mode}-1'
        for path in sorted(job.glob('*/result.json')):
            data = json.loads(path.read_text())
            steps = []
            for step in data.get('step_results') or [data]:
                folder = path.parent / 'steps' / step['step_name'] if 'step_name' in step else path.parent
                observed = json.loads((folder / 'verifier/observed.json').read_text())
                steps.append(dict(checks=observed['checks'], mechanical_pass=observed['mechanical_pass'],
                                  before_sha256=observed['before_sha256']))
            controls.append(dict(task=data['task_name'], mode=mode, task_checksum=data['task_checksum'],
                                 execution_error=data.get('exception_info'), steps=steps))
    assert len(controls) == len(CASES) * 2
    assert all(not c['execution_error'] and all(s['mechanical_pass'] for s in c['steps']) == (c['mode'] == 'oracle') for c in controls)
    return controls


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('selftest')
    b = sub.add_parser('build'); b.add_argument('destination', type=Path)
    c = sub.add_parser('collect'); c.add_argument('jobs', type=Path); c.add_argument('output', type=Path); c.add_argument('--prefix', required=True)
    r = sub.add_parser('report'); r.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.command == 'selftest':
        selftest()
    elif args.command == 'build':
        build_study(args.destination.resolve())
    elif args.command == 'collect':
        trials, packets = collect(args.jobs, args.prefix, CASES, CONDITIONS)
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / 'trials.json').write_text(json.dumps(trials, indent=2) + '\n')
        (args.output / 'review-packets.json').write_text(json.dumps(packets, indent=2) + '\n')
        (args.output / 'controls.json').write_text(json.dumps(control_results(args.jobs, args.prefix), indent=2) + '\n')
        print(f'Collected {len(trials)} trials and {len(packets)} step review packets.')
    else:
        trials = json.loads((args.output / 'trials.json').read_text())
        reviews = json.loads((args.output / 'reviews.json').read_text())
        # These fixtures inject configuration only between passes. Each later
        # Markdown input must therefore match the actual preceding output exactly.
        for trial in trials:
            for previous, current in zip(trial['steps'], trial['steps'][1:]):
                assert current['observed']['before_documents'] == previous['observed']['documents'], 'Input continuity mismatch'
        summary, table = summarize(trials, reviews['steps'], CASES, CONDITIONS, attempts=2)
        quality = all(t['success'] for t in trials)
        lower = sum(summary['by_task'][c['id']]['candidate']['median_word_delta'] < summary['by_task'][c['id']]['original']['median_word_delta'] for c in CASES)
        growth_guard = all(summary['by_task'][c['id']]['candidate']['median_word_delta'] <= summary['by_task'][c['id']]['original']['median_word_delta'] + 50 for c in CASES)
        no_churn = all(t['third_pass_unchanged'] for t in trials if len(t['steps']) == 3)
        summary['adoption_gate'] = dict(all_trials_pass=quality, tasks_with_lower_candidate_growth=lower, no_task_over_50_extra_words=growth_guard, final_passes_unchanged=no_churn, passed=quality and lower >= 2 and growth_guard and no_churn)
        (args.output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
        (args.output / 'table.md').write_text(table + '\n')
        print(table); print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
