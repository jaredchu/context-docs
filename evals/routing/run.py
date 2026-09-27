"""Controlled README routing and full-text exposure follow-up; prior artifacts unchanged."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'public'))
import study as base
sys.path.insert(0,str(HERE))
from exposure import audit, selftest as exposure_selftest
MODES=['discovery','directed']
PREVIOUS=ROOT/'evals/results/2026-09-27-public'


def sources():
    paths=list(HERE.glob('*.py'))+[HERE/'README.md',PREVIOUS/'maintenance.json']
    return {str(p.relative_to(ROOT)):base.sha(p.read_bytes()) for p in paths if p.is_file()}


def artifacts():
    maintenance=json.loads((PREVIOUS/'maintenance.json').read_text())
    out=[]
    for w in base.CASES:
        original,provenance=base.corpus(w)
        for arm in base.ARMS:
            files=dict(original);target='docs/index.rst';parent_id=None
            if arm!='upstream':
                t=next(t for t in maintenance if t['metadata']['world']==w and t['metadata']['arm']==arm)
                additions=t['steps'][0]['observed']['additions']
                assert len(additions)==1 and not set(additions)&set(original)
                files.update(additions); target=next(iter(additions));parent_id=t['id']
                assert base.digest(files)==t['steps'][0]['observed']['files_sha256']
            before=base.digest(files)
            route=f'## Contributor orientation\n\n[Project orientation]({target})\n\n---\n\n'
            files['README.md']=route+files['README.md']
            out.append(dict(world=w,arm=arm,files=files,target=target,route_prefix=route,
                parent_trial_id=parent_id,original_snapshot_sha256=before,routed_snapshot_sha256=base.digest(files),upstream=provenance))
    return out


def prompt(world, mode):
    if mode=='discovery':
        lead='Begin by reading README.md. Then choose the project sources you need to answer the questions.\n\n'
    else:
        lead=('Begin by reading README.md. Follow its Project orientation link and read that linked document in full before writing answers. '
            'Then check relevant project sources as needed; the orientation document is a guide, not a replacement for evidence.\n\n')
    return lead+base.reader_prompt(world,1)


def build_suite(destination):
    cases=[];meta={};arts=artifacts()
    for mode in MODES:
        for a in arts:
            name='route-'+base.sha(f'{mode}/{a["world"]}/{a["arm"]}'.encode())[:12]
            cases.append(base.case(name,a['files'],{'@output/answers.json':json.dumps(base.answers(a['world']),indent=2)+'\n'}))
            meta[name]={k:v for k,v in a.items() if k not in ['files','upstream']}
            meta[name].update(mode=mode,variant=1,files_sha256=a['routed_snapshot_sha256'])
    manifest=base.build(destination,cases,{'reader':None},attempts=1)
    manifest.update(kind='reader',routing_sources=sources(),upstream={a['world']:a['upstream'] for a in arts})
    for p in manifest['packages']:
        m=meta[p['task']];task=destination/p['name']
        base.write(task/'instruction.md',prompt(m['world'],m['mode']))
        files=next(c['files'] for c in cases if c['id']==p['task'])
        base.dump(task/'tests/spec.json',dict(before=files,ids=[q['id'] for q in base.CASES[m['world']]['questions']]))
        shutil.copy2(HERE.parent/'public/reader_verify.py',task/'tests/verify.py')
        assert not (task/'environment/skill').exists()
    base.finalize(destination,manifest,meta)


def exposure_audit(suite,jobs,prefix,output):
    manifest=json.loads((suite.parent/(suite.name+'-manifest.json')).read_text())
    mapping={p['name']:p for p in manifest['packages']};rows=[]
    for result in sorted((jobs/(prefix+'-model-1')).glob('*/result.json')):
        d=json.loads(result.read_text());m=mapping[d['task_name']]
        sessions=list((result.parent/'agent/sessions').rglob('*.jsonl'))
        tid=base.sha((prefix+'/'+d['trial_name']).encode())[:12]
        if len(sessions)!=1:
            rows.append(dict(trial_id=tid,metadata=m,error='missing_or_multiple_sessions'));continue
        files=json.loads((suite/m['name']/'tests/spec.json').read_text())['before']
        rows.append(dict(trial_id=tid,metadata=m,**audit(sessions[0],files,m['target'])))
    base.dump(output,rows)
    print('Full orientation exposure:',sum(r.get('target',{}).get('full_text_exposed',False) for r in rows),'/',len(rows))


def selftest():
    exposure_selftest()
    from report import selftest as report_selftest
    report_selftest()
    arts=artifacts();assert len(arts)==6
    for a in arts:
        original,_=base.corpus(a['world'])
        assert a['files']['README.md']==a['route_prefix']+original['README.md']
        assert all(a['files'][p]==s for p,s in original.items() if p!='README.md')
        assert a['target'] in a['files']
    for w in base.CASES:
        for mode in MODES:
            assert all(label not in prompt(w,mode) for label in ['ordinary handoff','skill arm','Context Docs'])
    print('6 routed artifacts preserve all prior bytes except the declared README prefix; prompts do not label arms.')


def main():
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('selftest')
    b=sub.add_parser('build');b.add_argument('suite',type=Path)
    a=sub.add_parser('exposure');a.add_argument('suite',type=Path);a.add_argument('jobs',type=Path);a.add_argument('output',type=Path);a.add_argument('--prefix',required=True)
    args=p.parse_args()
    if args.command=='selftest':selftest()
    elif args.command=='build':build_suite(args.suite.resolve())
    else:exposure_audit(args.suite,args.jobs,args.prefix,args.output)

if __name__=='__main__':main()
