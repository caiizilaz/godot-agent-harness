"""Strict v1 configuration with project-relative, symlink-aware paths."""
import json
import math
from pathlib import Path


def inside(root: Path, value: str) -> Path:
    """Disallow absolute paths, traversal and symlinks outside the selected project."""
    if not isinstance(value, str) or Path(value).is_absolute() or ".." in Path(value).parts:
        raise ValueError("path must be project-relative without traversal")
    resolved = (root / value).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError("path escapes project root")
    return resolved


def load(path: Path) -> tuple[Path, dict]:
    """Inspect config without executing configured commands or importing plugins."""
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or set(data) != {"schema_version", "checks"} or type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("expected schema_version 1 and checks")
    if not isinstance(data["checks"], list) or not data["checks"]:
        raise ValueError("checks must be a nonempty list")
    root = path.resolve().parent
    ids = set()
    for check in data["checks"]:
        required = {"id", "adapter", "argv", "cwd", "required", "timeout", "log_cap"}
        if not isinstance(check, dict) or set(check) != required:
            raise ValueError("check keys must be " + ", ".join(sorted(required)))
        import re
        if not isinstance(check["id"], str) or not re.fullmatch(r"[a-z][a-z0-9-]*", check["id"]) or check["id"] in ids:
            raise ValueError("invalid or duplicate check id")
        ids.add(check["id"])
        if check["adapter"] not in ("command", "godot") or type(check["required"]) is not bool:
            raise ValueError("invalid adapter/required")
        if not isinstance(check["argv"], list) or not check["argv"] or not all(isinstance(a, str) and '\0' not in a for a in check["argv"]):
            raise ValueError("argv must be a nonempty string array")
        if type(check["timeout"]) not in (int, float) or not math.isfinite(check["timeout"]) or check["timeout"] <= 0:
            raise ValueError("timeout must be finite and positive")
        if type(check["log_cap"]) is not int or check["log_cap"] <= 0:
            raise ValueError("log_cap must be a positive integer")
        if not inside(root, check["cwd"]).is_dir():
            raise ValueError("cwd does not exist")
        if check["adapter"] == "godot" and check["argv"][0] not in ("test", "import", "capture"):
            raise ValueError("unknown Godot operation")
    return root, data
