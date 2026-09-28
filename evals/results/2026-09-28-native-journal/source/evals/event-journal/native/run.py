"""Bounded native comparison. Run once per fresh output directory."""
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
FEED = '''Synthetic supplied evidence (not checks executed by this evaluation):
E1, 2026-09-26 09:00Z: operator ran export-check in staging at retry=3;
exit 7, queue overflow. No production run. Source synthetic-event:E1.
E2, 2026-09-26 09:10Z: developer proposed retry=10. No owner approval.
Source synthetic-event:E2.
E3, 2026-09-26 09:20Z: owner Mira approved retry=5 only for staging because
retry=10 risks exceeding the memory budget. Operator's export-check then passed
in staging at retry=5. Production validation and rollout remain unknown.
Source synthetic-event:E3. Current config is retry=5, staging only.
No Git case has no repository. Sparse Git has only its initial commit; these
three observations and changed retry setting were never committed.
'''
INITIAL = '''# Context

## Existing decision
Owner Mira approved retry=3 for local checks on 2026-09-01 to bound memory use.
Source: synthetic-owner:D0. Production behavior is unknown.

## Current state
Retry=3; local checks only. No staging result recorded yet.
'''
RULE = '''# Project instructions

Preserve existing decisions and scope. Context is notes/state.md.
Method: context-docs
Adopted: 2026-09-01
Entry point: notes/state.md
'''


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file() and '.git' not in p.parts}


def git(project, *args):
    env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1')
    return subprocess.check_output(['git', '-c', 'core.hooksPath=/dev/null',
         '-c', 'commit.gpgsign=false', '-c', 'user.name=Synthetic Evaluator',
         '-c', 'user.email=eval@example.invalid', *args], cwd=project, env=env,
         text=True, stderr=subprocess.STDOUT)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    scratch = Path(tempfile.mkdtemp(prefix='context-journal-native-'))
    control = scratch / 'control'
    control.mkdir()
    for name in ('bridge.py', 'guard.py'):
        shutil.copy2(HERE / name, control / name)
    shutil.copy2(ROOT / 'tools/event_journal.py', control / 'event_journal.py')
    versions = {client: subprocess.check_output([client, '--version'], text=True).strip()
                for client in ('claude', 'codex')}
    frozen = {'scratch': str(scratch), 'versions': versions,
              'source_hashes': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in [HERE/'protocol.md', HERE/'run.py', HERE/'bridge.py', HERE/'guard.py', ROOT/'tools/event_journal.py']},
              'feed': FEED, 'initial_context': INITIAL, 'initial_instructions': RULE,
              'models': 'client default', 'sessions': 12}
    dump(out / 'frozen.json', frozen)
    shutil.copy2(HERE / 'protocol.md', out / 'protocol.md')
    # Mechanical Git control: committed event survives replacing current state.
    regular = scratch / 'regular-git'
    (regular / 'notes').mkdir(parents=True)
    (regular / 'notes/state.md').write_text(INITIAL)
    git(regular, 'init', '-q'); git(regular, 'add', '.'); git(regular, 'commit', '-qm', 'Initial')
    (regular / 'notes/state.md').write_text(INITIAL + '\nE1: staging retry=3 exit 7 queue overflow.\n')
    git(regular, 'add', '.'); git(regular, 'commit', '-qm', 'Record E1')
    (regular / 'notes/state.md').write_text('Current retry=5, staging only.\n')
    git(regular, 'add', '.'); git(regular, 'commit', '-qm', 'Current state')
    dump(out / 'regular-git-control.json', {'committed_event': git(regular, 'show', 'HEAD~1:notes/state.md'),
         'current_state': (regular / 'notes/state.md').read_text(),
         'passes': 'exit 7' in git(regular, 'show', 'HEAD~1:notes/state.md')})
    trials = []
    for client in ('claude', 'codex'):
        for arm in ('ordinary', 'markdown-log', 'jsonl'):
            label = client + '-' + arm
            workspace = scratch / label
            for case in ('no-git', 'sparse-git'):
                project = workspace / case
                (project / 'notes').mkdir(parents=True)
                (project / 'notes/state.md').write_text(INITIAL)
                (project / 'AGENTS.md').write_text(RULE)
                (project / 'CLAUDE.md').write_text(RULE)
                (project / 'README.md').write_text('# Synthetic project\n\nContext: notes/state.md\n')
                (project / 'settings.json').write_text('{"retry": 3, "scope": "local"}\n')
                if case == 'sparse-git':
                    git(project, 'init', '-q'); git(project, 'add', '.'); git(project, 'commit', '-qm', 'Initial context')
                    # Initial revision predates the change.
                if case == 'no-git':
                    (project / 'settings.json').write_text('{"retry": 5, "scope": "staging"}\n')
                else:
                    (project / 'settings.json').write_text('{"retry": 5, "scope": "staging", "uncommitted": true}\n')
            before = hashes(workspace)
            for phase in ('capture', 'investigate'):
                name = label + '-' + phase
                ro = phase == 'investigate'
                configpath = control / (name + '.json')
                prefix = [sys.executable, str(control / 'bridge.py'), str(configpath)]
                config = {'workspace': str(workspace), 'arm': arm, 'read_only': ro, 'feed': FEED,
                          'helper': str(control/'event_journal.py'), 'prefix': prefix,
                          'helper_calls': str(workspace/'helper-calls.jsonl'), 'hook_log': str(out/(name+'-hooks.jsonl'))}
                dump(configpath, config)
                command = shlex.join(prefix)
                prompt = ('This is a bounded synthetic evaluation. Use ONLY these shell commands: ' + command + ' show; or ' +
                    command + " save '<JSON>'. Each tool call must contain exactly one command, using canonical shlex.join quoting. "
                    'Do not use other tools, shell operators, redirections, network, subagents, or read outside the bridge. '
                    'The bridge show returns all relevant files for both projects. No skills need loading. ')
                if not ro:
                    extra = {'ordinary': 'Keep all useful evidence in notes/state.md; dated history there is allowed.',
                             'markdown-log': 'Use notes/state.md for current state and notes/history.md for event history.',
                             'jsonl': 'Use notes/state.md for current state and events for event history.'}[arm]
                    prompt += ('Maintain BOTH projects from the supplied events, preserving useful evidence for later investigation. ' + extra +
                       ' Keep existing approved decisions, rationale and unknowns. Save separately per case with JSON keys '
                       'case (no-git or sparse-git), context (full Markdown string), history (full Markdown string, empty unless markdown-log), '
                       'events (array, empty unless jsonl). JSONL events require type (verification/decision/context_update/contradiction), '
                       'status (observed/approved/proposed/unknown/superseded), actor, summary, sources (nonempty array), revision (string; '
                       'unavailable for no Git, uncommitted for changed sparse Git). Approved events require authority; verification '
                       'requires check={command,scope,result}. Do not supply generated UUID/time fields. Preserve event times in summaries. '
                       'The helper appends each event and returns its actual execution result. Avoid duplicate saves. '
                       'Do not claim to have executed the authored export checks. Report what was recorded and any failure.')
                else:
                    prompt += ('Audit/investigate BOTH projects read-only, saving nothing. From available records answer these five questions '
                       'for each case, citing file/record locations: 1. What was the original approved setting and why? '
                       '2. What failed before the latest staging change, at which setting, with what exit/result? '
                       '3. Was retry=10 approved, and by whom was it proposed? '
                       '4. Who approved the current setting, why, for what scope, and what check result followed? '
                       '5. What is known about production validation and Git coverage of these events? '
                       'Separate supplied synthetic outcomes from any commands you actually ran; report unavailable history as unknown.')
                (out / (name+'-prompt.txt')).write_text(prompt)
                settings = control / (name+'-settings.json')
                hook = shlex.join([sys.executable, str(control/'guard.py'), str(configpath)]) + ' || exit 2'
                dump(settings, {'hooks': {'PreToolUse': [{'matcher': '*', 'hooks': [{'type': 'command', 'command': hook}]}]}})
                if client == 'claude':
                    cmd = ['claude', '-p', prompt, '--output-format', 'stream-json', '--verbose',
                           '--permission-mode', 'dontAsk', '--setting-sources', 'project', '--strict-mcp-config',
                           '--no-session-persistence', '--tools', 'Bash', '--allowedTools', 'Bash', '--settings', str(settings)]
                else:
                    cmd = ['codex', 'exec', '--ignore-user-config', '--ignore-rules', '--ephemeral',
                           '--skip-git-repo-check', '--sandbox', 'read-only' if ro else 'workspace-write',
                           '--json', '--output-last-message', str(out/(name+'-final.txt')), prompt]
                phase_before = hashes(workspace)
                start = time.monotonic()
                print('START', name, flush=True)
                env = {k:v for k,v in os.environ.items() if not k.startswith('CLAUDE_CODE_')}
                with (out/(name+'-stream.jsonl')).open('w') as stream:
                    try:
                        run = subprocess.run(cmd, cwd=workspace, stdin=subprocess.DEVNULL, stdout=stream,
                             stderr=subprocess.PIPE, text=True, env=env, timeout=300)
                        code, stderr = run.returncode, run.stderr
                    except subprocess.TimeoutExpired:
                        code, stderr = 124, 'Session timed out'
                (out/(name+'-stderr.txt')).write_text(stderr)
                after = hashes(workspace)
                protected = {k:v for k,v in before.items() if not k.endswith('notes/state.md')}
                result = {'name': name, 'exit_code': code, 'seconds': round(time.monotonic()-start, 2),
                          'protected_unchanged': all(after.get(k)==v for k,v in protected.items()),
                          'audit_unchanged': after==phase_before if ro else None,
                          'before': phase_before, 'after': after}
                trials.append(result)
                dump(out/'trials.json', trials)
                shutil.copytree(workspace, out/name, ignore=shutil.ignore_patterns('.git'))
                print('DONE', name, code, result['seconds'], flush=True)
                if code:
                    break
    print('Artifacts:', out, flush=True)


if __name__ == '__main__':
    main()
