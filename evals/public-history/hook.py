"""Evaluation-only file guard, not an OS sandbox; launched tools are restricted."""
import base64
from pathlib import Path
import guard_hook

TOOLS = ('Read', 'Write', 'Edit', 'Glob', 'Grep')


def within(path, root):
    return path == root or root in path.parents


def resulting_bytes(path, name, payload):
    """Predict exact UTF-8 write; reject ambiguous edits rather than allow blindly."""
    if name == 'Write':
        value = payload.get('content')
        if not isinstance(value, str):
            raise ValueError('Write content must be text.')
        return value.encode('utf-8')
    old, new = payload.get('old_string'), payload.get('new_string')
    if not isinstance(old, str) or not old or not isinstance(new, str):
        raise ValueError('Edit requires nonempty old_string and text new_string.')
    body = path.read_bytes()
    old, new = old.encode('utf-8'), new.encode('utf-8')
    count = body.count(old)
    if not count or (count != 1 and not payload.get('replace_all', False)):
        raise ValueError('Edit target is missing or ambiguous.')
    return body.replace(old, new, -1 if payload.get('replace_all', False) else 1)


def decision(event, config):
    name, payload = event.get('tool_name'), event.get('tool_input') or {}
    if name not in TOOLS:
        return 'deny', 'Only the five frozen file tools are exposed.'
    project, evidence = Path(config['project']).resolve(), Path(config['evidence']).resolve()
    raw = payload.get('file_path') if name in ('Read', 'Write', 'Edit') else payload.get('path', str(project))
    if not isinstance(raw, str) or not raw:
        return 'deny', 'Missing or invalid path.'
    path = Path(raw) if Path(raw).is_absolute() else project / raw
    resolved = path.resolve()
    if not any(within(resolved, root) for root in (project, evidence)):
        return 'deny', 'Outside this session project and read-only evidence.'
    for key in (('pattern',) if name == 'Glob' else ('glob',) if name == 'Grep' else ()):
        pattern = payload.get(key, '')
        if not isinstance(pattern, str) or Path(pattern).is_absolute() or '..' in pattern:
            return 'deny', 'Search file patterns must stay within their selected root.'
    if name not in ('Write', 'Edit'):
        return 'allow', 'Read within this session inputs.'
    if not within(resolved, project) or str(resolved.relative_to(project)) not in config['writable']:
        return 'deny', 'Only the named handoff and README append are writable.'
    # Permit the host's /tmp -> /private/tmp ancestor alias, but no symlink
    # beneath the project boundary, including a link back to the project root.
    if '..' in path.parts:
        return 'deny', 'Write paths must not contain parent traversal.'
    boundaries = [p for p in path.parents if p.resolve() == project]
    boundary = boundaries[-1] if boundaries else project
    inside = []
    for parent in (path, *path.parents):
        if parent == boundary: break
        inside.append(parent)
    if any(p.is_symlink() for p in inside):
        return 'deny', 'Writes through symlinks are forbidden.'
    if resolved.exists() and (not resolved.is_file() or resolved.stat().st_nlink != 1):
        return 'deny', 'Only ordinary unlinked files are writable.'
    try:
        body = resulting_bytes(resolved, name, payload)
    except (OSError, ValueError, UnicodeError) as error:
        return 'deny', str(error)
    if resolved == project / 'README.md':
        prefix = base64.b64decode(config['readme_prefix_b64'])
        if not body.startswith(prefix):
            return 'deny', 'README original bytes must remain an exact prefix on every write.'
    return 'allow', 'Exact authorized destination and preserved README prefix.'


if __name__ == '__main__':
    guard_hook.decision = decision
    guard_hook.main()
