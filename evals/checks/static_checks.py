"""Repository static checks: packaging, links and published-table agreement.

These are mechanical repository checks. They establish nothing about agent
behavior; model evaluations remain separate and are reported separately.
"""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
SKILLS = {'context-docs': ['references/standard.md', 'assets/project-context.md',
                           'assets/decision-record.md', 'LICENSE', 'VERSION'],
          'adopt-context-docs': ['LICENSE', 'VERSION']}
SKILL_DEPENDENCIES = {'adopt-context-docs': ['context-docs']}
README_VERSION_LABELS = {'context-docs': 'core skill', 'adopt-context-docs': 'adoption skill'}
# Frozen skill copies used as evaluation fixtures. Their relative resource links
# resolve only after a study builder assembles a complete package, as recorded in
# evals/concise/README.md. Keep this list exact rather than skipping a directory.
LINK_EXCEPTIONS = {('evals/concise/candidate-SKILL.md', 'references/standard.md'),
                   ('evals/concise/candidate-SKILL.md', 'assets/project-context.md'),
                   ('evals/concise/original-SKILL.md', 'references/standard.md'),
                   ('evals/concise/original-SKILL.md', 'assets/project-context.md')}
# Generated result tables embedded in README.md, with the artifact each one comes from.
TABLES = {'quality-table': 'evals/results/2026-09-27-quality/table.md',
          'public-table': 'evals/results/2026-09-27-public/table.md',
          'routing-table': 'evals/results/2026-09-27-routing/table.md',
          'history-table': 'evals/results/2026-09-27-history/table.md',
          'evaluation-table': 'evals/results/2026-09-27-harbor/table.md'}
# Claude Code truncates description plus when_to_use at 1536 characters; Codex
# documents only name and description. Keep both fields inside the smaller limit.
DESCRIPTION_LIMIT = 1024
FRONTMATTER_FIELDS = {'name', 'description'}


def markdown_files():
    # .local is the repository's gitignored scratch area for generated studies.
    return [p for p in sorted(ROOT.rglob('*.md'))
            if '.git' not in p.relative_to(ROOT).parts
            and p.relative_to(ROOT).parts[0] != '.local']


def slugs(text):
    return {re.sub(r'[^a-z0-9\- ]', '', heading.lower()).replace(' ', '-')
            for heading in re.findall(r'^#+\s+(.*)$', text, re.M)}


def check_links(failures):
    checked = 0
    for source in markdown_files():
        relative = source.relative_to(ROOT).as_posix()
        for match in re.finditer(r'\[[^\]]*\]\(([^)]+)\)', source.read_text()):
            target = match.group(1).strip()
            if target.startswith(('http://', 'https://', 'mailto:', '#')):
                continue
            checked += 1
            path, _, fragment = target.partition('#')
            if not path:
                continue
            resolved = (source.parent / path).resolve()
            if (relative, target) in LINK_EXCEPTIONS:
                continue
            if not resolved.exists():
                failures.append(f'{relative}: missing link target {target}')
            elif fragment and resolved.suffix == '.md' and fragment.lower() not in slugs(resolved.read_text()):
                failures.append(f'{relative}: missing anchor {target}')
    return f'{checked} relative links and anchors'


def check_tables(failures):
    readme = (ROOT / 'README.md').read_text()
    for name, path in TABLES.items():
        embedded = re.search(r'<!-- %s:start -->\n(.*?)<!-- %s:end -->' % (name, name), readme, re.S)
        artifact = ROOT / path
        if embedded is None:
            failures.append(f'README.md: missing {name} markers')
        elif not artifact.is_file():
            failures.append(f'README.md: {name} has no published artifact at {path}')
        elif embedded.group(1) != artifact.read_text():
            failures.append(f'README.md: {name} differs from generated {path}')
    return f'{len(TABLES)} published result tables'


def check_skills(failures):
    for name, required in SKILLS.items():
        skill = ROOT / 'skills' / name
        document = skill / 'SKILL.md'
        if not document.is_file():
            failures.append(f'skills/{name}: no SKILL.md')
            continue
        text = document.read_text()
        frontmatter = re.match(r'---\n(.*?)\n---\n', text, re.S)
        if frontmatter is None:
            failures.append(f'skills/{name}: SKILL.md must open with YAML frontmatter')
            continue
        fields = dict(re.findall(r'^([A-Za-z_-]+):\s*(.*)$', frontmatter.group(1), re.M))
        if set(fields) != FRONTMATTER_FIELDS:
            failures.append(f'skills/{name}: frontmatter fields {sorted(fields)} != {sorted(FRONTMATTER_FIELDS)}')
        if fields.get('name') != name:
            failures.append(f'skills/{name}: frontmatter name {fields.get("name")!r} must match its directory')
        if len(fields.get('description', '')) > DESCRIPTION_LIMIT:
            failures.append(f'skills/{name}: description exceeds {DESCRIPTION_LIMIT} characters')
        for relative in required:
            if not (skill / relative).is_file():
                failures.append(f'skills/{name}: missing packaged file {relative}')
        version = (skill / 'VERSION')
        if version.is_file() and not re.fullmatch(r'\d+\.\d+\.\d+\n', version.read_text()):
            failures.append(f'skills/{name}: VERSION must hold one semantic version line')
        # Check nested references too. Only adoption may depend on the sibling core.
        allowed_roots = [skill.resolve()] + [
            (ROOT / 'skills' / dependency).resolve()
            for dependency in SKILL_DEPENDENCIES.get(name, [])]
        for source in sorted(skill.rglob('*.md')):
            for match in re.finditer(r'\[[^\]]*\]\(([^)]+)\)', source.read_text()):
                target = match.group(1).strip()
                if target.startswith(('http://', 'https://', 'mailto:', '#')):
                    continue
                path = Path(unquote(target.partition('#')[0]))
                resolved = (source.parent / path).resolve()
                if (path.is_absolute() or not resolved.exists()
                        or not any(resolved.is_relative_to(root) for root in allowed_roots)):
                    failures.append(f'{source.relative_to(ROOT)}: link {target} must resolve '
                                    'inside the package or a declared sibling dependency')
    return f'{len(SKILLS)} installable skill packages'


def check_versions(failures):
    readme = (ROOT / 'README.md').read_text()
    changelog = ROOT / 'CHANGELOG.md'
    history = changelog.read_text() if changelog.is_file() else ''
    status = re.search(r'^\*\*Status: (.*?)\*\*', readme, re.M)
    for name in SKILLS:
        version = (ROOT / 'skills' / name / 'VERSION')
        if not version.is_file():
            continue
        declared = version.read_text().strip()
        latest = re.search(r'^## ' + re.escape(name) + r' (\d+\.\d+\.\d+)\b', history, re.M)
        if latest is None or latest.group(1) != declared:
            failures.append(f'CHANGELOG.md: latest entry for {name} must match VERSION {declared}')
        current = re.search(re.escape(README_VERSION_LABELS[name]) + r' v(\d+\.\d+\.\d+)\b',
                            status.group(1) if status else '')
        if current is None or current.group(1) != declared:
            failures.append(f'README.md: current status for {name} must match VERSION {declared}')
    return f'{len(SKILLS)} declared package versions'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path, help='write the machine-readable result here')
    args = parser.parse_args()
    failures = []
    summary = {name: check(failures) for name, check in
               [('links', check_links), ('tables', check_tables),
                ('skills', check_skills), ('versions', check_versions)]}
    for name, scope in summary.items():
        print(f'{name}: checked {scope}')
    for failure in failures:
        print(f'FAIL {failure}')
    if args.json:
        args.json.write_text(json.dumps(dict(checked=summary, failures=failures), indent=2) + '\n')
    if failures:
        raise SystemExit(f'{len(failures)} static check failures. These are repository checks only.')
    print('Static repository checks passed. Model evaluations are separate and unaffected.')


if __name__ == '__main__':
    main()
