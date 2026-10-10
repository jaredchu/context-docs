import base64
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('public_history_run', Path(__file__).with_name('run.py'))
run = importlib.util.module_from_spec(spec); spec.loader.exec_module(run)
hook = run.hook


class Controls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name).resolve()
        self.project = self.root / 'session/project'; self.project.mkdir(parents=True)
        self.evidence = self.root / 'session/evidence'; self.evidence.mkdir()
        self.prefix = b'Original\r\nREADME\r\n'
        (self.project / 'README.md').write_bytes(self.prefix)
        self.config = dict(project=str(self.project), evidence=str(self.evidence),
            writable=['README.md', 'docs/upgrade-handoff.md'],
            readme_prefix_b64=base64.b64encode(self.prefix).decode())

    def tearDown(self): self.temp.cleanup()

    def event(self, tool, **payload):
        return dict(hook_event_name='PreToolUse', tool_name=tool, tool_use_id='one', tool_input=payload, decision='allow')

    def test_read_own_project_and_evidence_but_not_other_arm_or_ledger(self):
        for path, expected in [('README.md', 'allow'), (str(self.evidence / 'fix.diff'), 'allow'),
                               ('../../other/project/README.md', 'deny'), (str(run.ROOT / 'evals/public-history-ledger.md'), 'deny')]:
            self.assertEqual(hook.decision(self.event('Read', file_path=path), self.config)[0], expected, path)
        for tool in ('Bash', 'Skill', 'Agent', 'WebFetch'):
            self.assertEqual(hook.decision(self.event(tool), self.config)[0], 'deny')

    def test_search_cannot_escape_selected_root(self):
        for tool, args in [('Glob', dict(pattern='../*')), ('Grep', dict(pattern='word', glob='../*')),
                           ('Glob', dict(pattern='{..,x}/*')), ('Grep', dict(pattern='word', glob='{..,x}/*')),
                           ('Glob', dict(path=str(self.root), pattern='*'))]:
            self.assertEqual(hook.decision(self.event(tool, **args), self.config)[0], 'deny')
        self.assertEqual(hook.decision(self.event('Grep', path=str(self.evidence), pattern='ctx'), self.config)[0], 'allow')

    def test_exact_output_allowlist_and_readonly_evidence(self):
        for path, expected in [('docs/upgrade-handoff.md', 'allow'), ('docs/other.md', 'deny'),
                               (str(self.evidence / 'new.md'), 'deny'), ('CLAUDE.md', 'deny'),
                               ('.claude/skills/context-docs/SKILL.md', 'deny')]:
            self.assertEqual(hook.decision(self.event('Write', file_path=path, content='text'), self.config)[0], expected)

    def test_prefix_preserved_on_each_write_including_crlf(self):
        for text, expected in [(self.prefix.decode() + '\n[Handoff](docs/upgrade-handoff.md)\n', 'allow'),
                               (self.prefix.decode().replace('\r\n', '\n'), 'deny'), ('Replacement', 'deny')]:
            self.assertEqual(hook.decision(self.event('Write', file_path='README.md', content=text), self.config)[0], expected)
        self.assertEqual((self.project / 'README.md').read_bytes(), self.prefix)

    def test_edit_prediction_preserves_prefix_and_rejects_ambiguous_replace(self):
        (self.project / 'README.md').write_bytes(self.prefix + b'append\nappend\n')
        for args, expected in [({'old_string': 'Original', 'new_string': 'Changed'}, 'deny'),
                               ({'old_string': 'append', 'new_string': 'new'}, 'deny'),
                               ({'old_string': 'append', 'new_string': 'new', 'replace_all': True}, 'allow')]:
            self.assertEqual(hook.decision(self.event('Edit', file_path='README.md', **args), self.config)[0], expected)

    def test_binary_mode_and_internal_directory_symlink_snapshot(self):
        (self.project / 'pkg').mkdir(); (self.project / 'pkg/raw').write_bytes(b'\xff\x00\r\n')
        (self.project / 'alias').symlink_to('pkg', target_is_directory=True)
        before = run.snapshot(self.project)
        self.assertEqual(before['pkg/raw']['sha256'], run.sha(b'\xff\x00\r\n'))
        self.assertEqual(before['alias']['kind'], 'symlink'); self.assertEqual(before['alias']['target'], 'pkg')
        self.assertNotIn('alias/raw', before)
        (self.project / 'pkg/raw').chmod(0o755)
        self.assertNotEqual(before, run.snapshot(self.project))
        self.assertEqual(hook.decision(self.event('Read', file_path='alias/raw'), self.config)[0], 'allow')

    def test_external_symlinks_rejected_and_internal_write_alias_denied(self):
        (self.project / 'docs').symlink_to(self.evidence, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'External symlink'): run.snapshot(self.project)
        self.assertEqual(hook.decision(self.event('Write', file_path='docs/upgrade-handoff.md', content='x'), self.config)[0], 'deny')
        (self.project / 'docs').unlink(); (self.project / 'real').mkdir(); (self.project / 'docs').symlink_to('real', target_is_directory=True)
        config = {**self.config, 'writable': ['real/upgrade-handoff.md']}
        self.assertEqual(hook.decision(self.event('Write', file_path='docs/upgrade-handoff.md', content='x'), config)[0], 'deny')

    def test_ancestor_symlink_alias_allowed_but_internal_root_link_denied(self):
        alias = self.root / 'alias'; alias.symlink_to(self.project.parent, target_is_directory=True)
        event = self.event('Write', file_path=str(alias / 'project/README.md'), content=self.prefix.decode() + 'append')
        self.assertEqual(hook.decision(event, self.config)[0], 'allow')
        (self.project / 'loop').symlink_to('.', target_is_directory=True)
        event['tool_input']['file_path'] = str(self.project / 'loop/README.md')
        self.assertEqual(hook.decision(event, self.config)[0], 'deny')

    def test_fixture_drift_includes_newline_binary_and_unexpected_skill(self):
        (self.project / 'raw').write_bytes(b'\xff')
        sid = 'httpx-ordinary'; dest = self.root / 'runtime'; unit = dest / 'sessions' / sid
        unit.mkdir(parents=True)
        import shutil
        shutil.copytree(self.project, unit / 'project'); shutil.copytree(self.evidence, unit / 'evidence')
        p = dict(initial_hashes={sid: run.snapshot(unit / 'project')}, evidence_hashes={sid: run.snapshot(unit / 'evidence')})
        run.preflight(dest, p, {'id': sid})
        (unit / 'project/.claude/skills').mkdir(parents=True)
        (unit / 'project/.claude/skills/SKILL.md').write_text('leaked treatment')
        with self.assertRaisesRegex(ValueError, 'Fixture drift'): run.preflight(dest, p, {'id': sid})

    def write_read_result(self, text, error=False):
        log = self.root / 'stream.jsonl'
        log.write_text(json.dumps(dict(type='user', message=dict(content=[dict(type='tool_result', tool_use_id='one', content=text, is_error=error)]))))
        return log

    def test_skill_exposure_requires_successful_full_returned_body(self):
        body = '---\nname: context-docs\n---\nDo the work.\nKeep evidence.\n'
        event = self.event('Read', file_path='.claude/skills/context-docs/SKILL.md')
        full = '\n'.join(str(i) + '→' + line for i, line in enumerate(body.splitlines(), 1))
        self.assertTrue(run.complete_skill_read(self.write_read_result(full), [event], self.project, body))
        for text, error in [(full, True), (full.rsplit('\n', 1)[0], False), ('Read complete.', False)]:
            self.assertFalse(run.complete_skill_read(self.write_read_result(text, error), [event], self.project, body))
        event['decision'] = 'deny'
        self.assertFalse(run.complete_skill_read(self.write_read_result(full), [event], self.project, body))

    def test_matched_prompt_difference_is_only_explicit_core_delivery(self):
        for name in run.OUTPUTS:
            ordinary = run.prompt_for(name, 'ordinary'); skill = run.prompt_for(name, 'skill')
            self.assertTrue(skill.startswith(ordinary)); self.assertNotIn('context-docs', ordinary)
        self.assertEqual(run.ORDER, [('httpx', 'ordinary'), ('httpx', 'skill'), ('ripgrep', 'skill'), ('ripgrep', 'ordinary')])

    def test_native_skill_catalog_requires_observed_empty_arrays(self):
        log = self.root / 'stream.jsonl'
        for payload, expected in [({'skills': [], 'slash_commands': []}, True),
                                  ({'skills': ['context-docs'], 'slash_commands': []}, False),
                                  ({'skills': []}, False)]:
            log.write_text(json.dumps(dict(type='system', subtype='init', **payload)))
            self.assertEqual(run.native_skills_disabled(log), expected)

    def test_denial_alone_does_not_stop_but_uncovered_or_successful_denial_does(self):
        self.assertFalse(run.should_stop({'all_tool_calls_guarded': True}, 'permission_denied'))
        self.assertTrue(run.should_stop({'all_tool_calls_guarded': False}, None))
        self.assertTrue(run.should_stop({'all_tool_calls_guarded': True}, 'missing_terminal_result'))

    def test_timeout_and_skill_nondelivery_continue_without_masking_failed_checks(self):
        checks = {k: True for k in run.INTEGRITY_GATES}
        checks.update(completed=False, treatment_delivery=False)
        self.assertFalse(run.should_stop(checks, 'missing_terminal_result', timed_out=True))
        self.assertFalse(checks['completed']); self.assertFalse(checks['treatment_delivery'])
        self.assertTrue(run.should_stop(checks, 'missing_terminal_result', timed_out=False))
        checks['no_successful_denied_tool'] = False
        self.assertTrue(run.should_stop(checks, 'missing_terminal_result', timed_out=True))

    def test_instruction_injection_at_every_runtime_ancestor_rejected_prelaunch(self):
        destination = self.root / 'runtime'; unit = destination / 'sessions/httpx-ordinary'
        (unit / 'project').mkdir(parents=True); (unit / 'evidence').mkdir()
        for parent in (destination, unit.parent, unit):
            injected = parent / 'CLAUDE.md'; injected.write_text('contaminated')
            with self.assertRaisesRegex(ValueError, 'Ancestor instruction'):
                run.preflight(destination, {}, {'id': 'httpx-ordinary'})
            injected.unlink()
        (destination / '.claude').mkdir()
        with self.assertRaisesRegex(ValueError, 'Ancestor instruction'):
            run.preflight(destination, {}, {'id': 'httpx-ordinary'})
        (destination / '.claude').rmdir(); (unit / 'extra.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'Unexpected session-unit'):
            run.preflight(destination, {}, {'id': 'httpx-ordinary'})

    def test_subject_provenance_excludes_evaluator_notes_at_all_levels(self):
        identity = dict(id='case', repository='owner/repo', before='old', after='new', notes='SECRET-LEAD')
        source = dict(path='x', url='https://example.invalid/x', sha256='hash', rubric='SECRET-LEAD')
        fix = dict(commit='fix', diff_url='https://example.invalid/diff', diff_sha256='hash',
                   primary_file_provenance={'candidate_distinction': 'SECRET-LEAD'})
        refs = run.source_references(identity, [source], fix)
        self.assertNotIn('SECRET-LEAD', json.dumps(refs))
        self.assertEqual(refs['files'][0], {k: source[k] for k in ('path', 'url', 'sha256')})
        self.assertNotIn('primary_file_provenance', refs['fix'])

    def test_invalid_utf8_retained_with_specific_flag(self):
        text, valid = run.decode_artifact(b'a\xffb')
        self.assertEqual(text, 'a\ufffdb'); self.assertFalse(valid)
        self.assertEqual(run.decode_artifact(b'ok'), ('ok', True))

    def test_status_explicitly_records_unrun_and_stop(self):
        status = run.record_status(self.root, ['a', 'b', 'c', 'd'], ['a'], 'integrity failure', 'stopped')
        self.assertEqual(status['unrun'], ['b', 'c', 'd']); self.assertEqual(status['stopped_after'], 'a')
        self.assertEqual(status['stop_reason'], 'integrity failure')
        status = run.record_status(self.root, ['a'], ['a'], state='completed')
        self.assertEqual(status['unrun'], []); self.assertIsNone(status['stopped_after'])

    def test_diagnostic_exception_preserves_computed_gates_and_unrun_status(self):
        import shutil
        destination = self.root / 'runtime'; unit = destination / 'sessions/httpx-ordinary'
        unit.mkdir(parents=True); (destination / 'control').mkdir()
        shutil.copytree(self.project, unit / 'project'); (unit / 'evidence').mkdir()
        (unit / 'project/CLAUDE.md').write_text(run.BOOTSTRAP)
        sessions = [dict(id='httpx-ordinary', arm='ordinary', output='docs/upgrade-handoff.md', prompt='task'),
                    dict(id='httpx-skill', arm='skill', output='docs/upgrade-handoff.md', prompt='task')]
        before = run.snapshot(unit / 'project')
        p = dict(sessions=sessions, model='claude-opus-5-5', requested_effort='high', allowed_tools=list(hook.TOOLS),
                 initial_hashes={'httpx-ordinary': before}, evidence_hashes={'httpx-ordinary': {}},
                 configurations={'httpx-ordinary': self.config}, control_hashes={})
        loading = dict(hook_event_name='InstructionsLoaded', file_path=str(unit / 'project/CLAUDE.md'),
                       load_reason='session_start', file_sha256_at_event=before['CLAUDE.md']['sha256'])
        observed = dict(execution_error=None, final_message='done', event_types=['result'])
        with patch.object(run, 'validate', return_value=p), patch.object(run, 'preflight'), \
             patch.object(run.smoke, 'run_session', return_value=dict(exit_code=0, seconds=1)), \
             patch.object(run.smoke, 'parse_stream', return_value=observed), \
             patch.object(run.helper, 'observed_models', return_value={'responding_models': [p['model']]}), \
             patch.object(run.guarded, 'read_events', return_value=[loading]), \
             patch.object(run.guarded, 'coverage', return_value={'all_tool_calls_guarded': True}), \
             patch.object(run, 'native_skills_disabled', return_value=True), \
             patch.object(run, 'trajectory', side_effect=ValueError('diagnostic failure')), patch('builtins.print'):
            run.run(destination, 'frozen')
        trial = json.loads((destination / 'trials.json').read_text())[0]
        self.assertTrue(trial['execution_checks']['all_tool_calls_guarded'])
        self.assertTrue(trial['execution_checks']['responding_model_matches'])
        self.assertTrue(trial['execution_checks']['immutable_bytes_and_modes'])
        self.assertFalse(trial['execution_checks']['postprocess_ok'])
        self.assertEqual(trial['final_message'], 'done')
        self.assertTrue((destination / 'logs/httpx-ordinary.checks.json').exists())
        status = json.loads((destination / 'status.json').read_text())
        self.assertEqual(status['attempted'], ['httpx-ordinary']); self.assertEqual(status['unrun'], ['httpx-skill'])

    def test_export_trajectory_does_not_vendor_source_or_reveal_outside_paths(self):
        log = self.write_read_result('WHOLE-UPSTREAM-SOURCE')
        event = self.event('Read', file_path='README.md')
        data = run.trajectory(log, [event], self.project, self.evidence, self.root)
        self.assertNotIn('WHOLE-UPSTREAM-SOURCE', json.dumps(data)); self.assertEqual(data[0]['result_characters'], 21)
        event['tool_input']['file_path'] = '/Users/secret/private.txt'; event['decision'] = 'deny'
        data = run.trajectory(log, [event], self.project, self.evidence, self.root)
        self.assertNotIn('/Users/secret', json.dumps(data)); self.assertEqual(data[0]['path'], '[outside permitted roots]')

    def test_ancestor_instruction_blocks_before_build(self):
        (self.root / 'CLAUDE.md').write_text('Unrelated context')
        with patch.object(run.subprocess, 'check_output') as process:
            with self.assertRaisesRegex(ValueError, 'Ancestor instruction'): run.build(self.root / 'new', self.root, self.root)
            process.assert_not_called()

    def test_source_git_blob_and_mode_verification(self):
        import hashlib
        b = self.prefix
        manifest = dict(revision='pin', files={'README.md': dict(sha256=run.sha(b),
            git_blob=hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), mode='100644')})
        run.verify_source(self.project, manifest, 'pin')
        (self.project / 'README.md').chmod(0o755)
        with self.assertRaisesRegex(ValueError, 'content/mode drift'): run.verify_source(self.project, manifest, 'pin')


if __name__ == '__main__': unittest.main()
