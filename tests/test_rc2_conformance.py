#!/usr/bin/env python3
import sys,json,copy
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
sys.path.insert(0,str(ROOT/'tools'))
from validate_ostf import check
from canonicalize_v12 import canonicalize,dumps
cases=0
for path in sorted((ROOT/'examples').glob('*.ostf')):
    data=json.loads(path.read_text())
    assert not check(data),(path,check(data))
    one=canonicalize(data); two=canonicalize(one)
    assert one==two and dumps(one)==dumps(data)
    again=json.loads(dumps(data));assert not check(again)
    # preserve every exact time coordinate
    for name,key in [('meterMap','at'),('tempoMap','at'),('sections','start'),('chords','start')]:
        assert sorted(Fraction(x[key]) for x in data.get(name,[]))==sorted(Fraction(x[key]) for x in again.get(name,[]))
    cases+=1
x=json.loads((ROOT/'examples/mixed_meter_song.ostf').read_text())
def rejected(mut):
    c=copy.deepcopy(x);mut(c); assert check(c),c
rejected(lambda c:c['meterMap'].append(dict(c['meterMap'][0])))
rejected(lambda c:c['tempoMap'].__setitem__(0,{**c['tempoMap'][0],'transition':'linear-quarter-bpm'}) if len(c['tempoMap'])==1 else c['tempoMap'][-1].update(transition='linear-quarter-bpm'))
rejected(lambda c:c['sections'].append(dict(c['sections'][0])))
rejected(lambda c:c.update(duration='1/2'))
print(f'PASS: RC2 canonical serialization and exact-time roundtrips on {cases} fixtures; 4 negative checks')
