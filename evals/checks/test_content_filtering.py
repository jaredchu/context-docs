"""Offline acceptance controls for authored examples, not an agent or secret scanner."""
import copy
import importlib.util
import json
import posixpath
import re
import tempfile
import unittest
from pathlib import Path


CASES = json.loads((Path(__file__).parents[1] / 'content-filtering' / 'cases.json').read_text())
JOURNAL_SPEC = importlib.util.spec_from_file_location(
    'content_filtering_journal',
    Path(__file__).parents[2] / 'skills/context-docs/scripts/event_journal.py')
JOURNAL = importlib.util.module_from_spec(JOURNAL_SPEC)
JOURNAL_SPEC.loader.exec_module(JOURNAL)


def check(case, writes):
    """Check this fixture's explicit content contract; paraphrases need human review."""
    failures = []
    allowed = set(case['after'])
    if set(writes) != allowed:
        failures.append('write scope or no-change boundary')
    for path, required in case['retain'].items():
        for fact in required:
            if fact not in writes.get(path, ''):
                failures.append('missing fixture fact: ' + fact)
    for text in writes.values():
        for marker in case['omit']:
            if marker in text:
                failures.append('incidental metadata/bookkeeping: ' + marker)
        if case['audience'].startswith('public'):
            for source in case['before']:
                if source.startswith('private/') and source in text:
                    failures.append('private source location in public content')
    final = {**case['before'], **writes}
    for path, text in writes.items():
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            if target.startswith(('https://', 'http://', '#')):
                continue
            target = target.partition('#')[0]
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
            if target.startswith(('/', 'file:', '~')) or resolved not in final:
                failures.append('unportable/missing source reference: ' + target)
            elif resolved.startswith('private/') and case['audience'].startswith('public'):
                failures.append('private source exposed as public reference')
    if case['operation'] == 'capture':
        try:
            rows = [json.loads(line) for text in writes.values()
                    for line in text.splitlines() if line.strip()]
            if len(rows) != 1 or rows[0]['type'] != 'verification':
                failures.append('expected one meaningful event')
            JOURNAL.validate(rows[0], stored=True)
            for source in rows[0]['sources']:
                if source.startswith(('/', '~', 'file:')) or source not in final:
                    failures.append('unportable/missing event source')
                elif source.startswith('private/'):
                    failures.append('private source exposed as public reference')
        except (ValueError, KeyError, IndexError, TypeError):
            failures.append('invalid fixture event')
    return failures


class ContentFilteringExamples(unittest.TestCase):
    def test_six_worked_examples_meet_their_contracts(self):
        for case in CASES:
            with self.subTest(case=case['id']):
                self.assertEqual(check(case, case['after']), [])

    def test_loss_of_each_required_fact_is_detected(self):
        # In particular: conditions, uncertainty, rationale, blockers, diagnostic
        # root distinctions, useful personal paths and preservation of setup rules.
        for case in CASES:
            for path, facts in case['retain'].items():
                for fact in facts:
                    writes = copy.deepcopy(case['after'])
                    writes[path] = writes[path].replace(fact, '[omitted]')
                    with self.subTest(case=case['id'], fact=fact):
                        self.assertTrue(check(case, writes))

    def test_reintroduced_incidental_details_are_detected(self):
        for case in CASES:
            for marker in case['omit']:
                writes = copy.deepcopy(case['after'])
                path = next(iter(writes))
                if path.endswith('.jsonl'):
                    row = json.loads(writes[path]); row['summary'] += ' ' + marker
                    writes[path] = json.dumps(row) + '\n'
                else:
                    writes[path] += '\n' + marker + '\n'
                with self.subTest(case=case['id'], marker=marker):
                    self.assertTrue(check(case, writes))

    def test_frozen_sources_cannot_be_rewritten_as_cleanup(self):
        for case in CASES:
            for path in set(case['before']) - set(case['after']):
                writes = {**case['after'], path: 'Sanitized in place.\n'}
                with self.subTest(case=case['id'], path=path):
                    self.assertIn('write scope or no-change boundary', check(case, writes))

    def test_links_resolve_after_moving_fixture_root(self):
        # Resolution uses only the case's repository paths, never this checkout.
        for case in CASES:
            for root in ('fork-a', 'different-layout/fork-b'):
                files = {posixpath.join(root, p) for p in {**case['before'], **case['after']}}
                for path, text in case['after'].items():
                    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                        if target.startswith(('https://', 'http://', '#')):
                            continue
                        target = target.partition('#')[0]
                        self.assertIn(posixpath.normpath(posixpath.join(root, posixpath.dirname(path), target)), files)

    def test_absolute_broken_and_private_links_are_detected(self):
        case = CASES[0]
        for target in ('/Users/mira/evidence/C-7', 'file:///private/evidence',
                       '../missing.md', '../private/session.txt'):
            writes = copy.deepcopy(case['after'])
            writes['docs/context.md'] += '\n[Evidence](' + target + ')\n'
            with self.subTest(target=target):
                self.assertTrue(check(case, writes))

    def test_journal_does_not_duplicate_or_replace_existing_event(self):
        case = next(case for case in CASES if case['operation'] == 'capture')
        path = 'history/events/new.jsonl'
        writes = {path: case['after'][path] * 2}
        self.assertTrue(check(case, writes))
        writes = copy.deepcopy(case['after'])
        row = json.loads(writes[path]); row['sources'] = ['/Users/mira/evidence/C-8']
        writes[path] = json.dumps(row) + '\n'
        self.assertTrue(check(case, writes))
        row['sources'] = ['private/session.txt']
        writes[path] = json.dumps(row) + '\n'
        self.assertTrue(check(case, writes))

    def test_plain_private_source_locations_are_detected(self):
        for case in CASES:
            if not case['after'] or not case['audience'].startswith('public'):
                continue
            for source in case['before']:
                if not source.startswith('private/'):
                    continue
                writes = copy.deepcopy(case['after'])
                path = next(iter(writes))
                if path.endswith('.jsonl'):
                    row = json.loads(writes[path]); row['summary'] += ' See ' + source
                    writes[path] = json.dumps(row) + '\n'
                else:
                    writes[path] += '\nSee ' + source + '\n'
                with self.subTest(case=case['id'], source=source):
                    self.assertTrue(check(case, writes))

    def test_no_change_does_not_create_bookkeeping_event(self):
        case = next(case for case in CASES if case['operation'] == 'no-change')
        self.assertEqual(check(case, {}), [])
        self.assertTrue(check(case, {'history/events/new.jsonl': '{"summary":"Everything unchanged"}\n'}))

    def test_journal_example_uses_packaged_schema_and_helper(self):
        case = next(case for case in CASES if case['operation'] == 'capture')
        path = 'history/events/new.jsonl'
        row = json.loads(case['after'][path])
        JOURNAL.validate(row, stored=True)
        payload = {key: value for key, value in row.items() if key not in JOURNAL.GENERATED}
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / 'events'
            stored = JOURNAL.append_event(directory, 'synthetic-c8', payload)
            self.assertEqual(payload, {key: value for key, value in stored.items()
                                       if key not in JOURNAL.GENERATED})
            self.assertEqual(JOURNAL.read_events(directory, 'synthetic-c8'), [stored])
        for field in ('revision', 'check', 'recorded_at'):
            corrupt = dict(row); del corrupt[field]
            with self.subTest(field=field):
                self.assertTrue(check(case, {path: json.dumps(corrupt) + '\n'}))


if __name__ == '__main__':
    unittest.main()
