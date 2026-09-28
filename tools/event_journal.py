#!/usr/bin/env python3
"""Repository compatibility entry point; the core skill owns the implementation."""
import importlib.util
from pathlib import Path

_path = Path(__file__).resolve().parents[1] / 'skills/context-docs/scripts/event_journal.py'
_spec = importlib.util.spec_from_file_location('_context_docs_event_journal', _path)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
# Preserve the pilot's import API as well as its command line entry point.
globals().update({key: value for key, value in vars(_module).items() if not key.startswith('_')})

if __name__ == '__main__':
    raise SystemExit(_module.main())
