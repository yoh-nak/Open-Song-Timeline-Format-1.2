#!/usr/bin/env python3
import copy,json,sys
from pathlib import Path
from fractions import Fraction
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_ostf import check,REGISTRY,SCHEMA,interpreted_chord
root=Path(__file__).resolve().parents[1]
base=json.loads((root/'examples/mixed_meter_song.ostf').read_text())
assert check(base)==[]
assert set(SCHEMA['properties']['chords']['items']['oneOf'][0]['properties']['quality']['enum'])==set(REGISTRY['chordQualities'])
assert set(SCHEMA['properties']['keyMap']['items']['properties']['scale']['enum'])==set(REGISTRY['scales'])
def invalid(edit):
 x=copy.deepcopy(base); edit(x); assert check(x),json.dumps(x)
invalid(lambda x:x['meterMap'][0].update(at='1/2'))
invalid(lambda x:x['tempoMap'][0].update(at='1/2'))
invalid(lambda x:x['tempoMap'][-1].update(transition='linear-quarter-bpm'))
invalid(lambda x:x['tempoMap'][0].update(beatUnit='5/4'))
invalid(lambda x:x['meterMap'][0].update(beatGroups=[3,3]))
invalid(lambda x:x['sections'][0].update(start='01'))
invalid(lambda x:x['sections'][0].update(duration='2/4'))
invalid(lambda x:x['chords'][0].update(start='1/0'))
assert (9,13) in interpreted_chord({'quality':'dominant-seventh','additionalTones':[{'degree':9,'alter':-1},{'degree':9,'alter':1}]})
print('Audit: registry/schema parity + 8 negative semantic cases + dual altered ninth passed')
