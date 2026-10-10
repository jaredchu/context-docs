"""One fresh session per arm; reuse native smoke launcher, no fallback or resume."""
import difflib
import hashlib
import importlib.util
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('native_smoke', ROOT/'evals/claude-code/smoke.py')
smoke = importlib.util.module_from_spec(spec); spec.loader.exec_module(smoke)
DEST = Path(sys.argv[1]).resolve()
mode = sys.argv[2]
p = json.loads((DEST/'protocol.json').read_text())
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
assert digest(DEST/'protocol.json') == (DEST/'protocol.sha256').read_text().strip()
assert all(digest(ROOT/n)==h for n,h in p['harness_hashes'].items())
assert subprocess.check_output(['claude','--version'],text=True).strip()==p['cli_version']
assert all(digest(DEST/'control'/n)==h for n,h in p['control_hashes'].items())
# Do not inherit API credentials or alternate-provider routing.
for n in list(os.environ):
    if n.startswith(('ANTHROPIC_', 'CLAUDE_CODE_USE_')):
        os.environ.pop(n)
logs = DEST/'logs'; logs.mkdir(exist_ok=True)
if mode in ('preflight','review'):
    log = logs/(mode+'.jsonl')
    assert not log.exists(), 'One review only.'
    config = dict(project=str(DEST), events=str(DEST/'control'/(mode+'.events.jsonl')), writable=[])
    config_path = DEST/'control'/(mode+'.config.json'); config_path.write_text(json.dumps(config))
    import shlex
    command = shlex.join([sys.executable,str(DEST/'control/hook.py'),str(config_path)])+' || exit 2'
    settings = dict(autoMemoryEnabled=False,hooks={n:[dict(hooks=[dict(type='command',command=command,timeout=10)])] for n in ('InstructionsLoaded','PreToolUse','PostToolUse','PostToolUseFailure')})
    settings_path=DEST/'control'/(mode+'.settings.json'); settings_path.write_text(json.dumps(settings))
    prompt = ('Read protocol.json and inspect the fixture, requirements, and harness control/hook.py plus control/guard_hook.py. Review the frozen design for equivalence of facts, executable scope, answer leakage, and unsupported inference. Return concrete blockers or approve a bounded pilot. Do not edit or execute anything. Scope: only this evaluation workspace. Time limit three minutes.' if mode=='preflight' else 'Read protocol.json, assessment.json, and logs/curated.jsonl and logs/scattered.jsonl as needed. Review the Sol assessment against actual final files under projects/ and evidence. Focus on criterion scoring, unsupported claims, regressions and confounds. Return findings only; do not edit or execute anything. Scope only this workspace. Three-minute bound.')
    items=[(mode,DEST,prompt,settings_path,180,['Read','Glob','Grep'])]
else:
    assert mode=='subjects'
    assert not (DEST/'trials.json').exists(), 'No retries.'
    assert json.loads((DEST/'preflight-verdict.json').read_text())['accepted_by_coordinator']
    items=[]
    for arm in p['order']:
        project=DEST/'projects'/arm
        actual={str(f.relative_to(project)):f.read_text() for f in project.rglob('*') if f.is_file()}
        assert actual==p['fixtures'][arm], 'Fixture drift.'
        assert not (logs/(arm+'.jsonl')).exists()
        items.append((arm,project,p['prompts'][arm],DEST/'control'/(arm+'.settings.json'),420,p['allowed_tools']))
results=[]
for name,project,prompt,settings,timeout,tools in items:
    print('Starting '+name,flush=True)
    protocol=dict(model=p['model'],permission_mode='acceptEdits',setting_sources='project',allowed_tools=tools,session_timeout_seconds=timeout,extra_args=['--no-session-persistence','--disable-slash-commands','--effort','high','--tools',','.join(tools),'--settings',str(settings)])
    result=smoke.run_session(project,prompt,logs/(name+'.jsonl'),protocol)
    events=[json.loads(line) for line in (logs/(name+'.jsonl')).read_text().splitlines() if line.strip().startswith('{')]
    models=sorted({e['message']['model'] for e in events if e.get('type')=='assistant' and e.get('message',{}).get('model')})
    final=next((e.get('result','') for e in reversed(events) if e.get('type')=='result'),'')
    (DEST/(name+'-final.txt')).write_text(final)
    result.update(id=name,responding_models=models,result_received=any(e.get('type')=='result' for e in events))
    hook_path=DEST/'control'/(name+'.events.jsonl')
    hooks=[json.loads(line) for line in hook_path.read_text().splitlines()] if hook_path.exists() else []
    result['external_instructions']=[e for e in hooks if e.get('hook_event_name')=='InstructionsLoaded' and not Path(e['file_path']).resolve().is_relative_to(project)]
    result['denied_calls']=[e for e in hooks if e.get('decision')=='deny']
    if mode=='subjects':
        result['frozen_protocol_unchanged']=digest(DEST/'protocol.json')==(DEST/'protocol.sha256').read_text().strip()
        result['frozen_controls_unchanged']=all(digest(DEST/'control'/n)==h for n,h in p['control_hashes'].items())
    result['tool_calls']=sum(e.get('hook_event_name')=='PreToolUse' for e in hooks)
    if mode=='subjects':
        before=p['fixtures'][name]
        after={str(f.relative_to(project)):f.read_text() for f in project.rglob('*') if f.is_file() and '__pycache__' not in f.parts}
        result['after']=after
        result['protected_files_unchanged']=all(after.get(n)==body for n,body in before.items() if n not in ('queue_cli.py','tests/test_queue.py'))
        result['changed_files']=[n for n in sorted(set(before)|set(after)) if before.get(n)!=after.get(n)]
        patch=''.join(''.join(difflib.unified_diff(before.get(n,'').splitlines(True),after.get(n,'').splitlines(True),fromfile='before/'+n,tofile='after/'+n)) for n in result['changed_files'])
        (DEST/(name+'.patch')).write_text(patch)
    results.append(result)
    (DEST/('trials.json' if mode=='subjects' else mode+'-execution.json')).write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('after','denied_calls','external_instructions')}),flush=True)
    if models!=[p['model']] or result['exit_code']!=0 or not result['result_received'] or result['external_instructions'] or (mode=='subjects' and not all(result[k] for k in ('frozen_protocol_unchanged','frozen_controls_unchanged','protected_files_unchanged'))):
        print('Execution gate failed; retaining attempt and stopping.',flush=True); break
