"""Evaluation-only hook: observe loading and constrain the exposed file tools.

Not an OS sandbox. Bash, delegation, network and other tools must be excluded by
the caller. Config, this script and event logs live outside the model-write root.
"""
import fcntl
import hashlib
import json
import os
import sys
import time
from pathlib import Path

TOOLS = ('Read', 'Write', 'Edit', 'Glob', 'Grep', 'Skill')


def within(path, root):
    return path == root or root in path.parents


def decision(event, config):
    root = Path(config['project']).resolve()
    name, payload = event['tool_name'], event.get('tool_input') or {}
    if name not in TOOLS:
        return 'deny', 'This evaluation exposes file tools only; execution and other tools are disabled.'
    if name == 'Skill':
        if payload.get('skill') not in ('context-docs', 'adopt-context-docs'):
            return 'deny', 'Only the two frozen installed skills are allowed.'
        return 'allow', 'Frozen installed skill.'
    value = payload.get('file_path') if name in ('Read', 'Write', 'Edit') else payload.get('path', str(root))
    if not isinstance(value, str) or not value:
        return 'deny', 'Missing or invalid path.'
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    resolved = path.resolve()
    if not within(resolved, root):
        return 'deny', 'Outside the evaluation project boundary.'
    if name == 'Glob':
        pattern = payload.get('pattern', '')
        if Path(pattern).is_absolute() or '..' in Path(pattern).parts:
            return 'deny', 'Glob patterns must stay relative to the project.'
    if name in ('Write', 'Edit'):
        if config.get('read_only'):
            return 'deny', 'This session is read-only.'
        relative = str(resolved.relative_to(root))
        if relative in config['immutable'] or relative.split('/')[0] in ('.git', '.claude'):
            return 'deny', 'Protected fixture or evaluation installation.'
        if resolved == root or resolved.suffix != '.md':
            return 'deny', 'This documentation evaluation permits Markdown edits only.'
        if resolved.exists() and (not resolved.is_file() or resolved.stat().st_nlink > 1):
            return 'deny', 'Only ordinary, unlinked project files may be edited.'
    return 'allow', 'Within the evaluation file-tool policy.'


def append(path, record):
    with Path(path).open('a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        stream.write(json.dumps(record) + '\n')
        stream.flush()
        os.fsync(stream.fileno())


def handle(event, config):
    name = event['hook_event_name']
    record = {k: event[k] for k in ('hook_event_name', 'session_id', 'tool_use_id',
              'file_path', 'memory_type', 'load_reason', 'trigger_file_path', 'parent_file_path') if k in event}
    record['observed_at_ns'] = time.time_ns()
    output = None
    if name == 'InstructionsLoaded':
        path = Path(event['file_path'])
        # Record only the hash, never contents of a host instruction file.
        record['file_sha256_at_event'] = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
    elif name == 'PreToolUse':
        verdict, reason = decision(event, config)
        record.update(tool_name=event['tool_name'], tool_input=event.get('tool_input'),
                      decision=verdict, reason=reason)
        output = dict(hookSpecificOutput=dict(hookEventName=name, permissionDecision=verdict,
                                             permissionDecisionReason=reason))
    elif name in ('PostToolUse', 'PostToolUseFailure'):
        record.update(tool_name=event.get('tool_name'), error=event.get('error'))
    append(config['events'], record)
    return output


def main():
    try:
        config = json.loads(Path(sys.argv[1]).read_text())
        event = json.load(sys.stdin)
        output = handle(event, config)
        if output is not None:
            print(json.dumps(output))
    except Exception:
        # Exit 2 blocks PreToolUse rather than silently approving on parser/error paths.
        print('Evaluation hook failed; tool use is blocked.', file=sys.stderr)
        raise SystemExit(2)


if __name__ == '__main__':
    main()
