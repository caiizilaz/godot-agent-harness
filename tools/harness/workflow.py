"""Validate optional team manifests without reading the rest of an agent's board."""
import json
from pathlib import Path
import sys
from harness.config import inside


def validate(root: Path, tasks: list[dict]) -> None:
    by_id = {}
    owners = {}
    for task in tasks:
        if set(task) != {'id','state','owns','depends'} or task['id'] in by_id:
            raise ValueError('invalid task keys or duplicate id')
        if task['state'] not in ('planned','ready','active','complete'):
            raise ValueError('invalid state')
        if not isinstance(task['owns'], list) or not isinstance(task['depends'], list):
            raise ValueError('owns and depends must be lists')
        by_id[task['id']] = task
        for value in task['owns']:
            path = inside(root, value)
            if task['state'] != 'complete':
                for previous, owner in owners.items():
                    if path == previous or path.is_relative_to(previous) or previous.is_relative_to(path):
                        raise ValueError(f'ownership overlap: {owner} / {task["id"]}')
                owners[path] = task['id']
    visited, active = set(), set()
    def visit(task_id):
        if task_id not in by_id:
            raise ValueError('missing dependency: ' + task_id)
        if task_id in active:
            raise ValueError('dependency cycle')
        if task_id in visited:
            return
        active.add(task_id)
        task = by_id[task_id]
        for dep in task['depends']:
            visit(dep)
            if task['state'] in ('ready','active') and by_id[dep]['state'] != 'complete':
                raise ValueError('unfinished dependency for ' + task_id)
        active.remove(task_id)
        visited.add(task_id)
    for task_id in by_id:
        visit(task_id)


if __name__ == '__main__':
    try:
        path = Path(sys.argv[1]).resolve()
        validate(path.parent, json.loads(path.read_text()))
        print('workflow: ownership and dependencies valid')
    except (ValueError, OSError, IndexError, TypeError) as error:
        print('FAIL ' + str(error), file=sys.stderr)
        sys.exit(1)
