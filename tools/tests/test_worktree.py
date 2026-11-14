import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from harness.worktree import prepare


class WorktreeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='worktree space ')
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / 'repo'
        self.repo.mkdir()
        self.git('init', '-b', 'main')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'user.name', 'Fixture')
        (self.repo/'AGENTS.md').write_text('fixture')
        brief = self.repo/'docs/agents/tasks/CX-1.md'
        brief.parent.mkdir(parents=True)
        brief.write_text('**Branch:** `codex/cx-1`')
        self.git('add', '.')
        self.git('commit', '-m', 'fixture')

    def git(self, *args):
        return subprocess.run(['git','-C',str(self.repo),*args], check=True, capture_output=True)

    def test_reuse_preserves_dirty_files(self):
        dest = prepare(self.repo, 'CX-1', 'main', offline=True, skip_import=True)
        (dest/'user.txt').write_text('keep')
        self.assertEqual(prepare(self.repo, 'CX-1', 'main', offline=True, skip_import=True), dest)
        self.assertEqual((dest/'user.txt').read_text(), 'keep')

    def test_reject_wrong_destination(self):
        dest = self.repo.parent/'repo-worktrees/CX-1'
        dest.mkdir(parents=True)
        (dest/'important').write_text('keep')
        with self.assertRaises(ValueError):
            prepare(self.repo, 'CX-1', 'main', offline=True, skip_import=True)
        self.assertTrue((dest/'important').exists())

    def test_reject_wrong_branch(self):
        dest = prepare(self.repo, 'CX-1', 'main', offline=True, skip_import=True)
        subprocess.run(['git','-C',str(dest),'switch','-c','codex/other'], check=True, capture_output=True)
        with self.assertRaises(ValueError):
            prepare(self.repo, 'CX-1', 'main', offline=True, skip_import=True)

    def test_invalid_id_has_no_side_effects(self):
        with self.assertRaises(ValueError):
            prepare(self.repo, '../bad', 'main', offline=True)
        self.assertFalse((self.repo.parent/'repo-worktrees').exists())

    def test_stale_branch_is_reported_without_rebasing(self):
        dest = prepare(self.repo, 'CX-1', 'main', offline=True, skip_import=True)
        (self.repo/'new.txt').write_text('new base')
        self.git('add','new.txt'); self.git('commit','-m','advance base')
        with self.assertRaises(ValueError):
            prepare(self.repo, 'CX-1', 'main', offline=True, skip_import=True)
        self.assertFalse((dest/'new.txt').exists())
