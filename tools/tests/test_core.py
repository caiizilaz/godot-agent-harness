"""Behavioral and schema regressions for the engine-independent runner."""
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from harness.core import run


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="harness space ")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def execute(self, code, **kwargs):
        return run([sys.executable, "-c", code], self.root, self.root / "run.log", **kwargs)

    def test_result_contract(self):
        result = self.execute("print('ok')")
        self.assertEqual(set(result), {"schema_version", "status", "exit_code", "reason",
                                      "duration_seconds", "log", "artifacts", "tests"})
        self.assertEqual(result["schema_version"], 1)
        self.assertEqual(result["status"], "passed")
        self.assertIsNone(result["tests"])

    def test_nonzero_after_success_text(self):
        result = self.execute("print('1/1 passed'); raise SystemExit(42)")
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["exit_code"], 42)

    def test_silent_timeout(self):
        start = time.monotonic()
        result = self.execute("import time; time.sleep(30)", timeout=0.15)
        self.assertEqual(result["reason"], "timeout")
        self.assertLess(time.monotonic() - start, 3)

    def test_log_flood(self):
        result = self.execute("import os\nwhile True: os.write(1,b'x'*4096)", log_cap=1024)
        self.assertEqual(result["reason"], "log_limit")
        self.assertLessEqual((self.root / "run.log").stat().st_size, 1024)

    def test_descendant_holds_output(self):
        result = self.execute("import subprocess,sys; subprocess.Popen([sys.executable,'-c',"
                              "'import time; time.sleep(30)'])", timeout=0.15)
        self.assertEqual(result["reason"], "timeout")

    def test_argv_is_not_shell_code(self):
        arg = "space $(touch PWNED); `touch PWNED`"
        result = run([sys.executable, "-c", "import sys; print(sys.argv[1])", arg],
                     self.root, self.root / "run.log")
        self.assertEqual(result["status"], "passed")
        self.assertEqual((self.root / "run.log").read_text().strip(), arg)
        self.assertFalse((self.root / "PWNED").exists())

    def test_missing_binary(self):
        result = run(["nonexistent-space8-binary"], self.root, self.root / "run.log")
        self.assertEqual(result["status"], "failed")
        self.assertIsNone(result["exit_code"])

    def test_invalid_limits(self):
        for kwargs in ({"timeout": 0}, {"timeout": float("nan")}, {"log_cap": -1}):
            with self.assertRaises(ValueError):
                self.execute("pass", **kwargs)


if __name__ == "__main__":
    unittest.main()
