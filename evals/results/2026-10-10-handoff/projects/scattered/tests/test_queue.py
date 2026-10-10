import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from queue_cli import format_records, main

class QueueTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(format_records([]), "")

    def test_input_order(self):
        self.assertEqual(format_records([{"id": "b"}, {"id": "a"}]), '{"id": "b"}\n{"id": "a"}\n')

class LimitTests(unittest.TestCase):
    CONTENT = '{"id": "c"}\n{"id": "a"}\n\n{"id": "b"}\n'

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.path = Path(tmp.name) / "queue.jsonl"
        self.path.write_text(self.CONTENT)

    def run_cli(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            main([str(self.path), *args])
        return out.getvalue()

    def test_default_output_unchanged(self):
        self.assertEqual(self.run_cli(), '{"id": "c"}\n{"id": "a"}\n{"id": "b"}\n')

    def test_limit_keeps_input_order(self):
        self.assertEqual(self.run_cli("--limit", "2"), '{"id": "c"}\n{"id": "a"}\n')

    def test_limit_zero_emits_nothing(self):
        self.assertEqual(self.run_cli("--limit", "0"), "")

    def test_limit_exceeding_count_emits_all(self):
        self.assertEqual(self.run_cli("--limit", "10"), '{"id": "c"}\n{"id": "a"}\n{"id": "b"}\n')

    def test_invalid_limit_exits_2(self):
        for value in ("-1", "abc"):
            with self.subTest(value=value):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as cm:
                        self.run_cli("--limit", value)
                self.assertEqual(cm.exception.code, 2)

    def test_input_file_untouched(self):
        self.run_cli("--limit", "1")
        self.assertEqual(self.path.read_text(), self.CONTENT)

if __name__ == "__main__":
    unittest.main()
