"""Additive Markdown scope checks. Semantics are reviewed separately."""
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit


def snapshot(root):
    return {str(p.relative_to(root)): p.read_bytes().decode('utf-8') for p in sorted(root.rglob('*'))
            if p.is_file() and '.git' not in p.relative_to(root).parts}


def grade(before, root):
    files = snapshot(root)
    additions = {p: s for p, s in files.items() if p not in before}
    changed = [p for p, s in before.items() if files.get(p) != s]
    errors = []
    for p, body in additions.items():
        for dest in re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', body):
            url = urlsplit(dest.strip('<>'))
            if url.scheme or url.netloc or not url.path:
                continue
            parts = []
            for part in (PurePosixPath(p).parent / unquote(url.path)).parts:
                if part == '..':
                    if parts: parts.pop()
                    else: parts.append('..')
                elif part != '.': parts.append(part)
            if '/'.join(parts) not in files:
                errors.append({'file': p, 'target': dest})
    checks = dict(upstream_unchanged=not changed,
                  added_markdown=bool(additions) and all(p.endswith('.md') and s.strip() for p, s in additions.items()),
                  local_link_paths=not errors)
    if (root / '.git').exists():
        checks['git_unchanged'] = (subprocess.check_output(['git', 'rev-list', '--count', 'HEAD'], cwd=root, text=True).strip() == '1'
            and not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=root, text=True).strip())
    return dict(checks=checks, mechanical_pass=all(checks.values()), files=files,
                additions=additions, changed_upstream=changed, link_errors=errors)


if __name__ == '__main__':
    spec = json.loads(Path(sys.argv[1]).read_text())
    before = json.loads(Path(spec['input_snapshot']).read_text())
    result = grade(before, Path('/workspace'))
    logs = Path('/logs/verifier'); logs.mkdir(parents=True, exist_ok=True)
    (logs/'observed.json').write_text(json.dumps(result, indent=2)+'\n')
    (logs/'reward.json').write_text(json.dumps({'mechanical': int(result['mechanical_pass'])})+'\n')
    print(json.dumps({'checks': result['checks'], 'semantic_review': 'required'}))
