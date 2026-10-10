"""Fresh freeze setup and control integrity without model execution."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

SPEC=importlib.util.spec_from_file_location('handoff_large_study',Path(__file__).with_name('study.py'))
study=importlib.util.module_from_spec(SPEC)
session=types.ModuleType('session')
session.launch=Mock(side_effect=AssertionError('Tests must not launch a model.'))
with patch.dict(sys.modules,{'session':session}):
    SPEC.loader.exec_module(study)


class FreezeTests(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root=Path(temporary.name)
        fixture=dict(common={'README.md':'# Synthetic project\n','code.py':'pass\n'},
                     curated={'docs/project-context.md':'# Context\n'},task='Update code.',
                     criteria={'task':'Make the scoped update.'},writable=['code.py'])
        study.dump(self.root/'fixture.json',fixture)
        study.dump(self.root/'preflight.json',{'accepted':True})
        (self.root/'verify.py').write_text('# Synthetic verifier\n')
        self.version=patch.object(study.subprocess,'check_output',return_value='frozen-cli\n')
        self.version.start()
        self.addCleanup(self.version.stop)

    def freeze(self):
        with contextlib.redirect_stdout(io.StringIO()):
            study.freeze(self.root)
        return json.loads((self.root/'protocol.json').read_text())

    def assert_controls_work(self):
        protocol=self.freeze()
        self.assertEqual(set(protocol['control_hashes']),set(study.CONTROL_FILES))
        for name,source in study.CONTROL_SCRIPTS.items():
            self.assertEqual((self.root/'control'/name).read_bytes(),source.read_bytes())
            self.assertEqual(protocol['control_hashes'][name],study.sha(source))
        self.assertEqual(study.validate(self.root),protocol)
        settings=json.loads((self.root/'control/scattered.settings.json').read_text())
        command=settings['hooks']['PreToolUse'][0]['hooks'][0]['command']
        argv=shlex.split(command.removesuffix(' || exit 2'))
        project=self.root/'projects/scattered'
        event=dict(hook_event_name='PreToolUse',tool_name='Read',
                   tool_input={'file_path':str(project/'code.py')})
        result=subprocess.run(argv,input=json.dumps(event),capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout)['hookSpecificOutput']['permissionDecision'],'allow')

    def test_freeze_creates_control_directory_and_executable_hooks(self):
        self.assertFalse((self.root/'control').exists())
        self.assert_controls_work()

    def test_freeze_populates_an_existing_empty_control_directory(self):
        (self.root/'control').mkdir()
        self.assert_controls_work()

    def test_freeze_preserves_matching_controls_and_other_preparation(self):
        study.initialize_controls(self.root)
        original={name:(self.root/'control'/name).stat().st_mtime_ns for name in study.CONTROL_SCRIPTS}
        note=self.root/'control/author-note.txt'
        note.write_text('Keep preparation evidence.\n')
        self.assert_controls_work()
        self.assertEqual(note.read_text(),'Keep preparation evidence.\n')
        self.assertEqual(original,{name:(self.root/'control'/name).stat().st_mtime_ns for name in study.CONTROL_SCRIPTS})

    def test_freeze_rejects_conflicting_controls_without_overwriting(self):
        control=self.root/'control'
        control.mkdir()
        script=control/'hook.py'
        script.write_text('# Preserve this different control.\n')
        with self.assertRaisesRegex(ValueError,'Existing control script differs'):
            self.freeze()
        self.assertEqual(script.read_text(),'# Preserve this different control.\n')
        self.assertFalse((self.root/'protocol.json').exists())
        self.assertFalse((self.root/'projects').exists())

    def test_validate_rejects_missing_tampered_or_unlisted_control_scripts(self):
        original=self.freeze()
        for name in study.CONTROL_SCRIPTS:
            with self.subTest(script=name):
                script=self.root/'control'/name
                body=script.read_bytes()
                script.unlink()
                with self.assertRaises(FileNotFoundError):
                    study.validate(self.root)
                script.write_bytes(body+b'\n# changed\n')
                with self.assertRaises(AssertionError):
                    study.validate(self.root)
                script.write_bytes(body)
                protocol=json.loads(json.dumps(original))
                del protocol['control_hashes'][name]
                study.dump(self.root/'protocol.json',protocol)
                (self.root/'protocol.sha256').write_text(study.sha(self.root/'protocol.json')+'\n')
                with self.assertRaisesRegex(AssertionError,'Missing frozen controls'):
                    study.validate(self.root)
                study.dump(self.root/'protocol.json',original)
                (self.root/'protocol.sha256').write_text(study.sha(self.root/'protocol.json')+'\n')
        self.assertEqual(study.validate(self.root),original)


if __name__=='__main__':
    unittest.main()
