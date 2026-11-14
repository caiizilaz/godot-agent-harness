"""Create/reuse only the checkout declared by a task brief; never overwrite work."""
import argparse
from pathlib import Path
import re
import subprocess
import sys


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


def prepare(repo: Path, task: str, base: str, *, offline=False, skip_import=False) -> Path:
    if not re.fullmatch(r'[A-Z][A-Z0-9]*-[A-Z0-9]+', task):
        raise ValueError('invalid task id')
    repo = Path(git(repo, 'rev-parse', '--show-toplevel')).resolve()
    brief = repo / 'docs/agents/tasks' / (task + '.md')
    if not brief.is_file():
        raise ValueError('missing brief: ' + str(brief))
    branches = re.findall(r'\*\*Branch:\*\*\s*`([^`]+)`', brief.read_text())
    if len(branches) != 1:
        raise ValueError('brief must declare exactly one **Branch:** `name`')
    branch = branches[0]
    if not branch.startswith(('agent/', 'codex/')):
        raise ValueError('task branch must use agent/ or codex/')
    subprocess.run(['git', 'check-ref-format', '--branch', branch], check=True, stdout=subprocess.DEVNULL)
    dest = repo.parent / (repo.name + '-worktrees') / task
    if dest.exists():
        if dest.is_symlink():
            raise ValueError('worktree destination must not be a symlink')
        try:
            same_root = Path(git(dest, 'rev-parse', '--show-toplevel')).resolve() == dest.resolve()
            same_common = Path(git(dest, 'rev-parse', '--path-format=absolute', '--git-common-dir')).resolve() == Path(git(repo, 'rev-parse', '--path-format=absolute', '--git-common-dir')).resolve()
            same_branch = git(dest, 'branch', '--show-current') == branch
        except subprocess.CalledProcessError as error:
            raise ValueError('existing destination is not the expected worktree') from error
        if not (same_root and same_common and same_branch):
            raise ValueError('existing destination has wrong repository or branch')
        if base == 'origin/main' and 'origin' not in git(repo, 'remote').splitlines():
            base = 'main'
        status = subprocess.run(['git','-C',str(repo),'merge-base','--is-ancestor',base,branch], capture_output=True)
        if status.returncode != 0:
            raise ValueError('existing task branch does not contain the requested base; ask integrator to update it')
        # Reuse preserves all dirty files; import is safe to retry after interrupted setup.
    else:
        if not offline and 'origin' in git(repo, 'remote').splitlines():
            subprocess.run(['git', '-C', str(repo), 'fetch', '-q', 'origin'], check=True)
        if base == 'origin/main' and 'origin' not in git(repo, 'remote').splitlines():
            base = 'main'
        git(repo, 'cat-file', '-e', base + ':AGENTS.md')
        existing = subprocess.run(['git','-C',str(repo),'show-ref','--verify','--quiet','refs/heads/'+branch]).returncode == 0
        cmd = ['git', '-C', str(repo), 'worktree', 'add']
        if existing:
            cmd += [str(dest), branch]
        else:
            cmd += ['-b', branch, str(dest), base]
        subprocess.run(cmd, check=True)
    if not skip_import:
        check = dest / 'tools/test.sh'
        if check.exists():
            subprocess.run(['bash', str(check), '--import-only'], cwd=dest, check=True)
    return dest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('task')
    parser.add_argument('base', nargs='?', default='origin/main')
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--skip-import', action='store_true')
    args = parser.parse_args()
    try:
        print(prepare(Path.cwd(), args.task, args.base, offline=args.offline, skip_import=args.skip_import))
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print('FAIL ' + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
