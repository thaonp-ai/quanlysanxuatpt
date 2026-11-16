import sys,json;sys.path.insert(0,'/home/claude/vwork');import glyph,os
page,sid=int(sys.argv[1]),sys.argv[2]
v=json.load(open(f'vp/{sid}.json'));g=glyph.render(page)
out=[[*b[:4],b[4],glyph.read_bubble(g,b[:4])] for b in v['bub']]
os.makedirs('br',exist_ok=True);json.dump(out,open(f'br/{sid}.json','w'));print(sid,len(out))
