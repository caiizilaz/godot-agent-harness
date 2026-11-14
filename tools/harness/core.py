"""Bound subprocess lifetime and output independently of engine log wording."""
from __future__ import annotations

import math
import os
from pathlib import Path
import selectors
import signal
import subprocess
import time


def result(status: str, reason: str, log: Path, *, code: int | None = None,
           duration: float = 0.0) -> dict:
    """Keep unknown test counts explicit instead of manufacturing zero passes."""
    return {"schema_version": 1, "status": status, "exit_code": code, "reason": reason,
            "duration_seconds": duration, "log": str(log), "artifacts": [], "tests": None}


def run(argv: list[str], cwd: Path, log: Path, *, timeout: float = 600,
        log_cap: int = 50_000_000) -> dict:
    """Run literal argv on POSIX, killing the owned process group on every exit path."""
    if not argv or not all(isinstance(x, str) and '\0' not in x for x in argv):
        raise ValueError("argv must be a nonempty string array")
    if isinstance(timeout, bool) or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be finite and positive")
    if type(log_cap) is not int or log_cap <= 0:
        raise ValueError("log_cap must be a positive integer")
    if os.name != "posix":
        return result("failed", "unsupported_platform: use WSL; native Windows unverified", log)
    log.parent.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    proc = None
    reason = ""
    code = None
    written = 0
    with log.open("wb") as output, selectors.DefaultSelector() as selector:
        try:
            proc = subprocess.Popen(argv, cwd=cwd, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, start_new_session=True)
            selector.register(proc.stdout, selectors.EVENT_READ)
            while selector.get_map() or proc.poll() is None:
                remaining = timeout - (time.monotonic() - start)
                if remaining <= 0:
                    reason = "timeout"
                    break
                events = selector.select(min(remaining, 0.05))
                for key, _ in events:
                    chunk = os.read(key.fd, 65536)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    available = log_cap - written
                    output.write(chunk[:available])
                    written += min(len(chunk), available)
                    if len(chunk) > available:
                        reason = "log_limit"
                        break
                if reason:
                    break
            if not reason:
                code = proc.wait(timeout=max(0.01, timeout - (time.monotonic() - start)))
                reason = "completed" if code == 0 else "nonzero_exit"
        except KeyboardInterrupt:
            reason = "interrupted"
        except (OSError, subprocess.TimeoutExpired) as error:
            reason = "timeout" if isinstance(error, subprocess.TimeoutExpired) else "launch_error: " + str(error)
        finally:
            if proc is not None:
                # Kill even after the parent exits: background children belong to this run.
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                proc.wait()
                code = proc.returncode
                proc.stdout.close()
    return result("passed" if reason == "completed" else "failed", reason, log,
                  code=code, duration=time.monotonic() - start)
