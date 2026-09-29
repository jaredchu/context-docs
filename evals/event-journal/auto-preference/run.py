"""Four bounded native sessions; bulky local traces are not published by this runner."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts}


def git(*args):
    subprocess.run(['git', *map(str, args)], check=True, capture_output=True)


def build(out):
    out.mkdir(parents=True, exist_ok=False)
    scratch = Path(tempfile.mkdtemp(prefix='auto-preference-')).resolve()
    frozen = {'root': str(scratch), 'packages': hashes(ROOT / 'skills'),
              'acceptance': 'Only no-git/AGENTS.md gains jsonl with existing directory; all other files preserved. Repeated maintenance after Git initialization and audit of an unconfigured no-Git project make no edits. No event or journal created.',
              'clients': {}}
    for client in ('codex', 'claude'):
        root = scratch / client
        shutil.copytree(ROOT / 'skills', root / 'skills', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        for name in ('no-git', 'off', 'default', 'git-parent/nested', 'broken', 'audit-only'):
            case = root / 'cases' / name
            case.mkdir(parents=True)
            (case / 'README.md').write_text('# Synthetic project\n\n[Current context](context.md).\n')
            (case / 'context.md').write_text('# Current context\n\nSynthetic local utility; manual release review required.\n')
            instructions = ('# Project instructions\n\nUse context-docs for maintenance. Preserve manual release review.\n\nMethod: context-docs\nAdopted: 2026-09-01\nEntry point: context.md\n')
            if name != 'default':
                instructions += 'Context Docs logging preference: auto\n'
            if name == 'off':
                instructions += 'Event journal: off\n'
            if name in ('no-git', 'off'):
                instructions += 'Event journal directory: history/events\n'
                (case / 'history/events').mkdir(parents=True)
                (case / 'history/events/legacy.jsonl').write_text('{"synthetic":"preserve these legacy bytes without reading or migrating"}\n')
            (case / 'AGENTS.md').write_text(instructions)
        git('init', root / 'cases/git-parent')
        git('-C', root / 'cases/git-parent', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '--allow-empty', '-m', 'Fixture')
        git('-C', root / 'cases/git-parent', 'worktree', 'add', '--detach', root / 'cases/worktree')
        for name in ('README.md', 'context.md', 'AGENTS.md'):
            shutil.copy2(root / 'cases/git-parent/nested' / name, root / 'cases/worktree' / name)
        (root / 'cases/broken/.git').write_text('gitdir: missing-directory\n')
        (root / 'AGENTS.md').write_text('# Evaluation workspace\nEach cases/ directory is a separate synthetic project. Use its own instructions. Candidate packages are in skills/. Do not change them.\n')
        (root / 'CLAUDE.md').write_text('@AGENTS.md\n')
        frozen['clients'][client] = {'root': str(root), 'version': subprocess.check_output([client, '--version'], text=True).strip(), 'initial': hashes(root)}
    (out / 'frozen.json').write_text(json.dumps(frozen, indent=2) + '\n')
    shutil.copy2(__file__, out / 'runner.py')
    shutil.copy2(HERE / 'guard.py', out / 'guard.py')
    print(out, flush=True)


def run(out, client):
    frozen = json.loads((out / 'frozen.json').read_text())
    assert frozen['packages'] == hashes(ROOT / 'skills')
    root = Path(frozen['clients'][client]['root'])
    assert hashes(root) == frozen['clients'][client]['initial']
    results = []
    for stage in ('setup', 'repeat-audit'):
        if stage == 'repeat-audit':
            git('init', root / 'cases/no-git')
        stem = out / (client + '-' + stage)
        assert not stem.with_suffix('.jsonl').exists(), 'Never overwrite runs'
        request = ('Apply the candidate adopt-context-docs skill by reading skills/adopt-context-docs/SKILL.md directly. Set up the logging preferences already selected in each project: cases/no-git, cases/off, cases/default, cases/git-parent/nested, cases/worktree, cases/broken. Do not touch cases/audit-only.' if stage == 'setup' else
                   'Read the candidate context-docs skill at skills/context-docs/SKILL.md directly. Maintain cases/no-git after Git was initialized; no new work or facts need recording. Separately audit logging setup in cases/audit-only, read-only. Do not modify the other projects.')
        prompt = request + '\nUse candidate files directly; do not invoke globally installed skills. Each project already has context and an adoption marker. Preserve all existing wording, dates, paths and history. Only edit the relevant project AGENTS.md when setup requires it. No network, commits, delegation, package edits or writes outside this workspace. Shell commands must be individual python3 policy-helper commands with --project and --preference auto, no shell operators. File tools are available for reading/editing. Do not create logs for setup.'
        if client == 'codex':
            prompt = prompt.replace('Shell commands must be individual python3 policy-helper commands with --project and --preference auto, no shell operators. File tools are available for reading/editing.', 'Use read-only shell commands to inspect the fixture and candidate files, apply_patch for permitted instruction edits, and direct python3 policy-helper commands for detection.')
        stem.with_suffix('.prompt.txt').write_text(prompt)
        before = hashes(root)
        if client == 'claude':
            hook = shlex.join(['python3', str(out / 'guard.py'), str(root), str(stem) + '.hooks.jsonl', 'false'])
            settings = Path(str(stem) + '.settings.json')
            settings.write_text(json.dumps({'hooks': {'PreToolUse': [{'matcher': '*', 'hooks': [{'type': 'command', 'command': hook}]}]}}))
            cmd = ['claude', '-p', prompt, '--output-format', 'stream-json', '--verbose', '--permission-mode', 'dontAsk', '--setting-sources', 'project', '--strict-mcp-config', '--no-session-persistence', '--tools', 'Read,Write,Edit,Glob,Grep,Bash', '--allowedTools', 'Read', 'Write', 'Edit', 'Glob', 'Grep', 'Bash', '--settings', str(settings)]
        else:
            cmd = ['codex', 'exec', '--ignore-user-config', '--ephemeral', '--skip-git-repo-check', '--sandbox', 'workspace-write', '--json', '--output-last-message', str(stem) + '.final.txt', prompt]
        env = {k: v for k, v in os.environ.items() if not k.startswith('CLAUDE_CODE_')}
        print('START', client, stage, flush=True)
        with stem.with_suffix('.jsonl').open('w') as stream:
            try:
                p = subprocess.run(cmd, cwd=root, env=env, stdin=subprocess.DEVNULL, stdout=stream, stderr=subprocess.PIPE, text=True, timeout=240)
                code, error = p.returncode, p.stderr
            except subprocess.TimeoutExpired:
                code, error = 124, 'Timeout'
        stem.with_suffix('.stderr.txt').write_text(error)
        rows = [json.loads(line) for line in stem.with_suffix('.jsonl').read_text().splitlines()]
        if client == 'claude':
            Path(str(stem) + '.final.txt').write_text(next((r.get('result', '') for r in reversed(rows) if r.get('type') == 'result'), ''))
        after = hashes(root)
        changed = [k for k in sorted(set(before) | set(after)) if before.get(k) != after.get(k)]
        result = {'stage': stage, 'exit_code': code, 'changed': changed,
                  'terminal': any(r.get('type') == ('result' if client == 'claude' else 'turn.completed') for r in rows),
                  'instructions': {str(p.relative_to(root)): p.read_text() for p in (root / 'cases').rglob('AGENTS.md')}}
        results.append(result)
        (out / (client + '-summary.json')).write_text(json.dumps(results, indent=2) + '\n')
        print(client, stage, 'exit', code, 'changed', changed, flush=True)
        if code != 0 or not result['terminal']:
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('build', 'run'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--client', choices=('codex', 'claude'))
    args = parser.parse_args()
    if args.mode == 'build':
        build(args.output.resolve())
    else:
        run(args.output.resolve(), args.client)
