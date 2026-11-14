"""Đường đi của các bơm (hút từ đâu → đẩy đến thiết bị nào), đọc trên P&ID (11/2026).

apply(tags) được ugt.apply gọi cuối cùng:
  - ROUTE[tag]: câu "Đường đi: …" chèn thành đoạn đầu intro của đoạn công nghệ đã có.
  - NEW[tag]: đoạn mới cho bơm chưa có đoạn riêng (bơm hóa chất, bơm dầu bôi trơn…).
  - ALIAS[motor] = bơm: motor dùng chung đoạn với bơm.
"""


def sh(dwg, label=None):
    return ["sheet:" + dwg, label or "P&ID " + dwg]


def ent(t, intro, src):
    return {"t": t, "intro": intro, "s": [], "src": src}


ROUTE = {
    # Unit 18
    "10-P-8001": "Hút từ bình chứa nước khử khí 10-V-8001 → đẩy nước cấp HHP (144 barg) sang lò hơi siêu cao áp/WHB của X.Amo (bao hơi 10-V-2001); dòng hồi lưu tối thiểu về 10-V-8001.",
    "10-P-8002": "Hút từ 10-V-8001 → đẩy nước cấp HP (60 barg) vào lò hơi phụ 10-B-8001 (qua FV-8251/LV-8250), lò hơi thu hồi nhiệt 10-B-9001, WHB X.Amo, X.UFC85 và nước giảm ôn (quench) của trạm giảm áp; hồi lưu tối thiểu về 10-V-8001.",
    "10-P-8003": "Hút từ bình nước ngưng 10-V-8004 → đẩy về thiết bị khử khí 10-PK-8004 / bình 10-V-8001.",
    # Unit 32
    "30-P-2001": "Hút từ bồn nước thô 30-TK-2001 → đẩy đến cụm Demi 30-PK-1001 (đầu vào bình cation 30-PK-1001/V1A/B/C, bồn NaOH TK8, bơm tái sinh P3), header nước công nghệ và bồn nước sinh hoạt 30-TK-2002 qua 30-PK-2001; hồi lưu về 30-TK-2001 qua FIC-32002.",
    "30-P-2002": "Hút từ bồn nước sinh hoạt 30-TK-2002 → đẩy qua lọc than hoạt tính 30-PK-2001/FL2 và lọc tinh /FL1 → header nước sinh hoạt toàn nhà máy; hồi lưu về 30-TK-2002.",
    "30-PK-2001/P1": "Hút từ bồn NaOCl 30-PK-2001/TK1 → châm vào đường nước sinh hoạt (qua bộ trộn tĩnh 30-PK-2001/2Z1) trước bồn 30-TK-2002.",
    "30-PK-2001/P2": "Hút từ bồn NaOCl 30-PK-2001/TK1 → châm sốc vào bồn nước sinh hoạt 30-TK-2002.",
    "30-PK-2001/P3": "Hút từ can/thùng NaOCl → nạp vào bồn 30-PK-2001/TK1.",
    "30-P-4001": "Hút từ đáy bồn 30-TK-2001 (6.000 m³ dự trữ chữa cháy) → đẩy vào mạng nước cứu hỏa toàn nhà máy (họng nước, hệ phun); đường tuần hoàn thử bơm về 30-TK-2001.",
    "30-P-4002": "Hút từ bồn 30-TK-2001 → đẩy vào mạng nước cứu hỏa để giữ áp > 7 barg.",
    # Unit 31
    "30-P-1001": "Hút từ bồn nước khử ion 30-TK-1001 → đẩy vào các bình trao đổi tầng hỗn hợp 30-PK-1001/V4A/B/C → bồn nước khử khoáng 30-TK-1002; hồi lưu tối thiểu về 30-TK-1001 (FIC-31001).",
    "30-P-1002": "Hút từ bồn nước khử khoáng 30-TK-1002 → đẩy đến thiết bị khử khí 10-PK-8004/10-V-8001 (qua trao đổi nhiệt X.Amo), các hộ dùng nước Demi của X.Amo/X.Urê, bình giãn nở 30-V-3001 và các cụm hóa chất; hồi lưu tối thiểu về 30-TK-1002.",
    "30-P-1003": "Bơm A: dỡ H₂SO₄ từ xe bồn → bồn 30-TK-1003. Bơm B: chuyển H₂SO₄ từ 30-TK-1003 → bồn đo axit 30-PK-1001/TK3/TK4 (tái sinh Demi), bồn axit tháp giải nhiệt 30-TK-3001 và 20-V-1040 (X.Urê); 30-P-1003B tự chạy/dừng theo tín hiệu yêu cầu của 3 hộ dùng.",
    "30-P-1004": "Dỡ NaOH từ xe bồn → bồn 30-TK-1004. Từ 30-TK-1004, xút tự chảy xuống bồn đo 30-PK-1001/TK5/TK6 và bồn NaOH trung hòa /TK8.",
    "30-PK-1001/P1": "Hút nước khử khoáng từ 30-TK-1002 → làm nước động lực cho ejector axit/xút 30-PK-1001/J1…J4, nước pha bồn Na₂SO₃ /TK7 và (từ 2021) nước làm mát máy nén khí 30-K-5001A~E.",
    "30-PK-1001/P2": "Hút từ bể chứa dưới tháp khử CO₂ 30-PK-1001/V2A/B/C → đẩy vào bình trao đổi anion 30-PK-1001/V3A/B/C (mỗi chuyền một bơm, LV-31201A/B/C giữ mức).",
    "30-PK-1001/P3": "Hút nước thô từ đầu đẩy bơm 30-P-2001A/B/C → rửa ngược và tái sinh bình cation 30-PK-1001/V1A/B/C.",
    "30-PK-1001/P5": "Hút từ hố trung hòa 30-PK-1001/BA1 → nước đã trung hòa xả sang bể nước sông làm mát 30-BA-3001; nếu nước nhiễm NH₃ thì chuyển sang bể cân bằng 40-BA-2001.",
    "30-PK-1001/P6": "Hút từ bồn Na₂SO₃ 30-PK-1001/TK7 → châm vào đường nước thô cấp cho cụm Demi (trước bình cation 30-PK-1001/V1A/B/C) để khử clo dư; tốc độ bơm điều khiển theo AI-31201.",
    "30-PK-1001/P7": "Hút từ bồn NaOH 30-PK-1001/TK8 → châm vào hố trung hòa 30-PK-1001/BA1.",
    "30-PK-1001/P8": "Hút từ bồn H₂SO₄ 30-PK-1001/TK9 → châm vào hố trung hòa 30-PK-1001/BA1.",
    # Unit 33
    "30-P-3001": "Hút từ bể tháp giải nhiệt 30-BA-3001 (A~D) / 30-BA-3003 (E) → header nước sông → bình ngưng tuabin X.Amo/X.Urê, bình ngưng NH₃, trao đổi nhiệt tấm 30-E-3001A~I → nước nóng về tháp 30-CT-3001A~L.",
    "30-P-3002": "Hút từ đường hồi nước sạch sau các trao đổi nhiệt tấm 30-E-3001A~I (áp hút giữ bằng bình giãn nở 30-V-3001) → header nước sạch làm mát cấp cho X.Amo, X.Urê, X.Phụ trợ → quay về 30-E-3001A~I.",
    "30-P-3003": "Hút từ bồn axit 30-TK-3001 → châm H₂SO₄ vào bể tháp giải nhiệt 30-BA-3001 và 30-BA-3003.",
    "30-P-3001A": "Hút từ bể tháp giải nhiệt 30-BA-3001 → header nước sông (cùng 30-P-3001B~E) → bình ngưng tuabin X.Amo/X.Urê, bình ngưng NH₃, trao đổi nhiệt tấm 30-E-3001A~I → về tháp 30-CT-3001A~L.",
    "30-P-3002A": "Hút từ đường hồi nước sạch sau 30-E-3001A~I → header nước sạch làm mát (cùng 30-P-3002B~D) → các hộ dùng X.Amo, X.Urê, X.Phụ trợ.",
    "30-P-3003A": "Hút từ bồn axit 30-TK-3001 → châm H₂SO₄ vào bể tháp giải nhiệt 30-BA-3001 và 30-BA-3003.",
    "30-P-3010": "Hút từ trạm bơm nước sông ngoài hàng rào → cụm lọc 30-PK-3006 → bể tháp 30-BA-3001/3003; một phần làm nguội kênh xả.",
    # Unit 42
    "40-PK-2001/P1": "Hút từ bể nước đã tách dầu 40-PK-2001/BA1 → thiết bị tách CPI 40-PK-2001/V4 → bồn trộn nhanh /TK3.",
    "40-PK-2001/P2": "Hút từ bể dự phòng 40-PK-2001/BA2 → bể tách dầu API 40-PK-2001/V1.",
    "40-PK-2001/P3": "Hút từ bể dầu 40-PK-2001/BA3 → thiết bị đông tụ (coalescer) 40-PK-2001/V2.",
    "40-PK-2001/P5": "Bơm /P5A/B hút từ bồn phụ 40-PK-2001/V3 (chất phá nhũ pha ở /TK1) → bồn trộn nhanh 40-PK-2001/TK3. Bơm khí /P6 chuyển hóa chất từ phuy → /TK1.",
    "40-PK-2001/P6": "Bơm khí /P6 chuyển chất phá nhũ từ phuy → bồn 40-PK-2001/TK1. Bơm /P5A/B châm từ /V3 → bồn trộn nhanh /TK3.",
    "40-PK-2001/P9": "Bơm /P9A/B hút từ bồn phụ 40-PK-2001/V8 (chất keo tụ pha ở /TK6) → bồn keo tụ 40-PK-2001/TK4. Bơm khí /P10 chuyển hóa chất từ phuy → /TK6.",
    "40-PK-2001/P10": "Bơm khí /P10 chuyển chất keo tụ từ phuy → bồn 40-PK-2001/TK6. Bơm /P9A/B châm từ /V8 → bồn keo tụ /TK4.",
    "40-PK-2001/P7": "Hút nước sạch sau tuyển nổi → bình bão hòa khí 40-PK-2001/V5 → xả áp vào thiết bị tuyển nổi 40-PK-2001/Z5.",
    "40-PK-2001/P8": "Hút từ bồn chứa cuối 40-PK-2001/TK5 → bể điều hòa TK-102 của 40-PK-2003 (thiết kế gốc: qua lọc /V6, /V7 rồi ra ngoài).",
    "40-PK-2002/P1": "Hút từ bể cân bằng 40-PK-2002/BA1 → bể oxy hóa 40-PK-2002/BA2A/B.",
    "40-PK-2002/P2": "Hút bùn từ bể ổn định bùn 40-PK-2002/BA4 → tuần hoàn về bể oxy hóa 40-PK-2002/BA2A/B.",
    "40-PK-2002/P3": "Hút bùn từ bể lên men hiếu khí 40-PK-2002/BA6A (/P3A/B) và /BA6B (/P3C/D) → đầu nối xe bồn để chở đi chôn lấp.",
    "40-PK-2002/P4": "Hút từ bể clo hóa 40-PK-2002/BA5 → bộ lọc đa lớp 40-PK-2002/FL1 → bể nước lọc /BA7.",
    "40-PK-2002/P5": "Hút từ bể nước lọc 40-PK-2002/BA7 → rửa ngược lọc 40-PK-2002/FL1 (nước rửa về bể cân bằng /BA1) và nước phun dập bọt cho bể oxy hóa /BA2A/B.",
    "40-PK-2002/P6": "Hút từ bể nước sạch 40-PK-2002/BA8 → xả nước thải đạt chuẩn ra ranh giới nhà máy (KCN).",
    "40-PK-2002/P9": "Hút từ bể nước sạch 40-PK-2002/BA8 → xả ra ranh giới nhà máy (KCN); từ 12/2025 có đường tuần hoàn về /BA8 (đầu dò pH 40-AI-42218B đặt trên đường này).",
    "40-PK-2002/P8": "Hút nước mưa đọng ở hố van 40-PK-2002/BA9 → đưa về hệ thống xử lý của cụm.",
    "40-P-2001": "Hút từ bể cân bằng 40-BA-2001 → trao đổi nhiệt 40-E-2001 → tháp tách NH₃ 40-T-2001 (đã ngừng).",
    "40-P-2002": "Hút nước đáy tháp 40-T-2001 → trao đổi nhiệt 40-E-2001 → bể nước sông 30-BA-3001 (đã ngừng).",
    # Unit 45
    "40-P-5001": "Hút NH₃ lỏng từ bồn 40-TK-5001 → đường NH₃ lỏng cấp cho X.Urê.",
    "40-P-5002": "Hút NH₃ lỏng từ bồn 40-TK-5001 → bộ gia nhiệt 40-E-5001 → cần nạp xe bồn 40-LA-5001 (dự phòng 40-LA-5005).",
    "40-P-5003": "Hút NH₃ lỏng từ bồn 40-TK-5001 → bộ gia nhiệt 40-E-5002 → cần nạp xe bồn 40-LA-5003 (dự phòng 40-LA-5005).",
}

S18a, S18b, S18c = sh("2539-18-PID-0031-02"), sh("2539-18-PID-0031-06"), sh("2098-18-PID-0031-02")
NEW = {
    "10-PK-8001/P1": ent("Bơm châm phosphate cho lò hơi phụ 10-PK-8001/P1A/B",
        "Đường đi: hút dung dịch phosphate từ bồn 10-PK-8001/V1A/B → châm vào bao hơi lò hơi phụ 10-B-8001.\n"
        "Bơm định lượng (1 chạy, 1 dự phòng): 0,017 m³/h, đẩy 46 barg, 0,15 kW, 70 lần/ph; motor 10-PK-8001/MP1A/B. Van an toàn đặt 50 barg, có cột hiệu chuẩn CP-1.", [S18a]),
    "10-PK-8001/P2": ent("Bơm châm phosphate cho HRSG 10-PK-8001/P2A/B",
        "Đường đi: hút dung dịch phosphate từ bồn 10-PK-8001/V1A/B → châm vào lò hơi thu hồi nhiệt 10-B-9001 (HRSG).\n"
        "Bơm định lượng (1 chạy, 1 dự phòng): 0,017 m³/h, đẩy 46 barg, 0,15 kW, 70 lần/ph; motor 10-PK-8001/MP2A/B. Van an toàn đặt 50 barg, có cột hiệu chuẩn CP-2.", [S18a]),
    "10-PK-8001/P3": ent("Bơm châm phosphate cho X.Amo 10-PK-8001/P3A/B/C",
        "Đường đi: hút dung dịch phosphate từ bồn 10-PK-8001/V1A/B → châm vào bao hơi 10-V-2001 của lò hơi X.Amo.\n"
        "Bơm định lượng: 0,039 m³/h, đẩy 120 barg, 0,7 kW, 87 lần/ph; motor 10-PK-8001/MP3A/B/C. Van an toàn đặt 130 barg, có cột hiệu chuẩn CP-3/CP-4.", [S18a]),
    "10-PK-8001/P4": ent("Bơm châm phosphate cho 10-E-5000 – 10-PK-8001/P4A/B",
        "Đường đi: hút dung dịch phosphate từ bồn 10-PK-8001/V1B → châm vào 10-E-5000 (X.Amo). Lắp thêm khi revamp.\n"
        "Bơm định lượng: 4,58 l/h, đẩy 120 barg, 0,1 kW, 117 lần/ph; motor 10-PK-8001/MP4A/B. Van an toàn đặt 130 barg, có cột hiệu chuẩn CP-4A/4B.", [S18b]),
    "10-PK-8002/P1": ent("Bơm châm chất kiềm hóa 10-PK-8002/P1A/B",
        "Đường đi: hút chất kiềm hóa (filming amine) từ bồn 10-PK-8002/V1 → châm vào bình chứa nước khử khí 10-V-8001.\n"
        "Bơm định lượng (1 chạy, 1 dự phòng): 0–0,061 m³/h, đẩy 8 barg, 0,15 kW, 87 lần/ph; motor 10-PK-8002/MP1A/B. Van an toàn đặt 10 barg.", [S18c]),
    "10-PK-8003/P1": ent("Bơm châm chất khử oxy 10-PK-8003/P1A/B",
        "Đường đi: hút chất khử oxy từ bồn 10-PK-8003/V1 → châm vào bình chứa nước khử khí 10-V-8001.\n"
        "Bơm định lượng (1 chạy, 1 dự phòng): 0–0,039 m³/h, đẩy 8 barg, 0,15 kW, 87 lần/ph; motor 10-PK-8003/MP1A/B. Van an toàn đặt 10 barg.", [S18c]),
    "10-P-8004": ent("Bơm thùng hóa chất 10-P-8004",
        "Đường đi: hút từ phuy 200 l (chất kiềm hóa, chất khử oxy, phosphate) → nạp vào bồn 10-PK-8002/V1, 10-PK-8003/V1 và bồn phosphate 10-PK-8001/V1A/B.\n"
        "Bơm thùng chạy bằng khí nén (plant air).", [S18c, S18a]),
    "20-P-1018": ent("Bơm nước ngưng tuabin 20-P-1018A/B (X.Urê)",
        "Đường đi: nước ngưng tuabin của X.Urê (cùng nước ngưng từ 10-P-4001A/B của X.Amo) → làm mát qua 30-E-1001/30-E-1002 → bồn nước khử ion 30-TK-1001. Bơm thuộc X.Urê, chỉ thể hiện trên P&ID Demi ở đầu vào.", [sh("2539-31-PID-0031-01")]),
    "30-P-3001A/P2": ent("Bơm dầu bôi trơn phụ 30-P-3001A/P2",
        "Đường đi: hút dầu từ thùng 30-P-3001A/V1 → làm mát 30-P-3001A/E1 → lọc kép /FL1A/B → gối đỡ bơm 30-P-3001A, hộp số và tuabin 30-STP-3001A → dầu về /V1.\n"
        "Bơm bánh răng 6,54 m³/h, 6 bar, 3 kW (motor /MP2), tự chạy khi áp dầu thấp (PAL). Bơm dầu chính /P1 (cùng lưu lượng) dẫn động từ trục. Theo ghi chú P&ID 06/2018, tuabin đã bỏ khi revamp (bơm chạy motor).", [sh("2098-33-PID-0031-04")]),
    "30-P-3001A/P3": ent("Bơm dầu chính hộp số góc vuông 30-P-3001A/P3",
        "Đường đi: hút dầu từ thùng dầu hộp số góc vuông của 30-P-3001A → làm mát /E2 → lọc kép /FL2A/B → hộp số góc vuông → dầu về thùng.\n"
        "Bơm bánh răng 2,52 m³/h, 6 bar, dẫn động từ trục (740 v/ph). Bơm phụ /P4 (1,1 kW, motor /MP4) tự chạy khi áp dầu thấp.", [sh("2098-33-PID-0031-04")]),
    "30-P-3002A/P1": ent("Bơm dầu bôi trơn 30-P-3002A/P1, /P2",
        "Đường đi: hút dầu từ thùng 30-P-3002A/V1 → làm mát 30-P-3002A/E1 → lọc kép /FL1A/B → gối đỡ bơm 30-P-3002A, hộp số và tuabin 30-STP-3002A → dầu về /V1.\n"
        "/P1 là bơm chính (bánh răng 4,2 m³/h, 3 bar, dẫn động từ trục); /P2 là bơm phụ (4,6 m³/h, 1,1 kW, motor /MP2) tự chạy khi áp dầu thấp. Theo ghi chú P&ID 06/2018, tuabin đã bỏ khi revamp.", [sh("2098-33-PID-0031-07")]),
    "30-PK-3001/P1": ent("Bơm chuyển NaOCl 30-PK-3001/P1A/B/C (đã bỏ)",
        "Đường đi: hút NaOCl 2.000 ppm từ bồn 30-PK-3001/TK1 → châm liên tục vào các khoang tháp giải nhiệt 30-CT-3001A~J (và đường nạp/xuất NaOCl).\n"
        "Bơm ly tâm 10 m³/h, 30 m, 3 kW. Cụm sản xuất hypochlorite đã bị bỏ (ghi chú trên P&ID).", [sh("2098-33-PID-0031-04")]),
    "30-PK-3001/P2": ent("Bơm rửa axit 30-PK-3001/P2 (đã bỏ)",
        "Đường đi: hút HCl loãng từ bồn rửa axit 30-PK-3001/TK2 → tuần hoàn qua bộ điện phân 30-PK-3001/Z2A/B để rửa cặn → về /TK2.\n"
        "Bơm ly tâm 6 m³/h, 15 m, 3 kW. Cụm đã bị bỏ.", [sh("2098-33-PID-0031-04")]),
    "30-PK-3001/P5": ent("Bơm tăng áp nước sông 30-PK-3001/P5A/B (đã bỏ)",
        "Đường đi: nước sông qua lọc tự động 30-PK-3001/Z3 → bơm /P5A/B → bộ điện phân 30-PK-3001/Z2A/B.\n"
        "Bơm ly tâm 10 m³/h, 30 m, 3 kW. Cụm đã bị bỏ.", [sh("2098-33-PID-0031-04")]),
    "30-PK-3002/P1R": ent("Bơm châm chất chống cáu cặn 30-PK-3002/P1RA/B",
        "Đường đi: hút chất chống cáu cặn từ thùng 30-PK-3002/V1 → châm vào bể tháp giải nhiệt 30-BA-3001 và 30-BA-3003.\n"
        "Bơm màng 10 l/h, 2,5 barg, 0,25 kW, 117 lần/ph (1 chạy, 1 dự phòng), lắp mới khi revamp. Ở chế độ remote hành trình bơm theo FIC-33001.", [sh("2539-33-PID-0031-05")]),
    "30-PK-3002/P2": ent("Bơm thùng hóa chất 30-PK-3002/P2",
        "Đường đi: hút từ phuy 200 l → nạp chất chống cáu cặn vào thùng 30-PK-3002/V1, và chất ức chế ăn mòn vào thùng 30-PK-3003/V1.\n"
        "Bơm màng chạy bằng khí nén (plant air), 2,1 m³/h, 30 m.", [sh("2539-33-PID-0031-05"), sh("2098-33-PID-0031-08")]),
    "30-PK-3003/P1": ent("Bơm châm chất ức chế ăn mòn 30-PK-3003/P1A/B",
        "Đường đi: hút chất ức chế ăn mòn từ thùng 30-PK-3003/V1 → châm vào đầu hút bơm nước sạch 30-P-3002A~C (vòng kín nước sạch làm mát).\n"
        "Bơm màng 0,044 m³/h, 30 m, 0,25 kW, 112 lần/ph (1 chạy, 1 dự phòng); van giữ áp 4 barg.", [sh("2098-33-PID-0031-08")]),
    "30-PK-3005/P1": ent("Bơm châm chất keo tụ 30-PK-3005/P1A/B",
        "Đường đi: hút chất keo tụ từ thùng 30-PK-3005/V1 → châm vào nước rửa ngược của 30-PK-3006 trước bể lắng 30-BA-3004.\n"
        "Bơm màng 4,63 l/h, 0,25 kW, 30 lần/ph; van an toàn đặt 6 barg.", [sh("2539-33-PID-0031-14")]),
    "30-PK-3005/P2": ent("Bơm châm chất trợ keo tụ 30-PK-3005/P2A/B",
        "Đường đi: hút chất trợ keo tụ (polymer) từ thùng 30-PK-3005/V2 → châm vào nước rửa ngược của 30-PK-3006 trước bể lắng 30-BA-3004.\n"
        "Bơm màng 2,54 l/h, 0,25 kW, 46 lần/ph; van an toàn đặt 6 barg.", [sh("2539-33-PID-0031-14")]),
    "30-K-5001A/P1": ent("Bơm dầu máy nén khí 30-K-5001/P1",
        "Đường đi: hút dầu từ thùng dầu 30-K-5001/TK1 → làm mát dầu /E2 → lọc dầu /FL2 → gối đỡ và hộp số máy nén → dầu về /TK1.\n"
        "Bơm gerotor dẫn động từ trục máy nén, 4 m³/h, 3 bar. Bảo vệ áp dầu thấp PAL/PALL-35204.", [sh("2098-35-PID-0031-01")]),
    "40-PK-2002/P7": ent("Bơm châm NaOCl 40-PK-2002/P7A/B",
        "Đường đi: hút NaOCl từ bồn 40-PK-2002/TK1 (755 l, nạp tay từ 30-TK-3002) → châm vào bể clo hóa 40-PK-2002/BA5.\n"
        "Bơm màng 17,5 l/h, 6 bar, 0,25 kW (1 chạy, 1 dự phòng); van an toàn đặt 5 barg.", [sh("2098-42-PID-0031-03")]),
    "40-PK-5001/P1": ent("Bơm dầu bôi trơn 40-PK-5001/P1A/B",
        "Đường đi: hút dầu từ bình tách dầu 40-PK-5001/V3 → làm mát 40-PK-5001/E2 → lọc /FL1A/B → máy nén NH₃ 40-PK-5001/K1A/B (bôi trơn, làm kín) → dầu theo hơi nén về /V3.\n"
        "Bơm bánh răng 4.600 kg/h, cột áp 25 m, motor /MP1A/B; bơm dầu chạy trước khoảng 10 s khi khởi động máy nén, bơm dự phòng tự chạy khi bơm chính hỏng.", [sh("2098-45-PID-0031-03")]),
    "40-PK-5005/P1": ent("Bơm dầu 40-PK-5005/P1A/B",
        "Đường đi: hút dầu từ bình tách dầu 40-PK-5005/V3A (/V3B) → làm mát /E2A (/E2B) → lọc /FL1A (/FL1B) → máy nén 40-PK-5005/K1A (/K1B). Mỗi máy nén có một bơm riêng.\n"
        "Bơm chỉ chạy khi PLC thấy nhu cầu dầu tăng; motor /MP1A/B.", [sh("2539-45-PID-0031-05")]),
}
# tag đầy đủ của bơm/motor dùng chung đoạn
ALIAS = {
    "10-MP-8001": "10-P-8001", "10-MP-8002": "10-P-8002", "10-MP-8003": "10-P-8003", "30-MP-2001": "30-P-2001", "30-MP-2002": "30-P-2002",
    "30-PK-3005/P1B": "30-PK-3005/P1",
    "30-PK-3002/P1RA": "30-PK-3002/P1R", "30-PK-3002/P1RB": "30-PK-3002/P1R",
    "30-PK-3002/MP1RA": "30-PK-3002/P1R", "30-PK-3002/MP1RB": "30-PK-3002/P1R",
    "30-P-3002A/P2": "30-P-3002A/P1", "30-P-3002A/MP2": "30-P-3002A/P1",
    "30-P-3001A/P4": "30-P-3001A/P3", "30-P-3001A/MP4": "30-P-3001A/P3", "30-P-3001A/MP2": "30-P-3001A/P2",
    "30-P-3003A/P1": "30-P-3001A/P2",  # nhãn "30-P3003A/P1" ở Detail A trên P&ID dầu bôi trơn 30-P-3001A (bơm dầu chính)
    "30-K-5001B/P1": "30-K-5001A/P1", "30-K-5001C/P1": "30-K-5001A/P1",
}


def apply(tags):
    for k, txt in ROUTE.items():
        if k in tags:
            old = tags[k]
            e = dict(old)
            e["intro"] = "Đường đi: " + txt[0].lower() + txt[1:] + ("\n" + e["intro"] if e.get("intro") else "")
            for kk, v in list(tags.items()):  # motor/bơm dùng chung đoạn
                if v is old:
                    tags[kk] = e
    tags.update(NEW)
    for a, b in ALIAS.items():
        tags[a] = tags[b]
