"""Reuse native evaluation observation; authorize only this pilot's code/test scope."""
from pathlib import Path
import guard_hook

TOOLS = ('Read', 'Write', 'Edit', 'Glob', 'Grep', 'Bash')

def decision(event, config):
    name, payload = event['tool_name'], event.get('tool_input') or {}
    if name == 'Bash':
        if payload.get('command') == 'python3 -m unittest discover -s tests -v':
            return 'allow', 'Only the fixed local fixture test command.'
        return 'deny', 'Only python3 -m unittest discover -s tests -v is authorized.'
    if name not in TOOLS:
        return 'deny', 'Tool outside frozen pilot set.'
    root = Path(config['project']).resolve()
    value = payload.get('file_path') if name in ('Read', 'Write', 'Edit') else payload.get('path', str(root))
    if not isinstance(value, str) or not value:
        return 'deny', 'Missing path.'
    path = (root / value).resolve()
    if not guard_hook.within(path, root):
        return 'deny', 'Outside fixture.'
    if name == 'Glob' and (Path(payload.get('pattern', '')).is_absolute() or '..' in Path(payload.get('pattern', '')).parts):
        return 'deny', 'Glob escapes fixture.'
    if name in ('Write', 'Edit') and str(path.relative_to(root)) not in config['writable']:
        return 'deny', 'Only frozen editable scope.'
    return 'allow', 'Within frozen pilot scope.'

if __name__ == '__main__':
    guard_hook.decision = decision
    guard_hook.main()
