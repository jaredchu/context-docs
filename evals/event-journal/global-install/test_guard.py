import tempfile
import unittest
from pathlib import Path
import guard


class GlobalGuardTests(unittest.TestCase):
    def test_global_read_project_write_and_read_only_boundaries(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve(); project=root/'project'; project.mkdir()
            skills=root/'skills'; skills.mkdir(); helper=skills/'event_journal.py'
            cfg={'project':str(project),'skill_roots':[str(skills)],'helper':str(helper),
                 'python':'python3','read_only':False,'immutable':['AGENTS.md']}
            def event(tool,path): return {'tool_name':tool,'tool_input':{'file_path':str(path)}}
            self.assertTrue(guard.decision(event('Read',helper),cfg))
            self.assertFalse(guard.decision(event('Write',helper),cfg))
            self.assertFalse(guard.decision(event('Read',root/'private'),cfg))
            self.assertFalse(guard.decision(event('Write',project/'AGENTS.md'),cfg))
            command=f'python3 {helper} --directory .context/events append --session test --input payload.json'
            self.assertTrue(guard.guard.shell_allowed(command,cfg))
            cfg['read_only']=True
            self.assertFalse(guard.guard.shell_allowed(command,cfg))
