"""Công nghệ Unit 31 (nước khử khoáng – Demi) và Unit 35 (khí nén điều khiển & khí công nghệ).

Nguồn: PFD as-built 2539-31/35-PFD-0010-01-01 (cân bằng vật chất case 2/case 3) và bảng thông số
thiết bị trên các P&ID 2098/2539-31-PID-0031-01…09, 2098/2539-35-PID-0031-01…06.
Chưa dùng tài liệu vendor (thư mục "4. Demi", "7. Air System") – bổ sung khi đã có danh mục.
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
                "Sau đó nhập với nước ngưng hơi từ 20-E1023 (25,9 t/h) thành 187,2 t/h vào 30-TK-1001. Na₂SO₃ được châm vào dòng nước khử ion.",
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
                "Na₂SO₃: bồn khuấy TK7 (6,28 m³) và bơm màng P6A/B (0,01 m³/h) châm vào nước khử ion để khử oxy hòa tan."],
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
                          "Bồn 6,28 m³ (Ø2.000 × 2.000 mm) có khuấy Z1. Bơm màng P6A/B (0,01 m³/h, 50 m, 0,25 kW) châm Na₂SO₃ vào nước khử ion để khử oxy.", src=[D6, D_PFD]),
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
