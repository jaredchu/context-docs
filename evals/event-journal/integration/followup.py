"""Prepare the separately frozen Claude task-first/native-invocation condition."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import run

out=Path(sys.argv[1]).resolve()
run.build(out)
frozen=json.loads((out/'frozen.json').read_text())
case=frozen['trajectories']['claude']
for stage,prompt in case['prompts'].items():
    marker='Use adopt-context-docs' if stage in ('default-off','enable','repeat','disable') else 'Use context-docs'
    index=prompt.rindex(marker) if stage!='repeat' else prompt.index('Use adopt-context-docs with')
    constraints,request=prompt[:index],prompt[index:]
    skill='adopt-context-docs' if marker.endswith('adopt-context-docs') else 'context-docs'
    request=request.replace(marker,'/'+skill,1)
    case['prompts'][stage]=request+'\n\nEvaluation constraints (apply to this task):\n'+constraints
frozen['condition']='Claude only: task first, native skill invocation; skills unchanged'
for file in ('followup.py','followup-protocol.md'):
    p=run.HERE/file
    rel=p.relative_to(run.ROOT)
    target=out/'source'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    frozen['sources'][str(rel)]=hashlib.sha256(p.read_bytes()).hexdigest()
shutil.copy2(run.HERE/'followup-protocol.md',out/'followup-protocol.md')
run.dump(out/'frozen.json',frozen)
