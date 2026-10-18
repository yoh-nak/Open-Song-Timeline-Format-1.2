#!/usr/bin/env python3
import copy,json,sys,math
from fractions import Fraction
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'tools'));sys.path.insert(0,str(root/'tests'))
from reference_timeline import measure_spans,seconds_between,at_time
from validate_ostf import check
examples=sorted((root/'examples').glob('*.ostf'))
for path in examples:
 d=json.loads(path.read_text(encoding='utf8'));assert check(d)==[],(path,check(d))
 spans=measure_spans(d);assert spans[0][0]==0 and spans[-1][1]==Fraction(d['duration'])
 assert all(a[1]==b[0] for a,b in zip(spans,spans[1:])),path
 assert seconds_between(d,'0',d['duration'])>0
 for cut in set([Fraction(0),Fraction(d['duration'])]+[s[0] for s in spans]):
  # additive wall clock even across ramps; tolerant of numerical floating point
  assert math.isclose(at_time(d,cut)+seconds_between(d,cut,d['duration']),at_time(d,d['duration']),rel_tol=1e-10,abs_tol=1e-8),path
 encoded=json.dumps(d,ensure_ascii=False);restored=json.loads(encoded)
 assert restored==d and check(restored)==[]
# 4/4 -> 3/4 -> 4/4: exact bar sequence
base={'duration':'18','meterMap':[{'at':'0','numerator':4,'denominator':4},{'at':'8','numerator':3,'denominator':4},{'at':'14','numerator':4,'denominator':4}]}
assert [(str(a),str(b),sig,partial) for a,b,sig,partial in measure_spans(base)]==[("0","4","4/4",False),("4","8","4/4",False),("8","11","3/4",False),("11","14","3/4",False),("14","18","4/4",False)]
# mid-measure change closes an incomplete bar; does not move changes
base={'duration':'10','meterMap':[{'at':'0','numerator':4,'denominator':4},{'at':'3','numerator':3,'denominator':4}]}
sp=measure_spans(base);assert sp[0]==(Fraction(0),Fraction(3),'4/4',True)
assert sp[1]==(Fraction(3),Fraction(6),'3/4',False)
# 6/8, dotted quarter 80 BPM -> 1.5 seconds per bar
base={'duration':'3','tempoMap':[{'at':'0','bpm':80,'beatUnit':'3/8','transition':'step'}]}
assert math.isclose(at_time(base,'3'),1.5)
# 120 -> 60 quarter BPM over 4 quarter notes: exact integral 4*ln(2) seconds
base={'duration':'4','tempoMap':[{'at':'0','bpm':120,'beatUnit':'1/4','transition':'linear-quarter-bpm'},{'at':'4','bpm':60,'beatUnit':'1/4','transition':'step'}]}
# standalone integration ends at 4: last endpoint at song end permitted for this mathematical fixture only
base['duration']='5'
assert math.isclose(seconds_between(base,'0','4'),4*math.log(2),rel_tol=1e-12)
print(f'PASS: RC1 temporal conformance ({len(examples)} full fixtures; bar continuity, mid-bar meter, pickup, ramp integration, roundtrip)')
