"""Validate reference solutions and deliberately broken controls before model runs."""
import tempfile
from pathlib import Path
from build import spec_for
from cases import CASES
from verify import grade, link_errors


def put(root, files):
    for name, body in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)


def main():
    n = 0
    for case in CASES:
        before = {**case['files'], **case['uncommitted']}
        for i, step in enumerate(case['steps']):
            before.update(step['updates'])
            spec = spec_for(case, i, dict(before))
            with tempfile.TemporaryDirectory() as temp:
                root, output = Path(temp) / 'project', Path(temp) / 'output'
                root.mkdir(); output.mkdir()
                put(root, before)
                if not spec['allow_noop']:
                    assert not grade(spec, root, output)['mechanical_pass'], (case['id'], 'no-op passed')
                    n += 1
                edits = {p: s for p, s in step['oracle'].items() if not p.startswith('@output/')}
                reports = {p.removeprefix('@output/'): s for p, s in step['oracle'].items() if p.startswith('@output/')}
                put(root, edits); put(output, reports)
                assert grade(spec, root, output)['mechanical_pass'], (case['id'], grade(spec, root, output)['checks'])
                n += 1
                # Missing source/anchor targets must never silently pass.
                path = root / 'README.md'
                saved = path.read_text()
                path.write_text(saved + '\n[Broken](missing.md#absent)\n')
                assert not grade(spec, root, output)['mechanical_pass'], case['id']
                path.write_text(saved)
                n += 1
                # All tasks must reject loss of an original input file.
                path.unlink()
                assert not grade(spec, root, output)['mechanical_pass'], case['id']
                n += 1
                before.update(edits)
    assert not link_errors({'a.md': '# A\n[Go](b.md#hello-world)\n', 'b.md': '# Hello world\n'})
    assert link_errors({'a.md': '[Go](b.md#wrong)', 'b.md': '# Hello world\n'})
    print(f'{n + 2} reference/control assertions passed across 8 tasks and 10 steps.')


if __name__ == '__main__':
    main()
