"""Bounded fresh-session check of actual global skills; raw streams stay local."""
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

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
NAMES = ('context-docs', 'adopt-context-docs')
REQUESTS = {
    'capture': 'Run python3 checks/probe.py and update the project context with the actual outcome.',
    'repeat': 'Maintain project context. No new facts or work have occurred since the previous update. Do not rerun checks.',
    'audit': 'Investigate the earlier staging check, read-only: what failed, what value was tested, was production checked, and what historical evidence survives? Cite source files. Do not rerun checks or write anything.',
}


def hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def build(out):
    out.mkdir(parents=True, exist_ok=True)
    if (out / 'frozen.json').exists():
        raise SystemExit('Already frozen; use a fresh output directory.')
    scratch = Path(tempfile.mkdtemp(prefix='global-journal-eval-'))
    frozen = {'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
              'requests': REQUESTS, 'clients': {}, 'source_hashes': hashes(HERE),
              'acceptance': 'Capture actual failure via global helper without a logging reminder; repeat and audit preserve bytes; audit correctly distinguishes staging failure from untested production; preserve source/instructions/global packages; no cross-project logs.',
              'limits': 'One synthetic no-Git trajectory per client; ordinary maintenance prompts but a standing project skill rule. Claude uses evaluation guard; Codex uses workspace sandbox. Not real-project effort or unrestricted reliability evidence.'}
    for client in ('codex', 'claude'):
        project = scratch / client
        (project / 'checks').mkdir(parents=True)
        (project / 'notes').mkdir()
        skills = Path.home() / ('.agents/skills' if client == 'codex' else '.claude/skills')
        rule = ('# Synthetic project\n\nRead README.md and notes/current.md first.\n'
                'Use the globally installed context-docs skill after meaningful changes and for context maintenance/audits.\n'
                f'Read its instructions at {skills / "context-docs/SKILL.md"}.\n'
                'Preserve existing decisions and evidence. Audits are read-only. Do not write outside this project.\n\n'
                'Method: context-docs\nAdopted: 2026-09-01\nEntry point: notes/current.md\n'
                'Event journal: jsonl\nEvent journal directory: .context/events\n')
        (project / 'AGENTS.md').write_text(rule)
        (project / 'CLAUDE.md').write_text('@AGENTS.md\n')
        (project / 'README.md').write_text('# Queue fixture\n\nSynthetic staging only. [Current context](notes/current.md).\n')
        (project / 'notes/current.md').write_text('# Current context\n\nBatch limit 4 is configured for synthetic staging. The probe has not yet run. Production remains untested. Manual release review is still required.\n')
        (project / 'checks/probe.py').write_text('import sys\nprint("Synthetic staging: batch_limit=4; queue overflow; exit 7. No production check.")\nsys.exit(7)\n')
        frozen['clients'][client] = {'project': str(project), 'skills': str(skills),
            'version': subprocess.check_output([client, '--version'], text=True).strip(),
            'packages': {n: hashes(skills / n) for n in NAMES}, 'initial': hashes(project)}
        shutil.copytree(project, out / (client + '-initial'))
    dump(out / 'frozen.json', frozen)
    print('Frozen', out, flush=True)


def run(out, client):
    frozen = json.loads((out / 'frozen.json').read_text())
    assert hashes(HERE) == frozen['source_hashes']
    case = frozen['clients'][client]
    project, skills = Path(case['project']), Path(case['skills'])
    assert hashes(project) == case['initial']
    results = []
    for stage, request in frozen['requests'].items():
        stem = client + '-' + stage
        stream_path = out / (stem + '-stream.jsonl')
        if stream_path.exists(): raise SystemExit('Refusing to overwrite a prior run')
        readonly = stage == 'audit'
        config = {'project': str(project), 'helper': str(skills / 'context-docs/scripts/event_journal.py'),
                  'python': sys.executable, 'read_only': readonly,
                  'immutable': ['AGENTS.md', 'CLAUDE.md', 'README.md', 'checks/probe.py'],
                  'skill_roots': [str(skills/n) for n in NAMES], 'log': str(out/(stem+'-hooks.jsonl'))}
        cfg = out / (stem + '-config.json'); dump(cfg, config)
        hook = shlex.join([sys.executable, str(HERE/'guard.py'), str(cfg)]) + ' || exit 2'
        settings = out / (stem+'-settings.json')
        dump(settings, {'hooks': {kind: [{'matcher': '*', 'hooks': [{'type': 'command', 'command': hook}]}]
                                 for kind in ('InstructionsLoaded', 'PreToolUse', 'PostToolUse', 'PostToolUseFailure')}})
        # The boundary describes supported tool syntax but never names logging or the helper.
        prompt = request + '\n\nWork only in this synthetic project. Preserve instructions, scripts and global skill files. No network, delegation or commits.'
        if client == 'claude':
            prompt += ' Evaluation shell boundary: use individual direct python3 commands (file arguments, no stdin, redirection or shell operators), pwd/ls or simple read-only git commands.'
            cmd = ['claude','-p',prompt,'--output-format','stream-json','--verbose','--permission-mode','dontAsk',
                   '--setting-sources','user,project','--strict-mcp-config','--no-session-persistence',
                   '--tools','Read,Write,Edit,Glob,Grep,Skill,Bash','--allowedTools','Read','Write','Edit','Glob','Grep','Skill','Bash','--settings',str(settings)]
        else:
            cmd = ['codex','exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--sandbox',
                   'read-only' if readonly else 'workspace-write','--json','--output-last-message',str(out/(stem+'-final.txt')),prompt]
        (out/(stem+'-prompt.txt')).write_text(prompt)
        before = hashes(project)
        env = {k:v for k,v in os.environ.items() if not k.startswith('CLAUDE_CODE_')}
        env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1')
        start = time.monotonic(); print('START',stem,flush=True)
        with stream_path.open('w') as stream:
            try:
                p = subprocess.run(cmd,cwd=project,env=env,stdin=subprocess.DEVNULL,stdout=stream,stderr=subprocess.PIPE,text=True,timeout=240)
                code, error = p.returncode, p.stderr
            except subprocess.TimeoutExpired:
                code, error = 124, 'Timeout'
        (out/(stem+'-stderr.txt')).write_text(error)
        rows = [json.loads(l) for l in stream_path.read_text().splitlines() if l.strip()]
        if client == 'claude':
            final = next((r.get('result','') for r in reversed(rows) if r.get('type')=='result'), '')
            (out/(stem+'-final.txt')).write_text(final)
        after = hashes(project)
        packages = all(hashes(skills/n)==case['packages'][n] for n in NAMES)
        immutable = all(after.get(n)==before[n] for n in config['immutable'])
        terminal = any(r.get('type')==('result' if client=='claude' else 'turn.completed') for r in rows)
        events = []
        for file in sorted((project/'.context/events').glob('*.jsonl')):
            events += [json.loads(l) for l in file.read_text().splitlines()]
        result = dict(stage=stage, exit_code=code, seconds=round(time.monotonic()-start,2), terminal=terminal,
                      immutable_unchanged=immutable, global_packages_unchanged=packages,
                      all_bytes_unchanged=before==after, events=events, before=before, after=after)
        results.append(result); dump(out/(client+'-trials.json'),results)
        shutil.copytree(project,out/stem,ignore=shutil.ignore_patterns('__pycache__'))
        print('DONE',stem,'exit',code,'events',len(events),'unchanged',before==after,flush=True)
        if code or not terminal or not immutable or not packages: break


if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('mode',choices=['build','run']);p.add_argument('--output',type=Path,required=True);p.add_argument('--client',choices=['codex','claude'])
    args=p.parse_args();out=args.output.resolve()
    if args.mode=='build':build(out)
    else:run(out,args.client)
