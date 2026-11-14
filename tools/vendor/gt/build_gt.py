#!/usr/bin/env python3
"""Danh mục "Vendor Data/10GT9001" (tuabin khí 10-GT-9001, Nuovo Pignone MS5001PA DLN, job 170.5540) -> docs.json + sizes.json.

Đầu vào:
  listing.txt     đường dẫn tương đối trong "10GT9001" | byte. Đã bỏ: bản sao "Volume VII_2  INST LIST_Alignment GTC-TB.pdf"
                  (trùng byte và ngày với "Volume VII_2  INST LIST.pdf"), Thumbs.db, file tạm ~$, ảnh TORQUE CONVERTER/New Image.JPG,
                  Them/Cover.ppt và Them/Frontsheet Revision.doc (trang bìa).
  sections.json   trang bắt đầu các mục của Volume I và II (tìm bằng OCR chân trang "Sect. N - P. x of y").
  split_sizes.json  kích thước các file đã tách.

Vol I, II là bản scan không bookmark; OneDrive không mở PDF tới trang, nên các mục được tách thành file riêng ở
"10GT9001/Tach theo muc/" (đã chép lên OneDrive). Tách lại:
    python3 build_gt.py <thư mục 10GT9001> <thư mục ra>
Các volume khác giữ nguyên cả cuốn (mục lục ở "Them/General Index.doc").
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
R = "10GT9001"
SPLIT = "Tach theo muc"

G_DS = "Data sheet & tài liệu chính"
G_DW = "Bản vẽ chế tạo"
G_OM = "Vận hành & bảo dưỡng"
G_INS = "Thiết bị đo & điều khiển"
G_EL = "Điện & tủ điều khiển"
G_SP = "Phụ tùng"
G_GEN = "Tổng quát, móng & lắp dựng"
G_SYS = "Hệ thống (P&ID, mô tả công nghệ)"
G_INC = "Sự cố & trao đổi"
G_REF = "Tài liệu tham khảo"
G_BOOK = "Bộ sách đầy đủ"

GT = "10-GT-9001"
HXL = GT + "/HXL-2"
NP = "Nuovo Pignone MS5001PA DLN · job 170.5540"

# group of each split section: [volume tag][section number] -> group (default by volume)
SEC_G = {"Vol I": {0: G_BOOK, 1: G_DS, 14: G_OM, 15: G_OM}, "Vol II": {0: G_BOOK}}
SEC_TAGS = {("Vol I", 9): [GT, HXL]}

L = [
    # Bộ sách Nuovo Pignone (job 170.5540)
    ("Volume I    Turb Desc Op.pdf", "Vol I – Mô tả & vận hành tuabin khí (cả cuốn)", G_BOOK, [GT, HXL]),
    ("Volume II   Maintenance.pdf", "Vol II – Bảo dưỡng tuabin khí (cả cuốn)", G_BOOK, [GT]),
    ("Volume III  Parts.pdf", "Vol III – Danh mục chi tiết, phụ tùng (parts breakdown)", G_SP, [GT]),
    ("Volume IV   Aux Equipment Vendor.pdf", "Vol IV tome 1 – Tài liệu nhà cung cấp thiết bị phụ: bảng đồng hồ tại chỗ, dầu bôi trơn, dầu điều khiển, thủy lực & ratchet, quạt mát dầu, tách hơi dầu, khí nhiên liệu, cụm khí nhiên liệu DLN (mục 1–8)", G_DS, [GT, HXL]),
    ("Volume IV tome 2 of 4.pdf", "Vol IV tome 2 – Tài liệu nhà cung cấp thiết bị phụ (tiếp)", G_DS, [GT]),
    ("Volume IV tome 3 of 4.pdf", "Vol IV tome 3 – Tài liệu nhà cung cấp thiết bị phụ (tiếp)", G_DS, [GT]),
    ("Volume IV tome 4 of 4.pdf", "Vol IV tome 4 – Hệ thống lọc gió đầu vào 3 cấp (AAF) & hệ thống thông gió", G_DS, [GT]),
    ("Volume V   UCS 1 modbus.pdf", "Vol V tome 1 – Hệ thống điều khiển: tủ Promel, Speedtronic Mark VI TMR (GEH-6421), Modbus", G_INS, [GT]),
    ("Volume V   UCS 2.pdf", "Vol V tome 2 – Hệ thống điều khiển: phần mềm & phần cứng HMI (Advantech)", G_INS, [GT]),
    ("Volume V   UCS 3.pdf", "Vol V tome 3 – Hệ thống phát hiện cháy khí & giám sát rung/nhiệt Bently Nevada 3500", G_INS, [GT]),
    ("Volume V   UCS 4.pdf", "Vol V tome 4 – In chương trình PLC & trang màn hình HMI", G_INS, [GT]),
    ("Volume VI tome 1 of 2.pdf", "Vol VI tome 1 – Máy phát điện xoay chiều Brush: hướng dẫn, lắp ráp, data sheet, bản vẽ, biên bản thử", G_EL, [GT]),
    ("Volume VI tome 2 of 2.pdf", "Vol VI tome 2 – Máy phát: tài liệu nhà cung cấp (ổ trượt, hộp số, kích từ, cảm biến…) & tủ điều khiển – bảo vệ chính", G_EL, [GT]),
    ("Volume VII_1.pdf", "Vol VII tome 1 – Bản vẽ tổng thể, kết cấu & mặt cắt tuabin khí và thiết bị phụ (mục 1–2)", G_DW, [GT, HXL]),
    ("Volume VII_2  INST LIST.pdf", "Vol VII tome 2 – Móng, sơ đồ nguyên lý & danh mục thiết bị đo, sơ đồ đấu nối, tiêu chuẩn kỹ thuật (mục 3–6)", G_INS, [GT, HXL]),
    ("Volume VII_3  barrier.pdf", "Vol VII tome 3 – Bản vẽ máy phát & tủ điều khiển – bảo vệ máy phát (mục 7–8)", G_EL, [GT]),
    ("Volume VII_4.pdf", "Vol VII tome 4 – Kế hoạch kiểm soát chất lượng (QCP) & data sheet (mục 9–10)", G_DS, [GT]),
    ("Volume VIII.pdf", "Vol VIII – Dụng cụ chuyên dùng (tiêu chuẩn, DLN, căn chỉnh rotor & hộp số, tháo liner)", G_SP, [GT]),
    ("Volume IX Vent Sys.pdf", "Vol IX – Vỏ cách âm, cầu trục, hệ thống thông gió & hút gió", G_GEN, [GT]),
    ("Volume X.pdf", "Vol X – Tủ MCC (ABB): hướng dẫn & bản vẽ", G_EL, [GT]),
    ("Volume XI.pdf", "Vol XI – Ắc quy FIAMM, UPS CEG, hệ khởi động diesel & tủ nạp ắc quy", G_EL, [GT]),
    ("Volume XII.pdf", "Vol XII – Cabin điều khiển (điều hòa, thông gió phòng ắc quy, phát hiện cháy)", G_EL, [GT]),
    ("Them/General Index.doc", "Mục lục tổng bộ sách (Vol 0 – XII)", G_BOOK, [GT]),
    ("Them/Vol. II  Maintenance/Index.doc", "Vol II – mục lục (bản Word)", G_BOOK, [GT]),
    ("Them/Vol. II  Maintenance/Sect_3.doc", "Vol II mục 3 – Tiêu chí bảo dưỡng (bản Word)", G_OM, [GT]),
    ("Them/Vol. II  Maintenance/Sect_5.doc", "Vol II mục 5 – Kiểm tra buồng đốt (bản Word)", G_OM, [GT]),
    ("Them/Vol. IV Auxialiary Equipment/Aux_index.doc", "Vol IV – bảng thiết bị phụ, nhà sản xuất & tag khách hàng (bản Word)", G_INS, [GT, HXL]),
    ("Them/Vol. IV Auxialiary Equipment/ABB.pdf", "Vol IV – Motor ABB (bơm dầu phụ 88QA…)", G_DS, [GT]),
    ("Them/Vol. IV Auxialiary Equipment/ARIS CHIAPPA.pdf", "Vol IV – Bơm dầu phụ & bơm dầu sự cố Aris Chiappa CVTG65/250", G_DS, [GT]),
    ("Them/Vol. IV Auxialiary Equipment/SICME MOTORI.pdf", "Vol IV – Motor DC SICME (bơm dầu sự cố 88QE)", G_DS, [GT]),
    ("Them/FILTER HOUSE/VFR 01154.pdf", "Nhà lọc gió đầu vào (VFR 01154)", G_DS, [GT]),
    # Hệ truyền động, khởi động (sửa chữa 2015)
    ("Voith Torque Converter.pdf", "Bộ biến mô thủy lực Voith (khởi động)", G_DS, [GT]),
    ("TORQUE CONVERTER/Manual_213214.pdf", "Bộ biến mô Voith – hướng dẫn vận hành & bảo dưỡng (213214)", G_OM, [GT]),
    ("TORQUE CONVERTER/SQ14284 Petrovietnam E7WAT.PDF", "Bộ biến mô Voith E7WAT – báo giá sửa chữa SQ14284", G_INC, [GT]),
    ("TORQUE CONVERTER/SQ14299 Petrovietnam E7WAT Spare Parts.pdf", "Bộ biến mô Voith E7WAT – báo giá phụ tùng SQ14299", G_SP, [GT]),
    ("TORQUE CONVERTER/SMQ10343 Petrovietnam Service Rate_Daily.pdf", "Voith – đơn giá dịch vụ theo ngày SMQ10343", G_INC, [GT]),
    ("TORQUE CONVERTER/Voith GTC Version Singapore 2014-10.pdf", "Voith – điều kiện thương mại (Singapore 10/2014)", G_INC, [GT]),
    ("SSS MAIN CLUTCH/IB.71710.pdf", "Ly hợp chính SSS – hướng dẫn IB.71710", G_OM, [GT]),
    ("SSS MAIN CLUTCH/17737.pdf", "Ly hợp chính SSS – bản vẽ 17737", G_DW, [GT]),
    ("SSS MAIN CLUTCH/Parts list 17737.pdf", "Ly hợp chính SSS – danh mục phụ tùng 17737", G_SP, [GT]),
    ("Gearbox BHS.PDF", "Hộp số BHS", G_DS, [GT]),
    ("Auxilary Coupling.pdf", "Khớp nối phụ (auxiliary coupling)", G_DW, [GT]),
    ("SOM6600967_001_A coupling assembly.pdf", "Lắp ráp khớp nối SOM6600967", G_DW, [GT]),
    ("TRAIN TORSIONAL ANALYSIS.pdf", "Phân tích dao động xoắn trục máy (train torsional analysis)", G_DS, [GT]),
    ("Compbell Diagram for 1705540.pdf", "Biểu đồ Campbell (job 170.5540)", G_DS, [GT]),
    ("Can tam may phat - hop so.pdf", "Căn tâm máy phát – hộp số", G_OM, [GT]),
    # Tài liệu khác
    ("PID GT9001.pdf", "P&ID cụm tuabin khí của nhà cung cấp (19 tờ)", G_SYS, [GT, HXL]),
    ("STVB114768_G5-30-MĐB-064 TECHNICAL REQUIREMENT FOR REFURBISHING PARTS OF 10-GTG-9001_vps.pdf", "Yêu cầu kỹ thuật phục hồi chi tiết 10-GTG-9001 (G5-30-MĐB-064)", G_OM, [GT]),
    ("6421C Vol I System Manual For Mark VI.pdf", "Speedtronic Mark VI – System manual GEH-6421C tập I", G_INS, [GT]),
    ("6421C Vol II System Manual For Mark VI.pdf", "Speedtronic Mark VI – System manual GEH-6421C tập II", G_INS, [GT]),
    ("GEH-6421F_Vol II.pdf", "Speedtronic Mark VI – System guide GEH-6421F tập II", G_INS, [GT]),
    ("Multicustomer'06/00_MCT_HEAVY_DUTY_GAS_TURBINE_NOV.06.pdf", "Khóa đào tạo GE Multicustomer 2006 – tuabin khí heavy duty (trọn bộ)", G_REF, [GT]),
    ("Multicustomer'06/01_INSTALLATION LAYOUT .pdf", "Đào tạo GE 2006 – 01 Bố trí lắp đặt", G_REF, [GT]),
    ("Multicustomer'06/02_THERMODYNAMICS .pdf", "Đào tạo GE 2006 – 02 Nhiệt động học", G_REF, [GT]),
    ("Multicustomer'06/03a_GE10_2_TURBINE CONSTRUCTION .pdf", "Đào tạo GE 2006 – 03a Kết cấu tuabin GE10-2", G_REF, [GT]),
    ("Multicustomer'06/03b_MS5001_TURBINE CONSTRUCTION .pdf", "Đào tạo GE 2006 – 03b Kết cấu tuabin MS5001", G_REF, [GT]),
    ("Multicustomer'06/03c_MS5002_TURBINE CONSTRUCTION .pdf", "Đào tạo GE 2006 – 03c Kết cấu tuabin MS5002", G_REF, [GT]),
    ("Multicustomer'06/03d_MS7001EA CONSTRUCTION .pdf", "Đào tạo GE 2006 – 03d Kết cấu tuabin MS7001EA", G_REF, [GT]),
    ("Multicustomer'06/04_AUXILIARY SYSTEM _1.pdf", "Đào tạo GE 2006 – 04 Hệ thống phụ trợ (1)", G_REF, [GT]),
    ("Multicustomer'06/04a_AUXILIARY SYSTEM _2.pdf", "Đào tạo GE 2006 – 04a Hệ thống phụ trợ (2)", G_REF, [GT]),
    ("Multicustomer'06/05_CONTROL AND PROTECTION SYSTEM .pdf", "Đào tạo GE 2006 – 05 Điều khiển & bảo vệ", G_REF, [GT]),
    ("Multicustomer'06/06_TURBINE PERFORMANCE CURVES .pdf", "Đào tạo GE 2006 – 06 Đường đặc tính tuabin", G_REF, [GT]),
    ("Multicustomer'06/07_TURBINE ASSEMBLY .pdf", "Đào tạo GE 2006 – 07 Lắp ráp tuabin", G_REF, [GT]),
    ("Multicustomer'06/08_maintenance .pdf", "Đào tạo GE 2006 – 08 Bảo dưỡng", G_REF, [GT]),
    ("Multicustomer'06/09_troubleshooting .pdf", "Đào tạo GE 2006 – 09 Xử lý sự cố", G_REF, [GT]),
    ("2140. (ME-51043) GAS TURBINE THEORY BY HIH SARAVANAMUTTOO, H. COHEN & GFC ROGERS.pdf", "Sách: Gas Turbine Theory (Saravanamuttoo, Cohen, Rogers)", G_REF, [GT]),
    ("634. Advanced Gas Turbine Cycles.pdf", "Sách: Advanced Gas Turbine Cycles", G_REF, [GT]),
    ("1248. A Textbook of Fluid Mechanics and Hydraulic Machines.pdf", "Sách: A Textbook of Fluid Mechanics and Hydraulic Machines", G_REF, [GT]),
]


def split_names():
    S = json.load(open(os.path.join(HERE, "sections.json")))
    out = []
    for book, v in S.items():
        s = v["s"]
        for i, (no, p0, t) in enumerate(s):
            p1 = (s[i + 1][1] - 1) if i + 1 < len(s) else v["n"]
            name = f'{v["tag"]} - {no:02d} {t}.pdf'.replace("/", "-")
            out.append((book, v["tag"], no, t, p0, p1, name))
    return out


if len(sys.argv) == 3:  # tách lại
    src, dst = sys.argv[1:]
    os.makedirs(dst, exist_ok=True)
    for book, vt, no, t, p0, p1, name in split_names():
        subprocess.run(["qpdf", "--empty", "--pages", os.path.join(src, book), f"{p0}-{p1}", "--", os.path.join(dst, name)], check=True)

sizes = {}
for line in open(os.path.join(HERE, "listing.txt"), encoding="utf-8"):
    line = line.rstrip("\n")
    if line:
        p, b = line.rsplit("|", 1)
        sizes[p] = int(b)
ssz = json.load(open(os.path.join(HERE, "split_sizes.json")))

docs, seen = [], set()
for book, vt, no, t, p0, p1, name in split_names():
    p = SPLIT + "/" + name
    sizes[p] = ssz[name]
    g = SEC_G.get(vt, {}).get(no, G_OM if vt == "Vol II" else G_SYS)
    docs.append({"p": R + "/" + p, "t": f"{vt} mục {no} – {t}" if no else f"{vt} – {t}", "g": g,
                 "tags": SEC_TAGS.get((vt, no), [GT]), "no": "", "src": NP, "kb": 0, "bp": R + "/" + book, "bpg": p0})
    seen.add(p)
for p, t, g, tags in L:
    assert p in sizes, "không có trong listing: " + p
    seen.add(p)
    np_ = p.startswith("Volume") or p.startswith("Them/")
    docs.append({"p": R + "/" + p, "t": t, "g": g, "tags": tags, "no": "", "src": NP if np_ else "", "kb": 0})
miss = sorted(set(sizes) - seen)
if miss:
    print("chưa xếp:", *miss, sep="\n  ")
json.dump(docs, open(os.path.join(HERE, "docs.json"), "w"), ensure_ascii=False, indent=0)
json.dump([[R + "/" + p, s] for p, s in sizes.items()], open(os.path.join(HERE, "sizes.json"), "w"), ensure_ascii=False)
print(len(docs), "tài liệu tuabin khí 10-GT-9001")
