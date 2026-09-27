"""Aggregate frozen answer reviews and measured exposure separately."""
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import run


def summarize(trials,reviews,exposures):
    assert len(trials)==12 and len(reviews)==72 and len(exposures)==12
    expected_grid={(m,w,a) for m in run.MODES for w in run.base.CASES for a in run.base.ARMS}
    assert {(t['metadata']['mode'],t['metadata']['world'],t['metadata']['arm']) for t in trials}==expected_grid
    rev={(r['trial_id'],r['id']):r for r in reviews}; exp={r['trial_id']:r for r in exposures}
    assert len(rev)==72 and set(exp)=={t['id'] for t in trials}
    scores=[];expected=set()
    for t in trials:
        step=t['steps'][0];m=t['metadata']
        for q in run.base.CASES[m['world']]['questions']:
            key=t['id'],q['id'];expected.add(key);r=rev[key]
            assert len(r['criteria'])==2 and all(type(x)==bool for x in r['criteria'])
            assert type(r['supported'])==bool and type(r['material_error'])==bool and r['evidence'].strip()
            passed=bool(step['observed'] and step['observed']['mechanical_pass'] and not step['execution_error'] and all(r['criteria']) and r['supported'] and not r['material_error'])
            scores.append(dict(trial_id=t['id'],mode=m['mode'],world=m['world'],arm=m['arm'],question=q['id'],passed=passed))
    assert expected==set(rev)
    rows=[]
    for mode in run.MODES:
        for world in [*run.base.CASES,'all']:
            for arm in run.base.ARMS:
                ts=[t for t in trials if t['metadata']['mode']==mode and t['metadata']['arm']==arm and (world=='all' or t['metadata']['world']==world)]
                ss=[s for s in scores if s['mode']==mode and s['arm']==arm and (world=='all' or s['world']==world)]
                rows.append(dict(mode=mode,world=world,arm=arm,correct=sum(s['passed'] for s in ss),answers=len(ss),sessions=len(ts),
                    readme_exposed=sum(exp[t['id']].get('readme',{}).get('full_text_exposed',False) for t in ts),
                    target_exposed=sum(exp[t['id']].get('target',{}).get('full_text_exposed',False) for t in ts)))
    lines=['| Reader mode and outcome | Upstream orientation | Ordinary handoff | Context Docs handoff |','| --- | ---: | ---: | ---: |']
    for mode in run.MODES:
        rs=[next(r for r in rows if r['mode']==mode and r['world']=='all' and r['arm']==a) for a in run.base.ARMS]
        label='README-first discovery' if mode=='discovery' else 'Directed reading'
        lines.append('| '+label+': supported answers | '+' | '.join(f'{r["correct"]}/{r["answers"]}' for r in rs)+' |')
        lines.append('| '+label+': full orientation text exposed | '+' | '.join(f'{r["target_exposed"]}/{r["sessions"]}' for r in rs)+' |')
    return dict(rows=rows,answer_scores=scores),'\n'.join(lines)+'\n'


def selftest():
    trials=[];reviews=[];exposures=[]
    for mode in run.MODES:
        for world in run.base.CASES:
            for arm in run.base.ARMS:
                tid=f'{mode}-{world}-{arm}'
                trials.append(dict(id=tid,metadata=dict(mode=mode,world=world,arm=arm),steps=[dict(observed=dict(mechanical_pass=True),execution_error=None)]))
                exposures.append(dict(trial_id=tid,readme=dict(full_text_exposed=True),target=dict(full_text_exposed=False)))
                for q in run.base.CASES[world]['questions']:
                    reviews.append(dict(trial_id=tid,id=q['id'],criteria=[True,True],supported=True,material_error=False,evidence='Reference control.'))
    summary,_=summarize(trials,reviews,exposures)
    assert sum(s['passed'] for s in summary['answer_scores'])==72
    assert not any(r['target_exposed'] for r in summary['rows'])
    reviews[0]['criteria'][1]=False;reviews[1]['supported']=False;reviews[2]['material_error']=True
    summary,_=summarize(trials,reviews,exposures)
    assert sum(s['passed'] for s in summary['answer_scores'])==69
    trials[0]['steps'][0]['execution_error']='Timeout'
    summary,_=summarize(trials,reviews,exposures)
    assert sum(s['passed'] for s in summary['answer_scores'])==66
    print('Report controls passed: answer/exposure separation, omission, unsupported claim, material error and execution failure.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('trials',type=Path);p.add_argument('reviews',type=Path);p.add_argument('exposures',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    trials=json.loads(a.trials.read_text());reviews=json.loads(a.reviews.read_text());exposures=json.loads(a.exposures.read_text())
    summary,table=summarize(trials,reviews,exposures)
    clean=json.loads(json.dumps(trials))
    for t in clean:
        for s in t['steps']:s.pop('tool_calls',None)
    for name,data in [('trials.json',clean),('reviews.json',reviews),('exposure.json',exposures),('summary.json',summary)]:run.base.dump(a.output/name,data)
    run.base.write(a.output/'table.md',table);print(table)
