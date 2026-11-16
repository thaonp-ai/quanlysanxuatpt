import json,glob,os,re,sys
sys.path.insert(0,'/home/claude/quanlysanxuatpt/tools/valves')
from fuzzy import clean,dist
from PIL import Image,ImageDraw,ImageFont
d=json.load(open('/home/claude/vwork/data_before.json'))
K={t['t']:t for t in d['tags']}
rows=[]
for f in sorted(glob.glob('/home/claude/vwork/vp/*.json')):
    sid=os.path.basename(f)[:-5];v=json.load(open(f))
    for i,(t,box,r) in enumerate(v['tags']):
        e=K.get(t)
        if not e or e['k']!='valve' or e['s']=='BLOCK':continue
        x,y,w,h=box;cx,cy=x+w/2,y+h/2
        b=min(v['bub'],key=lambda b:abs(b[0]+b[2]/2-cx)+abs(b[1]+b[3]/2-cy),default=None)
        bt=b[4] if b and abs(b[0]+b[2]/2-cx)<.006 and abs(b[1]+b[3]/2-cy)<.006 else ''
        m=re.match(r'^\d\d-([A-Z]+)-(\w+)$',t);exp=clean(m.group(1)+m.group(2)) if m else clean(t)
        ok=clean(bt)==exp
        rows.append(dict(sid=sid,i=i,t=t,bt=bt,ok=ok,d=dist(clean(bt),exp)))
json.dump(rows,open('/home/claude/vwork/rev/rows.json','w'))
print(len(rows),sum(r['ok'] for r in rows))
bad=[r for r in rows if not r['ok']]
fnt=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15) if os.path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf') else None
N=36
for p in range(0,len(bad),N):
    G=Image.new('RGB',(6*240,6*260),'white');dr=ImageDraw.Draw(G)
    for j,r in enumerate(bad[p:p+N]):
        fn=f"/home/claude/vwork/vp/img/{r['sid']}_{r['i']}.png"
        X,Y=(j%6)*240,(j//6)*260
        if os.path.exists(fn):G.paste(Image.open(fn).convert('RGB').resize((220,220)),(X+10,Y))
        dr.text((X+5,Y+222),f"{p+j} {r['t']}",fill='blue',font=fnt);dr.text((X+5,Y+240),f"ocr:{r['bt']}",fill='red',font=fnt)
    G.save(f"/home/claude/vwork/rev/p{p//N:02d}.png")
print(len(bad))
