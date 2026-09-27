"""Follow up the initial marker run's ambiguous evaluation-date wording."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

import marker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    checks = marker.controls()
    case = copy.deepcopy(marker.CASES[0])
    for step, old, date in zip(case['steps'],
                              ['The evaluation date is 2026-10-01.',
                               'The evaluation date is now 2026-10-02.'],
                              ['2026-10-01', '2026-10-02']):
        step['request'] = step['request'].replace(old,
            f'For this simulation, treat the current date as {date}, '
            'regardless of the actual environment date.')
    dest = args.destination.resolve()
    manifest = marker.build(dest, cases=[case],
                            variants={'skill': marker.ROOT / 'skills'}, attempts=1)
    for i in range(2):
        folder = dest / (case['id'] + '-skill') / 'steps' / f'pass-{i+1}'
        p = folder / 'instruction.md'
        p.write_text(p.read_text().replace(
            'Use the context-docs skill at /opt/context-docs/SKILL.md and its relevant references.',
            'Read the adoption skill at /opt/context-docs/adopt-context-docs/SKILL.md and its linked core skill. These are installed outside the project; read them there.'))
        p = folder / 'tests/spec.json'
        spec = json.loads(p.read_text()); spec['allow_noop'] = i > 0
        p.write_text(json.dumps(spec, indent=2) + '\n')
    sources = [Path(__file__), Path(marker.__file__), Path(marker.adoption.__file__)]
    manifest['marker_source_files'] = {
        str(p.relative_to(marker.ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sources}
    manifest['controls'] = checks
    manifest['followup'] = 'One new trajectory with explicit simulated dates; unchanged skills and criteria. Retain the original run.'
    marker.write(dest.parent / (dest.name + '-manifest.json'),
                 json.dumps(manifest, indent=2) + '\n')
    print('Built one trial / two sessions with explicit simulated dates; original static controls passed.')


if __name__ == '__main__':
    main()
