"""Build instruction-file routing regressions for adoption v0.1.3.

A maintenance rule only takes effect in the instruction file the client actually
loads. These cases cover a project whose instructions live in CLAUDE.md and a
project holding both files, where the loaded one must reach the rule without a
second copy. Client loading rules are external behavior: these fixtures state
which file is in effect in the request, rather than detecting a client.

This builder runs static grader controls only. Model sessions and semantic
review must be executed and reported separately.
"""
import argparse
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# Load the sibling adoption fixtures under another name: evals/suite/build.py and
# evals/adoption/build.py share a module name, as in marker.py.
loader = importlib.util.spec_from_file_location('adoption_cases', Path(__file__).with_name('build.py'))
adoption = importlib.util.module_from_spec(loader); loader.loader.exec_module(adoption)
from build import build, write
from verify import grade

RULE = adoption.RULE
REQUEST = ('Use the adopt-context-docs skill to adopt Context Docs in this project, '
           'including its ongoing maintenance rule in the loaded project instructions.')
REPEAT = REQUEST + ' No new project evidence or decisions have been supplied.'
CLAUDE_CLIENT = (' This project keeps its agent instructions in CLAUDE.md;'
                 ' no AGENTS.md is loaded here.')
SPLIT_CLIENT = (' This client loads CLAUDE.md only; AGENTS.md is kept for'
                ' another tool. Do not duplicate guidance between them.')
FIRST_DATE = ' For this test, treat the current date as 2026-10-01, regardless of the environment date.'
NEXT_DATE = ' For this test, treat the current date as 2026-10-02, regardless of the environment date.'
STATE, BLOCKER = adoption.STATE, adoption.BLOCKER

README = '# Offline pilot\n\n[Current context](knowledge/state.md).\n'
CLAUDE = ('# Project instructions\n\nUse the existing knowledge/ layout.\n'
          'Production publication requires owner approval.\n')
AGENTS_ONLY = '# Agent instructions\n\nRun `python3 -m pytest` before proposing a change.\n'
# One valid reference: the rule reaches the loaded file through an import.
IMPORT = '\nProject conventions are maintained in @AGENTS.md.\n'
CASES = [
    dict(id='adopt-claude-instructions',
         files={'README.md': README, 'CLAUDE.md': CLAUDE, 'knowledge/state.md': STATE},
         uncommitted={'knowledge/state.md': STATE + BLOCKER},
         protected=['Use the existing knowledge/ layout.',
                    'Production publication requires owner approval.',
                    'Approved: keep the pilot offline because customer data must stay local.',
                    BLOCKER.strip()],
         immutable=['README.md'], steps=[
             dict(request=REQUEST + CLAUDE_CLIENT + FIRST_DATE,
                  updates={}, oracle={'CLAUDE.md': CLAUDE + RULE.replace('$context-docs', 'the context-docs skill')
                                      + '\nMethod: context-docs\nAdopted: 2026-10-01\n'
                                        'Entry point: knowledge/state.md\n'}, rubric=[
                 'Places the ongoing maintenance rule and marker in the loaded CLAUDE.md, preserving its existing instructions.',
                 'Does not create an unloaded AGENTS.md, or a second instruction file holding the only copy of the rule.',
                 'References the skill in wording valid for this client instead of another client\'s invocation syntax.',
             ]),
             dict(request=REPEAT + CLAUDE_CLIENT + NEXT_DATE, updates={}, oracle={}, rubric=[
                 'Repeated adoption leaves instructions and documents byte-identical, with one rule and one marker.',
             ]),
         ]),
    dict(id='adopt-split-instructions',
         files={'README.md': README, 'CLAUDE.md': CLAUDE, 'AGENTS.md': AGENTS_ONLY,
                'knowledge/state.md': STATE},
         uncommitted={},
         protected=['Use the existing knowledge/ layout.',
                    'Run `python3 -m pytest` before proposing a change.',
                    'Approved: keep the pilot offline because customer data must stay local.'],
         immutable=['README.md', 'knowledge/state.md'], steps=[
             dict(request=REQUEST + SPLIT_CLIENT + FIRST_DATE,
                  updates={}, oracle={
                      'AGENTS.md': AGENTS_ONLY + RULE.replace('$context-docs', 'the context-docs skill')
                      + '\nMethod: context-docs\nAdopted: 2026-10-01\nEntry point: knowledge/state.md\n',
                      'CLAUDE.md': CLAUDE + IMPORT}, rubric=[
                 'The rule is reachable from the loaded CLAUDE.md, by placement or an explicit reference to the file that holds it.',
                 'Both existing instruction files keep their original content; the rule and marker are not copied into both.',
                 'Reports which file now carries the rule and how the loaded file reaches it.',
             ]),
             dict(request=REPEAT + SPLIT_CLIENT + NEXT_DATE, updates={}, oracle={}, rubric=[
                 'Repeated adoption preserves all project files byte-identically, including one rule and marker with the original date.',
             ]),
         ]),
]


def controls():
    results = []
    for case in CASES:
        initial = {**case['files'], **case['uncommitted']}
        reference = {**initial, **case['steps'][0]['oracle']}
        spec = dict(id=case['id'], before=initial, protected=case['protected'],
                    immutable=case['immutable'], entry='README.md', allow_noop=False)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'project'; root.mkdir(); output = Path(tmp) / 'output'; output.mkdir()
            for p, s in initial.items(): write(root / p, s)
            assert not grade(spec, root, output)['mechanical_pass'], 'unchanged first pass must fail'
            for p, s in reference.items(): write(root / p, s)
            assert grade(spec, root, output)['mechanical_pass'], 'reference must pass'
            repeated = {**spec, 'before': reference, 'allow_noop': True}
            assert grade(repeated, root, output)['mechanical_pass'], 'no-change repeat must pass'
            saved = (root / 'CLAUDE.md').read_text()
            (root / 'CLAUDE.md').write_text(saved + '\n[Missing](absent.md)\n')
            assert not grade(repeated, root, output)['mechanical_pass'], 'broken link must fail'
            (root / 'CLAUDE.md').write_text(saved)
            # Reverting every instruction file must fail the marker preservation token.
            dropped = {**repeated, 'protected': case['protected'] + ['Adopted: 2026-10-01']}
            for name, body in [('CLAUDE.md', CLAUDE), ('AGENTS.md', AGENTS_ONLY)]:
                if name in case['files']:
                    write(root / name, body)
            result = grade(dropped, root, output)
            assert not result['mechanical_pass'], 'removed marker must fail'
            assert any(not passed for name, passed in result['checks'].items()
                       if name.startswith('preserved:')), 'must fail on the marker token'
        results.append({'case': case['id'], 'reference': True, 'unchanged_first_pass_rejected': True,
                        'repeat_reference': True, 'broken_link_rejected': True,
                        'removed_marker_rejected': True})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    checks = controls()
    dest = args.destination.resolve()
    manifest = build(dest, cases=CASES, variants={'skill': ROOT / 'skills'}, attempts=1)
    for case in CASES:
        for i in range(len(case['steps'])):
            task = dest / (case['id'] + '-skill')
            folder = task / 'steps' / f'pass-{i+1}' if len(case['steps']) > 1 else task
            p = folder / 'instruction.md'
            instruction = p.read_text().replace(
                'Use the context-docs skill at /opt/context-docs/SKILL.md and its relevant references.',
                'Read the adoption skill at /opt/context-docs/adopt-context-docs/SKILL.md and its linked core skill. These are installed outside the project; read them there.')
            instruction += '\nKeep these project files byte-identical: ' + ', '.join(case['immutable']) + '.\n'
            p.write_text(instruction)
            p = folder / 'tests/spec.json'
            spec = json.loads(p.read_text()); spec['allow_noop'] = i > 0
            spec['external_reference_roots'] = ['/opt/context-docs']
            spec['external_references'] = {
                '/opt/context-docs/' + str(source.relative_to(ROOT / 'skills')):
                    hashlib.sha256(source.read_bytes()).hexdigest()
                for source in sorted((ROOT / 'skills').rglob('*')) if source.is_file()}
            p.write_text(json.dumps(spec, indent=2) + '\n')
    manifest['adoption_files'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in sorted((ROOT / 'skills/adopt-context-docs').rglob('*')) if p.is_file()}
    manifest['instructions_builder_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    manifest['controls'] = checks
    write(dest.parent / (dest.name + '-manifest.json'), json.dumps(manifest, indent=2) + '\n')
    print(f'Built {len(CASES)} trajectories / {sum(len(c["steps"]) for c in CASES)} model sessions. '
          f'{5 * len(CASES)} static grader controls passed. No model run is included.')


if __name__ == '__main__':
    main()
