import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from harness.config import load, inside


class ConfigTests(unittest.TestCase):
    def test_invalid_config_rejected_before_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "harness.json"
            base = {"schema_version": 1, "checks": [{"id": "test", "adapter": "command",
                    "argv": ["echo", "literal"], "cwd": ".", "required": True,
                    "timeout": 1, "log_cap": 1000}]}
            path.write_text(json.dumps(base))
            self.assertEqual(load(path)[1], base)
            for key, value in (("id", "../bad"), ("cwd", ".."), ("required", "true"),
                               ("timeout", float("nan")), ("argv", "echo bad")):
                data = copy.deepcopy(base)
                data["checks"][0][key] = value
                path.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    load(path)
            (root / "outside").symlink_to(root.parent)
            with self.assertRaises(ValueError):
                inside(root, "outside/file")
