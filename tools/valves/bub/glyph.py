import cv2,numpy as np,re,subprocess,tempfile,json
PDF="/mnt/user-data/uploads/PIDvaQLSX/02. P&ID Xuong Phu Tro_2025.pdf"
def render(page,dpi=900,width='3'):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["qpdf","--empty","--pages",PDF,str(page),"--",f"{d}/a.pdf"],check=True)
        subprocess.run(["qpdf","--qdf","--object-streams=disable",f"{d}/a.pdf",f"{d}/q.pdf"],check=True)
        b=open(f"{d}/q.pdf",'rb').read();b=re.sub(rb'(?<=[\s\n])(\d+(?:\.\d+)?) w\b',width.encode()+b' w',b);open(f"{d}/t.pdf",'wb').write(b)
        subprocess.run(["pdftoppm","-r",str(dpi),"-png","-singlefile",f"{d}/t.pdf",f"{d}/r"],check=True,stderr=subprocess.DEVNULL)
        return cv2.imread(f"{d}/r.png",0)
def bubble_lines(g,box):
    H,W=g.shape;x,y,w,h=box;cx,cy=(x+w/2)*W,(y+h/2)*H;R=min(w*W,h*H)/2
    X=1.45
    c=g[max(0,int(cy-R)):int(cy+R),max(0,int(cx-R*X)):int(cx+R*X)].copy()
    if c.size==0 or min(c.shape)<20:return None,None
    k=c.shape[0]//2;cxl=int(cx-max(0,int(cx-R*X)))
    # erase the circle outline only (text may extend past it)
    cv2.circle(c,(cxl,k),int(R*0.985),255,max(5,int(R*0.09)))
    c[:, :max(0,cxl-int(R*1.42))]=255;c[:, cxl+int(R*1.42):]=255
    rows=(c<200).mean(axis=1)
    for i in range(len(rows)):
        if rows[i]>0.5:c[max(0,i-3):i+4,:]=255
    return c[:k],c[k:]
def glyphs(img):
    """segment a text line into glyphs by vertical projection gaps (stroke font: glyphs do not overlap in x)."""
    if img is None or img.size==0:return []
    b=(img<200).astype(np.uint8)
    H0,W0=b.shape
    n,lab,st,_=cv2.connectedComponentsWithStats(b,connectivity=8)
    for i in range(1,n):
        x,y,w,h,a=st[i]
        if w>0.33*W0 or h>0.62*H0 or x==0 or x+w>=W0 or y==0 and h<0.15*H0:b[lab==i]=0
    # keep only the main text band: rows with ink, largest run
    rows=b.sum(axis=1)>0
    if not rows.any():return []
    runs=[];st=None
    for i,r in enumerate(list(rows)+[False]):
        if r and st is None:st=i
        if not r and st is not None:runs.append((st,i));st=None
    y0,y1=max(runs,key=lambda r:r[1]-r[0])
    if y1-y0<img.shape[0]*0.2:return []
    bb=b[y0:y1]
    cols=bb.sum(axis=0)>0
    segs=[];st=None
    for i,c in enumerate(list(cols)+[False]):
        if c and st is None:st=i
        if not c and st is not None:segs.append([st,i]);st=None
    out=[]
    for x0,x1 in segs:
        sub=bb[:,x0:x1];r=np.where(sub.sum(axis=1)>0)[0]
        if len(r)==0:continue
        ya,yb=r[0],r[-1]+1
        if (yb-ya)<(y1-y0)*0.45 and (x1-x0)<(y1-y0)*0.2:continue   # specks
        out.append(([x0,y0+ya,x1-x0,yb-ya],sub[ya:yb]))
    return out
def feat(gl,ref_h):
    h,w=gl.shape
    gl=cv2.dilate(gl.astype(np.uint8),np.ones((3,3),np.uint8))
    g=cv2.resize(gl.astype(np.float32),(24,36),interpolation=cv2.INTER_AREA)
    v=g.flatten();v=v/(np.linalg.norm(v)+1e-6)
    return np.concatenate([v*0.97,[w/h*0.12,h/ref_h*0.12]])
_T=None
def _load():
    global _T
    if _T is None:
        d=json.load(open('/home/claude/vwork/tmpl.json'));_T=(np.array(d['X']),np.array(d['Y']))
    return _T
LET=set("ABCDEFGHIJKLMNOPQRSTUVWXYZ");DIG=set("0123456789")
def read_line(img,kind=None):
    X,Y=_load();gl=glyphs(img)
    if not gl:return "",[]
    hs=sorted(c[3] for c,_ in gl);rh=hs[len(hs)//2]
    gl=[(c,gg) for c,gg in gl if 0.75*rh<=c[3]<=1.25*rh]
    # drop outliers far from the text cluster (circle fragments)
    if len(gl)>2:
        xs=[c[0]+c[2]/2 for c,_ in gl];gaps=[xs[i+1]-xs[i] for i in range(len(xs)-1)];mg=sorted(gaps)[len(gaps)//2]
        while len(gl)>2 and xs[1]-xs[0]>1.8*mg:gl=gl[1:];xs=xs[1:]
        while len(gl)>2 and xs[-1]-xs[-2]>1.8*mg:gl=gl[:-1];xs=xs[:-1]
    out=[];sc=[]
    n=len(gl)
    for k,(c,gg) in enumerate(gl):
        f=feat(gg,rh);sims=X@f
        if kind=="top":allowed=LET|({"1","2","3"} if k==1 else set())
        elif kind=="bot":allowed=DIG|(LET if k==n-1 and k>=3 else set())|({"/"})
        else:allowed=None
        if allowed:
            m=np.array([y in allowed for y in Y]);sims=np.where(m,sims,-1)
        j=int(np.argmax(sims))
        if sims[j]<0.75:continue
        out.append(Y[j]);sc.append(float(sims[j]))
    return "".join(out),sc
def read_bubble(g,box):
    top,bot=bubble_lines(g,box)
    t,_=read_line(top,"top");b,_=read_line(bot,"bot")
    return (t+" "+b).strip()
