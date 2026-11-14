# Trích mục lục giáo trình (tất cả cấp, kể cả a), b), 1.) từ text PDF đã làm sạch C01..C09.txt (pdftotext) → toc2.json; chạy tiếp gtcv_tocfix.py để sửa dòng ngắt và ghi gtcv_auto.json. Trang in = trang PDF (đã kiểm tra).
import re,json
HEAD=re.compile(r'^\s*(CHƯƠNG|Chương|PHẦN|PHỤ LỤC|Phụ lục|CÂU HỎI|[IVX]+\s*\.|\d+(\.\d+)*\s*\.?\s|[a-h]\)|[a-h]\.\d|DANH MỤC)')
out={}
for n in range(1,10):
    L=open('/tmp/claude-0/gtcv/C0%d.txt'%n).read().split('\n')
    # TOC region: from first dotted line to last dotted line within first 420 lines
    idx=[i for i,l in enumerate(L[:420]) if re.search(r'\.{4,}',l)]
    a,b=idx[0],idx[-1]
    toc=[];prev=None;seen=set()
    for i in range(a,b+1):
        l=L[i].strip()
        if not l or ('NHÀ MÁY ĐẠM' in l and not re.search(r'\.{4,}',l)): continue
        m=re.match(r'^(.*?\S)\s*\.{4,}[\s.]*(\d+)?\s*$',l)
        if not m:
            if re.fullmatch(r'\d+',l): 
                if toc and toc[-1][1] is None: toc[-1][1]=int(l)
                continue
            prev=l if HEAD.match(l) else (prev+' '+l if prev else None); continue
        t,p=m.group(1).strip(),m.group(2)
        if not HEAD.match(t) and prev: t=prev+' '+t
        prev=None
        t=re.sub(r'\s+',' ',t)
        k=(t,p)
        if k in seen: continue
        seen.add(k); toc.append([t,int(p) if p else None])
    out['GT%02d'%n]=toc
json.dump(out,open('/tmp/claude-0/toc2.json','w'),ensure_ascii=False,indent=0)
for k,v in out.items():
    print('=====',k,len(v))
    for t,p in v:
        if not HEAD.match(t): print('  ??',t,'|',p)
