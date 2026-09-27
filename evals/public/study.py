"""Pinned public-source handoff study. Fetches corpora, isolates sessions, exports evidence."""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent/'suite'))
from build import build, write, CLI_VERSION
from collect import seconds
sys.path.insert(0, str(HERE))
from reader_verify import grade as reader_grade
# Import by file path: shared suite also has a module named verify.
import importlib.util
_spec = importlib.util.spec_from_file_location('public_verify', HERE/'verify.py')
_verify = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_verify)
CASES = json.loads((HERE/'cases.json').read_text())
ARMS = ['upstream', 'ordinary', 'skill']


def dump(path, value): write(path, json.dumps(value, indent=2)+'\n')
def sha(data): return hashlib.sha256(data).hexdigest()
def digest(files): return sha(json.dumps(files, sort_keys=True).encode())


def corpus(world):
    c = CASES[world]; path = ROOT/'.local'/('upstream-'+world)
    if not path.exists():
        subprocess.run(['git', 'clone', '--no-checkout', c['repository'], str(path)], check=True)
        subprocess.run(['git', 'checkout', '--detach', c['revision']], cwd=path, check=True)
    head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=path,text=True).strip()
    assert head == c['revision'], 'Wrong upstream revision; do not silently substitute a release.'
    assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=path), 'Modified upstream clone'
    names = subprocess.check_output(['git','ls-files','-z'],cwd=path).decode().split('\0')
    files = {}; excluded = []
    for name in filter(None, names):
        p = path/name; raw = p.read_bytes()
        if p.is_symlink(): excluded.append(dict(path=name,reason='symlink')); continue
        try: body = raw.decode('utf-8')
        except UnicodeDecodeError: excluded.append(dict(path=name,reason='non-UTF-8')); continue
        if '\0' in body: excluded.append(dict(path=name,reason='binary NUL')); continue
        assert '\r' not in body, 'Snapshot reader normalizes newlines; preserve bytes explicitly if needed.'
        files[name] = body
    assert not any(Path(p).name in ['AGENTS.md','AGENTS.override.md'] for p in files), 'Project instruction discovery needs explicit review.'
    return files, dict(repository=c['repository'], revision=head, release=c['release'],
        files_sha256={p:sha(s.encode()) for p,s in files.items()}, excluded=excluded,
        file_count=len(files), words=sum(len(s.split()) for s in files.values()),
        bytes=sum(len(s.encode()) for s in files.values()), license=files['LICENSE.txt'])


def frozen_sources():
    paths = list(HERE.glob('*.py')) + [HERE/'cases.json', HERE/'README.md'] + list((ROOT/'skills/context-docs').rglob('*'))
    paths += [HERE.parent/p for p in ['suite/build.py','suite/collect.py','suite/codex.toml','suite/audit_isolation.py','quality/reader_verify.py']]
    return {str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in paths if p.is_file()}


def reference_docs(world):
    rows = ['# Project handoff', '', 'Reference synthesis for the pinned public release; no deployment topology is known.', '']
    for q in CASES[world]['questions']:
        rows += ['## '+q['id'], '', ' '.join(q['required']), '', 'Sources: '+', '.join(f'[{p}]({p})' for p in q['sources']), '']
    return {'context.md':'\n'.join(rows)}


def answers(world):
    return [dict(id=q['id'],answer=' '.join(q['required']),sources=q['sources']) for q in CASES[world]['questions']]


def maint_prompt(world, arm):
    c = CASES[world]
    prompt = ('Work only in /workspace and /output, using the supplied pinned public repository. '
        'Do not contact external services or inspect harness files, /tests, /solution, /logs or credentials. '
        'Do not install dependencies or run upstream code/tests. Read code/tests/docs as evidence. '
        'Preserve every existing project file and Git state; add only new Markdown documents. '
        'No live deployment details are supplied. Complete autonomously.\n\n')
    if arm == 'skill': prompt += 'Use the context-docs skill at /opt/context-docs/SKILL.md and its relevant references.\n\n'
    return prompt + ('Create a concise, useful project handoff for a future contributor working on '+c['focus']+'. '
        'Inspect the relevant existing documentation, implementation and tests. Record the supported behavior, important constraints and version-specific pitfalls, '
        'with links to canonical evidence. Separate established facts from unknown deployment details; resolve inconsistent guidance using implementation/tests where appropriate. '
        'Choose a minimal layout that fits this repository, avoid duplicating the whole documentation, and review your additions for accuracy and valid links.\n')


def reader_prompt(world, variant):
    return ('Use only the supplied project in /workspace to answer for this checkout. Read its code, tests and documentation as needed. '
        'Do not edit project files or Git state. Do not install dependencies or run upstream code/tests. '
        'Do not contact external services or inspect harness files, /tests, /solution, /logs or credentials. '
        'Write /output/answers.json as a JSON array with exactly one object per question: '
        '{"id":"q1","answer":"your supported answer including material uncertainty","sources":["repository-relative/source/path"]}. '
        'Cite existing source paths without line numbers or fragments. Complete autonomously.\n\nQuestions:\n'+
        json.dumps([dict(id=q['id'],question=q['variants'][variant]) for q in CASES[world]['questions']],indent=2)+'\n')


def case(name, files, oracle):
    return dict(id=name,files=files,uncommitted={},protected=[],immutable=[],steps=[dict(request='',updates={},oracle=oracle,rubric=[])])


def finalize(destination, manifest, meta):
    manifest.update(public_sources=frozen_sources(), concurrency=3, timeout_sec=480,
        execution_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip())
    for p in manifest['packages']:
        p.update(meta[p['task']]); task=destination/p['name']
        write(task/'task.toml',(task/'task.toml').read_text().replace('timeout_sec = 240','timeout_sec = 480'))
        docker=task/'environment/Dockerfile'
        write(docker,docker.read_text().replace('Initial synthetic fixture','Pinned public source snapshot'))
    dump(destination.parent/(destination.name+'-manifest.json'),manifest)
    print(f'Built {len(manifest["packages"])} {manifest["kind"]} sessions.',flush=True)


def build_maint(destination):
    cases=[]; provenance={}; meta={}
    for w in CASES:
        files,provenance[w]=corpus(w)
        cases.append(case(w,files,reference_docs(w))); meta[w]=dict(world=w)
    manifest=build(destination,cases,{'ordinary':None,'skill':ROOT/'skills/context-docs'},attempts=1)
    manifest.update(kind='maintenance',upstream=provenance)
    for p in manifest['packages']:
        task=destination/p['name']
        write(task/'instruction.md',maint_prompt(p['task'],p['arm']))
        shutil.copy2(HERE/'verify.py',task/'tests/verify.py')
    finalize(destination,manifest,meta)


def build_readers(destination, maintenance):
    trials=json.loads((maintenance/'trials.json').read_text())
    assert len(trials)==4
    cases=[];meta={};snaps=[];provenance={}
    for w in CASES:
        original,provenance[w]=corpus(w)
        for arm in ARMS:
            if arm=='upstream': files=original
            else:
                t=next(t for t in trials if t['metadata']['world']==w and t['metadata']['arm']==arm)
                assert t['steps'][0]['observed'], 'Cannot invent missing artifacts'
                files=t['steps'][0]['observed']['files']
            sid=sha(f'{w}/{arm}'.encode())[:12]
            snaps.append(dict(id=sid,world=w,arm=arm,files_sha256=digest(files),files=files))
            for variant in range(2):
                name='read-'+sha(f'{sid}/{variant}'.encode())[:12]
                cases.append(case(name,files,{'@output/answers.json':json.dumps(answers(w),indent=2)+'\n'}))
                meta[name]=dict(world=w,arm=arm,variant=variant,snapshot_id=sid,files_sha256=digest(files))
    dump(maintenance/'snapshots.json',snaps)
    manifest=build(destination,cases,{'reader':None},attempts=1)
    manifest.update(kind='reader',upstream=provenance)
    for p in manifest['packages']:
        m=meta[p['task']]; task=destination/p['name']
        write(task/'instruction.md',reader_prompt(m['world'],m['variant']))
        files=next(c['files'] for c in cases if c['id']==p['task'])
        dump(task/'tests/spec.json',dict(before=files,ids=[q['id'] for q in CASES[m['world']]['questions']]))
        shutil.copy2(HERE/'reader_verify.py',task/'tests/verify.py')
        assert not (task/'environment/skill').exists()
    finalize(destination,manifest,meta)


def run(suite,jobs,prefix,mode):
    manifest=json.loads((suite.parent/(suite.name+'-manifest.json')).read_text()); jobs.mkdir(parents=True,exist_ok=True)
    name=f'{prefix}-{mode}-1'
    assert not (jobs/name).exists(), 'Preserve previous runs; do not retry silently'
    packages=manifest['packages']
    if mode!='model': packages=[next(p for p in packages if p['world']==w) for w in CASES]
    if manifest['kind']=='maintenance':
        packages=[p for i,w in enumerate(CASES) for arm in (['ordinary','skill'] if i%2==0 else ['skill','ordinary']) for p in packages if p['world']==w and p['arm']==arm]
    else: packages=sorted(packages,key=lambda p:p['name'])
    env=dict(os.environ)
    if mode=='model':
        auth=Path(env.get('CODEX_AUTH_JSON_PATH',str(Path(env.get('CODEX_HOME',str(Path.home()/'.codex')))/'auth.json')))
        assert auth.is_file(), 'Existing Codex login required'
        env['CODEX_AUTH_JSON_PATH']=str(auth.resolve())
        for key in ['OPENAI_API_KEY','CODEX_API_KEY','OPENAI_BASE_URL']: env.pop(key,None)
        agent=dict(name='codex',model_name='openai/gpt-6-astra',kwargs=dict(version=CLI_VERSION,reasoning_effort='low',web_search='disabled',config=str(HERE.parent/'suite/codex.toml')))
    else: agent=dict(name=mode)
    config=dict(job_name=name,jobs_dir=str(jobs.resolve()),agents=[agent],tasks=[dict(path=str((suite/p['name']).resolve())) for p in packages],n_attempts=1,n_concurrent_trials=3,retry=dict(max_retries=0))
    path=jobs/(name+'.json');dump(path,config)
    print(f'Starting {name}: {len(packages)} trials',flush=True)
    subprocess.run(['uv','tool','run','--from','harbor==0.23.0','harbor','run','--config',str(path)],env=env,check=True)
    result=json.loads((jobs/name/'result.json').read_text())
    if result['stats']['n_errored_trials']: raise SystemExit('Execution errors retained; inspect before proceeding.')
    if mode!='model':
        for p in (jobs/name).glob('*/result.json'):
            d=json.loads(p.read_text())
            assert (d['verifier_result']['rewards']['mechanical']==1)==(mode=='oracle'),(d['task_name'],mode)


def collect(suite,jobs,prefix,output):
    manifest=json.loads((suite.parent/(suite.name+'-manifest.json')).read_text()); packages={p['name']:p for p in manifest['packages']}; trials=[]
    for p in sorted((jobs/(prefix+'-model-1')).glob('*/result.json')):
        d=json.loads(p.read_text());meta=packages[d['task_name']]
        tid=sha((prefix+'/'+d['trial_name']).encode())[:12]
        op=p.parent/'verifier/observed.json';tp=p.parent/'agent/trajectory.json'
        trajectory=json.loads(tp.read_text()) if tp.exists() else {}
        calls=[dict(function_name=c['function_name'],arguments=c.get('arguments')) for e in trajectory.get('steps',[]) for c in e.get('tool_calls',[])]
        error=d.get('exception_info')
        step=dict(review_id=tid,observed=json.loads(op.read_text()) if op.exists() else None,execution_error=error.get('exception_type') if error else None,
            seconds=seconds(d.get('agent_execution')),tool_calls=calls,usage={k:(d.get('agent_result') or {}).get(k) for k in ['n_input_tokens','n_cache_tokens','n_output_tokens']})
        trials.append(dict(id=tid,metadata=meta,task_checksum=d['task_checksum'],steps=[step],agent_info=d.get('agent_info')))
    output.mkdir(parents=True,exist_ok=True);dump(output/'trials.json',trials)
    controls=[]
    for mode in ['oracle','nop']:
        for p in sorted((jobs/f'{prefix}-{mode}-1').glob('*/result.json')):
            d=json.loads(p.read_text()); controls.append(dict(task=d['task_name'],mode=mode,task_checksum=d['task_checksum'],error=(d.get('exception_info') or {}).get('exception_type'),rewards=d['verifier_result']['rewards']))
    dump(output/'controls.json',controls)
    print(f'Exported {len(trials)} trials')


def selftest():
    n=0
    for w in CASES:
        files,meta=corpus(w)
        for q in CASES[w]['questions']: assert all(p in files for p in q['sources'])
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'project';out=Path(tmp)/'output';root.mkdir();out.mkdir()
            for p,s in files.items(): write(root/p,s)
            assert not _verify.grade(files,root)['mechanical_pass'];n+=1
            for p,s in reference_docs(w).items(): write(root/p,s)
            assert _verify.grade(files,root)['mechanical_pass'];n+=1
            write(root/'context.md',reference_docs(w)['context.md']+'\n[bad](absent.md)\n')
            assert not _verify.grade(files,root)['mechanical_pass'];n+=1
            write(root/'context.md',reference_docs(w)['context.md'])
            write(root/'LICENSE.txt','modified')
            assert not _verify.grade(files,root)['mechanical_pass'];n+=1
            write(root/'LICENSE.txt',files['LICENSE.txt'])
            write(root/'extra.py','pass')
            assert not _verify.grade(files,root)['mechanical_pass'];n+=1
            (root/'extra.py').unlink()
            spec=dict(before=_verify.snapshot(root),ids=[q['id'] for q in CASES[w]['questions']])
            assert not reader_grade(spec,root,out)['mechanical_pass'];n+=1
            dump(out/'answers.json',answers(w));assert reader_grade(spec,root,out)['mechanical_pass'];n+=1
            bad=answers(w);bad[0]['sources']=['absent.md'];dump(out/'answers.json',bad)
            assert not reader_grade(spec,root,out)['mechanical_pass'];n+=1
            dump(out/'answers.json',answers(w));write(root/'context.md','unauthorized change')
            assert not reader_grade(spec,root,out)['mechanical_pass'];n+=1
        print(w,meta['file_count'],'files',meta['words'],'words',len(meta['excluded']),'omissions')
    print(n,'scope/schema/reference assertions passed; semantics require author review.')


def main():
    parser=argparse.ArgumentParser();sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('selftest')
    b=sub.add_parser('build-maint');b.add_argument('suite',type=Path)
    b=sub.add_parser('build-readers');b.add_argument('suite',type=Path);b.add_argument('maintenance',type=Path)
    r=sub.add_parser('run');r.add_argument('suite',type=Path);r.add_argument('jobs',type=Path);r.add_argument('--prefix',required=True);r.add_argument('--mode',choices=['oracle','nop','model'],required=True)
    e=sub.add_parser('collect');e.add_argument('suite',type=Path);e.add_argument('jobs',type=Path);e.add_argument('output',type=Path);e.add_argument('--prefix',required=True)
    a=parser.parse_args()
    if a.command=='selftest': selftest()
    elif a.command=='build-maint': build_maint(a.suite.resolve())
    elif a.command=='build-readers': build_readers(a.suite.resolve(),a.maintenance)
    elif a.command=='run': run(a.suite.resolve(),a.jobs,a.prefix,a.mode)
    else: collect(a.suite,a.jobs,a.prefix,a.output)

if __name__=='__main__': main()
