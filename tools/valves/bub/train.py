import sys,json,numpy as np,cv2
sys.path.insert(0,'/home/claude/vwork');import glyph
meta=json.load(open('/home/claude/vwork/lab_meta.json'))
lab={int(l.split()[0]):l.split()[1:] for l in open('/home/claude/vwork/labels.txt')}
pages={'PID-019':19,'PID-054':54,'PID-087':87,'PID-093':93}
X=[];Y=[];bad=0;used=0;dbg=[]
for sid,pg in pages.items():
    g=glyph.render(pg)
    for i,(s,box) in enumerate(meta):
        if s!=sid or i not in lab:continue
        top,bot=glyph.bubble_lines(g,box)
        for img,txt in ((top,lab[i][0]),(bot,lab[i][1])):
            gl=glyph.glyphs(img)
            if len(gl)!=len(txt):
                bad+=1;dbg.append((i,txt,len(gl)))
                if len(dbg)<6:cv2.imwrite(f'/home/claude/vwork/dbg{len(dbg)}.png',img)
                continue
            used+=1
            rh=max(c[3] for c,_ in gl)
            for (c,gg),ch in zip(gl,txt):X.append(glyph.feat(gg,rh).tolist());Y.append(ch)
json.dump({'X':X,'Y':Y},open('/home/claude/vwork/tmpl.json','w'))
print(used,bad,len(X));print(dbg)
