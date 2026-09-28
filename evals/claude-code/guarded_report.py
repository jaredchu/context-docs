"""Regenerate integration and semantic summaries without running a model."""
import argparse
import json
from pathlib import Path

import guarded
from paired import dump


def report(destination):
    protocol=json.loads((destination/'protocol.json').read_text())
    trials=json.loads((destination/'trials.json').read_text())
    reviews=json.loads((destination/'reviews.json').read_text())['sessions']
    expected=[s['id'] for s in protocol['sessions']]
    complete=[t['id'] for t in trials]==expected
    rows=[]
    for trial in trials:
        sid=trial['id']; review=reviews[sid]
        assert type(review['accepted']) is bool and review['evidence'].strip()
        if 'criteria' in review:
            assert all(type(value) is bool for value in review['criteria'])
            assert all(review['criteria'])==review['accepted']
        replay=guarded.coverage(destination/'logs'/f'{sid}.jsonl',trial['events'],protocol['exposed_tools'])
        assert all(trial['checks'][name]==value for name,value in replay.items()), sid
        rows.append(dict(session=sid, integration=all(trial['checks'].values()),
                         failed_checks=[name for name,ok in trial['checks'].items() if not ok],
                         semantic=review['accepted'], execution_error=trial['observed']['execution_error'],
                         denied_calls=sum(e.get('decision')=='deny' for e in trial['events'])))
    mapping={t['id']:t for t in trials}
    fresh=(complete and mapping['front-door-refresh']['after_hashes']==
           mapping['fresh-rule-audit']['before_hashes']==mapping['fresh-rule-audit']['after_hashes'])
    summary=dict(sessions=len(rows), complete=complete, integration_passed=sum(r['integration'] for r in rows),
                 semantic_passed=sum(r['semantic'] for r in rows), fresh_rule_preserved=fresh,
                 integration_gate_passed=complete and fresh and all(r['integration'] for r in rows))
    dump(destination/'summary.json',dict(summary=summary,rows=rows))
    table=['| Session | Integration checks | Semantic review | Denied calls |',
           '| --- | --- | --- | ---: |']
    for row in rows:
        table.append(f'| {row["session"]} | {"pass" if row["integration"] else "fail"} | '
                     f'{"pass" if row["semantic"] else "fail"} | {row["denied_calls"]} |')
    (destination/'table.md').write_text('\n'.join(table)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('destination',type=Path)
    report(parser.parse_args().destination)
