"""Exercise adoption and aggregate gates through the public executable."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from harness import config
from harness.adapters import godot

CLI = Path(__file__).resolve().parents[1] / 'harness.py'


class CLITests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.config = self.root/'harness.json'
        self.config.write_text(json.dumps({'schema_version':1,'checks':[dict(id='fixture',adapter='command',
          argv=[sys.executable,'-c',"from pathlib import Path; Path('executed').touch()"],cwd='.',required=True,timeout=5,log_cap=10000)]}))

    def cli(self, *args):
        return subprocess.run([sys.executable,str(CLI),'--config',str(self.config),*args],capture_output=True,text=True,timeout=10)

    def test_inspect_and_doctor_are_read_only(self):
        for op in ['inspect','doctor']:
            self.assertEqual(self.cli(op).returncode,0)
            self.assertFalse((self.root/'executed').exists())

    def test_adopt_then_rollback_preserves_project(self):
        original=self.root/'original.txt'
        original.write_text('user-owned project')
        self.assertEqual(self.cli('check').returncode,0)
        self.assertTrue((self.root/'executed').exists())
        self.config.unlink()
        self.assertEqual(original.read_text(),'user-owned project')

    def test_unknown_check_is_error(self):
        self.assertEqual(self.cli('check','typo').returncode,2)
        self.assertFalse((self.root/'executed').exists())

    def test_unknown_schema_is_error(self):
        data=json.loads(self.config.read_text());data['schema_version']=2
        self.config.write_text(json.dumps(data))
        self.assertEqual(self.cli('check').returncode,2)

    def test_nonzero_generic_command_fails(self):
        data=json.loads(self.config.read_text());data['checks'][0]['argv']=[sys.executable,'-c','raise SystemExit(7)']
        self.config.write_text(json.dumps(data))
        self.assertEqual(self.cli('check').returncode,1)

    def test_missing_required_tool_fails_doctor(self):
        data=json.loads(self.config.read_text());data['checks'][0]['argv']=['missing-space8-tool']
        self.config.write_text(json.dumps(data))
        self.assertEqual(self.cli('doctor').returncode,1)

    def test_required_skip_fails_optional_skip_passes(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location('harness_cli',CLI)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        record=dict(schema_version=1,status='skipped',exit_code=None,reason='display_unavailable',duration_seconds=0,log='none',artifacts=[],tests=None)
        data=json.loads(self.config.read_text());data['checks'][0]['adapter']='godot';data['checks'][0]['argv']=['capture']
        for required,expected in [(True,1),(False,0)]:
            data['checks'][0]['required']=required;self.config.write_text(json.dumps(data))
            with patch.object(sys,'argv',[str(CLI),'--config',str(self.config),'check']), patch.object(module.godot,'check',return_value=record):
                self.assertEqual(module.main(),expected)
