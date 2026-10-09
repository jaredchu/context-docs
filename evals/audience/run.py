"""Five frozen synthetic audience/destination sessions; build never runs subjects."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
import re
import shlex
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('audience_public_helpers', ROOT / 'evals/public-adoption/run.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
case_spec = importlib.util.spec_from_file_location('audience_cases', Path(__file__).with_name('cases.py'))
cases = importlib.util.module_from_spec(case_spec)
case_spec.loader.exec_module(cases)
CASES, GENERAL = cases.CASES, cases.GENERAL
import hook

sha, dump, snapshot, hashes = helper.sha, helper.dump, helper.snapshot, helper.hashes
smoke, guarded, guard_hook = helper.smoke, helper.guarded, helper.guard_hook
PIN = '53be1a2fc99c9d9885eff3a7002eea6b1b022c79'
KIND = 'audience-destination-v1'


def harness_hashes():
    paths = [*Path(__file__).parent.glob('*.py'), Path(__file__).with_name('protocol.md'),
             ROOT / 'evals/public-adoption/run.py']
    for directory in ('claude-code', 'adoption', 'suite'):
        paths.extend((ROOT / 'evals' / directory).glob('*.py'))
    return {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in sorted(paths)}


def build(destination):
    if destination.exists() or destination == ROOT or ROOT in destination.parents:
        raise ValueError('Choose a fresh directory outside the repository.')
    for parent in destination.parents:
        if any((parent / name).exists() for name in ('CLAUDE.md', 'CLAUDE.local.md', '.claude/CLAUDE.md', '.claude/rules')):
            raise ValueError('Ancestor instruction file; use a clean evaluation location.')
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', PIN, '--', 'skills'], cwd=ROOT, text=True).splitlines()
    packages = {'.claude/' + n: subprocess.check_output(['git', 'show', PIN + ':' + n], cwd=ROOT).decode() for n in paths}
    if any((ROOT / n.removeprefix('.claude/')).read_bytes().decode() != text for n, text in packages.items()):
        raise ValueError('Working package differs from candidate pin.')
    destination.mkdir(parents=True)
    control = destination / 'control'; control.mkdir()
    for path in (Path(guard_hook.__file__), Path(hook.__file__)):
        shutil.copyfile(path, control / path.name)
    fixtures, configs = {}, {}
    for case in CASES:
        sid = case['id']; project = destination / 'projects' / sid
        files = {**case['files'], **packages}; fixtures[sid] = files
        smoke.write_files(project, files)
        immutable = [n for n in files if not hook.writable(n, dict(writable=case['writable'], immutable=case.get('protected', [])))]
        config = dict(project=str(project), events=str(control / (sid + '.events.jsonl')),
                      immutable=immutable, writable=case['writable'], read_only=case.get('audit', False))
        configs[sid] = config; config_path = control / (sid + '.config.json'); dump(config_path, config)
        command = shlex.join([sys.executable, str(control / 'hook.py'), str(config_path)]) + ' || exit 2'
        dump(control / (sid + '.settings.json'), dict(autoMemoryEnabled=False, hooks={e: [dict(hooks=[dict(type='command', command=command, timeout=10)])]
            for e in ('InstructionsLoaded', 'PreToolUse', 'PostToolUse', 'PostToolUseFailure')}))
    protocol = dict(kind=KIND, build_id=str(uuid.uuid4()), built_at=datetime.now(timezone.utc).isoformat(),
        package_commit=PIN, package_versions={n: packages['.claude/skills/' + n + '/VERSION'].strip() for n in smoke.SKILLS},
        model='claude-opus-5-5', requested_effort='high', effort_observed=False,
        cli_version=subprocess.check_output(['claude', '--version'], text=True).strip(),
        permission_mode='acceptEdits', setting_sources='project', auto_memory_enabled=False, session_timeout_seconds=600,
        allowed_tools=list(guard_hook.TOOLS), fixtures=fixtures, cases=CASES, general_rubric=GENERAL,
        initial_hashes={n: hashes(f) for n, f in fixtures.items()}, configurations=configs,
        control_hashes=hashes(snapshot(control)), harness_hashes=harness_hashes())
    dump(destination / 'protocol.json', protocol)
    (destination / 'protocol.sha256').write_text(sha((destination / 'protocol.json').read_bytes()) + '\n')
    print('Built five independent sessions; review and commit frozen inputs before execution.')


def validate(destination, expected_hash):
    data = (destination / 'protocol.json').read_bytes(); p = json.loads(data)
    if sha(data) != expected_hash or p.get('kind') != KIND:
        raise ValueError('Frozen protocol identity mismatch.')
    if p['harness_hashes'] != harness_hashes(): raise ValueError('Harness drift.')
    if p['cli_version'] != subprocess.check_output(['claude', '--version'], text=True).strip(): raise ValueError('CLI drift.')
    for name, digest in p['control_hashes'].items():
        if sha((destination / 'control' / name).read_bytes()) != digest: raise ValueError('Control drift.')
    return p


def preflight(destination, p, case):
    current = snapshot(destination / 'projects' / case['id'])
    if hashes(current) != p['initial_hashes'][case['id']]: raise ValueError('Fixture drift: ' + case['id'])
    return current


def provenance(log, project, body):
    prefix = 'Base directory for this skill: ' + str(project / '.claude/skills/context-docs') + '\n'
    for event in guarded.read_events(log):
        message = event.get('message', {})
        if event.get('type') != 'user' or not isinstance(message, dict): continue
        for block in message.get('content', []):
            if isinstance(block, dict) and block.get('type') == 'text':
                text = block.get('text', '')
                if text.startswith(prefix) and body.split('---', 2)[-1].strip() in text: return True
    return False


def clean(text, destination):
    aliases = [(str(destination), '/fixture')]
    if str(destination).startswith('/private/tmp/'):
        aliases.append((str(destination).removeprefix('/private'), '/fixture'))
    for path, replacement in [*aliases, (str(ROOT), '/context-docs-repo'), (str(Path.home()), '/user-home')]:
        text = text.replace(path, replacement)
    return text


def trajectory(log, events, project, case, destination):
    """Only allowlisted calls/results. Scan scope is evidence for review, not proof of reading."""
    project = project.resolve()
    results = {}
    for event in guarded.read_events(log):
        message = event.get('message', {})
        if not isinstance(message, dict): continue
        for block in message.get('content', []):
            if isinstance(block, dict) and block.get('type') == 'tool_result': results[block['tool_use_id']] = block
    output = []
    journal = case.get('journal')
    for event in events:
        if event.get('hook_event_name') != 'PreToolUse': continue
        name = event.get('tool_name'); payload = event.get('tool_input') or {}
        if name not in guard_hook.TOOLS: continue
        allowed_keys = {'Read': ('file_path', 'offset', 'limit'), 'Write': ('file_path',), 'Edit': ('file_path',),
                        'Glob': ('path', 'pattern'), 'Grep': ('path', 'pattern', 'glob', 'type', 'output_mode'), 'Skill': ('skill',)}[name]
        inputs = {k: clean(str(payload[k]), destination) for k in allowed_keys if k in payload}
        result = results.get(event.get('tool_use_id'), {})
        content = result.get('content', '')
        if isinstance(content, list): content = '\n'.join(b.get('text', '') for b in content if isinstance(b, dict) and b.get('type') == 'text')
        path = Path(payload.get('file_path') or payload.get('path') or project)
        resolved = (project / path).resolve(); inside = resolved == project or project in resolved.parents
        # Skill output may include startup/environment metadata; omit it. Read/search results
        # are retained only for permitted paths inside the synthetic fixture, excluding packages.
        selected = str(content) if inside and '.claude' not in resolved.relative_to(project).parts and name in ('Read', 'Grep', 'Glob') and event.get('decision') == 'allow' else ''
        journal_path = project / journal if journal else None
        candidate = bool(journal_path and name in ('Glob', 'Grep') and (resolved == journal_path or resolved in journal_path.parents))
        successful_content = bool(selected.strip() and result and not result.get('is_error'))
        grep_content = bool(successful_content and name == 'Grep' and payload.get('output_mode') == 'content'
            and selected.strip() != 'No matches found'
            and (resolved == journal_path or (candidate and re.search(r'(?:^|[/\\])' + re.escape(journal) + r'[:\-].+', selected, re.MULTILINE))))
        output.append(dict(tool=name, inputs=inputs, decision=event.get('decision'),
            result_present=bool(result), result_error=result.get('is_error', False) if result else None,
            selected_result=clean(selected, destination), write_attempt=name in ('Write', 'Edit'),
            journal_read_attempt=bool(journal_path and name == 'Read' and resolved == journal_path),
            journal_scan_candidate=candidate,
            journal_filename_returned=bool(journal and journal in selected),
            journal_content_returned=bool(grep_content or (journal_path and name == 'Read' and resolved == journal_path and successful_content))))
    return output


def should_stop(checks, execution_error):
    """Stop for execution gates; a guarded behavioral denial alone can continue."""
    return not all(checks.values()) or execution_error not in (None, 'permission_denied')


def run(destination, expected_hash):
    if (destination / 'logs').exists(): raise ValueError('Execution already attempted; no retries.')
    p = validate(destination, expected_hash)
    if any((destination / 'control').glob('*.events.jsonl')): raise ValueError('Prior hook evidence exists.')
    for case in p['cases']: preflight(destination, p, case)
    logs = destination / 'logs'; logs.mkdir(); trials = []
    for case in p['cases']:
        validate(destination, expected_hash)
        sid = case['id']; project = destination / 'projects' / sid; before = preflight(destination, p, case)
        local = {**p, 'extra_args': ['--no-session-persistence', '--effort', p['requested_effort'], '--tools', ','.join(p['allowed_tools']),
                                   '--settings', str(destination / 'control' / (sid + '.settings.json'))]}
        log = logs / (sid + '.jsonl'); print('Starting ' + sid, flush=True)
        execution = smoke.run_session(project, case['prompt'], log, local)
        observed = smoke.parse_stream(log); model = helper.observed_models(log)
        events = guarded.read_events(destination / 'control' / (sid + '.events.jsonl')); after = snapshot(project)
        checks = guarded.coverage(log, events, p['allowed_tools'])
        config = p['configurations'][sid]
        changed = {n for n in before.keys() | after.keys() if before.get(n) != after.get(n)}
        checks.update(completed=execution['exit_code'] == 0 and 'result' in observed['event_types'],
            responding_model_matches=model['responding_models'] == [p['model']],
            core_skill_called='context-docs' in observed['skill_names'],
            core_skill_delivered=provenance(log, project, before['.claude/skills/context-docs/SKILL.md']),
            immutable_bytes=all(before[n] == after.get(n) for n in config['immutable']),
            authorized_changes=all(hook.writable(n, config) and not case.get('audit') for n in changed),
            controls_unchanged=all(sha((destination / 'control' / n).read_bytes()) == h for n, h in p['control_hashes'].items()),
            no_external_loading=all(Path(e.get('file_path', '')).resolve().is_relative_to(project)
                for e in events if e.get('hook_event_name') == 'InstructionsLoaded'),
            initial_loading_observed=any(e.get('hook_event_name') == 'InstructionsLoaded' and Path(e.get('file_path', '')).resolve() == project / 'CLAUDE.md'
                and e.get('load_reason') == 'session_start' and e.get('file_sha256_at_event') == sha(before['CLAUDE.md'].encode()) for e in events))
        trial = dict(id=sid, execution=execution, execution_error=observed['execution_error'], model_evidence=model, execution_checks=checks,
            final_message=observed['final_message'], before=before, after=after, events=events,
            trajectory=trajectory(log, events, project, case, destination))
        trials.append(trial); dump(destination / 'trials.json', trials)
        print('Completed ' + sid + ': failed execution checks ' + str([k for k, v in checks.items() if not v]), flush=True)
        if should_stop(checks, observed['execution_error']):
            print('Execution gate failed; retain attempt and stop.'); break


def export_data(p, trials, destination):
    result = {k: p[k] for k in ('kind', 'build_id', 'built_at', 'package_commit', 'package_versions', 'model', 'requested_effort', 'effort_observed', 'cli_version', 'auto_memory_enabled', 'general_rubric', 'harness_hashes')}
    result['protocol_sha256'] = sha((destination / 'protocol.json').read_bytes())
    result['cases'] = [{**{k: c[k] for k in ('id', 'entry', 'prompt', 'criteria', 'writable')},
                        'protected': c.get('protected', []), 'audit': c.get('audit', False), 'journal': c.get('journal')}
                       for c in p['cases']]
    result['sessions'] = []
    for t in trials:
        files = lambda key: {n: clean(b, destination) for n, b in t[key].items() if not n.startswith('.claude/')}
        result['sessions'].append(dict(id=t['id'], execution_checks=t['execution_checks'], model_evidence=t['model_evidence'],
            exit_code=t['execution']['exit_code'], seconds=t['execution']['seconds'],
            execution_error=clean(str(t['execution_error']), destination) if t['execution_error'] is not None else None,
            final_message=clean(t['final_message'] or '', destination), before_hashes=hashes(t['before']), after_hashes=hashes(t['after']),
            files_before=files('before'), files_after=files('after'), trajectory=t['trajectory']))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); sub = parser.add_subparsers(dest='action', required=True)
    for name in ('build', 'run', 'export'):
        p = sub.add_parser(name); p.add_argument('destination', type=Path)
        if name == 'run': p.add_argument('--frozen-sha256', required=True)
        if name == 'export': p.add_argument('output', type=Path)
    args = parser.parse_args(); destination = args.destination.resolve()
    if args.action == 'build': build(destination)
    elif args.action == 'run': run(destination, args.frozen_sha256)
    else:
        if args.output.exists(): raise ValueError('Preserve existing export.')
        dump(args.output, export_data(json.loads((destination / 'protocol.json').read_text()), json.loads((destination / 'trials.json').read_text()), destination))
