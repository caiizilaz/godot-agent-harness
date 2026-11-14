from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from harness.workflow import validate


class WorkflowTests(unittest.TestCase):
    def task(self, id, owns, depends=(), state='planned'):
        return dict(id=id,owns=owns,depends=list(depends),state=state)

    def test_overlap_and_dependency_rules(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            validate(root,[self.task('a',['a'],state='complete'),self.task('b',['b'],['a'],'ready')])
            for tasks in ([self.task('a',['a']),self.task('b',['a/child'])],
                          [self.task('a',['a'],['b']),self.task('b',['b'],['a'])],
                          [self.task('a',['a'],['missing'])],
                          [self.task('a',['a']),self.task('b',['b'],['a'],'ready')]):
                with self.assertRaises(ValueError):
                    validate(root,tasks)
