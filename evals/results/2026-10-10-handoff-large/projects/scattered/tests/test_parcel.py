import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from parcel.cli import main
from parcel.service import execute

def run_cli(argv):
    stdout=io.StringIO()
    with contextlib.redirect_stdout(stdout):
        main(argv)
    return stdout.getvalue()

def rejected(test, argv):
    stderr=io.StringIO()
    with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
        with test.assertRaises(SystemExit) as caught:
            main(argv)
    test.assertEqual(caught.exception.code,2)
    return stderr.getvalue()

class ParcelTests(unittest.TestCase):
    def test_empty(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"input.jsonl"
            path.write_text("")
            self.assertEqual(execute(path),"")

    def test_tenant_order_and_first_duplicate(self):
        rows=[{"tenant":"red","id":"z","value":1},{"tenant":"blue","id":"z"},{"tenant":"red","id":"z","value":2},{"tenant":"red","id":"a"}]
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"input.jsonl"
            path.write_text("\n".join(json.dumps(row) for row in rows))
            actual=[json.loads(line) for line in execute(path,tenant="red").splitlines()]
            self.assertEqual(actual,[rows[0],rows[3]])

    def test_full_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"input.jsonl"
            path.write_text('{"tenant":"red","id":"ok"}\n{"id":"bad"}\n')
            with self.assertRaises(ValueError):
                execute(path,tenant="red")

class LimitTests(unittest.TestCase):
    rows=[
        {"tenant":"blue","id":"b1"},
        {"tenant":"red","id":"z","value":1},
        {"tenant":"red","id":"z","value":2},
        {"tenant":"blue","id":"b2"},
        {"tenant":"red","id":"a"},
        {"tenant":"red","id":"m"},
    ]

    def setUp(self):
        self.directory=tempfile.TemporaryDirectory()
        self.path=Path(self.directory.name)/"input.jsonl"
        self.text="\n".join(json.dumps(row) for row in self.rows)+"\n"
        self.path.write_text(self.text)

    def tearDown(self):
        self.directory.cleanup()

    def parsed(self, output):
        return [json.loads(line) for line in output.splitlines()]

    def test_limit_applies_after_tenant_filter_and_dedup(self):
        # Two red records, not two raw lines: the blue row and the duplicate z are skipped.
        actual=self.parsed(run_cli([str(self.path),"--tenant","red","--limit","2"]))
        self.assertEqual(actual,[self.rows[1],self.rows[4]])

    def test_limit_keeps_arrival_order_not_id_order(self):
        actual=self.parsed(run_cli([str(self.path),"--limit","3"]))
        self.assertEqual(actual,[self.rows[0],self.rows[1],self.rows[3]])

    def test_limit_zero_emits_nothing(self):
        self.assertEqual(run_cli([str(self.path),"--tenant","red","--limit","0"]),"")

    def test_limit_above_selection_emits_all_selected(self):
        expected=run_cli([str(self.path),"--tenant","red"])
        self.assertEqual(run_cli([str(self.path),"--tenant","red","--limit","50"]),expected)
        self.assertEqual(self.parsed(expected),[self.rows[1],self.rows[4],self.rows[5]])

    def test_without_limit_output_is_unchanged(self):
        self.assertEqual(run_cli([str(self.path)]),execute(self.path))
        self.assertEqual(execute(self.path,limit=None),execute(self.path))

    def test_limit_still_validates_later_corrupt_records(self):
        self.path.write_text(self.text+'{"id":"bad"}\n')
        for limit in ("0","1"):
            with self.subTest(limit=limit):
                rejected(self,[str(self.path),"--tenant","red","--limit",limit])
        with self.assertRaises(ValueError):
            execute(self.path,tenant="red",limit=0)

    def test_limit_still_rejects_later_invalid_json(self):
        self.path.write_text(self.text+"{not json\n")
        rejected(self,[str(self.path),"--limit","1"])

    def test_negative_and_noninteger_limits_are_argparse_errors(self):
        for value in ("-1","1.5","two",""):
            with self.subTest(value=value):
                message=rejected(self,[str(self.path),"--limit",value])
                self.assertIn("--limit",message)

    def test_input_file_untouched(self):
        run_cli([str(self.path),"--tenant","red","--limit","1"])
        self.assertEqual(self.path.read_text(),self.text)

if __name__=="__main__":
    unittest.main()
