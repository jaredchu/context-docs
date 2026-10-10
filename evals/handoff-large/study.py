"""Build, freeze, run and collect one larger matched pair. No historical mutations."""
import argparse
import difflib
import hashlib
import json
import shlex
import shutil
import subprocess
import sys
from datetime import datetime,timezone
from pathlib import Path
from session import launch

ROOT=Path(__file__).resolve().parents[2]
BUDGET=dict(reads=16,bytes=16000,searches=6)
CONTROL_SCRIPTS={'hook.py':Path(__file__).with_name('hook.py'),
                 'guard_hook.py':ROOT/'evals/claude-code/guard_hook.py'}
CONTROL_FILES=(*CONTROL_SCRIPTS, 'scattered.config.json', 'scattered.settings.json',
               'curated.config.json', 'curated.settings.json')

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def dump(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def snapshot(path):return {str(p.relative_to(path)):p.read_text() for p in sorted(path.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
def initialize_controls(root):
    control=root/'control'
    control.mkdir(exist_ok=True)
    for name,source in CONTROL_SCRIPTS.items():
        target=control/name
        if target.exists():
            if sha(target)!=sha(source):
                raise ValueError(f'Existing control script differs from source: {target}')
        else:
            shutil.copyfile(source,target)

def config(root,name,project,writable,budget=None):
    control=root/'control'
    body=dict(project=str(project),events=str(control/(name+'.events.jsonl')),writable=writable,budget=budget)
    c=control/(name+'.config.json');dump(c,body)
    command=shlex.join([sys.executable,str(control/'hook.py'),str(c)])+' || exit 2'
    settings=dict(autoMemoryEnabled=False,hooks={n:[dict(hooks=[dict(type='command',command=command,timeout=10)])] for n in ('InstructionsLoaded','PreToolUse','PostToolUse','PostToolUseFailure')})
    p=control/(name+'.settings.json');dump(p,settings);return p

def freeze(root):
    assert not (root/'protocol.json').exists(),'Freeze once after coordinator preflight.'
    fixture=json.loads((root/'fixture.json').read_text())
    assert set(fixture)=={'common','curated','task','criteria','writable'}
    assert all(n in fixture['common'] for n in fixture['writable'])
    assert json.loads((root/'preflight.json').read_text())['accepted']
    initialize_controls(root)
    common=dict(fixture['common'])
    topics=['dashboard colors','documentation examples','UI margins','keyboard hints','sample filenames','release illustration']
    for i in range(36):
        topic=topics[i%len(topics)]
        paragraph=(f'Workshop note {i+1}: discussion of {topic}. This review concerns presentation examples only. Participants examined wording, spacing and sample labels for future documentation. No request to change queue selection or processing behavior was made. The current examples remain readable while visual polish is deferred. No owner decision, exporter compatibility evidence or production rollout was recorded here. ')
        common[f'notes/workshops/session-{i+1:02d}.md']='# Workshop notes\n\n'+paragraph*3+'\n'
    neutral=fixture['task']+'\n\nFrozen retrieval budget: at most 16 Read calls and 16000 UTF-8 file bytes total, plus 6 Glob/Grep calls. Every Read must load a complete file (no offset/limit/pages); repeated reads consume the budget again. Grep returns filenames only. Code, tests and documentation all count; Write/Edit do not. Tools are Read, Write, Edit, Glob, Grep only. Skills, Bash, network, delegation and external services are unavailable. Do not execute code or claim tests ran; provide tests for the coordinator to execute after your session. Edit only '+', '.join(fixture['writable'])+'. Do not change notes, README, settings or protected code, commit or publish. Final answer must identify owner authority and rationale in your own words, the superseded proposal, remaining blocker and next action, changes, supporting evidence and verification limits. Seven-minute bound; no correction or retry.'
    protocol=dict(kind='fresh-handoff-large-v1',frozen_at=datetime.now(timezone.utc).isoformat(),model='claude-opus-5-5',requested_effort='high',effort_observed=False,cli_version=subprocess.check_output(['claude','--version'],text=True).strip(),budget=BUDGET,budget_definition='Full UTF-8 bytes charged before Read is admitted; repeated and unsuccessful admitted reads count. Search is filenames only and consumes one metadata call. No subject code execution. File bytes are not model tokens or actual rendered output size.',agent_seconds_cap=1200,allocation=dict(author=180,curated=420,scattered=420,review=180),order=['scattered','curated'],attempts=1,criteria=fixture['criteria'],writable=fixture['writable'],fixtures={},prompts={},harness_hashes={},control_hashes={},preflight_sha256=sha(root/'preflight.json'),fixture_author_sha256=sha(root/'fixture.json'),verifier_sha256=sha(root/'verify.py'),limits=['One author-created fixture, one fixed-order pair, no blinding or statistical significance.','Curated context+explicit routing; skills disabled in both, not a skill-activation or maintenance test.','No actual human correction interventions; code and report correction needs are reviewer estimates.','Budget prevents file-tool bypass by excluding subject execution, not an OS sandbox guarantee.','Exact coordinator model not independently exposed; Opus exact responding identity checked.','High effort requested, not independently observed.','Metadata call budget separately bounds filenames but does not charge filename-result bytes.'])
    for arm in protocol['order']:
        files=dict(common)
        if arm=='curated':
            files.update(fixture['curated'])
            files['README.md']+='\nContext entry point: [project context](docs/project-context.md).\n'
        project=root/'projects'/arm;project.mkdir(parents=True)
        for name,body in files.items():
            p=project/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body)
        protocol['fixtures'][arm]=files
        protocol['prompts'][arm]=('Read docs/project-context.md first and follow relevant sources as needed.\n\n' if arm=='curated' else '')+neutral
        config(root,arm,project,fixture['writable'],BUDGET)
    sources=[*Path(__file__).parent.glob('*.py'),ROOT/'evals/claude-code/smoke.py',ROOT/'evals/claude-code/guard_hook.py']
    protocol['harness_hashes']={str(p.relative_to(ROOT)):sha(p) for p in sources}
    protocol['control_hashes']={name:sha(root/'control'/name) for name in CONTROL_FILES}
    dump(root/'protocol.json',protocol);(root/'protocol.sha256').write_text(sha(root/'protocol.json')+'\n')
    print('Frozen '+sha(root/'protocol.json'))

def validate(root):
    p=json.loads((root/'protocol.json').read_text())
    assert sha(root/'protocol.json')==(root/'protocol.sha256').read_text().strip()
    assert all(sha(ROOT/n)==h for n,h in p['harness_hashes'].items())
    assert set(CONTROL_FILES)<=p['control_hashes'].keys(),'Missing frozen controls.'
    assert all(sha(root/'control'/n)==h for n,h in p['control_hashes'].items())
    assert sha(root/'verify.py')==p['verifier_sha256']
    assert sha(root/'preflight.json')==p['preflight_sha256']
    assert subprocess.check_output(['claude','--version'],text=True).strip()==p['cli_version']
    return p

def run(root):
    p=validate(root); assert not (root/'trials.json').exists(),'One attempt per condition.'
    for arm in p['order']:assert snapshot(root/'projects'/arm)==p['fixtures'][arm]
    author=json.loads((root/'author-execution.json').read_text());assert author['responding_models']==[p['model']]
    assert (author['exit_code']==0 and author['result_received']) or (author['exit_code']==124 and json.loads((root/'preflight.json').read_text()).get('preparation_timeout_retained'))
    logs=root/'logs';logs.mkdir(exist_ok=True);trials=[]
    for arm in p['order']:
        validate(root);project=root/'projects'/arm;before=p['fixtures'][arm]
        print('Starting '+arm,flush=True)
        result=launch(project,p['prompts'][arm],logs/(arm+'.jsonl'),root/'control'/(arm+'.settings.json'),420)
        events_path=root/'control'/(arm+'.events.jsonl')
        events=[json.loads(line) for line in events_path.read_text().splitlines()] if events_path.exists() else []
        calls=[e for e in events if e.get('hook_event_name')=='PreToolUse']
        admitted=[e for e in calls if e.get('decision')=='allow']
        after=snapshot(project)
        result.update(id=arm,after=after,changed_files=[n for n in sorted(before.keys()|after.keys()) if before.get(n)!=after.get(n)],protected_unchanged=all(after.get(n)==body for n,body in before.items() if n not in p['writable']),denied_calls=[e for e in calls if e.get('decision')=='deny'],tool_calls=len(calls),reads=sum(e.get('tool_name')=='Read' for e in admitted),retrieval_bytes=sum(e.get('retrieval_bytes',0) for e in admitted),searches=sum(e.get('tool_name') in ('Glob','Grep') for e in admitted),external_instructions=[e for e in events if e.get('hook_event_name')=='InstructionsLoaded' and not Path(e['file_path']).resolve().is_relative_to(project)])
        result['execution_valid']=result['exit_code']==0 and result['result_received'] and result['responding_models']==[p['model']] and not result['external_instructions'] and result['protected_unchanged'] and all(n in p['writable'] for n in result['changed_files']) and result['reads']<=BUDGET['reads'] and result['retrieval_bytes']<=BUDGET['bytes'] and result['searches']<=BUDGET['searches']
        patch=''.join(''.join(difflib.unified_diff(before.get(n,'').splitlines(True),after.get(n,'').splitlines(True),fromfile='before/'+n,tofile='after/'+n)) for n in result['changed_files'])
        (root/(arm+'.patch')).write_text(patch);trials.append(result);dump(root/'trials.json',trials)
        validate(root)
        print(json.dumps({k:v for k,v in result.items() if k not in ('after','denied_calls','external_instructions')}),flush=True)
        if not result['execution_valid']:
            print('Execution gate failed; retaining failure and stopping.');break

def review(root):
    validate(root)
    settings=config(root,'review',root,[])
    prompt='Read protocol.json, preflight.json and assessment.json; inspect subject patches, final files and raw logs as needed. Review frozen criteria scoring, retrieval-budget integrity, semantic failures, unsupported claims, and consequential harness changes in control/hook.py. Focus on specific gaps; do not repeat implementation. Return findings only, no writes/execution. Scope this workspace only; three-minute bound. This is one initial outcome review; do not ask for retries.'
    result=launch(root,prompt,root/'review.jsonl',settings,180)
    dump(root/'review-execution.json',result);print(json.dumps(result))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['freeze','run','review']);parser.add_argument('destination',type=Path);args=parser.parse_args()
    globals()[args.mode](args.destination.resolve())
