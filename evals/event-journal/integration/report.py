"""Mechanical report; authored semantic reviews remain a separate artifact."""
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('packaged_journal',ROOT/'skills/context-docs/scripts/event_journal.py')
journal=importlib.util.module_from_spec(spec);spec.loader.exec_module(journal)


def report(out):
    frozen=json.loads((out/'frozen.json').read_text());summary=[]
    for client in ('claude','codex'):
        trialsfile=out/(client+'-trials.json')
        if not trialsfile.exists():continue
        case=frozen['trajectories'][client]
        for trial in json.loads(trialsfile.read_text()):
            stage=trial['stage'];name=client+'-'+stage;project=out/name
            rows=[json.loads(l) for l in (out/(name+'-stream.jsonl')).read_text().splitlines()]
            calls=[];failures=[];model=None;terminal=False;final=''
            for event in rows:
                if event.get('type')=='system' and event.get('subtype')=='init':model=event.get('model')
                if event.get('type')=='assistant':
                    for block in event.get('message',{}).get('content',[]):
                        if block.get('type')=='tool_use':calls.append(block)
                if event.get('type')=='user':
                    for block in event.get('message',{}).get('content',[]):
                        if block.get('type')=='tool_result' and block.get('is_error'):failures.append(block)
                if event.get('type')=='result':
                    terminal=True;final=event.get('result','')
                if event.get('type')=='item.completed':
                    item=event.get('item',{})
                    if item.get('type') not in ('agent_message','reasoning'):calls.append(item)
                    if item.get('type')=='command_execution' and item.get('exit_code'):failures.append(item)
                if event.get('type')=='turn.completed':terminal=True
            if client=='claude':(out/(name+'-final.txt')).write_text(final)
            else:final=(out/(name+'-final.txt')).read_text() if (out/(name+'-final.txt')).exists() else ''
            hooksfile=out/(name+'-hooks.jsonl')
            hooks=[json.loads(l) for l in hooksfile.read_text().splitlines()] if hooksfile.exists() else []
            pre=[h for h in hooks if h.get('hook_event_name')=='PreToolUse']
            loaded=[h for h in hooks if h.get('hook_event_name')=='InstructionsLoaded' and Path(h.get('file_path','')).name==case['instruction']]
            records=journal.read_events(project/'history/events')
            new=[r for r in records if r['session_id']!='legacy']
            instructions=(project/case['instruction']).read_text()
            original=(out/(client+'-upgraded')/case['instruction']).read_text()
            stripped=re.sub(r'^Event journal(?: directory)?:[^\n]*\n','',instructions,flags=re.M)
            summary.append({'client':client,'stage':stage,'exit_code':trial['exit_code'],'terminal':terminal,
                'model_from_stream':model,'seconds':trial['seconds'],'protected_unchanged':trial['protected_unchanged'],
                'legacy_unchanged':trial['legacy_unchanged'],'all_bytes_unchanged':trial['all_bytes_unchanged'],
                'journal_unchanged':trial['journal_unchanged'],'instruction_text_except_settings_unchanged':stripped==original,
                'logging_setting':next(iter(re.findall(r'^Event journal: (.+)$',instructions,re.M)),'absent'),
                'journal_records':len(records),'new_records':len(new),'new_record_actors':sorted({e['actor'] for e in new}),
                'journal_bytes':sum(p.stat().st_size for p in (project/'history/events').glob('*.jsonl')),
                'changed_files':sorted(k for k in set(trial['before'])|set(trial['after']) if trial['before'].get(k)!=trial['after'].get(k)),
                'tool_calls':calls,'tool_failures':failures,'guard_denials':[h for h in pre if not h['allowed']],
                'guard_covers_calls':sorted(h.get('tool_use_id') for h in pre)==sorted(c['id'] for c in calls) if client=='claude' else None,
                'instruction_load_events':loaded})
    (out/'mechanical-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    lines=['| Client / stage | Seconds | Tools | Journal records | Setting | Project bytes unchanged |',
           '| --- | ---: | ---: | ---: | --- | --- |']
    for row in summary:
        lines.append(f"| {row['client']} / {row['stage']} | {row['seconds']} | {len(row['tool_calls'])} | {row['journal_records']} | {row['logging_setting']} | {row['all_bytes_unchanged']} |")
        print(row['client'],row['stage'],'records',row['journal_records'],'setting',row['logging_setting'],
              'preserved',row['protected_unchanged'] and row['legacy_unchanged'],'unchanged',row['all_bytes_unchanged'])
    (out/'table.md').write_text('\n'.join(lines)+'\n')


if __name__=='__main__':report(Path(sys.argv[1]).resolve())
