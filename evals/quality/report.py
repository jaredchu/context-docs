"""Aggregate explicit human/assistant semantic reviews; never infer correctness from strings."""
import argparse
import json
from pathlib import Path
from fixtures import CASES,ARMS,QUESTIONS,ledger

STATUSES=('correct','missing','incorrect','conflicting')


def checked_document(snapshot,review):
    ids={f['id'] for f in ledger(snapshot['world'],snapshot['stage'])}
    assert set(review['statuses'])==ids
    assert all(v in STATUSES for v in review['statuses'].values())
    accounted=set()
    for evidence in review['evidence']:
        assert evidence['reason'].strip() and evidence['items']
        assert set(evidence['items'])<=ids
        assert all(p in snapshot['files'] for p in evidence['paths'])
        accounted.update(evidence['items'])
    assert accounted==ids,'Every semantic grade requires a specific supporting explanation.'
    assert all(isinstance(v,str) and v.strip() for v in review['critical_errors'])
    counts={s:list(review['statuses'].values()).count(s) for s in STATUSES}
    return dict(snapshot_id=snapshot['id'],case=snapshot['case'],world=snapshot['world'],condition=snapshot['condition'],arm=snapshot['arm'],stage=snapshot['stage'],mechanical_pass=snapshot['mechanical_pass'],**counts,critical_errors=len(review['critical_errors']),additional_findings=review['additional_findings'])


def summarize(snapshots,document_reviews,readers,reader_reviews):
    expected={(c['id'],a,s) for c in CASES for a in ARMS for s in range(3)}
    assert len(snapshots)==54 and {(s['case'],s['arm'],s['stage']) for s in snapshots}==expected
    docrows=[checked_document(s,document_reviews[s['id']]) for s in snapshots]
    assert len(readers)==36
    assert {(t['metadata']['case'],t['metadata']['arm'],t['metadata']['variant']) for t in readers}=={(c['id'],a,v) for c in CASES for a in ARMS for v in range(2)}
    readerrows=[]
    for trial in readers:
        m=trial['metadata'];assert len(trial['steps'])==1
        step=trial['steps'][0];r=reader_reviews[step['review_id']]
        assert set(r['answers'])=={q[0] for q in QUESTIONS[m['world']]}
        mechanical=bool(step['observed'] and step['observed']['mechanical_pass'] and not step['execution_error'])
        for q in QUESTIONS[m['world']]:
            answer=r['answers'][q[0]]
            assert type(answer['correct']) is bool and type(answer['supported']) is bool
            assert type(answer['critical_error']) is bool and answer['reason'].strip()
            readerrows.append(dict(case=m['case'],world=m['world'],condition=m['condition'],arm=m['arm'],variant=m['variant'],question=q[0],correct=answer['correct'],supported=answer['supported'],mechanical_pass=mechanical,passed=mechanical and answer['correct'] and answer['supported'],critical_error=answer['critical_error']))
    def group(arm,case=None,condition=None):
        docs=[d for d in docrows if d['arm']==arm and d['stage']==2 and (case is None or d['case']==case) and (condition is None or d['condition']==condition)]
        answers=[r for r in readerrows if r['arm']==arm and (case is None or r['case']==case) and (condition is None or r['condition']==condition)]
        paired={}
        for r in answers: paired.setdefault((r['case'],r['question']),[]).append(r['passed'])
        assert all(len(v)==2 for v in paired.values())
        correct=sum(d['correct'] for d in docs); missing=sum(d['missing'] for d in docs)
        wrong=sum(d['incorrect'] for d in docs);conflicts=sum(d['conflicting'] for d in docs)
        denominator=correct+wrong+conflicts
        return dict(document_snapshots=len(docs),required_knowledge_correct=correct,required_knowledge_total=9*len(docs),missing_items=missing,incorrect_items=wrong,conflicting_items=conflicts,target_claim_accuracy=correct/denominator if denominator else None,critical_document_errors=sum(d['critical_errors'] for d in docs),reader_answers_passed=sum(r['passed'] for r in answers),reader_answers_total=len(answers),reader_critical_errors=sum(r['critical_error'] for r in answers),consistent_correct_pairs=sum(all(v) for v in paired.values()),reader_pairs=len(paired))
    result={'by_arm':{a:group(a) for a in ARMS},'by_condition':{c:{a:group(a,condition=c) for a in ARMS} for c in ['scattered','conflicting','absent']},'by_case':{c['id']:{a:group(a,case=c['id']) for a in ARMS} for c in CASES}}
    result['stages']={str(s):{a:{k:sum(d[k] for d in docrows if d['arm']==a and d['stage']==s) for k in ['correct','missing','incorrect','conflicting','critical_errors']} for a in ARMS} for s in range(3)}
    losses=[]
    for c in CASES:
        for a in ARMS:
            seq=[s for s in snapshots if s['case']==c['id'] and s['arm']==a]
            seq.sort(key=lambda s:s['stage'])
            for previous,current in zip(seq,seq[1:]):
                before=document_reviews[previous['id']]['statuses'];after=document_reviews[current['id']]['statuses']
                for key in before:
                    if before[key]=='correct' and after[key]!='correct': losses.append(dict(case=c['id'],arm=a,stage=current['stage'],item=key,status=after[key]))
    result['durability_losses']=losses
    result['no_change_passes']={a:sum({p:v for p,v in s['files'].items() if p.endswith('.md')}=={p:v for p,v in next(z for z in snapshots if z['case']==s['case'] and z['arm']==a and z['stage']==1)['files'].items() if p.endswith('.md')} for s in snapshots if s['stage']==2 and s['arm']==a) for a in ARMS}
    labels={'untreated':'Unmaintained','ordinary':'Ordinary maintenance','skill':'Context Docs v0.1.1'}
    table=['| Final-artifact measure | Unmaintained | Ordinary maintenance | Context Docs v0.1.1 |','| --- | ---: | ---: | ---: |']
    for label,n,d in [('Required knowledge recorded','required_knowledge_correct','required_knowledge_total'),('Correct, supported reader answers','reader_answers_passed','reader_answers_total'),('Correct in both reader sessions','consistent_correct_pairs','reader_pairs')]:
        table.append('| '+label+' | '+' | '.join(f"{result['by_arm'][a][n]}/{result['by_arm'][a][d]}" for a in ARMS)+' |')
    table.append('| Target-claim accuracy | '+' | '.join(f"{result['by_arm'][a]['target_claim_accuracy']:.1%}" if result['by_arm'][a]['target_claim_accuracy'] is not None else 'Not defined' for a in ARMS)+' |')
    for label,key in [('Missing required items','missing_items'),('Incorrect required items','incorrect_items'),('Critical document findings','critical_document_errors')]:
        table.append('| '+label+' | '+' | '.join(str(result['by_arm'][a][key]) for a in ARMS)+' |')
    table.append('| Conflicting required items | '+' | '.join(str(result['by_arm'][a]['conflicting_items']) for a in ARMS)+' |')
    return result,'\n'.join(table)+'\n',docrows,readerrows


def main():
    p=argparse.ArgumentParser();p.add_argument('results',type=Path);args=p.parse_args();root=args.results
    snapshots=json.loads((root/'snapshots.json').read_text())
    docs=json.loads((root/'document-reviews.json').read_text())
    trials=json.loads((root/'reader-trials.json').read_text())
    reviews=json.loads((root/'reader-reviews.json').read_text())
    summary,table,docrows,readerrows=summarize(snapshots,docs['snapshots'],trials,reviews['steps'])
    for name,value in [('summary.json',summary),('document-scores.json',docrows),('reader-scores.json',readerrows)]:
        (root/name).write_text(json.dumps(value,indent=2)+'\n')
    (root/'table.md').write_text(table)
    print(table);print(json.dumps(summary['by_arm'],indent=2))


if __name__=='__main__':main()
