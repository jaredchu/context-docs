"""Build self-contained Harbor task packages from public synthetic fixtures."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path
from cases import CASES

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CLI_VERSION = '0.158.0-alpha.2'


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def writer_script(files, base):
    # JSON embedded in repr avoids shell interpolation of fixture content.
    return 'python3 - <<\'PY\'\nimport json\nfrom pathlib import Path\nfiles=json.loads(' + repr(json.dumps(files)) + ')\nfor name, text in files.items():\n    p=Path(' + repr(base) + ')/name\n    p.parent.mkdir(parents=True,exist_ok=True)\n    p.write_text(text)\nPY\n'


def spec_for(case, step, before):
    entry = next((p for p in before if p.endswith(('context.md', 'current.md'))), 'README.md')
    return dict(id=case['id'], before=before, protected=case['protected'], immutable=case['immutable'],
                allow_noop=step == 2, entry=entry, rubric=case['steps'][step]['rubric'])


def build(destination):
    destination.mkdir(parents=True, exist_ok=False)
    manifest = dict(harbor_version='0.23.0', codex_version=CLI_VERSION, model='gpt-6-astra',
                    effort='low', task_count=8, conditions=['baseline', 'skill'], attempts=3,
                    skill_files={}, suite_files={}, packages=[])
    for p in sorted((ROOT / 'skills/context-docs').rglob('*')):
        if p.is_file():
            manifest['skill_files'][str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted(HERE.iterdir()):
        if p.suffix not in {'.py', '.toml'}:
            continue
        manifest['suite_files'][p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    for case in CASES:
        for arm in ['baseline', 'skill']:
            task = destination / (case['id'] + '-' + arm)
            initial = {**case['files'], **case['uncommitted']}
            for name, body in case['files'].items():
                write(task / 'environment/input' / name, body)
            write(task / 'environment/uncommitted.sh', writer_script(case['uncommitted'], '/workspace'))
            dockerfile = f'''FROM node:22-bookworm-slim@sha256:48e4b67d85f87bd551df43704e24d252f56cc5f8e9718841aace50f19948f0f9
RUN apt-get update && apt-get install -y --no-install-recommends python3 git ripgrep curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN npm install -g @openai/codex@{CLI_VERSION}
WORKDIR /workspace
COPY input/ /workspace/
RUN git init -q && git config user.name "Fixture Author" && git config user.email "fixture@example.invalid" && git add . && git commit -qm "Initial synthetic fixture"
COPY uncommitted.sh /tmp/uncommitted.sh
RUN bash /tmp/uncommitted.sh && rm /tmp/uncommitted.sh && mkdir /output
'''
            if arm == 'skill':
                shutil.copytree(ROOT / 'skills/context-docs', task / 'environment/skill')
                dockerfile += 'COPY skill/ /opt/context-docs/\n'
            write(task / 'environment/Dockerfile', dockerfile)
            config = '''schema_version = "1.4"
multi_step_reward_strategy = "mean"
[metadata]
category = "documentation"
[agent]
timeout_sec = 240
[verifier]
timeout_sec = 30
[environment]
build_timeout_sec = 600
cpus = 1
memory_mb = 1024
storage_mb = 2048
'''
            multi = len(case['steps']) > 1
            if multi:
                for i in range(len(case['steps'])):
                    config += f'\n[[steps]]\nname = "pass-{i+1}"\n'
            write(task / 'task.toml', config)
            before = dict(initial)
            for i, step in enumerate(case['steps']):
                folder = task / 'steps' / f'pass-{i+1}' if multi else task
                before.update(step['updates'])
                common = ('Work only in /workspace and /output. This is a synthetic project; use only its supplied evidence. '
                          'Do not contact external services or inspect harness files, /tests, /solution, /logs or credentials. '
                          'Do not change code/configuration or Git history. Preserve existing project layout and unique information. '
                          'No live environment access is supplied. Complete the task autonomously using the available evidence.\n\n')
                if arm == 'skill':
                    common += 'Use the context-docs skill at /opt/context-docs/SKILL.md and its relevant references.\n\n'
                write(folder / 'instruction.md', common + step['request'] + '\n')
                spec = spec_for(case, i, before)
                write(folder / 'tests/spec.json', json.dumps(spec, indent=2) + '\n')
                shutil.copy2(HERE / 'verify.py', folder / 'tests/verify.py')
                write(folder / 'tests/test.sh', '#!/bin/bash\nset -euo pipefail\npython3 /tests/verify.py /tests/spec.json\n')
                oracle = {p: v for p, v in step['oracle'].items() if not p.startswith('@output/')}
                output = {p.removeprefix('@output/'): v for p, v in step['oracle'].items() if p.startswith('@output/')}
                write(folder / 'solution/solve.sh', '#!/bin/bash\nset -euo pipefail\n' + writer_script(oracle, '/workspace') + writer_script(output, '/output'))
                if multi:
                    # Prior-step graders must not remain visible to the next agent.
                    write(folder / 'workdir/setup.sh', '#!/bin/bash\nset -euo pipefail\nrm -rf /tests /solution\n' + writer_script(step['updates'], '/workspace') + 'rm /workspace/setup.sh\n')
                before.update(oracle)
            manifest['packages'].append(dict(name=task.name, task=case['id'], arm=arm, steps=len(case['steps'])))
    write(destination.parent / (destination.name + '-manifest.json'), json.dumps(manifest, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    build(args.destination.resolve())
    print('Built 16 Harbor packages (8 tasks × 2 conditions).')
