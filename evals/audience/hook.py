"""Small destination restriction around the existing evaluation file-tool guard."""
from pathlib import Path
import guard_hook

base_decision = guard_hook.decision


def writable(name, config):
    return name.endswith('.md') and name not in config.get('immutable', []) and any(
        name.startswith(p) if p.endswith('/') else name == p for p in config['writable'])


def decision(event, config):
    verdict, reason = base_decision(event, config)
    if verdict == 'allow' and event['tool_name'] in ('Write', 'Edit'):
        root = Path(config['project']).resolve()
        path = Path(event['tool_input']['file_path'])
        relative = str((root / path).resolve().relative_to(root))
        if not writable(relative, config):
            return 'deny', 'Only the explicitly authorized Markdown destinations may be edited.'
    return verdict, reason


if __name__ == '__main__':
    guard_hook.decision = decision
    guard_hook.main()
