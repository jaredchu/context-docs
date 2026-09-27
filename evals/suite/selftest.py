"""Validate reference solutions and deliberately broken controls before model runs."""
import tempfile
from pathlib import Path
from build import spec_for
from cases import CASES
from verify import grade, link_errors, snapshot


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
    # A valid alternative first-pass output differs from the reference. This used
    # to let a subsequent no-op pass the edit check. Capture its actual input.
    case = CASES[-1]
    with tempfile.TemporaryDirectory() as temp:
        root, output = Path(temp) / 'project', Path(temp) / 'output'
        root.mkdir(); output.mkdir()
        before = {**case['files'], **case['steps'][0]['oracle'], **case['steps'][1]['updates']}
        put(root, before)
        p = root / 'context.md'
        p.write_text(p.read_text() + '\nAdditional valid operator note.\n')
        (root / 'operator.md').write_text('Unique work carried from the previous pass.\n')
        actual = snapshot(root)
        spec = spec_for(case, 1, before)
        assert grade(spec, root, output)['checks']['documentation_changed']
        assert not grade(spec, root, output, actual)['checks']['documentation_changed']
        p.write_text(p.read_text().replace('60 seconds', '45 seconds'))
        assert grade(spec, root, output, actual)['mechanical_pass']
        assert grade(spec, root, output, actual)['before_documents']['operator.md'] == actual['operator.md']
        (root / 'operator.md').unlink()
        assert not grade(spec, root, output, actual)['checks']['input_files_retained']
    print(f'{n + 7} reference/control assertions passed, including actual multi-pass inputs.')


if __name__ == '__main__':
    main()
