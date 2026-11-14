#!/usr/bin/env python3
"""Danh mục "Vendor Data/9. Xử lý nước thải" (Unit 42: 40-PK-2001 nhiễm dầu, 40-PK-2002 sinh hoạt, 40-PK-2003 MBR mới) -> docs.json + sizes.json.

Đầu vào: listing.txt (đường dẫn tương đối | byte). Đã bỏ:
  - "Tai lieu huong dan van hanh Tram XLNT Phu My/" (bản sao của "20. 40-PK-2003/"),
  - 2 file STVB127286 trong "DNTD thay mang membrane/" (trùng file ở gốc), "Revamp_WWT/Section 300…" (trùng Section 200),
  - "So do cac diem thu gom NTND nha may (1).pdf" ở gốc (trùng file trong "Kiểm soát nước thải đầu vào/"),
  - .dwg/.DWG, ~$*, Thumbs.db, ảnh "Hình ảnh hiện trường", các PDF 814 byte (file hỏng) trong "Kiểm soát nước thải đầu vào/".
Tài liệu là file riêng, không cần tách sách.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
R = "9. Xử lý nước thải"

G_DS = "Data sheet & tài liệu chính"
G_OM = "Vận hành & bảo dưỡng"
G_SYS = "Hệ thống (P&ID, mô tả công nghệ)"
G_INC = "Sự cố & trao đổi"
G_REF = "Tài liệu tham khảo"
G_REV = "Dự án cải tạo 2016"
G_ORD = "Đơn hàng & yêu cầu kỹ thuật (MR/SR)"

OW, SW, NW = "40-PK-2001", "40-PK-2002", "40-PK-2003"
ALL = [OW, SW, NW]
P3 = "40-PK-2003"
KS = "Kiểm soát nước thải đầu vào/"
GT = "Giảm thể tích bùn/Giảm thể tích bùn/"
MB = "DNTD thay mang membrane/STVB127286_"

L = [
    # Hệ thống XLNT mới 40-PK-2003 (MBR, 2012)
    ("20. 40-PK-2003/So tay huong dan van hanh tram Phu My 03072012 NOP Ref3.doc", "Sổ tay hướng dẫn vận hành trạm XLNT mới (07/2012)", G_OM, [NW]),
    ("20. 40-PK-2003/So tay huong dan van hanh phan xu ly sinh hoc.doc", "Sổ tay vận hành phần xử lý sinh học", G_OM, [NW]),
    ("20. 40-PK-2003/Xu Ly Nc Thai.doc", "Tài liệu xử lý nước thải (lý thuyết & vận hành)", G_REF, ALL),
    ("20. 40-PK-2003/So tay van hanh bao duong mang KOBUTA-VN.docx", "Sổ tay vận hành & bảo dưỡng màng MBR Kubota (tiếng Việt)", G_OM, [NW]),
    ("20. 40-PK-2003/Van hanh bao duong mang KOBUTA-EN.pdf", "Vận hành & bảo dưỡng màng MBR Kubota (tiếng Anh)", G_OM, [NW]),
    ("20. 40-PK-2003/So tay huong dan bao tri may ep bun.pdf", "Sổ tay bảo trì máy ép bùn BF-202", G_OM, [NW]),
    ("20. 40-PK-2003/So tay huong dan thi nghiem 200612.doc", "Sổ tay hướng dẫn thí nghiệm (MLSS, SVI, COD…)", G_OM, [NW]),
    ("20. 40-PK-2003/Tong hop khoi luong hoa chat.xlsx", "Tổng hợp khối lượng hóa chất", G_DS, [NW]),
    ("20. 40-PK-2003/Ke hoach dao tao va chuyen giao cong nghe sua 22062012 ver 2.doc", "Kế hoạch đào tạo & chuyển giao công nghệ (06/2012)", G_REF, [NW]),
    ("20. 40-PK-2003/B-PID-01-VN New Design_2-Model.pdf", "P&ID hệ thống XLNT mới 40-PK-2003 (bản nhà thầu)", G_SYS, [NW]),
    ("19. 40-P-3001AB & 40-P-3002AB/C) Datasheet and manufacturer manual.pdf", "Bơm thu gom nước thải sinh hoạt 40-P-3001A/B, 40-P-3002A/B – data sheet & hướng dẫn", G_DS, [NW, SW]),
    (MB + "Catologue Mang MBR -KOReD 03.2023_vps.pdf", "Catalogue màng MBR KOReD (03/2023)", G_REF, [NW]),
    (MB + "Email xác nhận của P.KTTB_vps.pdf", "Thay màng MBR – email xác nhận P.KTTB", G_INC, [NW]),
    (MB + "GETECH_ LG MBR _ NM DAM PHU MY 03012020_vps.pdf", "Chào giá màng MBR LG (Getech, 01/2020)", G_REF, [NW]),
    (MB + "Kubota_SMU_E_vps.pdf", "Catalogue màng Kubota SMU", G_REF, [NW]),
    (MB + "Phụ lục 1 Bảng so sánh thông số kỹ thuật màng lọc MBR_vps.pdf", "Thay màng MBR – so sánh thông số kỹ thuật các loại màng", G_INC, [NW]),
    (MB + "Phụ lục 2 Bảng so sánh giá_vps.pdf", "Thay màng MBR – so sánh giá", G_INC, [NW]),
    ("STVB127286_BM 08A-DGRR KTCN De xuat thu nghiem su dung NSX tuong duong cho he thong MBR HT XLNT moi_vps.pdf",
     "Đề xuất thử nghiệm màng MBR nhà sản xuất tương đương (BM 08A)", G_INC, [NW]),
    ("STVB127286_BM10 - De xuat thu nghiem su dung NSX tuong duong cho he thong MBR HT XLNT moi_vps.pdf",
     "Đề xuất thử nghiệm màng MBR nhà sản xuất tương đương (BM 10)", G_INC, [NW]),
    # Sân phơi bùn (giảm thể tích bùn)
    (GT + "Ban ve hoan cong - San phoi bun.pdf", "Bản vẽ hoàn công sân phơi bùn TK-202A/B", G_SYS, [NW]),
    (GT + "BAO CAO KINH TE KY THUAT_San phoi bun.docx", "Báo cáo kinh tế – kỹ thuật sân phơi bùn", G_REF, [NW]),
    (GT + "Bao cao rev 3.doc", "Báo cáo giảm thể tích bùn (rev 3)", G_REF, [NW]),
    (GT + "Copy of Giảm thể tích bùn.doc", "Giảm thể tích bùn (bản thảo)", G_REF, [NW]),
    (GT + "QD ban hanh van ban Quy trinh du bao va lap KH K-001.pdf", "Quyết định ban hành quy trình dự báo & lập kế hoạch K-001", G_REF, [NW]),
    ("TTr phe duyet ve BC Danh gia hieu qua van hanh lan dau cua SPB.pdf", "Tờ trình đánh giá hiệu quả vận hành lần đầu sân phơi bùn", G_INC, [NW]),
    # Nguồn thải, kiểm soát đầu vào
    ("STVB99072_G2-00-PA-174-L3 Phuong an kiem soat nguon xa thai vao he thong nuoc nhiem dau_vps.pdf",
     "Phương án kiểm soát nguồn xả thải vào hệ thống nước nhiễm dầu G2-00-PA-174 (lần 3, 12/2023)", G_OM, [OW, NW]),
    (KS + "G2-00-PA-xxx-Kiem soat xa thai vao HT nuoc nhiem dau.docx", "Phương án kiểm soát xả thải vào hệ thống nước nhiễm dầu (bản thảo 2014)", G_OM, [OW]),
    (KS + "Phụ lục 1_Thong ke cac diem thai.xlsx", "Thống kê các điểm thải vào hệ thống nước nhiễm dầu", G_OM, [OW]),
    (KS + "So do cac diem thu gom NTND nha may.pdf", "Sơ đồ các điểm thu gom nước thải nhiễm dầu toàn nhà máy", G_SYS, [OW]),
    ("STVB126972_TTr ve phuong an xu ly nuoc thai nong do o nhiem cao cum UFC85_vps.pdf",
     "Tờ trình phương án xử lý nước thải ô nhiễm cao cụm UFC85 (08/2024)", G_INC, [NW]),
    ("DOMESTIC WASTEWATER COLLECTION SYSTEM.pdf", "Hệ thống thu gom nước thải sinh hoạt (bản vẽ)", G_SYS, [SW, NW]),
    (KS + "2098-10-DW-1452-05-7.pdf", "Bản vẽ hệ thống ngầm X.Amonia 2098-10-DW-1452-05", G_SYS, [OW]),
    (KS + "Ban ve underground lien quan/2098-10-DW-1452-04.pdf", "Bản vẽ hệ thống ngầm X.Amonia 2098-10-DW-1452-04", G_SYS, [OW]),
    (KS + "2098-20-DW-0053-01.pdf", "Bản vẽ X.Urê 2098-20-DW-0053-01", G_SYS, [OW]),
    (KS + "2098-20-DW-1452-01.pdf", "Bản vẽ hệ thống ngầm X.Urê 2098-20-DW-1452-01", G_SYS, [OW]),
    (KS + "2098-20-DW-1452-02.pdf", "Bản vẽ hệ thống ngầm X.Urê 2098-20-DW-1452-02", G_SYS, [OW]),
    (KS + "2098-20-DW-1452-04.pdf", "Bản vẽ hệ thống ngầm X.Urê 2098-20-DW-1452-04", G_SYS, [OW]),
    (KS + "2098-20-DW-1452-05.pdf", "Bản vẽ hệ thống ngầm X.Urê 2098-20-DW-1452-05", G_SYS, [OW]),
    (KS + "2098-20-DW-1452-07.pdf", "Bản vẽ hệ thống ngầm X.Urê 2098-20-DW-1452-07", G_SYS, [OW]),
    (KS + "2098-30-DW-1452-01.pdf", "Bản vẽ hệ thống ngầm X.Phụ trợ 2098-30-DW-1452-01", G_SYS, [OW]),
    (KS + "2098-30-DW-1452-02.pdf", "Bản vẽ hệ thống ngầm X.Phụ trợ 2098-30-DW-1452-02", G_SYS, [OW]),
    (KS + "2098-30-DW-1452-03.pdf", "Bản vẽ hệ thống ngầm X.Phụ trợ 2098-30-DW-1452-03", G_SYS, [OW]),
    (KS + "2098-30-DW-1452-05.pdf", "Bản vẽ hệ thống ngầm X.Phụ trợ 2098-30-DW-1452-05", G_SYS, [OW]),
    (KS + "2098-30-DW-1452-06.pdf", "Bản vẽ hệ thống ngầm X.Phụ trợ 2098-30-DW-1452-06", G_SYS, [OW]),
    (KS + "2098-30-DW-1452-07.pdf", "Bản vẽ hệ thống ngầm X.Phụ trợ 2098-30-DW-1452-07", G_SYS, [OW]),
    (KS + "2098-30-DW-1452-08.pdf", "Bản vẽ hệ thống ngầm X.Phụ trợ 2098-30-DW-1452-08", G_SYS, [OW]),
    (KS + "2098-45-DW-1452-01.pdf", "Bản vẽ hệ thống ngầm kho NH3 2098-45-DW-1452-01", G_SYS, [OW]),
    # Cải tạo 2016
    ("Revamp_WWT/Section 200. WWT/2539-42-PID-0031-01-03_0 Ties-in.pdf", "P&ID 2539-42-PID-0031-01 tờ 3 – điểm tie-in (revamp)", G_REV, [OW]),
    ("Revamp_WWT/Section 200. WWT/2539-42-PID-0031-03-01_0 Ties-in.pdf", "P&ID 2539-42-PID-0031-03 – điểm tie-in (revamp)", G_REV, [OW]),
    # Hợp đồng, quy chuẩn
    ("HD nuoc thai nam 2018.pdf", "Hợp đồng xử lý nước thải với KCN (2018)", G_ORD, ALL),
    ("PLHĐ XLNT 01 SỐ 169_CTY PB VÀ HC DK-NHÀ MÁY ĐẠM PM.pdf", "Phụ lục hợp đồng xử lý nước thải số 169", G_ORD, ALL),
    ("CV99560_24-923-IZICO-PM1_vps.pdf", "Công văn IZICO 24-923 về tiếp nhận nước thải", G_ORD, ALL),
    ("qcvn_40-2025_nuoc_thai_cong_nghiep..pdf", "QCVN 40:2025/BTNMT – quy chuẩn nước thải công nghiệp", G_REF, ALL),
    ("CV85771_Thu ngo001_vps_xư ly nươc thải.pdf", "Thư ngỏ Oceania Bros/Veolia – chương trình hóa chất (Depositrol BL6501) cho nước sông làm mát", G_REF, ["30-CT-3001", "30-BA-3001"]),
]

sizes = {}
for line in open(os.path.join(HERE, "listing.txt"), encoding="utf-8"):
    line = line.rstrip("\n")
    if line:
        p, b = line.rsplit("|", 1)
        sizes[p] = int(b)

docs, seen = [], set()
for p, t, g, tags in L:
    assert p in sizes, "không có trong listing: " + p
    seen.add(p)
    docs.append({"p": R + "/" + p, "t": t, "g": g, "tags": tags, "no": "", "src": "", "kb": 0})
miss = sorted(set(sizes) - seen)
if miss:
    print("chưa xếp:", *miss, sep="\n  ")
json.dump(docs, open(os.path.join(HERE, "docs.json"), "w"), ensure_ascii=False, indent=0)
json.dump([[R + "/" + p, s] for p, s in sizes.items()], open(os.path.join(HERE, "sizes.json"), "w"), ensure_ascii=False)
print(len(docs), "tài liệu xử lý nước thải")
