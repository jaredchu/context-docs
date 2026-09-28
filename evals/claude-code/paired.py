"""Bounded native comparison; immutable skills, paired requests, explicit review."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

import smoke


CODE = '''import csv
import json
import sys

def read_records(path):
    with open(path, newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter=";", restkey="surplus"))

if __name__ == "__main__":
    print(json.dumps(read_records(sys.argv[1]), ensure_ascii=False))
'''
INSTRUCTIONS = '''# Project instructions

Work only in this project. Preserve supplied code and sample data. Do not commit.
At the start of your first reply, include the exact phrase: Session check: amber-orbit.
This phrase checks instruction exposure; it is not project knowledge to document.
'''
CASES = [
    dict(id='delimited-records', files={
        'CLAUDE.md': INSTRUCTIONS,
        'records.py': CODE,
        'samples/visits.csv': 'site;visits;active\nnorth;12;true\nsouth;8\nwest;4;false;manual;checked\n',
    }, immutable=['records.py', 'samples/visits.csv'], entry='README.md',
        prompt='Set up ongoing project context documentation for this small utility. '
        'Explain its invocation and data behavior from the supplied source and sample, '
        'provide a README entry point, and put a concise maintenance rule in the project '
        'instructions. Keep records.py and samples/visits.csv byte-identical. Do not '
        'commit or change files outside this project. Report what changed, what you '
        'verified, and what remains uncertain.',
        expected=[
            'README navigation leads to useful context and a correct python records.py samples/visits.csv invocation.',
            'Context accurately explains the supplied irregular records: missing active becomes null/None and surplus fields become a list; it does not claim all output values are strings.',
            'The resulting context and final response agree with the resulting files; no unqualified current assertion that README or maintenance guidance is absent after creating it.',
            'All factual and authority claims stay within evidence: no invented owner approvals, execution verification, version, publication or automatic-loading claims.',
            'One reachable ongoing maintenance rule exists in CLAUDE.md, with supplied instructions and code/data preserved.',
        ]),
    dict(id='front-door-refresh', files={
        'CLAUDE.md': INSTRUCTIONS,
        'count_lines.py': 'import sys\nfrom pathlib import Path\nprint(len(Path(sys.argv[1]).read_text().splitlines()))\n',
        'samples/three.txt': 'alpha\nbeta\ngamma\n',
        'notes/state.md': '# Current project state\n\nThis is a local line-counting utility. Run `python count_lines.py samples/three.txt`.\n\nThere is no README or documentation front door. Command details live only in this file.\nNo ongoing documentation maintenance rule exists in the project instructions.\n\nAn unresolved question is whether empty trailing lines should count; no decision has been made.\nSee [scope](scope.md) for the approved boundary.\n',
        'notes/scope.md': '# Scope decision\n\nThe owner approved local text files only for this pilot on 2026-09-12.\nNetwork ingestion remains a proposal, not an approved feature.\n',
    }, immutable=['count_lines.py', 'samples/three.txt', 'notes/scope.md'], entry='README.md',
        prompt='Set up ongoing context documentation maintenance using the existing notes. '
        'Create a concise README front door, move the usage instructions into notes/usage.md, '
        'and keep notes/state.md as the current-state entry point. Add a concise maintenance '
        'rule to the project instructions. Preserve the scope decision and unresolved '
        'question. Keep count_lines.py, samples/three.txt and notes/scope.md byte-identical. '
        'Do not commit or change files outside this project. Report what changed, what '
        'you verified, and what remains uncertain.',
        expected=[
            'README links to notes/state.md; state links to notes/usage.md, which has the correct invocation.',
            'The unresolved trailing-line question and approved local-only scope survive; proposed network ingestion is not promoted to approval.',
            'Current state and the final response reconcile the newly created README, usage guide and maintenance rule; old absence/only-here claims are removed or explicitly historical.',
            'All factual and authority claims stay within evidence: no invented owner approvals, execution verification, version, publication or automatic-loading claims.',
            'One reachable ongoing maintenance rule exists in CLAUDE.md, with supplied instructions and immutable files preserved.',
        ]),
]


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def build(destination, model):
    if destination.exists():
        raise SystemExit('Destination exists; preserve prior inputs/results.')
    destination.mkdir(parents=True)
    protocol = dict(kind='native-paired-v1', model=model, permission_mode='acceptEdits',
                    setting_sources='project', session_timeout_seconds=600,
                    allowed_tools=[*smoke.TOOLS, 'Bash(python3:*)'],
                    common_extra_args=['--no-session-persistence', '--tools',
                                       'Read,Write,Edit,Glob,Grep,Skill,Bash'],
                    cli_version=subprocess.check_output(['claude', '--version'], text=True).strip(),
                    source_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=smoke.ROOT, text=True).strip(),
                    skills={n: (smoke.ROOT/'skills'/n/'VERSION').read_text().strip() for n in smoke.SKILLS},
                    installed_files=smoke.installed_files(),
                    user_claude_md_present=(Path.home()/'.claude/CLAUDE.md').exists(),
                    cases=CASES, sessions=[],
                    decision_rule='A same-case semantic criterion failing in both skill attempts and passing in both ordinary attempts is a repeatable adverse association requiring investigation, not causal proof. Mixed or shared failures are inconclusive; no skill-specific regression observed permits consideration of experimental merge with limitations, not a reliability claim. Missing skill exposure, contamination or incomplete execution makes the affected comparison inconclusive. No prompt tuning or extra model runs within this study.')
    for case in CASES:
        for repeat in (1, 2):
            # Counterbalance order without changing requests or inputs.
            arms = ('ordinary', 'skills') if repeat == 1 else ('skills', 'ordinary')
            for arm in arms:
                sid = f'{case["id"]}-{arm}-{repeat}'
                project = destination/'projects'/sid
                project.mkdir(parents=True)
                smoke.write_files(project, case['files'])
                if arm == 'skills':
                    smoke.install_skills(project)
                subprocess.run(['git', 'init', '-q'], cwd=project, check=True)
                subprocess.run(['git', 'add', '.'], cwd=project, check=True)
                subprocess.run(['git', '-c', 'user.email=fixture@example.invalid', '-c',
                                'user.name=Fixture Author', 'commit', '-qm', 'Initial synthetic fixture'], cwd=project, check=True)
                protocol['sessions'].append(dict(id=sid, case=case['id'], arm=arm, repeat=repeat,
                                                initial_tree=smoke.tree_hashes(project)))
    dump(destination/'protocol.json', protocol)
    print(f'Built {len(protocol["sessions"])} sessions. Freeze protocol before execution.')


def measure(project, destination, case, before, installed):
    spec = dict(id=case['id'], before=before, immutable=case['immutable'],
                protected=[line for line in case['files']['CLAUDE.md'].splitlines() if line and not line.startswith('#')],
                entry=case['entry'], allow_noop=False, external_references=installed)
    return smoke.grade(spec, project, destination, before)


def run(destination):
    protocol = json.loads((destination/'protocol.json').read_text())
    if protocol['kind'] != 'native-paired-v1':
        raise SystemExit('Unsupported protocol.')
    if (destination/'trials.json').exists() or (destination/'logs').exists():
        raise SystemExit('Preserve prior execution; choose a fresh destination.')
    for session in protocol['sessions']:
        if smoke.tree_hashes(destination/'projects'/session['id']) != session['initial_tree']:
            raise SystemExit('Input drift: ' + session['id'])
    (destination/'logs').mkdir()
    cases = {c['id']: c for c in protocol['cases']}
    trials = []
    for session in protocol['sessions']:
        project = destination/'projects'/session['id']
        case = cases[session['case']]
        before = smoke.snapshot(project)
        local = {**protocol, 'extra_args': protocol['common_extra_args'] +
                 (['--disable-slash-commands'] if session['arm'] == 'ordinary' else [])}
        print('Starting ' + session['id'], flush=True)
        log = destination/'logs'/f'{session["id"]}.jsonl'
        execution = smoke.run_session(project, case['prompt'], log, local)
        observed = smoke.parse_stream(log)
        installed = protocol['installed_files'] if session['arm'] == 'skills' else {}
        graded = measure(project, destination, case, before, installed)
        checks = graded['checks']
        hashes = smoke.tree_hashes(project)
        checks['immutable_bytes'] = all(hashes.get(n) == session['initial_tree'][n] for n in case['immutable'])
        checks['packages_unchanged'] = all(hashes.get(n) == h for n, h in installed.items())
        checks['no_execution_error'] = execution['exit_code'] == 0 and observed['execution_error'] is None
        trials.append(dict(**session, prompt=case['prompt'], rubric=case['expected'],
                           execution=execution, observed=observed, checks=checks,
                           mechanical_pass=all(checks.values()), link_errors=graded['link_errors'],
                           tree_after=hashes, files_before={n:b for n,b in before.items() if not n.startswith('.claude/')},
                           files_after=smoke.project_files(project)))
        dump(destination/'trials.json', trials)
        print('Completed ' + session['id'] + ': ' + str([n for n,ok in checks.items() if not ok]), flush=True)
        if execution['exit_code'] or observed['execution_error'] not in (None, 'permission_denied'):
            print('Execution failed; partial results retained. No automatic retries.')
            break


def report(destination, reviews_path):
    trials = json.loads((destination/'trials.json').read_text())
    reviews = json.loads(reviews_path.read_text())['sessions']
    rows = []
    for trial in trials:
        reviewed = reviews[trial['id']]
        assert len(reviewed['criteria']) == len(trial['rubric'])
        assert all(type(v) is bool for v in reviewed['criteria']) and reviewed['evidence'].strip()
        rows.append(dict(id=trial['id'], arm=trial['arm'], case=trial['case'],
                         mechanical=trial['mechanical_pass'], semantic=all(reviewed['criteria']),
                         criteria=reviewed['criteria'], invoked=trial['observed']['invoked'],
                         failed_checks=[n for n, ok in trial['checks'].items() if not ok]))
    totals = {arm: dict(sessions=sum(r['arm']==arm for r in rows),
                       mechanical=sum(r['mechanical'] for r in rows if r['arm']==arm),
                       semantic=sum(r['semantic'] for r in rows if r['arm']==arm))
              for arm in ('ordinary', 'skills')}
    table = ['| Session | Mechanical | Semantic | Criteria |', '| --- | --- | --- | --- |']
    for r in rows:
        table.append(f'| {r["id"]} | {"pass" if r["mechanical"] else "fail"} | '
                     f'{"pass" if r["semantic"] else "fail"} | {sum(r["criteria"])}/{len(r["criteria"])} |')
    dump(destination/'summary.json', dict(totals=totals, rows=rows))
    (destination/'table.md').write_text('\n'.join(table)+'\n')
    print(json.dumps(totals, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['build','run','report'])
    parser.add_argument('destination', type=Path)
    parser.add_argument('--model', default='claude-opus-5')
    parser.add_argument('--reviews', type=Path)
    args = parser.parse_args()
    if args.action == 'build': build(args.destination, args.model)
    elif args.action == 'run': run(args.destination)
    else: report(args.destination, args.reviews)


if __name__ == '__main__':
    main()
