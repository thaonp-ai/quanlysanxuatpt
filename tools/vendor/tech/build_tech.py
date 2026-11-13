#!/usr/bin/env python3
"""Nội dung "Công nghệ" (mô tả công nghệ trích từ tài liệu vendor + PFD) -> web/data/tech.json.

Cấu trúc:
  units{mã Unit: {t, intro, s:[mục]}}   – trang tổng quan cả Unit
  tags{mã: {t, intro, s:[mục]}}         – đoạn công nghệ cho thiết bị; web tìm theo tag đầy đủ,
                                          bỏ chữ cuối (A/B/C), bỏ "M" của motor (/MP1A -> /P1), phần trước "/"
  mục = {h: tiêu đề, p:[đoạn], ul:[gạch đầu dòng], kv:[[thông số, giá trị]], tb:[[hàng tiêu đề], [hàng]...]}
  src = [[đường dẫn trong Vendor Data | "sheet:<dwg>", nhãn]]  – web tạo link mở tài liệu / bản vẽ
Nội dung viết tay từ: 30-PK-2001 Vendor Data Book (Chemitreat, MR 0230-50: 2.1, 2.2, 4, 5, 9.1.x, 9.3),
data sheet & biên bản thử bơm Flowserve (MR 0910-52), PFD 2539-32-PFD-0010-01-01 (as-built 08/03/2018).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "..", "web", "data", "tech.json")
V = "9. Raw-Pot-Fire/"
PK = V + "30-PK-2001 (MR-0230-50)/Potable - Vol 1 of 3/"
SA = PK + "Section A - Erection, Operating And Maintenance Instruction Manu/"
S_DESIGN = [SA + "Section 2/2.1 System Design Specification.pdf", "30-PK-2001 · 2.1 Thông số thiết kế"]
S_PROC = [SA + "Section 2/2.2 Process Description.pdf", "30-PK-2001 · 2.2 Mô tả công nghệ"]
S_MECH = [SA + "Section 4/4 - Mechanical Equipment Specification.pdf", "30-PK-2001 · 4 Thông số thiết bị"]
S_CHEM = [SA + "Section 5/5 - Chemicals And Utilities Consumption.pdf", "30-PK-2001 · 5 Tiêu hao hóa chất"]
S_ACF = [SA + "Section 9/9.1.1-Activated Carbon Filter.pdf", "30-PK-2001 · 9.1.1 Lọc than hoạt tính"]
S_DOSE = [SA + "Section 9/9.1.2 - Sodium Hypochlorite Dosing System.pdf", "30-PK-2001 · 9.1.2 Châm hypochlorite"]
S_MF = [SA + "Section 9/9.1.3 - Micro Filter.pdf", "30-PK-2001 · 9.1.3 Lọc tinh 1 µm"]
S_SEQ = [SA + "Section 9/9.2 - Sequence Flow Chart.pdf", "30-PK-2001 · 9.2 Lưu đồ trình tự"]
S_CTRL = [SA + "Section 9/9.3 - Process Control Write-up.pdf", "30-PK-2001 · 9.3 Điều khiển"]
S_ALM = [SA + "Section 9/9.4 List of Alarms.pdf", "30-PK-2001 · 9.4 Danh sách báo động"]
S_CE = [SA + "Section 9/9.6 - Cause & Effect.pdf", "30-PK-2001 · 9.6 Cause & Effect"]
S_PID = [PK + "Section B - Documents And Drawings/1.2 Process & Instrumentation Diagram-P&ID.pdf", "30-PK-2001 · P&ID cụm"]
S_BLOCK = [PK + "Section B - Documents And Drawings/1.3 - Block Diagram For Potable Water Plant.pdf", "30-PK-2001 · Sơ đồ khối"]
RAWB = V + "30-P-2002AB (MR-0910-52)/30-P-2001ABC (MR-0910-52)copy/Vendor Data Book - Raw Water Pumps/"
POTB = V + "30-P-2002AB (MR-0910-52)/Vendor Data Book - Portable Water Pumps/"
S_P1 = [RAWB + "Section 01 - Pump as Built Data.pdf", "Bơm 30-P-2001 · data sheet & biên bản thử"]
S_P1M = [RAWB + "Section 02 - I O Ms.pdf", "Bơm 30-P-2001 · IOM"]
S_P2 = [POTB + "Section 1 - Pump as Built Data.pdf", "Bơm 30-P-2002 · data sheet & biên bản thử"]
S_P2M = [POTB + "Section 2 - I O & Ms.pdf", "Bơm 30-P-2002 · IOM"]
S_PFD = ["sheet:2539-32-PFD-0010-01-01 (trang 1)", "PFD 2539-32-PFD-0010-01-01 (as-built)"]
S_PID1 = ["sheet:2098-32-PID-0031-01", "P&ID 2098-32-PID-0031-01 Raw water"]
S_PID2 = ["sheet:2098-32-PID-0031-02", "P&ID 2098-32-PID-0031-02 Potable water"]

unit32 = {
    "t": "Công nghệ Unit 32 – Nước thô & nước sinh hoạt",
    "intro": "Nước thô từ ranh giới nhà máy (B.L.) được chứa ở bồn 30-TK-2001 rồi bơm 30-P-2001A/B/C cấp đi các nơi: "
             "cụm khử khoáng (Demi, 30-PK-1001), header nước công nghệ, cụm xử lý nước sinh hoạt 30-PK-2001 và dự trữ nước cứu hỏa. "
             "Nước sinh hoạt được khử trùng bằng NaOCl, chứa ở bồn 30-TK-2002, sau đó bơm 30-P-2002A/B đẩy qua lọc than hoạt tính "
             "và lọc tinh 1 µm rồi cấp ra header nước sinh hoạt.",
    "s": [
        {"h": "Sơ đồ dòng (theo PFD as-built)",
         "ul": ["Nước thô từ B.L. (dòng 32.2) → bồn chứa nước thô 30-TK-2001 (7.155 m³).",
                "30-TK-2001 → bơm nước thô 30-P-2001A/B/C (dòng 32.8, 5,0 barg), sau đó chia đi: cụm Demi 30-PK-1001 (dòng 32.1), "
                "header nước thô/nước công nghệ cho hộ tiêu thụ (dòng 32.14), cụm xử lý nước sinh hoạt 30-PK-2001 (dòng 32.3), "
                "và hồi lưu về 30-TK-2001 (dòng 32.9) qua van điều khiển lưu lượng FIC-32002.",
                "Bồn 30-TK-2001 cũng là nguồn nước cho bơm cứu hỏa 30-P-4001A/B/C và 30-P-4002A (dòng 32.7, sang P&ID Unit 34).",
                "Trong 30-PK-2001: nước thô được châm NaOCl 10 % (dòng 32.10), qua bộ trộn tĩnh, rồi chảy vào bồn nước sinh hoạt 30-TK-2002 (dòng 32.4).",
                "30-TK-2002 → bơm nước sinh hoạt 30-P-2002A/B (dòng 32.11) → lọc than hoạt tính + lọc tinh trong 30-PK-2001 (dòng 32.13) "
                "→ header nước sinh hoạt cho hộ tiêu thụ (dòng 32.6, 4,0 barg). Một phần hồi lưu về 30-TK-2002 (dòng 32.12).",
                "Nước rửa ngược lọc than đi ra hệ thống thoát nước mưa (dòng 32.5)."],
         "src": [S_PFD, S_PID1, S_PID2]},
        {"h": "Thiết bị chính",
         "tb": [["Tag", "Chức năng", "Thông số chính"],
                ["30-TK-2001", "Bồn chứa nước thô", "7.155 m³; Ø28.000 × 11.620 mm; áp thiết kế F.W +35/−25 mmH₂O; 60 °C"],
                ["30-P-2001A/B/C", "Bơm nước thô (Flowserve 100-65CPX200)", "160 m³/h; cột áp 50 m; NPSHr 4,1 m; motor 37 kW; 2940 v/ph"],
                ["30-PK-2001", "Cụm xử lý nước sinh hoạt (Chemitreat)", "Khử trùng NaOCl + lọc than hoạt tính + lọc tinh 1 µm; 22 m³/h; đạt tiêu chuẩn WHO"],
                ["30-TK-2002", "Bồn nước sinh hoạt", "260 m³; Ø6.700 × 7.380 mm; 60 °C"],
                ["30-P-2002A/B", "Bơm nước sinh hoạt (Flowserve 50-32CPX200)", "23,4 m³/h; cột áp 50 m; NPSHr 1 m; motor 7,5 kW; 2900 v/ph"]],
         "src": [S_PFD, S_P1, S_P2, S_MECH]},
        {"h": "Lưu lượng các dòng chính (PFD, t/h)",
         "tb": [["Dòng", "Mô tả", "Case 2", "Case 3"],
                ["32.2", "Nước thô vào 30-TK-2001", "44,1", "101,5"],
                ["32.8", "Đầu đẩy 30-P-2001A/B/C", "60,6", "118"],
                ["32.1", "Nước thô đi cụm Demi 30-PK-1001", "37", "94,4"],
                ["32.14", "Nước thô ra header", "5,0", "5,0"],
                ["32.9", "Hồi lưu về 30-TK-2001", "18,6", "18,6"],
                ["32.3 / 32.4", "Vào 30-PK-2001 / nước sinh hoạt về 30-TK-2002", "2,1 / 1,9", "2,1 / 1,9"],
                ["32.11", "Đầu đẩy 30-P-2002A/B", "3,3", "3,3"],
                ["32.6", "Nước sinh hoạt ra header", "1,9", "1,9"],
                ["32.7", "Nước cứu hỏa sang 30-P-4001/4002", "895,5", "(khi chữa cháy)"]],
         "p": ["Case 2: amoniac 1620 MTPD, urê 2385 MTPD. Case 3: amoniac 1620 MTPD về bồn chứa, xưởng urê dừng. "
               "Ghi chú trên PFD: lưu lượng khởi động 480 m³/h; lưu lượng đỉnh nước sinh hoạt 22 m³/h; châm sốc mỗi tháng một lần."],
         "src": [S_PFD]},
        {"h": "Chất lượng nước",
         "kv": [["Nước thô (thiết kế)", "Độ đục 0,3 NTU; pH 7,19; độ cứng 14,95 mg/L CaCO₃; nitrat 0,13 mg/L; Na 6,9 mg/L; Cl 10,65 mg/L; sunfat 8,0 mg/L; Fe 0,28 mg/L; NH₄⁺ < 1 mg/L"],
                ["Nước sinh hoạt (đầu ra)", "Vị, mùi, vi sinh theo tiêu chuẩn nước uống WHO 1996 (ví dụ: độ đục ≤ 5 NTU, pH 6,5–8,5, Fe ≤ 0,3 mg/L, coliform 0/100 mL)"],
                ["Clo dư sau khử trùng", "Đặt 2 ppm (máy phân tích AIT-32201)"]],
         "src": [S_DESIGN]},
        {"h": "Tiêu hao & phụ trợ (theo vendor)",
         "kv": [["NaOCl 10 %", "8,1 tấn/năm (2 ppm châm liên tục + châm sốc khử trùng bồn mỗi tháng)"],
                ["Nước thô cho rửa ngược", "4.100 m³/năm (một lọc, rửa ngược mỗi ngày)"],
                ["Nước cấp cho xử lý", "192.720 m³/năm (tối đa 22 m³/h)"],
                ["Điện", "400 V / 50 Hz / 3 pha"], ["Khí điều khiển", "Khí không dầu, không ẩm, 4–6,8 bar cho van khí nén lọc than"]],
         "src": [S_CHEM, S_DESIGN, S_ACF]},
        {"h": "Lưu ý khi đối chiếu tài liệu",
         "ul": ["Tài liệu vendor 30-PK-2001 (2003) tính châm sốc 5 mg/L cho \"bồn nước sinh hoạt 7.000 m³\", trong khi PFD as-built ghi 30-TK-2002 là 260 m³ "
                "(30-TK-2001 nước thô mới là 7.155 m³). Khi tính lượng châm sốc, dùng thể tích bồn thực tế.",
                "Theo thông số thiết bị của vendor: lọc than hoạt tính là 30-PK-2001/FL2A/B, lọc tinh 1 µm là 30-PK-2001/FL1A/B."],
         "src": [S_PROC, S_MECH, S_PFD]},
    ],
}

pk2001 = {
    "t": "Cụm xử lý nước sinh hoạt 30-PK-2001",
    "intro": "Cụm do Chemitreat cung cấp, gồm một skid với hai phần: châm sodium hypochlorite để khử trùng nước thô, "
             "và xử lý nước sinh hoạt bằng lọc than hoạt tính rồi lọc tinh 1 µm. Công suất 22 m³/h (thiết kế), trung bình 45 m³/ngày.",
    "s": [
        {"h": "Phần châm sodium hypochlorite",
         "ul": ["Nước thô từ trạm bơm vào header 4\"; van giảm áp giữ áp sau van ở 5 barg. Header tách làm hai: nhánh 3\" qua phần châm hóa chất "
                "về bồn nước sinh hoạt, nhánh 4\" cấp nước rửa ngược cho lọc than.",
                "Lưu lượng vào phần châm được chỉnh cố định khoảng 22 m³/h (lưu lượng kế FIT-32201 và van cầu điều chỉnh đầu ra) để liều châm ổn định.",
                "NaOCl 10 % được châm vào đường ống với liều 2 mg/L, sau đó qua bộ trộn tĩnh 2Z1. Máy phân tích clo dư AIT-32201 theo dõi clo dư của nước vào bồn.",
                "Châm sốc: định kỳ (khoảng mỗi tháng một lần) bơm P2 châm 5 mg/L vào bồn nước sinh hoạt để khử trùng bồn."],
         "src": [S_PROC, S_DOSE]},
        {"h": "Phần xử lý nước sinh hoạt",
         "ul": ["Bơm nước sinh hoạt hút từ bồn 30-TK-2002, đẩy ở áp tối đa 5 bar, 22 m³/h qua lọc than hoạt tính. Lọc than khử clo dư và chất hữu cơ, đồng thời giữ cặn thô.",
                "Có 2 lọc than: 1 vận hành, 1 dự phòng. Lọc đang vận hành được rửa ngược mỗi ngày, hoặc sớm hơn khi chênh áp cao; khi đó lọc dự phòng vào thay. Nước rửa ngược lấy từ nước thô.",
                "Sau lọc than là lọc tinh 1 µm (2 bình: 1 vận hành, 1 dự phòng), giữ cặn lớn hơn 1 µm. Thay lõi lọc khi chênh áp vượt 0,7 bar.",
                "Nước sau lọc (22 m³/h, 4 bar) đi ra header phân phối nước sinh hoạt.",
                "Tủ điều khiển tại chỗ bằng inox, đặt ngoài trời, chứa PLC; gửi tín hiệu liên động và báo động về DCS."],
         "src": [S_PROC, S_MECH]},
        {"h": "Nguyên lý khử clo bằng than hoạt tính",
         "p": ["NaOCl trong nước tạo HOCl ⇄ H⁺ + OCl⁻ (clo dư tự do). Than hoạt tính khử clo dư theo phản ứng C + 2Cl₂ + 2H₂O → 4HCl + CO₂. "
               "Than còn hấp phụ chất hữu cơ hòa tan và giữ hạt keo, hạt lơ lửng nhỏ nhờ lực hút tĩnh điện giữa bề mặt than (tích điện dương) và hạt (tích điện âm)."],
         "src": [S_PROC]},
        {"h": "Điều khiển & liên động",
         "ul": ["Lọc than: công tắc chọn lọc chính (A hoặc B) và chế độ rửa ngược Auto/Off/Manual. Ở chế độ Auto, rửa ngược bắt đầu khi hết thời gian vận hành tối đa (24 h), "
                "hoặc khi PDAH-32201A/B báo chênh áp cao (có trễ, khóa bởi bộ đếm thời gian vận hành tối thiểu).",
                "Trình tự rửa ngược: Service (24 h) → Backwash (10 phút) → Rinse (5 phút) → về Service hoặc Standby. "
                "Mỗi lọc có 6 van khí nén XV-32201…32206, điều khiển qua van điện từ XYS-32201…32206 (24 VDC). Khi mất điện, PLC lưu trạng thái và chạy tiếp từ bước cũ.",
                "Bơm châm P1A/B (motor MP1A/B, 0,25 kW): 1 chạy, 1 dự phòng; bơm dự phòng tự chạy khi bơm chính trip. Ở Auto, PLC bật/tắt bơm theo clo dư (AIT-32201, dải 0–5 ppm) giữa ngưỡng thấp và cao; "
                "bơm chỉ chạy khi DCS cho phép (liên động mức cao bồn 30-TK-2002).",
                "Bơm châm sốc P2 (0,55 kW) chạy tay từ MCC, liên động mức thấp bồn NaOCl (LSL-32201).",
                "Báo động: mức thấp bồn NaOCl (LAL-32201), chênh áp cao lọc than A/B (PDAH-32201A/B) và lọc tinh (PDAH-32202), clo cao/thấp (AAH/AAL-32201), trip bơm châm."],
         "src": [S_CTRL, S_SEQ, S_ALM, S_CE]},
    ],
}

TAGS = {
    "30-PK-2001": pk2001,
    "30-P-2001": {
        "t": "Bơm nước thô 30-P-2001A/B/C",
        "intro": "Bơm ly tâm một cấp Flowserve 100-65CPX200, hút từ bồn nước thô 30-TK-2001, cấp nước thô cho cụm Demi 30-PK-1001, "
                 "header nước công nghệ và cụm xử lý nước sinh hoạt 30-PK-2001. Đầu đẩy có đường hồi lưu về 30-TK-2001 qua FIC-32002.",
        "s": [{"h": "Thông số (data sheet & biên bản thử)",
               "kv": [["Kiểu", "Ly tâm, 1 cấp, 100-65CPX200 (Flowserve)"], ["Lưu lượng định mức", "160 m³/h"], ["Cột áp", "50 m"],
                      ["NPSHr", "4,1 m"], ["Tốc độ", "2940 v/ph"], ["Hiệu suất khi thử (30-P-2001A)", "74,5 %"], ["Đường kính cánh", "195 mm"],
                      ["Motor", "Siemens 37 kW, khung 200L, 400 V / 50 Hz, 65 A"], ["Áp đầu đẩy vận hành (PFD)", "5,0 barg"]]},
              {"h": "Vận hành",
               "ul": ["Lưu lượng đầu đẩy theo PFD: 60,6 t/h (case 2) – 118 t/h (case 3); phần dư hồi lưu về bồn (khoảng 18,6 t/h).",
                      "Phớt cơ khí và khớp nối Metastream: xem hướng dẫn trong Vendor Data Book (mục 6-3, 6-4)."]}],
        "src": [S_P1, S_P1M, S_PFD, S_PID1],
    },
    "30-P-2002": {
        "t": "Bơm nước sinh hoạt 30-P-2002A/B",
        "intro": "Bơm ly tâm một cấp Flowserve 50-32CPX200 (1 chạy, 1 dự phòng). Hút từ bồn nước sinh hoạt 30-TK-2002, đẩy qua lọc than hoạt tính "
                 "và lọc tinh 1 µm của 30-PK-2001 ra header nước sinh hoạt (4,0 barg). Có đường hồi lưu về 30-TK-2002.",
        "s": [{"h": "Thông số (data sheet & biên bản thử)",
               "kv": [["Kiểu", "Ly tâm, 1 cấp, 50-32CPX200 (Flowserve)"], ["Lưu lượng định mức", "23,4 m³/h"], ["Cột áp", "50 m (chênh áp 4,88 bar)"],
                      ["NPSHr", "1 m"], ["Tốc độ", "2900 v/ph"], ["Hiệu suất khi thử", "58,3 %"], ["Đường kính cánh", "178 mm"],
                      ["Motor", "Siemens 7,5 kW, khung 132S, 400 V / 50 Hz, 13,8 A"]]},
              {"h": "Đường đặc tính khi thử (30-P-2002A)",
               "tb": [["Q (m³/h)", "0", "6", "12", "18", "23,4", "29", "34"],
                      ["Cột áp đẩy (m)", "56,3", "56,3", "55,7", "52,9", "49,3", "43", "33,3"],
                      ["Công suất motor (kW)", "3,42", "4,08", "4,86", "5,61", "6,3", "6,96", "7,56"]]}],
        "src": [S_P2, S_P2M, S_PFD, S_PID2],
    },
    "30-TK-2001": {"t": "Bồn chứa nước thô 30-TK-2001",
                   "intro": "Nhận nước thô từ ranh giới nhà máy, cấp cho bơm nước thô 30-P-2001A/B/C và dự trữ nước cho bơm cứu hỏa 30-P-4001/4002. Mức bồn đo bằng LI-32001.",
                   "s": [{"h": "Thông số (PFD)", "kv": [["Thể tích", "7.155 m³"], ["Kích thước", "Ø28.000 × 11.620 mm (cao)"],
                                                         ["Áp thiết kế", "F.W +35 / −25 mmH₂O"], ["Nhiệt độ thiết kế", "60 °C"]]}],
                   "src": [S_PFD, S_PID1]},
    "30-TK-2002": {"t": "Bồn nước sinh hoạt 30-TK-2002",
                   "intro": "Chứa nước thô đã khử trùng bằng NaOCl (clo dư khoảng 2 ppm) từ 30-PK-2001, cấp cho bơm nước sinh hoạt 30-P-2002A/B. "
                            "Mức bồn đo bằng LI-32002. Tín hiệu mức cao của bồn (từ DCS) cho phép hoặc chặn bơm châm hypochlorite. Bồn được khử trùng định kỳ bằng châm sốc.",
                   "s": [{"h": "Thông số (PFD)", "kv": [["Thể tích", "260 m³"], ["Kích thước", "Ø6.700 × 7.380 mm (cao)"],
                                                         ["Áp thiết kế", "F.W +35 / −25 mmH₂O"], ["Nhiệt độ thiết kế", "60 °C"]]}],
                   "src": [S_PFD, S_PID2, S_CTRL]},
    "30-PK-2001/FL2": {"t": "Lọc than hoạt tính 30-PK-2001/FL2A/B",
                       "intro": "Bình áp lực chứa lớp than hoạt tính dạng hạt (ACF 1400 × 1800P). Lọc khử clo dư và chất hữu cơ, giữ cặn thô. 2 bình: 1 vận hành, 1 dự phòng.",
                       "s": [{"h": "Thông số", "kv": [["Kích thước", "Ø1.400 × 1.800 mm"], ["Áp / nhiệt độ thiết kế", "7,0 barg / 60 °C"],
                                                      ["Lưu lượng", "22 m³/h mỗi bình"], ["Chênh áp cho phép", "0,5 bar"], ["Lưu lượng rửa ngược", "45 m³/h"],
                                                      ["Vật liệu", "Thép carbon, sơn epoxy (food grade)"], ["Tuổi thọ than", "khoảng 3 năm (than theo chuẩn AWWA)"]]},
                             {"h": "Chu trình", "ul": ["Service (dòng xuống) → Backwash (dòng lên, 10 phút) → Rinse (dòng xuống ra xả, 5 phút) → Standby.",
                                                      "Rửa ngược mỗi ngày, hoặc khi chênh áp đạt khoảng 0,7 bar (PDAH-32201A/B). Có chốt hạn chế độ mở van xả rửa ngược để tránh cuốn mất than."]}],
                       "src": [S_ACF, S_MECH, S_CTRL]},
    "30-PK-2001/FL1": {"t": "Lọc tinh 1 µm 30-PK-2001/FL1A/B",
                       "intro": "Bình inox SS304 chứa lõi lọc cartridge (Filterite) giữ cặn lớn hơn 1 µm sau lọc than. 2 bình: 1 vận hành, 1 dự phòng.",
                       "s": [{"h": "Thông số", "kv": [["Lưu lượng", "22 m³/h"], ["Áp / nhiệt độ thiết kế", "7,0 barg / 60 °C"],
                                                      ["Chênh áp", "0,2 bar (sạch) / 0,7 bar (bẩn, cần thay lõi)"], ["Báo động", "PDAH-32202"]]},
                             {"h": "Thay lõi lọc", "ul": ["Đóng van vào và ra, xả cạn bình, mở nắp, thay lõi mới.",
                                                        "Đóng nắp, mở van vào và van xả khí đến khi đầy nước, rồi mở van xả/rinse để rửa lõi mới. Sau đó đưa về cấu hình vận hành."]}],
                       "src": [S_MF, S_MECH]},
    "30-PK-2001/P1": {"t": "Bơm châm NaOCl 30-PK-2001/P1A/B",
                      "intro": "Bơm màng Milton Roy, mỗi bơm 1 L/h, 6 barg, chỉnh hành trình 0–100 % khi đang chạy (1 chạy, 1 dự phòng). Có van an toàn đặt 7 bar và cột hiệu chuẩn.",
                      "s": [{"h": "Liều châm", "p": ["Lưu lượng châm (L/h) = liều clo (mg/L) × lưu lượng nước (m³/h) / (nồng độ × tỷ trọng × 10). "
                                                     "Với 2 mg/L, 22 m³/h, NaOCl 10 %, tỷ trọng 1,2: khoảng 0,37 L/h, tức hành trình khoảng 37 % của bơm 1 L/h."]},
                            {"h": "Điều khiển", "ul": ["Ở Auto: PLC bật/tắt bơm theo clo dư AIT-32201 (ngưỡng đặt 2 ppm); bơm dự phòng tự chạy khi bơm chính trip.",
                                                       "Liên động với tín hiệu mức cao bồn 30-TK-2002 từ DCS."]}],
                      "src": [S_DOSE, S_MECH, S_CTRL]},
    "30-PK-2001/P2": {"t": "Bơm châm sốc NaOCl 30-PK-2001/P2",
                      "intro": "Bơm màng Milton Roy 700 L/h, 3 barg. Dùng để khử trùng định kỳ bồn nước sinh hoạt bằng liều 5 mg/L (tính theo vendor: bồn 7.000 m³ trong 2 giờ). "
                               "Chạy tay từ MCC, liên động mức thấp bồn NaOCl (LSL-32201).",
                      "s": [], "src": [S_PROC, S_MECH, S_CTRL]},
    "30-PK-2001/P3": {"t": "Bơm thùng NaOCl 30-PK-2001/P3",
                      "intro": "Bơm thùng (drum pump) chạy bằng khí nén, Finish Thompson, 1,36 m³/h, 0,3 barg. Dùng để chuyển NaOCl từ can/thùng vào bồn chứa TK1.",
                      "s": [], "src": [S_MECH]},
    "30-PK-2001/TK1": {"t": "Bồn NaOCl 10 % 30-PK-2001/TK1",
                       "intro": "Bồn 350 L (hữu dụng), Ø600 × 1.440 mm, thép carbon lót cao su, áp khí quyển. Đủ cho một lần châm sốc. "
                                "Có công tắc mức thấp LSL-32201 (Magnetrol) báo động và chặn bơm châm sốc.",
                       "s": [], "src": [S_MECH, S_PROC]},
    "30-PK-2001/2Z1": {"t": "Bộ trộn tĩnh 30-PK-2001/2Z1",
                       "intro": "Đặt trên đường ống ngay sau điểm châm NaOCl, giúp phân tán dung dịch hypochlorite đậm đặc đều vào nước thô trước khi đo clo dư và vào bồn.",
                       "s": [], "src": [S_PROC]},
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import u18, u31_35
TAGS.update(u18.TAGS)
TAGS.update(u31_35.TAGS)
json.dump({"units": {"32": unit32, "18": u18.UNIT, **u31_35.UNITS}, "tags": TAGS}, open(OUT, "w"), ensure_ascii=False, separators=(",", ":"))
print("tech.json:", len(TAGS), "thiết bị, Unit 32, 18, 31, 35")
