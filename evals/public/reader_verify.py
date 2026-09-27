"""Reader scope/schema/citation-path checks. Answer semantics require separate review."""
import json
import subprocess
import sys
from pathlib import Path


def snapshot(root):
    return {str(p.relative_to(root)):p.read_bytes().decode('utf-8') for p in sorted(root.rglob('*'))
            if p.is_file() and '.git' not in p.relative_to(root).parts}


def grade(spec, root, output):
    files=snapshot(root)
    checks={'project_byte_identical':files==spec['before']}
    error=None
    try:
        answers=json.loads((output/'answers.json').read_text())
    except (OSError,ValueError) as exc:
        answers=None;error=type(exc).__name__
    valid=isinstance(answers,list) and len(answers)==len(spec['ids']) and all(
        isinstance(a,dict) and set(a)=={'id','answer','sources'} and
        isinstance(a['id'],str) and isinstance(a['answer'],str) and bool(a['answer'].strip()) and
        isinstance(a['sources'],list) and bool(a['sources']) and all(isinstance(p,str) for p in a['sources']) for a in answers)
    if valid:
        valid=sorted(a['id'] for a in answers)==sorted(spec['ids'])
    checks['answer_schema']=valid
    checks['citation_paths_exist']=valid and all(p in files for a in answers for p in a['sources'])
    if (root/'.git').exists():
        checks['git_unchanged']=(subprocess.check_output(['git','rev-list','--count','HEAD'],cwd=root,text=True).strip()=='1' and not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=root,text=True).strip())
    return dict(checks=checks,mechanical_pass=all(checks.values()),answers=answers,parse_error=error)


if __name__=='__main__':
    result=grade(json.loads(Path(sys.argv[1]).read_text()),Path('/workspace'),Path('/output'))
    logs=Path('/logs/verifier');logs.mkdir(parents=True,exist_ok=True)
    (logs/'observed.json').write_text(json.dumps(result,indent=2)+'\n')
    (logs/'reward.json').write_text(json.dumps({'mechanical':int(result['mechanical_pass'])})+'\n')
    print(json.dumps({'checks':result['checks'],'semantic_review':'required'}))
