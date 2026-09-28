"""Exact bridge-command gate for native Claude; evaluation only, not OS sandbox."""
import json
from pathlib import Path
import shlex
import sys


def allowed(event, config):
    if event.get('tool_name') != 'Bash':
        return False
    command = event.get('tool_input', {}).get('command', '')
    try:
        parts = shlex.split(command)
    except ValueError:
        return False
    # Canonical shell quoting ensures $, backticks, redirects and separators
    # cannot become shell syntax, even when contained in a JSON argument.
    if command != shlex.join(parts) or parts[:3] != config['prefix']:
        return False
    if len(parts) == 4 and parts[3] == 'show':
        return True
    if len(parts) == 5 and parts[3] == 'save' and not config['read_only']:
        try:
            return isinstance(json.loads(parts[4]), dict)
        except ValueError:
            pass
    return False


if __name__ == '__main__':
    try:
        config = json.loads(Path(sys.argv[1]).read_text())
        event = json.load(sys.stdin)
        verdict = allowed(event, config)
        with Path(config['hook_log']).open('a') as stream:
            stream.write(json.dumps({'event': event, 'allowed': verdict}) + '\n')
        print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse',
              'permissionDecision': 'allow' if verdict else 'deny',
              'permissionDecisionReason': 'Frozen evaluation bridge only; use canonical shlex quoting.'}}))
    except Exception:
        sys.exit(2)
