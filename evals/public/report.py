"""Validate explicit author reviews and render public results, never infer semantic scores."""
import argparse
import json
from pathlib import Path
from study import CASES, ARMS, dump, digest


def summarize(maintenance, readers, reviews):
    assert len(maintenance)==4 and len(readers)==12
    ds={r['trial_id']:r for r in reviews['documents']}
    ars={(r['trial_id'],r['id']):r for r in reviews['answers']}
    assert len(ds)==len(reviews['documents'])==4 and len(ars)==len(reviews['answers'])==72
    expected=set(); rows=[]; scores=[]
    for t in maintenance:
        review=ds[t['id']]; items=review['items']
        assert {r['id'] for r in items}=={f'{q["id"]}.{i+1}' for q in CASES[t['metadata']['world']]['questions'] for i in range(2)}
        assert len(items)==12 and all(r['status'] in ['accurate','missing','incorrect','conflicting'] and r['evidence'].strip() for r in items)
    for t in readers:
        for q in CASES[t['metadata']['world']]['questions']:
            key=(t['id'],q['id']);expected.add(key);r=ars[key]
            assert len(r['criteria'])==2 and all(type(x)==bool for x in r['criteria'])
            assert type(r['supported'])==bool and type(r['material_error'])==bool and r['evidence'].strip()
            s=t['steps'][0]
            passed=bool(s['observed'] and s['observed']['mechanical_pass'] and not s['execution_error'] and all(r['criteria']) and r['supported'] and not r['material_error'])
            scores.append(dict(trial_id=t['id'],world=t['metadata']['world'],arm=t['metadata']['arm'],variant=t['metadata']['variant'],question=q['id'],passed=passed))
    assert expected==set(ars)
    for world in [*CASES,'all']:
        for arm in ARMS:
            r=[s for s in scores if s['arm']==arm and (world=='all' or s['world']==world)]
            pairs={(s['world'],s['question']) for s in r}
            trials=[t for t in maintenance if t['metadata']['arm']==arm and (world=='all' or t['metadata']['world']==world)]
            items=[x for t in trials for x in ds[t['id']]['items']]
            rows.append(dict(world=world,arm=arm,correct=sum(s['passed'] for s in r),answers=len(r),
                correct_pairs=sum(all(s['passed'] for s in r if (s['world'],s['question'])==p) for p in pairs),pairs=len(pairs),
                handoff_items={status:sum(x['status']==status for x in items) for status in ['accurate','missing','incorrect','conflicting']} if items else None,
                additional_findings=sum(len(ds[t['id']]['findings']) for t in trials) if trials else None))
    lines=['| Reader outcome | Upstream docs/code | Ordinary handoff | Context Docs v0.1.1 |','| --- | ---: | ---: | ---: |']
    for world in [*CASES,'all']:
        data=[next(r for r in rows if r['world']==world and r['arm']==a) for a in ARMS]
        lines.append('| '+('**Total**' if world=='all' else world.title())+' | '+' | '.join(f'{r["correct"]}/{r["answers"]}' for r in data)+' |')
    data=[next(r for r in rows if r['world']=='all' and r['arm']==a) for a in ARMS]
    lines.append('| Correct in both phrasings | '+' | '.join(f'{r["correct_pairs"]}/{r["pairs"]}' for r in data)+' |')
    return dict(rows=rows,answer_scores=scores), '\n'.join(lines)+'\n'


def publish(maint_dir,read_dir,review_path,output):
    maintenance=json.loads((maint_dir/'trials.json').read_text()); readers=json.loads((read_dir/'trials.json').read_text());reviews=json.loads(review_path.read_text())
    summary,table=summarize(maintenance,readers,reviews)
    for kind,trials in [('maintenance',maintenance),('readers',readers)]:
        clean=json.loads(json.dumps(trials))
        for t in clean:
            for s in t['steps']:
                s.pop('tool_calls',None)  # raw sessions remain local
                observed=s['observed']
                if observed and 'files' in observed:
                    observed['files_sha256']=digest(observed.pop('files'))
        dump(output/(kind+'.json'),clean)
    dump(output/'reviews.json',reviews);dump(output/'summary.json',summary)
    output.mkdir(parents=True,exist_ok=True);(output/'table.md').write_text(table)
    print(table)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('maintenance',type=Path);p.add_argument('readers',type=Path);p.add_argument('reviews',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();publish(a.maintenance,a.readers,a.reviews,a.output)
