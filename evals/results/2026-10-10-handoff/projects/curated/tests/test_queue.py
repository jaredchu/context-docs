import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from queue_cli import format_records, main

ROWS = '{"id": "c"}\n{"id": "a"}\n{"id": "b"}\n'

class QueueTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(format_records([]), "")

    def test_input_order(self):
        self.assertEqual(format_records([{"id": "b"}, {"id": "a"}]), '{"id": "b"}\n{"id": "a"}\n')

    def test_limit_keeps_input_order(self):
        records = [{"id": "c"}, {"id": "a"}, {"id": "b"}]
        self.assertEqual(format_records(records, 2), '{"id": "c"}\n{"id": "a"}\n')

    def test_limit_zero(self):
        self.assertEqual(format_records([{"id": "a"}], 0), "")

    def test_limit_excess(self):
        self.assertEqual(format_records([{"id": "b"}, {"id": "a"}], 5), '{"id": "b"}\n{"id": "a"}\n')

    def test_limit_does_not_mutate_records(self):
        records = [{"id": "b"}, {"id": "a"}]
        format_records(records, 1)
        self.assertEqual(records, [{"id": "b"}, {"id": "a"}])

class MainTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "queue.jsonl"
        self.path.write_text(ROWS)

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            main([str(self.path), *args])
        return out.getvalue()

    def test_default_output_unchanged(self):
        self.assertEqual(self.run_main(), ROWS)

    def test_limit_flag(self):
        self.assertEqual(self.run_main("--limit", "2"), '{"id": "c"}\n{"id": "a"}\n')

    def test_limit_zero_flag(self):
        self.assertEqual(self.run_main("--limit", "0"), "")

    def test_limit_excess_flag(self):
        self.assertEqual(self.run_main("--limit", "10"), ROWS)

    def test_source_file_untouched(self):
        self.run_main("--limit", "1")
        self.assertEqual(self.path.read_text(), ROWS)

    def test_negative_limit_exits_2(self):
        for value in ("-1", "abc"):
            with self.subTest(value=value):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as ctx:
                        self.run_main("--limit", value)
                self.assertEqual(ctx.exception.code, 2)

if __name__ == "__main__":
    unittest.main()
