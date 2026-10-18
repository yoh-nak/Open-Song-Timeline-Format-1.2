#!/usr/bin/env python3
"""Execute shipped regression suites plus the new example validation."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1]
tests=sorted((root/'tests').glob('test_*.py'))
for t in tests:
 print('RUN',t.name,flush=True)
 if subprocess.call([sys.executable,str(t)],cwd=root):raise SystemExit('FAILED: '+str(t))
if subprocess.call([sys.executable,str(root/'tools/validate_all_examples.py')],cwd=root):raise SystemExit('Example validation failed')
print('ALL SUITES PASSED')
