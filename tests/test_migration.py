import sys,json,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'tools'))
from migrate_v11_preview import convert
from validate_ostf import check
p=Path(__file__).parents[1]/'examples'/'legacy_v11_preview_fixture.json'
src=json.loads(p.read_text())
out,r=convert(src)
assert r['valid_v12'] and not r['unsupported'],r
assert not check(out)
assert out['meterMap'][1]['at']=='8' and out['chords'][2]['kind']=='no-chord'
assert out['sections'][1]['start']=='8'
s=copy.deepcopy(src);s['harmony']['tracks'][0]['events'][0]['symbol']='C7(b9,#9)'
o,r=convert(s)
assert any('Unparsed chord' in x for x in r['unsupported'])
assert len(o['chords'])==2
print('PASS: legacy preview subset migration, structure and loss reporting')
