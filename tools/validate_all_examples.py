#!/usr/bin/env python3
"""Validate all OSTF examples on Windows, macOS and Linux."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1]
files=sorted((root/'examples').glob('*.ostf'))
if not files:raise SystemExit('No .ostf examples found')
raise SystemExit(subprocess.call([sys.executable,str(root/'tests/validate_ostf.py'),*[str(p) for p in files]]))
