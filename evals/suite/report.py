"""Derive report tables from exported trials plus explicit semantic reviews."""
import argparse
import json
import re
import statistics
from pathlib import Path
from cases import CASES


def summarize(trials, reviews, case_list=CASES, conditions=('baseline', 'skill'), attempts=3):
    cases = {c['id']: c for c in case_list}
    assert len(conditions) == 2
    assert len(trials) == len(cases) * len(conditions) * attempts, 'Incomplete experiment; report separately.'
    assert {(t['task'], t['arm'], t['attempt']) for t in trials} == {
        (name, arm, attempt) for name in cases for arm in conditions for attempt in range(1, attempts + 1)}
    for t in trials:
        complete = len(t['steps']) == t['expected_steps']
        t['mechanical_pass'] = complete and all(s['mechanical_pass'] and not s['execution_error'] for s in t['steps'])
        semantic = True
        for i, s in enumerate(t['steps']):
            review = reviews[s['review_id']]
            assert len(review['criteria']) == len(cases[t['task']]['steps'][i]['rubric'])
            assert all(type(x) is bool for x in review['criteria']) and review['reason'].strip()
            semantic = semantic and all(review['criteria'])
        t['semantic_pass'] = complete and semantic
        t['success'] = t['mechanical_pass'] and t['semantic_pass']
        timings = [s['execution_seconds'] for s in t['steps']]
        t['agent_seconds'] = sum(timings) if all(x is not None for x in timings) else None
        final = t['steps'][-1]['observed']
        initial = {**cases[t['task']]['files'], **cases[t['task']]['uncommitted']}
        initial_words = sum(len(s.split()) for p, s in initial.items() if p.endswith('.md'))
        t['word_delta'] = final['word_count'] - initial_words if final else None
        t['third_pass_unchanged'] = (t['steps'][1]['observed']['documents'] == final['documents']
                                     if len(cases[t['task']]['steps']) == 3 and complete and final and t['steps'][1]['observed'] else None)
    labels = {'baseline': 'Ordinary instructions', 'skill': 'With Context Docs', 'original': 'Original v0.1.0', 'candidate': 'Concise candidate'}
    table = [f'| Task | {labels[conditions[0]]} | {labels[conditions[1]]} |', '| --- | ---: | ---: |']
    for case in case_list:
        counts = [sum(t['success'] for t in trials if t['task'] == case['id'] and t['arm'] == arm) for arm in conditions]
        table.append(f"| {case['id']} | {counts[0]}/{attempts} | {counts[1]}/{attempts} |")
    totals = [sum(t['success'] for t in trials if t['arm'] == arm) for arm in conditions]
    table.append(f'| **Total trials** | **{totals[0]}/{len(cases) * attempts}** | **{totals[1]}/{len(cases) * attempts}** |')
    summary = {}
    for arm in conditions:
        group = [t for t in trials if t['arm'] == arm]
        times = [t['agent_seconds'] for t in group if t['agent_seconds'] is not None]
        delta = [t['word_delta'] for t in group if t['word_delta'] is not None]
        summary[arm] = dict(success=sum(t['success'] for t in group), mechanical_pass=sum(t['mechanical_pass'] for t in group),
                            semantic_pass=sum(t['semantic_pass'] for t in group), median_agent_seconds=statistics.median(times),
                            agent_seconds_range=[min(times), max(times)], total_agent_seconds=sum(times),
                            median_word_delta=statistics.median(delta), word_delta_range=[min(delta), max(delta)])
        for key in ['n_input_tokens', 'n_cache_tokens', 'n_output_tokens']:
            values = [t['usage'][key] for t in group]
            summary[arm][key] = sum(values) if all(v is not None for v in values) else None
        if summary[arm]['n_input_tokens'] is not None and summary[arm]['n_cache_tokens'] is not None:
            summary[arm]['uncached_input_tokens'] = summary[arm]['n_input_tokens'] - summary[arm]['n_cache_tokens']
        summary[arm]['unchanged_third_passes'] = sum(t['third_pass_unchanged'] is True for t in group)
    summary['by_task'] = {}
    for name in cases:
        summary['by_task'][name] = {}
        for arm in conditions:
            group = [t for t in trials if t['task'] == name and t['arm'] == arm]
            summary['by_task'][name][arm] = dict(success=sum(t['success'] for t in group),
                median_word_delta=statistics.median(t['word_delta'] for t in group if t['word_delta'] is not None),
                median_agent_seconds=statistics.median(t['agent_seconds'] for t in group if t['agent_seconds'] is not None))
    return summary, '\n'.join(table)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('results', type=Path)
    parser.add_argument('--readme', type=Path, help='Update an existing evaluation-table marker block.')
    args = parser.parse_args()
    trials = json.loads((args.results / 'trials.json').read_text())
    reviews = json.loads((args.results / 'reviews.json').read_text())
    summary, table = summarize(trials, reviews['steps'])
    (args.results / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    (args.results / 'table.md').write_text(table + '\n')
    if args.readme:
        body = args.readme.read_text()
        pattern = r'<!-- evaluation-table:start -->.*?<!-- evaluation-table:end -->'
        assert len(re.findall(pattern, body, re.S)) == 1, 'README must contain exactly one evaluation-table marker block.'
        body = re.sub(pattern, lambda _: '<!-- evaluation-table:start -->\n' + table + '\n<!-- evaluation-table:end -->', body, flags=re.S)
        args.readme.write_text(body)
    print(table)
    print(json.dumps(summary, indent=2))
