#!/usr/bin/env python3
"""Optional, local JSONL event journal. Python 3.9+; standard library only."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
from uuid import UUID, uuid4


TYPES = ('verification', 'contradiction', 'decision', 'context_update')
STATUSES = ('observed', 'approved', 'proposed', 'unknown', 'superseded')
REQUIRED = {'type', 'status', 'actor', 'summary', 'sources', 'revision'}
OPTIONAL = {'authority', 'check', 'supersedes'}
GENERATED = {'schema_version', 'event_id', 'recorded_at', 'session_id'}


class JournalError(ValueError):
    """Invalid input or journal state; no automatic repair is attempted."""


def require(condition, message):
    if not condition:
        raise JournalError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def session_name(value):
    require(isinstance(value, str) and
            re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', value),
            'session must be 1–80 ASCII letters, digits, underscores or hyphens; '
            'start with a letter or digit')
    return value


def uuid(value):
    require(isinstance(value, str), 'event references must be UUID strings')
    try:
        require(str(UUID(value)) == value, 'use canonical lowercase UUIDs')
    except ValueError as exc:
        raise JournalError('invalid UUID') from exc


def validate(record, stored=False):
    require(isinstance(record, dict), 'event must be an object')
    required = REQUIRED | (GENERATED if stored else set())
    require(required <= record.keys(), 'missing fields: ' + ', '.join(sorted(required - record.keys())))
    require(record.keys() <= required | OPTIONAL,
            'unknown or reserved fields: ' + ', '.join(sorted(record.keys() - required - OPTIONAL)))
    require(record['type'] in TYPES, 'unsupported event type')
    require(record['status'] in STATUSES, 'unsupported statement status')
    for field in ('actor', 'summary', 'revision'):
        require(nonempty(record[field]), field + ' must be a nonempty string')
    require(isinstance(record['sources'], list) and record['sources'] and
            all(nonempty(source) for source in record['sources']),
            'sources must contain at least one nonempty evidence reference')
    if record['status'] == 'approved':
        require('authority' in record, 'approved events require authority')
    if 'authority' in record:
        require(nonempty(record['authority']), 'authority must be a nonempty string')
    if record['type'] == 'verification':
        require('check' in record, 'verification requires check: command, scope, result')
    if 'check' in record:
        check = record['check']
        require(isinstance(check, dict) and set(check) == {'command', 'scope', 'result'}
                and all(nonempty(value) for value in check.values()),
                'check must contain nonempty command, scope and result strings')
    if 'supersedes' in record:
        uuid(record['supersedes'])
    if stored:
        require(type(record['schema_version']) is int and record['schema_version'] == 1,
                'unsupported schema_version')
        session_name(record['session_id'])
        uuid(record['event_id'])
        require(record.get('supersedes') != record['event_id'], 'event cannot supersede itself')
        stamp = record['recorded_at']
        require(isinstance(stamp, str) and stamp.endswith('Z'), 'recorded_at must be UTC ending in Z')
        try:
            datetime.strptime(stamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError as exc:
            raise JournalError('invalid recorded_at timestamp') from exc
    try:
        encode(record).encode('utf-8')
    except UnicodeError as exc:
        raise JournalError('event strings must be valid UTF-8') from exc
    return record


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def reject_constant(value):
    raise JournalError('invalid JSON constant: ' + value)


def decode(text):
    try:
        return json.loads(text, object_pairs_hook=unique_keys, parse_constant=reject_constant)
    except (ValueError, UnicodeError) as exc:
        raise JournalError(str(exc)) from exc


def encode(record):
    return json.dumps(record, ensure_ascii=False, allow_nan=False, separators=(',', ':')) + '\n'


def read_session(path):
    require(not path.is_symlink(), 'session file must not be a symlink: ' + str(path))
    records = []
    with path.open('rb') as stream:
        for number, line in enumerate(stream, 1):
            try:
                require(line.endswith(b'\n'), 'unterminated record; preserve file and inspect interrupted write')
                record = validate(decode(line.decode('utf-8')), stored=True)
                require(record['session_id'] == path.stem, 'session_id does not match filename')
                records.append(record)
            except (JournalError, UnicodeError) as exc:
                raise JournalError(f'{path}:{number}: {exc}') from exc
    return records


def read_events(directory, session=None):
    if session is not None:
        paths = [directory / (session_name(session) + '.jsonl')]
    else:
        require(directory.is_dir(), 'journal directory does not exist: ' + str(directory))
        paths = sorted(directory.glob('*.jsonl'))
    records = []
    seen = set()
    for path in paths:
        for record in read_session(path):
            require(record['event_id'] not in seen, 'duplicate event_id: ' + record['event_id'])
            seen.add(record['event_id'])
            records.append(record)
    return records


@contextmanager
def writer_lock(directory, session):
    """Exclusive creation rejects overlapping writers; never steal stale locks."""
    lock = directory / (session + '.lock')
    try:
        fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise JournalError(f'{lock}: session busy or stale lock; inspect before retrying') from exc
    try:
        os.close(fd)
        yield
    finally:
        lock.unlink()


def append_event(directory, session, payload):
    session_name(session)
    validate(payload)
    record = dict(payload, schema_version=1, event_id=str(uuid4()),
                  recorded_at=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                  session_id=session)
    # Encode before any filesystem change, including invalid Unicode rejection.
    data = encode(validate(record, stored=True)).encode('utf-8')
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / (session + '.jsonl')
    with writer_lock(directory, session):
        require(not path.is_symlink(), 'session file must not be a symlink: ' + str(path))
        if path.exists():
            read_events(directory, session)
        with path.open('ab') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, default=Path('.context/events'),
                        help='journal directory, relative to current working directory')
    commands = parser.add_subparsers(dest='command', required=True)
    append = commands.add_parser('append', help='validate and append one JSON object')
    append.add_argument('--session', required=True)
    append.add_argument('--input', type=Path, help='JSON input file; omit to read stdin')
    read = commands.add_parser('read', help='validate selected files and emit JSONL without modifying them')
    read.add_argument('--session', help='read just one session; otherwise read all sessions')
    read.add_argument('--type', choices=TYPES, help='filter output after validation')
    args = parser.parse_args(argv)
    try:
        if args.command == 'append':
            source = args.input.read_text(encoding='utf-8') if args.input else sys.stdin.read()
            records = [append_event(args.directory, args.session, decode(source))]
        else:
            records = read_events(args.directory, args.session)
            if args.type:
                records = [record for record in records if record['type'] == args.type]
        # Validate all selected history before emitting any records.
        for record in records:
            print(encode(record), end='')
    except (JournalError, OSError, UnicodeError) as exc:
        print(f'event-journal: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
