"""Freeze/run one normal global invocation per client after the candidate upgrade."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('global_runner',HERE.parent/'global-install/run.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
p=argparse.ArgumentParser();p.add_argument('mode',choices=['build','run']);p.add_argument('--output',type=Path,required=True);p.add_argument('--client',choices=['codex','claude']);p.add_argument('--explicit-tool',action='store_true')
a=p.parse_args();out=a.output.resolve()
if a.mode=='build':
    base.build(out)
    f=json.loads((out/'frozen.json').read_text())
    f['explicit_tool']=a.explicit_tool
    f['condition']='Normal named invocation of actual global core 0.1.4/adoption 0.1.5; no-change maintenance with existing synthetic history'
    f['requests']={'repeat':base.REQUESTS['repeat']}
    f['acceptance']='Native invocation exposes the updated global skill; no journal listing/search/content read, no rerun, and no project/package writes. Do not count byte preservation alone as a no-read pass.'
    for client,case in f['clients'].items():
        project=Path(case['project'])
        event={'type':'verification','status':'observed','actor':'Synthetic fixture author',
               'summary':'Synthetic fixture history: staging probe at batch_limit=4 printed queue overflow and exited 7; production untested.',
               'sources':['synthetic-fixture:H1','checks/probe.py'],'revision':'unavailable (no Git)',
               'check':{'command':'python3 checks/probe.py','scope':'Authored synthetic staging history, not a live production test',
                        'result':'Fixture history: queue overflow at limit 4; exit 7; production untested'}}
        subprocess.run([sys.executable,str(Path(case['skills'])/'context-docs/scripts/event_journal.py'),
                        '--directory',str(project/'.context/events'),'append','--session','fixture-history'],
                       input=json.dumps(event),text=True,capture_output=True,check=True)
        (project/'notes/current.md').write_text('# Current context\n\nThe synthetic staging probe previously reported queue overflow at batch_limit=4 and exited 7. Production remains untested and manual release review is required. This is authored fixture history, not a live service check.\n\n[Recorded event](../.context/events/fixture-history.jsonl) preserves this same outcome. No new work or facts have occurred since that record.\n')
        case['initial']=base.hashes(project)
        shutil.copytree(project,out/(client+'-ready'))
    f['global_check_source']=__file__
    f['global_check_sha256']=base.hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    base.dump(out/'frozen.json',f)
    shutil.copy2(__file__,out/'global-check.py')
    shutil.copy2(HERE/'global-check-protocol.md',out/'protocol.md')
else:
    f=json.loads((out/'frozen.json').read_text())
    assert base.hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==f['global_check_sha256']
    # Freeze the client-native invocation prefix before the single session starts.
    prefix=('/context-docs ' if a.client=='claude' else '$context-docs ')
    if f.get('explicit_tool') and a.client=='claude':
        prefix='Invoke context-docs using the Skill tool, then '
    f['requests']['repeat']=prefix+base.REQUESTS['repeat']
    runtime=out/(a.client+'-run');runtime.mkdir(exist_ok=False)
    base.dump(runtime/'frozen.json',f)
    base.run(runtime,a.client)
