#!/usr/bin/env python3
"""Install the pinned official engine/templates, checking upstream SHA-512 sums."""

import argparse
import hashlib
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import subprocess
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def download(url: str, destination: Path) -> None:
    """Never retain an interrupted download as a usable cached archive."""
    temporary = destination.with_suffix(destination.suffix + ".partial")
    with urllib.request.urlopen(url, timeout=120) as response, temporary.open("wb") as output:
        shutil.copyfileobj(response, output)
    temporary.replace(destination)


def verify_checksum(archive: Path, sums: str) -> None:
    entries = {}
    for line in sums.splitlines():
        parts = line.split()
        if len(parts) == 2:
            entries[parts[1].lstrip("*")] = parts[0]
    expected = entries.get(archive.name, "")
    if not re.fullmatch(r"[a-fA-F0-9]{128}", expected):
        raise ValueError(f"Missing SHA-512 for {archive.name}")
    with archive.open("rb") as source:
        actual = hashlib.file_digest(source, "sha512").hexdigest()
    if actual != expected.lower():
        raise ValueError(f"SHA-512 mismatch: {archive.name}")


def validate_archive(archive: Path) -> None:
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            path = PurePosixPath(member.filename.replace("\\", "/"))
            if path.is_absolute() or ".." in path.parts or ":" in member.filename:
                raise ValueError("Unsafe archive member")


def install(templates: bool, cache_root: Path | None = None) -> Path:
    version = (ROOT / "tools/ci/godot-version.txt").read_text().strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Expected an exact stable Godot version")
    system = platform.system()
    suffix, executable = {
        "Linux": ("linux.x86_64.zip", f"Godot_v{version}-stable_linux.x86_64"),
        "Darwin": ("macos.universal.zip", "Godot.app/Contents/MacOS/Godot"),
        "Windows": ("win64.exe.zip", f"Godot_v{version}-stable_win64_console.exe"),
    }[system]
    cache = (cache_root or Path.home() / "godot") / version
    cache.mkdir(parents=True, exist_ok=True)
    base = f"https://github.com/godotengine/godot/releases/download/{version}-stable"
    with urllib.request.urlopen(f"{base}/SHA512-SUMS.txt", timeout=120) as response:
        sums = response.read().decode("utf-8")

    def asset(name: str) -> Path:
        path = cache / name
        if not path.exists():
            download(f"{base}/{name}", path)
        verify_checksum(path, sums)
        validate_archive(path)
        return path

    engine = asset(f"Godot_v{version}-stable_{suffix}")
    engine_dir = cache / "engine"
    if engine_dir.exists():
        shutil.rmtree(engine_dir)
    engine_dir.mkdir(exist_ok=True)
    if system == "Darwin":
        subprocess.run(["ditto", "-x", "-k", str(engine), str(engine_dir)], check=True)
    else:
        with zipfile.ZipFile(engine) as bundle:
            bundle.extractall(engine_dir)
    binary = engine_dir / executable
    binary.chmod(binary.stat().st_mode | 0o111)
    actual = subprocess.check_output([str(binary), "--version"], text=True).strip()
    if not actual.startswith(version + ".stable."):
        raise ValueError(f"Unexpected engine version: {actual}")
    if templates:
        archive = asset(f"Godot_v{version}-stable_export_templates.tpz")
        data_root = {
            "Darwin": Path.home() / "Library/Application Support",
            "Windows": Path(os.environ.get("APPDATA", str(Path.home() / "AppData/Roaming"))),
            "Linux": Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local/share"))),
        }[system]
        folder_name = "Godot" if system == "Windows" else "godot"
        # macOS uses a capital G, unlike Linux.
        if system == "Darwin":
            folder_name = "Godot"
        target = data_root / folder_name / "export_templates" / f"{version}.stable"
        target.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive) as bundle:
            for member in bundle.infolist():
                relative = PurePosixPath(member.filename)
                if relative.parts[0] != "templates":
                    raise ValueError("Unexpected template archive layout")
                destination = target.joinpath(*relative.parts[1:])
                if member.is_dir():
                    destination.mkdir(parents=True, exist_ok=True)
                else:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with bundle.open(member) as source, destination.open("wb") as output:
                        shutil.copyfileobj(source, output)
    if os.environ.get("GITHUB_ENV"):
        with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as output:
            output.write(f"GODOT={binary.as_posix()}\nGODOT_VERSION={version}\n")
    print(f"Godot {actual}: {binary}")
    return binary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--templates", action="store_true")
    parser.add_argument("--cache-dir", type=Path, help="Override the archive/engine cache root")
    args = parser.parse_args()
    install(args.templates, args.cache_dir)
