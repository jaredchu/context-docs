"""Run the unchanged native prompts against isolated candidate packages."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('global_runner',HERE.parent/'global-install/run.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)

p=argparse.ArgumentParser();p.add_argument('mode',choices=['build','run']);p.add_argument('--output',type=Path,required=True);p.add_argument('--client',choices=['codex','claude']);p.add_argument('--direct-read',action='store_true')
a=p.parse_args();out=a.output.resolve()
if a.mode=='build':
    base.build(out)
    frozen=json.loads((out/'frozen.json').read_text())
    frozen['direct_read']=a.direct_read
    frozen['condition']='Unreleased core 0.1.4 read gating; isolated project-installed candidates, unchanged maintenance prompts and guard.'
    frozen['acceptance']='Capture one accurate failure event through candidate helper; no journal listing/search/content read and no write during repeat; audit accesses historical record and recovers actual synthetic result without writing; preserve package/instruction/source bytes.'
    frozen['candidate_sources']={}
    for source in [HERE/'run.py',HERE/'protocol.md',base.HERE/'run.py',base.HERE/'guard.py',base.HERE.parent/'integration/guard.py']+list((base.ROOT/'skills').rglob('*')):
        if not source.is_file() or '__pycache__' in source.parts:continue
        rel=str(source.relative_to(base.ROOT));frozen['candidate_sources'][rel]=hashlib.sha256(source.read_bytes()).hexdigest()
        dest=out/'source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
    for client,case in frozen['clients'].items():
        project=Path(case['project']).resolve();skills=project/('.agents/skills' if client=='codex' else '.claude/skills')
        case['project']=str(project)
        for name in base.NAMES:
            shutil.copytree(base.ROOT/'skills'/name,skills/name,ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.pyo'))
        rule=project/'AGENTS.md'
        rule.write_text(rule.read_text().replace('globally installed','project-installed').replace(case['skills'],str(skills)))
        case['released_global_packages']=case['packages']
        case['skills']=str(skills);case['packages']={n:base.hashes(skills/n) for n in base.NAMES}
        case['initial']=base.hashes(project)
        shutil.copytree(project,out/(client+'-candidate'))
    base.dump(out/'frozen.json',frozen)
    shutil.copy2(HERE/'protocol.md',out/'protocol.md')
else:
    frozen=json.loads((out/'frozen.json').read_text())
    assert all(hashlib.sha256((base.ROOT/p).read_bytes()).hexdigest()==h for p,h in frozen['candidate_sources'].items())
    if frozen.get('direct_read'):
        original_run=base.subprocess.run
        def isolated_run(command, **kwargs):
            if command[0]=='claude':
                command=list(command)
                command += ['--disable-slash-commands']
                command[command.index('--tools')+1]='Read,Write,Edit,Glob,Grep,Bash'
                command.remove('Skill')
                command[command.index('--setting-sources')+1]='project'
            return original_run(command, **kwargs)
        base.subprocess.run=isolated_run
    base.run(out,a.client)
