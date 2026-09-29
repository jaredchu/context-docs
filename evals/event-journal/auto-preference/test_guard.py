"""Check native evaluator command and write boundaries before interpreting runs."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('auto_guard', Path(__file__).with_name('guard.py'))
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class GuardTests(unittest.TestCase):
    def test_policy_command_and_write_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            command = f'python3 {root}/skills/context-docs/scripts/journal_policy.py --project {root}/cases/example --preference auto'
            event = lambda text: {'tool_name': 'Bash', 'tool_input': {'command': text}}
            self.assertTrue(guard.allowed(event(command), root, False))
            self.assertFalse(guard.allowed(event(command + '; touch escaped'), root, False))
            self.assertFalse(guard.allowed(event(command.replace(str(root) + '/cases/example', '/tmp')), root, False))
            self.assertFalse(guard.allowed(event(command.replace('journal_policy.py', 'event_journal.py')), root, False))
            write = {'tool_name': 'Write', 'tool_input': {'file_path': str(root / 'cases/example/AGENTS.md')}}
            self.assertTrue(guard.allowed(write, root, False))
            self.assertFalse(guard.allowed(write, root, True))
            write['tool_input']['file_path'] = str(root / 'skills/context-docs/SKILL.md')
            self.assertFalse(guard.allowed(write, root, False))
            write['tool_input']['file_path'] = str(root / '../AGENTS.md')
            self.assertFalse(guard.allowed(write, root, False))


if __name__ == '__main__':
    unittest.main()
