#!/usr/bin/env python3
"""Local CLI: inspect/doctor never execute project-configured commands."""
import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

from harness.config import load, inside
from harness.adapters import command, godot


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("harness.json"))
    sub = parser.add_subparsers(dest="operation", required=True)
    sub.add_parser("inspect")
    sub.add_parser("doctor")
    checks = sub.add_parser("check")
    checks.add_argument("ids", nargs="*")
    direct = sub.add_parser("godot")
    direct.add_argument("action", choices=["import", "test", "capture"])
    direct.add_argument("args", nargs="*")
    args = parser.parse_args()
    output = Path(tempfile.mkdtemp(prefix="space8-harness-"))
    try:
        if args.operation == "godot":
            records = [godot.check([args.action, *args.args], Path.cwd(), output,
                       timeout=float(os.environ.get("SUITE_TIMEOUT", "600")),
                       log_cap=int(os.environ.get("LOG_CAP_BYTES", "50000000")))]
            required = [True]
        else:
            root, data = load(args.config)
            if args.operation == "inspect":
                print(json.dumps(data, ensure_ascii=False, indent=2))
                return 0
            if args.operation == "doctor":
                ready = True
                for check in data["checks"]:
                    binary = os.environ.get("GODOT", "godot") if check["adapter"] == "godot" else check["argv"][0]
                    if "/" in binary and not Path(binary).is_absolute():
                        binary = str(inside(root, check["cwd"]) / binary)
                    found = shutil.which(binary) is not None
                    print(f"{check['id']}: {'ready' if found else 'missing'} {binary}")
                    ready = ready and (found or not check["required"])
                return 0 if ready else 1
            known = {c["id"] for c in data["checks"]}
            if set(args.ids) - known:
                raise ValueError("unknown check ids: " + ", ".join(sorted(set(args.ids) - known)))
            records, required = [], []
            for check in data["checks"]:
                if args.ids and check["id"] not in args.ids:
                    continue
                adapter = godot if check["adapter"] == "godot" else command
                records.append(adapter.check(check["argv"], inside(root, check["cwd"]),
                               output / check["id"], timeout=check["timeout"], log_cap=check["log_cap"]))
                required.append(check["required"])
                print(f"{check['id']}: {records[-1]['status']} ({records[-1]['reason']})")
        for record in records:
            if record["tests"]:
                print(f"{record['tests']['passed']}/{record['tests']['total']} passed")
            print(f"{record['status']}: {record['reason']}; log: {record['log']}")
        (output / "results.json").write_text(json.dumps(records, indent=2) + "\n")
        print(f"Evidence: {output / 'results.json'}")
        return int(any(r["status"] == "failed" or (needed and r["status"] != "passed")
                       for r, needed in zip(records, required)))
    except (ValueError, OSError) as error:
        print(f"FAIL {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
