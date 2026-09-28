"""Credential-free paired-design and failure-control checks."""
import contextlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import paired


class PairedTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/'run'
        original = subprocess.check_output
        def output(command, **kwargs):
            if command == ['claude', '--version']: return 'fixture-cli'
            return original(command, **kwargs)
        with patch.object(paired.subprocess, 'check_output', side_effect=output), contextlib.redirect_stdout(io.StringIO()):
            paired.build(self.root, 'fixed-model')
        self.protocol = json.loads((self.root/'protocol.json').read_text())

    def test_pairs_have_identical_requests_and_nonpackage_inputs(self):
        self.assertEqual(len(self.protocol['sessions']), 8)
        for case in self.protocol['cases']:
            sessions = [s for s in self.protocol['sessions'] if s['case']==case['id']]
            self.assertEqual([s['arm'] for s in sessions], ['ordinary','skills','skills','ordinary'])
            trees = [{n:h for n,h in s['initial_tree'].items() if not n.startswith('.claude/')} for s in sessions]
            self.assertTrue(all(t==trees[0] for t in trees))

    def test_actual_fixture_has_null_and_list_counterexamples(self):
        project = self.root/'projects/delimited-records-ordinary-1'
        result = subprocess.check_output(['python3','records.py','samples/visits.csv'],cwd=project,text=True)
        rows = json.loads(result)
        self.assertEqual(rows[0],dict(site='north',visits='12',active='true'))
        self.assertIsNone(rows[1]['active'])
        self.assertEqual(rows[2]['surplus'],['manual','checked'])

    def test_positive_and_negative_file_controls(self):
        case = self.protocol['cases'][0]
        project = self.root/'projects/delimited-records-skills-1'
        before = paired.smoke.snapshot(project)
        (project/'README.md').write_text('# Records\n\n[Context](context.md)\n')
        (project/'context.md').write_text('# Context\n\nUse `python records.py samples/visits.csv`.\nMissing active is null; surplus is a list.\n')
        with (project/'CLAUDE.md').open('a') as f: f.write('\nMaintain [context](context.md) after project changes.\n')
        def graded(): return paired.measure(project,self.root,case,before,self.protocol['installed_files'])
        self.assertTrue(graded()['mechanical_pass'])
        original = (project/'records.py').read_text()
        (project/'records.py').write_text('changed\n')
        self.assertFalse(graded()['checks']['immutable:records.py'])
        (project/'records.py').write_text(original)
        (project/'README.md').write_text('[Missing](absent.md)\n')
        self.assertFalse(graded()['checks']['local_links_and_anchors'])
        (project/'README.md').write_text('[Context](context.md)\n')
        subprocess.run(['git','add','README.md'],cwd=project,check=True)
        self.assertFalse(graded()['checks']['no_agent_commits_or_staging'])

    def test_drift_fails_before_any_model_call(self):
        (self.root/'projects/front-door-refresh-ordinary-2/notes/state.md').write_text('drift')
        with patch.object(paired.smoke,'run_session') as call, self.assertRaisesRegex(SystemExit,'Input drift'):
            paired.run(self.root)
        call.assert_not_called()

    def test_frozen_requests_and_baseline_disable_flag_reach_runner(self):
        calls=[]
        def session(project,prompt,log,protocol):
            calls.append((prompt,protocol))
            log.write_text(json.dumps({'type':'result','is_error':False,'result':'Done.'})+'\n')
            return dict(exit_code=0,stderr='',seconds=0)
        with patch.object(paired,'CASES',[]), patch.object(paired.smoke,'run_session',side_effect=session), contextlib.redirect_stdout(io.StringIO()):
            paired.run(self.root)
        self.assertEqual(len(calls),8)
        for item,(prompt,protocol) in zip(self.protocol['sessions'],calls):
            case=next(c for c in self.protocol['cases'] if c['id']==item['case'])
            self.assertEqual(prompt,case['prompt'])
            self.assertEqual('--disable-slash-commands' in protocol['extra_args'],item['arm']=='ordinary')
            self.assertEqual(protocol['model'],'fixed-model')


if __name__ == '__main__': unittest.main()
