import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC=importlib.util.spec_from_file_location('integration_guard',Path(__file__).with_name('guard.py'))
guard=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(guard)


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve()
        self.config={'project':str(self.root),'python':'/usr/bin/python3','helper':'.claude/skills/context-docs/scripts/event_journal.py',
                     'read_only':False,'immutable':['checks/probe.py','settings.json']}
        self.cmd='python3 .claude/skills/context-docs/scripts/event_journal.py --directory history/events append --session trial --input event.json'

    def test_direct_helper_and_probe(self):
        self.assertTrue(guard.shell_allowed(self.cmd,self.config))
        self.assertTrue(guard.shell_allowed('python3 checks/probe.py',self.config))
        self.assertTrue(guard.shell_allowed('git status --short',self.config))

    def test_shell_and_outside_paths_rejected(self):
        for command in (self.cmd+'; pwd',self.cmd+' > out',self.cmd.replace('event.json','/tmp/event.json'),
                        self.cmd.replace('history/events','../outside'), 'python3 -c "print(1)"',
                        'git diff --output=/tmp/out',self.cmd.replace('event.json','$(whoami).json')):
            self.assertFalse(guard.shell_allowed(command,self.config),command)

    def test_audit_rejects_append_probe_and_file_writes(self):
        self.config['read_only']=True
        self.assertFalse(guard.shell_allowed(self.cmd,self.config))
        self.assertFalse(guard.shell_allowed('python3 checks/probe.py',self.config))
        self.assertTrue(guard.shell_allowed('python3 .claude/skills/context-docs/scripts/event_journal.py --directory history/events read',self.config))
        self.assertFalse(guard.decision({'tool_name':'Write','tool_input':{'file_path':'notes/context.md'}},self.config))

    def test_packages_sources_and_jsonl_immutable(self):
        for path in ('.claude/skills/context-docs/SKILL.md','checks/probe.py','settings.json','history/events/record.jsonl','/tmp/out.md'):
            self.assertFalse(guard.decision({'tool_name':'Write','tool_input':{'file_path':path}},self.config),path)
        self.assertTrue(guard.decision({'tool_name':'Write','tool_input':{'file_path':'event.json'}},self.config))
        self.assertTrue(guard.decision({'tool_name':'Edit','tool_input':{'file_path':'CLAUDE.md'}},self.config))

    def test_symlink_escape_rejected(self):
        (self.root/'outside').symlink_to(self.root.parent,target_is_directory=True)
        self.assertFalse(guard.shell_allowed(self.cmd.replace('history/events','outside/events'),self.config))
        self.assertFalse(guard.decision({'tool_name':'Read','tool_input':{'file_path':'outside/private.md'}},self.config))


if __name__=='__main__':
    unittest.main()
