"""Four-pass public decision histories, followed by independent fresh reader sessions."""
import argparse, hashlib, importlib.util, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE.parent/'suite'))
from build import build,write,CLI_VERSION
from collect import seconds
from verify import grade,snapshot
from selftest import put
sys.path.insert(0,str(HERE.parent/'routing'))
from exposure import audit
CASES=json.loads((HERE/'cases.json').read_text()); ARMS=['unmaintained','ordinary','skill']

def dump(p,d):write(p,json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(d):return sha(json.dumps(d,sort_keys=True).encode())
def ledger(w,s):return CASES[w]['ledgers'][min(s,2)]
def sources():
    paths=list(HERE.rglob('*'))+list((ROOT/'skills/context-docs').rglob('*'))
    paths += [HERE.parent/p for p in ['suite/build.py','suite/verify.py','suite/collect.py','suite/codex.toml','suite/audit_isolation.py','quality/maintenance_verify.py','quality/reader_verify.py','routing/exposure.py']]
    return {str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in paths if p.is_file() and '__pycache__' not in p.parts}

def evidence(w,s):
    selected=CASES[w]['sources'][:min(s,2)+1];files={};lines=['Public policy history packet.', 'Scope: upstream policy snapshots only; no downstream service adoption or feature-specific exception approval evidence is supplied.', 'Treat each dated snapshot as historical. Latest supplied date is the evaluation cutoff, not today.', 'Source-internal conflicts should be identified; do not silently rewrite original evidence.','']
    for p in selected:
        b=(HERE/p['file']).read_bytes();assert sha(b)==p['sha256']
        name='evidence/'+Path(p['file']).name;files[name]=b.decode()
        lines += [p['date']+' '+name,p['url'],'SHA-256: '+p['sha256'],'']
    files['evidence/index.txt']='\n'.join(lines)+'\n';return files

def initial(w):return {'README.md':'# '+('Compatibility policy' if w=='compatibility' else 'Release policy')+' workspace\n\n[Historical evidence index](evidence/index.txt)\n\nThis workspace tracks the supplied upstream decision history.\n'}
def materialized(w,s):return {**initial(w),**evidence(w,s)}
def reference(w,s):
    lines=['# Policy context','','Current cutoff: '+CASES[w]['sources'][min(s,2)]['date']+'.','']
    for f in ledger(w,s):
        paths=f['sources'] or ['evidence/index.txt']
        lines += ['## '+f['id'],'',f['expected'],'','Sources: '+', '.join(f'[{p}]({p})' for p in paths),'']
    return {'README.md':initial(w)['README.md']+'\n[Current policy context](context.md)\n','context.md':'\n'.join(lines)}
def answers(w):
    fs={f['id']:f for f in ledger(w,2)}
    return [dict(id=q['id'],answer=' '.join(fs[k]['expected'] for k in q['items']),sources=list(dict.fromkeys(p for k in q['items'] for p in (fs[k]['sources'] or ['evidence/index.txt'])))) for q in CASES[w]['questions']]

def maint_prompt(w,s,arm):
    common=('Work only in /workspace and /output using the supplied historical public-policy evidence. Do not contact external services or inspect harness files, /tests, /solution, /logs or credentials. '
      'Do not change raw evidence, non-Markdown files or Git state. Preserve existing project files and unique information. No downstream runtime access is supplied. Complete autonomously.\n\n')
    if arm=='skill':common+='Use the context-docs skill at /opt/context-docs/SKILL.md and its relevant references.\n\n'
    task=('Establish' if s==0 else 'Update')+' concise, navigable Markdown project context for a future contributor. '
    if s==3:task='Review the maintained context with no new evidence; change documents only if needed for correctness or consistency. '
    return common+task+('Read the evidence index and source snapshots. Record current requirements, authority/status, rationale, exceptions and unknowns. '
      'Preserve significant earlier decisions and explain supersession instead of leaving old instructions operative. Identify internal source contradictions without guessing. '
      'Link the context from README and cite authoritative local evidence. Keep useful details through later updates; avoid copying entire sources or adding session diaries. '
      'Choose a layout that fits the project and check links and factual consistency. Focus on '+('compatibility scope, deprecation timing and notices, soft-deprecation semantics when specified, exception authority and historical changes.' if w=='compatibility' else 'release/support timing, historical changes and rejected alternatives, rationale, versioning non-goals and dependent governance rules.')+'\n')

def reader_prompt(w,v):
    return ('Use only /workspace at its latest supplied historical cutoff, not current outside knowledge. Begin with README.md and read every Markdown context document in full before writing answers; then consult the common raw evidence as needed. '
      'Do not edit project files or Git state. Do not contact external services or inspect harness files, /tests, /solution, /logs or credentials. '
      'Write /output/answers.json as an array of exactly one object per question: {"id":"q1","answer":"supported answer including material uncertainty","sources":["repository-relative/source/path"]}. '
      'Cite existing local paths without fragments or line numbers. Complete autonomously.\n\nQuestions:\n'+json.dumps([dict(id=q['id'],question=q['variants'][v]) for q in CASES[w]['questions']],indent=2)+'\n')

def finalize(dest,m):
    m.update(history_sources=sources(),execution_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),concurrency=3,timeout_sec=480)
    for p in m['packages']:
        t=dest/p['name'];write(t/'task.toml',(t/'task.toml').read_text().replace('timeout_sec = 240','timeout_sec = 480'))
        docker=t/'environment/Dockerfile';write(docker,docker.read_text().replace('Initial synthetic fixture','Public policy history workspace'))
    dump(dest.parent/(dest.name+'-manifest.json'),m)

def build_maint(dest):
    cases=[]
    for w in CASES:
        steps=[dict(request='',updates={} if s in [0,3] else evidence(w,s),oracle=reference(w,s),rubric=[]) for s in range(4)]
        cases.append(dict(id=w,files=materialized(w,0),uncommitted={},protected=[],immutable=[],steps=steps))
    m=build(dest,cases,{'ordinary':None,'skill':ROOT/'skills/context-docs'},attempts=1);m['kind']='maintenance'
    for p in m['packages']:
        p['world']=p['task']
        for s in range(4):
            t=dest/p['name']/'steps'/f'pass-{s+1}'
            write(t/'instruction.md',maint_prompt(p['world'],s,p['arm']))
            spec=json.loads((t/'tests/spec.json').read_text());spec['allow_noop']=s==3;dump(t/'tests/spec.json',spec)
            shutil.copy2(HERE.parent/'suite/verify.py',t/'tests/base_verify.py')
            shutil.copy2(HERE.parent/'quality/maintenance_verify.py',t/'tests/verify.py')
    finalize(dest,m)

def snapshots(export):
    ts=json.loads((export/'trials.json').read_text());assert len(ts)==4
    out=[]
    for w in CASES:
        for arm in ARMS:
            trial=next((t for t in ts if t['metadata']['world']==w and t['metadata']['arm']==arm),None)
            for s in range(4):
                files=materialized(w,s);ok=True;error=None
                if trial:
                    step=trial['steps'][s];obs=step['observed'];assert obs,'Missing artifact cannot be replaced'
                    expected=materialized(w,0) if s==0 else dict(trial['steps'][s-1]['observed']['files'])
                    if s in [1,2]:expected.update(evidence(w,s))
                    assert digest(expected)==obs['before_sha256'],'Actual continuity mismatch'
                    files=obs['files'];ok=obs['mechanical_pass'] and not step['execution_error'];error=step['execution_error']
                out.append(dict(id=sha(f'{w}/{arm}/{s}'.encode())[:12],world=w,arm=arm,stage=s,files=files,files_sha256=digest(files),mechanical_pass=ok,execution_error=error))
    return out

def build_readers(dest,export):
    snaps=snapshots(export);dump(export/'snapshots.json',snaps);cases=[];meta={}
    for s in snaps:
        if s['stage']!=3:continue
        for v in range(2):
            name='read-'+sha(f'{s["id"]}/{v}'.encode())[:12]
            cases.append(dict(id=name,files=s['files'],uncommitted={},protected=[],immutable=[],steps=[dict(request='',updates={},oracle={'@output/answers.json':json.dumps(answers(s['world']),indent=2)+'\n'},rubric=[])]))
            meta[name]=dict(world=s['world'],arm=s['arm'],variant=v,snapshot_id=s['id'],files_sha256=s['files_sha256'])
    m=build(dest,cases,{'reader':None},attempts=1);m['kind']='reader'
    for p in m['packages']:
        p.update(meta[p['task']]);t=dest/p['name']
        write(t/'instruction.md',reader_prompt(p['world'],p['variant']))
        files=next(c['files'] for c in cases if c['id']==p['task'])
        dump(t/'tests/spec.json',dict(before=files,ids=[q['id'] for q in CASES[p['world']]['questions']]))
        shutil.copy2(HERE.parent/'quality/reader_verify.py',t/'tests/verify.py')
        assert not (t/'environment/skill').exists()
    finalize(dest,m)

def run(suite,jobs,prefix,mode):
    m=json.loads((suite.parent/(suite.name+'-manifest.json')).read_text());jobs.mkdir(parents=True,exist_ok=True)
    name=prefix+'-'+mode+'-1';assert not (jobs/name).exists(),'Never overwrite or silently retry'
    ps=m['packages']
    if mode!='model':ps=[next(p for p in ps if p['world']==w and (m['kind']!='maintenance' or p['arm']=='ordinary')) for w in CASES]
    if m['kind']=='maintenance':ps=[p for i,w in enumerate(CASES) for a in (['ordinary','skill'] if i%2==0 else ['skill','ordinary']) for p in ps if p['world']==w and p['arm']==a]
    else:ps=sorted(ps,key=lambda p:p['name'])
    env=dict(os.environ)
    if mode=='model':
        auth=Path(env.get('CODEX_AUTH_JSON_PATH',str(Path(env.get('CODEX_HOME',str(Path.home()/'.codex')))/'auth.json')));assert auth.is_file()
        env['CODEX_AUTH_JSON_PATH']=str(auth.resolve())
        for k in ['OPENAI_API_KEY','CODEX_API_KEY','OPENAI_BASE_URL']:env.pop(k,None)
        agent=dict(name='codex',model_name='openai/gpt-6-astra',kwargs=dict(version=CLI_VERSION,reasoning_effort='low',web_search='disabled',config=str(HERE.parent/'suite/codex.toml')))
    else:agent=dict(name=mode)
    config=dict(job_name=name,jobs_dir=str(jobs.resolve()),agents=[agent],tasks=[dict(path=str((suite/p['name']).resolve())) for p in ps],n_attempts=1,n_concurrent_trials=3,retry=dict(max_retries=0))
    path=jobs/(name+'.json');dump(path,config);print(f'Starting {name}: {len(ps)} trials',flush=True)
    subprocess.run(['uv','tool','run','--from','harbor==0.23.0','harbor','run','--config',str(path)],env=env,check=True)
    result=json.loads((jobs/name/'result.json').read_text())
    if result['stats']['n_errored_trials']:raise SystemExit('Execution errors retained; inspect before proceeding.')
    if mode!='model':
        for p in (jobs/name).glob('*/result.json'):
            d=json.loads(p.read_text());ss=d.get('step_results') or [d]
            assert all(s['verifier_result']['rewards']['mechanical']==1 for s in ss)==(mode=='oracle')

def collect(suite,jobs,prefix,output):
    m=json.loads((suite.parent/(suite.name+'-manifest.json')).read_text());mapping={p['name']:p for p in m['packages']};ts=[];ex=[]
    for p in sorted((jobs/(prefix+'-model-1')).glob('*/result.json')):
        d=json.loads(p.read_text());meta=mapping[d['task_name']];tid=sha((prefix+'/'+d['trial_name']).encode())[:12];ss=[]
        for i,s in enumerate(d.get('step_results') or [d]):
            folder=p.parent/'steps'/s['step_name'] if 'step_name' in s else p.parent
            op=folder/'verifier/observed.json';obs=json.loads(op.read_text()) if op.exists() else None;error=s.get('exception_info') or d.get('exception_info')
            ss.append(dict(stage=i,observed=obs,execution_error=error.get('exception_type') if error else None,seconds=seconds(s.get('agent_execution')),usage={k:(s.get('agent_result') or {}).get(k) for k in ['n_input_tokens','n_cache_tokens','n_output_tokens']}))
        ts.append(dict(id=tid,metadata=meta,task_checksum=d['task_checksum'],steps=ss))
        if m['kind']=='reader':
            sessions=list((p.parent/'agent/sessions').rglob('*.jsonl'));assert len(sessions)==1
            files=json.loads((suite/meta['name']/'tests/spec.json').read_text())['before']
            docs={name:audit(sessions[0],files,name)['target'] for name in files if name.endswith('.md')}
            ex.append(dict(trial_id=tid,documents=docs,all_markdown_exposed=all(x['full_text_exposed'] for x in docs.values())))
    dump(output/'trials.json',ts)
    if ex:dump(output/'exposure.json',ex)
    controls=[]
    for mode in ['oracle','nop']:
        for p in sorted((jobs/(prefix+'-'+mode+'-1')).glob('*/result.json')):
            d=json.loads(p.read_text());controls.append(dict(task=d['task_name'],mode=mode,task_checksum=d['task_checksum'],error=(d.get('exception_info') or {}).get('exception_type'),stage_rewards=[s['verifier_result']['rewards'] for s in d.get('step_results') or [d]]))
    dump(output/'controls.json',controls);print(f'Exported {len(ts)} trials')

def selftest():
    from exposure import selftest as exposure_selftest
    exposure_selftest();count=0
    for w in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            r=Path(tmp)/'project';o=Path(tmp)/'output';r.mkdir();o.mkdir();put(r,materialized(w,0))
            for s in range(4):
                if s in [1,2]:put(r,evidence(w,s))
                before=snapshot(r);spec=dict(id=w,before=before,protected=[],immutable=[],allow_noop=s==3,entry='README.md')
                if s<3:assert not grade(spec,r,o,before)['mechanical_pass'];count+=1
                put(r,reference(w,s));assert grade(spec,r,o,before)['mechanical_pass'];count+=1
                path=r/next(p for p in before if p.endswith('.rst'));old=path.read_text();path.write_text(old+'unauthorized')
                assert not grade(spec,r,o,before)['mechanical_pass'];path.write_text(old);count+=1
            assert len(answers(w))==8 and all(a['sources'] for a in answers(w))
    print(f'{count} maintenance reference/no-op/source-preservation controls passed.')

if __name__=='__main__':
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True);sub.add_parser('selftest')
    b=sub.add_parser('build-maint');b.add_argument('suite',type=Path)
    b=sub.add_parser('build-readers');b.add_argument('suite',type=Path);b.add_argument('maintenance',type=Path)
    for command in ['run','collect']:
        r=sub.add_parser(command);r.add_argument('suite',type=Path);r.add_argument('jobs',type=Path);r.add_argument('--prefix',required=True)
        if command=='run':r.add_argument('--mode',choices=['oracle','nop','model'],required=True)
        else:r.add_argument('output',type=Path)
    a=p.parse_args()
    if a.command=='selftest':selftest()
    elif a.command=='build-maint':build_maint(a.suite.resolve())
    elif a.command=='build-readers':build_readers(a.suite.resolve(),a.maintenance)
    elif a.command=='run':run(a.suite,a.jobs,a.prefix,a.mode)
    else:collect(a.suite,a.jobs,a.prefix,a.output)
