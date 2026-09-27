"""Conservative full-text exposure detection from model-visible tool responses."""
import hashlib
import json
from pathlib import Path


def visible_text(value):
    if isinstance(value, str):
        try:
            parsed=json.loads(value)
        except (ValueError, TypeError):
            return value
        return visible_text(parsed) if isinstance(parsed,(dict,list)) else value
    if isinstance(value, list):
        return '\n'.join(visible_text(v) for v in value)
    if isinstance(value, dict):
        # Codex output content blocks and JSON-encoded exec results.
        if 'text' in value: return visible_text(value['text'])
        if 'output' in value: return visible_text(value['output'])
    return ''


def coverage(body, blocks):
    expected={line.strip() for line in body.splitlines() if line.strip()}
    seen=set(); evidence=[]
    for index,text in blocks:
        lines={line.strip() for line in text.splitlines() if line.strip()}
        matched=expected & lines
        if matched:
            seen |= matched
            evidence.append(dict(event_index=index,matched_unique_lines=len(matched),visible_text_sha256=hashlib.sha256(text.encode()).hexdigest()))
    missing=expected-seen
    return dict(full_text_exposed=bool(expected) and not missing,
        expected_unique_nonblank_lines=len(expected),matched_unique_nonblank_lines=len(seen),
        missing_line_numbers=[i+1 for i,line in enumerate(body.splitlines()) if line.strip() in missing],
        first_line_seen=body.splitlines()[0].strip() in seen,evidence=evidence)


def audit(session, files, target):
    events=[json.loads(s) for s in session.read_text().splitlines()]
    blocks=[]; answer_event=None; calls=[]
    for i,e in enumerate(events):
        p=e.get('payload',{})
        if e.get('type')!='response_item': continue
        if p.get('type') in ['custom_tool_call','function_call']:
            command=str(p.get('input',p.get('arguments','')))
            # Stop before the first call referring to the answer artifact, including
            # a premature create/validation call. This favors false negatives.
            if 'answers.json' in command:
                answer_event=i;break
            calls.append(dict(event_index=i,name=p.get('name'),input=command))
        elif p.get('type') in ['custom_tool_call_output','function_call_output']:
            blocks.append((i,visible_text(p.get('output'))))
    return dict(answer_artifact_call_event=answer_event,
        readme=coverage(files['README.md'],blocks),target=coverage(files[target],blocks),
        target_path=target,source_calls=calls)


def selftest():
    body='# Handoff\n\nUnique fact alpha.\nUnique fact beta.\n'
    assert not coverage(body,[])['full_text_exposed']
    assert not coverage(body,[(1,'CONTEXT.md')])['full_text_exposed']
    assert not coverage(body,[(1,'# Handoff\nUnique fact alpha.')])['full_text_exposed']
    assert coverage(body,[(1,'# Handoff\nUnique fact alpha.'),(3,'Unique fact beta.')])['full_text_exposed']
    assert coverage(body,[(1,body)])['full_text_exposed']
    payload=[{'type':'input_text','text':json.dumps({'output':body,'exit_code':0})}]
    assert visible_text(payload)==body
    assert visible_text('raw output')=='raw output'
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        session=Path(tmp)/'session.jsonl'
        def event(kind, **values): return dict(type='response_item',payload=dict(type=kind,**values))
        read=event('custom_tool_call_output',output=payload)
        answer=event('custom_tool_call',input="write('/output/answers.json')")
        files={'README.md':body,'context.md':body}
        session.write_text('\n'.join(json.dumps(e) for e in [read,answer]))
        assert audit(session,files,'context.md')['target']['full_text_exposed']
        session.write_text('\n'.join(json.dumps(e) for e in [answer,read]))
        assert not audit(session,files,'context.md')['target']['full_text_exposed']
    print('9 exposure controls passed (listing, partial, split/full text, decoding and answer ordering).')
