"""Mechanical checks only. Semantic rubric review is separate from these rewards."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


def snapshot(root):
    return {str(p.relative_to(root)): p.read_text() for p in sorted(root.rglob('*'))
            if p.is_file() and '.git' not in p.relative_to(root).parts}


def anchors(text):
    result, counts = set(), {}
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        n = counts.get(slug, 0)
        result.add(slug + (f'-{n}' if n else ''))
        counts[slug] = n + 1
    result.update(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', text))
    return result


def link_errors(files):
    errors = []
    for name, body in files.items():
        if not name.endswith('.md'):
            continue
        # Fixtures use inline Markdown links and ordinary heading anchors.
        for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)', body):
            if re.match(r'[a-zA-Z]+:', dest):
                continue
            part, _, anchor = unquote(dest).partition('#')
            import posixpath
            target = posixpath.normpath(str(Path(name).parent / part)) if part else name
            if target not in files:
                errors.append(f'{name}: missing {dest}')
            elif anchor and anchor not in anchors(files[target]):
                errors.append(f'{name}: missing anchor {dest}')
    return errors


def grade(spec, root, output, before=None):
    before = spec['before'] if before is None else before
    files = snapshot(root)
    docs = {p: s for p, s in files.items() if p.endswith('.md')}
    text = '\n'.join(docs.values())
    checks = {}
    checks['input_files_retained'] = all(p in files for p in before)
    checks['non_document_inputs_unchanged'] = all(
        files.get(p) == body for p, body in before.items() if not p.endswith('.md'))
    checks['only_document_files_created'] = all(p.endswith('.md') for p in files if p not in before)
    for p in spec['immutable']:
        checks['immutable:' + p] = files.get(p) == spec['before'][p]
    for token in spec['protected']:
        checks['preserved:' + hashlib.sha256(token.encode()).hexdigest()[:10]] = token in text
    errors = link_errors(files)
    checks['local_links_and_anchors'] = not errors
    if spec['id'] == 'links-and-fences':
        checks['external_anchor_preserved'] = 'restore-steps' in anchors(files.get('docs/runbook.md', ''))
    if spec['id'] == 'audit-only':
        checks['project_byte_identical'] = files == before
        checks['audit_report_exists'] = (output / 'audit.md').is_file() and bool((output / 'audit.md').read_text().strip())
    elif not spec.get('allow_noop'):
        checks['documentation_changed'] = any(files.get(p) != s for p, s in before.items() if p.endswith('.md')) or any(p not in before for p in docs)
    if (root / '.git').exists():
        count = subprocess.check_output(['git', 'rev-list', '--count', 'HEAD'], cwd=root, text=True).strip()
        staged = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=root, text=True)
        checks['no_agent_commits_or_staging'] = count == '1' and not staged.strip()
    return dict(checks=checks, mechanical_pass=all(checks.values()), link_errors=errors,
                documents=docs, audit=(output / 'audit.md').read_text() if (output / 'audit.md').exists() else None,
                word_count=sum(len(s.split()) for s in docs.values()),
                entry_words=len(docs.get(spec['entry'], '').split()),
                before_documents={p: s for p, s in before.items() if p.endswith('.md')},
                before_sha256=hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest(),
                before_words=sum(len(s.split()) for p, s in before.items() if p.endswith('.md')))


if __name__ == '__main__':
    spec = json.loads(Path(sys.argv[1]).read_text())
    # Missing or malformed snapshots fail verification; never fall back to oracle text.
    before = json.loads(Path(spec['input_snapshot']).read_text()) if 'input_snapshot' in spec else None
    if before is not None and (not isinstance(before, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in before.items())):
        raise ValueError('Invalid input snapshot')
    result = grade(spec, Path('/workspace'), Path('/output'), before)
    logs = Path('/logs/verifier')
    logs.mkdir(parents=True, exist_ok=True)
    (logs / 'observed.json').write_text(json.dumps(result, indent=2) + '\n')
    (logs / 'reward.json').write_text(json.dumps({'mechanical': int(result['mechanical_pass'])}) + '\n')
    print(json.dumps({'checks': result['checks'], 'semantic_review': 'required'}))
