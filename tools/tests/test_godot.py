"""Reproduce false greens without depending on the installed editor."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from harness.adapters.godot import check


class GodotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "tools/ci").mkdir(parents=True)
        (self.root / "tools/ci/godot-version.txt").write_text("4.7.2\n")
        self.fake = self.root / "fake"
        self.fake.write_text('#!' + sys.executable + '''
import os,sys
if '--version' in sys.argv:
 print(os.environ.get('FAKE_VERSION','4.7.2.stable.fake')); sys.exit(0)
if '--import' in sys.argv:
 sys.exit(int(os.environ.get('IMPORT_EXIT','0')))
print(os.environ.get('FAKE_SUMMARY','1/1 passed'))
sys.exit(int(os.environ.get('SUITE_EXIT','0')))
''')
        self.fake.chmod(0o755)
        self.env = patch.dict(os.environ, {"GODOT": str(self.fake), "IMPORT_TRIES": "1"})
        self.env.start()
        self.addCleanup(self.env.stop)

    def run_case(self, env=None, op="test"):
        with patch.dict(os.environ, env or {}):
            return check([op], self.root, self.root / "logs", timeout=5)

    def test_happy_path(self):
        self.assertEqual(self.run_case()["tests"], {"passed": 1, "total": 1})

    def test_import_nonzero(self):
        record = self.run_case({"IMPORT_EXIT": "23"}, "import")
        self.assertEqual(record["exit_code"], 23)
        self.assertEqual(record["status"], "failed")

    def test_exit_after_summary(self):
        self.assertEqual(self.run_case({"SUITE_EXIT": "42"})["status"], "failed")

    def test_error_after_summary(self):
        self.assertEqual(self.run_case({"FAKE_SUMMARY": "1/1 passed\nSCRIPT ERROR: bad"})["status"], "failed")

    def test_empty_missing_failed_duplicate_summary(self):
        for summary in ("0/0 passed", "hello", "0/1 passed", "1/1 passed\n1/1 passed"):
            self.assertEqual(self.run_case({"FAKE_SUMMARY": summary})["status"], "failed")

    def test_wrong_patch_version(self):
        self.assertEqual(self.run_case({"FAKE_VERSION": "4.7.1.stable.fake"})["reason"], "engine_version_mismatch")

    def test_capture_cannot_reuse_old_file(self):
        target = self.root / "shots/main.png"
        target.parent.mkdir()
        target.write_bytes(b"old")
        with patch.dict(os.environ, {"DISPLAY": ":fake"}):
            record = check(["capture"], self.root, self.root / "logs", timeout=5)
        self.assertEqual(record["status"], "failed")
        self.assertEqual(target.read_bytes(), b"old")

    def test_missing_import_output(self):
        (self.root / "asset.png").touch()
        (self.root / "asset.png.import").write_text('dest_files=["res://.godot/imported/missing"]')
        self.assertEqual(self.run_case()["reason"], "missing_imports")

    def test_import_only_does_not_run_suite(self):
        record = self.run_case({'SUITE_EXIT':'42'}, 'import')
        self.assertEqual(record['status'], 'passed')
        self.assertFalse((self.root/'logs/suite.log').exists())

    def test_capture_without_display_is_explicitly_skipped(self):
        with patch('harness.adapters.godot.sys.platform','linux'), patch.dict(os.environ,{'DISPLAY':'','WAYLAND_DISPLAY':''}):
            record=check(['capture'],self.root,self.root/'logs',timeout=5)
        self.assertEqual(record['status'],'skipped')
        self.assertEqual(record['reason'],'display_unavailable')
