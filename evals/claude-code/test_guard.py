"""No credentials: boundary attacks and native observer schema controls."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import guard_hook as guard
import guarded


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base/'project'
        self.root.mkdir()
        self.config = dict(project=str(self.root), immutable=['locked.md'],
                           events=str(self.base/'events.jsonl'))

    def verdict(self, name='Write', **payload):
        return guard.decision(dict(tool_name=name, tool_input=payload), self.config)[0]

    def test_normal_markdown_allowed_but_outside_and_traversal_denied(self):
        self.assertEqual(self.verdict(file_path='docs/new.md'), 'allow')
        self.assertEqual(self.verdict(file_path=str(self.base/'outside.md')), 'deny')
        self.assertEqual(self.verdict(file_path='../outside.md'), 'deny')
        self.assertEqual(self.verdict(file_path=str(self.base/'project-other/new.md')), 'deny')

    def test_symlink_escape_and_hardlink_are_denied(self):
        (self.root/'escape').symlink_to(self.base, target_is_directory=True)
        self.assertEqual(self.verdict(file_path='escape/outside.md'), 'deny')
        outside = self.base/'linked.md'
        outside.write_text('original')
        import os
        os.link(outside, self.root/'linked.md')
        self.assertEqual(self.verdict(file_path='linked.md'), 'deny')

    def test_installation_immutable_and_read_only_are_protected(self):
        for path in ['locked.md', '.claude/settings.md', '.git/config.md', 'run.py']:
            self.assertEqual(self.verdict(file_path=path), 'deny', path)
        self.config['read_only'] = True
        self.assertEqual(self.verdict(file_path='README.md'), 'deny')
        self.assertEqual(self.verdict('Read', file_path='README.md'), 'allow')

    def test_unexposed_tools_and_unknown_skills_are_denied(self):
        for name in ['Bash', 'Agent', 'NotebookEdit', 'WebFetch', 'ToolSearch']:
            self.assertEqual(self.verdict(name), 'deny')
        self.assertEqual(self.verdict('Skill', skill='unknown'), 'deny')
        self.assertEqual(self.verdict('Skill', skill='context-docs'), 'allow')
        self.assertEqual(self.verdict('Glob', pattern='../*'), 'deny')

    def test_loading_event_records_reason_and_hash_without_injecting_context(self):
        path = self.root/'CLAUDE.md'
        path.write_text('Synthetic instructions.\n')
        output = guard.handle(dict(hook_event_name='InstructionsLoaded', file_path=str(path),
                                  memory_type='Project', load_reason='session_start'), self.config)
        self.assertIsNone(output)
        event = json.loads(Path(self.config['events']).read_text())
        self.assertEqual(event['load_reason'], 'session_start')
        self.assertEqual(len(event['file_sha256_at_event']), 64)
        self.assertNotIn('Synthetic instructions', str(event))

    def test_invalid_input_exits_two_instead_of_failing_open(self):
        config = self.base/'config.json'
        config.write_text(json.dumps(self.config))
        result = subprocess.run([sys.executable, str(Path(guard.__file__)), str(config)],
                                input='not JSON', text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')

    def test_coverage_rejects_unobserved_or_successful_denied_tools(self):
        log=self.base/'stream.jsonl'
        events=[dict(type='system',subtype='init',tools=['Write']),
                dict(type='assistant',message=dict(content=[dict(type='tool_use',id='call-1',name='Write')])),
                dict(type='user',message=dict(content=[dict(type='tool_result',tool_use_id='call-1',is_error=False)]))]
        log.write_text('\n'.join(json.dumps(e) for e in events)+'\n')
        self.assertFalse(guarded.coverage(log,[],guard.TOOLS)['all_tool_calls_guarded'])
        hook=[dict(hook_event_name='PreToolUse',tool_use_id='call-1',decision='deny')]
        self.assertFalse(guarded.coverage(log,hook,guard.TOOLS)['no_successful_denied_tool'])
        hook[0]['decision']='allow'
        self.assertTrue(all(guarded.coverage(log,hook,guard.TOOLS).values()))
        events[0]['tools'].append('Bash')
        log.write_text('\n'.join(json.dumps(e) for e in events)+'\n')
        self.assertFalse(guarded.coverage(log,hook,guard.TOOLS)['tool_catalog_restricted'])


if __name__ == '__main__':
    unittest.main()
