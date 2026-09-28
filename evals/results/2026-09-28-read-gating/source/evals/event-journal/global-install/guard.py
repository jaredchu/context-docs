"""Reuse integration controls, permitting reads of the two installed global skills."""
import importlib.util
from pathlib import Path
import sys

spec = importlib.util.spec_from_file_location('integration_guard', Path(__file__).resolve().parents[1] / 'integration/guard.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)
original = guard.decision


def decision(event, config):
    if event.get('tool_name') == 'Read':
        value = (event.get('tool_input') or {}).get('file_path')
        if isinstance(value, str):
            path = guard.resolve(value, Path(config['project']))
            if any(guard.inside(path, Path(root).resolve()) for root in config['skill_roots']):
                return True
    return original(event, config)


if __name__ == '__main__':
    guard.decision = decision
    guard.main()
