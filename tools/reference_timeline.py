#!/usr/bin/env python3
"""Reference musical timeline for OSTF v1.2 RC1. Score time only, no UI/MIDI."""
from fractions import Fraction
from math import log

def F(s): return Fraction(str(s))

def measure_spans(document):
    """Return (start,end,signature,partial) including pickup, changes mid-bar and last partial."""
    total=F(document['duration']); events=sorted(document['meterMap'],key=lambda e:F(e['at']))
    if not events or F(events[0]['at'])!=0: raise ValueError('missing initial meter')
    pickup=F(document.get('song',{}).get('pickupDuration','0'))
    out=[]; pos=F(0); i=0
    while pos<total:
        while i+1<len(events) and F(events[i+1]['at'])<=pos:i+=1
        meter=events[i]; length=Fraction(meter['numerator']*4,meter['denominator'])
        first=pickup if pos==0 and pickup else length
        next_change=F(events[i+1]['at']) if i+1<len(events) else total
        end=min(pos+first,next_change,total)
        if end<=pos:raise ValueError('non-progressing measure')
        out.append((pos,end,f"{meter['numerator']}/{meter['denominator']}",end-pos!=length))
        pos=end
    return out

def quarter_bpm(event):
    q=float(event['bpm'])*4*float(F(event['beatUnit']))
    if q<=0:raise ValueError('nonpositive tempo')
    return q

def seconds_between(document,start,end):
    """Integrate tempo map from score position start to end (quarter notes)."""
    start,end=F(start),F(end);total=F(document['duration'])
    if not (0<=start<=end<=total):raise ValueError('range outside composition')
    events=sorted(document['tempoMap'],key=lambda e:F(e['at']))
    result=0.
    for i,ev in enumerate(events):
        a=F(ev['at']); b=F(events[i+1]['at']) if i+1<len(events) else total
        lo=max(a,start);hi=min(b,end)
        if lo>=hi:continue
        q0=quarter_bpm(ev)
        if ev['transition']=='step':result+=60*float(hi-lo)/q0
        elif ev['transition']=='linear-quarter-bpm':
            if i+1>=len(events):raise ValueError('ramp without endpoint')
            q1=quarter_bpm(events[i+1]);slope=(q1-q0)/float(b-a)
            qa=q0+slope*float(lo-a);qb=q0+slope*float(hi-a)
            result+=(60/slope)*log(qb/qa) if abs(slope)>1e-12 else 60*float(hi-lo)/q0
        else:raise ValueError('unknown tempo interpolation')
    return result

def at_time(document, position):return seconds_between(document,'0',position)
