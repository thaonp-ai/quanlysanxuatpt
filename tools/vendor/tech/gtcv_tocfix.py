# Sửa tay các dòng mục lục bị ngắt/thừa và gán cấp (0 chương, 1 X.n, 2 X.n.n, 3 a)/1./X.n.n.n) → gtcv_auto.json.
import json,re
toc=json.load(open('/tmp/claude-0/toc2.json'))
auto=json.load(open('/home/claude/quanlysanxuatpt/tools/vendor/tech/gtcv_auto.json'))
FIX={
 'GT01':{'NHÀ MÁY ĐẠM PHÚ MỸ':None,'CHƯƠNG II: HỆ THỐNG NƯỚC THÔ - NƯỚC SINH HOẠT':('CHƯƠNG II: HỆ THỐNG NƯỚC THÔ - NƯỚC SINH HOẠT NHÀ MÁY ĐẠM PHÚ MỸ',20)},
 'GT02':{'NHÀ MÁY ĐẠM PHÚ MỸ':None,'Chương II: HỆ THỐNG NƯỚC LÀM MÁT TẠI XƯỞNG PHỤ TRỢ-':('Chương II: HỆ THỐNG NƯỚC LÀM MÁT TẠI XƯỞNG PHỤ TRỢ – NHÀ MÁY ĐẠM PHÚ MỸ',19)},
 'GT04':{'PHIẾU NHẬN XÉT, ĐÁNH GIÁ GIÁO TRÌNH/TÀI LIỆU':None},
 'GT05':{'MỸ':('PHẦN II: HỆ THỐNG XỬ LÝ NƯỚC THẢI – NHÀ MÁY ĐẠM PHÚ MỸ',60)},
 'GT06':{'Và các thiết bị đo lường, điều khiển, các loại van.':None,'Mô tả công nghệ:':None},
 'GT07':{'30-PK-6001':None},
 'GT09':{'II.7.1. Quy trình công nghệ cụm làm lạnh 40-PK-5005':[('II.7. Hướng dẫn vận hành hệ thống làm lạnh hóa lỏng hơi NH3 40-PK-5005',31),('II.7.1. Quy trình công nghệ cụm làm lạnh 40-PK-5005',31)]},
}
def lvl(t):
    if re.match(r'(CHƯƠNG|Chương|PHẦN|PHỤ LỤC|CÂU HỎI|DANH MỤC)',t): return 0
    if re.match(r'^[IVX1]+\.\s*\d+\.\s*\d+\.\s*\d+',t): return 3
    if re.match(r'^[IVX1]+\.\s*\d+\.\s*\d+',t): return 2
    if re.match(r'^[IVX]+\.\s*\d+\.?\s',t): return 1
    if re.match(r'^Phụ lục',t): return 1
    return 3   # a), b)…, 1. 2. …
for k,v in toc.items():
    f=FIX.get(k,{});L=[]
    for t,p in v:
        if re.match(r'^(\d|I+)\.\s*(MỤC ĐÍCH|PHẠM VI|TÀI LIỆU|ĐỊNH NGHĨA)',t): continue
        if t in f:
            r=f[t]
            if r is None: continue
            for tt,pp in (r if isinstance(r,list) else [r]): L.append([lvl(tt),tt,pp])
            continue
        t=t.replace('30-PK- 1001','30-PK-1001')
        L.append([lvl(t),t,p])
    auto[k]['toc']=L
    print(k,len(L),sum(1 for x in L if x[2] is None))
json.dump(auto,open('/home/claude/quanlysanxuatpt/tools/vendor/tech/gtcv_auto.json','w'),ensure_ascii=False,indent=0)
