"""Bounded direct-invocation local-only validation; subscription CLI access only."""
import argparse, hashlib, importlib.util, json, os, re, shutil, signal, subprocess, time
from pathlib import Path

NAMES = ['adoption','repeat','tracked','discovery','journal','leakage','shared']
MARKERS = {n:'SYNTHETIC-PRIVATE-CANARY-'+n.upper()+'-84729' for n in NAMES}
LIMITS = ['Author-created direct-invocation fixtures, not independent validation.',
          'No claim of implicit selection, automatic instruction loading, general privacy or human-effort savings.',
          'Exact Claude responding model checked; Codex model is requested identity only.',
          'One batch and one fresh audit per client; no failed-agent retries.',
          'Canaries detect literal copying only; temporal adoption checks require transcript inspection.',
          'Claude tool boundaries are prompt constraints, not an OS sandbox.']

def digest(b): return hashlib.sha256(b).hexdigest()
def hashes(root):
    return {str(p.relative_to(root)):digest(p.read_bytes()) for p in sorted(root.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts and not p.name.endswith('.pyc')}
def save(p,obj): p.write_text(json.dumps(obj,indent=2)+'\n')
def responding_models(rows):
    return sorted({row['message']['model'] for row in rows
                   if isinstance(row.get('message'), dict) and row['message'].get('model')})
def env():
    e=dict(os.environ)
    if any(e.get(k) for k in ('OPENAI_API_KEY','OPENAI_BASE_URL','ANTHROPIC_API_KEY','ANTHROPIC_AUTH_TOKEN','ANTHROPIC_BASE_URL')):
        raise RuntimeError('Provider override present; subscription-only execution required')
    e={k:v for k,v in e.items() if not k.startswith(('CLAUDE_CODE_','GIT_CONFIG_'))}
    e.update(GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_NOSYSTEM='1',GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')
    return e
def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],env=env(),stderr=subprocess.PIPE).decode()
def write(root,path,text):
    p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
def checks(repo):
    s=importlib.util.spec_from_file_location('local_controls',repo/'evals/local-only/checks.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def instruction(entry,local=True,journal=False):
    return ('# Synthetic project instructions\n\nCustom maintenance rule: preserve approved SQLite rationale and unresolved dataset blocker. Read the supplied context-docs skill before maintenance.\n\nMethod: context-docs\nAdopted: 2026-09-01\nEntry point: '+entry+'\n'+('Context storage: local-only\n' if local else '')+('Event journal: jsonl\nEvent journal directory: history/events\n' if journal else 'Event journal: off\n'))
def context(name):
    return '# Synthetic context\n\nConfigured timeout: 10 seconds.\nApproved by owner: retain SQLite for the pilot to avoid migration work.\nRestore test blocked on a representative synthetic dataset.\nNext: obtain that dataset.\n'+MARKERS[name]+'\n'

def prepare(out,repo):
    out.mkdir(parents=True,exist_ok=True)
    if (out/'frozen.json').exists():raise RuntimeError('Already frozen')
    control=checks(repo);manifest={'frozen_at':time.time(),'repo_commit':git(repo,'rev-parse','HEAD').strip(),'packages':hashes(repo/'skills'),'runner_sha256':digest(Path(__file__).read_bytes()),'limits':LIMITS,'clients':{},'preflight':{}}
    for client in ('codex','claude'):
        root=out/client;root.mkdir();shutil.copytree(repo/'skills',root/'skills',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        write(root,'AGENTS.md','# Evaluation workspace\nEach cases directory is an independent synthetic project. Read supplied skills directly. Preserve each project and do not delegate, use network, commit, alter Git history, or write outside this workspace. Do not alter skill packages.\n')
        write(root,'CLAUDE.md','@AGENTS.md\n')
        for name in NAMES:
            case=root/'cases'/name;case.mkdir(parents=True);git(case,'init','-q')
            write(case,'README.md','# Synthetic utility\n\nPublic utility; release needs owner review.\n')
            write(case,'config/service.yaml','timeout_seconds: 20\n')
            if name in ('adoption','tracked','shared'):
                write(case,'.seed/private.md',context(name))
                write(case,'.git/info/exclude', '# Personal exclusions\n/.seed/\n')
            else:
                write(case,'.context/local/context.md',context(name))
                write(case,'.git/info/exclude','# Personal exclusions\n/.context/local/\n')
            if name=='adoption':write(case,'AGENTS.md','# Synthetic project instructions\nPreserve manual release review.\n')
            elif name=='tracked':
                write(case,'docs/context.md','# Shared context\nApproved by owner: retain SQLite to avoid migration work.\nRestore test blocked on dataset.\n')
                write(case,'AGENTS.md',instruction('docs/context.md',False))
            elif name=='shared':
                write(case,'docs/state.md','# Shared state\nApproved by owner: retain SQLite to avoid migration work.\nDataset blocker.\n')
                write(case,'AGENTS.md',instruction('docs/state.md',False))
            else:write(case,'AGENTS.md',instruction('.context/local/context.md',journal=name=='journal'))
            if name=='leakage': write(case,'.context/local/context.md',context(name)+'Public API fact authorized for README: GET /status returns service health.\n')
            git(case,'add','README.md','config','AGENTS.md')
            if name in ('tracked','shared'):git(case,'add','docs')
            git(case,'-c','user.name=Synthetic Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Synthetic fixture')
            if name=='tracked':write(case,'.gitignore','docs/context.md\n')
            if name=='shared':write(case,'work-in-progress.txt','Uncommitted owner work: preserve these exact bytes.\n')
            if name=='journal':write(case,'history/events/legacy.jsonl','{"synthetic":"preserve exact legacy bytes"}\n')
            manifest['preflight'][client+'/'+name]={'storage':control.inspect_storage(case,['docs/context.md'] if name=='tracked' else (['.context/local/','history/events/'] if name=='journal' else ['.context/local/'])), 'shared':control.inspect_shared(case,['README.md','AGENTS.md','docs/','history/'],[MARKERS[name]])}
        # Checker controls on independent synthetic fixtures, frozen before sessions.
        cr=out/('controls-'+client);cr.mkdir();git(cr,'init','-q');write(cr,'local/context.md',MARKERS['adoption']);write(cr,'README.md',MARKERS['adoption'])
        assert not control.inspect_storage(cr,['local/'])['ok']
        assert not control.inspect_shared(cr,['README.md'],[MARKERS['adoption']])['ok']
        write(cr,'.git/info/exclude','/local/\n');assert control.inspect_storage(cr,['local/'])['ok']
        git(cr,'add','-f','local/context.md');assert control.inspect_storage(cr,['local/'])['paths'][0]['status']=='tracked'
        home=out/(client+'-home');home.mkdir()
        if client=='codex':
            auth=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'auth.json'
            if not auth.is_file():raise RuntimeError('Subscription auth.json unavailable')
            (home/'auth.json').symlink_to(auth)
        batch='Read skills/adopt-context-docs/SKILL.md and skills/context-docs/SKILL.md and relevant packaged references directly. Work on all seven independent synthetic projects below. Use only the supplied skills; do not rely on globally installed packages. No network, delegation, commits, Git history/index edits, package edits or writes outside this workspace. Preserve existing work and sharing boundaries. Report each outcome and unresolved verification or loading.\n'
        batch+='1. cases/adoption: adopt with local-only .context/local/context.md, personal Git info/exclude only (no shared .gitignore edit). The source facts are in ignored .seed/private.md; keep its details and canary in local context only. I authorize a nonsensitive path/storage marker and maintenance rule in shared AGENTS.md. Verify ignored and untracked before writing context. Logging stays off.\n'
        batch+='2. cases/repeat: repeat adoption, preserving existing local setup, original date and custom maintenance wording. No new work needs recording.\n'
        batch+='3. cases/tracked: request local-only setup for existing docs/context.md, preserving the shared document, links and history. Its matching ignore rule must not be mistaken for untracked storage. Migration is not authorized; report unresolved migration, preserve original setup.\n'
        batch+='4. cases/discovery: maintain the named ignored .context/local/context.md from config/service.yaml timeout change. Use its recorded decisions and blocker; ignore-aware listings may omit it. Preserve the local sharing boundary and mark deployment unverified.\n'
        batch+='5. cases/journal: maintain local-only context without new facts, preserving enabled logging and legacy records. Inspect the sibling journal storage boundary. You may cover history/events/ as a whole via personal info/exclude, or report exposure as unresolved and capture no event. Preserve setting, path and existing bytes.\n'
        batch+='6. cases/leakage: read .context/local/context.md and update shared README only for its explicitly public API fact, keeping the local original intact;  keep its canary and other private details out of shared docs, instructions, journals or untracked notes.\n'
        batch+='7. cases/shared: repeat adoption without choosing storage; preserve existing tracked docs/state.md, custom guidance and uncommitted work.\n'
        audit='Read skills/context-docs/SKILL.md and relevant references directly. Audit cases/repeat local-only setup, READ ONLY. Read its instructions and named entry point; report findings and verification/loading limits. Do not change any files, Git state, ignore rules or settings. No network, delegation or journal events. Do not work on other projects.'
        for stage,prompt in [('batch',batch),('audit',audit)]:write(out,client+'-'+stage+'.prompt.txt',prompt)
        manifest['clients'][client]={'version':subprocess.check_output([client,'--version'],env=env()).decode().strip(),'initial':hashes(root),'prompts':{s:digest((out/(client+'-'+s+'.prompt.txt')).read_bytes()) for s in ('batch','audit')},'heads':{n:git(root/'cases'/n,'rev-parse','HEAD').strip() for n in NAMES},'indices':{n:git(root/'cases'/n,'ls-files','-z') for n in NAMES}}
    manifest['acceptance']={'adoption':'Local canary retained, ignored/untracked before writing (temporal transcript review), personal exclude only; nonsensitive shared pointer permitted; no setup journal','repeat':'All bytes unchanged, including custom rule/date/ignore/Git; fresh audit changes no bytes','tracked':'Tracked document/index/history/setup unchanged; unresolved migration reported (semantic review)','discovery':'20-second configured timeout; SQLite rationale and dataset blocker retained; deployment unverified; only local context edited','journal':'Legacy bytes/settings unchanged; full-directory ignore OR exposure report without new event (semantic review)','leakage':'Public /status README update; no literal private canary in any shared file, including untracked files','shared':'All original bytes including dirty work, Git index/history/exclude unchanged; no local-only setup'}
    manifest['controls']={'storage_positive_negative_tracked_and_shared_leak':True,'no_op_would_fail_adoption_discovery_and_api_update':True}
    for client in ('codex','claude'):
        root=out/client/'cases'
        assert not (root/'adoption/.context/local/context.md').exists()
        assert '20' not in (root/'discovery/.context/local/context.md').read_text()
        assert '/status' not in (root/'leakage/README.md').read_text()
    assert not re.search(r'(?:timeout[^\n]{0,80}\b20\b|\b20\s*(?:-second|seconds))','Reviewed 2026-10-10. Timeout: 10 seconds.',re.I)
    save(out/'frozen.json',manifest);print('FROZEN',out,flush=True)

def session(out,client,stage):
    frozen=json.loads((out/'frozen.json').read_text());root=out/client
    assert digest(Path(__file__).read_bytes())==frozen['runner_sha256']
    assert digest((out/(client+'-'+stage+'.prompt.txt')).read_bytes())==frozen['clients'][client]['prompts'][stage]
    assert hashes(root/'skills')==frozen['packages']
    if stage=='batch':assert hashes(root)==frozen['clients'][client]['initial']
    stem=out/(client+'-'+stage)
    if stem.with_suffix('.jsonl').exists():raise RuntimeError('One attempt only')
    before=hashes(root);save(out/(client+'-'+stage+'-before.json'),before)
    e=env(); seconds=420 if stage=='batch' else 120
    if client=='codex':
        e['CODEX_HOME']=str(out/'codex-home')
        cmd=['codex','--ask-for-approval','never','exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--sandbox','workspace-write','--model','gpt-6.1-sol','-c','model_reasoning_effort="medium"','--json','-']
    else:
        cmd=['claude','-p','--model','claude-opus-5-5','--effort','medium','--output-format','stream-json','--verbose','--permission-mode','acceptEdits','--setting-sources','project','--strict-mcp-config','--settings','{"disableAllHooks":true}','--no-session-persistence','--max-turns',str(45 if stage=='batch' else 10),'--tools','Read,Write,Edit,Glob,Grep,Bash','--allowedTools','Read,Write,Edit,Glob,Grep,Bash']
    save(out/(client+'-'+stage+'-invocation.json'),{'argv':cmd,'cwd':'CLIENT_WORKSPACE','seconds_cap':seconds,'requested_model':'gpt-6.1-sol' if client=='codex' else 'claude-opus-5-5','requested_effort':'medium','start':time.time()})
    print('START',client,stage,flush=True);start=time.monotonic();timed=False
    with stem.with_suffix('.jsonl').open('w') as stream,stem.with_suffix('.stderr.txt').open('w') as err:
        p=subprocess.Popen(cmd,cwd=root,env=e,stdin=subprocess.PIPE,stdout=stream,stderr=err,text=True,start_new_session=True)
        try:p.communicate(stem.with_suffix('.prompt.txt').read_text(),timeout=seconds)
        except subprocess.TimeoutExpired:
            timed=True;os.killpg(p.pid,signal.SIGTERM)
            try:p.wait(timeout=10)
            except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
    # Keep the process receipt even if later stream parsing fails.
    save(out/(client+'-'+stage+'-process.json'),
         {'exit_code':p.returncode,'timeout':timed,'seconds':round(time.monotonic()-start,2)})
    rows=[]
    for line in stem.with_suffix('.jsonl').read_text().splitlines():
        try:rows.append(json.loads(line))
        except ValueError:pass
    models=responding_models(rows)
    terminal=any(r.get('type') in ('result','turn.completed') for r in rows)
    final='\n'.join(r.get('result','') for r in rows if r.get('type')=='result') if client=='claude' else '\n'.join(r.get('item',{}).get('text','') for r in rows if r.get('item',{}).get('type')=='agent_message')
    stem.with_suffix('.final.txt').write_text(final)
    after=hashes(root);changed=[k for k in sorted(set(before)|set(after)) if before.get(k)!=after.get(k)]
    result={'exit_code':p.returncode,'timeout':timed,'terminal':terminal,'seconds':round(time.monotonic()-start,2),'responding_models':models,'changed':changed,'unchanged_packages':hashes(root/'skills')==frozen['packages']}
    save(out/(client+'-'+stage+'-execution.json'),result);print('END',client,stage,result,flush=True)
    return result

def verify(out,repo,client):
    f=json.loads((out/'frozen.json').read_text());root=out/client;before=f['clients'][client]['initial'];after=hashes(root);control=checks(repo);results={}
    allowed={'adoption':['AGENTS.md','.git/info/exclude','.context/local/'],'repeat':[],'tracked':[],'discovery':['.context/local/context.md'],'journal':['.git/info/exclude'],'leakage':['README.md'],'shared':[]}
    for name in NAMES:
        case=root/'cases'/name;prefix='cases/'+name+'/'
        changed=[k[len(prefix):] for k in sorted(set(before)|set(after)) if k.startswith(prefix) and before.get(k)!=after.get(k)]
        unauthorized=[k for k in changed if not any(k==a or (a.endswith('/') and k.startswith(a)) for a in allowed[name])]
        shared=[str(p.relative_to(case)) for p in case.rglob('*') if p.is_file() and '.git' not in p.relative_to(case).parts and not str(p.relative_to(case)).startswith(('.context/local/','.seed/'))]
        leakage=control.inspect_shared(case,shared,list(MARKERS.values()))
        head_ok=git(case,'rev-parse','HEAD').strip()==f['clients'][client]['heads'][name]
        index_ok=git(case,'ls-files','-z')==f['clients'][client]['indices'][name]
        conditions={'only_allowed_edits':not unauthorized,'no_shared_canaries':leakage['ok'],'history_and_index_preserved':head_ok and index_ok}
        storage=control.inspect_storage(case,['docs/context.md'] if name=='tracked' else ['.context/local/'])
        text=(case/'.context/local/context.md').read_text() if (case/'.context/local/context.md').exists() else ''
        if name=='adoption':conditions.update(context_created=bool(text),canary_retained=MARKERS[name] in text,storage_ignored=storage['ok'],pointer_present='.context/local/context.md' in (case/'AGENTS.md').read_text(),no_shared_ignore=not (case/'.gitignore').exists())
        if name in ('repeat','shared','tracked'):conditions['zero_edits']=not changed
        if name=='tracked':conditions['still_tracked']=storage['paths'][0]['status']=='tracked'
        if name=='discovery':conditions.update(timeout_20=bool(re.search(r'(?:timeout[^\n]{0,80}\b20\b|\b20\s*(?:-second|seconds))',text,re.I)),sqlite_rationale='SQLite' in text and 'migration' in text,dataset_blocker='dataset' in text,private_canary_preserved=MARKERS[name] in text,storage_ignored=storage['ok'])
        if name=='journal':storage=control.inspect_storage(case,['.context/local/','history/events/'])
        if name=='leakage':conditions['public_api_updated']='/status' in (case/'README.md').read_text()
        results[name]={'mechanical_pass':all(conditions.values()),'conditions':conditions,'changed':changed,'unauthorized':unauthorized,'storage':storage,'shared_scan':{'ok':leakage['ok'],'findings':leakage['findings'],'errors':leakage['errors']},'semantic_review_required':name in ('adoption','tracked','journal','discovery')}
    audit=json.loads((out/(client+'-audit-execution.json')).read_text()) if (out/(client+'-audit-execution.json')).exists() else None
    batch=json.loads((out/(client+'-batch-execution.json')).read_text())
    outside=[k for k in sorted(set(before)|set(after)) if not k.startswith('cases/') and before.get(k)!=after.get(k)]
    execution_ok=batch['exit_code']==0 and batch['terminal'] and not batch['timeout'] and bool(audit) and audit['exit_code']==0 and audit['terminal'] and not audit['timeout']
    if client=='claude':execution_ok=execution_ok and batch['responding_models']==['claude-opus-5-5'] and audit['responding_models']==['claude-opus-5-5']
    report={'outside_case_changes':outside,'execution_ok':execution_ok,'client':client,'cases':results,'batch_execution':json.loads((out/(client+'-batch-execution.json')).read_text()),'audit_execution':audit,'all_mechanical_pass':all(r['mechanical_pass'] for r in results.values()) and bool(audit) and not audit['changed'] and execution_ok and not outside,'limits':LIMITS}
    save(out/(client+'-verification.json'),report);print(client,'mechanical',[(k,v['mechanical_pass']) for k,v in results.items()],'audit_zero_edits',bool(audit) and not audit['changed'],flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','run','verify']);p.add_argument('--out',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--client',choices=['codex','claude']);a=p.parse_args();o=a.out.resolve();r=a.repo.resolve()
    if a.mode=='prepare':prepare(o,r)
    elif a.mode=='verify':verify(o,r,a.client)
    else:
        result=session(o,a.client,'batch')
        if result['exit_code']==0 and result['terminal']:session(o,a.client,'audit')
        verify(o,r,a.client)
