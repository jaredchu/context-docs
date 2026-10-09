"""Credential-free controls for the bounded public-source adoption evaluator."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run


class GraderControls(unittest.TestCase):
    def setUp(self):
        self.initial = {'CLAUDE.md': run.NEW, 'README.md': '# Upstream\n',
                        'match.go': 'package match\n', 'LICENSE': 'license\n',
                        '.claude/skills/context-docs/SKILL.md': 'frozen skill\n'}
        self.reference = {**self.initial,
            'CLAUDE.md': run.NEW + '\n## Context maintenance\n\n' + run.new_marker() + '\n' +
                         run.RULE.replace('$context-docs', 'the context-docs skill'),
            'README.md': '# Upstream\n\n[Context](docs/context.md)\n',
            'docs/context.md': '# Context\n\n[Source](../match.go)\n'}
        self.legacy = {**self.initial, 'CLAUDE.md': run.LEGACY,
                       'README.md': '# Upstream\n[Context](notes/project.md)\n',
                       'notes/project.md': run.CONTEXT}
        self.marker = 'Method: context-docs\nAdopted: unknown\nEntry point: notes/project.md\n'

    def passed(self, sid, before, after):
        return all(run.grade(sid, before, after).values())

    def test_reference_and_repeat_pass(self):
        self.assertTrue(self.passed('new-adopt', self.initial, self.reference))
        self.assertTrue(self.passed('new-repeat', self.reference, self.reference))

    def test_marker_without_maintenance_rule_fails(self):
        candidate = copy.deepcopy(self.reference)
        candidate['CLAUDE.md'] = run.NEW + '\n## Context maintenance\n\n' + run.new_marker()
        checks = run.grade('new-adopt', self.initial, candidate)
        self.assertFalse(checks['skill_named'])
        self.assertFalse(all(checks.values()))

    def test_appended_readme_context_section_passes_without_self_link(self):
        candidate = copy.deepcopy(self.reference)
        candidate.pop('docs/context.md')
        candidate['CLAUDE.md'] = candidate['CLAUDE.md'].replace('docs/context.md', 'README.md#project-context')
        candidate['README.md'] = self.initial['README.md'] + '\n## Project context\n\nSource-backed summary.\n'
        self.assertTrue(self.passed('new-adopt', self.initial, candidate))
        for fragment in ('missing', 'upstream'):
            invalid = copy.deepcopy(candidate)
            invalid['CLAUDE.md'] = invalid['CLAUDE.md'].replace('#project-context', '#' + fragment)
            self.assertFalse(self.passed('new-adopt', self.initial, invalid), fragment)

    def test_new_invocation_prefixes_fail_but_installed_paths_and_marker_pass(self):
        for token in ('$context-docs', '/context-docs'):
            candidate = copy.deepcopy(self.reference)
            candidate['CLAUDE.md'] = candidate['CLAUDE.md'].replace('the context-docs skill', token)
            self.assertFalse(self.passed('new-adopt', self.initial, candidate), token)
        for token in ('.claude/skills/context-docs', '.claude/skills/context-docs/',
                      '.claude/skills/context-docs/SKILL.md', 'Method: context-docs'):
            self.assertTrue(run.no_invocation_syntax(token), token)
        for token in ('.claude/skills/context-docs', '.claude/skills/context-docs/'):
            candidate = copy.deepcopy(self.reference)
            candidate['CLAUDE.md'] += '\nInstalled at `' + token + '`.\n'
            self.assertTrue(self.passed('new-adopt', self.initial, candidate), token)

    def test_invocation_example_outside_ongoing_instructions_is_not_a_prefix_failure(self):
        candidate = copy.deepcopy(self.reference)
        candidate['README.md'] += '\nFor a user-requested audit, invoke `/context-docs`.\n'
        self.assertTrue(run.grade('new-adopt', self.initial, candidate)['new_instructions_neutral'])
        # Whether this extra README text is still only navigation is semantic review.

    def test_changed_repeat_date_and_audit_mutation_fail(self):
        changed = copy.deepcopy(self.reference)
        changed['CLAUDE.md'] = changed['CLAUDE.md'].replace('2026-10-09', '2026-10-10')
        self.assertFalse(self.passed('new-repeat', self.reference, changed))
        self.assertFalse(self.passed('legacy-audit', self.reference, changed))

    def test_broken_entry_and_link_fail(self):
        changed = copy.deepcopy(self.reference)
        changed['CLAUDE.md'] = changed['CLAUDE.md'].replace('docs/context.md', 'docs/missing.md')
        self.assertFalse(self.passed('new-adopt', self.initial, changed))
        changed = copy.deepcopy(self.reference)
        changed['docs/context.md'] += '[missing](absent.md)\n'
        self.assertFalse(self.passed('new-adopt', self.initial, changed))

    def test_equivalent_relative_entry_and_navigation_paths_pass(self):
        for entry, link in [('docs/context.md', './docs/context.md'),
                            ('./docs/context.md', 'docs/context.md'),
                            ('docs/../docs/context.md', 'docs/%63ontext.md'),
                            ('./docs/context.md#context', 'docs/context.md#%63ontext')]:
            changed = copy.deepcopy(self.reference)
            changed['CLAUDE.md'] = changed['CLAUDE.md'].replace('Entry point: docs/context.md', 'Entry point: ' + entry)
            changed['README.md'] = changed['README.md'].replace('(docs/context.md)', '(' + link + ')')
            self.assertTrue(self.passed('new-adopt', self.initial, changed), (entry, link))
        changed = copy.deepcopy(self.reference)
        changed['CLAUDE.md'] = changed['CLAUDE.md'].replace('Entry point: docs/context.md', 'Entry point: ./docs/context.md   ')
        changed['README.md'] = changed['README.md'].replace('(docs/context.md)', '(./docs/context.md "Project context")')
        self.assertTrue(self.passed('new-adopt', self.initial, changed))

    def test_escaping_or_mismatched_navigation_targets_fail(self):
        for target in ('../docs/context.md', '%2e%2e/docs/context.md', 'docs/context.md#missing'):
            changed = copy.deepcopy(self.reference)
            changed['README.md'] = changed['README.md'].replace('(docs/context.md)', '(' + target + ')')
            self.assertFalse(self.passed('new-adopt', self.initial, changed), target)
            changed = copy.deepcopy(self.reference)
            changed['CLAUDE.md'] = changed['CLAUDE.md'].replace('Entry point: docs/context.md', 'Entry point: ' + target)
            self.assertFalse(self.passed('new-adopt', self.initial, changed), target)
        changed = copy.deepcopy(self.reference)
        changed['docs/context.md'] += '\n## Details\nMore information.\n'
        changed['CLAUDE.md'] = changed['CLAUDE.md'].replace('Entry point: docs/context.md', 'Entry point: docs/context.md#details')
        changed['README.md'] = changed['README.md'].replace('(docs/context.md)', '(docs/context.md#context)')
        self.assertFalse(self.passed('new-adopt', self.initial, changed))

    def test_upstream_package_and_readme_rewrite_fail(self):
        for name in ('match.go', 'LICENSE', '.claude/skills/context-docs/SKILL.md', 'README.md'):
            changed = copy.deepcopy(self.reference)
            changed[name] = 'replacement\n'
            self.assertFalse(self.passed('new-adopt', self.initial, changed), name)

    def test_original_overlay_order_and_one_logging_setting(self):
        changed = copy.deepcopy(self.reference)
        changed['CLAUDE.md'] = changed['CLAUDE.md'].replace('Event journal: off', 'Event journal: on')
        self.assertFalse(self.passed('new-adopt', self.initial, changed))
        changed = copy.deepcopy(self.reference)
        changed['CLAUDE.md'] += '\nEvent journal: off\n'
        self.assertFalse(self.passed('new-adopt', self.initial, changed))

    def test_legacy_marker_above_or_below_rule_passes(self):
        for body in (run.LEGACY.replace(run.RULE, self.marker + '\n' + run.RULE),
                     run.LEGACY.replace(run.RULE, run.RULE + '\n' + self.marker)):
            self.assertTrue(self.passed('legacy-marker', self.legacy, {**self.legacy, 'CLAUDE.md': body}))

    def test_legacy_rewritten_rule_or_new_heading_fails(self):
        body = run.LEGACY.replace(run.RULE, self.marker + '\n' + run.RULE)
        for changed in (body.replace('$context-docs', 'the context-docs skill'),
                        body.replace(self.marker, '## Adoption\n\n' + self.marker),
                        body.replace('Adopted: unknown', 'Adopted: 2026-10-09')):
            self.assertFalse(self.passed('legacy-marker', self.legacy, {**self.legacy, 'CLAUDE.md': changed}))

    def test_legacy_context_readme_or_extra_file_mutation_fails(self):
        reference = {**self.legacy, 'CLAUDE.md': run.LEGACY.replace(run.RULE, self.marker + '\n' + run.RULE)}
        for name in ('README.md', 'notes/project.md', 'extra.md'):
            self.assertFalse(self.passed('legacy-marker', self.legacy, {**reference, name: 'changed\n'}))

    def test_repository_root_license_and_escape_links(self):
        self.assertTrue(run.local_links_valid({'README.md': '[License](/LICENSE)', 'LICENSE': 'ok'}, ['README.md']))
        self.assertFalse(run.local_links_valid({'README.md': '[escape](../outside.md)'}, ['README.md']))

    def test_legacy_context_has_no_calendar_date(self):
        self.assertNotRegex(run.CONTEXT, r'\d{4}-\d{2}-\d{2}')

    def test_frozen_hash_mismatch_fails_before_launch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'protocol.json').write_text('{}')
            with patch.object(run.smoke, 'run_session') as subject:
                with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                    run.run(root, 'wrong')
                subject.assert_not_called()

    def test_crlf_mutation_is_not_hidden_by_text_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file = root / 'CLAUDE.md'
            file.write_bytes(b'First line\nSecond line\n')
            before = run.snapshot(root)
            file.write_bytes(b'First line\r\nSecond line\r\n')
            after = run.snapshot(root)
            self.assertNotEqual(run.hashes(before), run.hashes(after))
            self.assertFalse(self.passed('new-repeat', before, after))
            self.assertFalse(self.passed('legacy-audit', before, after))

    def test_dependent_input_and_immutable_baseline_drift_fail_before_launch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); project = root / 'projects/new'
            project.mkdir(parents=True)
            run.smoke.write_files(project, self.reference)
            frozen = run.hashes(self.reference)
            config = {'new-repeat': {'config': {'immutable': ['match.go']}}}
            p = dict(initial_hashes={'new': frozen}, control_hashes={},
                     harness_hashes=run.harness_hashes(), configurations=config)
            session = dict(id='new-repeat', project='new')
            self.assertEqual(run.preflight_session(root, p, session, {'new': frozen}), self.reference)
            (project / 'docs/context.md').write_text('inter-session mutation\n')
            with self.assertRaisesRegex(ValueError, 'Dependent input drift'):
                run.preflight_session(root, p, session, {'new': frozen})
            (project / 'match.go').write_text('changed immutable\n')
            actual = run.hashes(run.snapshot(project))
            with self.assertRaisesRegex(ValueError, 'Immutable baseline drift'):
                run.preflight_session(root, p, session, {'new': actual})

    def test_skill_provenance_requires_local_path_and_exact_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); log = root / 'log.jsonl'
            skill = '---\nname: adopt-context-docs\n---\n\nFrozen candidate body.'
            def write(base, body):
                log.write_text(json.dumps(dict(type='user', message=dict(content=[dict(type='text',
                    text='Base directory for this skill: ' + base + '\n\n' + body)]))) + '\n')
            path = str(root / '.claude/skills/adopt-context-docs')
            write(path, 'Frozen candidate body.')
            self.assertTrue(run.provenance(log, root, skill))
            write('/global/adopt-context-docs', 'Frozen candidate body.')
            self.assertFalse(run.provenance(log, root, skill))
            write(path, 'Old released body.')
            self.assertFalse(run.provenance(log, root, skill))

    def test_responding_model_mismatch_is_not_hidden_by_init_label(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / 'stream.jsonl'
            events = [dict(type='system', subtype='init', model='claude-opus-5-5'),
                      dict(type='assistant', message=dict(model='different-model'))]
            log.write_text('\n'.join(json.dumps(e) for e in events) + '\n')
            observed = run.observed_models(log)
            self.assertEqual(observed['responding_models'], ['different-model'])
            self.assertNotEqual(observed['responding_models'], ['claude-opus-5-5'])
            self.assertTrue(observed['confirmed'])
            log.write_text(json.dumps(events[0]) + '\n')
            self.assertFalse(run.observed_models(log)['confirmed'])

    def test_model_usage_canonical_evidence_is_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / 'stream.jsonl'
            event = dict(type='result', modelUsage={'opus': {'canonicalModel': 'claude-opus-5-5'}})
            log.write_text(json.dumps(event) + '\n')
            observed = run.observed_models(log)
            self.assertEqual(observed['usage_models'], ['claude-opus-5-5'])
            self.assertEqual(observed['responding_models'], [])
            self.assertEqual(observed['evidence_sources'], [])
            self.assertFalse(observed['confirmed'])

    def test_auxiliary_usage_model_does_not_fail_correct_responder_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / 'stream.jsonl'
            events = [dict(type='assistant', message=dict(model='claude-opus-5-5')),
                      dict(type='result', modelUsage={
                          'opus': {'canonicalModel': 'claude-opus-5-5'},
                          'haiku': {'canonicalModel': 'claude-haiku-4-5-20251001'}})]
            log.write_text('\n'.join(json.dumps(event) for event in events) + '\n')
            observed = run.observed_models(log)
            self.assertEqual(observed['responding_models'], ['claude-opus-5-5'])
            self.assertTrue(observed['confirmed'])
            self.assertEqual(observed['evidence_sources'], ['assistant_message.model'])
            self.assertEqual(observed['usage_models'], ['claude-haiku-4-5-20251001', 'claude-opus-5-5'])


if __name__ == '__main__':
    unittest.main()
