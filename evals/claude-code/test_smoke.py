"""Credential-free regression tests for frozen native-client evaluations."""
import contextlib
import copy
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

module_spec = importlib.util.spec_from_file_location('native_smoke', Path(__file__).with_name('smoke.py'))
smoke = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(smoke)


class SmokeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.destination = Path(self.temp.name) / 'run'
        self.audit = copy.deepcopy(next(t for t in smoke.trajectories() if t['id'] == 'audit-only'))
        original_run = subprocess.run

        def local_run(command, **kwargs):
            if command == ['claude', '--version']:
                return subprocess.CompletedProcess(command, 0, stdout='fixture-cli-version')
            return original_run(command, **kwargs)

        with patch.object(smoke, 'trajectories', return_value=[self.audit]), \
                patch.object(smoke.subprocess, 'run', side_effect=local_run), \
                contextlib.redirect_stdout(io.StringIO()):
            smoke.build(self.destination, 'frozen-model')
        self.project = self.destination / 'projects/audit-only'

    def run_fake(self, mutation=None):
        def session(project, prompt, log, protocol):
            if mutation:
                mutation(project)
            log.write_text(json.dumps({'type': 'result', 'is_error': False,
                                       'result': 'Audit complete.'}) + '\n')
            return dict(exit_code=0, stderr='', seconds=0)

        with patch.object(smoke, 'run_session', side_effect=session) as called, \
                contextlib.redirect_stdout(io.StringIO()):
            smoke.run(self.destination)
        return called, json.loads((self.destination / 'trials.json').read_text())[0]['steps'][0]

    def test_run_uses_frozen_prompt_model_criteria_and_installation(self):
        with patch.object(smoke, 'trajectories', side_effect=AssertionError('live fixtures used')), \
                patch.object(smoke, 'installed_files', side_effect=AssertionError('live skills used')):
            called, step = self.run_fake()
        args = called.call_args.args
        self.assertEqual(args[1], self.audit['steps'][0]['prompt'])
        self.assertEqual(args[3]['model'], 'frozen-model')
        self.assertEqual(step['rubric'], self.audit['steps'][0]['rubric'])
        self.assertTrue(step['mechanical_pass'])

    def test_conflicting_model_rejected_before_execution(self):
        with patch.object(smoke, 'run_session') as called, self.assertRaisesRegex(SystemExit, 'Model differs'):
            smoke.run(self.destination, 'different-model')
        called.assert_not_called()

    def test_changed_input_rejected_before_execution(self):
        (self.project / 'README.md').write_text('Changed after freeze.\n')
        with patch.object(smoke, 'run_session') as called, self.assertRaisesRegex(SystemExit, 'Inputs differ'):
            smoke.run(self.destination)
        called.assert_not_called()

    def test_old_protocol_rejected(self):
        path = self.destination / 'protocol.json'
        protocol = json.loads(path.read_text())
        del protocol['schema_version']
        path.write_text(json.dumps(protocol))
        with patch.object(smoke, 'run_session') as called, self.assertRaisesRegex(SystemExit, 'frozen inputs'):
            smoke.run(self.destination)
        called.assert_not_called()

    def test_added_claude_rule_fails_read_only_check(self):
        def mutation(project):
            path = project / '.claude/rules/injected.md'
            path.parent.mkdir()
            path.write_text('Unrequested rule.\n')
        _, step = self.run_fake(mutation)
        self.assertFalse(step['checks']['project_byte_identical'])
        self.assertFalse(step['mechanical_pass'])
        self.assertIn('.claude/rules/injected.md', step['tree_after'])

    def test_newline_only_byte_change_fails_read_only_check(self):
        def mutation(project):
            path = project / 'README.md'
            path.write_bytes(path.read_bytes().replace(b'\n', b'\r\n'))
        _, step = self.run_fake(mutation)
        self.assertFalse(step['checks']['project_byte_identical'])

    def test_absolute_and_relative_links_require_declared_unchanged_target(self):
        before = smoke.snapshot(self.project)
        spec = smoke.spec_for(self.audit['case'], before, self.audit['steps'][0])
        target = self.project / smoke.INSTALL / 'context-docs/SKILL.md'
        for destination in (str(target), str(target.relative_to(self.project))):
            (self.project / 'link.md').write_text(f'[Skill]({destination})\n')
            self.assertTrue(smoke.grade(spec, self.project, self.destination, before)['mechanical_pass'])
        (self.project / 'link.md').write_text(f'[Skill]({target})\n')
        target.write_text('tampered\n')
        self.assertFalse(smoke.grade(spec, self.project, self.destination, before)['mechanical_pass'])
        target.unlink()
        self.assertFalse(smoke.grade(spec, self.project, self.destination, before)['mechanical_pass'])
        (self.project / 'link.md').write_text(f'[Missing]({target.parent / "absent.md"})\n')
        self.assertFalse(smoke.grade(spec, self.project, self.destination, before)['checks']['local_links_and_anchors'])

    def test_cli_receives_frozen_settings(self):
        protocol = json.loads((self.destination / 'protocol.json').read_text())
        protocol['allowed_tools'] = ['Read']
        with patch.object(smoke.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, stderr='')) as called:
            smoke.run_session(self.project, 'frozen request', self.destination / 'log.jsonl', protocol)
        command = called.call_args.args[0]
        self.assertEqual(command[command.index('--model') + 1], 'frozen-model')
        self.assertEqual(command[command.index('--allowedTools') + 1], 'Read')
        self.assertNotIn('Edit', command)
        # Claude -p appends piped stdin to the prompt. A heredoc used to launch
        # this harness must never become part of the frozen model request.
        self.assertEqual(called.call_args.kwargs['stdin'], subprocess.DEVNULL)

    def test_execution_failure_is_saved_and_stops_remaining_sessions(self):
        path = self.destination / 'protocol.json'
        protocol = json.loads(path.read_text())
        protocol['trajectories'][0]['steps'] *= 2
        path.write_text(json.dumps(protocol))

        def session(project, prompt, log, protocol):
            log.write_text(json.dumps({'type': 'result', 'is_error': True,
                                       'result': 'Authentication failed.'}) + '\n')
            return dict(exit_code=1, stderr='', seconds=0)

        with patch.object(smoke, 'run_session', side_effect=session) as called, \
                contextlib.redirect_stdout(io.StringIO()):
            smoke.run(self.destination)
        self.assertEqual(called.call_count, 1)
        steps = json.loads((self.destination / 'trials.json').read_text())[0]['steps']
        self.assertEqual(len(steps), 1)
        self.assertFalse(steps[0]['checks']['no_execution_error'])

    def test_incomplete_stream_is_execution_error(self):
        path = self.destination / 'incomplete.jsonl'
        path.write_text(json.dumps(smoke.POSITIVE_STREAM[0]) + '\n')
        self.assertEqual(smoke.parse_stream(path)['execution_error'], 'missing_terminal_result')

    def test_permission_event_with_text_message_is_retained_as_failure(self):
        path = self.destination / 'denial.jsonl'
        events = [{'type': 'system', 'subtype': 'permission_denied',
                   'message': 'This command needs approval.'},
                  {'type': 'result', 'is_error': False, 'result': 'Audit complete.'}]
        path.write_text('\n'.join(json.dumps(e) for e in events) + '\n')
        parsed = smoke.parse_stream(path)
        self.assertEqual(parsed['execution_error'], 'permission_denied')
        self.assertEqual(parsed['final_message'], 'Audit complete.')

    def test_unknown_followup_trajectory_rejected_before_creating_files(self):
        destination = self.destination / 'bad-selection'
        with self.assertRaisesRegex(SystemExit, 'trajectory selection'):
            smoke.build(destination, 'frozen-model', ['does-not-exist'])
        self.assertFalse(destination.exists())


if __name__ == '__main__':
    unittest.main()
