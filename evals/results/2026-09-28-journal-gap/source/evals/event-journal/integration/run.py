"""Build and run native installed-skill integration trajectories, with no bridge."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SKILLS=('context-docs','adopt-context-docs')
STAGES=('default-off','enable','failure','approval','repeat','missing-helper','audit','disable','disabled-maintenance')
PROBE='''import json
from pathlib import Path
import sys
limit=json.loads(Path("settings.json").read_text())["batch_limit"]
if limit == 4:
    print("Synthetic staging fixture: batch_limit=4; queue overflow; exit 7. No production check.")
    sys.exit(7)
print(f"Synthetic staging fixture: batch_limit={limit}; passed; exit 0. No production check.")
'''
RULE='''# Project working agreement

Keep the unrelated release checklist intact. This project is a synthetic staging fixture.

## Our continuity notes
Method: context-docs
Adopted: 2026-09-01
Entry point: notes/current.md

Use the context-docs skill after meaningful changes and for context audits.
Read the skill before maintaining our existing notes. Preserve decisions and evidence.
Audits leave files unchanged. If nothing durable changed, make no bookkeeping edits.
'''
CONTEXT='''# Current project context

## Earlier decision
Rina approved a batch limit of 2 for local smoke checks on 2026-09-01 to bound
memory use. Source: synthetic-owner:D0. Preserve this separate local scope.

## Current state
settings.json configures batch_limit=4 for the synthetic staging fixture.
The staging probe has not been run in this trajectory. Production is unverified.

## History
Earlier context history is retained in history/events/legacy.jsonl. Its existence
does not enable logging. Release checklist: manual review remains required.
'''
APPROVAL='''# Supplied fixture owner decision

2026-09-28: Fixture owner Rina approves batch_limit=6 only for staging because
larger batches increase peak memory. Developer proposed batch_limit=12; that
proposal has no owner approval. Local smoke-check approval at limit 2 is unchanged.
Production validation and rollout are not approved or established here.
Source ID: synthetic-owner:A1.
'''


def dump(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2)+'\n')


def hashes(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts}


def git(root,*args):
    env=dict(os.environ,GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_NOSYSTEM='1')
    return subprocess.check_output(['git','-c','core.hooksPath=/dev/null','-c','commit.gpgsign=false',
        '-c','user.name=Synthetic Evaluator','-c','user.email=eval@example.invalid',*args],cwd=root,env=env,text=True,stderr=subprocess.STDOUT)


def build(out):
    out.mkdir(parents=True,exist_ok=False)
    scratch=Path(tempfile.mkdtemp(prefix='context-optin-'))
    control=scratch/'control';control.mkdir()
    shutil.copy2(HERE/'guard.py',control/'guard.py')
    frozen={'scratch':str(scratch),'source_commit':git(ROOT,'rev-parse','HEAD').strip(),
            'versions':{c:subprocess.check_output([c,'--version'],text=True).strip() for c in ('claude','codex')},
            'models':'client defaults','trajectories':{},'sources':{}}
    for p in [HERE/'protocol.md',HERE/'run.py',HERE/'guard.py',HERE/'test_guard.py']+list((ROOT/'skills').rglob('*')):
        if not p.is_file() or '__pycache__' in p.parts:continue
        rel=p.relative_to(ROOT);target=out/'source'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
        frozen['sources'][str(rel)]=hashlib.sha256(p.read_bytes()).hexdigest()
    for client in ('claude','codex'):
        project=scratch/client;project.mkdir()
        install='.claude/skills' if client=='claude' else '.agents/skills'
        instruction='CLAUDE.md' if client=='claude' else 'AGENTS.md'
        (project/'notes').mkdir();(project/'checks').mkdir();(project/'evidence').mkdir()
        (project/instruction).write_text(RULE)
        if client=='codex':(project/'CLAUDE.md').write_text('@AGENTS.md\n')
        (project/'README.md').write_text('# Synthetic staging fixture\n\nCurrent context: notes/current.md.\n')
        (project/'notes/current.md').write_text(CONTEXT)
        (project/'checks/probe.py').write_text(PROBE)
        (project/'settings.json').write_text('{"batch_limit":4,"scope":"synthetic staging"}\n')
        oldfiles=git(ROOT,'ls-tree','-r','--name-only','HEAD','skills').splitlines()
        for rel in oldfiles:
            target=project/install/Path(rel).relative_to('skills');target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT))
        legacy={'type':'decision','status':'approved','actor':'synthetic-recorder',
                'summary':'2026-09-01: Rina approved limit 2 for local smoke checks to bound memory use.',
                'sources':['synthetic-owner:D0'],'revision':'unavailable (historical fixture)',
                'authority':'Fixture owner Rina; synthetic-owner:D0'}
        result=subprocess.run([sys.executable,str(ROOT/'skills/context-docs/scripts/event_journal.py'),
               '--directory',str(project/'history/events'),'append','--session','legacy'],input=json.dumps(legacy),text=True,capture_output=True,check=True)
        before=hashes(project)
        if client=='codex':
            git(project,'init','-q');git(project,'add','.');git(project,'commit','-qm','Original adopted fixture')
        old_versions={s:(project/install/s/'VERSION').read_text().strip() for s in SKILLS}
        for name in SKILLS:
            shutil.copytree(ROOT/'skills'/name,project/install/name,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
        after=hashes(project)
        protected={k:v for k,v in before.items() if not k.startswith(install+'/')}
        assert all(after[k]==v for k,v in protected.items())
        helper=install+'/context-docs/scripts/event_journal.py'
        candidate={k:v for k,v in after.items() if k.startswith(install+'/')}
        prompts={}
        boundary=('Evaluation boundary: use project file tools normally. Bash permits direct python3 commands for the installed '
                  'event_journal.py with --input JSON files (no stdin/redirects/pipes), checks/probe.py, python3 --version, '
                  'pwd/ls and simple read-only git status/diff/log/rev-parse. Do not write packages, source scripts, settings.json, '
                  'evidence files or raw JSONL directly. No outside-project reads/writes, network or delegation. ')
        common=('Work only in this synthetic project. Preserve the existing adoption date, custom context path, '
                'release checklist, instruction routing, installed packages and supplied evidence. '
                f'The project-installed skills are under {install}; use those copies and their full instructions. ')
        if client=='claude':common+=boundary
        requests={
          'default-off':'Use adopt-context-docs to verify ordinary adoption after the installed skill upgrade. There are no new project facts. No request to enable logging has been made. Leave an equivalent setup unchanged.',
          'enable':'Use adopt-context-docs to enable optional JSONL logging at history/events in this existing adopted project.',
          'failure':'Use context-docs. Run python3 checks/probe.py for this synthetic staging fixture, then maintain context from the actual result and follow the project logging preference.',
          'approval':'Use context-docs. The fixture owner supplied evidence/approval.md and settings.json now reflects the approved staging setting. Read that evidence, run python3 checks/probe.py, and maintain context and opted-in history from this new work.',
          'repeat':'Use adopt-context-docs with the same enabled JSONL directory history/events, then use context-docs for maintenance. There are no new facts or events. Do not rerun checks; leave equivalent setup and unchanged context alone.',
          'missing-helper':'Use context-docs to maintain notes from the new supplied evidence/pending.md, following existing project settings. Installed packages are immutable; report any unavailable capability and continue the authorized documentation work.',
          'audit':'Use context-docs for a read-only audit/investigation. What actually failed earlier, what setting and scope did Rina later approve, was limit 12 approved, what happened on the later check, and which new fact could not be journaled? Cite evidence. Distinguish local smoke, synthetic staging and production. Do not rerun checks, repair files or write anything.',
          'disable':'Use adopt-context-docs to disable optional event logging for this project, retaining its history.',
          'disabled-maintenance':'Use context-docs to maintain the new fact in evidence/followup.md. Honor the current disabled logging preference. Installed packages are immutable.'}
        for stage in STAGES:prompts[stage]=common+requests[stage]
        frozen['trajectories'][client]={'project':str(project),'install':install,'instruction':instruction,'helper':helper,
            'old_versions':old_versions,'before_upgrade':before,'after_upgrade':after,'candidate_packages':candidate,
            'upgrade_preserved_project':True,'prompts':prompts,'legacy':(project/'history/events/legacy.jsonl').read_text()}
        shutil.copytree(project,out/(client+'-upgraded'),ignore=shutil.ignore_patterns('.git','__pycache__'))
    dump(out/'frozen.json',frozen)
    shutil.copy2(HERE/'protocol.md',out/'protocol.md')
    print('Built:',out,flush=True)


def run(out,client):
    frozen=json.loads((out/'frozen.json').read_text());case=frozen['trajectories'][client]
    project=Path(case['project']);control=Path(frozen['scratch'])/'control'
    assert hashes(project)==case['after_upgrade'],'Fixture changed since freeze'
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in frozen['sources'].items()),'Candidate changed since freeze'
    trials=[]
    if (out/(client+'-trials.json')).exists():raise SystemExit('Already run; preserve existing results')
    for stage in STAGES:
        name=client+'-'+stage
        if (out/(name+'-stream.jsonl')).exists():raise SystemExit('Existing log; no retry in place')
        if stage=='approval':
            (project/'evidence/approval.md').write_text(APPROVAL)
            (project/'settings.json').write_text('{"batch_limit":6,"scope":"synthetic staging"}\n')
        if stage=='missing-helper':
            (project/'evidence/pending.md').write_text('# Pending check\n\nRestore verification is still pending; no restore check has been executed. Source: synthetic-team:P1.\n')
        if stage=='disabled-maintenance':
            (project/'evidence/followup.md').write_text('# New project fact\n\nThe fixture owner scheduled manual review for the next work session. This is a plan, not a completed review. Source: synthetic-owner:F1.\n')
        missing=stage in ('missing-helper','disabled-maintenance')
        helper=project/case['helper']
        if missing:
            saved=helper.read_bytes();helper.unlink()
        immutable=['README.md','checks/probe.py','settings.json']+[str(p.relative_to(project)) for p in (project/'evidence').glob('*')]
        if client=='codex':immutable.append('CLAUDE.md')
        before=hashes(project)
        config={'project':str(project),'helper':case['helper'],'python':sys.executable,'read_only':stage=='audit',
                'immutable':immutable,'log':str(out/(name+'-hooks.jsonl'))}
        cfg=control/(name+'.json');dump(cfg,config)
        hook=shlex.join([sys.executable,str(control/'guard.py'),str(cfg)])+' || exit 2'
        settings=control/(name+'-settings.json')
        dump(settings,{'hooks':{kind:[{'matcher':'*','hooks':[{'type':'command','command':hook}]}]
                      for kind in ('InstructionsLoaded','PreToolUse','PostToolUse','PostToolUseFailure')}})
        prompt=case['prompts'][stage];(out/(name+'-prompt.txt')).write_text(prompt)
        if client=='claude':
            command=['claude','-p',prompt,'--output-format','stream-json','--verbose','--permission-mode','dontAsk',
                '--setting-sources','project','--strict-mcp-config','--no-session-persistence',
                '--tools','Read,Write,Edit,Glob,Grep,Skill,Bash','--allowedTools','Read','Write','Edit','Glob','Grep','Skill','Bash','--settings',str(settings)]
        else:
            command=['codex','exec','--ignore-user-config','--ignore-rules','--ephemeral','--skip-git-repo-check',
                '--sandbox','read-only' if stage=='audit' else 'workspace-write','--json',
                '--output-last-message',str(out/(name+'-final.txt')),prompt]
        env={k:v for k,v in os.environ.items() if not k.startswith('CLAUDE_CODE_')}
        env.update(GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_NOSYSTEM='1')
        started=time.monotonic();print('START',name,flush=True)
        with (out/(name+'-stream.jsonl')).open('w') as stream:
            try:
                completed=subprocess.run(command,cwd=project,env=env,stdin=subprocess.DEVNULL,
                    stdout=stream,stderr=subprocess.PIPE,text=True,timeout=300)
                code,stderr=completed.returncode,completed.stderr
            except subprocess.TimeoutExpired:
                code,stderr=124,'Session timed out'
        (out/(name+'-stderr.txt')).write_text(stderr)
        after=hashes(project)
        packages={k:v for k,v in after.items() if k.startswith(case['install']+'/')}
        expected=dict(case['candidate_packages'])
        if missing:expected.pop(case['helper'])
        protected=all(after.get(p)==before.get(p) for p in immutable) and packages==expected
        journal_before={k:v for k,v in before.items() if k.startswith('history/events/')}
        journal_after={k:v for k,v in after.items() if k.startswith('history/events/')}
        legacy=(project/'history/events/legacy.jsonl').read_text()==case['legacy']
        result={'stage':stage,'exit_code':code,'seconds':round(time.monotonic()-started,2),
                'protected_unchanged':protected,'legacy_unchanged':legacy,'all_bytes_unchanged':before==after,
                'journal_unchanged':journal_before==journal_after,'before':before,'after':after}
        shutil.copytree(project,out/name,ignore=shutil.ignore_patterns('.git','__pycache__'))
        if missing:helper.write_bytes(saved)
        trials.append(result);dump(out/(client+'-trials.json'),trials)
        print('DONE',name,code,result['seconds'],'protected',protected,'legacy',legacy,flush=True)
        rows=[json.loads(l) for l in (out/(name+'-stream.jsonl')).read_text().splitlines()]
        terminal=any(r.get('type')==('result' if client=='claude' else 'turn.completed') for r in rows)
        fatal=any(r.get('type') in ('error','turn.failed') or (r.get('type')=='result' and r.get('is_error')) for r in rows)
        if code or not protected or not legacy or not terminal or fatal:
            print('STOP',name,'integration gate failure',flush=True);break
    print('FINISHED',client,flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=('build','run'));p.add_argument('--output',type=Path,required=True);p.add_argument('--client',choices=('claude','codex'))
    args=p.parse_args();out=args.output.resolve()
    if args.mode=='build':build(out)
    else:run(out,args.client)
