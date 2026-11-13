#!/usr/bin/env python3
"""Danh mục "Vendor Data/8. Hệ thống Nito" (cụm sản xuất nitơ 30-PK-6001, Linde GAN, MR 4112-50) -> docs.json + sizes.json.

Đầu vào: listing.txt (đường dẫn tương đối trong "8. Hệ thống Nito" | byte). Đã bỏ:
  - thư mục "18. 30-PK-6001 (MR-4112-50)" (bản sao của "30-PK-6001 (MR-4112-50) Nitrogen", thiếu thư mục PDF files),
  - ảnh/video ("2021-Dai tu HT N2", z*.jpg), Thumbs.db, thư mục Security (file khóa phần mềm), .dwg, plot.log, chiller.png,
  - các file "... - Copy".
Tài liệu đã là file riêng theo mục nên không cần tách sách.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
R = "8. Hệ thống Nito"
V = "30-PK-6001 (MR-4112-50) Nitrogen/"
V1 = V + "Vol 1 O&M/"
V3 = V + "Vol 3 Inst/"
BD = "Nitrogen BD 2011/"

G_DS = "Data sheet & tài liệu chính"
G_DW = "Bản vẽ chế tạo"
G_OM = "Vận hành & bảo dưỡng"
G_INS = "Thiết bị đo & điều khiển"
G_EL = "Điện & tủ điều khiển"
G_SP = "Phụ tùng"
G_TEST = "Chạy thử"
G_GEN = "Tổng quát, móng & lắp dựng"
G_SYS = "Hệ thống (P&ID, mô tả công nghệ)"
G_INC = "Sự cố & trao đổi"
G_REF = "Tài liệu tham khảo"
G_BOOK = "Bộ sách đầy đủ"

PK = "30-PK-6001"
CHILL = [PK + "/ACC1", PK + "/E5", PK + "/E6"]          # cụm làm lạnh khí đầu vào (chiller + 2 trao đổi nhiệt)
TSA = [PK + "/DR1", PK + "/V2", PK + "/V3"]             # cụm làm sạch không khí (2 bình hấp phụ)
COLD = [PK + "/E3", PK + "/T1", PK + "/V4", PK + "/E4"]  # cold box
TURB = [PK + "/EK1", PK + "/ABC1"]                       # tuabin giãn nở + quạt làm mát
VAP = [PK + "/TK1", PK + "/E1A", PK + "/E1B", PK + "/E2A", PK + "/E2B"]  # bồn LIN + thiết bị bay hơi
SRC = "Linde CryoPlants · GAN 600 · MR 4112-50"

L = [
    # Vol 1 – Operating & Maintenance (Linde)
    (V1 + "Customer front sht.pdf", "Vol 1 O&M – bìa", G_BOOK, [PK]),
    (V1 + "Index.doc", "Vol 1 O&M – mục lục", G_BOOK, [PK]),
    (V1 + "Section frontsheets.doc", "Vol 1 O&M – trang bìa các mục", G_BOOK, [PK]),
    (V1 + "Sect 1/S1.doc", "Mục 1 – Giới thiệu, danh mục các tập tài liệu", G_GEN, [PK]),
    (V1 + "Sect 2/S2.doc", "Mục 2 – An toàn (lưu chất lạnh sâu, thiếu oxy, cháy nổ…); HMI & hướng dẫn vận hành", G_OM, [PK]),
    (V1 + "Sect 3/S3 Equip Dsheets.pdf", "Mục 3 – Data sheet thiết bị", G_DS, [PK] + CHILL + TSA + COLD + TURB + VAP),
    (V1 + "Sect 3/S3 Vendor list.pdf", "Mục 3 – Danh sách nhà cung cấp thiết bị", G_DS, [PK]),
    (V1 + "Sect 4/S4 Std & Symbols 2098-00 PID-0021-01-1b Key .pdf", "Mục 4 – Ký hiệu P&ID (2098-00-PID-0021-01)", G_SYS, [PK]),
    (V1 + "Sect 4/Sect 4 Process Description.doc", "Mục 4 – Mô tả công nghệ (Process description)", G_SYS, [PK]),
    (V1 + "Sect 5/S5 Plant Operation.doc", "Mục 5 – Vận hành cụm (trang bìa)", G_OM, [PK]),
    (V1 + "Sect 6/S6 Maint Schedule.doc", "Mục 6 – Lịch bảo dưỡng định kỳ", G_OM, [PK]),
    (V1 + "Sect 6/S6 OPM 097 Safety checks.DOC", "Mục 6 – Kiểm tra an toàn định kỳ (OPM 097)", G_OM, [PK]),
    (V1 + "Sect 6/S6 Routine Maint note.doc", "Mục 6 – Ghi chú bảo dưỡng thường xuyên", G_OM, [PK]),
    (V1 + "Sect 7/S7 Setpoints.doc", "Mục 7 – Giá trị cài đặt chạy thử (trang bìa)", G_INS, [PK]),
    (V1 + "Sect 8/S8 Safety Inst for fitment of spares (OPM 089).doc", "Mục 8 – Hướng dẫn an toàn khi thay phụ tùng (OPM 089)", G_SP, [PK]),
    (V1 + "Sect 8/S8 Spares ordering proc (OPM 103).DOC", "Mục 8 – Thủ tục đặt phụ tùng (OPM 103)", G_SP, [PK]),
    (V1 + "Sect 8/Spares list/Air Cooled Chiller Module  Package-1.DOC", "Phụ tùng – cụm chiller giải nhiệt gió (1/2)", G_SP, CHILL),
    (V1 + "Sect 8/Spares list/Air Cooled Chiller Module-2.DOC", "Phụ tùng – cụm chiller giải nhiệt gió (2/2)", G_SP, CHILL),
    (V1 + "Sect 8/Spares list/Chiller, Refigeration Drier System 1.DOC", "Phụ tùng – hệ làm lạnh & tách ẩm khí vào (1/3)", G_SP, CHILL + [PK + "/V1"]),
    (V1 + "Sect 8/Spares list/Chiller, Refigeration Drier System 2.DOC", "Phụ tùng – hệ làm lạnh & tách ẩm khí vào (2/3)", G_SP, CHILL + [PK + "/V1"]),
    (V1 + "Sect 8/Spares list/Chiller, Refigeration Drier System 3.DOC", "Phụ tùng – hệ làm lạnh & tách ẩm khí vào (3/3)", G_SP, CHILL + [PK + "/V1"]),
    (V1 + "Sect 8/Spares list/TSA1.doc", "Phụ tùng – cụm hấp phụ TSA (1/3)", G_SP, TSA),
    (V1 + "Sect 8/Spares list/TSA2.doc", "Phụ tùng – cụm hấp phụ TSA (2/3)", G_SP, TSA),
    (V1 + "Sect 8/Spares list/TSA3.doc", "Phụ tùng – cụm hấp phụ TSA (3/3)", G_SP, TSA),
    (V1 + "Sect 8/Spares list/TSAControl.doc", "Phụ tùng – điều khiển cụm TSA", G_SP, TSA),
    (V1 + "Sect 8/Spares list/Coldbox 1.doc", "Phụ tùng – cold box (1/3)", G_SP, COLD + TURB),
    (V1 + "Sect 8/Spares list/Coldbox 2.doc", "Phụ tùng – cold box (2/3)", G_SP, COLD + TURB),
    (V1 + "Sect 8/Spares list/Coldbox 3.doc", "Phụ tùng – cold box (3/3)", G_SP, COLD + TURB),
    (V1 + "Sect 8/Spares list/Buffer-GasControl1.DOC", "Phụ tùng – điều khiển khí đệm/khí bổ sung (1/2)", G_SP, VAP),
    (V1 + "Sect 8/Spares list/Buffer-GasControl2.DOC", "Phụ tùng – điều khiển khí đệm/khí bổ sung (2/2)", G_SP, VAP),
    (V1 + "Sect 9&10.doc", "Mục 9 & 10 – không sử dụng", G_BOOK, [PK]),
    # Vol 3 – Installation
    (V3 + "Inst Man Cust front sht.pdf", "Vol 3 Lắp đặt – bìa", G_BOOK, [PK]),
    (V3 + "VOL3-Index.doc", "Vol 3 Lắp đặt – mục lục", G_BOOK, [PK]),
    (V3 + "V3-Sect Frontshts.doc", "Vol 3 Lắp đặt – trang bìa các mục", G_BOOK, [PK]),
    (V3 + "Sect 1/V3s1 Amended by CEM.DOC", "Vol 3 Mục 1 – Giới thiệu lắp đặt", G_GEN, [PK]),
    (V3 + "Sect 2/S4 Std & Symbols 2098-00 PID-0021-01-1b Key .pdf", "Vol 3 Mục 2 – Ký hiệu P&ID (2098-00-PID-0021-01)", G_SYS, [PK]),
    (V3 + "Sect 3/V3s3 Amended by CEM.DOC", "Vol 3 Mục 3 – Vận chuyển, nâng hạ, định vị thiết bị", G_GEN, [PK]),
    (V3 + "Sect 3/Site powder filling.pdf", "Vol 3 Mục 3 – Nạp bột cách nhiệt perlite cold box tại công trường", G_GEN, COLD),
    (V3 + "Sect 4/V3s4 Amended by CEM.DOC", "Vol 3 Mục 4 – Lắp đặt cơ khí", G_GEN, [PK]),
    (V3 + "Sect 4/Vap Inst 3-107.003.300 .pdf", "Vol 3 Mục 4 – Lắp đặt cụm bay hơi (3-107.003.300)", G_DW, VAP),
    (V3 + "Sect 4/Folder of Inst Drgs/Inst Drgs.pdf", "Vol 3 Mục 4 – Bản vẽ lắp đặt", G_DW, [PK]),
    (V3 + "Sect 4/Folder of ISO's/ISO's.pdf", "Vol 3 Mục 4 – Bản vẽ isometric đường ống", G_DW, [PK]),
    (V3 + "Sect 5/LS drg schedule.pdf", "Vol 3 Mục 5 – Danh mục sơ đồ đấu dây (LS)", G_EL, [PK]),
    (V3 + "Sect 5/LS 1-20 of 39.pdf", "Vol 3 Mục 5 – Sơ đồ đấu dây LS 1–20", G_EL, [PK]),
    (V3 + "Sect 5/LS 21-39 of 39.pdf", "Vol 3 Mục 5 – Sơ đồ đấu dây LS 21–39", G_EL, [PK]),
    (V3 + "Sect 6/Mech Testing.pdf", "Vol 3 Mục 6 – Thử nghiệm cơ khí", G_TEST, [PK]),
    (V3 + "Sect 7/Elec Testing.pdf", "Vol 3 Mục 7 – Thử nghiệm điện", G_TEST, [PK]),
    (V3 + "Sect 8/Linde Specs.pdf", "Vol 3 Mục 8 – Tiêu chuẩn kỹ thuật Linde", G_GEN, [PK]),
    # Điện – điều khiển
    (V + "PDF files/7829_0 Control Loops.pdf", "Sơ đồ vòng điều khiển (control loops)", G_INS, [PK]),
    (V + "PDF files/7829_0 Electrical Block Diagram.pdf", "Sơ đồ khối điện", G_EL, [PK]),
    (V + "PDF files/7829_0 Panel Layout Drawings.pdf", "Bản vẽ bố trí tủ điều khiển", G_EL, [PK]),
    (V + "PDF files/7829_3 System Wiring Diagrams.pdf", "Sơ đồ đấu dây hệ thống", G_EL, [PK]),
    (V + "PDF files/7829_6 Instrument List.pdf", "Danh mục thiết bị đo", G_INS, [PK]),
    (V + "PDF files/Hamrin TSA Diagrams.pdf", "Sơ đồ cụm hấp phụ TSA (Hamrin)", G_DW, TSA),
    (V + "PDF files/Setpoints2.pdf", "Danh sách giá trị cài đặt (van, analyser, bộ điều áp)", G_INS, [PK]),
    (V + "PDF files/SMS01_2005.pdf", "Chương trình/cấu hình điều khiển SMS01 (2005)", G_INS, [PK]),
    (V + "Chiller.pdf", "Tài liệu chiller giải nhiệt gió", G_DS, CHILL),
    # Bộ tài liệu đào tạo 2011
    (BD + "0-107.003.110 Sht 1 iss 6 Flowsheet.pdf", "Lưu đồ công nghệ 0-107.003.110 tờ 1 (rev 6)", G_SYS, [PK]),
    (BD + "0-107.003.110 Sht 2 iss 6 Flowsheet.pdf", "Lưu đồ công nghệ 0-107.003.110 tờ 2 (rev 6)", G_SYS, [PK]),
    (BD + "0-107.003.110 Sht 3 iss 6 Flowsheet.pdf", "Lưu đồ công nghệ 0-107.003.110 tờ 3 (rev 6)", G_SYS, [PK]),
    (BD + "116SAMa.doc", "Hướng dẫn vận hành cụm (Plant operating instructions GAN 600)", G_OM, [PK]),
    (BD + "OPM114-SAM.doc", "Hướng dẫn màn hình điều khiển HMI (OPM 114)", G_OM, [PK]),
    (BD + "Setpoints.doc", "Danh sách giá trị cài đặt (set point list GAN 600)", G_INS, [PK]),
    (BD + "Maint Schedule iss 3.doc", "Lịch bảo dưỡng (rev 3)", G_OM, [PK]),
    (BD + "Process calculation Phu My7829  240+30.doc", "Tính toán công nghệ (240 Nm³/h khí + 31 Nm³/h lỏng)", G_DS, [PK]),
    (BD + "Process Training Vietnam.ppt", "Đào tạo công nghệ (Linde, 2011)", G_REF, [PK]),
    (BD + "GAN Operator Training Vietnam.ppt", "Đào tạo vận hành (Linde, 2011)", G_REF, [PK]),
    (BD + "GAN Maintenance Training Vietnam.ppt", "Đào tạo bảo dưỡng (Linde, 2011)", G_REF, [PK]),
    (BD + "Safety Training Vietnam.ppt", "Đào tạo an toàn (Linde, 2011)", G_REF, [PK]),
    # Tài liệu của nhà máy
    ("a30-QT-01-006_QTVH CỤM SẢN XUẤT NITƠ ok.doc", "Quy trình vận hành hệ thống sản xuất nitơ G2-30-QT-01-006", G_OM, [PK]),
    ("Process Training Vietnam done.docx", "Tài liệu đào tạo công nghệ (bản dịch tiếng Việt)", G_REF, [PK]),
    ("PID Nito Vendor.pdf", "P&ID cụm nitơ của nhà cung cấp", G_SYS, [PK]),
    ("nito word ngày 04-12-2016.pdf", "Màn hình điều khiển & giá trị cài đặt (04/12/2016)", G_INS, [PK]),
    ("G2-00-HD-118 HD kiểm soát tiêu hao Nitơ.pdf", "Hướng dẫn kiểm soát tiêu hao nitơ G2-00-HD-118", G_OM, [PK]),
    ("STVB134898_KHBD_N2_ 2024_ban hanh da bo cac hang muc TDH da co KHBD trong T10 (1)_vps.pdf", "Kế hoạch bảo dưỡng cụm N2 năm 2024", G_OM, [PK]),
    ("HỘI THẢO TRAO ĐỔI KINH NGHIỆM KHI GS ĐẠI TU 30-PK-6001.pdf", "Hội thảo kinh nghiệm giám sát đại tu 30-PK-6001", G_INC, [PK]),
    ("Bao cáo nito.docx", "Báo cáo tình hình hệ thống N2 (09–18/09/2010)", G_INC, [PK]),
    ("Su co Nito.xlsx", "Thống kê sự cố hệ thống sản xuất nitơ 2009–2010", G_INC, [PK]),
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
    docs.append({"p": R + "/" + p, "t": t, "g": g, "tags": tags, "no": "", "src": SRC if p.startswith(V) or p.startswith(BD) else "", "kb": 0})
miss = sorted(set(sizes) - seen)
if miss:
    print("chưa xếp:", *miss, sep="\n  ")
json.dump(docs, open(os.path.join(HERE, "docs.json"), "w"), ensure_ascii=False, indent=0)
json.dump([[R + "/" + p, s] for p, s in sizes.items()], open(os.path.join(HERE, "sizes.json"), "w"), ensure_ascii=False)
print(len(docs), "tài liệu hệ thống nitơ")
