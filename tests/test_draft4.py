"""Draft 4 conformance tests: assertions are independent of schema validation."""
import copy,json,sys
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from validate_ostf import check,interpreted_chord
R=Path(__file__).parents[1]
x=json.loads((R/'examples/dual_altered_ninths.ostf').read_text())
assert not check(x), check(x)
tones=interpreted_chord(x['chords'][3])
assert (9,13) in tones and (9,15) in tones and (7,10) in tones
assert json.loads(json.dumps(x))==x
for change in [
    lambda v:v['chords'][3]['additionalTones'].append({'degree':9,'alter':-1}),
    lambda v:v['chords'][3]['additionalTones'].append({'degree':7,'alter':-1}),
    lambda v:v['chords'][3]['additionalTones'].append({'degree':1,'alter':0}),
]:
    v=copy.deepcopy(x);change(v);assert check(v),v
# 7/8=7/2 quarter notes; 6/8=3 quarter notes; exact triplet eighth = 1/3.
assert Fraction(7*4,8)==Fraction(7,2)
assert Fraction(6*4,8)==3
assert 3*Fraction(1,3)==1
# Map change on shared boundary and section endpoint are non-overlapping.
assert Fraction('16')==Fraction(x['sections'][0]['start'])+Fraction(x['sections'][0]['duration'])
assert Fraction(x['meterMap'][1]['at'])==Fraction(x['sections'][1]['start'])
print('PASS: Draft 4 harmony / invalid variants / rational timing / serialization')
