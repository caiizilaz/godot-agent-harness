"""Generic commands preserve the process exit code as the source of truth."""
from pathlib import Path
from ..core import run


def check(argv: list[str], root: Path, artifacts: Path, **limits) -> dict:
    return run(argv, root, artifacts / "command.log", **limits)
