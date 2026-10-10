"""Frozen independent CLI outcomes; semantic criteria reviewed separately."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

def verify(project):
    rows=[{'tenant':'blue','id':'z','value':10},{'tenant':'red','id':'z','value':1},{'tenant':'red','id':'z','value':2},{'tenant':'red','id':'a','value':3},{'tenant':'blue','id':'a','value':11},{'tenant':'red','id':'Z','value':4},{'tenant':'Red','id':'z','value':20}]
    unique=[rows[i] for i in (0,1,3,4,5,6)];red=[rows[i] for i in (1,3,5)]
    render=lambda rr:''.join(json.dumps(row,sort_keys=True)+'\n' for row in rr)
    normal='\n'+'\n\n'.join(json.dumps(row) for row in rows)+'\n'
    cases=[('default',normal,[],unique,0),('zero',normal,['--limit','0'],[],0),('one',normal,['--limit','1'],unique[:1],0),('two',normal,['--limit','2'],unique[:2],0),('excess',normal,['--limit','99'],unique,0),('tenant_before_cap',normal,['--tenant','red','--limit','2'],red[:2],0),('dedup_before_cap',normal,['--tenant','red','--limit','3'],red,0),('tenant_case_sensitive',normal,['--tenant','Red','--limit','1'],[rows[6]],0),('no_tenant_match',normal,['--tenant','green','--limit','1'],[],0),('negative',normal,['--limit','-1'],None,2),('noninteger',normal,['--limit','abc'],None,2),('empty_input','',['--limit','1'],[],0),('late_invalid_json',normal+'not-json\n',['--limit','1'],None,2),('late_invalid_schema',normal+'{"tenant":"red","id":42}\n',['--limit','1'],None,2),('late_invalid_with_zero',normal+'{"id":"missing"}\n',['--limit','0'],None,2),('unselected_invalid_row',normal+'{"tenant":"blue","id":null}\n',['--tenant','red','--limit','1'],None,2)]
    checks=[]
    with tempfile.TemporaryDirectory(prefix='parcel-verifier-') as directory:
        path=Path(directory)/'input.jsonl'
        for name,body,args,expected,code in cases:
            original=body.encode();path.write_bytes(original)
            run=subprocess.run([sys.executable,'-m','parcel',str(path),*args],cwd=project,text=True,capture_output=True,timeout=10)
            unchanged=path.read_bytes()==original
            passed=run.returncode==code and unchanged and (run.stdout==render(expected) if expected is not None else run.stdout=='' and 'error:' in run.stderr)
            checks.append(dict(name=name,passed=passed,exit_code=run.returncode,stdout=run.stdout,stderr=run.stderr,source_unchanged=unchanged))
    suite=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=project,text=True,capture_output=True,timeout=30)
    return dict(checks=checks,all_acceptance_passed=all(c['passed'] for c in checks),suite=dict(exit_code=suite.returncode,stdout=suite.stdout,stderr=suite.stderr))
if __name__=='__main__':print(json.dumps(verify(Path(sys.argv[1]).resolve()),indent=2))
