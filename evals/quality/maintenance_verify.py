"""Shared maintenance checks plus the complete resulting synthetic artifact."""
import json
import sys
from pathlib import Path
from base_verify import grade,snapshot

spec=json.loads(Path(sys.argv[1]).read_text())
before=json.loads(Path(spec['input_snapshot']).read_text())
assert isinstance(before,dict) and all(isinstance(k,str) and isinstance(v,str) for k,v in before.items())
result=grade(spec,Path('/workspace'),Path('/output'),before)
result['files']=snapshot(Path('/workspace'))
logs=Path('/logs/verifier');logs.mkdir(parents=True,exist_ok=True)
(logs/'observed.json').write_text(json.dumps(result,indent=2)+'\n')
(logs/'reward.json').write_text(json.dumps({'mechanical':int(result['mechanical_pass'])})+'\n')
print(json.dumps({'checks':result['checks'],'semantic_review':'required'}))
