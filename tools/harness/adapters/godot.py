"""Godot operations add engine-specific evidence to bounded process results."""
import os
from pathlib import Path
import re
import sys
import uuid

from ..core import run, result
from ..config import inside


def failed(record: dict, reason: str) -> dict:
    record.update(status="failed", reason=reason)
    return record


def errors(text: str) -> bool:
    return bool(re.search(r"SCRIPT ERROR|^ERROR\b|Program crashed|CAPTURE_FAIL", text, re.M))


def check(argv: list[str], root: Path, artifacts: Path, *, timeout=600,
          log_cap=50_000_000) -> dict:
    binary = os.environ.get("GODOT", "godot")
    op, *args = argv
    if op not in ("import", "test", "capture"):
        raise ValueError("unknown Godot operation")
    if op == "import" and args:
        raise ValueError("import takes no arguments")
    version_file = root / "tools/ci/godot-version.txt"
    version = run([binary, "--version"], root, artifacts / "version.log", timeout=timeout, log_cap=log_cap)
    if version["status"] != "passed":
        return version
    actual = Path(version["log"]).read_text(errors="replace").strip()
    if not version_file.is_file() or not actual.startswith(version_file.read_text().strip() + ".stable."):
        return failed(version, "engine_version_mismatch")
    tries = int(os.environ.get("IMPORT_TRIES", "3"))
    if tries < 1 or tries > 10:
        raise ValueError("IMPORT_TRIES must be between 1 and 10")
    for attempt in range(tries):
        imported = run([binary, "--headless", "--path", ".", "--import"], root,
                       artifacts / f"import-{attempt + 1}.log", timeout=timeout, log_cap=log_cap)
        text = Path(imported["log"]).read_text(errors="replace")
        missing = []
        for source in root.rglob("*.import"):
            if ".godot" in source.relative_to(root).parts or not Path(str(source)[:-7]).exists():
                continue
            for line in source.read_text(errors="replace").splitlines():
                if line.startswith("dest_files="):
                    for name in re.findall(r'"res://([^"\n]+)"', line):
                        if not inside(root, name).exists():
                            missing.append(name)
        if imported["status"] == "passed" and not errors(text) and not missing:
            break
        if imported["status"] == "passed":
            failed(imported, "import_errors" if errors(text) else "missing_imports")
        # Retry a crashed/partial import without deleting project caches or user data.
        if imported["reason"] in ("timeout", "log_limit", "interrupted"):
            return imported
    else:
        return imported
    if op == "import":
        return imported
    if op == "capture":
        if sys.platform != "darwin" and not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
            return result("skipped", "display_unavailable", artifacts / "capture.log")
        scene = args[0] if args else "main"
        output = inside(root, args[1] if len(args) > 1 else "shots/main.png")
        wait = args[2] if len(args) > 2 else "1.5"
        if scene != "main":
            if not scene.startswith("res://"):
                raise ValueError("scene must be main or res:// path")
            inside(root, scene[6:])
        output.parent.mkdir(parents=True, exist_ok=True)
        fresh = output.with_name(output.stem + "-" + uuid.uuid4().hex + ".png")
        record = run([binary, "--path", ".", "--resolution", os.environ.get("SHOT_RES", "1280x720"),
                      "-s", "tools/godot/capture.gd", "--", scene, str(fresh), wait],
                     root, artifacts / "capture.log", timeout=timeout, log_cap=log_cap)
        text = Path(record["log"]).read_text(errors="replace")
        # Godot can emit resource-leak shutdown diagnostics after successful capture.
        if record["status"] == "passed" and (errors(text.split("CAPTURE_OK")[0]) or "CAPTURE_OK" not in text or not fresh.is_file()):
            failed(record, "capture_evidence_missing_or_errors")
        if record["status"] == "passed":
            fresh.replace(output)
            record["artifacts"] = [str(output)]
        elif fresh.exists():
            fresh.unlink()
        return record
    record = run([binary, "--headless", "--path", ".", "-s", "tests/run_tests.gd", "--", *args],
                 root, artifacts / "suite.log", timeout=timeout, log_cap=log_cap)
    text = Path(record["log"]).read_text(errors="replace")
    summaries = re.findall(r"^(\d+)/(\d+) passed$", text, re.M)
    if summaries:
        passed, total = map(int, summaries[-1])
        record["tests"] = {"passed": passed, "total": total}
    if record["status"] == "passed":
        if errors(text):
            failed(record, "script_errors")
        elif len(summaries) != 1:
            failed(record, "invalid_summary")
        elif total == 0 or passed != total:
            failed(record, "test_failures_or_empty")
    return record
