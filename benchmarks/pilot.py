"""Repeatable zero-cost tool pilot; does not measure agent tokens or productivity."""
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
BASE = '0893df46e30af8b08c283d6ad53dd102929f77c4'
old = subprocess.check_output(['git','show',BASE+':tools/test.sh'], cwd=ROOT, text=True)
records=[]
with tempfile.TemporaryDirectory(prefix='harness-pilot-') as tmp:
    root=Path(tmp)
    (root/'tools/ci').mkdir(parents=True)
    (root/'tools/test.sh').write_text(old)
    (root/'tools/ci/godot-version.txt').write_text('4.7.2\n')
    fake=root/'fake-godot'
    fake.write_text('#!'+sys.executable+'''\nimport os,sys
if '--version' in sys.argv:
 print('4.7.2.stable.fake'); sys.exit(0)
if '--import' in sys.argv: sys.exit(int(os.environ['IMPORT_EXIT']))
print('1/1 passed'); sys.exit(int(os.environ['SUITE_EXIT']))
''')
    fake.chmod(0o755)
    for case,imp,suite in [('healthy',0,0),('import_failure',23,0),('exit_after_summary',0,42)]:
        for repetition in range(3):
            for arm in (['before','after'] if repetition%2==0 else ['after','before']):
                env=dict(os.environ,GODOT=str(fake),IMPORT_TRIES='1',IMPORT_EXIT=str(imp),SUITE_EXIT=str(suite))
                cmd=['bash',str(root/'tools/test.sh')] if arm=='before' else [sys.executable,str(ROOT/'tools/harness.py'),'godot','test']
                start=time.monotonic()
                run=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,timeout=10)
                records.append(dict(case=case,repetition=repetition+1,arm=arm,exit_code=run.returncode,
                                    accepted=(run.returncode==0)==(case=='healthy'),seconds=time.monotonic()-start,
                                    input_tokens=None,output_tokens=None,human_seconds=None))
summary={arm:{'accepted':sum(r['accepted'] for r in records if r['arm']==arm),'runs':9,
              'median_seconds':statistics.median(r['seconds'] for r in records if r['arm']==arm)} for arm in ['before','after']}
result=dict(kind='tool_correctness_pilot_not_agent_benchmark',baseline_commit=BASE,
            python=platform.python_version(),platform=platform.platform(),records=records,summary=summary,
            limitations=['No model calls or token measurements','Synthetic Godot executable','No cross-model or real game productivity conclusion'])
(ROOT/'benchmarks/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(summary,indent=2))
