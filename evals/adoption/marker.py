"""Build marker, repeat-date, existing-adoption and audit-only regressions."""
import argparse
import copy
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
loader=importlib.util.spec_from_file_location('adoption_cases',Path(__file__).with_name('build.py'))
adoption=importlib.util.module_from_spec(loader);loader.loader.exec_module(adoption)
from build import build,write
from verify import grade

CASES=copy.deepcopy(adoption.CASES)
for case in CASES:
    case['steps'][0]['request']+=' The evaluation date is 2026-10-01.'
    case['steps'][1]['request']+=' The evaluation date is now 2026-10-02.'
    entry='context.md' if case['id']=='adopt-empty-docs' else 'knowledge/state.md'
    case['steps'][0]['oracle']['AGENTS.md']+='\nMethod: context-docs\nAdopted: 2026-10-01\nEntry point: '+entry+'\n'
    case['steps'][0]['rubric'].append('Records one completed-adoption marker with the supplied adoption date and actual context entry point; no claim of certified accuracy.')
    case['steps'][1]['rubric'].append('Preserves the original 2026-10-01 adoption date on the next day and does not duplicate the marker.')

already={'README.md':'# Offline pilot\n\n[Current context](knowledge/state.md).\n',
         'AGENTS.md':adoption.POLICY+adoption.RULE,
         'knowledge/state.md':adoption.STATE}
CASES.append(dict(id='adopt-unmarked',files=already,uncommitted={'knowledge/state.md':adoption.STATE+adoption.BLOCKER},
                 protected=[adoption.POLICY.strip(),adoption.RULE.strip(),adoption.BLOCKER.strip()],immutable=['README.md','knowledge/state.md'],steps=[dict(
                     request=adoption.REQUEST+' The evaluation date is 2026-10-01. No original adoption date has been recorded.',updates={},
                     oracle={'AGENTS.md':already['AGENTS.md']+'\nMethod: context-docs\nAdopted: unknown\nEntry point: knowledge/state.md\n'},rubric=[
                         'Recognizes existing adoption from guidance and documents despite the absent marker; does not initialize another context file or duplicate instructions.',
                         'Adds only one marker to AGENTS.md, retaining original guidance and using unknown for the undocumented adoption date.',
                     ])]))
# Immutable checks use the case files; represent the pre-existing dirty state there too.
CASES[-1]['files']['knowledge/state.md']=adoption.STATE+adoption.BLOCKER
CASES.append(dict(id='audit-only',files=copy.deepcopy(already),uncommitted={},protected=[],immutable=list(already),steps=[dict(
    request='Use $adopt-context-docs to audit adoption only. Do not edit project files. Report whether existing instructions and documents already follow the method, and distinguish a missing marker from non-adoption. Write your report to /output/audit.md.',updates={},
    oracle={'@output/audit.md':'The existing maintenance guidance and linked context implement the method. Adoption is present but unmarked; the original date is unknown. A marker could be added in a separately requested edit. No project files changed.\n'},rubric=[
        'Reports existing workflow adoption with an absent marker and unrecorded date; does not classify the project as non-adopted merely because its marker is missing.',
        'Leaves every project file byte-identical and writes the audit report only to /output/audit.md.',
    ])]))


def controls():
    results=[]
    for case in CASES:
        initial={**case['files'],**case['uncommitted']}
        spec=dict(id=case['id'],before=initial,protected=case['protected'],immutable=case['immutable'],entry='README.md',allow_noop=False)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'project';root.mkdir();out=Path(tmp)/'output';out.mkdir()
            for p,s in initial.items():write(root/p,s)
            assert not grade(spec,root,out)['mechanical_pass']
            for p,s in case['steps'][0]['oracle'].items():
                write(out/p.removeprefix('@output/') if p.startswith('@output/') else root/p,s)
            assert grade(spec,root,out)['mechanical_pass']
            if case['id']=='audit-only':
                write(root/'AGENTS.md',already['AGENTS.md']+'\nMethod: context-docs\n')
            else:write(root/'README.md','# Invalid\n\n[Broken](missing.md)\n')
            assert not grade(spec,root,out)['mechanical_pass']
        results.append({'case':case['id'],'reference':True,'incomplete_noop_rejected':True,'invalid_change_rejected':True})
    return results


def main():
    parser=argparse.ArgumentParser();parser.add_argument('destination',type=Path);args=parser.parse_args()
    checks=controls();dest=args.destination.resolve()
    manifest=build(dest,cases=CASES,variants={'skill':ROOT/'skills'},attempts=1)
    for case in CASES:
        for i in range(len(case['steps'])):
            task=dest/(case['id']+'-skill')
            folder=task/'steps'/f'pass-{i+1}' if len(case['steps'])>1 else task
            p=folder/'instruction.md';p.write_text(p.read_text().replace(
                'Use the context-docs skill at /opt/context-docs/SKILL.md and its relevant references.',
                'Read the adoption skill at /opt/context-docs/adopt-context-docs/SKILL.md and its linked core skill. These are installed outside the project; read them there.'))
            p=folder/'tests/spec.json';spec=json.loads(p.read_text());spec['allow_noop']=i>0;p.write_text(json.dumps(spec,indent=2)+'\n')
    manifest['adoption_files']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'skills/adopt-context-docs').rglob('*')) if p.is_file()}
    manifest['marker_source_files']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_name('build.py')]}
    manifest['controls']=checks
    write(dest.parent/(dest.name+'-manifest.json'),json.dumps(manifest,indent=2)+'\n')
    print('Built four trials / six model sessions. Twelve static grader controls passed. Marker semantics require explicit review.')

if __name__=='__main__':main()
