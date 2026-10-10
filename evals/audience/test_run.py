import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))
import run
import hook


class Controls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)
        self.project = self.root / 'projects' / 'audit'; self.project.mkdir(parents=True)
        self.config = dict(project=str(self.project), immutable=['source.md'], writable=['docs/'], read_only=False)

    def tearDown(self): self.temp.cleanup()

    def event(self, name, **payload):
        return dict(hook_event_name='PreToolUse', tool_use_id='one', tool_name=name, tool_input=payload, decision='allow')

    def test_authorized_destinations_and_boundary(self):
        for name, expected in [('docs/new.md', 'allow'), ('other/new.md', 'deny'), ('docs/data.txt', 'deny'), ('../escape.md', 'deny'), ('source.md', 'deny'), ('.claude/skills/x.md', 'deny')]:
            self.assertEqual(hook.decision(self.event('Write', file_path=name), self.config)[0], expected, name)

    def test_audit_read_allowed_write_denied(self):
        config = {**self.config, 'read_only': True}
        self.assertEqual(hook.decision(self.event('Read', file_path='history/events/old.jsonl'), config)[0], 'allow')
        self.assertEqual(hook.decision(self.event('Write', file_path='docs/new.md'), config)[0], 'deny')

    def test_protected_public_report(self):
        case = run.CASES[0]
        self.assertFalse(hook.writable('reports/portability.md', dict(writable=case['writable'], immutable=case['protected'])))
        self.assertTrue(hook.writable('reports/summary.md', dict(writable=case['writable'], immutable=case['protected'])))

    def test_byte_drift_detects_newline_change(self):
        file = self.project / 'a.md'; file.write_bytes(b'one\r\ntwo\r\n')
        p = dict(initial_hashes={'audit': run.hashes(run.snapshot(self.project))})
        run.preflight(self.root, p, {'id': 'audit'})
        file.write_bytes(b'one\ntwo\n')
        with self.assertRaisesRegex(ValueError, 'Fixture drift'): run.preflight(self.root, p, {'id': 'audit'})

    def test_core_provenance_not_adoption(self):
        log = self.root / 'stream.jsonl'; body = '---\nname: context-docs\n---\nCore body.'
        def write(skill):
            log.write_text(json.dumps(dict(type='user', message=dict(content=[dict(type='text', text='Base directory for this skill: ' + str(self.project / '.claude/skills' / skill) + '\nCore body.')]))))
        write('adopt-context-docs'); self.assertFalse(run.provenance(log, self.project, body))
        write('context-docs'); self.assertTrue(run.provenance(log, self.project, body))

    def trajectory(self, event, result, is_error=False):
        log = self.root / 'stream.jsonl'
        log.write_text(json.dumps(dict(type='user', message=dict(content=[dict(type='tool_result', tool_use_id='one', content=result, is_error=is_error)]))))
        return run.trajectory(log, [event], self.project, {'journal': 'history/events/old.jsonl'}, self.root)[0]

    def test_scan_scope_is_not_filename_exposure(self):
        e = self.event('Glob', path=str(self.project), pattern='**/*.md')
        t = self.trajectory(e, 'README.md\ncontext.md')
        self.assertTrue(t['journal_scan_candidate']); self.assertFalse(t['journal_filename_returned'])
        self.assertFalse(t['journal_content_returned'])
        t = self.trajectory(e, 'history/events/old.jsonl')
        self.assertTrue(t['journal_filename_returned']); self.assertFalse(t['journal_content_returned'])

    def test_journal_read_and_denied_write_separate(self):
        t = self.trajectory(self.event('Read', file_path=str(self.project / 'history/events/old.jsonl')), '{"summary":"failure"}')
        self.assertTrue(t['journal_read_attempt']); self.assertTrue(t['journal_content_returned'])
        e = self.event('Write', file_path='context.md'); e['decision'] = 'deny'
        t = self.trajectory(e, 'blocked')
        self.assertTrue(t['write_attempt']); self.assertEqual(t['decision'], 'deny')

    def test_root_grep_attributes_journal_content(self):
        e = self.event('Grep', path=str(self.project), pattern='failure', output_mode='content')
        t = self.trajectory(e, 'history/events/old.jsonl:1:{"summary":"failure"}')
        self.assertTrue(t['journal_scan_candidate']); self.assertTrue(t['journal_filename_returned'])
        self.assertTrue(t['journal_content_returned']); self.assertFalse(t['journal_read_attempt'])
        t = self.trajectory(e, 'context.md:1:Evidence is history/events/old.jsonl')
        self.assertTrue(t['journal_filename_returned']); self.assertFalse(t['journal_content_returned'])

    def test_targeted_grep_content_and_no_match(self):
        e = self.event('Grep', path=str(self.project / 'history/events/old.jsonl'), pattern='failure', output_mode='content')
        t = self.trajectory(e, '1:{"summary":"failure"}')
        self.assertTrue(t['journal_content_returned']); self.assertFalse(t['journal_filename_returned'])
        for text in ('', 'No matches found'):
            self.assertFalse(self.trajectory(e, text)['journal_content_returned'])
        self.assertFalse(self.trajectory(e, 'Tool failed', is_error=True)['journal_content_returned'])
        e['decision'] = 'deny'
        self.assertFalse(self.trajectory(e, 'blocked')['journal_content_returned'])

    def test_filename_only_grep_is_not_content(self):
        for mode in (None, 'files_with_matches', 'count'):
            payload = dict(path=str(self.project), pattern='failure')
            if mode: payload['output_mode'] = mode
            t = self.trajectory(self.event('Grep', **payload), 'history/events/old.jsonl')
            self.assertTrue(t['journal_filename_returned']); self.assertFalse(t['journal_content_returned'])
        e = self.event('Grep', path=str(self.project), pattern='failure', output_mode='content')
        self.assertFalse(self.trajectory(e, 'history/events/old.jsonl')['journal_content_returned'])

    def test_denied_write_with_passing_coverage_does_not_stop(self):
        event = self.event('Write', file_path='context.md'); event['decision'] = 'deny'
        log = self.root / 'coverage.jsonl'
        stream = [dict(type='system', subtype='init', tools=list(run.guard_hook.TOOLS)),
                  dict(type='assistant', message=dict(content=[dict(type='tool_use', id='one', name='Write', input=event['tool_input'])])),
                  dict(type='user', message=dict(content=[dict(type='tool_result', tool_use_id='one', content='Denied', is_error=True)]))]
        log.write_text('\n'.join(json.dumps(e) for e in stream))
        checks = run.guarded.coverage(log, [event], run.guard_hook.TOOLS)
        self.assertTrue(all(checks.values()), checks)
        self.assertFalse(run.should_stop(checks, 'permission_denied'))
        self.assertTrue(run.trajectory(log, [event], self.project, {}, self.root)[0]['write_attempt'])
        stream[-1]['message']['content'][0]['is_error'] = False
        log.write_text('\n'.join(json.dumps(e) for e in stream))
        checks = run.guarded.coverage(log, [event], run.guard_hook.TOOLS)
        self.assertTrue(run.should_stop(checks, None))

    def test_missing_explicit_core_invocation_stops(self):
        self.assertTrue(run.should_stop(dict(core_skill_called=False, core_skill_delivered=True), None))
        self.assertTrue(run.should_stop(dict(core_skill_called=True, core_skill_delivered=False), None))

    def test_export_allowlist_omits_host_inventory(self):
        p = {k: {} for k in ('kind', 'build_id', 'built_at', 'package_commit', 'package_versions', 'model', 'requested_effort', 'effort_observed', 'cli_version', 'auto_memory_enabled', 'general_rubric', 'harness_hashes')}
        p.update(cases=run.CASES, configurations={'secret': 'HOST-INVENTORY'}, runtime_home='HOST-INVENTORY',
                 build_id='unique-build-id', built_at='2026-10-10T00:00:00+00:00')
        (self.root / 'protocol.json').write_text('{}')
        t = dict(id='audit', execution_checks={}, model_evidence={}, final_message='See ' + str(self.project),
                 before={'context.md': '/Users/synthetic/path', '.claude/settings.json': 'HOST-INVENTORY'}, after={}, trajectory=[],
                 events=[{'session_id': 'HOST-INVENTORY'}], execution_error=None,
                 execution={'stderr': 'HOST-INVENTORY', 'exit_code': 0, 'seconds': 1})
        data = run.export_data(p, [t], self.root)
        out = json.dumps(data)
        self.assertNotIn('HOST-INVENTORY', out); self.assertNotIn(str(self.root), out)
        self.assertIn('/Users/synthetic/path', out)
        self.assertEqual(data['build_id'], p['build_id']); self.assertEqual(data['built_at'], p['built_at'])
        self.assertEqual(data['cases'][0]['protected'], ['reports/portability.md'])
        self.assertEqual(data['cases'][0]['writable'], ['docs/', 'reports/'])
        self.assertTrue(data['cases'][-1]['audit'])
        self.assertEqual(data['cases'][-1]['journal'], 'history/events/old.jsonl')

    def test_export_normalizes_equivalent_macos_temporary_alias(self):
        root = Path('/private/tmp/audience-control')
        self.assertEqual(run.clean('/tmp/audience-control/projects/audit/context.md', root),
                         '/fixture/projects/audit/context.md')

    def test_ancestor_instructions_rejected_before_build(self):
        (self.root / 'CLAUDE.md').write_text('Unrelated ancestor instructions.')
        with patch.object(run.subprocess, 'check_output') as external:
            with self.assertRaisesRegex(ValueError, 'Ancestor instruction'):
                run.build(self.root / 'new-runtime')
            external.assert_not_called()

    def test_ancestor_rules_rejected_before_build(self):
        (self.root / '.claude/rules').mkdir(parents=True)
        with patch.object(run.subprocess, 'check_output') as external:
            with self.assertRaisesRegex(ValueError, 'Ancestor instruction'):
                run.build(self.root / 'new-runtime')
            external.assert_not_called()

    def test_build_disables_auto_memory_and_records_unique_identity(self):
        paths = ['skills/' + name + '/VERSION' for name in run.smoke.SKILLS]
        def command(args, **kwargs):
            if args[:2] == ['git', 'ls-tree']: return '\n'.join(paths)
            if args[:2] == ['git', 'show']: return (run.ROOT / args[2].split(':', 1)[1]).read_bytes()
            if args == ['claude', '--version']: return 'mocked-cli-version'
            self.fail('Unexpected subprocess: ' + str(args))
        protocols = []
        with patch.object(run.subprocess, 'check_output', side_effect=command), patch('builtins.print'):
            for name in ('first', 'second'):
                destination = self.root / name
                run.build(destination)
                protocol = json.loads((destination / 'protocol.json').read_text()); protocols.append(protocol)
                self.assertFalse(protocol['auto_memory_enabled'])
                self.assertIsNotNone(run.datetime.fromisoformat(protocol['built_at']).utcoffset())
                self.assertEqual(str(run.uuid.UUID(protocol['build_id'])), protocol['build_id'])
                for case in run.CASES:
                    path = destination / 'control' / (case['id'] + '.settings.json')
                    self.assertFalse(json.loads(path.read_text())['autoMemoryEnabled'])
                    self.assertEqual(protocol['control_hashes'][path.name], run.sha(path.read_bytes()))
        self.assertNotEqual(protocols[0]['build_id'], protocols[1]['build_id'])

    def test_old_manifest_rejected_without_launch(self):
        path = self.root / 'protocol.json'; path.write_text('{"kind":"old"}')
        with patch.object(run.smoke, 'run_session') as launch:
            with self.assertRaisesRegex(ValueError, 'identity mismatch'): run.run(self.root, run.sha(path.read_bytes()))
            launch.assert_not_called()

    def test_journal_fixture_valid_schema(self):
        path = run.ROOT / 'skills/context-docs/scripts/event_journal.py'
        spec = importlib.util.spec_from_file_location('journal_validator', path)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        module.validate(json.loads(run.CASES[-1]['files']['history/events/old.jsonl']), stored=True)


if __name__ == '__main__': unittest.main()
