"""Mechanical budget controls, separate from subject behavior."""
import importlib.util
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'claude-code'))
import hook

class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);(self.root/'note.md').write_text('éé')
        self.config=dict(project=str(self.root),events=str(self.root/'events.jsonl'),writable=['code.py'],budget=dict(reads=2,bytes=8,searches=1))
    def event(self,name='Read',**payload):
        return dict(hook_event_name='PreToolUse',tool_name=name,tool_input=payload or dict(file_path=str(self.root/'note.md')))
    def test_utf8_repeated_reads_charge_and_read_cap(self):
        for _ in range(2):
            self.assertEqual(hook.handle(self.event(),self.config)['hookSpecificOutput']['permissionDecision'],'allow')
        self.assertEqual(hook.decision(self.event(),self.config)[0],'deny')
        events=[json.loads(l) for l in (self.root/'events.jsonl').read_text().splitlines()]
        self.assertEqual(sum(e['retrieval_bytes'] for e in events),8)
    def test_parallel_reservations_cannot_overrun_budget(self):
        config=self.root/'config.json';config.write_text(json.dumps(self.config))
        event=json.dumps(self.event())
        def invoke(_):
            return subprocess.run([sys.executable,str(Path(hook.__file__)),str(config)],input=event,text=True,capture_output=True,env={'PATH':'/usr/bin:/bin','PYTHONPATH':str(Path(__file__).resolve().parents[1]/'claude-code')},timeout=10)
        with ThreadPoolExecutor(max_workers=5) as pool:
            calls=list(pool.map(invoke,range(5)))
        self.assertTrue(all(c.returncode==0 for c in calls))
        decisions=[json.loads(c.stdout)['hookSpecificOutput']['permissionDecision'] for c in calls]
        self.assertEqual(decisions.count('allow'),2)
        self.assertEqual(decisions.count('deny'),3)

    def test_byte_cap_denies_before_read(self):
        self.config['budget']['bytes']=3
        self.assertEqual(hook.decision(self.event(),self.config)[0],'deny')
    def test_partial_content_search_and_outside_rejected(self):
        for e in (self.event(file_path=str(self.root/'note.md'),limit=1),self.event('Grep',pattern='.',output_mode='content'),self.event(file_path='/outside.md'),self.event('Bash',command='cat note.md')):
            self.assertEqual(hook.decision(e,self.config)[0],'deny')
    def test_filename_search_cap_and_edit_scope(self):
        prior=self.event('Glob',pattern='**/*');prior['decision']='allow'
        (self.root/'events.jsonl').write_text(json.dumps(prior)+'\n')
        self.assertEqual(hook.decision(self.event('Grep',pattern='owner'),self.config)[0],'deny')
        self.assertEqual(hook.decision(self.event('Write',file_path=str(self.root/'code.py')),self.config)[0],'allow')
        self.assertEqual(hook.decision(self.event('Write',file_path=str(self.root/'note.md')),self.config)[0],'deny')

if __name__=='__main__':unittest.main()
