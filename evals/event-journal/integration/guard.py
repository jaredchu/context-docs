"""Evaluation-only Claude file/command policy; no execution bridge or OS sandbox."""
import argparse
import fcntl
import hashlib
import json
from pathlib import Path
import re
import shlex
import sys

TOOLS = ('Read', 'Write', 'Edit', 'Glob', 'Grep', 'Skill', 'Bash')


def inside(path, root):
    return path == root or root in path.parents


def resolve(value, root):
    path = Path(value)
    return (path if path.is_absolute() else root/path).resolve()


def shell_allowed(command, config):
    root = Path(config['project']).resolve()
    if not isinstance(command, str) or any(c in command for c in ';&|<>\n`$\\\r*?'):
        return False
    try:
        parts = shlex.split(command)
    except ValueError:
        return False
    if not parts:
        return False
    if parts in (['pwd'], ['ls'], ['ls', '-la'], ['python3', '--version']):
        return True
    git_reads = [['status', '--short'], ['status', '--porcelain'], ['diff'], ['diff', '--stat'],
                 ['diff', '--check'], ['log', '-1', '--oneline'], ['rev-parse', 'HEAD'],
                 ['rev-parse', '--show-toplevel'], ['rev-parse', '--is-inside-work-tree']]
    if parts[0] == 'git':
        return parts[1:] in git_reads
    if len(parts) < 2 or parts[0] not in ('python3', config['python']):
        return False
    script = resolve(parts[1], root)
    if script == root/'checks/probe.py':
        return len(parts) == 2 and not config['read_only']
    if script != root/config['helper']:
        return False
    args = parts[2:]
    if args == ['--help']:
        return True
    directory = root/'.context/events'
    if len(args) >= 2 and args[0] == '--directory':
        directory = resolve(args[1], root)
        args = args[2:]
    if not inside(directory, root) or any(x in directory.relative_to(root).parts for x in ('.git', '.claude', '.agents')):
        return False
    if not args or args[0] not in ('append', 'read'):
        return False
    action, rest = args[0], args[1:]
    if action == 'append' and config['read_only']:
        return False
    if len(rest) % 2:
        return False
    opts = dict(zip(rest[::2], rest[1::2]))
    if len(opts) != len(rest)//2 or set(opts) - ({'--session','--input'} if action=='append' else {'--session','--type'}):
        return False
    if '--session' in opts and not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}',opts['--session']):
        return False
    if '--type' in opts and opts['--type'] not in ('verification','decision','contradiction','context_update'):
        return False
    if action == 'append':
        if not {'--session','--input'} <= set(opts):
            return False
        source = resolve(opts['--input'],root)
        if not inside(source,root) or source.suffix != '.json':
            return False
    return True


def decision(event, config):
    root = Path(config['project']).resolve()
    name = event.get('tool_name')
    data = event.get('tool_input') or {}
    if name == 'Bash':
        return shell_allowed(data.get('command'),config)
    if name == 'Skill':
        return data.get('skill') in ('context-docs','adopt-context-docs')
    if name not in TOOLS:
        return False
    value = data.get('file_path') if name in ('Read','Write','Edit') else data.get('path',str(root))
    if not isinstance(value,str) or not value:
        return False
    path = resolve(value,root)
    if not inside(path,root):
        return False
    if name == 'Glob':
        pattern = data.get('pattern','')
        if Path(pattern).is_absolute() or '..' in Path(pattern).parts:
            return False
    if name in ('Write','Edit'):
        relative = str(path.relative_to(root))
        if config['read_only'] or relative in config['immutable']:
            return False
        if relative.split('/')[0] in ('.git','.claude','.agents') or path.suffix not in ('.md','.json'):
            return False
        if path.exists() and (not path.is_file() or path.stat().st_nlink > 1):
            return False
    return True


def main():
    try:
        config = json.loads(Path(sys.argv[1]).read_text())
        event = json.load(sys.stdin)
        record = {k:event[k] for k in ('hook_event_name','tool_name','tool_input','tool_use_id',
                  'file_path','memory_type','load_reason','session_id') if k in event}
        output = None
        if event['hook_event_name'] == 'InstructionsLoaded':
            path = Path(event['file_path'])
            record['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        if event['hook_event_name'] == 'PreToolUse':
            allowed = decision(event,config)
            record['allowed'] = allowed
            output = {'hookSpecificOutput': {'hookEventName':'PreToolUse',
                      'permissionDecision':'allow' if allowed else 'deny',
                      'permissionDecisionReason':'Evaluation policy: project file tools; installed journal CLI with --input JSON; fixture probe; simple read-only Git commands. No shell operators or out-of-project writes.'}}
        with Path(config['log']).open('a') as stream:
            fcntl.flock(stream.fileno(),fcntl.LOCK_EX)
            stream.write(json.dumps(record)+'\n')
        if output:
            print(json.dumps(output))
    except Exception:
        sys.exit(2)


if __name__=='__main__':
    main()
