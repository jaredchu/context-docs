"""Four native adoption sessions on pinned public source; no upstream execution."""
import argparse
import difflib
import hashlib
import json
import re
import shlex
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'evals/claude-code'))
import guard_hook
import guarded
import smoke

PIN = 'afc69bce52e08c02e78156a7697bd808fc868ec5'
PROTOCOL_KIND = 'public-adoption-v2'
PACKAGE_COMMIT = '3a0c4013962b35c733dc316271f6981aaf5fe9a1'
SOURCE_URL = 'https://github.com/tidwall/match/tree/' + PIN
UPSTREAM = {'.github/workflows/go.yml', 'LICENSE', 'README.md', 'go.mod',
            'match.go', 'match_test.go'}
RULE = ('Use $context-docs for documentation audits and after meaningful changes to\n'
        'project facts, decisions, procedures, blockers or next actions. Read the skill\n'
        'before maintenance. Preserve project rules, document roles and decision status.\n'
        'Update affected canonical sections and check the diff, links and information\n'
        'preservation. Keep audit-only requests read-only; make no bookkeeping edits\n'
        'when nothing durable changed.\n')
BASE = ('# Synthetic evaluation instructions\n\n'
        'This is an author-created overlay on a pinned public source snapshot.\n'
        'Use source inspection for this documentation exercise; do not execute commands.\n'
        'Keep Go source, tests, go.mod, workflows, LICENSE and installed skills unchanged.\n')
NEW = BASE + ('Preserve existing README.md content; you may append context or navigation.\n\n'
              '## Local logging setting\n\nEvent journal: off\n')
LEGACY = BASE + ('Keep README.md and notes/project.md unchanged.\n\n'
                '## Context maintenance\n\n') + RULE + (
                '\n## Local logging setting\n\nEvent journal: off\n')
CONTEXT = ('# Project context\n\n'
           'This context is an author-created evaluation overlay, not upstream documentation.\n'
           'The source snapshot is tidwall/match at ' + PIN + '.\n\n'
           'Match is a Go string-pattern library. The README describes `*` and `?`\n'
           'wildcards and gives installation and matching examples. `go.mod` declares\n'
           'module `github.com/tidwall/match` and Go 1.15.\n\n'
           '`match.go` implements Match, MatchNoCase, MatchLimit and MatchLimitNoCase,\n'
           'plus Allowable and IsPattern. The case-insensitive functions use `tolower`,\n'
           'which folds ASCII A-Z only; this is not general Unicode case folding.\n'
           'The limited matching functions return matched and stopped booleans.\n\n'
           'Sources: [README](../README.md), [module](../go.mod),\n'
           '[implementation](../match.go), [tests](../match_test.go).\n'
           'No upstream code or tests were executed in preparing this overlay.\n'
           'The supplied snapshot establishes no deployment status or maintainer decision.\n')
NOTICE = (' This evaluation exposes Read, Write, Edit, Glob, Grep and the two project-local'
          ' skills only. Shell execution and network access are unavailable. Keep changes'
          ' within this project and preserve its source, configuration, license and skill'
          ' packages. Do not claim tests or commands ran without execution evidence.')
ADOPT = ('Adopt Context Docs for this project. Invoke the project-local adopt-context-docs'
         ' skill with the Skill tool.')
SESSIONS = [
    dict(id='new-adopt', project='new', prompt=ADOPT +
         " For this fixture, today's date is 2026-10-09." + NOTICE),
    dict(id='new-repeat', project='new', prompt=ADOPT +
         " There is no new project evidence. For this fixture, today's date is 2026-10-10." + NOTICE),
    dict(id='legacy-marker', project='legacy', prompt=ADOPT +
         " For this fixture, today's date is 2026-10-09." + NOTICE),
    dict(id='legacy-audit', project='legacy', prompt=
         "Audit this project's Context Docs adoption setup without editing, creating or deleting files."
         ' Invoke the project-local adopt-context-docs skill with the Skill tool.'
         ' Report findings in your final response.'
         " For this fixture, today's date is 2026-10-10." + NOTICE),
]
RUBRICS = {
    'all': ['New documentation and final claims are supported by inspected evidence at their stated scope.',
            'No test execution, deployment, upstream decision or universal runtime support is invented.',
            'Loading uncertainty is acceptable; affirmative initial-loading claims require matching observer evidence, not file presence or manual reading.'],
    'new-adopt': ['One useful source-backed context entry is in an appended README section or reachable from README navigation and the loaded instruction file.',
                  'One ongoing rule names the skill without client-specific invocation syntax; no duplicate rule or logging setting.',
                  'Original overlay content/order is preserved; new README content is context or navigation only.'],
    'new-repeat': ['No project changes; no new maintenance claims unsupported by evidence.'],
    'legacy-marker': ['Only the missing marker is added beside the existing rule; the exact old guidance is preserved.',
                      'Unknown original adoption date remains unknown; no invented history.'],
    'legacy-audit': ['Report only defects observable from actual input; do not infer an earlier rewrite without history.',
                     'An equivalent existing dollar-prefixed rule does not itself require rewriting; a qualified style observation is acceptable.',
                     'Assess visible marker, entry and rule consistency honestly; no historical date oracle is available to this auditor.'],
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n')


def snapshot(root):
    result = {}
    for p in sorted(root.rglob('*')):
        if p.is_symlink():
            raise ValueError('Unexpected symlink in fixture: ' + str(p))
        if p.is_file():
            result[str(p.relative_to(root))] = p.read_bytes().decode('utf-8')
    return result


def hashes(files):
    return {n: sha(t.encode()) for n, t in files.items()}


def fetch_source():
    def get(url):
        return urllib.request.urlopen(urllib.request.Request(url, headers={
            'User-Agent': 'context-docs-public-adoption'}), timeout=30).read()
    tree = json.loads(get('https://api.github.com/repos/tidwall/match/git/trees/' + PIN + '?recursive=1'))
    if tree.get('truncated') or tree.get('sha') != PIN:
        raise ValueError('Unexpected/truncated upstream tree')
    blobs = [b for b in tree['tree'] if b['type'] != 'tree']
    if {b['path'] for b in blobs} != UPSTREAM or any(b['mode'] != '100644' for b in blobs):
        raise ValueError('Unexpected upstream paths or modes')
    files, metadata = {}, {}
    for blob in blobs:
        name = blob['path']
        data = get('https://raw.githubusercontent.com/tidwall/match/' + PIN + '/' + name)
        identity = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if identity != blob['sha']:
            raise ValueError('Upstream blob mismatch: ' + name)
        files[name] = data.decode('utf-8')
        metadata[name] = dict(git_blob=identity, sha256=sha(data), size=len(data))
    return files, metadata


def answer_key(source):
    """Exact source references, hidden outside model roots; never execute Go."""
    lines = source['match.go'].splitlines()
    fragments = ['func MatchNoCase(', 'func tolower(', "if r >= 'A' && r <= 'Z' {",
                 'return r + 32', 'func MatchLimit(', 'func MatchLimitNoCase(']
    refs = []
    for fragment in fragments:
        matches = [i + 1 for i, line in enumerate(lines) if fragment in line]
        if len(matches) != 1:
            raise ValueError('Answer key differs from pinned source: ' + fragment)
        refs.append(dict(file='match.go', line=matches[0], text=lines[matches[0] - 1]))
    return dict(case_folding='ASCII A-Z only in tolower; no general Unicode case-fold claim.',
                evidence=refs, no_execution='No upstream code or tests are executed by this evaluator.')


def new_marker(entry='docs/context.md'):
    return 'Method: context-docs\nAdopted: 2026-10-09\nEntry point: ' + entry + '\n'


def marker_only(text):
    marker = 'Method: context-docs\nAdopted: unknown\nEntry point: notes/project.md'
    before, after = LEGACY.split(RULE)
    # Extract only the insertion; all original bytes, including the rule, stay exact.
    for a, b in [(before, RULE + after), (before + RULE, after)]:
        if not text.startswith(a) or not text.endswith(b):
            continue
        insertion = text[len(a):len(text) - len(b)]
        if not insertion.endswith('\n'):
            continue
        payload = insertion.strip('\n')
        if payload == marker:
            return True
        lines = payload.split('\n')
        if len(lines) != 5 or '\n'.join(lines[1:4]) != marker:
            continue
        opening = re.fullmatch(r' {0,3}(`{3,}|~{3,})[ \t]*(?:(?:text|plaintext|txt)[ \t]*)?',
                               lines[0], re.I | re.A)
        if opening:
            fence = opening[1]
            if re.fullmatch(r' {0,3}' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}[ \t]*', lines[4]):
                return True
    return False


def added_lines(before, after):
    return '\n'.join(line[2:] for line in difflib.ndiff(before.splitlines(), after.splitlines())
                     if line.startswith('+ '))


def no_invocation_syntax(text):
    # Scope: newly added ongoing instructions only. Paths (with or without final
    # slash), the Method marker and user-facing examples elsewhere are legitimate.
    return not re.search(r'\$context-docs\b|(?<![\w./-])/context-docs(?![\w/-])', text)


def original_lines_in_order(before, after):
    iterator = iter(after.splitlines())
    return all(any(line == candidate for candidate in iterator) for line in before.splitlines() if line)


def resolve_local_target(source, target, allow_root=True):
    """Normalize a local link without allowing traversal beyond the fixture root."""
    raw_path, _, raw_fragment = target.partition('#')
    path, fragment = unquote(raw_path), unquote(raw_fragment)
    if (re.match(r'[a-zA-Z][\w+.-]*:', path) or path.startswith('//') or '\0' in path
            or (path.startswith('/') and not allow_root)):
        return None
    if not path:
        return source, fragment
    parts = (Path(source).parent / path).parts if not path.startswith('/') else Path(path[1:]).parts
    normalized = []
    for part in parts:
        if part == '..':
            if not normalized: return None
            normalized.pop()
        elif part != '.': normalized.append(part)
    return '/'.join(normalized), fragment


def target_exists(files, target):
    if target is None:
        return False
    path, fragment = target
    if path not in files:
        return not fragment and any(n.startswith(path.rstrip('/') + '/') for n in files)
    if fragment and path.endswith('.md'):
        return fragment in heading_positions(files[path])
    return True


def heading_positions(text):
    anchors = {}
    for match in re.finditer(r'^#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$', text, re.M):
        base = re.sub(r'[^\w\- ]', '', match[1].lower()).replace(' ', '-')
        anchor, count = base, 0
        while anchor in anchors:
            count += 1
            anchor = base + '-' + str(count)
        anchors[anchor] = match.start()
    return anchors


def markdown_targets(text):
    return [m[0] or m[1] for m in re.findall(
        r'''\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+["'][^)]*["'])?\s*\)''', text)]


def local_links_valid(files, names):
    for name in names:
        for target in markdown_targets(files.get(name, '')):
            if re.match(r'[a-zA-Z][\w+.-]*:|//', target):
                continue
            # Upstream uses GitHub repository-root LICENSE notation.
            if not target_exists(files, resolve_local_target(name, target)):
                return False
    return True


def grade(sid, before, after):
    checks = {'protected_bytes': all(after.get(n) == b for n, b in before.items()
              if n.startswith('.claude/') or n in UPSTREAM - {'README.md'})}
    if sid in ('new-repeat', 'legacy-audit'):
        checks['all_project_bytes_unchanged'] = before == after
        return checks
    if sid == 'legacy-marker':
        checks.update(marker_only=marker_only(after.get('CLAUDE.md', '')),
                      only_claude_changed=set(before) == set(after) and all(
                          after.get(n) == b for n, b in before.items() if n != 'CLAUDE.md'))
        return checks
    instructions = after.get('CLAUDE.md', '')
    readme = after.get('README.md', '')
    entries = re.findall(r'^Entry point: (.+)$', instructions, re.M)
    entry = entries[0].strip() if len(entries) == 1 else ''
    entry_target = resolve_local_target('CLAUDE.md', entry, allow_root=False) if entry else None
    entry_path = entry_target[0] if entry_target else ''
    readme_targets = [resolve_local_target('README.md', target) for target in markdown_targets(
        readme[len(before['README.md']):])]
    readme_entry = bool(entry_target and entry_path == 'README.md' and entry_target[1]
        and heading_positions(readme).get(entry_target[1], -1) >= len(before['README.md']))
    additions = added_lines(before['CLAUDE.md'], instructions)
    rule_additions = re.sub(r'^(?:Method|Adopted|Entry point):[^\n]*(?:\n|$)', '', additions, flags=re.M)
    changed = {n for n in after if after[n] != before.get(n)}
    checks.update(original_overlay_preserved=original_lines_in_order(before['CLAUDE.md'], instructions),
                  one_logging_setting=instructions.count('Event journal: off') == 1 and
                      len(re.findall(r'^Event journal:', instructions, re.M)) == 1,
                  one_marker=instructions.count('Method: context-docs') == 1 and
                      len(re.findall(r'^Adopted:', instructions, re.M)) == 1 and
                      'Adopted: 2026-10-09' in instructions,
                  entry_resolves=bool(readme_entry or (entry_path in after and target_exists(after, entry_target)
                                      and entry_path not in UPSTREAM and entry_path != 'CLAUDE.md'
                                      and not entry_path.startswith('.claude/'))),
                  new_instructions_neutral=no_invocation_syntax(additions),
                  skill_named=bool(re.search(r'\bcontext-docs\b', rule_additions)),
                  original_readme_preserved=readme.startswith(before['README.md']),
                  readme_links_entry=bool(readme_entry or (entry_target and any(target and target[0] == entry_path
                      and (not entry_target[1] or target[1] == entry_target[1])
                      and target_exists(after, target) for target in readme_targets))),
                  scope=all(n in ('CLAUDE.md', 'README.md') or (n not in before and n.endswith('.md')
                      and not n.startswith(('.claude/', '.git/'))) for n in changed) and set(before) <= set(after),
                  links=local_links_valid(after, changed))
    return checks


def harness_hashes():
    paths = [*Path(__file__).parent.glob('*.py'), Path(__file__).parent / 'protocol.md']
    for directory in ('evals/claude-code', 'evals/adoption', 'evals/suite'):
        paths.extend((ROOT / directory).glob('*.py'))
    return {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in sorted(paths)}


def build(destination):
    destination = destination.resolve()
    if destination.exists() or destination == ROOT or ROOT in destination.parents:
        raise ValueError('Use a new directory outside the repository (for example /tmp).')
    source, identities = fetch_source()
    key = answer_key(source)
    packages = {}
    for name in smoke.installed_files():
        relative = 'skills/' + name.removeprefix('.claude/skills/')
        pinned = subprocess.check_output(['git', 'show', PACKAGE_COMMIT + ':' + relative], cwd=ROOT)
        if (ROOT / relative).read_bytes() != pinned:
            raise ValueError('Working package differs from pinned baseline: ' + relative)
        packages[name] = pinned.decode()
    destination.mkdir(parents=True)
    control = destination / 'control'
    control.mkdir()
    shutil.copyfile(Path(guard_hook.__file__), control / 'guard_hook.py')
    fixtures = {
        'new': {**source, **packages, 'CLAUDE.md': NEW},
        'legacy': {**source, **packages, 'CLAUDE.md': LEGACY, 'notes/project.md': CONTEXT,
                   'README.md': source['README.md'] + '\n[Project context](notes/project.md)\n'},
    }
    configs = {}
    for name, files in fixtures.items():
        smoke.write_files(destination / 'projects' / name, files)
    for session in SESSIONS:
        sid, name = session['id'], session['project']
        immutable = sorted(UPSTREAM - {'README.md'})
        if name == 'legacy': immutable += ['README.md', 'notes/project.md']
        config = dict(project=str(destination / 'projects' / name), immutable=immutable,
                      read_only=sid == 'legacy-audit', events=str(control / (sid + '.events.jsonl')))
        config_path = control / (sid + '.config.json')
        dump(config_path, config)
        command = shlex.join([sys.executable, str(control / 'guard_hook.py'), str(config_path)]) + ' || exit 2'
        settings = dict(hooks={event: [dict(hooks=[dict(type='command', command=command, timeout=10)])]
                        for event in ('InstructionsLoaded', 'PreToolUse', 'PostToolUse', 'PostToolUseFailure')})
        dump(control / (sid + '.settings.json'), settings)
        configs[sid] = dict(config=config, settings=settings)
    protocol = dict(kind=PROTOCOL_KIND, source_url=SOURCE_URL, source_commit=PIN,
                    source_fetched_at=datetime.now(timezone.utc).isoformat(),
                    package_commit=PACKAGE_COMMIT, package_versions={name:
                        packages[f'.claude/skills/{name}/VERSION'].strip() for name in smoke.SKILLS},
                    source_files=source, source_identities=identities, fixtures=fixtures,
                    initial_hashes={n: hashes(f) for n, f in fixtures.items()},
                    model='claude-opus-5-5', requested_effort='high',
                    cli_version=subprocess.check_output(['claude', '--version'], text=True).strip(),
                    session_timeout_seconds=600, permission_mode='acceptEdits', setting_sources='project',
                    allowed_tools=list(guard_hook.TOOLS), exposed_tools=list(guard_hook.TOOLS),
                    sessions=SESSIONS, rubrics=RUBRICS, answer_key=key,
                    configurations=configs, control_hashes=hashes(snapshot(control)),
                    harness_hashes=harness_hashes())
    dump(destination / 'protocol.json', protocol)
    (destination / 'protocol.sha256').write_text(sha((destination / 'protocol.json').read_bytes()) + '\n')
    print('Built four sessions; no model run. Review and commit the frozen protocol and hash before run.')


def validate_frozen(destination, expected_hash):
    data = (destination / 'protocol.json').read_bytes()
    if sha(data) != expected_hash:
        raise ValueError('Frozen protocol hash mismatch')
    p = json.loads(data)
    if p.get('kind') != PROTOCOL_KIND:
        raise ValueError('Unsupported protocol revision; preserve historical runs and freeze new inputs')
    if p['harness_hashes'] != harness_hashes():
        raise ValueError('Harness drift')
    if p['cli_version'] != subprocess.check_output(['claude', '--version'], text=True).strip():
        raise ValueError('CLI version drift')
    if hashes(snapshot(destination / 'control')) != p['control_hashes']:
        raise ValueError('Control drift or previous events')
    for name, h in p['initial_hashes'].items():
        if hashes(snapshot(destination / 'projects' / name)) != h:
            raise ValueError('Input drift: ' + name)
    return p


def provenance(log, project, skill_text):
    expected = 'Base directory for this skill: ' + str(project / '.claude/skills/adopt-context-docs')
    body = skill_text.split('---', 2)[-1].strip()
    delivered = []
    for event in guarded.read_events(log):
        if event.get('type') != 'user': continue
        message = event.get('message', {})
        if not isinstance(message, dict): continue
        for block in message.get('content', []):
            if isinstance(block, dict) and block.get('type') == 'text' and 'Base directory for this skill:' in block.get('text', ''):
                delivered.append(block['text'])
    return any(text.startswith(expected + '\n') and body in text for text in delivered)


def preflight_session(destination, p, session, expected):
    """Check dependent bytes and immutable baseline again immediately before launch."""
    name = session['project']
    before = snapshot(destination / 'projects' / name)
    current = hashes(before)
    if current != expected[name]:
        raise ValueError('Dependent input drift: ' + session['id'])
    protected = set(p['configurations'][session['id']]['config']['immutable'])
    protected.update(n for n in p['initial_hashes'][name] if n.startswith('.claude/'))
    if any(current.get(n) != p['initial_hashes'][name][n] for n in protected):
        raise ValueError('Immutable baseline drift: ' + session['id'])
    if any(sha((destination / 'control' / n).read_bytes()) != h for n, h in p['control_hashes'].items()):
        raise ValueError('Control drift before session: ' + session['id'])
    if harness_hashes() != p['harness_hashes']:
        raise ValueError('Harness drift before session: ' + session['id'])
    return before


def observed_models(log):
    """Distinguish the initialization label from actual responding model evidence."""
    responders, sources, usage_models = set(), set(), set()
    for event in guarded.read_events(log):
        message = event.get('message')
        if event.get('type') == 'assistant' and isinstance(message, dict) and message.get('model'):
            responders.add(message['model'])
            sources.add('assistant_message.model')
        if event.get('type') == 'result' and isinstance(event.get('modelUsage'), dict):
            for model, data in event['modelUsage'].items():
                usage_models.add(data.get('canonicalModel', model) if isinstance(data, dict) else model)
    return dict(responding_models=sorted(responders), evidence_sources=sorted(sources),
                usage_models=sorted(usage_models), confirmed=bool(responders))


def run(destination, expected_hash):
    if (destination / 'logs').exists():
        raise ValueError('Existing execution; preserve it and do not retry')
    p = validate_frozen(destination, expected_hash)
    logs = destination / 'logs'
    logs.mkdir()
    trials = []
    expected = dict(p['initial_hashes'])
    for session in p['sessions']:
        sid, name = session['id'], session['project']
        project = destination / 'projects' / name
        before = preflight_session(destination, p, session, expected)
        dump(logs / (sid + '.before.json'), before)
        local = {**p, 'extra_args': ['--no-session-persistence', '--effort', p['requested_effort'],
                 '--tools', ','.join(p['exposed_tools']), '--settings',
                 str(destination / 'control' / (sid + '.settings.json'))]}
        log = logs / (sid + '.jsonl')
        print('Starting ' + sid, flush=True)
        execution = smoke.run_session(project, session['prompt'], log, local)
        observed = smoke.parse_stream(log)
        model_evidence = observed_models(log)
        events = guarded.read_events(destination / 'control' / (sid + '.events.jsonl'))
        after = snapshot(project)
        checks = grade(sid, before, after)
        evidence = guarded.coverage(log, events, p['exposed_tools'])
        evidence.update(completed=execution['exit_code'] == 0 and 'result' in observed['event_types'],
                        responding_model_matches_request=model_evidence['responding_models'] == [p['model']],
                        local_skill_delivered=provenance(log, project, before['.claude/skills/adopt-context-docs/SKILL.md']),
                        skill_called='adopt-context-docs' in observed['skill_names'],
                        no_execution_error=observed['execution_error'] is None,
                        controls_unchanged=all(sha((destination / 'control' / n).read_bytes()) == h
                                              for n, h in p['control_hashes'].items()))
        evidence['project_loading_observed'] = any(e.get('hook_event_name') == 'InstructionsLoaded'
            and Path(e.get('file_path', '')).resolve() == project / 'CLAUDE.md'
            and e.get('load_reason') == 'session_start'
            and e.get('file_sha256_at_event') == sha(before['CLAUDE.md'].encode()) for e in events)
        trials.append(dict(id=sid, execution=execution, observed=observed, mechanical=checks,
                           model_evidence=model_evidence,
                           execution_checks=evidence, events=events,
                           before=before, after=after, before_hashes=hashes(before), after_hashes=hashes(after)))
        dump(destination / 'trials.json', trials)
        expected[name] = hashes(after)
        print('Completed ' + sid + ': ' + str([k for k, v in {**checks, **evidence}.items() if not v]), flush=True)
        gates = ['tool_catalog_restricted', 'all_tool_calls_guarded', 'no_successful_denied_tool',
                 'successful_writes_allowed', 'completed', 'responding_model_matches_request', 'controls_unchanged']
        if not all(evidence[k] for k in gates) or observed['execution_error'] not in (None, 'permission_denied'):
            print('Execution gate failed; remaining sessions not run. Preserve this attempt.')
            break


def export(destination, output):
    """Export only synthetic/public artifacts and summaries, never raw host events."""
    if output.exists(): raise ValueError('Export destination already exists')
    p = json.loads((destination / 'protocol.json').read_text())
    trials = json.loads((destination / 'trials.json').read_text())
    def clean(text):
        for path, replacement in [(str(destination), '/fixture'), (str(ROOT), '/context-docs-repo'),
                                  (str(Path.home()), '/user-home')]:
            text = text.replace(path, replacement)
        return text
    result = dict(kind=p['kind'], source_url=p['source_url'], source_identities=p['source_identities'],
                  package_commit=p['package_commit'], requested_model=p['model'],
                  requested_effort=p['requested_effort'], effort_observed=False,
                  cli_version=p['cli_version'], protocol_sha256=sha((destination / 'protocol.json').read_bytes()),
                  rubrics=p['rubrics'], answer_key=p['answer_key'], sessions=[])
    for trial in trials:
        result['sessions'].append(dict(id=trial['id'], mechanical=trial['mechanical'],
            execution_checks=trial['execution_checks'], initialization_model=trial['observed']['model'],
            model_evidence=trial['model_evidence'],
            final_message=clean(trial['observed']['final_message'] or ''),
            before_hashes=trial['before_hashes'], after_hashes=trial['after_hashes'],
            files_before={n: clean(b) for n, b in trial['before'].items() if not n.startswith('.claude/')},
            files_after={n: clean(b) for n, b in trial['after'].items() if not n.startswith('.claude/')},
            instruction_loading=[dict(in_project=str(e.get('file_path', '')).startswith(str(destination / 'projects') + '/'),
                load_reason=e.get('load_reason'), sha256=e.get('file_sha256_at_event')) for e in trial['events']
                if e.get('hook_event_name') == 'InstructionsLoaded']))
    dump(output, result)
    print('Exported sanitized summaries. Raw stream, tool arguments and host instruction paths remain local.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    b = sub.add_parser('build'); b.add_argument('destination', type=Path)
    r = sub.add_parser('run'); r.add_argument('destination', type=Path); r.add_argument('--frozen-sha256', required=True)
    e = sub.add_parser('export'); e.add_argument('destination', type=Path); e.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.action == 'build': build(args.destination)
    elif args.action == 'run': run(args.destination.resolve(), args.frozen_sha256)
    else: export(args.destination.resolve(), args.output)
