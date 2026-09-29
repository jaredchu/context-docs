"""Bounded native evaluation: read fixture files, edit instructions, run policy only."""
import json
from pathlib import Path
import shlex
import sys


def allowed(event, root, readonly):
    data = event.get('tool_input', {})
    name = event.get('tool_name')
    if name == 'Bash':
        command = data.get('command', '')
        if any(c in command for c in ';&|<>\n`$\\\r*?'):
            return False
        parts = shlex.split(command)
        if len(parts) != 6 or parts[0] != 'python3':
            return False
        script = Path(parts[1])
        script = (root / script).resolve()
        return (script == root / 'skills/context-docs/scripts/journal_policy.py'
                and parts[2] == '--project' and parts[4:] == ['--preference', 'auto']
                and (root / parts[3]).resolve().is_relative_to(root))
    if name not in ('Read', 'Edit', 'Write', 'Glob', 'Grep'):
        return False
    value = data.get('file_path', data.get('path', str(root)))
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        return False
    if name in ('Edit', 'Write'):
        return not readonly and path.name == 'AGENTS.md' and 'cases' in path.relative_to(root).parts
    return True


if __name__ == '__main__':
    root, log, readonly = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), sys.argv[3] == 'true'
    event = json.load(sys.stdin)
    try:
        ok = allowed(event, root, readonly)
    except (ValueError, TypeError):
        ok = False
    with log.open('a') as stream:
        stream.write(json.dumps({'tool': event.get('tool_name'), 'input': event.get('tool_input'), 'allowed': ok}) + '\n')
    print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse',
          'permissionDecision': 'allow' if ok else 'deny',
          'permissionDecisionReason': 'Fixture-only reads/instruction edits and direct policy-helper commands.'}}))
