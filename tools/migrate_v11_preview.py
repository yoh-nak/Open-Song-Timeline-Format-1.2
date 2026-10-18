#!/usr/bin/env python3
"""Conservative migration of editor-produced OSTF 1.1 preview documents to 1.2.
Never silently guess chord semantics. Produces explicit loss report.
This supports only the documented legacy *preview-export subset*, not all OSTF 1.1.
"""
import json,re,sys,argparse
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests'))
from validate_ostf import check
QUAL={"":"major","m":"minor","min":"minor","maj":"major","7":"dominant-seventh","maj7":"major-seventh","M7":"major-seventh","m7":"minor-seventh","min7":"minor-seventh","dim":"diminished","aug":"augmented","sus2":"sus2","sus4":"sus4","m7b5":"half-diminished-seventh","dim7":"diminished-seventh","6":"major-sixth","m6":"minor-sixth","9":"dominant-ninth","maj9":"major-ninth","m9":"minor-ninth"}
PAT=re.compile(r'^([A-G](?:b|#)?)(maj9|maj7|min7|m7b5|dim7|sus2|sus4|maj|min9|dim|aug|min|M7|m9|m7|m6|m|9|7|6)?(?:/([A-G](?:b|#)?))?$')
def q(v):
    x=Fraction(str(v));return str(x)
def convert(src):
    report={'source':'OSTF 1.1 editor preview subset','warnings':[],'unsupported':[],'preserved':[]}
    if str(src.get('ostf'))!='1.1':raise ValueError('Source must declare ostf: 1.1')
    timeline=src.get('timeline',{}); arr=src.get('arrangement',{})
    if 'duration' not in arr:raise ValueError('arrangement.duration required')
    d=q(arr['duration']);sections=[]
    for s in src.get('structure',{}).get('sections',[]):
        sections.append({'id':s['id'],'name':s.get('name',''),'start':q(s['at']),'duration':q(s['duration'])})
        if 'tonality' in s or 'tonalRegions' in s:
            report['unsupported'].append('Section-specific tonality/tonalRegions require manual mapping to keyMap; data not converted')
    meters=[{'at':q(e['at']),'numerator':e['numerator'],'denominator':e['denominator']} for e in timeline.get('meter',[])]
    tempos=[]
    for e in timeline.get('tempo',[]):
        if e.get('shape','step')!='step':report['unsupported'].append('Non-step legacy tempo shape requires manual review');continue
        tempos.append({'at':q(e['at']),'bpm':e['bpm'],'beatUnit':'1/4','transition':'step'})
    chords=[]
    tracks=src.get('harmony',{}).get('tracks',[])
    if len(tracks)>1:report['unsupported'].append('Multiple legacy harmony tracks cannot be flattened losslessly')
    for t in tracks:
        for e in t.get('events',[]):
            kind=e.get('kind','chord');item={'start':q(e['at']),'duration':q(e['duration'])}
            if kind in ('none','no-chord') or e.get('symbol')=='N.C.':item['kind']='no-chord'
            else:
                symbol=e.get('symbol','');m=PAT.fullmatch(symbol)
                if not m or (m.group(2) or '') not in QUAL:
                    report['unsupported'].append(f'Unparsed chord symbol at {item["start"]}: {symbol!r}');continue
                item.update(kind='chord',root=m.group(1),quality=QUAL[m.group(2) or ''],symbol=symbol)
                if m.group(3):item['bass']=m.group(3)
            chords.append(item)
    out={'format':'OSTF','version':'1.2','timeBase':'quarter-note','duration':d,'song':{'title':src.get('work',{}).get('title','')},'meterMap':meters,'tempoMap':tempos,'sections':sections,'chords':chords}
    for k in src:
        if k not in ('ostf','document','work','arrangement','timeline','structure','harmony'):
            report['unsupported'].append('Unknown source top-level field: '+k)
    if len(tracks)>1 or any('Unparsed chord' in x for x in report['unsupported']):
        report['warnings'].append('Conversion is INCOMPLETE: skipped harmony data; do not replace original')
    if not meters or not tempos:report['warnings'].append('Missing first meter/tempo event; 1.2 validation will fail')
    report['preserved']=['time positions as exact rational values','meter changes','step tempos assuming quarter-note beat unit','section positions','recognized basic chord symbols / N.C.']
    report['warnings'].append('Legacy tempo beat-unit is not explicit: assumed quarter note; manually verify compound-meter projects')
    errors=check(out)
    if errors:report['unsupported'].extend('v1.2 validation: '+e for e in errors)
    report['valid_v12']=not errors
    report['lossless']=not report['unsupported'] and not report['warnings']
    return out,report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');args=p.parse_args()
    out,r=convert(json.loads(Path(args.source).read_text(encoding='utf8')))
    Path(args.output).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    Path(args.output+'.report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(r,indent=2,ensure_ascii=False));sys.exit(0 if r['valid_v12'] and not r['unsupported'] else 2)
