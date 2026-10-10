"""Independent CLI acceptance checks; results are mechanical, not semantic grades."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def verify(project):
    rows = [{"id": "z", "priority": 1}, {"id": "a", "priority": 2}, {"id": "m", "priority": 3}]
    render = lambda values: ''.join(json.dumps(row, sort_keys=True)+'\n' for row in values)
    cases = [('default', [], rows, 0), ('zero', ['--limit','0'], [], 0), ('one', ['--limit','1'], rows[:1], 0), ('two', ['--limit','2'], rows[:2], 0), ('excess', ['--limit','99'], rows, 0), ('negative', ['--limit','-1'], None, 2), ('noninteger', ['--limit','bad'], None, 2)]
    results = []
    with tempfile.TemporaryDirectory(prefix='handoff-verify-') as directory:
        path = Path(directory)/'input.jsonl'
        # Blank lines check preserved parsing; non-sorted IDs expose forbidden sorting.
        original = ('\n'+ '\n\n'.join(json.dumps(row) for row in rows)+'\n').encode()
        path.write_bytes(original)
        for name,args,expected,exit_code in cases:
            run = subprocess.run([sys.executable,str(project/'queue_cli.py'),str(path),*args],capture_output=True,text=True,timeout=10)
            passed = run.returncode==exit_code and (run.stdout==render(expected) if expected is not None else run.stdout=='' and 'error:' in run.stderr) and path.read_bytes()==original
            results.append(dict(name=name,passed=passed,exit_code=run.returncode,stdout=run.stdout,stderr=run.stderr,source_unchanged=path.read_bytes()==original))
        path.write_text('')
        run=subprocess.run([sys.executable,str(project/'queue_cli.py'),'--limit','1',str(path)],capture_output=True,text=True,timeout=10)
        results.append(dict(name='empty_input_option_before_path',passed=run.returncode==0 and run.stdout=='' and path.read_bytes()==b'',exit_code=run.returncode,stdout=run.stdout,stderr=run.stderr))
    run=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=project,capture_output=True,text=True,timeout=30)
    return dict(acceptance_checks=results,all_acceptance_passed=all(r['passed'] for r in results),fixture_tests=dict(exit_code=run.returncode,stdout=run.stdout,stderr=run.stderr))

if __name__=='__main__':
    print(json.dumps(verify(Path(sys.argv[1]).resolve()),indent=2))
