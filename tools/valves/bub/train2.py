import sys,json,numpy as np,cv2,re,glob,os
sys.path.insert(0,'/home/claude/vwork');import glyph
base=json.load(open('/home/claude/vwork/tmpl_base.json')) if os.path.exists('/home/claude/vwork/tmpl_base.json') else json.load(open('/home/claude/vwork/tmpl.json'))
json.dump(base,open('/home/claude/vwork/tmpl_base.json','w'))
X=list(base['X']);Y=list(base['Y'])
jobs=dict(l.split()[::-1] for l in open('vjobs.txt'))
cl=lambda s:re.sub(r'[^A-Z0-9/-]','',s.upper())
sheets=['PID-019','PID-023','PID-029','PID-031','PID-040','PID-045','PID-054','PID-073','PID-079','PID-087','PID-094','PID-034','PID-064','PID-085']
for sid in sheets:
    v=json.load(open(f'vp/{sid}.json'));g=glyph.render(int(jobs[sid]));H,W=g.shape;n0=len(Y)
    for t,box,r in v['tags']:
        s=cl(t)
        if not r or cl(r[0])!=s or len(s)<6:continue
        x,y,w,h=box
        if h*H>w*W:continue
        c=g[int((y-.001)*H):int((y+h+.001)*H),int((x-.001)*W):int((x+w+.001)*W)]
        gl=glyph.glyphs(c)
        if len(gl)!=len(s):continue
        rh=max(cc[3] for cc,_ in gl)
        for (cc,gg),ch in zip(gl,s):
            if ch in '-/' :continue
            if cc[3]<rh*0.7:continue
            X.append(glyph.feat(gg,rh).tolist());Y.append(ch)
    print(sid,len(Y)-n0)
json.dump({'X':X,'Y':Y},open('/home/claude/vwork/tmpl.json','w'))
import collections;print(sorted(collections.Counter(Y).items()))
