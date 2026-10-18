#!/usr/bin/env python3
"""OSTF 1.2 RC3 audited reference structural + semantic validator."""
import json, sys
from fractions import Fraction
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA = json.loads((Path(__file__).parents[1] / 'spec' / 'OSTF_v1.2.schema.json').read_text())
REGISTRY = json.loads((Path(__file__).parents[1] / 'spec' / 'OSTF_v1.2_harmony_registry.json').read_text())
MAJOR_DEGREE = {1:0,2:2,3:4,4:5,5:7,6:9,7:11,8:12,9:14,10:16,11:17,12:19,13:21}

def rat(s):
    v = Fraction(s)
    if str(v) != s: raise ValueError(f'Rational must be canonical: {s} -> {v}')
    return v

def interpreted_chord(chord):
    """Return sorted (degree, chromatic-offset) pairs; NOT performed MIDI notes."""
    base = {x['degree']:x['semitones'] for x in REGISTRY['chordQualities'][chord['quality']]}
    for item in chord.get('degrees',[]):
        d, op, alter = item['degree'], item['operation'], item['alter']
        if op == 'omit':
            if alter != 0 or d not in base: raise ValueError('degrees: omit requires present degree, alter=0')
            del base[d]
        elif op == 'alter':
            if d not in base: raise ValueError('degrees: alter requires present degree')
            # Relative to diatonic MAJOR-reference degree; not an increment to quality-specific baseline.
            base[d] = MAJOR_DEGREE[d] + alter
        elif op == 'add':
            if d in base: raise ValueError('degrees: add requires absent degree')
            base[d] = MAJOR_DEGREE[d] + alter
    if 1 not in base: raise ValueError('degrees: root is mandatory')
    tones = list(base.items())
    # Additional asserted harmonic degree variants such as b9 + #9.
    # An exact duplicate of an existing (degree, chromatic-offset) is forbidden.
    for item in chord.get('additionalTones', []):
        d = item['degree']
        tone = (d, MAJOR_DEGREE[d] + item['alter'])
        if tone in tones:
            raise ValueError('additionalTones: duplicate harmonic tone')
        tones.append(tone)
    return sorted(tones)

def check(data):
    errors = [str(e) for e in Draft202012Validator(SCHEMA).iter_errors(data)]
    if errors: return errors
    D=rat(data['duration'])
    try:
        for mapname in ('meterMap','tempoMap','keyMap'):
            events=data.get(mapname,[])
            positions=[rat(e['at']) for e in events]
            if mapname != 'keyMap' and (not positions or 0 not in positions): errors.append(f'{mapname}: no event at 0')
            if len(positions)!=len(set(positions)): errors.append(f'{mapname}: duplicate event location')
            if any(p >= D for p in positions): errors.append(f'{mapname}: event at or beyond song end')
        for e in data['meterMap']:
            if 'beatGroups' in e and sum(e['beatGroups']) != e['numerator']:
                errors.append('meterMap: beatGroups must sum to numerator')
        pickup=data.get('song',{}).get('pickupDuration')
        if pickup is not None:
            p=rat(pickup)
            first=next(e for e in data['meterMap'] if rat(e['at'])==0)
            full=Fraction(first['numerator']*4,first['denominator'])
            if p>=full or p>=D:errors.append('song: pickupDuration must be shorter than first full measure and song')
            if any(0<rat(e['at'])<p for e in data['meterMap']):errors.append('song: meter change inside pickup')
        tempos=sorted(data['tempoMap'], key=lambda e:rat(e['at']))
        if tempos[-1]['transition']!='step': errors.append('tempoMap: last event must have step transition')
        for event in tempos:
            if event['transition']=='linear-quarter-bpm' and event is tempos[-1]:
                errors.append('tempoMap: ramp requires next event')
        for collection in ('sections','chords'):
            spans=[]
            for e in data[collection]:
                start,duration=rat(e['start']),rat(e['duration'])
                if start+duration>D: errors.append(f'{collection}: span exceeds duration')
                spans.append((start,start+duration))
                if 'degrees' in e:
                    keys=[x['degree'] for x in e['degrees']]
                    if len(keys)!=len(set(keys)):errors.append('degrees: duplicate degree (use one operation per degree)')
                if e.get('kind')=='chord':
                    try: interpreted_chord(e)
                    except ValueError as exc: errors.append(str(exc))
            spans.sort()
            if any(b[0]<a[1] for a,b in zip(spans,spans[1:])): errors.append(f'{collection}: overlaps')
        ids=[s['id'] for s in data['sections']]
        if len(ids)!=len(set(ids)): errors.append('sections: duplicate ID')
        # All rational fields are canonical, including semantic fractional fields.
        for e in data['tempoMap']:
            unit=rat(e['beatUnit'])
            if unit<=0 or unit>1: errors.append('tempoMap: beatUnit must be <=1 whole note')
    except (ValueError,ZeroDivisionError) as exc:
        errors.append(str(exc))
    return errors

if __name__=='__main__':
    paths=sys.argv[1:] or [str(Path(__file__).parents[1]/'examples'/'mixed_meter_song.ostf')]
    failures=0
    for p in paths:
        e=check(json.loads(Path(p).read_text()))
        print(f'{p}: '+ ('VALID' if not e else 'INVALID: '+'; '.join(e)))
        failures+=bool(e)
    sys.exit(int(bool(failures)))
