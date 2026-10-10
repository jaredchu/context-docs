"""Four frozen public-history handoffs. Build/validate/export never run subjects."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import stat
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('history_helpers', ROOT / 'evals/public-adoption/run.py')
helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
spec = importlib.util.spec_from_file_location('history_hook', Path(__file__).with_name('hook.py'))
hook = importlib.util.module_from_spec(spec); spec.loader.exec_module(hook)
smoke, guarded, guard_hook = helper.smoke, helper.guarded, helper.guard_hook
sha, dump = helper.sha, helper.dump
KIND = 'public-history-v1'
ORDER = [('httpx', 'ordinary'), ('httpx', 'skill'), ('ripgrep', 'skill'), ('ripgrep', 'ordinary')]
OUTPUTS = {'httpx': 'docs/upgrade-handoff.md', 'ripgrep': 'UPGRADE-HANDOFF.md'}
SCOPES = {'httpx': 'HTTPX SSL configuration guidance and its consistency with source, 0.28.0 to 0.28.1',
          'ripgrep': 'ripgrep matching behavior and build-feature compatibility, 14.1.0 to 14.1.1'}
BOOTSTRAP = ('# Documentation exercise\n\n'
    'This is an evaluator-authored task over public upstream history.\n'
    'Read the README and the supplied task. Use source inspection only.\n'
    'Only the task-named handoff and a README navigation append may be written.\n'
    'All other files, including these instructions, are immutable.\n')


def snapshot(root):
    """Byte hashes, modes and symlink targets; never decode upstream binaries."""
    root = root.resolve(); files = {}
    for directory, dirs, names in os.walk(root, followlinks=False):
        for name in sorted(set(dirs + names)):
            p = Path(directory) / name; mode = p.lstat().st_mode
            relative = p.relative_to(root).as_posix()
            if stat.S_ISLNK(mode):
                target = os.readlink(p)
                if not hook.within(p.resolve(), root):
                    raise ValueError('External symlink in input: ' + relative)
                data = os.fsencode(target)
                files[relative] = dict(kind='symlink', target=target, sha256=sha(data), bytes=len(data), mode=stat.S_IMODE(mode))
            elif stat.S_ISREG(mode):
                if p.stat().st_nlink != 1:
                    raise ValueError('Hard-linked input: ' + relative)
                data = p.read_bytes()
                files[relative] = dict(kind='file', sha256=sha(data), bytes=len(data), mode=stat.S_IMODE(mode))
            elif not stat.S_ISDIR(mode):
                raise ValueError('Unsupported file type: ' + relative)
    return dict(sorted(files.items()))


def frozen_inputs():
    paths = [*Path(__file__).parent.glob('*.py'), Path(__file__).with_name('README.md'),
             ROOT / 'evals/public-adoption/run.py']
    paths += [ROOT / ('evals/public-history-' + name) for name in ('plan.md', 'ledger.md', 'sources.json', 'review.json')]
    for directory in ('claude-code', 'adoption', 'suite'):
        paths.extend((ROOT / 'evals' / directory).glob('*.py'))
    return {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in sorted(paths)}


def instruction_preflight(destination):
    for parent in (destination, *destination.parents):
        for name in ('CLAUDE.md', 'AGENTS.md', 'CLAUDE.local.md', '.claude'):
            if (parent / name).exists():
                raise ValueError('Ancestor instruction contamination: ' + str(parent / name))
    home = Path(os.environ.get('CLAUDE_CONFIG_DIR', str(Path.home() / '.claude')))
    paths = [home / 'CLAUDE.md', home / 'rules',
             Path('/Library/Application Support/ClaudeCode/CLAUDE.md'),
             Path('/Library/Application Support/ClaudeCode/.claude/rules'),
             Path('/etc/claude-code/CLAUDE.md'), Path('/etc/claude-code/.claude/rules')]
    if any(p.exists() for p in paths):
        raise ValueError('User or managed instructions present; do not start subjects.')


def verify_source(project, manifest, revision):
    current = snapshot(project)
    if manifest['revision'] != revision or set(current) != set(manifest['files']):
        raise ValueError('Upstream snapshot inventory mismatch.')
    for name, entry in current.items():
        expected = manifest['files'][name]
        git_mode = '120000' if entry['kind'] == 'symlink' else '100755' if entry['mode'] & 0o111 else '100644'
        data = os.fsencode(entry['target']) if entry['kind'] == 'symlink' else (project / name).read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if entry['sha256'] != expected['sha256'] or git_mode != expected['mode'] or blob != expected['git_blob']:
            raise ValueError('Upstream content/mode drift: ' + name)
        if Path(name).name in ('CLAUDE.md', 'AGENTS.md', 'CLAUDE.local.md') or any(part in ('.claude', '.agents', '.git', '.mcp.json') for part in Path(name).parts):
            raise ValueError('Unexpected upstream instruction/tool configuration: ' + name)
    return current


def package_files():
    commit = subprocess.check_output(['git', 'rev-parse', 'v0.1.6^{commit}'], cwd=ROOT, text=True).strip()
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', commit, '--', 'skills/context-docs'], cwd=ROOT, text=True).splitlines()
    package = {n.removeprefix('skills/context-docs/'): subprocess.check_output(['git', 'show', commit + ':' + n], cwd=ROOT) for n in paths}
    if package.get('VERSION', b'').strip() != b'0.1.6':
        raise ValueError('Unexpected core package version.')
    return commit, package


def prompt_for(case, arm):
    name, output = case, OUTPUTS[case]
    prompt = ('Prepare a contributor upgrade handoff for ' + SCOPES[name] +
        ' from the supplied evidence, and link it from the README.\n'
        'The project is the complete after-tag tree. Before-tag files and the fix diff are in ../evidence; '
        '../evidence/sources.json gives their immutable URLs and the before/after revisions.\n'
        'Write only ' + output + ' and append one navigation link to README.md. Preserve the entire '
        'original README byte-for-byte as a prefix, including during intermediate writes. '
        'All other files and the evidence are read-only. Do not create adoption rules or markers, '
        'enable logging, migrate directories, execute source or tests, install dependencies, use '
        'network access, delegate work or publish. Use Read, Grep and Glob for inspection, and '
        'Write/Edit for the two permitted outputs. Finish with a brief account of the changes and checks.\n')
    if arm == 'skill':
        prompt += ('Read the complete frozen .claude/skills/context-docs/SKILL.md using Read and apply '
                   'Context Docs v0.1.6 to this task. Follow its packaged references as needed.\n')
    return prompt


def source_references(identity, files, fix):
    """Only provenance, never evaluator commentary, enters subject-readable inputs."""
    select = lambda value, keys: {k: value[k] for k in keys if k in value}
    return dict(project=select(identity, ('id', 'repository', 'before', 'after')),
                files=[select(f, ('path', 'url', 'commit', 'sha256', 'git_blob')) for f in files],
                fix=select(fix, ('commit', 'url', 'diff_url', 'diff_sha256', 'date', 'parents', 'after')))


def build(destination, source_root, scout_root):
    destination = destination.resolve()
    if destination.exists() or destination == ROOT or ROOT in destination.parents:
        raise ValueError('Choose a fresh runtime directory outside the repository.')
    instruction_preflight(destination)
    inventory = json.loads((ROOT / 'evals/public-history-sources.json').read_text())
    identities = {p['id']: p for p in inventory['projects']}
    sources = {}
    for name in OUTPUTS:
        manifest = json.loads((source_root / (name + '-snapshot.json')).read_text())
        sources[name] = verify_source(source_root / name, manifest, identities[name]['after'])
        if OUTPUTS[name] in sources[name]: raise ValueError('Output already exists upstream.')
    commit, package = package_files()
    destination.mkdir(parents=True); control = destination / 'control'; control.mkdir()
    for p in (Path(guard_hook.__file__), Path(hook.__file__)):
        shutil.copyfile(p, control / p.name)
    sessions = []; initial = {}; evidence_hashes = {}; configs = {}
    for name, arm in ORDER:
        sid = name + '-' + arm; unit = destination / 'sessions' / sid
        project, evidence = unit / 'project', unit / 'evidence'
        shutil.copytree(source_root / name, project, symlinks=True)
        (project / 'CLAUDE.md').write_text(BOOTSTRAP)
        if arm == 'skill':
            for relative, data in package.items():
                path = project / '.claude/skills/context-docs' / relative
                path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
        evidence.mkdir(); before_refs = []
        for f in inventory['files']:
            if f['project'] == name and f['state'] == 'before':
                raw = (scout_root / name / 'before' / f['path']).read_bytes()
                if sha(raw) != f['sha256']: raise ValueError('Before evidence drift.')
                target = evidence / 'before' / f['path']; target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw); before_refs.append(f)
        fix = next(f for f in inventory['fixes'] if f['project'] == name)
        raw = (scout_root / name / 'fix.diff').read_bytes()
        if sha(raw) != fix['diff_sha256'] or not fix['ancestor_of_after']:
            raise ValueError('Fix evidence drift or missing ancestry.')
        (evidence / 'fix.diff').write_bytes(raw)
        dump(evidence / 'sources.json', source_references(identities[name], before_refs, fix))
        for p in evidence.rglob('*'):
            if p.is_file(): p.chmod(0o444)
        config = dict(project=str(project), evidence=str(evidence), writable=['README.md', OUTPUTS[name]],
                      events=str(control / (sid + '.events.jsonl')),
                      readme_prefix_b64=base64.b64encode((project / 'README.md').read_bytes()).decode())
        configs[sid] = config; config_path = control / (sid + '.config.json'); dump(config_path, config)
        command = shlex.join([sys.executable, str(control / 'hook.py'), str(config_path)]) + ' || exit 2'
        dump(control / (sid + '.settings.json'), dict(autoMemoryEnabled=False, hooks={e: [dict(hooks=[dict(type='command', command=command, timeout=10)])]
            for e in ('InstructionsLoaded', 'PreToolUse', 'PostToolUse', 'PostToolUseFailure')}))
        initial[sid] = snapshot(project); evidence_hashes[sid] = snapshot(evidence)
        sessions.append(dict(id=sid, project=name, arm=arm, output=OUTPUTS[name], prompt=prompt_for(name, arm)))
    protocol = dict(kind=KIND, build_id=str(uuid.uuid4()), built_at=datetime.now(timezone.utc).isoformat(),
        model='claude-opus-5-5', requested_effort='high', effort_observed=False,
        cli_version=subprocess.check_output(['claude', '--version'], text=True).strip(),
        package_commit=commit, package_version='0.1.6', package_hashes={n: sha(b) for n, b in package.items()},
        session_timeout_seconds=600, setting_sources='project', permission_mode='acceptEdits',
        allowed_tools=list(hook.TOOLS), auto_memory_enabled=False, disable_slash_commands=True,
        skill_delivery='explicit complete Read of frozen core; not native discovery',
        sessions=sessions, source_identities=identities, source_hashes=sources,
        initial_hashes=initial, evidence_hashes=evidence_hashes, configurations=configs,
        control_hashes=snapshot(control), frozen_input_hashes=frozen_inputs(),
        frozen_skill_body=package['SKILL.md'].decode('utf-8'))
    dump(destination / 'protocol.json', protocol)
    (destination / 'protocol.sha256').write_text(sha((destination / 'protocol.json').read_bytes()) + '\n')
    print('Built four unexecuted sessions. Review and freeze protocol before run.')


def validate(destination, expected_hash):
    data = (destination / 'protocol.json').read_bytes(); p = json.loads(data)
    if sha(data) != expected_hash or p.get('kind') != KIND: raise ValueError('Frozen identity mismatch.')
    if p['frozen_input_hashes'] != frozen_inputs(): raise ValueError('Harness/criteria/source drift.')
    if p['cli_version'] != subprocess.check_output(['claude', '--version'], text=True).strip(): raise ValueError('CLI drift.')
    instruction_preflight(destination)
    for name, item in p['control_hashes'].items():
        if not (destination / 'control' / name).is_file() or sha((destination / 'control' / name).read_bytes()) != item['sha256']:
            raise ValueError('Control drift: ' + name)
    return p


def preflight(destination, p, session):
    sid = session['id']; unit = destination / 'sessions' / sid
    instruction_preflight(unit)
    if sorted(p.name for p in unit.iterdir()) != ['evidence', 'project']:
        raise ValueError('Unexpected session-unit entries: ' + sid)
    for dirname, key in (('project', 'initial_hashes'), ('evidence', 'evidence_hashes')):
        if snapshot(unit / dirname) != p[key][sid]: raise ValueError('Fixture drift: ' + sid + '/' + dirname)


def results_by_id(log):
    results = {}
    for e in guarded.read_events(log):
        message = e.get('message')
        if not isinstance(message, dict): continue
        for block in message.get('content', []):
            if isinstance(block, dict) and block.get('type') == 'tool_result': results[block['tool_use_id']] = block
    return results


def result_text(block):
    value = block.get('content', '')
    return value if isinstance(value, str) else '\n'.join(b.get('text', '') for b in value if isinstance(b, dict) and b.get('type') == 'text')


def native_skills_disabled(log):
    initializations = [e for e in guarded.read_events(log) if e.get('type') == 'system' and e.get('subtype') == 'init']
    return bool(initializations) and all(e.get('skills') == [] and e.get('slash_commands') == [] for e in initializations)


def complete_skill_read(log, events, project, body):
    results = results_by_id(log); wanted = [s.strip() for s in body.splitlines() if s.strip()]
    target = project / '.claude/skills/context-docs/SKILL.md'
    for e in events:
        if e.get('hook_event_name') != 'PreToolUse' or e.get('tool_name') != 'Read' or e.get('decision') != 'allow': continue
        path = Path((e.get('tool_input') or {}).get('file_path', ''))
        if (project / path).resolve() != target: continue
        result = results.get(e.get('tool_use_id'), {})
        if not result or result.get('is_error'): continue
        delivered = [re.sub(r'^\s*\d+(?:→|\t)', '', s).strip() for s in result_text(result).splitlines()]
        delivered = [s for s in delivered if s]
        if any(delivered[i:i + len(wanted)] == wanted for i in range(len(delivered))): return True
    return False


def clean(text, destination):
    for path, replacement in [(str(destination), '/fixture'), (str(destination).removeprefix('/private'), '/fixture'),
                              (str(ROOT), '/context-docs-repo'), (str(Path.home()), '/user-home')]:
        text = text.replace(path, replacement)
    return text


def trajectory(log, events, project, evidence, destination):
    """Export scope and returned-byte evidence, not upstream source bodies or host events."""
    results = results_by_id(log); output = []
    for e in events:
        if e.get('hook_event_name') != 'PreToolUse': continue
        name = e.get('tool_name'); payload = e.get('tool_input') or {}
        if name not in hook.TOOLS: continue
        raw = payload.get('file_path') or payload.get('path') or str(project)
        path = (project / raw).resolve()
        label = next((tag + '/' + path.relative_to(root).as_posix() for tag, root in [('project', project), ('evidence', evidence)] if hook.within(path, root)), '[outside permitted roots]')
        result = results.get(e.get('tool_use_id'), {}); text = result_text(result)
        output.append(dict(tool=name, path=label, decision=e.get('decision'),
            reason=clean(e.get('reason', ''), destination), result_present=bool(result),
            result_error=result.get('is_error') if result else None, result_sha256=sha(text.encode()),
            result_characters=len(text), offset=payload.get('offset'), limit=payload.get('limit')))
    return output


INTEGRITY_GATES = ('tool_catalog_restricted', 'all_tool_calls_guarded', 'no_successful_denied_tool',
    'successful_writes_allowed', 'responding_model_matches', 'native_skill_catalog_empty',
    'readonly_evidence_unchanged', 'immutable_bytes_and_modes', 'authorized_new_files',
    'readme_prefix', 'readme_kind_and_mode', 'no_external_loading', 'initial_loading_observed',
    'controls_unchanged', 'process_exit_valid', 'postprocess_ok')


def stop_reason(checks, error, timed_out=False):
    failed = [k for k in INTEGRITY_GATES if k in checks and not checks[k]]
    if failed: return 'Integrity/infrastructure gates failed: ' + ', '.join(failed)
    if error not in (None, 'permission_denied') and not (timed_out and error == 'missing_terminal_result'):
        return 'Execution infrastructure error: ' + str(error)
    return None


def should_stop(checks, error, timed_out=False):
    return stop_reason(checks, error, timed_out) is not None


def decode_artifact(raw):
    try: return raw.decode('utf-8'), True
    except UnicodeError: return raw.decode('utf-8', errors='replace'), False


def record_status(destination, planned, attempted, reason=None, state='running'):
    value = dict(planned=planned, attempted=attempted, unrun=[s for s in planned if s not in attempted],
        state=state, stopped_after=attempted[-1] if reason and attempted else None, stop_reason=reason)
    dump(destination / 'status.json', value)
    return value


def run(destination, expected_hash):
    if (destination / 'logs').exists(): raise ValueError('Execution already attempted; no retries.')
    p = validate(destination, expected_hash)
    if any((destination / 'control').glob('*.events.jsonl')): raise ValueError('Prior hook evidence exists.')
    for session in p['sessions']: preflight(destination, p, session)
    (destination / 'logs').mkdir(); trials = []; planned = [s['id'] for s in p['sessions']]; attempted = []
    dump(destination / 'trials.json', trials); record_status(destination, planned, attempted)
    for session in p['sessions']:
        try:
            validate(destination, expected_hash); preflight(destination, p, session)
        except Exception as error:
            record_status(destination, planned, attempted, 'Preflight before ' + session['id'] + ': ' + str(error), 'stopped')
            break
        sid = session['id']; unit = destination / 'sessions' / sid; project = unit / 'project'; evidence = unit / 'evidence'
        local = {**p, 'extra_args': ['--no-session-persistence', '--disable-slash-commands', '--effort', p['requested_effort'],
                 '--tools', ','.join(hook.TOOLS), '--settings', str(destination / 'control' / (sid + '.settings.json'))]}
        log = destination / 'logs' / (sid + '.jsonl'); print('Starting ' + sid, flush=True)
        attempted.append(sid); record_status(destination, planned, attempted)
        checks = {}; trial = dict(id=sid, execution_checks=checks)
        try:
            execution = smoke.run_session(project, session['prompt'], log, local)
            trial.update(execution=execution, timed_out=execution['exit_code'] == 124)
            observed = smoke.parse_stream(log); model = helper.observed_models(log)
            trial.update(execution_error=observed['execution_error'], model_evidence=model, final_message=observed['final_message'] or '')
            events = guarded.read_events(destination / 'control' / (sid + '.events.jsonl'))
            after = snapshot(project); before = p['initial_hashes'][sid]
            checks.update(guarded.coverage(log, events, p['allowed_tools']))
            checks.update(completed=execution['exit_code'] == 0 and 'result' in observed['event_types'],
                process_exit_valid=execution['exit_code'] in (0, 124),
                native_skill_catalog_empty=native_skills_disabled(log),
                responding_model_matches=model['responding_models'] == [p['model']],
                readonly_evidence_unchanged=snapshot(evidence) == p['evidence_hashes'][sid],
                immutable_bytes_and_modes=all(after.get(n) == v for n, v in before.items() if n != 'README.md'),
                authorized_new_files=set(after) - set(before) <= {session['output']},
                readme_prefix=(project / 'README.md').read_bytes().startswith(base64.b64decode(p['configurations'][sid]['readme_prefix_b64'])),
                readme_kind_and_mode=all(after.get('README.md', {}).get(k) == before['README.md'][k] for k in ('kind', 'mode')),
                no_external_loading=all(Path(e.get('file_path', '')).resolve() == project / 'CLAUDE.md' for e in events if e.get('hook_event_name') == 'InstructionsLoaded'),
                initial_loading_observed=any(e.get('hook_event_name') == 'InstructionsLoaded' and Path(e.get('file_path', '')).resolve() == project / 'CLAUDE.md'
                    and e.get('load_reason') == 'session_start' and e.get('file_sha256_at_event') == before['CLAUDE.md']['sha256'] for e in events),
                controls_unchanged=all(sha((destination / 'control' / n).read_bytes()) == v['sha256'] for n, v in p['control_hashes'].items()))
            checks['treatment_delivery'] = complete_skill_read(log, events, project, p['frozen_skill_body']) if session['arm'] == 'skill' else not (project / '.claude/skills').exists()
            trial['after_hashes'] = after
            dump(destination / 'logs' / (sid + '.checks.json'), checks)
            handoff = project / session['output']; readme = (project / 'README.md').read_bytes()
            prefix = base64.b64decode(p['configurations'][sid]['readme_prefix_b64'])
            body, body_valid = decode_artifact(handoff.read_bytes()) if handoff.is_file() else (None, True)
            append, append_valid = decode_artifact(readme[len(prefix):]) if readme.startswith(prefix) else (None, True)
            checks.update(handoff_utf8_valid=body_valid, readme_append_utf8_valid=append_valid)
            trial.update(handoff=body, readme_append=append,
                behavioral_denials=[dict(tool=e.get('tool_name'), reason=e.get('reason')) for e in events if e.get('decision') == 'deny'],
                trajectory=trajectory(log, events, project, evidence, destination))
            checks['postprocess_ok'] = True
        except Exception as error:
            # Preserve the attempted session even if a diagnostic parser fails.
            checks['postprocess_ok'] = False
            trial['infrastructure_error'] = type(error).__name__ + ': ' + str(error)
            trial.setdefault('execution', dict(exit_code=None, seconds=None))
        trials.append(trial); dump(destination / 'trials.json', trials)
        print('Completed ' + sid + ': failed gates ' + str([k for k, v in trial['execution_checks'].items() if not v]), flush=True)
        reason = stop_reason(checks, trial.get('execution_error'), trial.get('timed_out', False))
        if reason:
            record_status(destination, planned, attempted, reason, 'stopped')
            print('Infrastructure gate failed; preserve this attempt and stop.'); break
    else:
        record_status(destination, planned, attempted, state='completed')


def export_data(p, trials, destination):
    result = {k: p[k] for k in ('kind', 'build_id', 'built_at', 'model', 'requested_effort', 'effort_observed', 'cli_version',
        'package_commit', 'package_version', 'package_hashes', 'session_timeout_seconds', 'skill_delivery', 'source_hashes', 'source_identities', 'frozen_input_hashes')}
    result['protocol_sha256'] = sha((destination / 'protocol.json').read_bytes())
    status = json.loads((destination / 'status.json').read_text())
    result.update(json.loads(clean(json.dumps(status), destination)))
    result['sessions'] = []
    for t in trials:
        selected = {k: t[k] for k in ('id', 'execution_checks', 'model_evidence', 'execution_error', 'infrastructure_error',
            'after_hashes', 'final_message', 'handoff', 'readme_append', 'behavioral_denials', 'trajectory', 'timed_out') if k in t}
        selected.update(exit_code=t['execution']['exit_code'], seconds=t['execution']['seconds'])
        result['sessions'].append(json.loads(clean(json.dumps(selected), destination)))
    result['prompts'] = {s['id']: s['prompt'] for s in p['sessions']}
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); sub = parser.add_subparsers(dest='action', required=True)
    for name in ('build', 'validate', 'run', 'export'):
        command = sub.add_parser(name); command.add_argument('destination', type=Path)
        if name == 'build':
            command.add_argument('--sources', type=Path, default=ROOT / '.local/public-history-snapshots')
            command.add_argument('--scout', type=Path, default=ROOT / '.local/public-history-scout-20261010')
        if name in ('validate', 'run'): command.add_argument('--frozen-sha256', required=True)
        if name == 'export': command.add_argument('output', type=Path)
    args = parser.parse_args(); destination = args.destination.resolve()
    if args.action == 'build': build(destination, args.sources.resolve(), args.scout.resolve())
    elif args.action == 'validate':
        p = validate(destination, args.frozen_sha256)
        for session in p['sessions']: preflight(destination, p, session)
        print('Frozen inputs and four untouched fixtures verified; no sessions launched.')
    elif args.action == 'run': run(destination, args.frozen_sha256)
    else:
        if args.output.exists(): raise ValueError('Preserve the existing export.')
        dump(args.output, export_data(json.loads((destination / 'protocol.json').read_text()), json.loads((destination / 'trials.json').read_text()), destination))
