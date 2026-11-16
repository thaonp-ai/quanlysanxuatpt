"""Đọc lại bong bóng + chữ tại vị trí từng tag trên một trang P&ID (nét vẽ đặt lại 3 đơn vị, 900 dpi)."""
import cv2,numpy as np,pytesseract,re,sys,json,subprocess,os,tempfile
PDF="/mnt/user-data/uploads/PIDvaQLSX/02. P&ID Xuong Phu Tro_2025.pdf"
DPI=900
WL='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-/'
def render(page,d):
    subprocess.run(["qpdf","--empty","--pages",PDF,str(page),"--",f"{d}/a.pdf"],check=True)
    subprocess.run(["qpdf","--qdf","--object-streams=disable",f"{d}/a.pdf",f"{d}/q.pdf"],check=True)
    b=open(f"{d}/q.pdf",'rb').read();b=re.sub(rb'(?<=[\s\n])(\d+(?:\.\d+)?) w\b',b'3 w',b);open(f"{d}/t.pdf",'wb').write(b)
    subprocess.run(["pdftoppm","-r",str(DPI),"-png","-singlefile",f"{d}/t.pdf",f"{d}/r"],check=True,stderr=subprocess.DEVNULL)
    return cv2.imread(f"{d}/r.png",0)
def prep(c):
    _,b=cv2.threshold(c,200,255,cv2.THRESH_BINARY)
    b=cv2.erode(b,np.ones((2,2),np.uint8))
    return cv2.copyMakeBorder(b,25,25,25,25,cv2.BORDER_CONSTANT,value=255)
def ocr(c,psm):
    if c.size==0:return ""
    return " ".join(pytesseract.image_to_string(prep(c),config=f'--psm {psm} '+WL).split())
def main(page,sid,tags,kinds):
    os.makedirs('vp/img',exist_ok=True)
    with tempfile.TemporaryDirectory() as d:g=render(page,d)
    H,W=g.shape
    items=[]
    for f in ("/home/claude/work/bub/","/home/claude/work/bub2/"):
        try:items+=json.load(open(f+sid+".json"))["items"]
        except Exception:pass
    bubs=[]
    for it in items:
        if any(abs(it['x']-b[0])<.002 and abs(it['y']-b[1])<.002 for b in bubs):continue
        x,y,w,h=it['x'],it['y'],it['w'],it['h']
        cx,cy=(x+w/2)*W,(y+h/2)*H;R=min(w*W,h*H)/2
        c=g[int(cy-R):int(cy+R),int(cx-R):int(cx+R)].copy()
        if c.size==0:continue
        k=c.shape[0]//2
        cv2.circle(c,(c.shape[1]//2,k),int(R*0.97),255,max(6,int(R*0.16)))
        m=np.full_like(c,255);cv2.circle(m,(c.shape[1]//2,k),int(R*0.86),0,-1);c[m==255]=255
        # erase a horizontal divider line if present
        rows=(c<128).mean(axis=1)
        for i in range(len(rows)):
            if rows[i]>0.55:c[max(0,i-3):i+4,:]=255
        top,bot=c[:k+2],c[k-2:]
        txt=(ocr(top[int(k*0.25):],7)+" "+ocr(bot[:int(k*0.8)],7)).strip()
        bubs.append([x,y,w,h,txt])
    out={"bub":bubs,"tags":[]}
    for t,o in tags:
        x,y,w,h=o[1:5];vert=h*H>w*W*1.4
        mx,my=(0.004,0.0025) if not vert else (0.0025,0.004)
        c=g[max(0,int((y-my)*H)):int((y+h+my)*H),max(0,int((x-mx)*W)):int((x+w+mx)*W)]
        r=[ocr(c,7)] if not vert else [ocr(cv2.rotate(c,cv2.ROTATE_90_CLOCKWISE),7),ocr(cv2.rotate(c,cv2.ROTATE_90_COUNTERCLOCKWISE),7)]
        out["tags"].append([t,o[1:5],r])
        if kinds.get(t)=="valve":
            cx,cy=(x+w/2)*W,(y+h/2)*H;R=max(w*W,h*H)*1.3
            cc=g[max(0,int(cy-R)):int(cy+R),max(0,int(cx-R)):int(cx+R)]
            if cc.size:cv2.imwrite(f"vp/img/{sid}_{len(out['tags'])-1}.png",cv2.resize(cc,(200,200),interpolation=cv2.INTER_AREA))
    os.makedirs("vp",exist_ok=True);json.dump(out,open(f"vp/{sid}.json","w"))
    print(sid,len(bubs),len(tags))
if __name__=="__main__":
    page,sid=int(sys.argv[1]),sys.argv[2]
    d=json.load(open("/home/claude/vwork/data_before.json"))
    si=[i for i,s in enumerate(d["sheets"]) if s["id"]==sid][0]
    tags=[(t["t"],o) for t in d["tags"] for o in t["o"] if o[0]==si and len(o)==5]
    kinds={t['t']:t['k'] for t in d['tags']}
    main(page,sid,tags,kinds)
