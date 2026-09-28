"""Native Claude Code smoke test for adoption v0.1.3 and the core skill.

Codex studies cover one client. This runs the same routing fixtures through the
Claude Code CLI to check four things on that client: whether the skill is found
and invoked, where the maintenance rule lands in Claude-only and mixed
instruction projects, whether a repeat pass preserves files and the original
adoption date, and whether an audit-only request leaves the project unchanged.

Fixtures come from the shared adoption cases, so the Codex and Claude Code runs
exercise the same projects and criteria. Only the invocation wording, the skill
installation path and the audit report destination differ, because this client
has no /output directory and uses its own skill locations.

Mechanical checks and skill invocation are recorded here. Semantic review is
separate and must be supplied explicitly, as in every other study.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'evals/suite'))
sys.path.insert(0, str(ROOT / 'evals/adoption'))
from verify import grade as grade_files, snapshot


def grade(spec, project, output, before):
    """Grade with the project as the working directory.

    The shared verifier resolves declared installed-file references from the
    current directory, as it does inside a Harbor container whose project is the
    working directory. Here the installed skills live at .claude/skills, so the
    same relative path must resolve for both the grader and the Markdown link.
    """
    previous = Path.cwd()
    os.chdir(project)
    try:
        return grade_files(spec, project, output, before)
    finally:
        os.chdir(previous)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


routing = load('routing_cases', ROOT / 'evals/adoption/instructions.py')
adoption = load('adoption_cases', ROOT / 'evals/adoption/build.py')
marker = load('marker_cases', ROOT / 'evals/adoption/marker.py')

SKILLS = ('context-docs', 'adopt-context-docs')
INSTALL = '.claude/skills'
# Claude Code invokes a skill as a slash command or selects it from the
# description. Both paths are exercised: named for routing, unnamed for discovery.
SLASH = '/adopt-context-docs'
FIRST_DATE = ' For this test, treat the current date as 2026-10-01, regardless of the environment date.'
NEXT_DATE = ' For this test, treat the current date as 2026-10-02, regardless of the environment date.'
AUDIT = ('Audit this project for Context Docs adoption only. Do not edit, create or delete any'
         ' project file. Report in your final message whether the existing instructions and'
         ' documents already follow the method, and distinguish a missing marker from'
         ' non-adoption.' + FIRST_DATE)
DISCOVER = ('Set up ongoing context documentation maintenance for this project, so later'
            ' sessions keep its project knowledge accurate and know where to start.' + FIRST_DATE)
TOOLS = ['Read', 'Write', 'Edit', 'Glob', 'Grep', 'Skill', 'TodoWrite', 'Bash(git status:*)',
         'Bash(git diff:*)', 'Bash(git log:*)', 'Bash(ls:*)', 'Bash(cat:*)']


def constraints(case):
    if not case['immutable']:
        return ''
    return '\nKeep these project files byte-identical: ' + ', '.join(case['immutable']) + '.\n'


def trajectories():
    """Frozen session list: four trajectories, six model sessions."""
    claude_case, split_case = routing.CASES
    audit_case = next(c for c in marker.CASES if c['id'] == 'audit-only')
    code_case = next(c for c in adoption.CASES if c['id'] == 'adopt-empty-docs')
    result = [
        dict(id='claude-instructions', case=claude_case, invocation='named', steps=[
            dict(prompt=SLASH + ' Adopt Context Docs in this project, including its ongoing'
                 ' maintenance rule in the loaded project instructions. This project keeps its'
                 ' agent instructions in CLAUDE.md; no AGENTS.md is loaded here.' + FIRST_DATE,
                 allow_noop=False, rubric=claude_case['steps'][0]['rubric']),
            dict(prompt=SLASH + ' Adopt Context Docs in this project. No new project evidence or'
                 ' decisions have been supplied.' + NEXT_DATE,
                 allow_noop=True, expect_unchanged=True, expect_date='2026-10-01',
                 rubric=claude_case['steps'][1]['rubric']),
        ]),
        dict(id='split-instructions', case=split_case, invocation='named', steps=[
            dict(prompt=SLASH + ' Adopt Context Docs in this project, including its ongoing'
                 ' maintenance rule in the loaded project instructions. This client loads'
                 ' CLAUDE.md only; AGENTS.md is kept for another tool. Do not duplicate guidance'
                 ' between them.' + FIRST_DATE,
                 allow_noop=False, rubric=split_case['steps'][0]['rubric']),
            dict(prompt=SLASH + ' Adopt Context Docs in this project. No new project evidence or'
                 ' decisions have been supplied.' + NEXT_DATE,
                 allow_noop=True, expect_unchanged=True, expect_date='2026-10-01',
                 rubric=split_case['steps'][1]['rubric']),
        ]),
        dict(id='audit-only', case=audit_case, invocation='named', steps=[
            dict(prompt=SLASH + ' ' + AUDIT, allow_noop=True, expect_unchanged=True,
                 report='final_message', rubric=[
                     'Reports existing workflow adoption with an absent marker and unrecorded date; does not classify the project as non-adopted merely because its marker is missing.',
                     'Leaves every project file byte-identical and reports findings without writing a project file.',
                 ]),
        ]),
        dict(id='discovery', case=code_case, invocation='unnamed', steps=[
            dict(prompt=DISCOVER, allow_noop=False, expect_skill='adopt-context-docs', rubric=[
                 'Claude selects a context-docs skill from its description, without the skill being named in the request.',
                 'Creates useful discoverable context grounded in the CSV script, without invented approvals or deployment claims.',
                 'Adds ongoing maintenance guidance to the instruction file this client loads; does not install skill copies or change code.',
            ]),
        ]),
    ]
    for trajectory in result:
        for step in trajectory['steps']:
            step['prompt'] += constraints(trajectory['case'])
    return result


def installed_files():
    return {f'{INSTALL}/{path.relative_to(ROOT / "skills")}': hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted((ROOT / 'skills').rglob('*')) if path.is_file()}


def project_files(root):
    """Documents and code the fixture supplies, without the installed skills.

    Grading uses the complete working tree so a stray file under .claude is
    visible to the shared verifier; this narrower view is what the report
    compares and what the unchanged-project checks use.
    """
    return {name: body for name, body in snapshot(root).items()
            if not name.startswith('.claude/')}


def spec_for(case, before, step):
    spec = dict(id='claude-' + case['id'], before=before, protected=case['protected'],
                immutable=[p for p in case['immutable']], entry=case.get('entry', 'README.md'),
                allow_noop=step['allow_noop'])
    spec['external_reference_roots'] = [INSTALL]
    spec['external_references'] = installed_files()
    return spec


def write_files(destination, files):
    for name, body in files.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)


def materialize(destination, case):
    destination.mkdir(parents=True)
    # Commit only the tracked fixture, then add uncommitted material on top, so the
    # agent meets a dirty working tree as it does in the Harbor packages.
    write_files(destination, case['files'])
    for name in SKILLS:
        shutil.copytree(ROOT / 'skills' / name, destination / INSTALL / name)
    subprocess.run(['git', 'init', '-q'], cwd=destination, check=True)
    for name in sorted(case['files']) + [INSTALL]:
        subprocess.run(['git', 'add', '--', name], cwd=destination, check=True)
    subprocess.run(['git', '-c', 'user.email=fixture@example.invalid', '-c', 'user.name=Fixture Author',
                    'commit', '-qm', 'Initial synthetic fixture'], cwd=destination, check=True)
    write_files(destination, case['uncommitted'])
    if case['uncommitted']:
        dirty = subprocess.run(['git', 'status', '--porcelain'], cwd=destination,
                               capture_output=True, text=True).stdout
        assert dirty.strip(), 'uncommitted fixture material must leave the tree dirty'


def parse_stream(path):
    """Tool calls, skill invocations and the final message, from model-visible output."""
    events, skill_calls, reads, final, error, usage = [], [], [], None, None, {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except ValueError:
            error = error or 'unparsable_stream_line'
            continue
        events.append(event.get('type'))
        message = event.get('message') or {}
        for block in message.get('content') or []:
            if not isinstance(block, dict):
                continue
            if block.get('type') == 'tool_use':
                name, payload = block.get('name'), block.get('input') or {}
                if name == 'Skill':
                    skill_calls.append(payload)
                elif name == 'Read' and str(payload.get('file_path', '')).find(INSTALL) >= 0:
                    reads.append(payload.get('file_path'))
            elif block.get('type') == 'text' and message.get('role') == 'assistant':
                final = block.get('text')
        if event.get('type') == 'result':
            usage = dict(num_turns=event.get('num_turns'), duration_ms=event.get('duration_ms'),
                         total_cost_usd=event.get('total_cost_usd'))
            if event.get('is_error'):
                error = error or str(event.get('result'))[:500]
            if event.get('permission_denials'):
                error = error or 'permission_denied'
            if isinstance(event.get('result'), str):
                final = event['result']
    named = {str(call.get('skill') or call.get('name') or '') for call in skill_calls}
    return dict(skill_calls=skill_calls, skill_names=sorted(n for n in named if n),
                installed_reads=reads, invoked=bool(skill_calls or reads), final_message=final,
                execution_error=error, event_types=sorted(set(events)), usage=usage)


def run_session(project, prompt, log, model):
    command = ['claude', '-p', prompt, '--output-format', 'stream-json', '--verbose',
               '--permission-mode', 'acceptEdits', '--setting-sources', 'project',
               '--strict-mcp-config', '--allowedTools', *TOOLS]
    if model:
        command += ['--model', model]
    environment = {k: v for k, v in os.environ.items() if not k.startswith('CLAUDE_CODE_')}
    environment['CLAUDE_CODE_ENTRYPOINT'] = 'context-docs-smoke'
    started = time.time()
    with log.open('w') as stream:
        completed = subprocess.run(command, cwd=project, stdout=stream,
                                   stderr=subprocess.PIPE, text=True, env=environment)
    return dict(exit_code=completed.returncode, stderr=completed.stderr[-2000:],
                seconds=round(time.time() - started, 1))


def build(destination, model=None):
    if destination.exists():
        raise SystemExit('Destination exists; choose a new path to preserve prior runs.')
    destination.mkdir(parents=True)
    protocol = dict(kind='claude-code-smoke', frozen_at=None, model=model or 'client default',
                    client='claude-code', cli_version=subprocess.run(['claude', '--version'],
                    capture_output=True, text=True).stdout.strip(),
                    skills={name: (ROOT / 'skills' / name / 'VERSION').read_text().strip() for name in SKILLS},
                    installed_files=installed_files(), allowed_tools=TOOLS,
                    setting_sources='project', permission_mode='acceptEdits',
                    user_claude_md_present=(Path.home() / '.claude/CLAUDE.md').exists(),
                    user_agents_md_present=(Path.home() / 'AGENTS.md').exists(),
                    trajectories=[])
    for trajectory in trajectories():
        materialize(destination / 'projects' / trajectory['id'], trajectory['case'])
        protocol['trajectories'].append(dict(
            id=trajectory['id'], invocation=trajectory['invocation'],
            case=trajectory['case']['id'], immutable=trajectory['case']['immutable'],
            protected=trajectory['case']['protected'],
            steps=[dict(prompt=step['prompt'], allow_noop=step['allow_noop'],
                        expect_unchanged=step.get('expect_unchanged', False),
                        expect_date=step.get('expect_date'), expect_skill=step.get('expect_skill'),
                        rubric=step['rubric']) for step in trajectory['steps']]))
    protocol['commit'] = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                                        capture_output=True, text=True).stdout.strip()
    (destination / 'protocol.json').write_text(json.dumps(protocol, indent=2) + '\n')
    sessions = sum(len(t['steps']) for t in protocol['trajectories'])
    print(f'Built {len(protocol["trajectories"])} trajectories / {sessions} sessions in {destination}.')
    print('Freeze this protocol in Git before running model sessions.')


def run(destination, model=None):
    protocol = json.loads((destination / 'protocol.json').read_text())
    if (destination / 'trials.json').exists():
        raise SystemExit('trials.json exists; preserve it and build a new destination.')
    logs = destination / 'logs'
    logs.mkdir(exist_ok=True)
    trials = []
    for trajectory in trajectories():
        project = destination / 'projects' / trajectory['id']
        before_tree, before = snapshot(project), project_files(project)
        steps = []
        for index, step in enumerate(trajectory['steps']):
            log = logs / f'{trajectory["id"]}-pass-{index + 1}.jsonl'
            execution = run_session(project, step['prompt'], log, model)
            observed = parse_stream(log)
            after_tree, after = snapshot(project), project_files(project)
            spec = spec_for(trajectory['case'], before_tree, step)
            graded = grade(spec, project, destination, before_tree)
            checks = dict(graded['checks'])
            checks['installed_skill_unchanged'] = all(
                (project / name).is_file()
                and hashlib.sha256((project / name).read_bytes()).hexdigest() == digest
                for name, digest in protocol['installed_files'].items())
            checks['no_agent_commits_or_staging'] = checks.get('no_agent_commits_or_staging', False)
            if step.get('expect_unchanged'):
                checks['project_byte_identical'] = after == before
            if step.get('expect_date'):
                checks['original_date_retained'] = any(
                    f'Adopted: {step["expect_date"]}' in body for body in after.values())
            if step.get('expect_skill'):
                checks['skill_selected_unnamed'] = step['expect_skill'] in observed['skill_names']
            checks['no_execution_error'] = observed['execution_error'] is None and execution['exit_code'] == 0
            steps.append(dict(pass_number=index + 1, prompt=step['prompt'], execution=execution,
                              observed={k: v for k, v in observed.items() if k != 'skill_calls'},
                              skill_calls=observed['skill_calls'], checks=checks,
                              mechanical_pass=all(checks.values()),
                              files_before=before, files_after=after, rubric=step['rubric']))
            before_tree, before = after_tree, after
        trials.append(dict(trajectory=trajectory['id'], invocation=trajectory['invocation'],
                           case=trajectory['case']['id'], steps=steps))
    (destination / 'trials.json').write_text(json.dumps(trials, indent=2) + '\n')
    passed = sum(s['mechanical_pass'] for t in trials for s in t['steps'])
    total = sum(len(t['steps']) for t in trials)
    print(f'Ran {total} sessions; {passed}/{total} passed mechanical checks.')
    print('Retain every session, including failures. Semantic review is required separately.')


def report(destination, reviews_path=None):
    trials = json.loads((destination / 'trials.json').read_text())
    reviews = json.loads(reviews_path.read_text()) if reviews_path else None
    rows, summary = [], dict(sessions=0, mechanical_passed=0, invoked=0, execution_errors=0,
                             trajectories=len(trials), semantic_reviewed=0, semantic_passed=0)
    for trial in trials:
        for step in trial['steps']:
            summary['sessions'] += 1
            summary['mechanical_passed'] += step['mechanical_pass']
            summary['invoked'] += bool(step['observed']['invoked'])
            summary['execution_errors'] += step['observed']['execution_error'] is not None
            key = f'{trial["trajectory"]}-pass-{step["pass_number"]}'
            judged = (reviews or {}).get('sessions', {}).get(key)
            if judged is not None:
                assert len(judged['criteria']) == len(step['rubric']), key
                assert all(isinstance(v, bool) for v in judged['criteria']), key
                assert judged['evidence'].strip(), key
                summary['semantic_reviewed'] += 1
                summary['semantic_passed'] += all(judged['criteria'])
            rows.append(dict(session=key, mechanical_pass=step['mechanical_pass'],
                             invoked=step['observed']['invoked'],
                             skills=step['observed']['skill_names'],
                             failed_checks=[n for n, ok in step['checks'].items() if not ok],
                             semantic=None if judged is None else all(judged['criteria'])))
    table = ['| Session | Skill invoked | Mechanical | Semantic |', '| --- | :---: | :---: | :---: |']
    for row in rows:
        semantic = 'not reviewed' if row['semantic'] is None else ('pass' if row['semantic'] else 'fail')
        table.append(f'| {row["session"]} | {"yes" if row["invoked"] else "no"} | '
                     f'{"pass" if row["mechanical_pass"] else "fail"} | {semantic} |')
    (destination / 'summary.json').write_text(json.dumps(dict(summary=summary, rows=rows), indent=2) + '\n')
    (destination / 'table.md').write_text('\n'.join(table) + '\n')
    print('\n'.join(table))
    print(json.dumps(summary, indent=2))
    if summary['semantic_reviewed'] != summary['sessions']:
        print('Semantic review incomplete: mechanical results alone do not establish behavior.')


POSITIVE_STREAM = [
    {'type': 'assistant', 'message': {'role': 'assistant', 'content': [
        {'type': 'tool_use', 'name': 'Skill', 'input': {'skill': 'adopt-context-docs'}}]}},
    {'type': 'result', 'is_error': False, 'num_turns': 4, 'result': 'Adoption recorded.'},
]
NEGATIVE_STREAM = [
    {'type': 'assistant', 'message': {'role': 'assistant', 'content': [
        {'type': 'tool_use', 'name': 'Read', 'input': {'file_path': '/project/README.md'}}]}},
    {'type': 'result', 'is_error': False, 'num_turns': 2, 'result': 'Nothing to do.'},
]
ERROR_STREAM = [{'type': 'result', 'is_error': True, 'result': 'Failed to authenticate'}]


def selftest():
    checks = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name, stream, invoked, error in [('positive', POSITIVE_STREAM, True, False),
                                             ('negative', NEGATIVE_STREAM, False, False),
                                             ('error', ERROR_STREAM, False, True)]:
            path = Path(tmp) / f'{name}.jsonl'
            path.write_text('\n'.join(json.dumps(event) for event in stream) + '\n')
            parsed = parse_stream(path)
            assert parsed['invoked'] == invoked, name
            assert (parsed['execution_error'] is not None) == error, name
            checks += 2
        assert parse_stream(Path(tmp) / 'positive.jsonl')['skill_names'] == ['adopt-context-docs']
        checks += 1
    for trajectory in trajectories():
        case = trajectory['case']
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / 'project'
            materialize(project, case)
            before = project_files(project)
            assert before == {**case['files'], **case['uncommitted']}, case['id']
            assert (project / INSTALL / 'context-docs/SKILL.md').is_file()
            checks += 2
            before = snapshot(project)
            first = trajectory['steps'][0]
            spec = spec_for(case, before, first)
            result = grade(spec, project, Path(tmp), before)
            # An untouched project must fail unless the step permits a no-op.
            assert result['mechanical_pass'] == bool(first['allow_noop']), case['id']
            checks += 1
            if not first['allow_noop']:
                for name, body in case['steps'][0]['oracle'].items():
                    if name.startswith('@output/'):
                        continue
                    (project / name).write_text(body)
                assert grade(spec, project, Path(tmp), before)['mechanical_pass'], case['id']
                checks += 1
                saved = snapshot(project)
                target = next(iter(case['immutable']), None)
                if target:
                    (project / target).write_text(case['files'][target] + '\nUnrequested edit.\n')
                    assert not grade(spec, project, Path(tmp), before)['mechanical_pass'], case['id']
                    (project / target).write_text(case['files'][target])
                    checks += 1
                # An editable project document: never an installed skill file or an
                # immutable input, so each control fails for its intended reason.
                broken = next(n for n in saved if n.endswith('.md')
                              and not n.startswith('.claude/') and n not in case['immutable'])
                (project / broken).write_text(saved[broken] + '\n[Missing](absent.md)\n')
                assert not grade(spec, project, Path(tmp), before)['mechanical_pass'], case['id']
                (project / broken).write_text(saved[broken])
                checks += 1
                # A reference to the installed skill is valid only while its bytes match.
                (project / broken).write_text(
                    saved[broken] + f'\n[Skill]({INSTALL}/adopt-context-docs/SKILL.md)\n')
                assert grade(spec, project, Path(tmp), before)['mechanical_pass'], case['id']
                (project / INSTALL / 'adopt-context-docs/SKILL.md').write_text('tampered\n')
                assert not grade(spec, project, Path(tmp), before)['mechanical_pass'], case['id']
                checks += 2
    print(f'{checks} stream, fixture and grader assertions passed. No model session was run.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('selftest')
    for name in ['build', 'run']:
        step = sub.add_parser(name)
        step.add_argument('destination', type=Path)
        step.add_argument('--model', default=None, help='pin a model, e.g. opus or sonnet')
    published = sub.add_parser('report')
    published.add_argument('destination', type=Path)
    published.add_argument('--reviews', type=Path, default=None)
    args = parser.parse_args()
    if args.command == 'selftest':
        selftest()
    elif args.command == 'build':
        build(args.destination.resolve(), args.model)
    elif args.command == 'run':
        run(args.destination.resolve(), args.model)
    else:
        report(args.destination.resolve(), args.reviews)


if __name__ == '__main__':
    main()
