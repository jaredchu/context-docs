import json
from pathlib import Path
import shlex
import tempfile
import unittest

import bridge
import guard


class Boundary(unittest.TestCase):
    def setUp(self):
        self.config = {'prefix': ['/usr/bin/python3', '/control/bridge.py', '/control/config.json'], 'read_only': False}

    def event(self, args):
        return {'tool_name': 'Bash', 'tool_input': {'command': shlex.join(self.config['prefix'] + args)}}

    def test_allowed(self):
        self.assertTrue(guard.allowed(self.event(['show']), self.config))
        self.assertTrue(guard.allowed(self.event(['save', json.dumps({'context': "literal $(touch /tmp/no) `pwd` ' & ;"})]), self.config))

    def test_shell_injection(self):
        for suffix in ('; touch /tmp/no', ' && pwd', ' > /tmp/no', '\nwhoami', ' &'):
            event = self.event(['show'])
            event['tool_input']['command'] += suffix
            self.assertFalse(guard.allowed(event, self.config))
        event = self.event(['show'])
        event['tool_input']['command'] = 'python3 -c "print(1)"'
        self.assertFalse(guard.allowed(event, self.config))

    def test_read_only_and_other_tools(self):
        self.config['read_only'] = True
        self.assertFalse(guard.allowed(self.event(['save', '{}']), self.config))
        self.assertTrue(guard.allowed(self.event(['show']), self.config))
        self.assertFalse(guard.allowed({'tool_name': 'Write'}, self.config))

    def test_invalid_payload(self):
        self.assertFalse(guard.allowed(self.event(['save', 'oops']), self.config))
        self.assertFalse(guard.allowed(self.event(['save', '[]']), self.config))

    def test_bridge_rejects_audit_write(self):
        with tempfile.TemporaryDirectory() as temp:
            config = {'workspace': temp, 'read_only': True}
            with self.assertRaises(ValueError):
                bridge.execute(config, 'save', {})
            self.assertEqual(list(Path(temp).iterdir()), [])

    def test_bridge_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            config = {'workspace': temp, 'read_only': False}
            with self.assertRaises(ValueError):
                bridge.execute(config, 'save', {'case': '../escape', 'context': '', 'history': '', 'events': []})
            self.assertEqual(list(Path(temp).iterdir()), [])


if __name__ == '__main__':
    unittest.main()
