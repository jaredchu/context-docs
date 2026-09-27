"""Isolated maintenance -> snapshot -> fresh-reader pipeline; no semantic auto-grading."""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'suite'))
from build import build,write,writer_script,CLI_VERSION
from collect import seconds
from verify import grade,snapshot
from selftest import put
from fixtures import CASES,WORLDS,ARMS,QUESTIONS,ledger,materialized,reference_docs
from reader_verify import grade as reader_grade


def dump(path,data):
    write(path,json.dumps(data,indent=2)+'\n')


def digest(data):
    return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()


def frozen_sources():
    paths=list(HERE.glob('*.py'))+[HERE/'README.md',HERE/'semantic-controls.json']+list((ROOT/'skills/context-docs').rglob('*'))+[HERE.parent/'suite'/p for p in ['build.py','verify.py','codex.toml']]
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}


def build_maint(destination):
    manifest=build(destination,CASES,{'ordinary':None,'skill':ROOT/'skills/context-docs'},attempts=1)
    manifest.update(kind='maintenance',execution_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),quality_sources=frozen_sources(),concurrency=3)
    for p in manifest['packages']:
        c=next(c for c in CASES if c['id']==p['task'])
        p.update(world=c['world'],condition=c['condition'])
        for stage in range(3):
            tests=destination/p['name']/'steps'/f'pass-{stage+1}'/'tests'
            shutil.copy2(HERE.parent/'suite/verify.py',tests/'base_verify.py')
            shutil.copy2(HERE/'maintenance_verify.py',tests/'verify.py')
    dump(destination.parent/(destination.name+'-manifest.json'),manifest)
    print(f'Built {len(manifest["packages"])} maintenance trials / 36 sessions.')


def run(suite,jobs,prefix,mode):
    manifest=json.loads((suite.parent/(suite.name+'-manifest.json')).read_text())
    jobs.mkdir(parents=True,exist_ok=True)
    name=f'{prefix}-{mode}-1'
    if (jobs/name).exists(): raise SystemExit('Job exists; preserve it and choose another prefix.')
    packages=manifest['packages']
    if mode!='model':
        if manifest['kind']=='maintenance': packages=[p for p in packages if p['arm']=='ordinary']
        else:
            packages=[next(p for p in packages if p['world']==w) for w in WORLDS]
    env=dict(os.environ)
    if mode=='model':
        auth=Path(env.get('CODEX_AUTH_JSON_PATH',str(Path(env.get('CODEX_HOME',str(Path.home()/'.codex')))/'auth.json')))
        if not auth.is_file(): raise SystemExit('Existing Codex login required.')
        env['CODEX_AUTH_JSON_PATH']=str(auth.resolve())
        for key in ['OPENAI_API_KEY','CODEX_API_KEY','OPENAI_BASE_URL']: env.pop(key,None)
        agent=dict(name='codex',model_name='openai/gpt-6-astra',kwargs=dict(version=CLI_VERSION,reasoning_effort='low',web_search='disabled',config=str(HERE.parent/'suite/codex.toml')))
    else: agent=dict(name=mode)
    # Adjacent matched arms, alternating order. Reader order is frozen by opaque id.
    if manifest['kind']=='maintenance':
        ordered=[]
        for i,c in enumerate(CASES):
            arms=['ordinary','skill'] if i%2==0 else ['skill','ordinary']
            ordered += [p for arm in arms for p in packages if p['task']==c['id'] and p['arm']==arm]
        packages=ordered
    else: packages=sorted(packages,key=lambda p:p['name'])
    config=dict(job_name=name,jobs_dir=str(jobs.resolve()),agents=[agent],tasks=[dict(path=str((suite/p['name']).resolve())) for p in packages],n_attempts=1,n_concurrent_trials=3,retry=dict(max_retries=0))
    path=jobs/(name+'.json');dump(path,config)
    print(f'Starting {name}: {len(packages)} trials',flush=True)
    subprocess.run(['uv','tool','run','--from','harbor==0.23.0','harbor','run','--config',str(path)],env=env,check=True)
    result=json.loads((jobs/name/'result.json').read_text())
    if result['stats']['n_errored_trials']: raise SystemExit('Infrastructure errors retained; inspect before proceeding.')
    if mode!='model':
        for p in (jobs/name).glob('*/result.json'):
            d=json.loads(p.read_text());steps=d.get('step_results') or [d]
            passed=all(s['verifier_result']['rewards']['mechanical']==1 for s in steps)
            assert passed==(mode=='oracle'),(d['task_name'],mode)


def export_trials(suite,jobs,prefix,output):
    manifest=json.loads((suite.parent/(suite.name+'-manifest.json')).read_text())
    packages={p['name']:p for p in manifest['packages']}
    trials=[]
    for p in sorted((jobs/(prefix+'-model-1')).glob('*/result.json')):
        d=json.loads(p.read_text());meta=packages[d['task_name']]
        tid=hashlib.sha256((prefix+'/'+d['trial_name']).encode()).hexdigest()[:12]
        steps=[]
        for i,s in enumerate(d.get('step_results') or [d]):
            folder=p.parent/'steps'/s['step_name'] if 'step_name' in s else p.parent
            op=folder/'verifier/observed.json'
            observed=json.loads(op.read_text()) if op.exists() else None
            tp=folder/'agent/trajectory.json'
            trajectory=json.loads(tp.read_text()) if tp.exists() else {}
            calls=[dict(function_name=c['function_name'],arguments=c.get('arguments')) for e in trajectory.get('steps',[]) for c in e.get('tool_calls',[])]
            error=s.get('exception_info') or d.get('exception_info')
            steps.append(dict(review_id=f'{tid}-{i+1}',stage=i,observed=observed,execution_error=error.get('exception_type') if error else None,seconds=seconds(s.get('agent_execution')),tool_calls=calls,usage={k:(s.get('agent_result') or {}).get(k) for k in ['n_input_tokens','n_cache_tokens','n_output_tokens']}))
        trials.append(dict(id=tid,metadata=meta,task_checksum=d['task_checksum'],steps=steps,agent_info=d.get('agent_info')))
    output.mkdir(parents=True,exist_ok=True)
    dump(output/'trials.json',trials)
    controls=[]
    for mode in ['oracle','nop']:
        for p in sorted((jobs/f'{prefix}-{mode}-1').glob('*/result.json')):
            d=json.loads(p.read_text())
            controls.append(dict(task=d['task_name'],mode=mode,task_checksum=d['task_checksum'],error=(d.get('exception_info') or {}).get('exception_type'),stage_rewards=[s['verifier_result']['rewards'] for s in d.get('step_results') or [d]]))
    dump(output/'controls.json',controls)
    print(f'Exported {len(trials)} {manifest["kind"]} trials.')
    return trials


def snapshots(maint_export):
    trials=json.loads((maint_export/'trials.json').read_text())
    assert len(trials)==12,'Need all maintenance trials; preserve failures rather than substituting reference outputs.'
    output=[]
    for c in CASES:
        for arm in ARMS:
            trial=next((t for t in trials if t['metadata']['task']==c['id'] and t['metadata']['arm']==arm),None)
            for stage in range(3):
                files=materialized(c,stage)
                error=None;mechanical=True
                if arm!='untreated':
                    assert trial and len(trial['steps'])==3
                    s=trial['steps'][stage];observed=s['observed'];error=s['execution_error']
                    if not observed: raise ValueError('Missing artifact: cannot fabricate a reader project.')
                    if stage:
                        assert observed['before_documents']==trial['steps'][stage-1]['observed']['documents'],'Snapshot continuity mismatch'
                    # Keep the complete actual artifact, including scope mistakes.
                    files=observed['files']
                    mechanical=observed['mechanical_pass'] and not error
                sid=hashlib.sha256(f'{c["id"]}/{arm}/{stage}'.encode()).hexdigest()[:12]
                output.append(dict(id=sid,case=c['id'],world=c['world'],condition=c['condition'],arm=arm,stage=stage,files=files,files_sha256=digest(files),mechanical_pass=mechanical,execution_error=error))
    return output


def reader_prompt(world,variant):
    questions=[dict(id=q[0],question=q[2+variant]) for q in QUESTIONS[world]]
    return ('Use only the supplied project in /workspace. Read project files as needed to answer the questions at the latest evidence cutoff present in the project. '
            'Do not edit project files or Git state. Do not contact external services or inspect harness files, /tests, /solution, /logs or credentials. '
            'Write /output/answers.json as a JSON array with exactly one object per question: {"id": "q1", "answer": "your supported answer, including material uncertainty", "sources": ["repository-relative/source/path"]}. '
            'Cite existing source file paths without line numbers or fragments; explain relevant evidence limits in the answer. No live access is supplied. Complete autonomously.\n\nQuestions:\n'+json.dumps(questions,indent=2)+'\n')


def reference_answers(world):
    facts={f['id']:f for f in ledger(world,2)}
    return [dict(id=q[0],answer=' '.join(facts[k]['expected'] for k in q[1]),sources=list(dict.fromkeys(p for k in q[1] for p in facts[k]['sources']))) for q in QUESTIONS[world]]


def build_readers(destination,maint_export):
    snaps=snapshots(maint_export)
    dump(maint_export/'snapshots.json',snaps)
    final=[s for s in snaps if s['stage']==2]
    reader_cases=[];meta={}
    for s in final:
        for variant in range(2):
            opaque=hashlib.sha256(f'{s["id"]}/{variant}'.encode()).hexdigest()[:12]
            name='read-'+opaque
            oracle={'@output/answers.json':json.dumps(reference_answers(s['world']),indent=2)+'\n'}
            reader_cases.append(dict(id=name,files=s['files'],uncommitted={},protected=[],immutable=[],steps=[dict(request='',updates={},oracle=oracle,rubric=[])]))
            meta[name]=dict(snapshot_id=s['id'],case=s['case'],world=s['world'],condition=s['condition'],arm=s['arm'],variant=variant,files_sha256=s['files_sha256'])
    manifest=build(destination,reader_cases,{'reader':None},attempts=1)
    manifest.update(kind='reader',quality_sources=frozen_sources(),concurrency=3)
    for p in manifest['packages']:
        m=meta[p['task']];p.update(m)
        task=destination/p['name']
        # Override the maintenance wrapper completely: no skill and no change request.
        write(task/'instruction.md',reader_prompt(m['world'],m['variant']))
        files=next(s['files'] for s in final if s['id']==m['snapshot_id'])
        dump(task/'tests/spec.json',dict(before=files,ids=[q[0] for q in QUESTIONS[m['world']]]))
        shutil.copy2(HERE/'reader_verify.py',task/'tests/verify.py')
        assert not (task/'environment/skill').exists()
    dump(destination.parent/(destination.name+'-manifest.json'),manifest)
    print(f'Built {len(manifest["packages"])} fresh-reader sessions over {len(final)} final snapshots.')


def selftest():
    n=0
    for c in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'project';out=Path(tmp)/'output';root.mkdir();out.mkdir()
            put(root,materialized(c,0))
            for stage,step in enumerate(c['steps']):
                put(root,step['updates']);before=snapshot(root)
                spec=dict(id=c['id'],before=before,protected=[],immutable=[],allow_noop=stage==2,entry='README.md')
                if stage<2:
                    assert not grade(spec,root,out,before)['mechanical_pass'];n+=1
                put(root,step['oracle']);assert grade(spec,root,out,before)['mechanical_pass'];n+=1
                saved=(root/'README.md').read_text();(root/'README.md').write_text(saved+'\n[broken](absent.md)\n')
                assert not grade(spec,root,out,before)['mechanical_pass'];n+=1
                (root/'README.md').write_text(saved)
            spec=dict(before=snapshot(root),ids=[q[0] for q in QUESTIONS[c['world']]])
            assert not reader_grade(spec,root,out)['mechanical_pass'];n+=1
            dump(out/'answers.json',reference_answers(c['world']))
            assert reader_grade(spec,root,out)['mechanical_pass'];n+=1
            p=root/'README.md';p.write_text(p.read_text()+'\nUnauthorized reader edit.\n')
            assert not reader_grade(spec,root,out)['mechanical_pass'];n+=1
    print(f'{n} scope/schema/reference assertions passed. Semantic controls are separately reviewed.')


def main():
    parser=argparse.ArgumentParser();sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('selftest')
    b=sub.add_parser('build-maint');b.add_argument('suite',type=Path)
    b=sub.add_parser('build-readers');b.add_argument('suite',type=Path);b.add_argument('maintenance',type=Path)
    r=sub.add_parser('run');r.add_argument('suite',type=Path);r.add_argument('jobs',type=Path);r.add_argument('--prefix',required=True);r.add_argument('--mode',choices=['oracle','nop','model'],required=True)
    e=sub.add_parser('collect');e.add_argument('suite',type=Path);e.add_argument('jobs',type=Path);e.add_argument('output',type=Path);e.add_argument('--prefix',required=True)
    args=parser.parse_args()
    if args.command=='selftest': selftest()
    elif args.command=='build-maint': build_maint(args.suite.resolve())
    elif args.command=='build-readers': build_readers(args.suite.resolve(),args.maintenance)
    elif args.command=='run': run(args.suite.resolve(),args.jobs,args.prefix,args.mode)
    else: export_trials(args.suite,args.jobs,args.prefix,args.output)


if __name__=='__main__': main()
