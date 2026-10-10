"""Subscription-only exact-model launcher; file-tools only, no retries."""
import importlib.util
import json
import os
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('native_smoke',ROOT/'evals/claude-code/smoke.py')
smoke=importlib.util.module_from_spec(spec);spec.loader.exec_module(smoke)

def launch(project,prompt,log,settings,seconds):
    assert not log.exists(),'One attempt only.'
    for name in list(os.environ):
        if name.startswith(('ANTHROPIC_','CLAUDE_CODE_USE_')):os.environ.pop(name)
    tools=['Read','Write','Edit','Glob','Grep']
    config=dict(model='claude-opus-5-5',permission_mode='acceptEdits',setting_sources='project',allowed_tools=tools,session_timeout_seconds=seconds,extra_args=['--no-session-persistence','--disable-slash-commands','--effort','high','--tools',','.join(tools),'--settings',str(settings)])
    result=smoke.run_session(project,prompt,log,config)
    events=[json.loads(line) for line in log.read_text().splitlines() if line.startswith('{')]
    result['responding_models']=sorted({e['message']['model'] for e in events if e.get('type')=='assistant' and e.get('message',{}).get('model')})
    result['result_received']=any(e.get('type')=='result' for e in events)
    final=next((e.get('result','') for e in reversed(events) if e.get('type')=='result'),'')
    log.with_suffix('.final.txt').write_text(final)
    return result

if __name__=='__main__':
    project=Path(sys.argv[1]).resolve();name=sys.argv[2];seconds=int(sys.argv[3])
    result=launch(project,(project/(name+'-prompt.txt')).read_text(),project/(name+'.jsonl'),project/'control'/(name+'.settings.json'),seconds)
    (project/(name+'-execution.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
