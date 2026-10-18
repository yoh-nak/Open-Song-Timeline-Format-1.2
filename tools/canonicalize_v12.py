#!/usr/bin/env python3
"""Canonical serialisation of VALID OSTF 1.2 core records. No UI/MIDI content."""
import json,sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tests"))
from validate_ostf import check
TIME_MAPS=("meterMap","tempoMap","keyMap")
def canonicalize(data):
    errors=check(data)
    if errors: raise ValueError("invalid OSTF: "+"; ".join(errors))
    out=deepcopy(data)
    for name in TIME_MAPS:
        if name in out:out[name].sort(key=lambda item:Fraction(item["at"]))
    for name in ("sections","chords"):
        if name in out:out[name].sort(key=lambda item:(Fraction(item["start"]),item.get("id","")))
    for chord in out.get("chords",[]):
        if "degrees" in chord:chord["degrees"].sort(key=lambda x:(x["degree"],x["operation"]))
        if "additionalTones" in chord:chord["additionalTones"].sort(key=lambda x:(x["degree"],x["alter"]))
    return out
def dumps(data):return json.dumps(canonicalize(data),ensure_ascii=False,indent=2,sort_keys=True)+"\n"
if __name__=="__main__":
    if len(sys.argv)!=2:raise SystemExit("usage: canonicalize_v12.py input.ostf.json")
    print(dumps(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))),end="")
