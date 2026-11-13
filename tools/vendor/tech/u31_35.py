"""Công nghệ Unit 31 (nước khử khoáng – Demi) và Unit 35 (khí nén điều khiển & khí công nghệ).

Nguồn: PFD as-built 2539-31/35-PFD-0010-01-01 (cân bằng vật chất case 2/case 3) và bảng thông số
thiết bị trên các P&ID 2098/2539-31-PID-0031-01…09, 2098/2539-35-PID-0031-01…06.
Bổ sung (cuối file) từ tài liệu vendor: sách Chemitreat 30-PK-1001 (Vol 1, Vol 2 mục 1.3 – bản scan, OCR),
mô tả công nghệ revamp 2539-31/35-CN-0009-01, data sheet & instruction book Atlas Copco, O&M máy sấy SPX Hankison.
"""


def sh(dwg, label):
    return ["sheet:" + dwg, label]


D_PFD = sh("2539-31-PFD-0010-01-01 (trang 1)", "PFD 2539-31 Demi (as-built)")
D1 = sh("2539-31-PID-0031-01", "P&ID 31-01 Nước khử ion, làm mát nước ngưng")
D2 = sh("2098-31-PID-0031-02", "P&ID 31-02 Trao đổi cation")
D3 = sh("2098-31-PID-0031-03", "P&ID 31-03 Tháp khử CO₂")
D4 = sh("2098-31-PID-0031-04", "P&ID 31-04 Trao đổi anion")
D5 = sh("2098-31-PID-0031-05", "P&ID 31-05 Mixed bed")
D6 = sh("2098-31-PID-0031-06", "P&ID 31-06 Hóa chất tái sinh")
D7 = sh("2098-31-PID-0031-07", "P&ID 31-07 Hố trung hòa")
D8 = sh("2098-31-PID-0031-08", "P&ID 31-08 Bồn & bơm nước khử khoáng")
D9 = sh("2098-31-PID-0031-09", "P&ID 31-09 Bồn axit, xút")

A_PFD = sh("2539-35-PFD-0010-01-01 (trang 1)", "PFD 2539-35 Khí nén (as-built)")
A1 = sh("2098-35-PID-0031-01", "P&ID 35-01 Máy nén A/B")
A2 = sh("2098-35-PID-0031-02", "P&ID 35-02 Máy nén C/D")
A3 = sh("2539-35-PID-0031-03", "P&ID 35-03 Bình chứa & máy sấy")
A4 = sh("2098-35-PID-0031-04", "P&ID 35-04 Phân phối khí")
A5 = sh("2539-35-PID-0031-05", "P&ID 35-05 Máy nén E (mới)")
A6 = sh("2539-35-PID-0031-06", "P&ID 35-06")


DM = "4. Demi/"
V1 = DM + "Demineralised Volume 1 of 6/"
V_DESC = [V1 + "2 - Plant Description.pdf", "Chemitreat Vol 1 · 2 – Mô tả hệ thống"]
V_CHEM = [V1 + "5 - Chemical And Utility Consumption.pdf", "Chemitreat Vol 1 · 5 – Tiêu hao hóa chất"]
V_START = [V1 + "9 - Operation - Normal Startup And Shutdown.pdf", "Chemitreat Vol 1 · 9 – Khởi động & dừng"]
V_REG = [V1 + "10 - Operation - Regeneration.pdf", "Chemitreat Vol 1 · 10 – Tái sinh"]
V_MON = [V1 + "11 - Plant Monitoring.pdf", "Chemitreat Vol 1 · 11 – Giám sát, phân tích"]
V_TS = [V1 + "13 - Trouble shooting.pdf", "Chemitreat Vol 1 · 13 – Xử lý sự cố"]
V_MECH = [V1 + "Mechanical Equipment Specifications.pdf", "Chemitreat Vol 1 · Thông số thiết bị"]
V_CTRL = [DM + "Demineralised Volume 2 of 6/Section 1.3/8 - Control Philosophy.pdf", "Chemitreat 1.3.8 – Triết lý điều khiển"]
V_CALC = [DM + "Demineralised Volume 2 of 6/Section 1.3/2 - Process Calculation with blended water operation.pdf", "Chemitreat 1.3.2 – Tính toán (nước pha trộn)"]
V_REV = [DM + "Revamp_.DEMINERALIZED WATER SYSTEM/1. PROCESS DESCRIPTION/2539-31-CN-0009-01_0.pdf", "2539-31-CN-0009-01 Mô tả công nghệ revamp"]
V_E1001 = [DM + "30-E-1001/Tag 3.pdf", "Alfa Laval 30-E-1001 · Data sheet"]
V_E1002 = [DM + "Revamp_.DEMINERALIZED WATER SYSTEM/4. DATASHEET/30-E1002/2539-31-SP-0660-01_PB.pdf", "Data sheet 30-E-1002"]

AS = "7. Air System/"
A_REV = [AS + "1. PROCESS DESCRIPTION/2539-35-CN-0009-01_B.pdf", "2539-35-CN-0009-01 Mô tả công nghệ revamp"]
A_VN = [AS + "1. PROCESS DESCRIPTION/Unit 30-Air Compression.docx", "Mô tả công nghệ khí nén (tiếng Việt)"]
A_DS = [AS + "30-K-5001A_D, DR-5001 (Air compressors).pdf", "Data sheet 30-K-5001A–D & 30-DR-5001"]
A_IB = [AS + "3. 30-K-5001/Tach theo tai lieu/16 - A5016 - Huong dan van hanh & bao duong (Instruction book).pdf", "Atlas Copco ZR – Instruction book"]
A_DBDS = [AS + "3. 30-K-5001/Tach theo tai lieu/01 - A1001 - Data sheet thiet bi (filled-in).pdf", "Atlas Copco – data sheet (data book)"]
A_KE = [AS + "30-K-5001E/2539-35-SP-1031-01_PB.pdf", "Data sheet 30-K-5001E"]
A_KEOM = [AS + "1. PROCESS DESCRIPTION/2539-1031-01-A5016-001_0-C.PDF", "O&M máy nén 30-K-5001E"]
A_D2 = [AS + "30-DR-5002/2539-35-SP-4171-01_0.pdf", "Data sheet 30-DR-5002"]
A_D2OM = [AS + "1. PROCESS DESCRIPTION/2539-4171-01-A5016-001_0-C.PDF", "O&M máy sấy 30-DR-5002 (SPX Hankison)"]


def ent(t, intro, s=None, src=None):
    return {"t": t, "intro": intro, "s": s or [], "src": src or []}


# ───────────────────────── Unit 31 – Demi ─────────────────────────
UNIT31 = {
    "t": "Công nghệ Unit 31 – Nước khử khoáng (Demi)",
    "intro": "Unit 31 sản xuất nước khử khoáng (độ dẫn điện < 0,2 µS/cm) cấp cho bình khử khí 10-V-8001 của lò hơi và cho xưởng Urê. "
             "Nước đầu vào gồm nước thô, nước ngưng công nghệ đã stripping và nước ngưng công nghệ từ xưởng Urê. "
             "Hỗn hợp này qua cụm 30-PK-1001 theo sơ đồ \"2B3T + MBP\": cation → tháp khử CO₂ → anion, ba dây chuyền A/B/C, mỗi dây 150 m³/h. "
             "Nước ra hòa với nước ngưng turbine (đã làm mát) trong bồn nước khử ion 30-TK-1001. Tiếp đó nước qua ba bình trao đổi hỗn hợp (mixed bed, 200 m³/h mỗi bình) và vào bồn chứa 30-TK-1002 (9.000 m³). "
             "Từ đây bơm 30-P-1002A/B cấp nước ra ở 9 barg.",
    "s": [
        {"h": "Sơ đồ dòng (PFD as-built, case 2)",
         "ul": ["Nguồn nước vào cụm khử khoáng: nước thô từ bơm 30-P-2001A/B/C (37 t/h, 25 °C), nước ngưng công nghệ đã stripping từ 10-E-7002 (60,6 t/h) "
                "và nước ngưng công nghệ (treated process water) từ 20-E1024 của xưởng Urê (64,9 t/h). Tổng 162,5 t/h vào bình cation.",
                "Dây chuyền 2B3T: bình cation 30-PK-1001/V1A/B/C → tháp khử CO₂ 30-PK-1001/V2A/B/C (quạt K2A/B/C thổi gió ngược chiều) → bơm P2A/B/C → bình anion V3A/B/C. "
                "Nước khử ion (156,3 t/h, 41 °C) vào bồn 30-TK-1001.",
                "Nước ngưng turbine từ 10-E-4001 và 20-E-1022 (161,3 t/h, 60 °C) được chia đều cho hai bộ làm mát dạng tấm 30-E-1001 (cũ) và 30-E-1002 (mới, revamp), làm mát xuống 45 °C bằng nước làm mát. "
                "Sau đó nhập với nước ngưng hơi từ 20-E1023 (25,9 t/h) thành 187,2 t/h vào 30-TK-1001.",
                "Bơm 30-P-1001A/B lấy nước từ 30-TK-1001 (344,1 t/h, 5 barg) qua bình mixed bed 30-PK-1001/V4A/B/C (đánh bóng) rồi vào bồn 30-TK-1002.",
                "Bơm 30-P-1002A/B cấp 343,5 t/h nước khử khoáng ở 9 barg, 43 °C tới bình khử khí 10-V-8001 và kho Urê. Có đường hồi lưu lưu lượng nhỏ nhất về bồn.",
                "Nước thải: nước nhiễm amoniac 4,2 t/h (trung bình) về 40-BA2001; nước thải hóa chất không nhiễm bẩn 2,6 t/h (trung bình, sau trung hòa ở hố 30-PK-1001/BA1) về 30-BA3001.",
                "Case 3 (Amoniac 1.620 t/ngày vào bồn chứa, Urê dừng): không có nước ngưng công nghệ, nước thô tăng lên 94,4 t/h; nước cấp ra 277,3 t/h, nhiệt độ ≈38,9 °C."],
         "src": [D_PFD]},
        {"h": "Dòng chính",
         "tb": [["Dòng", "Mô tả", "Case 2 (t/h)", "Case 3 (t/h)", "°C / barg"],
                ["31.1", "Nước thô vào", "37", "94,4", "25 / 5"],
                ["31.2", "Nước ngưng công nghệ đã stripping (10-E-7002)", "60,6", "60,6", "45 / 4"],
                ["31.3", "Nước ngưng công nghệ (20-E1024)", "64,9", "0", "45 / 3"],
                ["31.17", "Nước vào bình cation", "162,5", "155,0", "41 / 4"],
                ["31.9", "Nước khử ion ra khỏi anion", "156,3", "148,8", "41 / 1,5"],
                ["31.4", "Nước ngưng turbine", "161,3", "129,1", "60 / 4"],
                ["31.7", "Nước ngưng vào 30-TK-1001", "187,2", "129,1", "45 / 2"],
                ["31.8", "Bơm 30-P-1001A/B → mixed bed", "344,1", "277,9", "43 / 5"],
                ["31.16", "Nước khử khoáng tới 10-V-8001 & Urê", "343,5", "277,3", "43 / 9"],
                ["31.12", "Nước thải nhiễm NH₃ → 40-BA2001", "4,2", "4,2", "41 / 1"],
                ["31.19", "Nước thải hóa chất → 30-BA3001", "2,6", "2,6", "43 / 1,5"]],
         "p": ["Lưu lượng nước thô, nước khử ion và nước thải là giá trị trung bình, đã tính lượng nước tái sinh và rửa nhựa. "
               "Nước thải nhiễm NH₃ (154 ppm) xả theo mẻ: 95,57 m³ mỗi 24 giờ + 26,64 m³ mỗi 120 giờ. "
               "Nước thải hóa chất: 53,56 m³ mỗi 24 giờ + 40,12 m³ mỗi 120 giờ. Lưu lượng khởi động 314,4 m³/h."],
         "src": [D_PFD]},
        {"h": "Thiết bị chính",
         "tb": [["Tag", "Chức năng", "Thông số (P&ID)"],
                ["30-PK-1001", "Cụm khử khoáng 2B3T + MBP", "2B3T: 3 × 150 m³/h; MBP: 3 × 200 m³/h; độ dẫn điện < 0,2 µS/cm"],
                ["30-PK-1001/V1A/B/C", "Bình trao đổi cation", "Ø2.000 × 2.600 mm; 7 barg"],
                ["30-PK-1001/V2A/B/C", "Tháp khử CO₂ (degasifier)", "Tháp Ø1.800 × 3.300; bể Ø2.400 × 4.500 mm"],
                ["30-PK-1001/V3A/B/C", "Bình trao đổi anion", "Ø2.000 × 3.000 mm; 7 barg"],
                ["30-PK-1001/V4A/B/C", "Bình trao đổi hỗn hợp (mixed bed polisher)", "Ø2.400 × 2.500 mm; 7 barg"],
                ["30-TK-1001", "Bồn nước khử ion", "500 m³; Ø8.500 × 8.820 mm"],
                ["30-TK-1002", "Bồn nước khử khoáng", "9.000 m³; Ø29.500 × 13.200 mm"],
                ["30-P-1001A/B", "Bơm nước khử ion", "420 m³/h; 50 m; 90 kW"],
                ["30-P-1002A/B", "Bơm nước khử khoáng", "400 m³/h; 105 m; 150 kW"],
                ["30-E-1001 / 30-E-1002", "Làm mát nước ngưng turbine (dạng tấm)", "Mỗi bộ 1.630 kW; 85 → 75 °C thiết kế"],
                ["30-TK-1003 / 30-TK-1004", "Bồn H₂SO₄ / NaOH", "120 m³ / 15,7 m³"],
                ["30-PK-1001/BA1", "Hố trung hòa", "656 m³; 25 × 7,5 × 3,5 m"]],
         "src": [D1, D2, D3, D4, D5, D8, D9, D7]},
        {"h": "Tái sinh & trung hòa",
         "ul": ["Bình cation tái sinh bằng H₂SO₄ loãng, bình anion tái sinh bằng NaOH loãng; mixed bed dùng cả hai. "
                "Hóa chất đặc từ bồn 30-TK-1003/1004 được định lượng qua các bồn đong (TK3–TK6) và bồn pha loãng (TK10/TK11). "
                "Sau đó ejector J1–J4 hút hóa chất, dùng nước tái sinh từ bơm 30-PK-1001/P1A/B làm dòng động lực.",
                "Bơm nước tái sinh: P1A/B dùng nước khử ion (50 m³/h, 35 m). Bơm P3 dùng nước thô (160 m³/h, 50 m), dùng khi chỉ có nước thô làm nguồn cấp.",
                "Bình chứa khí nén 30-PK-1001/V5 (Ø1.800 × 2.000 mm, 11 barg) cấp khí trộn nhựa cho mixed bed.",
                "Nước thải tái sinh về hố trung hòa BA1. Hai quạt K1A/B (kiểu Roots, 350 m³/h, 11 kW) sục khí để khuấy trộn. "
                "pH được chỉnh bằng NaOH (TK8, bơm P7A/B) hoặc H₂SO₄ (TK9, bơm P8A/B), sau đó bơm P5A/B (125 m³/h) đưa đi. Có phân tích AI-31205 báo động pH cao/thấp.",
                "Na₂SO₃: bồn khuấy TK7 (6,28 m³) và bơm màng P6A/B (0,01 m³/h) châm vào đường nước thô trước bình cation (cách ≥ 20–30 m) để khử clo dư, bảo vệ nhựa cation."],
         "src": [D6, D7, D2, D5, D_PFD]},
    ],
}

TAGS31 = {
    "30-PK-1001": ent("Cụm khử khoáng 30-PK-1001",
                      "Cụm trao đổi ion \"2B3T + MBP\". 2B3T là 2 bình (cation, anion) và 3 tháp (cation, khử CO₂, anion) cho mỗi dây chuyền, ba dây A/B/C, 150 m³/h mỗi dây. "
                      "MBP là ba bình trao đổi hỗn hợp V4A/B/C, 200 m³/h mỗi bình. Cụm có tủ điều khiển tại chỗ, hệ hóa chất tái sinh và hố trung hòa. Nước ra có độ dẫn điện < 0,2 µS/cm.",
                      [{"h": "Thiết bị con (theo P&ID)",
                        "tb": [["Tag", "Chức năng"],
                               ["V1A/B/C", "Bình cation Ø2.000 × 2.600"], ["V2A/B/C", "Tháp khử CO₂ + bể chứa"], ["P2A/B/C", "Bơm sau khử CO₂, 170 m³/h"],
                               ["K2A/B/C, SL1, FL1", "Quạt khử CO₂ 3.100 m³/h, bộ tiêu âm, lọc gió"], ["V3A/B/C", "Bình anion Ø2.000 × 3.000"],
                               ["V4A/B/C", "Mixed bed Ø2.400 × 2.500"], ["V5", "Bình khí nén trộn nhựa"], ["P1A/B, P3", "Bơm nước tái sinh (khử ion / nước thô)"],
                               ["TK3–TK6, TK10, TK11, J1–J4, Z2, Z3", "Đong, pha loãng, ejector axit/xút"], ["TK7, Z1, P6A/B", "Pha & châm Na₂SO₃"],
                               ["BA1, K1A/B, SL2A/B, P5A/B", "Hố trung hòa, quạt sục, bơm nước thải"], ["TK8, Z4, P7A/B / TK9, P8A/B", "Châm NaOH / H₂SO₄ trung hòa"]]}],
                      [D_PFD, D2, D3, D4, D5, D6, D7]),
    "30-PK-1001/V1": ent("Bình trao đổi cation 30-PK-1001/V1A/B/C",
                         "Ba bình (Ø2.000 × 2.600 mm, thiết kế 7 barg / 75 °C), mỗi bình một dây chuyền. Bình giữ lại các cation (Ca²⁺, Mg²⁺, Na⁺, NH₄⁺…) và giải phóng H⁺, nên bicarbonate chuyển thành CO₂ tự do để khử ở tháp sau. "
                         "Nhựa được tái sinh bằng H₂SO₄ loãng từ ejector J1/J2, nước tái sinh lấy từ bơm P1A/B.", src=[D2, D6]),
    "30-PK-1001/V2": ent("Tháp khử CO₂ 30-PK-1001/V2A/B/C",
                         "Tháp có đệm (Ø1.800 × 3.300 mm) đặt trên bể chứa (Ø2.400 × 4.500 mm, áp khí quyển). Nước sau cation chảy từ trên xuống, gió từ quạt K2A/B/C thổi ngược lên để đuổi CO₂, giảm tải cho bình anion. "
                         "Bơm P2A/B/C (170 m³/h, 35 m, 30 kW) đưa nước sang bình anion.", src=[D3, D4]),
    "30-PK-1001/P2": ent("Bơm sau tháp khử CO₂ 30-PK-1001/P2A/B/C",
                         "Bơm ly tâm 170 m³/h, cột áp 35 m, NPSHr 5,3 m, motor 30 kW (MP2A/B/C), 2.940 v/ph. Lấy nước từ bể tháp khử CO₂ đưa sang bình anion.", src=[D3]),
    "30-PK-1001/K2": ent("Quạt tháp khử CO₂ 30-PK-1001/K2A/B/C",
                         "Quạt ly tâm 3.100 m³/h, 100 mmH₂O, 2,2 kW (MK2A/B/C), 1.500 v/ph. Có lọc gió vào FL1A/B/C và bộ tiêu âm SL1A/B/C.", src=[D4]),
    "30-PK-1001/V3": ent("Bình trao đổi anion 30-PK-1001/V3A/B/C",
                         "Ba bình Ø2.000 × 3.000 mm (7 barg / 75 °C). Bình giữ lại các anion (SO₄²⁻, Cl⁻, NO₃⁻, SiO₂, CO₂ còn lại). Nhựa tái sinh bằng NaOH loãng (ejector J3/J4). "
                         "Nước ra (nước khử ion, 156,3 t/h case 2) vào bồn 30-TK-1001.", src=[D4, D6, D_PFD]),
    "30-PK-1001/V4": ent("Bình trao đổi hỗn hợp 30-PK-1001/V4A/B/C",
                         "Ba bình mixed bed (Ø2.400 × 2.500 mm, 7 barg), mỗi bình 200 m³/h, đánh bóng nước khử ion từ bơm 30-P-1001A/B đến độ dẫn điện < 0,2 µS/cm rồi đưa vào 30-TK-1002. "
                         "Khi tái sinh, nhựa được phân lớp, tái sinh riêng bằng axit và xút, sau đó trộn lại bằng khí nén từ bình V5.", src=[D5, D_PFD, D6]),
    "30-PK-1001/V5": ent("Bình khí nén 30-PK-1001/V5", "Bình đứng Ø1.800 × 2.000 mm, thiết kế 11 barg / 75 °C. Chứa khí nén (plant air) dùng để trộn nhựa mixed bed khi tái sinh.", src=[D5]),
    "30-PK-1001/P1": ent("Bơm nước tái sinh 30-PK-1001/P1A/B",
                         "Bơm ly tâm 50 m³/h, 35 m, NPSHr 2,4 m, 11 kW, 2.940 v/ph. Cấp nước động lực cho các ejector axit/xút và nước rửa nhựa khi tái sinh.", src=[D2, D6]),
    "30-PK-1001/P3": ent("Bơm nước thô tái sinh 30-PK-1001/P3",
                         "Bơm ly tâm 160 m³/h, 50 m, NPSHr 4,1 m, 37 kW, 2.940 v/ph. Dùng nước thô cho rửa ngược và tái sinh bình cation.", src=[D2]),
    "30-PK-1001/TK7": ent("Bồn Na₂SO₃ 30-PK-1001/TK7",
                          "Bồn 6,28 m³ (Ø2.000 × 2.000 mm) có khuấy Z1. Bơm màng P6A/B (0,01 m³/h, 50 m, 0,25 kW) châm Na₂SO₃ vào nước thô trước bình cation để khử clo dư (clo tự do 0,6 mg/l → 0). Lưu lượng châm chỉnh theo clo dư đo trước bình cation. Hệ thống tính cho lưu lượng nước thô tối đa 450 m³/h.", src=[V_DESC, D6, D_PFD]),
    "30-PK-1001/P6": ent("Bơm châm Na₂SO₃ 30-PK-1001/P6A/B", "Bơm màng 0,01 m³/h, cột áp 50 m, 0,25 kW, 112 lần/ph, hút từ bồn TK7.", src=[D6]),
    "30-PK-1001/TK3": ent("Bồn đong H₂SO₄ số 1 30-PK-1001/TK3", "0,28 m³ (Ø600 × 1.000 mm). Đong axit đặc trước khi pha loãng ở TK10 và đưa qua ejector J1.", src=[D6]),
    "30-PK-1001/TK4": ent("Bồn đong H₂SO₄ số 2 30-PK-1001/TK4", "0,28 m³ (Ø600 × 1.000 mm), dùng cho ejector J2 / bồn pha loãng TK11.", src=[D6]),
    "30-PK-1001/TK5": ent("Bồn đong NaOH số 1 30-PK-1001/TK5", "1,58 m³ (Ø1.400 × 1.400 mm), có khuấy Z2. Cấp xút cho ejector J3.", src=[D6]),
    "30-PK-1001/TK6": ent("Bồn đong NaOH số 2 30-PK-1001/TK6", "0,94 m³ (Ø1.000 × 1.400 mm), có khuấy Z3. Cấp xút cho ejector J4.", src=[D6]),
    "30-PK-1001/TK10": ent("Bồn pha loãng H₂SO₄ số 1 30-PK-1001/TK10", "2,77 m³ (Ø1.400 × 1.800 mm).", src=[D6]),
    "30-PK-1001/TK11": ent("Bồn pha loãng H₂SO₄ số 2 30-PK-1001/TK11", "0,94 m³ (Ø1.000 × 1.200 mm).", src=[D6]),
    "30-PK-1001/BA1": ent("Hố trung hòa 30-PK-1001/BA1",
                          "Hố bê tông 656 m³ (25 × 7,5 × 3,5 m) nhận nước thải tái sinh và nước xả các bình. Quạt K1A/B sục khí để khuấy, châm NaOH (P7A/B) hoặc H₂SO₄ (P8A/B) để chỉnh pH. "
                          "Bơm P5A/B (125 m³/h, 30 m, 18,5 kW) đưa nước đã trung hòa về 30-BA3001. pH được giám sát bằng AI-31205.", src=[D7, D_PFD]),
    "30-PK-1001/K1": ent("Quạt sục hố trung hòa 30-PK-1001/K1A/B", "Quạt kiểu hai thùy (Roots), 350 m³/h, chênh áp 0,5 bar, 11 kW, 1.500 v/ph; bộ tiêu âm SL2A/B.", src=[D7]),
    "30-PK-1001/P5": ent("Bơm nước trung hòa 30-PK-1001/P5A/B", "Bơm ly tâm 125 m³/h, 30 m, NPSHr 3 m, 18,5 kW, 2.900 v/ph. Hút từ hố BA1.", src=[D7]),
    "30-PK-1001/P7": ent("Bơm châm NaOH trung hòa 30-PK-1001/P7A/B", "Bơm màng 0,5 m³/h, 50 m, 0,75 kW. Hút từ bồn TK8 (0,28 m³, có khuấy Z4).", src=[D7]),
    "30-PK-1001/P8": ent("Bơm châm H₂SO₄ trung hòa 30-PK-1001/P8A/B", "Bơm màng 0,5 m³/h, 50 m, 0,75 kW. Hút từ bồn TK9 (0,28 m³).", src=[D7]),
    "30-PK-1001/TK8": ent("Bồn NaOH trung hòa 30-PK-1001/TK8", "0,28 m³ (Ø600 × 1.000 mm), có khuấy Z4.", src=[D7]),
    "30-PK-1001/TK9": ent("Bồn H₂SO₄ trung hòa 30-PK-1001/TK9", "0,28 m³ (Ø600 × 1.000 mm).", src=[D7]),
    "30-TK-1001": ent("Bồn nước khử ion 30-TK-1001",
                      "Bồn mái cố định 500 m³ (Ø8.500 × 8.820 mm). Nhận nước khử ion từ bình anion và nước ngưng (turbine, hơi) đã làm mát, rồi cấp cho bơm 30-P-1001A/B → mixed bed. "
                      "Mức điều khiển bằng LIC-31001.", src=[D1, D_PFD]),
    "30-TK-1002": ent("Bồn nước khử khoáng 30-TK-1002",
                      "Bồn 9.000 m³ (Ø29.500 × 13.200 mm), thiết kế áp đầy chất lỏng +35 / −25 mmH₂O. Chứa nước sau mixed bed, cấp cho bơm 30-P-1002A/B. "
                      "Có lưới chắn côn trùng; từ 06/2018 lắp đường thông hơi để chống xi-phông.", src=[D8, D_PFD]),
    "30-P-1001": ent("Bơm nước khử ion 30-P-1001A/B",
                     "Bơm ly tâm 420 m³/h, 50 m, NPSHr 3,2 m, motor 90 kW (30-MP-1001A/B), 1.480 v/ph. Hút từ 30-TK-1001 đẩy qua mixed bed V4A/B/C; FIC-31002 hồi lưu lưu lượng nhỏ nhất về bồn. "
                     "Case 2: 344,1 t/h ở 5 barg.", src=[D1, D_PFD]),
    "30-P-1002": ent("Bơm nước khử khoáng 30-P-1002A/B",
                     "Bơm ly tâm 400 m³/h, 105 m, NPSHr 6,5 m, motor 150 kW (30-MP-1002A/B), 2.950 v/ph. Hút từ 30-TK-1002 cấp nước ở 9 barg tới bình khử khí 10-V-8001 và kho Urê "
                     "(343,5 t/h case 2). FIC-31003 hồi lưu lưu lượng nhỏ nhất về bồn.", src=[D8, D_PFD]),
    "30-E-1001": ent("Làm mát nước ngưng turbine 30-E-1001",
                     "Thiết bị trao đổi nhiệt dạng tấm (có từ trước). Công suất gốc 2.955 kW; khi revamp đã tháo bớt tấm, còn 1.630 kW. Làm mát một nửa dòng nước ngưng turbine (80,65 t/h) từ 60 °C xuống 45 °C bằng nước làm mát.",
                     src=[D_PFD, D1]),
    "30-E-1002": ent("Làm mát nước ngưng turbine số 2 30-E-1002",
                     "Thiết bị trao đổi nhiệt dạng tấm, lắp mới khi revamp, 1.630 kW. Chia đều lưu lượng với 30-E-1001: 80,65 t/h, 60 → 45 °C.", src=[D_PFD, D1]),
    "30-TK-1003": ent("Bồn H₂SO₄ 30-TK-1003",
                      "Bồn 120 m³ (Ø6.000 × 4.250 mm). Có van thở PVSV (−25 / +100 mmH₂O). Bơm 30-P-1003A/B (20 m³/h, 20 m, 5,5 kW) dùng để nhận axit và chuyển axit; bơm dừng khi mức bồn thấp-thấp.",
                      src=[D9]),
    "30-TK-1004": ent("Bồn NaOH 30-TK-1004",
                      "Bồn nằm ngang 15,7 m³ (Ø2.200 × 3.400 mm), đặt cao hơn các bồn đong TK5/TK6 để xút tự chảy. Nhận xút bằng bơm 30-P-1004 (20 m³/h, 20 m, 5,5 kW).",
                      src=[D9]),
    "30-P-1003": ent("Bơm nhận/chuyển H₂SO₄ 30-P-1003A/B", "Bơm ly tâm 20 m³/h, 20 m, NPSHr 1 m, 5,5 kW, 2.840 v/ph.", src=[D9]),
    "30-P-1004": ent("Bơm nhận NaOH 30-P-1004", "Bơm ly tâm 20 m³/h, 20 m, NPSHr 1,3 m, 5,5 kW, 2.900 v/ph.", src=[D9]),
}

# ───────────────────────── Unit 35 – khí nén ─────────────────────────
UNIT35 = {
    "t": "Công nghệ Unit 35 – Khí nén điều khiển & khí công nghệ",
    "intro": "Năm máy nén trục vít 30-K-5001A–E (mỗi máy 1.400 Nm³/h, 9 barg) nén không khí vào bình chứa 30-V-5001. Từ đây có hai nhánh. "
             "Nhánh khí công nghệ (plant air) đi thẳng tới các hộ dùng. "
             "Nhánh khí điều khiển (instrument air) qua hai máy sấy hấp phụ không gia nhiệt 30-DR-5001/5002 (điểm sương −25 °C), vào bình 30-V-5002, rồi phân phối ở 7,5 barg. "
             "Máy nén khí công nghệ 10-K-4021 của xưởng Amoniac là nguồn dự phòng.",
    "s": [
        {"h": "Sơ đồ dòng (PFD as-built, case 2)",
         "ul": ["30-K-5001A–D (có từ trước) và 30-K-5001E (lắp mới khi revamp) cùng nén khí vào 30-V-5001. Tổng 4.825 Nm³/h ở 9 barg / 45 °C.",
                "Dự phòng: khí từ máy nén 10-K-4021 (9 barg) cấp vào qua PIC-35002 khi áp hệ thống thấp; bình thường không có lưu lượng. PIC-35001 gửi tín hiệu áp sang xưởng Amoniac.",
                "Khí điều khiển: 3.138 Nm³/h vào máy sấy 30-DR-5001 (1.820 Nm³/h) và 30-DR-5002 (1.100 Nm³/h, mới). "
                "Hai máy hao 329 và 206 Nm³/h khí cho tái sinh, còn 2.603 Nm³/h khí khô vào 30-V-5002 (8,1 barg).",
                "Phân phối khí điều khiển (áp tại ranh giới hộ dùng 7,5 barg): Amoniac 1.050, Urê 395, Utility (hơi & điện) 55, phần còn lại của nhà máy 1.103 Nm³/h.",
                "Khí công nghệ: 1.687 Nm³/h đi thẳng từ 30-V-5001. Header 1.274 Nm³/h ở 8,5 barg cấp cho Amoniac 99, Urê 413, Utility 38, phần còn lại của nhà máy 468 Nm³/h, "
                "và cụm Nitơ 30-PK-6001 669 Nm³/h (tối đa 1.096 Nm³/h khi nhà máy chạy công suất thiết kế). Khí thụ động hóa (passivation) cấp cho xưởng 21, đỉnh 700 Nm³/h khi khởi động.",
                "Ưu tiên khí điều khiển: khi áp 30-V-5002 thấp-thấp (PIC-35003 / PALL-35004), van trên header khí công nghệ tự đóng để giữ áp cho khí điều khiển.",
                "Case 3 (Urê dừng): khí nén tổng 4.017 Nm³/h, khí điều khiển 2.208 Nm³/h; Urê không dùng khí."],
         "src": [A_PFD, A3, A4]},
        {"h": "Thiết bị chính",
         "tb": [["Tag", "Chức năng", "Thông số"],
                ["30-K-5001A–E", "Máy nén khí trục vít (rotary positive displacement)", "1.400 Nm³/h; 9 barg; 200 kW; 1.485 v/ph (mỗi máy)"],
                ["30-V-5001", "Bình chứa khí nén", "Ø2.300 × 6.100 mm; 11 barg"],
                ["30-DR-5001", "Máy sấy khí điều khiển (heatless)", "1.820 Nm³/h; điểm sương −25 °C"],
                ["30-DR-5002", "Máy sấy khí điều khiển (heatless, mới)", "1.100 Nm³/h; điểm sương −25 °C"],
                ["30-V-5002", "Bình chứa khí điều khiển", "Ø4.100 × 10.300 mm; 11 barg"]],
         "src": [A_PFD, A3]},
        {"h": "Điều khiển máy nén (load/unload)",
         "p": ["Mỗi máy nén có tủ điều khiển tại chỗ và chạy theo chế độ có tải/không tải. Các máy đặt ngưỡng lệch nhau để vào tải lần lượt:"],
         "tb": [["Bậc", "Có tải (load)", "Không tải (unload)"],
                ["1", "8,4 barg", "9,0 barg"], ["2", "8,6 barg", "9,2 barg"], ["3", "8,8 barg", "9,4 barg"], ["4", "9,0 barg", "9,6 barg"]],
         "src": [A1, A5]},
        {"h": "Dòng chính",
         "tb": [["Dòng", "Mô tả", "Case 2 (Nm³/h)", "barg"],
                ["35.1", "Khí nén từ 30-K-5001A–E", "4.825", "9,0"], ["35.3", "Khí nén vào máy sấy", "3.138", "9,0"],
                ["35.4", "Khí nén cho hộ dùng (plant air)", "1.687", "9,0"], ["35.5 / 35.18", "Khí tái sinh DR-5001 / DR-5002", "329 / 206", "0"],
                ["35.7", "Khí điều khiển từ 30-V-5002", "2.603", "8,1"], ["35.12", "Header khí công nghệ", "1.274", "8,5"],
                ["35.11", "Khí công nghệ → 30-PK-6001 (Nitơ)", "669", "8,5"]],
         "src": [A_PFD]},
    ],
}

K_AB = [{"h": "Thiết bị kèm theo máy nén (P&ID)",
         "tb": [["Tag con", "Chức năng", "Thông số"],
                ["E1", "Làm mát trung gian / làm mát sau (ống chùm)", "103,4 kW; ống 6/11 barg, 240 °C"],
                ["E2", "Làm mát dầu (dạng tấm)", "24 barg / 225 °C"],
                ["V1 / V2", "Tách nước sau làm mát trung gian / làm mát sau", "3,7 / 11 barg thiết kế"],
                ["FL1", "Lọc gió vào (giấy khô)", "2.700 m³/h; 3 µm 99,9 %"],
                ["FL2 / FL3", "Lọc dầu / lọc thở hộp dầu (ejector)", "4 m³/h"],
                ["TK1 / P1", "Hộp dầu 0,06 m³ / bơm dầu gerotor dẫn động từ trục", "4 m³/h, 3 bar"],
                ["SL1 / SL2", "Tiêu âm cửa hút / tiêu âm cấp cao áp", "1.400 / 140 m³/h; 68 dBA"]]},
        {"h": "Bảo vệ",
         "p": ["Tủ điều khiển tại chỗ điều khiển chạy/dừng, có tải/không tải (XL-35001) và trip (XA-35002). Có báo động rung (VAHH), nhiệt độ khí ra cao (TAH/TAHH-35201), "
               "áp dầu thấp (PAL/PALL-35204), nhiệt độ dầu cao (TAH/TAHH-35208), lỗi cảm biến (SSA-35001)."]}]

TAGS35 = {
    "30-K-5001": ent("Máy nén khí 30-K-5001A–E",
                     "Máy nén trục vít hai cấp kiểu dịch chuyển dương: 1.400 Nm³/h, chênh áp 9 bar, motor 200 kW, 1.485 v/ph. "
                     "A–D có từ trước (P&ID 35-01/02), E lắp mới khi revamp (P&ID 35-05). Khí qua làm mát trung gian/làm mát sau và tách nước, rồi vào bình 30-V-5001. "
                     "Các máy vào tải lần lượt theo các bậc áp 8,4–9,0 barg (không tải ở 9,0–9,6 barg).",
                     K_AB, [A1, A2, A5, A_PFD]),
    "30-V-5001": ent("Bình chứa khí nén 30-V-5001",
                     "Bình đứng Ø2.300 × 6.100 mm, thiết kế 11 barg / 75 °C. Gom khí từ các máy nén (≈4.825 Nm³/h, 9 barg), cấp khí cho máy sấy và header khí công nghệ. Nhận khí dự phòng từ 10-K-4021.",
                     src=[A3, A_PFD]),
    "30-V-5002": ent("Bình chứa khí điều khiển 30-V-5002",
                     "Bình đứng Ø4.100 × 10.300 mm, 11 barg. Chứa khí khô sau máy sấy (8,1 barg), đóng vai trò dự trữ khi mất máy nén. "
                     "Áp thấp-thấp (PALL-35004) đóng van header khí công nghệ để ưu tiên khí điều khiển. Khí phân phối tới hộ dùng ở 7,5 barg.",
                     src=[A3, A_PFD, A4]),
    "30-DR-5001": ent("Máy sấy khí điều khiển 30-DR-5001",
                      "Máy sấy hấp phụ không gia nhiệt (heatless, hai tháp luân phiên), 1.820 Nm³/h, điểm sương −25 °C. Tiêu hao ≈329 Nm³/h khí khô cho tái sinh (xả ra khí quyển).",
                      src=[A3, A_PFD]),
    "30-DR-5002": ent("Máy sấy khí điều khiển 30-DR-5002",
                      "Máy sấy heatless lắp mới khi revamp, 1.100 Nm³/h, điểm sương −25 °C, khí tái sinh ≈206 Nm³/h. Chạy song song với 30-DR-5001.", src=[A3, A_PFD]),
}
TAGS35["10-K-4021"] = ent("Máy nén khí công nghệ 10-K-4021 (nguồn dự phòng)",
                          "Máy nén khí công nghệ của xưởng Amoniac. Có đường dự phòng (9 barg, 47 °C) cấp vào hệ khí nén Unit 35 qua PIC-35002 khi áp thấp; bình thường không có lưu lượng.",
                          src=[A_PFD])

UNITS = {"31": UNIT31, "35": UNIT35}
TAGS = {**TAGS31, **TAGS35}

# alias: máy nén từng máy (tag con 30-K-5001A/E2 tra về 30-K-5001A), motor bơm 30-MP-xxxx
for x in "ABCDE":
    TAGS["30-K-5001" + x] = TAGS["30-K-5001"]
for n in ("1001", "1002", "1003", "1004"):
    TAGS["30-MP-" + n] = TAGS["30-P-" + n]


# ───────────── bổ sung từ tài liệu vendor (4. Demi, 7. Air System) ─────────────
UNIT31["s"] += [
    {"h": "Chế độ làm việc (theo vendor Chemitreat)",
     "tb": [["", "Dây cation – khử CO₂ – anion", "Mixed bed (MBP)"],
            ["Số dây / bình", "3 (2 chạy + 1 dự phòng / tái sinh)", "3 (2 chạy + 1 dự phòng / tái sinh)"],
            ["Lưu lượng thường / tối đa", "150 / 170 m³/h mỗi dây", "200 / 210 m³/h mỗi bình"],
            ["Sản lượng giữa hai lần tái sinh", "1.800 m³ (nước thô, chu kỳ 12 h); 3.600 m³ (nước pha trộn, 24 h)", "24.000 m³ (chu kỳ 120 h)"],
            ["Thời gian tái sinh", "≈5,5 h kể cả xả thải (6 h nếu tái sinh kèm MBP)", "≈2 h"],
            ["Hóa chất mỗi lần tái sinh (100 %)", "H₂SO₄ 396 kg (cation); NaOH 480 kg (anion)", "H₂SO₄ 265 kg; NaOH 265 kg"]],
     "ul": ["Cation tái sinh ngược chiều (counter-flow): axit vào từ đáy, nồng độ 1,6 % rồi 4 %, đồng thời có dòng nước giữ lớp nhựa từ trên xuống. "
            "Anion tái sinh ngược chiều bằng NaOH 5 %. Cứ 7 lần tái sinh thì có 1 lần rửa ngược và 1 lần dùng gấp đôi hóa chất.",
            "Mixed bed: rửa ngược để phân lớp (nhựa cation nặng nằm dưới, anion nhẹ nằm trên), rồi tái sinh đồng thời: xút từ trên, axit từ dưới, thu về ống góp giữa. "
            "Sau đó rửa, trộn lại bằng khí nén 0,4 bar trong 10 phút, rửa lần cuối rồi đưa vào chạy.",
            "Nước tái sinh: cation dùng nước đã khử CO₂ (bể V2); anion và mixed bed dùng nước khử khoáng do bơm tái sinh P1A/B cấp."],
     "src": [V_DESC, V_CHEM, V_REG]},
    {"h": "Chất lượng nước",
     "kv": [["Nước thô thiết kế", "pH 7,8; độ cứng 71 mg/l CaCO₃; SiO₂ 12,5–15 mg/l; Cl⁻ 30–42 mg/l; clo dư 0,6 mg/l; TDS 70 mg/l"],
            ["Nước pha trộn (thô + nước ngưng)", "≈133 m³/h thiết kế; NH₃ ≈4,9 mg/l, urê ≈1,3 mg/l, methanol ≈7,2 mg/l; độ cứng ≈14,8 mg/l CaCO₃"],
            ["Nước ra khỏi anion", "Độ dẫn điện thường < 30 µS/cm, tốt nhất 2–5 µS/cm"],
            ["Nước khử khoáng (ra MBP)", "pH 6,5–7,0; độ dẫn điện < 0,2 µS/cm; SiO₂ < 0,02 mg/l; Fe < 0,02 mg/l; Na < 0,02 mg/l; ≈45 °C"]],
     "p": ["Cation cạn trước thì độ dẫn điện nước ra tăng, pH tăng (rò Na⁺ tạo NaOH). Anion cạn trước thì pH nước ra giảm. SiO₂ ít làm thay đổi độ dẫn điện nên phải phân tích riêng."],
     "src": [V_CHEM, V_MON]},
    {"h": "Điều khiển (PLC)",
     "ul": ["Toàn cụm điều khiển tự động bằng PLC Allen-Bradley (CPU và nguồn dự phòng kép, I/O từ xa qua ControlNet) trên tủ điều khiển chính có màn hình cảm ứng, còi và đèn báo. "
            "Có 11 hộp điều khiển tại thiết bị: 3 cho cation, 3 cho anion + khử CO₂, 3 cho MBP, 1 cho hố trung hòa, 1 cho khu tái sinh và Na₂SO₃.",
            "Van tái sinh là van màng hoặc van bướm khí nén, đóng mở qua van điện từ, có công tắc hành trình hiển thị trạng thái.",
            "Mỗi dây và mỗi MBP có công tắc chọn SERVICE / OFF / REGENERATION. Công tắc RAW WATER / BLENDED WATER chọn cách xử lý nước thải tái sinh.",
            "Tối đa 2 dây và 2 MBP cùng chạy. Mỗi lúc chỉ tái sinh 1 dây và 1 MBP. Nếu cùng chọn tái sinh một dây và một MBP thì dây tái sinh trước.",
            "Dây hoặc MBP tự dừng về standby khi đạt sản lượng đặt (tổng lưu lượng) hoặc khi độ dẫn điện cao (AIT ở đầu ra anion / MBP).",
            "Điều kiện cho phép tái sinh: không có tái sinh khác đang chạy; hố trung hòa còn đủ chỗ (theo LAL-31232); mức bể khử CO₂ (LT-31201) ≥ 80 %; bơm sau khử CO₂ và bơm tái sinh ở chế độ AUTO.",
            "Khởi động: nạp đầy bình và xả khí 1 phút, rửa tuần hoàn đến khi độ dẫn điện đạt (báo động sau 10 phút nhưng vẫn rửa tiếp), rồi chuyển sang chạy. Người vận hành có thể bỏ qua bước bằng nút ADVANCE."],
     "src": [V_CTRL, V_START]},
    {"h": "Nước thải tái sinh",
     "ul": ["Nước thải sạch (rửa ngược, rửa ống góp giữa, rửa lần cuối) xả thẳng ra 30-BA3001.",
            "Nước thải chứa hóa chất (giai đoạn bơm hóa chất và rửa hóa chất) về hố trung hòa lát gạch chịu axit. Theo vendor, hố có 2 ngăn × 250 m³: ngăn trung hòa và ngăn điều hòa.",
            "Khi chỉ dùng nước thô: sục khí, tuần hoàn và châm axit hoặc xút cho đến khi pH đạt 6–9 thì xả.",
            "Khi dùng nước pha trộn: nước thải chứa NH₃ và urê nên không trung hòa. Nước chỉ được sục trộn rồi bơm đi xử lý ở hệ nước thải 40-BA2001 / tháp stripping 40-T2001."],
     "src": [V_DESC, V_REV, V_CTRL]},
    {"h": "Sau revamp (2539)",
     "ul": ["Nước vào dây khử ion ở ≈41 °C. Nước ngưng turbine (10-E4001, 20-E1022) được làm mát xuống 45 °C ở 30-E-1001/1002, nhập với nước ngưng hơi Urê (20-E-1023), rồi qua 30-TK-1001 vào MBP.",
            "Bồn 30-TK-1001: 500 / 450 m³ (danh định / hữu ích), đóng vai trò đệm giữa khử ion và MBP. "
            "Bồn 30-TK-1002: 9.000 / 8.000 m³, đủ dự trữ khoảng 23 giờ tiêu thụ.",
            "Hệ vẫn đủ cấp nước khi phải cô lập 30-E-1001 do rò (chỉ còn 30-E-1002 chạy).",
            "Tái sinh có thể khởi động tự động theo thời gian, tự động khi nước ra không đạt (độ dẫn điện cao), hoặc bằng tay."],
     "src": [V_REV]},
    {"h": "Xử lý sự cố thường gặp (vendor)",
     "tb": [["Hiện tượng", "Nguyên nhân / xử lý"],
            ["Nước ra anion không đạt", "Cation hoặc anion cạn (kiểm tra pH và độ dẫn điện), nước vào thay đổi, thiếu hóa chất tái sinh, quạt khử CO₂ hỏng hoặc tháp bị ngập, lưu lượng quá lớn, nhựa bẩn, già hoặc thiếu"],
            ["Lưu lượng giảm", "Áp nước vào thấp, bơm sau khử CO₂ yếu, lớp nhựa tắc hoặc nhiều hạt mịn, màng van kẹt"],
            ["Ejector không hút hóa chất", "Van chưa mở đủ, ejector tắc, áp nước động lực thấp"],
            ["Rửa lâu", "Nhựa anion nhiễm hữu cơ, van bị rò"],
            ["Sản lượng giữa hai lần tái sinh giảm", "Tạo kênh trong lớp nhựa (lưới lọc hỏng), nhựa bẩn (cation rửa HCl, anion rửa nước muối kiềm), nhựa già hoặc thiếu"]],
     "src": [V_TS]},
]
UNIT31["src"] = [V_DESC, V_REV, V_CTRL]

for k, extra in {"30-PK-1001": [V_DESC, V_CTRL, V_CHEM, V_MECH], "30-PK-1001/V1": [V_DESC, V_REG], "30-PK-1001/V3": [V_DESC, V_REG],
                 "30-PK-1001/V4": [V_DESC, V_REG], "30-PK-1001/V2": [V_DESC], "30-PK-1001/BA1": [V_DESC], "30-TK-1001": [V_REV],
                 "30-TK-1002": [V_REV], "30-E-1001": [V_REV, V_E1001], "30-E-1002": [V_REV, V_E1002]}.items():
    TAGS31[k]["src"] = extra + TAGS31[k]["src"]
TAGS31["30-PK-1001/V1"]["intro"] += " Tái sinh ngược chiều: axit 1,6 % rồi 4 % vào từ đáy, có dòng nước giữ lớp nhựa từ trên xuống. Lượng H₂SO₄ ≈396 kg/lần (100 %)."
TAGS31["30-PK-1001/V3"]["intro"] += " Tái sinh ngược chiều bằng NaOH 5 % (≈480 kg/lần, 100 %), nước tái sinh lấy từ nước khử khoáng."
TAGS31["30-PK-1001/V4"]["intro"] += " Chu kỳ chạy ≈120 h, sản lượng ≈24.000 m³ giữa hai lần tái sinh; hóa chất mỗi lần ≈265 kg H₂SO₄ + 265 kg NaOH."
TAGS31["30-PK-1001/V2"]["intro"] += " Đệm là vòng pall polypropylene; quạt có lọc gió hút và damper đầu đẩy. Bể nước khử CO₂ còn cấp nước tái sinh cho bình cation."
TAGS31["30-E-1001"]["intro"] += " Thiết bị của Alfa Laval (cùng đơn hàng với 30-E-3001A/H và 20-E-1016/1017/1024)."
TAGS31["30-TK-1002"]["intro"] += " Dung tích hữu ích 8.000 m³, đủ dự trữ khoảng 23 giờ tiêu thụ."

UNIT35["s"] += [
    {"h": "Công suất thiết kế sau revamp",
     "kv": [["Khí điều khiển (instrument air)", "2.920 Nm³/h (DR-5001 1.820 + DR-5002 1.100), điểm sương −25 °C"],
            ["Khí công nghệ (plant air)", "2.680 Nm³/h"],
            ["Tổng nhu cầu tối đa", "5.600 Nm³/h, kể cả hao hụt tái sinh máy sấy ≈500 Nm³/h"],
            ["Máy nén", "4 máy chạy + 1 dự phòng, mỗi máy 1.400 Nm³/h, 9 barg, 45 °C"],
            ["Bình 30-V-5001 / 30-V-5002", "28,5 m³ / 154 m³; mỗi bình đủ cấp khoảng 10 phút (V-5002 tính khi áp giảm từ 8,1 xuống 5 barg)"],
            ["Tiêu thụ lớn", "Cụm Nitơ 30-PK-6001 tối đa 1.096 Nm³/h; khí thụ động hóa Urê 700 Nm³/h khi khởi động; dùng gián đoạn tối đa 150 Nm³/h"]],
     "src": [A_REV, A_VN]},
    {"h": "Vận hành & dự phòng",
     "ul": ["Máy nén khởi động và dừng tự động, lần lượt theo công tắc áp. Người vận hành chọn máy chạy và máy dự phòng bằng công tắc chọn tay.",
            "Khi thiếu khí, PIC-35003 đóng dần van PV-35003 trên header khí công nghệ, ưu tiên giữ áp cho khí điều khiển.",
            "Trước revamp, khí công nghệ từ máy nén 10-K-4021 (xưởng Amoniac) là nguồn dự phòng thường xuyên vào 30-V-5001. "
            "Sau revamp, xưởng Amoniac cần toàn bộ khí này nên không còn dự phòng thường xuyên.",
            "Nếu thiếu khí kéo dài (một máy hỏng trong khi máy dự phòng đang bảo dưỡng), người vận hành kích hoạt tay PIC-35001. "
            "Tín hiệu điều khiển 10-FIC-4001 / 10-FV-4001 lấy khí từ xưởng Amoniac (phải giảm tải Amoniac). Thực tế hai xưởng liên lạc trực tiếp để mở 10-FV-4001 kịp thời."],
     "src": [A_REV, A_VN]},
    {"h": "Máy nén Atlas Copco ZR",
     "ul": ["30-K-5001A–D: Atlas Copco ZR200-10-50. 30-K-5001E (mới): Atlas Copco dòng ZR. Đây là máy nén trục vít hai cấp, không dầu (oil-free), dẫn động motor điện, làm mát bằng nước, có vỏ cách âm.",
            "Khí qua lọc gió → cấp áp thấp → làm mát trung gian → cấp áp cao → làm mát sau → tách nước → ra 45 °C. Dầu chỉ bôi trơn bánh răng và ổ đỡ, không tiếp xúc với khí.",
            "Thông số (data sheet A–D): 1.400 Nm³/h; khí vào 36 °C, độ ẩm 99 %; ra 9 barg / 45 °C; tỉ số nén 9,9; công suất 204 kW; 1.485 v/ph; hiệu suất thể tích 75,8 %.",
            "Bộ điều khiển Elektronikon giữ áp trong khoảng đặt bằng cách cho máy chạy có tải hoặc không tải (full-load / no-load). Máy chạy không tải 3 giây trước khi dừng.",
            "Máy dừng bảo vệ khi: nhiệt độ khí ra cấp áp thấp hoặc áp cao vượt mức, nhiệt độ khí vào cấp áp cao cao, nhiệt độ dầu cao, áp dầu thấp, quá tải motor. Trước khi dừng có cảnh báo trên màn hình."],
     "src": [A_DS, A_DBDS, A_IB, A_KE, A_KEOM]},
    {"h": "Máy sấy khí điều khiển",
     "ul": ["Cả hai máy là loại hấp phụ không gia nhiệt (heatless, pressure-swing), gồm hai tháp luân phiên. "
            "Một tháp sấy khí; tháp kia được tái sinh bằng một phần khí khô hạ áp xuống gần áp khí quyển (purge), sau đó nạp lại áp trước khi đổi tháp.",
            "30-DR-5001: Delair PDH-0716. Điểm sương −25 °C ở 6,5 barg; chu kỳ 10 phút; khí tái sinh tối đa 360 Nm³/h; activated alumina 450 kg mỗi tháp.",
            "30-DR-5002: SPX Hankison (van chuyển AccuShift, bộ điều khiển có chức năng tiết kiệm khí purge). Ra 1.100 Nm³/h khí khô. "
            "Lọc trước 1 µm (một chạy, một dự phòng); lọc sau 0,01 µm để giữ bụi hạt hấp phụ. Có đầu đo ẩm liên tục ở đầu ra."],
     "src": [A_DS, A_D2, A_D2OM]},
]
UNIT35["src"] = [A_REV, A_VN]
TAGS35["30-K-5001"]["intro"] = ("Máy nén Atlas Copco ZR trục vít hai cấp không dầu, làm mát bằng nước: 1.400 Nm³/h, 9 barg, 45 °C, motor 200 kW (công suất hấp thụ 204 kW), 1.485 v/ph. "
                                "A–D (ZR200-10-50) có từ dự án gốc, E lắp mới khi revamp. 4 máy chạy + 1 dự phòng, khởi động và dừng lần lượt theo áp. "
                                "Bộ điều khiển Elektronikon cho máy chạy có tải hoặc không tải theo các bậc áp 8,4–9,0 barg (không tải ở 9,0–9,6 barg).")
TAGS35["30-K-5001"]["src"] = [A_DS, A_DBDS, A_IB, A_KE, A_KEOM] + TAGS35["30-K-5001"]["src"]
TAGS35["30-DR-5001"]["intro"] += " Delair PDH-0716: chu kỳ 10 phút, activated alumina 450 kg mỗi tháp, điểm sương −25 °C ở 6,5 barg."
TAGS35["30-DR-5001"]["src"] = [A_DS] + TAGS35["30-DR-5001"]["src"]
TAGS35["30-DR-5002"]["intro"] += " SPX Hankison: lọc trước 1 µm, lọc sau 0,01 µm (mỗi loại một chạy, một dự phòng), có đầu đo ẩm ở đầu ra."
TAGS35["30-DR-5002"]["src"] = [A_D2, A_D2OM] + TAGS35["30-DR-5002"]["src"]
TAGS35["30-V-5001"]["intro"] += " Dung tích danh định 28,5 m³, đủ cấp khí công nghệ khoảng 10 phút."
TAGS35["30-V-5002"]["intro"] += " Dung tích danh định 154 m³, đủ cấp khoảng 10 phút khi áp giảm từ 8,1 xuống 5 barg."
for k in ("30-V-5001", "30-V-5002"):
    TAGS35[k]["src"] = [A_REV] + TAGS35[k]["src"]
TAGS.update(TAGS31)
TAGS.update(TAGS35)
for x in "ABCDE":
    TAGS["30-K-5001" + x] = TAGS["30-K-5001"]
