"""Synthetic journal controls; these do not evaluate agent behavior."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / 'tools' / 'event_journal.py'
SPEC = importlib.util.spec_from_file_location('event_journal', SCRIPT)
journal = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(journal)


class EventJournalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'events'
        self.payload = {
            'type': 'verification', 'status': 'observed', 'actor': 'synthetic-agent',
            'summary': 'Synthetic check: café\nsecond line',
            'sources': ['synthetic:test-output'], 'revision': 'synthetic:revision-a',
            'check': {'command': 'synthetic-check', 'scope': 'synthetic fixture only',
                      'result': 'passed'},
        }

    def append(self, session='session-a', payload=None):
        return journal.append_event(self.root, session, self.payload if payload is None else payload)

    def cli(self, *args, payload=None):
        return subprocess.run([sys.executable, str(SCRIPT), '--directory', str(self.root), *args],
                              input=payload, text=True, capture_output=True)

    def test_roundtrip_unicode_and_newlines_with_generated_metadata(self):
        first = self.append()
        second = self.append()
        self.assertEqual(journal.read_events(self.root), [first, second])
        self.assertNotEqual(first['event_id'], second['event_id'])
        raw = (self.root / 'session-a.jsonl').read_bytes()
        self.assertEqual(len(raw.splitlines()), 2)
        self.assertIn('café'.encode(), raw)
        self.assertEqual(first['schema_version'], 1)
        self.assertTrue(first['recorded_at'].endswith('Z'))

    def test_invalid_payloads_do_not_create_directory(self):
        variants = []
        for field in journal.REQUIRED | {'check'}:
            payload = copy.deepcopy(self.payload)
            del payload[field]
            variants.append(payload)
        for change in ({'sources': []}, {'summary': ' '}, {'actor': 9},
                       {'status': 'approved'}, {'type': 'transcript'},
                       {'schema_version': 1}, {'check': {'result': 'pass'}},
                       {'supersedes': 'not-a-uuid'}):
            variants.append(dict(self.payload, **change))
        for payload in variants:
            with self.subTest(payload=payload), self.assertRaises(journal.JournalError):
                self.append(payload=payload)
            self.assertFalse(self.root.exists())

    def test_approved_decision_requires_authority(self):
        payload = dict(self.payload, type='decision', status='approved')
        payload.pop('check')
        with self.assertRaises(journal.JournalError):
            self.append(payload=payload)
        payload['authority'] = 'Synthetic owner; source: synthetic:approval-1'
        self.assertEqual(self.append(payload=payload)['authority'], payload['authority'])

    def test_correction_preserves_original(self):
        original = self.append()
        before = (self.root / 'session-a.jsonl').read_bytes()
        correction = dict(self.payload, supersedes=original['event_id'], summary='Corrected scope')
        self.append(payload=correction)
        self.assertTrue((self.root / 'session-a.jsonl').read_bytes().startswith(before))
        self.assertEqual(len(journal.read_events(self.root)), 2)

    def test_path_traversal_sessions_rejected(self):
        for session in ('../escape', '/tmp/escape', 'a/b', 'a\\b', '.', '', 'a' * 81):
            with self.subTest(session=session), self.assertRaises(journal.JournalError):
                self.append(session)
        self.assertFalse(self.root.exists())

    def test_incomplete_tail_is_preserved_and_blocks_append(self):
        self.append()
        path = self.root / 'session-a.jsonl'
        with path.open('ab') as stream:
            stream.write(b'{"summary":"interrupted')
        before = path.read_bytes()
        with self.assertRaisesRegex(journal.JournalError, 'unterminated'):
            self.append()
        self.assertEqual(path.read_bytes(), before)
        self.assertFalse((self.root / 'session-a.lock').exists())

    def test_malformed_history_rejected_without_output_or_changes(self):
        self.append()
        path = self.root / 'session-a.jsonl'
        with path.open('ab') as stream:
            stream.write(b'not-json\n')
        before = path.read_bytes()
        result = self.cli('read')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        with self.assertRaises(journal.JournalError):
            self.append()
        self.assertEqual(path.read_bytes(), before)

    def test_invalid_stored_metadata_and_blank_lines_rejected(self):
        record = self.append()
        path = self.root / 'session-a.jsonl'
        for changes in ({'schema_version': True}, {'schema_version': 2},
                        {'recorded_at': 'yesterday'}, {'session_id': 'other'},
                        {'event_id': 'bad'}, {'supersedes': record['event_id']}):
            with self.subTest(changes=changes):
                path.write_text(journal.encode(dict(record, **changes)), encoding='utf-8')
                with self.assertRaises(journal.JournalError):
                    journal.read_events(self.root)
        path.write_bytes(b'\n')
        with self.assertRaises(journal.JournalError):
            journal.read_events(self.root)

    def test_duplicate_keys_and_non_json_numbers_rejected(self):
        for text in ('{"summary":"one","summary":"two"}', '{"result":NaN}',
                     '{"result":Infinity}', '{"check":{"scope":"a","scope":"b"}}'):
            with self.subTest(text=text), self.assertRaises(journal.JournalError):
                journal.decode(text)

    def test_duplicate_event_ids_rejected(self):
        self.append()
        path = self.root / 'session-a.jsonl'
        path.write_bytes(path.read_bytes() * 2)
        with self.assertRaisesRegex(journal.JournalError, 'duplicate event_id'):
            journal.read_events(self.root)
        with self.assertRaises(journal.JournalError):
            self.append()

    def test_unpaired_unicode_surrogate_rejected_before_write_or_read_output(self):
        with self.assertRaises(journal.JournalError):
            self.append(payload=dict(self.payload, summary='\ud800'))
        self.assertFalse(self.root.exists())
        record = self.append()
        path = self.root / 'session-a.jsonl'
        with path.open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(dict(record, summary='\ud800')) + '\n')
        result = self.cli('read')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')

    def test_output_filter_does_not_hide_invalid_history(self):
        self.append()
        path = self.root / 'session-a.jsonl'
        with path.open('ab') as stream:
            stream.write(b'{"type":"contradiction"}\n')
        result = self.cli('read', '--type', 'verification')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')

    def test_lock_rejects_competing_process_but_other_session_can_write(self):
        self.append()
        before = (self.root / 'session-a.jsonl').read_bytes()
        with journal.writer_lock(self.root, 'session-a'):
            result = self.cli('append', '--session', 'session-a', payload=json.dumps(self.payload))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('session busy or stale lock', result.stderr)
            self.append('session-b')
        self.assertEqual((self.root / 'session-a.jsonl').read_bytes(), before)
        self.append()

    def test_symlink_session_rejected_without_touching_target(self):
        self.root.mkdir()
        target = Path(self.temp.name) / 'outside.jsonl'
        target.write_bytes(b'preserve me')
        (self.root / 'session-a.jsonl').symlink_to(target)
        with self.assertRaises(journal.JournalError):
            self.append()
        with self.assertRaises(journal.JournalError):
            journal.read_events(self.root)
        self.assertEqual(target.read_bytes(), b'preserve me')

    def test_read_is_read_only_and_filter_preserves_source_order(self):
        first = self.append()
        self.append(payload=dict(self.payload, type='contradiction', status='unknown'))
        self.append('session-b')
        before = {path.name: path.read_bytes() for path in self.root.iterdir()}
        result = self.cli('read', '--session', 'session-a', '--type', 'verification')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([json.loads(line) for line in result.stdout.splitlines()], [first])
        self.assertEqual({path.name: path.read_bytes() for path in self.root.iterdir()}, before)

    def test_missing_read_does_not_initialize(self):
        result = self.cli('read')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.root.exists())

    def test_cli_append_from_stdin_and_file(self):
        result = self.cli('append', '--session', 'session-a', payload=json.dumps(self.payload))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['summary'], self.payload['summary'])
        source = Path(self.temp.name) / 'input.json'
        source.write_text(json.dumps(self.payload), encoding='utf-8')
        result = self.cli('append', '--session', 'session-a', '--input', str(source))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(journal.read_events(self.root)), 2)

    def test_fsync_failure_reports_failure_and_releases_lock(self):
        with patch.object(journal.os, 'fsync', side_effect=OSError('synthetic I/O failure')):
            with self.assertRaises(OSError):
                self.append()
        self.assertFalse((self.root / 'session-a.lock').exists())
        # An error is not proof that no bytes were written. Inspect before retrying.
        self.assertEqual(len(journal.read_events(self.root)), 1)

    def test_deep_input_has_clean_cli_error_without_writes(self):
        result = self.cli('append', '--session', 'session-a', payload='[' * 2000 + '0' + ']' * 2000)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertNotIn('Traceback', result.stderr)
        self.assertFalse(self.root.exists())

    def test_deep_history_has_clean_error_and_is_preserved(self):
        self.append()
        path = self.root / 'session-a.jsonl'
        with path.open('ab') as stream:
            stream.write(b'[' * 2000 + b'0' + b']' * 2000 + b'\n')
        before = path.read_bytes()
        for args in (('read',), ('append', '--session', 'session-a')):
            result = self.cli(*args, payload=json.dumps(self.payload))
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, '')
            self.assertNotIn('Traceback', result.stderr)
            self.assertEqual(path.read_bytes(), before)
        self.assertFalse((self.root / 'session-a.lock').exists())

    def test_killed_writer_leaves_lock_and_partial_tail_for_explicit_recovery(self):
        self.append()
        path = self.root / 'session-a.jsonl'
        before = path.read_bytes()
        ready = Path(self.temp.name) / 'ready'
        child = '''
import importlib.util, pathlib, sys, time, os
spec = importlib.util.spec_from_file_location('journal', sys.argv[1])
journal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(journal)
root, ready = pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
with journal.writer_lock(root, 'session-a'):
    with (root / 'session-a.jsonl').open('ab') as stream:
        stream.write(b'{"summary":"interrupted')
        stream.flush()
        os.fsync(stream.fileno())
    ready.write_text('ready')
    time.sleep(30)
'''
        proc = subprocess.Popen([sys.executable, '-c', child, str(SCRIPT), str(self.root), str(ready)])
        try:
            deadline = time.monotonic() + 5
            while not ready.exists() and time.monotonic() < deadline and proc.poll() is None:
                time.sleep(0.01)
            self.assertTrue(ready.exists(), 'child did not reach interrupted-write boundary')
            proc.kill()
            proc.wait(timeout=5)
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=5)
        damaged = path.read_bytes()
        self.assertTrue(damaged.startswith(before))
        with self.assertRaisesRegex(journal.JournalError, 'stale lock'):
            self.append()
        self.assertEqual(path.read_bytes(), damaged)
        (self.root / 'session-a.lock').unlink()  # Child exit verified above.
        with self.assertRaisesRegex(journal.JournalError, 'unterminated'):
            self.append()
        self.assertEqual(path.read_bytes(), damaged)
        path.rename(self.root.parent / 'preserved-damaged.jsonl')
        self.append('session-recovered')
        self.assertEqual(len(journal.read_events(self.root)), 1)

    def test_concurrent_independent_sessions_preserve_all_acknowledged_records(self):
        source = Path(self.temp.name) / 'input.json'
        source.write_text(json.dumps(self.payload), encoding='utf-8')
        processes = [subprocess.Popen(
            [sys.executable, str(SCRIPT), '--directory', str(self.root), 'append',
             '--session', f'worker-{index}', '--input', str(source)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for index in range(12)]
        try:
            acknowledged = []
            for proc in processes:
                stdout, stderr = proc.communicate(timeout=10)
                self.assertEqual(proc.returncode, 0, stderr)
                acknowledged.append(json.loads(stdout))
        finally:
            for proc in processes:
                if proc.poll() is None:
                    proc.kill()
                    proc.communicate(timeout=5)
        stored = journal.read_events(self.root)
        self.assertEqual({r['event_id'] for r in stored}, {r['event_id'] for r in acknowledged})
        self.assertEqual(len(stored), 12)

    def test_duplicate_id_across_sessions_rejected_by_full_read(self):
        first = self.append('session-a')
        second = self.append('session-b')
        second['event_id'] = first['event_id']
        (self.root / 'session-b.jsonl').write_text(journal.encode(second), encoding='utf-8')
        result = self.cli('read')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('duplicate event_id', result.stderr)
        self.assertEqual(result.stdout, '')

    def test_repeated_append_is_not_deduplicated(self):
        self.append()
        self.append()
        self.assertEqual(len(journal.read_events(self.root)), 2)

    def test_structurally_valid_unsupported_claims_are_not_verified(self):
        payload = dict(self.payload, type='decision', status='approved',
                       sources=['missing-source'], authority='unverified claim of approval',
                       supersedes='00000000-0000-4000-8000-000000000001')
        # This is a documented boundary, not a claim that approval is real.
        self.assertEqual(self.append(payload=payload)['sources'], ['missing-source'])


if __name__ == '__main__':
    unittest.main()
