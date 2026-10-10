"""Count full-file retrieval at PreToolUse; no code execution in subject sessions."""
import json
import fcntl
import time
from pathlib import Path
import guard_hook

TOOLS = ('Read', 'Write', 'Edit', 'Glob', 'Grep')

def decision(event, config):
    name,payload=event['tool_name'],event.get('tool_input') or {}
    root=Path(config['project']).resolve()
    if name not in TOOLS:
        return 'deny','Only frozen file tools are available.'
    value=payload.get('file_path') if name in ('Read','Write','Edit') else payload.get('path',str(root))
    if not isinstance(value,str) or not value:
        return 'deny','Invalid path.'
    path=(root/value).resolve()
    if not guard_hook.within(path,root):
        return 'deny','Outside project boundary.'
    if name=='Glob' and (Path(payload.get('pattern','')).is_absolute() or '..' in Path(payload.get('pattern','')).parts):
        return 'deny','Escaping glob.'
    if name=='Grep' and payload.get('output_mode','files_with_matches')!='files_with_matches':
        return 'deny','Search returns filenames only; load content with budgeted Read.'
    if name in ('Write','Edit'):
        if str(path.relative_to(root)) not in config['writable']:
            return 'deny','Outside frozen editable scope.'
        if path.exists() and (not path.is_file() or path.stat().st_nlink>1):
            return 'deny','Requires an ordinary unlinked file.'
        return 'allow','Authorized patch.'
    if not config.get('budget'):
        return 'allow','Read-only review or bounded authoring.'
    if name=='Read' and any(k in payload for k in ('limit','offset','pages')):
        return 'deny','Read complete UTF-8 text files; no partial reads.'
    if name=='Read' and (not path.is_file() or path.suffix not in ('.md','.py','.json')):
        return 'deny','Read requires a fixture text file.'
    # Event recorder serializes tool calls in this file-only session. Count prior
    # admitted retrievals, including failed calls conservatively, from our own log.
    events_path=Path(config['events'])
    prior=[json.loads(line) for line in events_path.read_text().splitlines()] if events_path.exists() else []
    prior=[e for e in prior if e.get('hook_event_name')=='PreToolUse' and e.get('decision')=='allow']
    reads=sum(e.get('tool_name')=='Read' for e in prior)
    searches=sum(e.get('tool_name') in ('Glob','Grep') for e in prior)
    loaded=sum(e.get('retrieval_bytes',0) for e in prior)
    cost=path.stat().st_size if name=='Read' else 0
    budget=config['budget']
    if name=='Read' and (reads>=budget['reads'] or loaded+cost>budget['bytes']):
        return 'deny',f"Frozen retrieval budget exhausted: {reads} reads, {loaded} bytes; request {cost} bytes."
    if name in ('Glob','Grep') and searches>=budget['searches']:
        return 'deny','Frozen filename-search budget exhausted.'
    return 'allow',f'Budgeted retrieval: charge {cost} bytes.'

original_handle=guard_hook.handle

def handle(event,config):
    if event.get('hook_event_name')!='PreToolUse':
        return original_handle(event,config)
    # Decision+reservation must be atomic even when Claude calls tools in parallel.
    with Path(config['events']+'.budget.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        verdict,reason=decision(event,config)
        payload=event.get('tool_input') or {}
        root=Path(config['project']).resolve()
        path=(root/payload.get('file_path','')).resolve()
        name=event.get('tool_name')
        record=dict(hook_event_name='PreToolUse',observed_at_ns=time.time_ns(),session_id=event.get('session_id'),tool_use_id=event.get('tool_use_id'),tool_name=name,tool_input=payload,decision=verdict,reason=reason,retrieval_bytes=path.stat().st_size if verdict=='allow' and name=='Read' and path.is_file() else 0)
        guard_hook.append(config['events'],record)
        return dict(hookSpecificOutput=dict(hookEventName='PreToolUse',permissionDecision=verdict,permissionDecisionReason=reason))

if __name__=='__main__':
    guard_hook.decision=decision
    guard_hook.handle=handle
    guard_hook.main()
