import json,re,sys,csv
sys.path.insert(0,'/home/claude/work')
import build as B, parse as P
U=json.load(open('/home/claude/work/areas_used.json')); HB=U['head']
d=json.load(open('/home/claude/work/site/data/data.json'))
alltags={t['t'] for t in d['tags']}
ok=re.compile(r"^\d{2}-[A-Z]{1,3}-\d{4}[A-Z]?(/[A-Z]{1,3}\d{0,2}[A-Z]?)?$")
tot=0; miss=[]
for i,s in enumerate(d['sheets']):
    if not s['id'].startswith('PID'): continue
    H=set()
    for src in ['ocr','ocr2']:
        words=json.load(open(f"/home/claude/work/{src}/{s['id']}.json"))['words']
        for t in P.extract({'words':words,'unit':''},None):
            if t[1]!='equipment': continue
            cx,cy=t[3]+t[5]/2,t[4]+t[6]/2
            if any(b[0]<=cx<=b[2] and b[1]<=cy<=b[3] for b in HB.get(s['id'],[])):
                for e in B.expand(t[0]):
                    e=re.sub('^50-','30-',e)
                    if ok.match(e) and e.split('-')[0]!='39': H.add(e)
    have={t['t'] for t in d['tags'] for o in t['o'] if o[0]==i}
    for h in sorted(H):
        tot+=1
        if h not in have: miss.append((s['unit'],s['dwg'],s['title'],h,'Có trên bản vẽ khác' if h in alltags else ''))
print(tot,len(miss), round(100*(1-len(miss)/tot)))
with open('/mnt/user-data/outputs/kiem-tra-thiet-bi-chua-nhan-dang.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['Unit','Bản vẽ','Tên bản vẽ','Thiết bị (theo khung tiêu đề)','Ghi chú'])
    for m in miss: w.writerow(m)
