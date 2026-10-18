import copy,json,sys
from pathlib import Path
from validate_ostf import check
R=Path(__file__).parents[1]
a=json.loads((R/'examples/mixed_meter_song.ostf').read_text())
b=json.loads((R/'examples/pickup_tempo_ramp.ostf').read_text())
def good(v): assert not check(v),check(v)
def bad(v): assert check(v),'Expected rejection'
good(a);good(b)
for fn in [lambda x:x['meterMap'][0].update(beatGroups=[2,3]),lambda x:x['tempoMap'][-1].update(transition='linear-quarter-bpm'),lambda x:x['song'].update(pickupDuration='4'),lambda x:x['meterMap'].append(copy.deepcopy(x['meterMap'][0])),lambda x:x['chords'][1].update(start='3')]:
    t=copy.deepcopy(a);fn(t);bad(t)
t=copy.deepcopy(b);t['song']['pickupDuration']='4';bad(t)
print('PASS: 2 valid examples, 6 invalid mutation checks')

# Draft 3: exact abstract interval dictionaries and semantic conflicts
from validate_ostf import REGISTRY, interpreted_chord
assert len(REGISTRY['chordQualities'])==25
assert len(REGISTRY['scales'])==20
assert interpreted_chord({'quality':'major-seventh'})==[(1,0),(3,4),(5,7),(7,11)]
assert interpreted_chord({'quality':'dominant-seventh','degrees':[{'degree':9,'alter':-1,'operation':'add'}]})[-1]==(9,13)
assert interpreted_chord({'quality':'major-seventh','degrees':[{'degree':5,'alter':0,'operation':'omit'}]})==[(1,0),(3,4),(7,11)]
for mutation in [
    [{'degree':5,'alter':0,'operation':'add'}],
    [{'degree':9,'alter':0,'operation':'alter'}],
    [{'degree':5,'alter':1,'operation':'omit'}],
    [{'degree':9,'alter':-1,'operation':'add'},{'degree':9,'alter':1,'operation':'add'}],
]:
    x=copy.deepcopy(a);x['chords'][0]['degrees']=mutation;bad(x)
good(json.loads((R/'examples/harmony_extensions.ostf').read_text()))
print('PASS: Draft 3 registry and harmony semantic cases')
