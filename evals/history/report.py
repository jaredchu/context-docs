"""Report explicit semantic reviews; mechanical checks and exposure remain separate."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import study
STATUSES=['correct','missing','incorrect','conflicting']

def summarize(snaps,trials,documents,readers,exposure):
    assert len(snaps)==24 and len(trials)==12 and len(documents)==24 and len(readers)==96 and len(exposure)==12
    assert {(s['world'],s['arm'],s['stage']) for s in snaps}=={(w,a,s) for w in study.CASES for a in study.ARMS for s in range(4)}
    assert {(t['metadata']['world'],t['metadata']['arm'],t['metadata']['variant']) for t in trials}=={(w,a,v) for w in study.CASES for a in study.ARMS for v in range(2)}
    dr={r['snapshot_id']:r for r in documents};rr={(r['trial_id'],r['id']):r for r in readers};ex={r['trial_id']:r for r in exposure}
    assert set(dr)=={s['id'] for s in snaps} and len(dr)==24 and len(rr)==96 and set(ex)=={t['id'] for t in trials}
    ds=[];rs=[];wanted=set()
    for s in snaps:
        review=dr[s['id']];expected={f['id'] for f in study.ledger(s['world'],s['stage'])}
        assert set(review['items'])==expected and isinstance(review['findings'],list)
        for f in review['findings']:assert f['severity'] in ['critical','minor'] and f['detail'].strip()
        for k,r in review['items'].items():
            assert r['status'] in STATUSES and r['evidence'].strip()
            ds.append(dict(snapshot_id=s['id'],world=s['world'],arm=s['arm'],stage=s['stage'],item=k,status=r['status'],passed=r['status']=='correct' and bool(s['mechanical_pass']) and not s['execution_error']))
    for t in trials:
        for q in study.CASES[t['metadata']['world']]['questions']:
            key=t['id'],q['id'];wanted.add(key);r=rr[key]
            assert all(type(r[k])==bool for k in ['correct','supported','critical']) and r['evidence'].strip()
            step=t['steps'][0]
            rs.append(dict(trial_id=t['id'],world=t['metadata']['world'],arm=t['metadata']['arm'],variant=t['metadata']['variant'],question=q['id'],passed=bool(step['observed'] and step['observed']['mechanical_pass'] and not step['execution_error'] and r['correct'] and r['supported'] and not r['critical'])))
    assert wanted==set(rr)
    rows=[]
    for world in [*study.CASES,'all']:
        for arm in study.ARMS:
            ss=[s for s in snaps if s['arm']==arm and (world=='all' or s['world']==world)]
            dd=[d for d in ds if d['arm']==arm and (world=='all' or d['world']==world)];final=[d for d in dd if d['stage']==3]
            aa=[r for r in rs if r['arm']==arm and (world=='all' or r['world']==world)]
            tt=[t for t in trials if t['metadata']['arm']==arm and (world=='all' or t['metadata']['world']==world)]
            pairkeys={(a['world'],a['question']) for a in aa}
            losses=[]
            for d in dd:
                if d['stage']==0:continue
                previous=next((p for p in dd if p['stage']==d['stage']-1 and p['world']==d['world'] and p['item']==d['item']),None)
                if previous and previous['passed'] and not d['passed']:losses.append(dict(world=d['world'],stage=d['stage'],item=d['item']))
            finals=[s for s in ss if s['stage']==3]
            stable=sum({p:b for p,b in s['files'].items() if p.endswith('.md')}=={p:b for p,b in next(x for x in ss if x['world']==s['world'] and x['stage']==2)['files'].items() if p.endswith('.md')} for s in finals)
            rows.append(dict(world=world,arm=arm,final_correct=sum(d['passed'] for d in final),final_items=len(final),all_stage_correct=sum(d['passed'] for d in dd),all_stage_items=len(dd),final_status_counts={status:sum(d['status']==status for d in final) for status in STATUSES},critical_document_findings=sum(f['severity']=='critical' for s in ss for f in dr[s['id']]['findings']),durability_losses=losses,correct_answers=sum(a['passed'] for a in aa),answers=len(aa),correct_pairs=sum(all(a['passed'] for a in aa if (a['world'],a['question'])==key) for key in pairkeys),pairs=len(pairkeys),fully_exposed_readers=sum(ex[t['id']]['all_markdown_exposed'] for t in tt),readers=len(tt),unchanged_final_passes=stable,final_passes=len(finals),final_markdown_words=sum(len(b.split()) for s in finals for p,b in s['files'].items() if p.endswith('.md'))))
    allrows=[r for r in rows if r['world']=='all']
    table=['| Outcome | Unmaintained | Ordinary maintenance | Context Docs v0.1.1 |','| --- | ---: | ---: | ---: |']
    metrics=[('Required knowledge in final context','final_correct','final_items'),('Required knowledge across all stages','all_stage_correct','all_stage_items'),('Correct, supported reader answers','correct_answers','answers'),('Correct in both reader sessions','correct_pairs','pairs'),('Readers exposed to all Markdown','fully_exposed_readers','readers')]
    for label,n,d in metrics:table.append('| '+label+' | '+' | '.join(f'{r[n]}/{r[d]}' for r in allrows)+' |')
    table.append('| Critical document findings across stages | '+' | '.join(str(r['critical_document_findings']) for r in allrows)+' |')
    return dict(rows=rows,document_scores=ds,reader_scores=rs),'\n'.join(table)+'\n'

def selftest():
    snaps=[];trials=[];docs=[];readers=[];ex=[]
    for w in study.CASES:
        for a in study.ARMS:
            for s in range(4):
                sid=f'{w}-{a}-{s}';snaps.append(dict(id=sid,world=w,arm=a,stage=s,files=study.reference(w,s),mechanical_pass=True,execution_error=None))
                docs.append(dict(snapshot_id=sid,items={f['id']:dict(status='correct',evidence='Reference control.') for f in study.ledger(w,s)},findings=[]))
            for v in range(2):
                tid=f'{w}-{a}-{v}';trials.append(dict(id=tid,metadata=dict(world=w,arm=a,variant=v),steps=[dict(observed=dict(mechanical_pass=True),execution_error=None)]));ex.append(dict(trial_id=tid,all_markdown_exposed=False))
                for q in study.CASES[w]['questions']:readers.append(dict(trial_id=tid,id=q['id'],correct=True,supported=True,critical=False,evidence='Reference control.'))
    summary,_=summarize(snaps,trials,docs,readers,ex);assert sum(r['passed'] for r in summary['reader_scores'])==96
    assert not any(r['fully_exposed_readers'] for r in summary['rows'])
    readers[0]['correct']=False;readers[1]['supported']=False;readers[2]['critical']=True
    docs[0]['items']['authority']['status']='incorrect';docs[1]['items']['rationale']['status']='missing';docs[2]['items']['scope']['status']='conflicting'
    summary,_=summarize(snaps,trials,docs,readers,ex);assert sum(r['passed'] for r in summary['reader_scores'])==93
    assert sum(not r['passed'] for r in summary['document_scores'])==3
    trials[0]['steps'][0]['execution_error']='Timeout';summary,_=summarize(snaps,trials,docs,readers,ex);assert sum(r['passed'] for r in summary['reader_scores'])==88
    print('Scoring controls passed: omission, unsupported claims, critical errors, conflicts, timeout and exposure separation.')

if __name__=='__main__':
    if len(sys.argv)==2 and sys.argv[1]=='selftest':selftest()
    else:
        root=Path(sys.argv[1]);load=lambda name:json.loads((root/name).read_text())
        summary,table=summarize(load('snapshots.json'),load('reader-trials.json'),load('document-reviews.json'),load('reader-reviews.json'),load('exposure.json'))
        study.dump(root/'summary.json',summary);study.write(root/'table.md',table);print(table)
