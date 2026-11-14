"""Apply the local website diff only to matching preimages; never deploy."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('target', type=Path)
parser.add_argument('--apply', action='store_true')
args = parser.parse_args()
root = Path(__file__).resolve().parent
target = args.target.resolve()
manifest = json.loads((root/'manifest.json').read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None

applied = 0
for item in manifest:
    rel = Path(item['path'])
    if rel.is_absolute() or '..' in rel.parts or not (target/rel).resolve().is_relative_to(target):
        raise SystemExit('Unsafe patch destination')
    current = digest(target/rel)
    if current == item['after_sha256']:
        applied += 1
    elif current != item['before_sha256']:
        raise SystemExit('Concurrent modification; not applied: '+str(rel))
if applied == len(manifest):
    print('All files already applied; hashes verified')
    raise SystemExit(0)
if applied:
    raise SystemExit('Partially applied patch; review before continuing')
patch = (root/'changes.patch').read_bytes()
subprocess.run(['git','apply','--unidiff-zero','--check','-'], cwd=target, input=patch, check=True)
print(f'{len(manifest)} files ready; patch preimages match')
if args.apply:
    backup = Path(tempfile.mkdtemp(prefix='space8-site-backup-'))
    for item in manifest:
        dst = target/item['path']
        if digest(dst) != item['before_sha256']:
            raise SystemExit('File changed during apply: '+str(dst))
        if dst.exists():
            saved = backup/item['path'];saved.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(dst,saved)
    subprocess.run(['git','apply','--unidiff-zero','-'],cwd=target,input=patch,check=True)
    for item in manifest:
        if digest(target/item['path']) != item['after_sha256']:
            raise SystemExit('Applied file verification failed: '+item['path'])
    print('Applied and verified; prior versions: '+str(backup))
else:
    print('Dry run only; --apply writes source but never builds or deploys')
