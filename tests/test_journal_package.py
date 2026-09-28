"""Packaged CLI portability and repository compatibility, without model calls."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class JournalPackageTests(unittest.TestCase):
    def test_copied_core_runs_without_repository_or_git(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            installed = root / 'installed/context-docs'
            shutil.copytree(ROOT/'skills/context-docs', installed, ignore=shutil.ignore_patterns('__pycache__'))
            project = root/'project'
            project.mkdir()
            payload = {'type':'decision', 'status':'proposed', 'actor':'synthetic-recorder',
                       'summary':'Fixture proposal, not approved.', 'sources':['synthetic:proposal'],
                       'revision':'unavailable (no Git)'}
            command = [sys.executable, str(installed/'scripts/event_journal.py'), '--directory', 'history/events']
            written = subprocess.run(command+['append','--session','portable'], input=json.dumps(payload),
                                     cwd=project, capture_output=True, text=True)
            self.assertEqual(written.returncode,0,written.stderr)
            read = subprocess.run(command+['read'],cwd=project,capture_output=True,text=True)
            self.assertEqual(read.returncode,0,read.stderr)
            self.assertEqual(read.stdout,written.stdout)
            self.assertFalse((project/'.git').exists())
            self.assertFalse((installed/'history').exists())

    def test_repository_entrypoint_reads_packaged_output(self):
        with tempfile.TemporaryDirectory() as temp:
            directory=Path(temp)/'events'
            payload={'type':'context_update','status':'observed','actor':'synthetic-recorder',
                     'summary':'Compatibility fixture','sources':['synthetic:test'],'revision':'unknown'}
            written=subprocess.run([sys.executable,str(ROOT/'skills/context-docs/scripts/event_journal.py'),
                '--directory',str(directory),'append','--session','compat'],input=json.dumps(payload),capture_output=True,text=True)
            read=subprocess.run([sys.executable,str(ROOT/'tools/event_journal.py'),
                '--directory',str(directory),'read'],capture_output=True,text=True)
            self.assertEqual(written.returncode,0,written.stderr)
            self.assertEqual(read.returncode,0,read.stderr)
            self.assertEqual(read.stdout,written.stdout)


if __name__=='__main__':
    unittest.main()
