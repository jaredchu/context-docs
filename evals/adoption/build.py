"""Build two bounded adoption/repeat regressions with the existing Harbor runner."""
import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'evals/suite'))
from build import build, write
from verify import grade

RULE = ('\nUse $context-docs after meaningful changes to project facts, decisions, procedures, '
        'blockers or next actions. Read the skill before maintenance. Preserve project rules '
        'and decisions, check links and the diff, keep audits read-only, and avoid changes '
        'when nothing durable changed.\n')
REQUEST = 'Use $adopt-context-docs to adopt Context Docs in this project, including its ongoing AGENTS.md maintenance rule.'
REPEAT = REQUEST + ' No new project evidence or decisions have been supplied.'
CODE = '''import csv
import json
import sys

with open(sys.argv[1], newline="") as source:
    rows = list(csv.DictReader(source))
with open(sys.argv[2], "w") as target:
    json.dump(rows, target)
'''
POLICY = '# Project instructions\n\nUse the existing knowledge/ layout.\nProduction publication requires owner approval.\nUse Approved, Proposed and Unknown as decision statuses.\n'
STATE = '# Current context\n\nApproved: keep the pilot offline because customer data must stay local.\nProposed: cloud sync; no owner approval recorded.\n'
BLOCKER = '\nUnknown: RESTORE-81 remains blocked on a missing test fixture.\n'
CASES = [
    dict(id='adopt-empty-docs', files={'convert.py': CODE}, uncommitted={},
         protected=[], immutable=['convert.py'], steps=[
             dict(request=REQUEST, updates={}, oracle={
                 'README.md': '# CSV conversion utility\n\n[Context](context.md).\n',
                 'context.md': '# Context\n\nThe local script reads CSV rows and writes a JSON array.\nRun `python3 convert.py input.csv output.json`; see [source](convert.py).\n',
                 'AGENTS.md': '# Project instructions\n' + RULE,
             }, rubric=[
                 'Creates useful discoverable context grounded in the CSV script, without invented approvals or deployment claims.',
                 'Adds ongoing context-docs maintenance guidance to project AGENTS.md; does not install skill copies or change code.',
             ]),
             dict(request=REPEAT, updates={}, oracle={}, rubric=[
                 'Repeated adoption leaves the established documentation and instructions byte-identical; no duplicate rules or files.',
             ]),
         ]),
    dict(id='adopt-existing', files={'README.md': '# Offline pilot\n\n[Current context](knowledge/state.md).\n',
                                  'AGENTS.md': POLICY, 'knowledge/state.md': STATE},
         uncommitted={'knowledge/state.md': STATE+BLOCKER}, protected=[
             'Use the existing knowledge/ layout.', 'Production publication requires owner approval.',
             'Use Approved, Proposed and Unknown as decision statuses.',
             'Approved: keep the pilot offline because customer data must stay local.',
             'Proposed: cloud sync; no owner approval recorded.', BLOCKER.strip(),
         ], immutable=[], steps=[
             dict(request=REQUEST, updates={}, oracle={'AGENTS.md': POLICY+RULE}, rubric=[
                 'Preserves layout, original instructions, Approved offline rationale, Proposed cloud status and uncommitted restore blocker.',
                 'Adds one effective ongoing context-docs maintenance rule in AGENTS.md; no competing context files or copied skills.',
             ]),
             dict(request=REPEAT, updates={}, oracle={}, rubric=[
                 'Repeated adoption preserves all files byte for byte, including prior uncommitted work and maintenance guidance.',
             ]),
         ]),
]


def controls():
    results=[]
    for case in CASES:
        initial={**case['files'], **case['uncommitted']}
        reference={**initial, **case['steps'][0]['oracle']}
        spec=dict(id=case['id'], before=initial, protected=case['protected'],
                  immutable=case['immutable'], entry='README.md', allow_noop=False)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'project';root.mkdir();output=Path(tmp)/'output';output.mkdir()
            for p,s in initial.items(): write(root/p,s)
            assert not grade(spec,root,output)['mechanical_pass']
            for p,s in reference.items():write(root/p,s)
            assert grade(spec,root,output)['mechanical_pass']
            repeated={**spec,'before':reference,'allow_noop':True}
            assert grade(repeated,root,output)['mechanical_pass']
            (root/'README.md').write_text('# Lost entry point\n\n[Broken](missing.md)\n')
            assert not grade(repeated,root,output)['mechanical_pass']
        results.append({'case':case['id'],'reference':True,'unchanged_first_pass_rejected':True,
                        'repeat_reference':True,'broken_link_rejected':True})
    return results


def main():
    parser=argparse.ArgumentParser();parser.add_argument('destination',type=Path);args=parser.parse_args()
    checks=controls()
    dest=args.destination.resolve()
    manifest=build(dest,cases=CASES,variants={'skill':ROOT/'skills'},attempts=1)
    for case in CASES:
        for i in range(2):
            folder=dest/(case['id']+'-skill')/'steps'/f'pass-{i+1}'
            p=folder/'instruction.md';s=p.read_text().replace(
                'Use the context-docs skill at /opt/context-docs/SKILL.md and its relevant references.',
                'Read the adoption skill at /opt/context-docs/adopt-context-docs/SKILL.md and its linked core skill. These are installed outside the project; read them there.')
            p.write_text(s)
            p=folder/'tests/spec.json';spec=json.loads(p.read_text());spec['allow_noop']=i==1;p.write_text(json.dumps(spec,indent=2)+'\n')
    manifest['adoption_files']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in sorted((ROOT/'skills/adopt-context-docs').rglob('*')) if p.is_file()}
    manifest['adoption_builder_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    manifest['controls']=checks
    write(dest.parent/(dest.name+'-manifest.json'),json.dumps(manifest,indent=2)+'\n')
    print('Built two trajectories / four fresh model sessions. Eight static grader controls passed.')

if __name__=='__main__':main()
