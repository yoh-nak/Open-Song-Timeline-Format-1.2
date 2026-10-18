#!/usr/bin/env python3
import copy,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_ostf import check
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'examples/mixed_meter_song.ostf').read_text())
assert not check(data), check(data)
def must_fail(change,label):
 d=copy.deepcopy(data);change(d)
 err=check(d)
 assert err, f'{label}: unexpectedly valid'
def must_pass(change,label):
 d=copy.deepcopy(data);change(d)
 assert not check(d), f'{label}: {check(d)}'
must_fail(lambda d:d['meterMap'].append(copy.deepcopy(d['meterMap'][0])),'duplicate meter')
must_fail(lambda d:d['tempoMap'].append(copy.deepcopy(d['tempoMap'][0])),'duplicate tempo')
must_fail(lambda d:d['sections'][0].update(duration='999'),'outside section')
must_fail(lambda d:d['chords'][0].update(duration='999'),'outside chord')
must_fail(lambda d:d['meterMap'][0].update(numerator=0),'invalid meter')
must_fail(lambda d:d['tempoMap'][0].update(bpm=0),'invalid tempo')
print('RC3 boundary/conformance negative fixtures: 6 passed')
