"""OCR lại nhãn van (B1-xx, C1-xx, BR-xx…) trên một trang của "02. P&ID Xuong Phu Tro_2025.pdf": đặt lại độ dày nét vẽ trong PDF (nhãn gốc nét rất đậm, OCR đọc sai 3/5/6/8), render 900 dpi, dò khung chữ nhật nhỏ, OCR.
    python3 relabel.py <trang PDF> <sheet id> [thư mục ra=hl] [độ dày nét=1.5; bản vẽ 2539 nét mảnh dùng 3]"""
import cv2,numpy as np,pytesseract,re,sys,json,subprocess,os,tempfile
PDF="/mnt/user-data/uploads/PIDvaQLSX/02. P&ID Xuong Phu Tro_2025.pdf"
DPI=900
PAT=re.compile(r'^([BCN][A-Z0-9]{0,2})-(\d{1,3}[A-Z]?)$')
def render(page,d):
    a=f"{d}/a.pdf";q=f"{d}/q.pdf";t=f"{d}/t.pdf"
    subprocess.run(["qpdf","--empty","--pages",PDF,str(page),"--",a],check=True)
    subprocess.run(["qpdf","--qdf","--object-streams=disable",a,q],check=True)
    b=open(q,'rb').read()
    b=re.sub(rb'(?<=[\s\n])(\d+(?:\.\d+)?) w\b',(sys.argv[4] if len(sys.argv)>4 else '1.5').encode()+b' w',b)
    open(t,'wb').write(b)
    subprocess.run(["pdftoppm","-r",str(DPI),"-png","-singlefile",t,f"{d}/r"],check=True,stderr=subprocess.DEVNULL)
    return cv2.imread(f"{d}/r.png",cv2.IMREAD_GRAYSCALE)
def ocr(c):
    c=cv2.copyMakeBorder(c,20,20,20,20,cv2.BORDER_CONSTANT,value=255)
    return pytesseract.image_to_string(c,config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-').strip().replace(" ","")
def find(g):
    H,W=g.shape
    bw=(g<170).astype(np.uint8)*255
    cnts,_=cv2.findContours(bw,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    seen=[];out=[]
    s=DPI/1160
    for c in cnts:
        x,y,w,h=cv2.boundingRect(c)
        lo,hi=min(w,h),max(w,h)
        if not(35*s<lo<110*s and 1.5<hi/lo<6 and hi<420*s):continue
        ap=cv2.approxPolyDP(c,0.04*cv2.arcLength(c,True),True)
        if len(ap)!=4:continue
        if any(abs(x-a)<8 and abs(y-b)<8 for a,b in seen):continue
        seen.append((x,y))
        m=5
        crop=g[y+m:y+h-m,x+m:x+w-m]
        if crop.size==0:continue
        if h>w:
            cands=[ocr(cv2.rotate(crop,cv2.ROTATE_90_CLOCKWISE)),ocr(cv2.rotate(crop,cv2.ROTATE_90_COUNTERCLOCKWISE))]
        else:cands=[ocr(crop)]
        t=next((z for z in cands if PAT.match(z)),None)
        if t:out.append([t,round(x/W,4),round(y/H,4),round(w/W,4),round(h/H,4)])
    return out
if __name__=='__main__':
    page,sid=int(sys.argv[1]),sys.argv[2]
    with tempfile.TemporaryDirectory() as d:
        g=render(page,d);r=find(g)
    json.dump(r,open(os.path.join(sys.argv[3] if len(sys.argv)>3 else "hl",f"{sid}.json"),"w"))
    print(sid,len(r))
