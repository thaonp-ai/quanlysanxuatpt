"""Công nghệ Unit 33 (nước làm mát: nước sông & nước sạch) và Unit 42 (xử lý nước thải, gồm cả Unit 43 thu gom nước thải/nước mưa).

Nguồn Unit 33: PFD 2539-33-PFD-0010-01-01/02 as-built (bảng dòng, bảng thiết bị, ghi chú), P&ID 2539/2098-33-PID-0031-xx,
mô tả công nghệ revamp 2539-33-CN-0009-01, mô tả liên động 2539-33-CN-0009-02 & C&E 2539-33-NM-0013-01,
triết lý điều khiển 30-PK-3006 (2539-0848-01-A0101-001 rev B), quy trình G2-30-QT-045 lần 3 (scan → OCR),
giáo trình G2-30-GT-02 "Nước làm mát & nước NHR" (bản Word Rev01), mô tả công nghệ & liên động 30-PK-3002/3003 (GE Betz).
Nguồn Unit 42: PFD 2098-42-PFD-0010-1/2, P&ID 2098/2539-42-PID-0031-01…06, 2539-43-PID-0031-01 (bảng thiết bị, ghi chú 12/2025),
giáo trình G2-30-GT-05 "Hệ thống xử lý nước thải" (bản Word Rev01), sổ tay vận hành trạm XLNT mới (2012),
phương án G2-00-PA-174 lần 3 (12/2023), tờ trình 24-143/TTr-CNSX (08/2024) về nước thải UFC85.
"""
NLM = "Nuoc lam mat/"
REV = NLM + "Revamp_COOLING WATER SYSTEM_revamp/"
WW = "9. Xử lý nước thải/"
GTN = "Giáo trình_New/"


def sh(dwg, label):
    return ["sheet:" + dwg, label]


def ent(t, intro, s=None, src=None):
    return {"t": t, "intro": intro, "s": s or [], "src": src or []}


# ======================================================================= Unit 33
PFD1 = sh("2539-33-PFD-0010-01-01 (trang 1)", "PFD 2539-33 tờ 1/2 (as-built)")
PFD2 = sh("2539-33-PFD-0010-01-02 (trang 1)", "PFD 2539-33 tờ 2/2 (as-built)")
PID_BA = sh("2539-33-PID-0031-01", "P&ID 33-01 Bể tháp & nước bổ sung")
PID_NHR = sh("2098-33-PID-0031-01", "P&ID trạm bơm nước sông ngoài hàng rào")
PID_P1 = sh("2539-33-PID-0031-02", "P&ID 33-02 Bơm nước sông 30-P-3001A–D")
PID_HDR = sh("2539-33-PID-0031-03", "P&ID 33-03 Header nước sông")
PID_LO = sh("2098-33-PID-0031-04", "P&ID 33-04 Dầu bôi trơn 30-P-3001A (cũ)")
PID_CHEM = sh("2539-33-PID-0031-05", "P&ID 33-05 Hóa chất nước sông")
PID_F1 = sh("2539-33-PID-0031-06", "P&ID 33-06 Nước sạch làm mát (1/4)")
PID_F2 = sh("2539-33-PID-0031-07", "P&ID 33-07 Nước sạch làm mát (2/4)")
PID_F3 = sh("2098-33-PID-0031-07", "P&ID 33-07 Nước sạch – bơm 30-P-3002A (tuabin cũ)")
PID_F4 = sh("2098-33-PID-0031-08", "P&ID 33-08 Nước sạch – 30-PK-3003")
PID_NEW = sh("2539-33-PID-0031-09", "P&ID 33-09 Tháp K/L & bơm 30-P-3001E")
PID_FIL = sh("2539-33-PID-0031-11", "P&ID 33-11 Cụm lọc 30-PK-3006")
PID_SB = sh("2539-33-PID-0031-12", "P&ID 33-12 Bể lắng 30-BA-3004")
PID_CF = sh("2539-33-PID-0031-14", "P&ID 33-14 Cụm keo tụ 30-PK-3005")

S_CN = [REV + "1. PROCESS DESCRIPTION/2539-33-CN-0009-01_0.pdf", "2539-33-CN-0009-01 Mô tả công nghệ (revamp)"]
S_ILK = [REV + "5. Tài Liệu Tham Khảo/INTERLOCK PROCESS DESCRIPTION/2539-33-CN-0009-02_0.pdf", "2539-33-CN-0009-02 Mô tả liên động"]
S_CE = [REV + "5. Tài Liệu Tham Khảo/INTERLOCK PROCESS DESCRIPTION/2539-33-NM-0013-01_0.pdf", "2539-33-NM-0013-01 Cause & Effect"]
S_QT = [REV + "G2-30-QT-045-L3.pdf", "Quy trình vận hành nước sông làm mát G2-30-QT-045"]
S_GT = [GTN + "STVB102393_G2-30-GT-02 GT dao tao HT nuoc lam mat - nuoc NHR_vps.pdf", "Giáo trình G2-30-GT-02 Nước làm mát & NHR"]
S_CP6 = [REV + "5. Tài Liệu Tham Khảo/2539-0848-01-A0101-001_B_Code 1.pdf", "30-PK-3006 · Triết lý điều khiển (rev B)"]
S_SP6 = [REV + "4. DATASHEET/30-PK-3006/2539-33-SP-0848-03_PA.pdf", "Yêu cầu kỹ thuật 30-PK-3006"]
S_CTKL = [REV + "4. DATASHEET/30-CT-3001 K-L/2539-33-SP-0310-01_PB.pdf", "Data sheet tháp 30-CT-3001K/L"]
S_CTDS = [NLM + "30-CT-3001A-J (MR-0311-50)/DOC/003Ctdata172.XLS", "Data sheet tháp 30-CT-3001A–J"]
S_CTOP = [NLM + "30-CT-3001A-J (MR-0311-50)/DOC/021Oper172.xls", "Hướng dẫn vận hành tháp giải nhiệt"]
S_P1E = [REV + "4. DATASHEET/30-P-3001 E/2539-33-SP-0910-01_A.pdf", "Data sheet bơm 30-P-3001E"]
S_P1A = [REV + "4. DATASHEET/30-P-3001 A/2539-33-SP-0910-02_PB.pdf", "Data sheet bơm 30-P-3001A (revamp)"]
S_P2A = [REV + "4. DATASHEET/30-P-3002 A/2539-33-SP-0910-03_PB.pdf", "Data sheet bơm 30-P-3002A (revamp)"]
S_BA3 = [REV + "4. DATASHEET/30-BA-3003/2539-33-SP-0271-01_PB.pdf", "Data sheet bể 30-BA-3003"]
S_BA4 = [REV + "4. DATASHEET/30-BA-3004/2539-33-SP-0271-02_PB.pdf", "Data sheet bể lắng 30-BA-3004"]
S_E31 = [NLM + "30-E-3001A-H (MR-0660-60)/Tag 3.pdf", "Alfa Laval · Data sheet TĐN tấm"]
S_E34 = [NLM + "30-E-3001A-H (MR-0660-60)/Tag 4.pdf", "Alfa Laval · Hướng dẫn lắp đặt, vận hành, bảo dưỡng"]
PKB = NLM + "30-PK-3002 & 3003 (MR-4046-50)/VENDOR DATA BOOK/"
S_PKP = [PKB + "PROCESS.doc", "30-PK-3002/3003 · Mô tả công nghệ (GE Betz)"]
S_PKI = [PKB + "interlock.doc", "30-PK-3002/3003 · Liên động"]
S_PK3S = [PKB + "Start-up-3003.doc", "30-PK-3003 · Quy trình khởi động"]
S_PK2S = [PKB + "Start-up-3002.doc", "30-PK-3002 · Quy trình khởi động"]
S_RUN_A = [NLM + "30-P-3001ABCD/Thông số chạy thử 30-P3001A.pdf", "Thông số chạy thử 30-P-3001A"]
S_RUN_E = [NLM + "30-P-3001ABCD/Thông số chạy thử 30-P3001E.pdf", "Thông số chạy thử 30-P-3001E"]
S_RDY6 = [REV + "Ready for commissioning 30pk3006.pdf", "Thông báo sẵn sàng chạy thử 30-PK-3006"]

UNIT33 = {
    "t": "Công nghệ Unit 33 – Nước làm mát (nước sông & nước sạch)",
    "intro": "Hệ thống làm mát gián tiếp hai vòng. Vòng hở nước sông (River Cooling Water, RCW) tuần hoàn qua tháp giải nhiệt 30-CT-3001A~L. "
             "Nước sông làm mát trực tiếp các bình ngưng tuabin hơi của X.Amonia/X.Urê, thiết bị ngưng tụ NH₃ (titan) và một số thiết bị khác. "
             "Phần còn lại giải nhiệt cho vòng kín nước sạch (Fresh Cooling Water, FCW – nước khử khoáng có chất ức chế ăn mòn) qua 9 TĐN tấm 30-E-3001A~I. "
             "Vòng kín FCW cấp cho các hộ tiêu thụ Amonia, Urê, Phụ trợ và cụm thu hồi CO₂. Nhờ vòng kín, các thiết bị trao đổi nhiệt này dùng được thép cacbon "
             "(không dùng đồng vì có thể lẫn NH₃). Dự án revamp 2016–2018 (1620 MTPD NH₃) bổ sung: 2 khoang tháp K/L, bể 30-BA-3003, bơm 30-P-3001E, "
             "cụm lọc nước bổ sung & side stream 30-PK-3006, bể lắng 30-BA-3004, cụm keo tụ 30-PK-3005; đồng thời thay tuabin hơi của 30-P-3001A và 30-P-3002A bằng motor điện.",
    "s": [
        {"h": "Sơ đồ dòng (PFD as-built)",
         "ul": ["Nước sông bổ sung từ trạm bơm ngoài hàng rào 30-P-3010A/B (2 × 4.100 m³/h, 34 m) đi qua 6 skid lọc MUF của 30-PK-3006, "
                "rồi vào bể 30-BA-3001 qua van mức LV-33001 (LIC-33001). Đường bypass cụm lọc bình thường đóng.",
                "Bể 30-BA-3001 (5.000 m³, 10 khoang tháp cũ) và 30-BA-3003 (2 khoang mới) nối nhau bằng mương ngầm có 2 van cửa (sluice gate), có thể tách riêng khi bảo dưỡng. "
                "Thời gian lưu tối thiểu 10 phút theo lưu lượng tuần hoàn thiết kế.",
                "Bơm 30-P-3001A~D (trong 30-BA-3001) và 30-P-3001E (trong 30-BA-3003) đẩy nước sông vào header chung, dòng 33.7 ≈31.860 t/h (case 2). Dòng chia ra:",
                "• 15.437 t/h qua TĐN tấm 30-E-3001A~I (dòng 33.3);",
                "• 11.657 t/h tới X.Amonia và 3.460 t/h tới X.Urê (33.16/33.18);",
                "• 1.305 t/h lấy từ header đi lọc side stream (33.51), trong đó 1.125 t/h quay về bể và 180 t/h dùng rửa ngược.",
                "Nước nóng 43 °C hồi về đỉnh tháp 30-CT-3001A~L (dòng 33.8, 30.554 t/h). Tại tháp, mất mát do bay hơi ≈443 t/h và cuốn theo 1,4 t/h. "
                "Xả đáy (blowdown) 2.216 t/h ra sông qua FV-33002. FIC-33002 được hiệu chỉnh tầng (cascade) bởi bộ đo độ dẫn AIC-33003 trên đường hồi.",
                "Đường tuần hoàn từ header đẩy về 30-BA-3001 qua van tay HV-33003 giúp bơm chạy gần điểm định mức khi nhu cầu nước sông thay đổi.",
                "Vòng FCW: 30-P-3002A~D (thường chạy 2 bơm) hút từ đường hồi qua TĐN tấm, đẩy 16.416 t/h ở 37 °C, 6 barg (dòng 33.1) tới các hộ tiêu thụ. Phân bố:",
                "• Amonia 5.524 t/h; Urê 8.527 t/h; Phụ trợ 477 t/h; CDRP (thu hồi CO₂) 1.888 t/h.",
                "• Nước hồi 45–46 °C, 3–4 barg (33.2).",
                "Bình giãn nở 30-V-3001 đặt trên đường hồi FCW: hấp thụ giãn nở nhiệt, giữ áp đầu hút và tách khí lọt vào khi rò ống ở xưởng. "
                "Nước khử khoáng bổ sung 6,9 t/h (33.27). Nitơ đệm áp qua PIC-33101A/B (split range)."],
         "src": [PFD1, PFD2, S_CN, S_GT]},
        {"h": "Chỉ tiêu công nghệ",
         "tb": [["Thông số", "Nước sông (RCW)", "Nước sạch (FCW)"],
                ["Nhiệt độ đi / về", "34 / 43 °C", "37 / 46 °C"],
                ["Áp suất đi / về", "4 / 2 barg (header ≈3,85 barg)", "5 / 3 barg (đẩy bơm 6–6,5 barg)"],
                ["Lưu lượng thiết kế", "29.900 m³/h (3 bơm); quy trình yêu cầu header ≥ 36.000 m³/h khi 4 bơm chạy", "14.800 m³/h (2 bơm), chưa kể ≈2.040 m³/h cho CDRP"],
                ["pH", "6,9–7,3 (châm H₂SO₄)", "8,5–11,3"],
                ["Khác", "Số vòng cô đặc 1,2 (TDS tuần hoàn/bổ sung); TSS blowdown < 100 mg/l", "NaNO₂ > 750 mg/l (NO₂⁻ 500–600 mg/l)"]],
         "p": ["Nước sông bổ sung là nước lợ, chất lượng thay đổi theo mùa (theo giáo trình): Cl⁻ 15.556–19.810 mg/l; TDS 11.700–29.200 mg/l; TSS 6–120 mg/l; pH 6,1–8. "
               "Vì vậy số vòng cô đặc giữ thấp (1,2) để tránh Cl⁻ quá cao và tránh kết tủa CaSO₄ trong thiết bị trao đổi nhiệt."],
         "src": [S_GT, S_QT, S_CN]},
        {"h": "Thiết bị chính (bảng trên PFD/P&ID)",
         "tb": [["Tag", "Chức năng", "Thông số"],
                ["30-CT-3001A~J", "Tháp giải nhiệt cũ, đối lưu ngược quạt hút", "9 × 3.109 m³/h; 9 × 34.700 kW (1 khoang dự phòng); quạt Cofimco 150 kW"],
                ["30-CT-3001K/L", "Hai khoang tháp mới (revamp)", "2 × 3.109 m³/h; 2 × 34.700 kW; quạt 150 kW"],
                ["30-BA-3001 / 3003", "Bể chứa nước tháp cũ / mới", "5.000 m³ / bê tông"],
                ["30-P-3001A~E", "Bơm nước sông, trục đứng ngập (Flowserve 38QL36)", "10.100 m³/h; 40 m; 740 v/ph; motor 1.515 kW 6,6 kV"],
                ["30-E-3001A~I", "TĐN tấm Alfa Laval (titan), 1 dự phòng", "20.715 kW mỗi bộ; 1.043 m²; 569 tấm"],
                ["30-P-3002A~D", "Bơm nước sạch, ly tâm 2 cửa hút (Flowserve 600 LNN 950)", "7.400–7.590 m³/h; 40 m; 590 v/ph; 1.010–1.100 kW"],
                ["30-V-3001", "Bình giãn nở nước sạch", "3.800 ID × 7.600 H; 100 m³; 4 barg"],
                ["30-PK-3006", "Cụm lọc nước bổ sung & side stream (multimedia/anthracite)", "9 skid × 8 cell; 3.000 / 1.125 m³/h"],
                ["30-BA-3004", "Bể lắng nước rửa ngược", "1.568 m³; lưu 6 giờ; 2 ngăn"],
                ["30-PK-3005", "Châm keo tụ / trợ keo tụ cho nước rửa ngược", "Coagulant 4,5 l/h; flocculant 2,3 l/h"],
                ["30-PK-3002", "Châm chất chống cáu cặn", "Bơm màng P1RA/B 10 l/h"],
                ["30-TK-3001 / 30-P-3003A/B", "Bồn H₂SO₄ 98 % / bơm châm axit", "2.100 ID × 3.000 L, 12,2 m³ / 0,05 m³/h"],
                ["30-PK-3003", "Châm chất ức chế ăn mòn cho vòng nước sạch", "Bơm 40–44 l/h, bồn 1 m³"],
                ["30-PK-3001 / 30-TK-3002", "Cụm điện phân sản xuất hypochlorite / bồn chứa 142 m³", "Đã ngừng sử dụng (PFD ghi chú 10)"]],
         "src": [PFD1, PFD2, S_GT]},
        {"h": "Xử lý hóa học nước tuần hoàn",
         "ul": ["Nước sông: H₂SO₄ châm liên tục vào bể 30-BA-3001/3003 để giữ pH 6,9–7,3. Liều thiết kế 12 wppm theo lượng blowdown. "
                "Axit lấy từ bồn 30-TK-3001, nhận từ bơm 30-P-1003A/B của cụm Demi; mức bồn điều khiển bằng LV-33006.",
                "Chống cáu cặn: châm liên tục 3–6 wppm theo nước bổ sung, bằng 30-PK-3002/P1RA/B (3,5–5 l/h mỗi bơm). Đây là 2 bơm mới thay cặp P1A/B cũ không đủ công suất. "
                "Khi chạy chế độ remote, hành trình bơm tỉ lệ theo tín hiệu FIC-33001 (lưu lượng nước bổ sung).",
                "Diệt vi sinh: NaOCl châm theo mẻ (shock) bằng xe bồn, 3.000 kg mỗi 36 giờ, thay cho cụm điện phân 30-PK-3001 đã bỏ.",
                "Nước sạch: ức chế ăn mòn châm theo mẻ (≈140 kg/tháng theo mô tả revamp) bằng 30-PK-3003, giữ NaNO₂ > 750 mg/l. "
                "Thiết kế gốc của GE Betz: Corrshield MD4100 nạp 3.000 ppm theo thể tích hệ, kèm biocide Spectrus NX1100 30 ppm/tháng (vi sinh < 10⁴ CFU/ml).",
                "Hóa chất theo giáo trình: Javel, H₂SO₄, Nalco 73202 / Hydex 2330 (chống cáu cặn), Tract 109, Nalco 7330."],
         "src": [S_CN, S_GT, S_QT, S_PKP]},
        {"h": "Lọc nước bổ sung & side stream (30-PK-3006)",
         "ul": ["9 skid × 8 cell anthracite. Chế độ NORMAL: 6 skid lọc nước sông bổ sung (MUF, 500 m³/h/skid, 1,4 barg) và 3 skid lọc side stream (SSF, ≈4 barg) từ header nước sông.",
                "Skid ở chế độ MUF chỉ lọc, không rửa ngược. Khi chuyển sang SSF, các cell lần lượt được rửa ngược bằng nước đã lọc của 7 cell còn lại (60 m³/h, ≈3 phút/cell, 30 phút/skid). "
                "Mỗi skid SSF trả ≈375 m³/h về bể, xả trung bình ≈132 m³/h nước rửa ngược sang bể lắng 30-BA-3004.",
                "PLC chuyển MUF ↔ SSF theo thời gian đặt (T1 ≥ 30 phút). 3 nhóm skid luân phiên: mỗi chu kỳ 2 lần MUF + 1 lần SSF. "
                "Ngoài NORMAL còn có PEAK1 (6 MUF + 2 SSF + 1 standby, T2 ≥ 20 phút, rửa 2 cell/skid) và PEAK2 (6 MUF + 1 SSF + 2 standby, T3 ≥ 10 phút, rửa 4 cell/skid). "
                "MANUAL và SEMI-AUTO dùng khi cần thao tác từng skid.",
                "Không có thiết bị phân tích online; KCS phân tích chất lượng nước hằng ngày. Chênh áp qua skid chỉ để tham khảo, không dùng để quyết định rửa ngược.",
                "Nước rửa ngược được châm keo tụ (8–10 wppm) và trợ keo tụ (3–5 wppm) từ 30-PK-3005 qua bộ trộn tĩnh, rồi lắng ở 30-BA-3004. "
                "Nước trong chảy tràn ra sông (TSS < 100 ppm); bùn hút định kỳ bằng bơm di động lên xe bồn."],
         "src": [S_CP6, S_GT, S_CN, PID_FIL, PID_SB]},
        {"h": "Khởi động & ngừng (G2-30-QT-045, giáo trình)",
         "ul": ["Chuẩn bị:",
                "• Mức dầu quạt và bơm hóa chất 60–80 %; bồn axit ≥ 50 %; hóa chất chống cáu cặn, keo tụ, trợ keo tụ sẵn sàng.",
                "• Hai sluice gate giữa 30-BA-3001 và 30-BA-3003 mở; bể sạch, van xả đáy đóng, lưới chắn rác đã vệ sinh và hạ xuống.",
                "• 30-PK-3006 đã nạp đủ anthracite, van bypass đóng, chọn chế độ (Normal/Peak1/Peak2).",
                "Khởi động bơm NHR cấp nước vào 30-PK-3006 và bể; mức bể tối thiểu 70 %. Nước làm mát/làm kín trục bơm (PI-33701A~E) 2–4 barg.",
                "Bơm nước sông: mở van đẩy 10–15 %, mở van block ở TĐN (mỗi bơm ≈3 TĐN), mở đường hồi ≈3 tháp, xả khí. Khởi động tại chỗ.",
                "• Rung: báo động 8 mm/s, trip 11 mm/s.",
                "• Khi ổn định, mở dần van đẩy: dòng 145–160 A; lưu lượng ≥ 6.000 m³/h (bình thường 9.060–10.100 m³/h/bơm).",
                "Sau đó: chạy 30-PK-3002/P1RA/B, mở axit xuống bể, rồi khởi động quạt tháp theo nhiệt độ (160–190 A).",
                "Bơm nước sạch: điền 30-V-3001 ≥ 80 % (LIT-33101, LG-33601A/B/C), nâng áp N₂ ≈2,0 barg qua PV-33101A, xả khí. "
                "Mở van đẩy 5–10 %, khởi động, rồi mở dần tới 6–6,5 barg, 4.200–7.590 m³/h/bơm. Nếu tiêu thụ < 4.200 m³/h, mở bypass ở đầu đẩy 30-P-3002D. "
                "Chạy 30-PK-3003 khi hệ ổn định.",
                "Ngừng bình thường: dừng bơm NHR, dừng 30-PK-3006, dừng hóa chất, quạt, rồi bơm nước sông. Hệ nước sông chỉ ngừng sau khi toàn nhà máy đã ngừng.",
                "Ngừng khẩn cấp: nhiệt độ/rung cao mà bảo vệ không tác động; mất dầu bôi trơn hoặc nước làm mát; mức bể quá thấp gây xâm thực; vỡ đường ống không khắc phục được."],
         "src": [S_QT, S_GT]},
        {"h": "Liên động (2539-33-CN-0009-02, giáo trình)",
         "tb": [["Logic", "Nguyên nhân", "Tác động"],
                ["30-I-33006 / 33012", "Rung cao-cao (XAP-3001A~E, 11 mm/s); nhiệt độ motor cao-cao TSHH-33308/33309 (100 °C); dừng từ DCS (B~D)", "Dừng bơm 30-P-3001A~E"],
                ["30-I-33002", "Mức rất thấp bình giãn nở LSLL-33102; rung cao-cao (11 mm/s); nhiệt độ gối đỡ bơm/motor cao-cao (90 °C)", "Dừng bơm 30-P-3002A~D"],
                ["30-I-33003", "Mức 30-V-3001 thấp / cao (LIT-33101, 75 % / 80 %)", "Mở / đóng LV-33101 cấp nước khử khoáng"],
                ["30-I-33001", "Mức rất thấp bồn axit 30-TK-3001 (LSLL-33006); dừng từ DCS", "Dừng bơm 30-P-3003A/B"],
                ["30-I-33011K/L", "Rung cao quạt tháp K/L (VSHF-33001K/L)", "Dừng motor quạt 30-CT-3001K/L/MF1"],
                ["30-I-33005", "Mức rất thấp / rất cao bồn 30-TK-3002", "Dừng bơm 30-PK-3001/P1A~C / tắt bộ điện phân (cụm đã bỏ)"]],
         "p": ["Bơm 30-P-3001A~E và 30-P-3002A~D được điều khiển từ tủ LCP tại chỗ (PLC + Bentley Nevada). Trạng thái bơm nước sạch được DCS biểu quyết và gửi cứng sang PLC-3, PLC-4, PLC-7."],
         "src": [S_ILK, S_CE, S_GT]},
        {"h": "Hộ tiêu thụ chính (giáo trình, t/h)",
         "tb": [["Mạch", "Hộ tiêu thụ", "Lưu lượng"],
                ["Nước sông", "Amonia: 10-E-4001 bình ngưng tuabin 7.525; 10-E-5010A/B ngưng tụ NH₃ 2.981; 10-E-3003 747; 10-E-7002R 362", "11.615"],
                ["Nước sông", "Urê: 20-E-1022 3.169; 20-E-1024 325", "3.494"],
                ["Nước sông", "Phụ trợ: 30-E-3001A~I", "12.737"],
                ["Nước sạch", "Amonia: làm mát giữa cấp máy nén 10-K-4021/4031/4041, 10-E-3006/3007/3012/5004…", "5.180"],
                ["Nước sạch", "Urê: 20-E-1008/1009, 20-PK-1003/1004 (3.615)…", "8.701"],
                ["Nước sạch", "Phụ trợ: 30-K-5001A~E, 30-E-1001/1002, 40-PK-5001/5005…", "460"],
                ["Nước sạch", "CRU / CDRP (thu hồi CO₂ khói thải)", "1.893"]],
         "src": [S_GT]},
        {"h": "Lưu ý",
         "ul": ["30-PK-3001 (điện phân nước sông tạo NaOCl 2 × 10 kg/h Cl₂) và bồn 30-TK-3002 đã ngừng; hiện dùng shock NaOCl bằng xe bồn.",
                "Tuabin hơi 30-STP-3001A, 30-STP-3002A đã thay bằng motor 30-MP-3001A, 30-MP-3002A. Các logic tuabin cũ (30-I-3007…) đã xóa. "
                "Hệ dầu bôi trơn tuabin/hộp số cũ trên P&ID 33-04 không còn dùng cho dẫn động mới.",
                "Quạt tháp K/L đã đổi hộp số và cánh quạt, từ 7 cánh xuống 5 cánh (ghi chú giáo trình). Năm 2019 có sự cố rò dầu và hỏng bánh răng quạt K."],
         "src": [PFD1, S_ILK, S_GT]},
    ],
    "src": [S_CN, S_GT, S_QT, PFD1, PFD2],
}

CT = ent("Tháp giải nhiệt 30-CT-3001A~L",
         "Tháp đối lưu ngược quạt hút, 12 khoang: 10 khoang cũ A~J (Hamon/KHC, MR 0311-50) trên bể 30-BA-3001 và 2 khoang mới K/L (revamp) trên bể 30-BA-3003. "
         "Vận hành 11 khoang, 1 dự phòng. Mỗi khoang 3.109 m³/h, 34.700 kW, làm mát nước sông 43 → 34 °C. Phân phối nước bằng vòi phun; mỗi khoang có 1 quạt hướng trục Cofimco Ø 9,14 m. "
         "Quạt chạy qua hộp giảm tốc góc vuông (A~J: Sumitomo, tỉ số 12,756; K/L: Dissan DKS-320, 14:1), motor Siemens 150 kW 400 V (dòng vận hành 160–190 A). "
         "Số khoang/quạt chạy chọn theo nhiệt độ nước lạnh và yêu cầu của trưởng ca.",
         [{"h": "Thông số (data sheet, giáo trình)",
           "tb": [["Thông số", "A~J", "K/L"],
                  ["Lưu lượng tuần hoàn (thường/thiết kế)", "27.181 / 29.900 m³/h (10 khoang)", "3.109 / 3.434 m³/h (2 khoang)"],
                  ["Nóng / lạnh", "43 / 34 °C", "43 / 34 °C"],
                  ["Bay hơi", "1,37 % lưu lượng", "42,28 m³/h"],
                  ["Kích thước khoang", "15,10 × 14,35 m", "15,10 × 14,35 m"],
                  ["Quạt", "5 cánh, 116 v/ph, 568 m³/s", "106 v/ph, 688 m³/s (đã đổi 7 → 5 cánh)"]]},
          {"h": "Bảo vệ",
           "ul": ["Quạt K/L: công tắc rung VSHF-33001K/L dừng motor (30-I-33011K/L).",
                  "Quạt A~J: công tắc rung Murphy VS2. Kiểm tra mức dầu hộp số 60–80 % trước khi chạy."]}],
         [S_CTDS, S_CTOP, S_CTKL, S_GT, S_ILK, PID_BA, PID_NEW])

TAGS33 = {
    "30-CT-3001": CT, "30-CT-3001K": CT, "30-CT-3001L": CT,
    "30-BA-3001": ent("Bể chứa nước tháp 30-BA-3001",
                      "Bể bê tông 5.000 m³ dưới 10 khoang tháp cũ, đặt bơm 30-P-3001A~D. Nhận nước bổ sung đã lọc (LV-33001 theo LIC-33001), nước side stream đã lọc (1.125 m³/h), "
                      "H₂SO₄ (30-P-3003A/B) và chất chống cáu cặn (30-PK-3002). Nối với 30-BA-3003 qua mương ngầm có 2 van cửa. "
                      "Mức bể tối thiểu 70 % trước khi khởi động bơm; mức quá thấp gây xâm thực, phải dừng khẩn cấp bơm. Lưới chắn rác đầu vào các khoang phải vệ sinh định kỳ.",
                      src=[PID_BA, S_CN, S_QT, S_GT]),
    "30-BA-3002": ent("Hố xả đáy bể tháp 30-BA-3002",
                      "Hố thu nước xả đáy của bể tháp giải nhiệt (8,1 m³), dùng khi xả cạn/vệ sinh bể 30-BA-3001.",
                      src=[PID_BA]),
    "30-BA-3003": ent("Bể chứa nước tháp mới 30-BA-3003",
                      "Bể bê tông dưới 2 khoang tháp mới 30-CT-3001K/L, đặt bơm 30-P-3001E. Nối với 30-BA-3001 bằng mương ngầm có 2 van cửa (sluice gate) để tách riêng khi bảo dưỡng. "
                      "Hai bể cùng nhận hóa chất (H₂SO₄, chống cáu cặn) và cùng bảo đảm thời gian lưu ≥ 10 phút theo lưu lượng tuần hoàn thiết kế.",
                      src=[S_BA3, S_CN, PID_NEW]),
    "30-BA-3004": ent("Bể lắng nước rửa ngược 30-BA-3004",
                      "Bể lắng trọng lực 1.568 m³ (thời gian lưu 6 giờ), chia 2 ngăn, mỗi ngăn có hố gom bùn và có thể cô lập để vệ sinh mà không dừng bể. "
                      "Nhận nước rửa ngược của 30-PK-3006 (trung bình ≈132 m³/h, tối đa 200 m³/h, TSS ≤ 2.000 mg/l) đã châm keo tụ/trợ keo tụ từ 30-PK-3005. "
                      "Nước trong chảy tràn ra sông (TSS < 100 ppm). Bùn hút định kỳ bằng bơm di động lên xe bồn (bên thứ ba).",
                      src=[S_BA4, S_CN, S_GT, PID_SB]),
    "30-P-3001": ent("Bơm nước sông 30-P-3001A~E",
                     "Bơm trục đứng ngập nước, 1 cấp (Flowserve 38QL36): 10.100 m³/h định mức (thường 9.060, tối thiểu 6.000), cột áp 40 m (≈3,9 barg), 740 v/ph. "
                     "Motor ABB 1.515 kW, 6,6 kV, 162 A (vận hành 145–160 A). A~D đặt trong 30-BA-3001, E (mới) đặt trong 30-BA-3003. Thường chạy 3–4 bơm. "
                     "Trục bơm làm mát/làm kín bằng nước, áp PI-33701A~E 2–4 barg. Nước sông nhiều muối nên dễ kết tủa ở hộp làm kín; cần theo dõi nước rò qua seal.",
                     [{"h": "Bảo vệ (30-I-33006 / 30-I-33012)",
                       "ul": ["Rung vỏ bơm VE-33301A~E: báo động 8 mm/s, trip 11 mm/s.",
                              "Nhiệt độ cuộn dây/gối motor TE-33308/33309: trip 100 °C. Bơm điều khiển qua LCP (PLC + Bentley Nevada); B~D có thể dừng từ DCS."]}],
                     [S_GT, S_QT, S_P1E, S_P1A, S_RUN_A, S_RUN_E, S_ILK, PID_P1, PID_NEW]),
    "30-P-3001A": ent("Bơm nước sông 30-P-3001A",
                      "Cùng kiểu với 30-P-3001B~D (10.100 m³/h, 40 m). Trước revamp được dẫn động bằng tuabin hơi 30-STP-3001A qua hộp số, có hệ dầu bôi trơn riêng (P&ID 33-04: E1/E2, EH1, FL1A/B, P2~P4, V1). "
                      "Năm 2016–2018 tuabin được thay bằng motor điện 30-MP-3001A (1.580/1.515 kW); logic tuabin cũ đã xóa, bảo vệ motor theo 30-I-33006.",
                      src=[S_P1A, S_RUN_A, S_ILK, PID_LO, PID_P1]),
    "30-P-3002": ent("Bơm nước sạch 30-P-3002A~D",
                     "Bơm ly tâm 2 cửa hút, 1 cấp (Flowserve 600 LNN 950): định mức 7.400–7.590 m³/h (thường 6.700, tối thiểu 4.200), cột áp 40 m, đẩy 6,1 barg, 590 v/ph. "
                     "Motor ABB 6,6 kV: A 1.100 kW; B/C/D 1.030 kW (vận hành 100–110 A). Thường chạy 2 bơm cho 14.800 m³/h, cộng thêm khi cấp cho CDRP. "
                     "Hút từ đường hồi sau TĐN tấm; áp hút giữ nhờ bình giãn nở 30-V-3001.",
                     [{"h": "Bảo vệ (30-I-33002A~D)",
                       "ul": ["Mức rất thấp bình giãn nở LSLL-33102 dừng tất cả bơm nước sạch.",
                              "Rung gối bơm VE-33351/33352: trip 11 mm/s. Nhiệt độ gối bơm TE-33351/33352 và gối motor TE-33359/33360: trip 90 °C.",
                              "Lưu lượng nhỏ hơn 4.200 m³/h: mở bypass ở đầu đẩy 30-P-3002D để bảo vệ bơm."]}],
                     [S_GT, S_P2A, S_ILK, S_CE, PID_F1, PID_F2]),
    "30-P-3002A": ent("Bơm nước sạch 30-P-3002A",
                      "Cùng kiểu với 30-P-3002B~D. Trước revamp dẫn động bằng tuabin hơi 30-STP-3002A qua hộp số, có hệ dầu bôi trơn và điều tốc Peak 150 riêng (P&ID 2098-33-PID-0031-07). "
                      "Đã thay bằng motor 30-MP-3002A (1.100 kW). Logic 30-I-3007 của tuabin đã xóa; tín hiệu trip LSLL-33102 nối lại để dừng motor mới.",
                      src=[S_P2A, S_ILK, S_CE, PID_F3]),
    "30-E-3001": ent("Thiết bị trao đổi nhiệt tấm 30-E-3001A~I",
                     "9 bộ TĐN tấm Alfa Laval (1 dự phòng), kiểu tháo lắp được, 569 tấm titan dày 0,6 mm, 1.043 m². Mỗi bộ 20.715 kW. "
                     "Phía nóng là nước sạch 46 → 37 °C; phía lạnh là nước sông 34 → 43 °C (≈1.924 t/h mỗi phía, ΔP ≤ 1 bar). "
                     "Áp thiết kế 9 barg (nóng) / 6 barg (lạnh). Kích thước 5.195 × 1.170 × 2.882 mm, nặng 8,2 t (11,7 t khi đầy nước). "
                     "Khi khởi động bơm, mở van block vào/ra TĐN tương ứng (≈3 TĐN mỗi bơm) và xả khí cả hai phía.",
                     src=[S_E31, S_E34, S_GT, PFD1, PID_F1]),
    "30-V-3001": ent("Bình giãn nở 30-V-3001",
                     "Bình đứng 3.800 ID × 7.600 H (100 m³), thiết kế 4 barg / 75 °C, đặt trên mạch nước sạch. "
                     "Hấp thụ giãn nở nhiệt, giữ áp đầu hút bơm 30-P-3002 ổn định, và tách khí lọt vào khi rò/thủng ống ở X.Amonia/Urê. "
                     "Nitơ đệm áp 2–2,3 barg bằng PIC-33101 split range: PV-33101A cấp N₂, PV-33101B xả. "
                     "Nước khử khoáng bổ sung qua LV-33101 theo LIT-33101 (mở ở 75 %, đóng ở 80 %). Mức rất thấp LSLL-33102 dừng tất cả bơm nước sạch.",
                     src=[S_GT, S_CN, S_ILK, PID_F1]),
    "30-PK-3006": ent("Cụm lọc nước bổ sung & side stream 30-PK-3006",
                      "Cụm lọc anthracite (revamp, MR 0848-01) gồm 9 skid × 8 cell, mỗi cell 62,5 m³/h. Áp thiết kế 6 barg, ΔP tối đa 0,8 bar. "
                      "6 skid lọc nước sông bổ sung (MUF): 3.000 m³/h, TSS vào ≤ 120 → ra ≤ 50–60 mg/l. "
                      "3 skid lọc side stream (SSF): 1.305 m³/h từ header, trả 1.125 m³/h về 30-BA-3001. "
                      "PLC tại LCP tự đổi vai trò MUF/SSF theo thời gian đặt. Ở SSF, các cell lần lượt rửa ngược bằng nước lọc của cell khác (60 m³/h, 3 phút/cell). "
                      "Nước rửa ngược sang 30-BA-3004. Chế độ: NORMAL, PEAK1, PEAK2, MANUAL, SEMI-AUTO. Bình 30-PK-3006/V1 là bình khí điều khiển cho các van tự động.",
                      [{"h": "Giá trị cài đặt (triết lý điều khiển rev B)",
                        "tb": [["Điểm đo", "Thấp", "Cao", "Ghi chú"],
                               ["PIT-33900", "1,33 barg", "1,47 barg", "Header nước sông vào"],
                               ["FIT-01 (mỗi skid)", "455 / 395 m³/h", "550 / 478 m³/h", "MUF / SSF"],
                               ["FIT-33202", "163 / 218 m³/h", "198 / 264 m³/h", "Tổng nước rửa ngược: Normal / Peak"],
                               ["PIT-33351", "4,55 barg", "5,5 barg", "Khí điều khiển ra bình"],
                               ["ΔP (PIT-01/03) MUF", "0,5 bar", "1,2 bar", "Báo trên HMI"]]},
                       {"h": "Lưu ý vận hành",
                        "ul": ["Không có phân tích online; dựa vào phân tích KCS hằng ngày. ΔP chỉ để theo dõi.",
                               "Khi có sự cố (điện, khí điều khiển, áp cao…), LCP báo đèn/còi, các van giữ nguyên trạng thái. Người vận hành xử lý tại chỗ.",
                               "Muốn sửa skid nào thì phải dừng hoặc bypass nguồn nước cấp vào cụm trong thời gian sửa."]}],
                      [S_CP6, S_SP6, S_GT, S_QT, S_RDY6, PID_FIL]),
    "30-PK-3005": ent("Cụm châm keo tụ / trợ keo tụ 30-PK-3005",
                      "Châm chất keo tụ (coagulant, 8–10 wppm) và trợ keo tụ (flocculant, 3–5 wppm) vào nước rửa ngược của 30-PK-3006 trước bể lắng 30-BA-3004. "
                      "Hóa chất hòa trộn qua bộ trộn tĩnh trên đường ống. Keo tụ trung hòa điện tích các hạt lơ lửng; trợ keo tụ (polymer) kết các hạt thành bông lớn để lắng nhanh.",
                      [{"h": "Thiết bị (P&ID 33-14)",
                        "tb": [["Tag", "Chức năng", "Thông số"],
                               ["/V1", "Thùng coagulant", "1.000 ID × 1.700 H"],
                               ["/P1A/B", "Bơm màng coagulant", "4,63 l/h; 0,25 kW"],
                               ["/V2", "Thùng flocculant", "800 ID × 1.400 H"],
                               ["/P2A/B", "Bơm màng flocculant", "2,54 l/h; 0,25 kW"]]}],
                      [PID_CF, S_CN, S_GT]),
    "30-PK-3002": ent("Cụm châm chất chống cáu cặn 30-PK-3002",
                      "Cụm của GE Betz: bơm hóa chất từ phuy 200 l vào thùng 30-PK-3002/V1 (1 m³, 1.080 D × 1.460 H) bằng bơm khí 30-PK-3002/P2 (dùng chung với 30-PK-3003). "
                      "Châm liên tục vào bể 30-BA-3001/3003, liều 3–6 wppm theo nước bổ sung, bằng 2 bơm màng 30-PK-3002/P1RA/B (1 chạy, 1 dự phòng; 10 l/h, 2,5 barg, 0,25 kW). "
                      "Hai bơm này là bơm mới (revamp), thay P1A/B cũ 5,5 l/h. Thường đặt 3,5–5 l/h. "
                      "Lưu lượng hiệu chỉnh bằng ống chuẩn trên đường hút. Ở chế độ remote, hành trình bơm tỉ lệ theo FIC-33001.",
                      [{"h": "Liên động",
                        "ul": ["Mức thấp thùng V1 dừng bơm đang chạy.",
                               "Báo lỗi chung (mức thấp hoặc trip bơm) gửi về DCS. Đèn chạy/lỗi trên tủ tại chỗ."]}],
                      [S_PKP, S_PKI, S_PK2S, S_GT, PID_CHEM]),
    "30-PK-3003": ent("Cụm châm chất ức chế ăn mòn 30-PK-3003",
                      "Cụm của GE Betz cho vòng kín nước sạch: thùng 30-PK-3003/V1 (1 m³), 2 bơm màng 30-PK-3003/P1A/B (1 chạy, 1 dự phòng; 40–44 l/h, đẩy ≥ 3 barg, 0,25 kW). "
                      "Châm gián đoạn theo kết quả phân tích, giữ NaNO₂ > 750 mg/l. Theo mô tả revamp ≈140 kg/tháng. "
                      "Thiết kế gốc: Corrshield MD4100 nạp 3.000 ppm theo thể tích tĩnh, cộng biocide Spectrus NX1100 30 ppm/tháng (bơm sau khi đã xả hết MD4100 khỏi thùng). "
                      "Hiệu chỉnh lưu lượng bằng ống chuẩn 500 cc; áp đẩy chỉnh bằng van giữ áp ≈2,5 bar. Mức thấp thùng dừng bơm, báo lỗi chung XA-33451 về DCS.",
                      src=[S_PKP, S_PK3S, S_PKI, S_GT, PID_F4]),
    "30-TK-3001": ent("Bồn H₂SO₄ 30-TK-3001",
                      "Bồn nằm ngang 2.100 ID × 3.000 L (12,2 m³), H₂SO₄ 98 %, thiết kế 3 barg / 60 °C, ăn mòn cho phép 3 mm. "
                      "Nhận axit từ bơm 30-P-1003A/B của cụm Demi; LV-33006 mở ở 35 %, đóng ở 65 % (LIT-33006). "
                      "Mức rất thấp LSLL-33006 dừng bơm châm 30-P-3003A/B (30-I-33001). Giữ mức bồn ≥ 50 % trước khi khởi động hệ.",
                      src=[S_GT, S_ILK, PID_CHEM]),
    "30-P-3003": ent("Bơm châm H₂SO₄ 30-P-3003A/B",
                     "Bơm màng 0,05 m³/h, 27,6 m, 0,55 kW. Châm axit liên tục vào bể 30-BA-3001/3003, giữ pH nước sông 6,9–7,3 (thiết kế 12 wppm theo blowdown). "
                     "Bị dừng khi bồn 30-TK-3001 mức rất thấp, hoặc dừng tay từ DCS (30-I-33001).",
                     src=[PFD1, S_ILK, S_QT, PID_CHEM]),
    "30-P-3010": ent("Bơm nước sông bổ sung 30-P-3010A/B (ngoài hàng rào)",
                     "Bơm ly tâm 4.100 m³/h, 34 m, motor 520 kW, 980 v/ph, đặt ở trạm bơm nước sông ngoài hàng rào (NHR). "
                     "Cấp nước sông cho cụm lọc 30-PK-3006 rồi vào bể tháp (≈2.930 m³/h). Ngoài ra cấp ≈810 m³/h làm nguội kênh xả. Áp đẩy ≈2,9 barg. "
                     "Trước khi chạy phải mở hoàn toàn van đẩy BV1/BV2 và LV-33001 (hoặc bypass). "
                     "Hộp làm kín bằng chính nước sông: giữ rò 0,5–1 l/h (40–120 giọt/phút), không chạy khô quá 1 phút. Muối kết tủa làm tắc rò thì phải vệ sinh.",
                     src=[S_GT, PID_NHR]),
    "30-J-3001": ent("Ejector 30-J-3001",
                     "Ejector bằng hơi (SS304): hút 2 m³/h nước ở −0,3 barg, dùng hơi động lực 53 kg/h ở 3,4 barg/230 °C, xả ở 0,5 barg. Nằm trên P&ID 33-01 và 33-05.",
                     src=[PID_CHEM, PID_BA]),
    "30-PK-3001": ent("Cụm sản xuất hypochlorite 30-PK-3001 (đã ngừng)",
                      "Cụm điện phân nước sông tạo dung dịch NaOCl 2.000 ppm (2 × 10 kg/h Cl₂ tương đương), gồm bộ điện phân Z2A/B, biến thế/chỉnh lưu, bồn chứa 30-TK-3002 (142 m³) và bơm chuyển P1A~C. "
                      "Theo PFD as-built (ghi chú 10), cụm đã bị bỏ. Diệt vi sinh hiện bằng shock NaOCl 3.000 kg mỗi 36 giờ từ xe bồn.",
                      src=[PFD1, S_CN, S_ILK]),
    "30-TK-3002": ent("Bồn chứa hypochlorite 30-TK-3002 (thuộc cụm đã ngừng)",
                      "Bồn 142 m³ (5.500 ID × 6.000 H) chứa dung dịch NaOCl của cụm 30-PK-3001. Mức rất thấp dừng bơm P1A~C, mức rất cao tắt bộ điện phân (30-I-33005). Cụm 30-PK-3001 đã ngừng sử dụng.",
                      src=[PFD1, S_ILK]),
}

# ======================================================================= Unit 42
PFD42_1 = sh("2098-42-PFD-0010-1-2", "PFD 2098-42 Xử lý nước nhiễm dầu")
PFD42_2 = sh("2098-42-PFD-0010-2-2", "PFD 2098-42 Xử lý nước thải sinh hoạt")
PID42_1 = sh("2098-42-PID-0031-01", "P&ID 42-01 Nhiễm dầu (API, CPI, hóa chất)")
PID42_3 = sh("2539-42-PID-0031-01", "P&ID 42 (3/7) Nhiễm dầu – DAF & lọc")
PID42_4 = sh("2098-42-PID-0031-02", "P&ID 42 (4/7) Sinh hoạt – bể sinh học")
PID42_5 = sh("2098-42-PID-0031-03", "P&ID 42 (5/7) Sinh hoạt – khử trùng & nước sạch")
PID42_6 = sh("2098-42-PID-0031-04", "P&ID 42 (6/7) Bể cân bằng NH₃ & bơm cấp stripper")
PID42_7 = sh("2098-42-PID-0031-05", "P&ID 42 (7/7) Tháp stripper NH₃")
PID42_N = sh("2539-42-PID-0031-06", "P&ID hệ thống XLNT mới 40-PK-2003")
PID43 = sh("2539-43-PID-0031-01", "P&ID 43 Thu gom nước thải nhiễm dầu")

S_GTW = [GTN + "STVB102393_G2-30-GT-05 GT dao tao HT xu ly nuoc thai_vps.pdf", "Giáo trình G2-30-GT-05 Hệ thống xử lý nước thải"]
S_STAY = [WW + "20. 40-PK-2003/So tay huong dan van hanh tram Phu My 03072012 NOP Ref3.doc", "Sổ tay vận hành trạm XLNT mới (2012)"]
S_SH = [WW + "20. 40-PK-2003/So tay huong dan van hanh phan xu ly sinh hoc.doc", "Sổ tay vận hành phần xử lý sinh học"]
S_KUB = [WW + "20. 40-PK-2003/So tay van hanh bao duong mang KOBUTA-VN.docx", "Sổ tay màng MBR Kubota"]
S_EP = [WW + "20. 40-PK-2003/So tay huong dan bao tri may ep bun.pdf", "Sổ tay bảo trì máy ép bùn"]
S_PA174 = [WW + "STVB99072_G2-00-PA-174-L3 Phuong an kiem soat nguon xa thai vao he thong nuoc nhiem dau_vps.pdf", "Phương án G2-00-PA-174 (12/2023)"]
S_UFC = [WW + "STVB126972_TTr ve phuong an xu ly nuoc thai nong do o nhiem cao cum UFC85_vps.pdf", "Tờ trình nước thải UFC85 (08/2024)"]
S_SPB = [WW + "TTr phe duyet ve BC Danh gia hieu qua van hanh lan dau cua SPB.pdf", "Tờ trình đánh giá sân phơi bùn"]
S_SODO = [WW + "Kiểm soát nước thải đầu vào/So do cac diem thu gom NTND nha may.pdf", "Sơ đồ điểm thu gom nước nhiễm dầu"]
S_DOM = [WW + "DOMESTIC WASTEWATER COLLECTION SYSTEM.pdf", "Hệ thống thu gom nước thải sinh hoạt"]
S_QCVN = [WW + "qcvn_40-2025_nuoc_thai_cong_nghiep..pdf", "QCVN 40:2025/BTNMT"]

UNIT42 = {
    "t": "Công nghệ Unit 42 – Xử lý nước thải",
    "intro": "Nước thải của nhà máy được xử lý qua ba cụm. "
             "(1) 40-PK-2001 xử lý nước nhiễm dầu bằng API → CPI → phá nhũ/keo tụ → tuyển nổi DAF, công suất 20 m³/h, dầu ra ≤ 5 mg/l. "
             "(2) 40-PK-2002 là cụm sinh hoạt cũ, bùn hoạt tính sục khí kéo dài, 50 m³/ngày. "
             "(3) 40-PK-2003 là hệ thống mới (2012), khử nitơ + màng sinh học MBR, ≈680 m³/ngày. "
             "Theo phiếu đề nghị thay đổi 62/2018, nước sau 40-PK-2001 không qua lọc multimedia/than hoạt tính mà đưa thẳng vào bể điều hòa TK-102 của 40-PK-2003. Nước thải sinh hoạt, nước từ nhà máy CO₂ và cụm UFC85/AF37 (X.Urê) cũng về TK-102. "
             "Nước đã xử lý gom tại bể 40-PK-2002/BA8, rồi bơm sang hệ thống xử lý tập trung của KCN Phú Mỹ (IZICO) theo hợp đồng. "
             "Cụm tách NH₃ cũ (40-BA-2001, 40-T-2001…) đã ngừng và một số thiết bị đã tháo (MOC M125/2025). "
             "Máy ép bùn BF-202 không dùng nữa; thay bằng sân phơi bùn TK-202A/B (MOC M134/2025).",
    "s": [
        {"h": "Sơ đồ dòng hiện tại",
         "ul": ["Nước nhiễm dầu (rò rỉ dầu, nước mưa 20 phút đầu khu vực đường, nước chữa cháy) theo mạng thu gom ngầm (P&ID 43) về bể tách dầu API 40-PK-2001/V1. "
                "Thiết kế: 20 m³/h; dầu đầu vào ≤ 500 vppm (rò dầu tới 10.000 vppm); mưa lớn tới 1.350 m³/h, phần vượt tràn sang bể dự phòng BA2 (742,5 m³).",
                "Trong 40-PK-2001: lưới rác /Z1 → API /V1 (dây đai gạt dầu /Z2 → hố dầu /BA3 → coalescer /V2). Nước tách dầu sang /BA1, bơm /P1A/B tới CPI /V4. "
                "Tiếp theo: trộn nhanh /TK3 với chất phá nhũ (Klaraid CDP1317, AlCl₃) → keo tụ /TK4 (Betz CE1154) → tuyển nổi DAF /Z5 → bồn /TK5 → bơm /P8A/B → TK-102.",
                "Nước thải sinh hoạt về bể gom TK-100 (bơm thu gom 40-P-3001A/B, 40-P-3002A/B theo mức), qua máy sàng rác tinh FS-101 (> 1 mm) vào bể điều hòa TK-102 (256 m³).",
                "TK-102 → bể khử nitơ TK-103 (thiếu khí, 147 m³) → bể đệm TK-104 (205 m³, sục khí chìm, tuần hoàn ≈4Q về TK-103) → bể MBR TK-105 (360 m³: ngăn sục khí 170 m³ + ngăn màng 190 m³). "
                "Một phần nhỏ (≈50 m³/ngày) bơm PM-102C/D sang bể cân bằng 40-PK-2002/BA1.",
                "Nước qua màng MBR (lỗ 0,4 µm) do bơm PM-105A1/2, B1/2 hút (chạy 9 phút, nghỉ 1 phút) → bể nước sạch 40-PK-2002/BA8 (200 m³) → bơm ra KCN.",
                "Bùn MBR tuần hoàn về TK-103 (PM-105C/D). Bùn dư 15–20 m³/ngày sang bể nén TK-201, rồi ra sân phơi bùn TK-202A/B. Nước tách bùn về TK-100/TK-102."],
         "src": [PFD42_1, PID42_N, S_GTW, S_UFC]},
        {"h": "Chỉ tiêu thiết kế",
         "tb": [["Dòng", "Thông số", "Giá trị"],
                ["Nhiễm dầu sau 40-PK-2001", "Dầu mỡ", "≤ 5 mg/l"],
                ["Sinh hoạt vào 40-PK-2002", "Lưu lượng / BOD₅ / COD / TSS / NH₃", "50 m³/ngày (đỉnh 13 m³/h) / 220 / 500 / 220 / 50 mg/l"],
                ["Sinh hoạt ra 40-PK-2002", "BOD₅ / TSS / Cl₂ dư", "< 20 (PFD 30) / < 50 (PFD 80) / < 0,1 mg/l"],
                ["Vào 40-PK-2003", "Sinh hoạt + nhiễm dầu", "200 + 480 m³/ngày; COD ≤ 1.500, BOD₅ ≤ 750, NH₄⁺-N ≤ 60–80 mg/l"],
                ["Ra 40-PK-2003", "Quy chuẩn", "Thiết kế QCVN 24:2009 cột B; vận hành 2024 đối chiếu QCVN 40:2011 cột B (thư mục có QCVN 40:2025)"]],
         "p": ["Trong vận hành thực tế hệ thống còn nhận nước thải nhà máy CO₂ và UFC85/AF37 (COD tới 7.800 mg/l, HCHO 200 mg/l). "
               "Hệ có lúc quá tải về lưu lượng và nồng độ, nhất là mùa mưa và khi UFC85 khởi động lại sau thay xúc tác. "
               "Hợp đồng với IZICO ngưng tiếp nhận khi nước ra có COD > 800 mg/l hoặc NH₄⁺ > 20 mg/l."],
         "src": [S_GTW, PFD42_2, S_UFC, S_QCVN]},
        {"h": "Thiết bị chính",
         "tb": [["Tag", "Chức năng", "Thông số"],
                ["40-PK-2001", "Xử lý nước nhiễm dầu (API + CPI + DAF + lọc)", "20 m³/h; dầu ra ≤ 5 mg/l"],
                ["40-PK-2001/BA2", "Bể tràn/dự phòng (surge basin)", "742,5 m³"],
                ["40-PK-2002", "Xử lý nước sinh hoạt (sục khí kéo dài)", "50 m³/ngày; quạt K1A/B/C 170 Nm³/h"],
                ["40-PK-2002/BA8", "Bể nước sạch cuối – xả ra KCN", "200 m³; bơm P6A/B 13 m³/h, P9A/B 50 m³/h"],
                ["40-PK-2003 TK-100/102", "Bể gom / bể điều hòa", "31,5 / 256 m³"],
                ["40-PK-2003 TK-103/104", "Bể khử nitơ / bể đệm", "147 / 205 m³; MLSS ≈11.500 mg/l"],
                ["40-PK-2003 TK-105", "Bể MBR (màng Kubota, lỗ 0,4 µm)", "360 m³; 2 × 315 m³/ngày; MLSS ≈15.000 mg/l"],
                ["40-PK-2003 BL-102A/B, BL-105A/B/C", "Máy thổi khí bể điều hòa / MBR", "≥ 2 m³/phút cho mỗi module màng"],
                ["40-T-2001, 40-E-2001, 40-P-2001/2002", "Tách NH₃ bằng hơi (cũ)", "Đã ngừng, một số thiết bị đã tháo (12/2025)"]],
         "src": [PID42_1, PID42_4, PID42_5, PID42_N, S_GTW]},
        {"h": "Vận hành hệ thống MBR 40-PK-2003",
         "ul": ["Mức bể (m), theo thứ tự HH / H / L / LL:",
                "• LS-100: 3,5 / 2,8 / 1,8 / 0,7;",
                "• LS-102: 3,5 / 1,9 / 0,6 / 0,5;",
                "• LS-104: 4,3 / 4,0 / 1,5 / 1,0;",
                "• LS-105: 4,3 / 4,0 / 3,6 / 3,0.",
                "Bơm bể điều hòa PM-102A/B chạy theo chu kỳ thời gian để lưu lượng vào sinh học ổn định. Hai lần khởi động liên tiếp cách nhau ≥ 15 phút.",
                "TK-103: 4 máy khuấy chìm chạy theo cặp luân phiên, không chạy đồng thời 2 máy đối diện. MLSS ≈11.500 mg/l (luôn < 20.000).",
                "Nếu tổng N hoặc NO₃⁻ ra cao: tăng MLSS (tăng tuần hoàn từ TK-104 hoặc bùn từ TK-105). Nếu pH giảm mạnh: ưu tiên chỉnh tuần hoàn nước từ TK-104.",
                "Dinh dưỡng: châm H₃PO₄ loãng 0,5 % (DP-401A/B) theo tỉ lệ BOD : N : P = 100 : 5 : 1. Khi thiếu cacbon, bổ sung mật rỉ đường (bồn DR-406, 2024). Có bồn NaOH DR-405 để chỉnh pH.",
                "MBR: TMP ≤ 20 kPa; khí cấp ≥ 2 m³/phút cho mỗi module (≈120–200 m³/h). Rút bùn 15–20 m³/ngày để giữ MLSS 12.000–15.000 mg/l.",
                "Rửa màng mỗi 2–3 tháng, hoặc sớm hơn khi TMP > 20 kPa hay lưu lượng giảm ≥ 15 %:",
                "• ngâm NaOCl 0,5 % trong 2 giờ, rồi axit oxalic 0,5 % trong 1 giờ (≈4,8 m³ dung dịch mỗi loại);",
                "• rửa sạch hóa chất trước khi chạy lại, Cl₂ dư < 10 mg/l.",
                "Shock javel định kỳ bể BA8: hạ mức ≈20 %, dừng P6A/B, châm 30 l javel 10 % (Cl₂ dư ≥ 1 mg/l). Khi mức lên 80 % và Cl₂ dư < 2 mg/l thì bơm ra KCN.",
                "Ngừng bình thường: dừng và cô lập nguồn thải về TK-100/102, dừng các bơm PM-100/102/105A-B. Vẫn duy trì máy thổi khí BL-102, BL-105 và sục khí JE-104 để giữ vi sinh."],
         "src": [S_GTW, S_STAY, S_SH, S_KUB, PID42_N]},
        {"h": "Kiểm soát nguồn thải (G2-00-PA-174)",
         "ul": ["Nguyên nhân quá tải nitơ: nước mưa cuốn chất ô nhiễm qua manhole hở; xả dịch khi bảo dưỡng, sự cố, dừng/chạy lại nhà máy; nước thải UFC85.",
                "Biện pháp: đậy kín manhole; xả vào hệ kín khi có thể; xưởng chủ quản báo trước cho X.Phụ trợ khi phải xả vào mạng nhiễm dầu. "
                "Nước UFC85 từ 20-TK-2601 chuyển về theo quy trình G2-20-QT-096; khi nồng độ cao thì chứa tạm ở 40-PK-2001/BA2.",
                "Khi tổng N ở TK-102 hoặc đầu vào cao bất thường (> 90 mg/l; NH₄⁺ > 60 mg/l):",
                "• X.Phụ trợ báo TCNM và giảm tải (pha loãng, giảm lưu lượng, đưa về bể surge, bổ sung COD);",
                "• các xưởng lấy mẫu tại 4 vị trí hố thu chung để tìm nguồn xả."],
         "src": [S_PA174, S_SODO, S_UFC]},
    ],
    "src": [S_GTW, S_STAY, PFD42_1, PFD42_2, PID42_N],
}

OW = "40-PK-2001"
SW = "40-PK-2002"
EB = ent("Hệ châm chất phá nhũ 40-PK-2001 (/TK1, /V3, /P5A/B, /P6, /Z6)",
         "Chất phá nhũ Klaraid CDP1317 (gốc AlCl₃, pH 2,7) pha trong bồn /TK1 (3,5 m³, 1.500 ID × 2.000 H) có cánh khuấy /Z6. "
         "Hóa chất từ phuy điền vào bằng bơm khí /P6 (1 m³/h). Bồn phụ /V3 (0,1 m³) làm ống định lượng. Bơm trục vít /P5A/B (0,01 m³/h, 30 m, 0,25 kW) châm vào bồn trộn nhanh /TK3. "
         "Pha mẻ: khi mức /TK1 còn ≈30 cm, cấp nước thô tới 130 cm, rồi điền hóa chất tới 180 cm, khuấy 30 phút. Các bơm châm liên động chạy theo bơm /P1A/B.",
         src=[PID42_1, S_GTW])
FLC = ent("Hệ châm chất keo tụ 40-PK-2001 (/TK6, /V8, /P9A/B, /P10, /Z7)",
          "Chất keo tụ Betz CE1154 (nhũ tương polymer) pha trong bồn /TK6 (0,6 m³, 1.200 D × 700 H) có cánh khuấy /Z7. "
          "Hóa chất từ phuy điền bằng bơm khí /P10 (1 m³/h). Bồn phụ /V8 (0,1 m³). Bơm trục vít /P9A/B (0,01 m³/h, 30 m, 0,25 kW) châm vào bồn keo tụ /TK4. "
          "Pha mẻ: khi mức /TK6 còn ≈15 cm, điền hóa chất tới 20 cm, thêm nước thô tới 50 cm, khuấy 30 phút.",
          src=[PID42_1, S_GTW])

TAGS42 = {
    OW: ent("Cụm xử lý nước thải nhiễm dầu 40-PK-2001",
            "Cụm API + CPI + DAF + lọc, công suất thiết kế 20 m³/h, dầu ra ≤ 5 mg/l. "
            "Nước nhiễm dầu từ các xưởng qua lưới rác tự động /Z1 vào bể tách dầu trọng lực API /V1. Dây đai gạt dầu /Z2 đưa dầu nổi vào hố /BA3. "
            "Bơm /P3A/B chuyển dầu sang coalescer /V2: dầu ra phuy, nước về /V1. Nước đã tách dầu chảy sang /BA1, bơm /P1A/B tới thiết bị tách tấm nghiêng CPI /V4. "
            "Sau CPI: bồn trộn nhanh /TK3 (chất phá nhũ) → bồn keo tụ /TK4 → tuyển nổi khí hòa tan /Z5. "
            "Dòng tuần hoàn áp cao (/P7A/B) bão hòa khí trong /V5 (≈4 l/ph khí, 450 kPa), khi giảm áp tạo bọt 30–120 µm kéo hạt dầu nổi lên để gạt bỏ. "
            "Nước trong vào /TK5, bơm /P8A/B (tự chạy/dừng theo mức LSHL-42208: H 1.450 mm, L 500 mm) sang bể TK-102 của 40-PK-2003. "
            "Từ 2018, không qua lọc multimedia /V6 và than hoạt tính /V7.",
            [{"h": "Khởi động (G2-30-QT-049)",
              "ul": ["Chuẩn bị: khí nén, khí điều khiển, nước service sẵn sàng; bồn /TK1, /TK6 đã pha hóa chất; mức /BA1 (LIT-42201) trong khoảng cho phép.",
                     "Thứ tự: chạy /Z1, /Z2 từ LCP → /P3A/B (dầu sang /V2) → /P1A/B, chỉnh lưu lượng sang CPI.",
                     "Theo /P1A/B sẽ tự chạy: bơm hóa chất /P5, /P9; khuấy /Z3, /Z4; van khí XV-42211; cụm DAF (/P7, /Z5).",
                     "Ngừng: chuyển cửa cống về /BA2 nếu cần, dừng /P1A/B, đưa thiết bị về Dừng và cô lập điện."]},
             {"h": "Nguồn nước nhiễm dầu (thiết kế)",
              "tb": [["Nguồn", "Lưu lượng lớn nhất", "Dầu"],
                     ["Tràn dầu ngẫu nhiên", "10 m³/h (TB 1,04; tối đa 25 m³/ngày)", "10.000 vppm"],
                     ["Nước mưa khu vực đường (20 phút đầu)", "1.350 m³/h", "500 vppm"],
                     ["Nước chữa cháy X.NH₃ / X.Urê (30 phút đầu)", "900 / 500 m³/h", "500 vppm"]]}],
            [PFD42_1, PID42_1, PID42_3, S_GTW, S_PA174]),
    OW + "/V1": ent("Bể tách dầu API 40-PK-2001/V1",
                    "Bể bê tông 7.200 × 2.000 × 4.430 mm tạo dòng chảy tĩnh để giọt dầu tự do nổi lên (tốc độ nổi ≥ tải trọng bề mặt). Trước bể có lưới rác tự động /Z1. "
                    "Dầu nổi được gạt liên tục bằng dây đai /Z2 vào hố dầu /BA3. Nước chảy tràn sang bể /BA1. Nước từ coalescer /V2 và bơm tuần hoàn /P2 cũng quay về /V1.",
                    src=[PID42_1, S_GTW]),
    OW + "/Z1": ent("Lưới rác tự động 40-PK-2001/Z1",
                    "Lưới băng (band screen) inox SS304, mắt lưới 3 mm, motor 0,25 kW. Loại rác trước bể API. Khởi động từ LCP trước tiên khi chạy cụm.",
                    src=[PID42_1, S_GTW]),
    OW + "/Z2": ent("Dây đai gạt dầu 40-PK-2001/Z2",
                    "Thiết bị gạt dầu kiểu đai liên tục (3 đai, 1.062 × 412 × 500 mm, 1.425 v/ph), lấy dầu nổi trên bể API /V1 đưa vào hố dầu /BA3.",
                    src=[PID42_1, S_GTW]),
    OW + "/BA1": ent("Bể nước đã tách dầu 40-PK-2001/BA1",
                     "Bể 10 m³ (4.000 × 2.000 × 6.630 mm), thông với bể API /V1. Đặt bơm chìm /P1A/B cấp nước sang CPI. "
                     "Mức LIT-42201 (HH: dừng /P2; H: chạy /P1A/B; L: dừng /P1A/B). Nhiều nước thải UFC85/nồng độ cao được chứa tạm ở /BA1, /BA2 khi hệ quá tải.",
                     src=[PID42_1, S_GTW, S_UFC]),
    OW + "/P1": ent("Bơm nước đã tách dầu 40-PK-2001/P1A/B",
                    "Bơm chìm 20 m³/h, 10 m, 1,5 kW (1 chạy, 1 dự phòng). Hút từ /BA1, đẩy sang CPI /V4 qua FIT-42201. "
                    "Bơm này là bơm chủ: khi chạy thì bơm hóa chất /P5, /P9, khuấy /Z3, /Z4, van khí XV-42211 và cụm DAF tự chạy theo.",
                    src=[PID42_1, S_GTW]),
    OW + "/BA3": ent("Hố dầu 40-PK-2001/BA3", "Hố 6 m³ (2.000 × 2.000 × 2.130 mm) chứa dầu gạt từ bể API. Bơm /P3A/B chuyển dầu lẫn nước sang coalescer /V2.", src=[PID42_1]),
    OW + "/P3": ent("Bơm dầu 40-PK-2001/P3A/B", "Bơm chìm 2 m³/h, 30 m, 0,95 kW. Chuyển dầu từ /BA3 sang coalescer /V2, nước tách ra quay về /V1.", src=[PID42_1, S_GTW]),
    OW + "/V2": ent("Coalescer 40-PK-2001/V2",
                    "Bình lọc kết tụ kiểu cartridge 2.000 ID × 3.000 L. Các giọt dầu nhỏ kết lại thành giọt lớn để tách: dầu ra phuy (dòng 42.9, ≈1 lần/ngày), nước về bể API /V1.",
                    src=[PFD42_1, PID42_1, S_GTW]),
    OW + "/BA2": ent("Bể dự phòng (surge basin) 40-PK-2001/BA2",
                     "Bể bê tông 742,5 m³ (7.500 × 15.700 × 6.980 mm) nhận nước tràn khẩn cấp và nước mưa lớn qua cửa cống. Bơm tuần hoàn /P2 (10 m³/h, 10 m, 1,8 kW) đưa nước dần về bể API. "
                     "Trong vận hành còn dùng chứa tạm nước thải ô nhiễm cao (UFC85…) để xử lý dần.",
                     src=[PID42_1, PFD42_1, S_PA174, S_UFC]),
    OW + "/P2": ent("Bơm tuần hoàn 40-PK-2001/P2", "Bơm chìm 10 m³/h, 10 m, 1,8 kW, đưa nước từ bể dự phòng /BA2 về bể API /V1 để xử lý dần.", src=[PID42_1]),
    OW + "/V4": ent("Thiết bị tách dầu CPI 40-PK-2001/V4",
                    "Thiết bị tách tấm song song nghiêng, gợn sóng (1.500 × 2.000 × 4.000 mm). Diện tích lắng tăng, giảm chảy rối, nên tách được giọt dầu nhỏ hơn bể API. "
                    "Dầu gom trên mặt, bùn trượt xuống đáy. Nước chảy trọng lực sang bồn trộn nhanh /TK3.",
                    src=[PID42_1, S_GTW]),
    OW + "/TK1": EB, OW + "/V3": EB, OW + "/P5": EB, OW + "/P6": EB, OW + "/Z6": EB,
    OW + "/TK6": FLC, OW + "/V8": FLC, OW + "/P9": FLC, OW + "/P10": FLC, OW + "/Z7": FLC,
    OW + "/TK3": ent("Bồn trộn nhanh 40-PK-2001/TK3 (+ khuấy /Z3)",
                     "Bồn 0,8 m³ (1.000 ID × 1.200 H), cánh khuấy chân vịt /Z3 (SS316, 345 v/ph). Trộn chất phá nhũ vào nước sau CPI để phá nhũ tương dầu–nước. Nước chảy tiếp sang /TK4.",
                     src=[PID42_1, S_GTW]),
    OW + "/Z3": ent("Máy khuấy nhanh 40-PK-2001/Z3", "Cánh chân vịt SS316 Ø 290 mm, 345 v/ph, trong bồn trộn nhanh /TK3. Chạy liên động theo bơm /P1A/B.", src=[PID42_1]),
    OW + "/TK4": ent("Bồn keo tụ 40-PK-2001/TK4 (+ khuấy /Z4)",
                     "Bồn 5 m³ (2.000 ID × 1.800 H), cánh khuấy mái chèo /Z4 (SS316, 193 v/ph). Chất keo tụ kết các hạt dầu rất nhỏ thành bông để tách trong DAF. Nước sang /Z5.",
                     src=[PID42_1, S_GTW]),
    OW + "/Z4": ent("Máy khuấy keo tụ 40-PK-2001/Z4", "Cánh mái chèo SS316 Ø 186 mm, 193 v/ph (khuấy chậm tạo bông) trong /TK4. Liên động theo /P1A/B.", src=[PID42_1]),
    OW + "/Z5": ent("Thiết bị tuyển nổi DAF 40-PK-2001/Z5",
                    "Bể tuyển nổi khí hòa tan SS304 (5.700 × 1.500 × 1.365 mm) có thanh gạt váng liên tục. "
                    "Dòng tuần hoàn áp cao từ /P7A/B bão hòa không khí ở /V5. Khi giảm áp, khí tách thành bọt 30–120 µm bám lên hạt dầu/bông keo, kéo chúng nổi lên để gạt bỏ. "
                    "Nước trong chảy xuống bồn chứa cuối /TK5.",
                    src=[PID42_3, S_GTW]),
    OW + "/V5": ent("Bình bão hòa khí 40-PK-2001/V5", "Bình 8\", 10 barg. Hòa tan không khí (≈4 l/ph, 450 kPa qua XV-42211) vào dòng tuần hoàn áp cao của DAF.", src=[PID42_3, S_GTW]),
    OW + "/P7": ent("Bơm cao áp DAF 40-PK-2001/P7A/B", "Bơm ly tâm 9,6 m³/h, 52 m, 4 kW, 3.000 v/ph. Tạo dòng tuần hoàn áp cao qua bình bão hòa khí /V5 cho DAF.", src=[PID42_3]),
    OW + "/TK5": ent("Bồn chứa cuối 40-PK-2001/TK5", "Bồn 13 m³ (4.500 × 1.800 × 1.650 mm) chứa nước sau DAF. Mức LSHL-42208 (H 1.450 mm / L 500 mm) điều khiển bơm /P8A/B.", src=[PID42_3, S_GTW]),
    OW + "/P8": ent("Bơm vận chuyển cuối 40-PK-2001/P8A/B",
                    "Bơm ly tâm 20 m³/h, 30 m, 4 kW. Tự chạy/dừng theo mức /TK5 và đưa nước sang bể điều hòa TK-102 của 40-PK-2003, không qua /V6, /V7 (phiếu thay đổi 62/2018).",
                    src=[PID42_3, S_GTW]),
    OW + "/V6": ent("Bộ lọc đa lớp 40-PK-2001/V6", "Bình lọc 1.600 ID × 2.159 H, 7 barg. Thiết kế lọc tinh trước khi xả. Hiện không dùng vì nước được đưa thẳng sang 40-PK-2003 (phiếu thay đổi 62/2018).", src=[PID42_3, S_GTW]),
    OW + "/V7": ent("Bộ lọc than hoạt tính 40-PK-2001/V7", "Bình lọc 1.600 ID × 2.159 H, 7 barg. Thiết kế khử dầu còn lại. Hiện không dùng (nước đi thẳng sang 40-PK-2003).", src=[PID42_3, S_GTW]),
    OW + "/FL1": ent("Bộ lọc sơ bộ 40-PK-2001/FL1", "Lọc đứng (SS304/PP) 2 m³/h, 10 barg, cỡ giữ hạt 10 µm.", src=[PID42_1]),
    SW: ent("Cụm xử lý nước thải sinh hoạt 40-PK-2002",
            "Cụm bùn hoạt tính sục khí kéo dài, 50 m³/ngày (đỉnh 13 m³/h). Theo PFD, nước ra BOD₅ ≤ 30 mg/l, TSS ≤ 80 mg/l. "
            "Dòng nước: nước thải qua lưới rác tự động /Z1 vào bể cân bằng /BA1 → bơm /P1A/B → bể oxy hóa /BA2A/B (sục khí) → bể lắng /BA3A/B. "
            "Nước lắng tràn sang bể clo hóa /BA5 (châm NaOCl từ /TK1 bằng /P7A/B) → bơm /P4A/B qua lọc /FL1 → bể nước lọc /BA7 → bể nước sạch /BA8 → bơm ra KCN. "
            "Bùn từ bể lắng về bể ổn định bùn /BA4, một phần tuần hoàn (/P2A/B) về bể oxy hóa, phần dư sang bể lên men hiếu khí /BA6A/B rồi bơm ra xe (/P3A~D). "
            "Quạt /K1A/B/C cấp khí chung. Hiện cụm nhận ≈50 m³/ngày từ TK-102 (40-PK-2003). Bể /BA8 là bể gom cuối của toàn hệ, nhận cả nước MBR.",
            src=[PFD42_2, PID42_4, PID42_5, S_GTW]),
    SW + "/BA1": ent("Bể cân bằng 40-PK-2002/BA1", "Bể 39 m³ (3.500 × 3.550 × 4.500 mm), có sục khí. Nhận nước sau lưới rác /Z1. Hiện nhận phần nước (≈50 m³/ngày) do PM-102C/D của 40-PK-2003 bơm sang.", src=[PID42_4, S_GTW]),
    SW + "/Z1": ent("Máy nghiền rác 40-PK-2002/Z1", "Máy nghiền rác (comminutor) 2 trục, inox, 1.500 v/ph, đặt đầu vào bể cân bằng.", src=[PID42_4]),
    SW + "/P1": ent("Bơm nước thải 40-PK-2002/P1A/B", "Bơm chìm 3 m³/h, 15,5 m, 1 kW. Bơm từ bể cân bằng /BA1 lên bể oxy hóa /BA2A/B.", src=[PID42_4]),
    SW + "/BA2": ent("Bể oxy hóa 40-PK-2002/BA2A/B",
                     "Hai bể 60 m³ (5.500 × 3.550 × 3.500 mm), sục khí từ quạt /K1. Vi sinh hiếu khí oxy hóa chất hữu cơ. Nhu cầu oxy ≈50 % BOD₅, tới 125 % khi phân hủy cả bùn dư.",
                     src=[PID42_4, S_GTW]),
    SW + "/BA3": ent("Bể lắng 40-PK-2002/BA3A/B", "Bể 16 m³ (2.500 ID), có cào bùn quay trung tâm /Z2A/B (0,23 v/ph). Lắng bùn hoạt tính. Nước trong tràn sang bể clo hóa /BA5, bùn về bể ổn định /BA4.", src=[PID42_4, S_GTW]),
    SW + "/Z2": ent("Cào bùn bể lắng 40-PK-2002/Z2A/B", "Thiết bị gạt bùn truyền động trung tâm, inox, 0,23 v/ph, trong bể lắng /BA3A/B.", src=[PID42_4]),
    SW + "/K1": ent("Quạt thổi khí 40-PK-2002/K1A/B/C", "Quạt kiểu quay (rotary) 1.880 v/ph, 170 Nm³/h, 0,4 bar, 4 kW, có bộ tiêu âm /SL1A/B/C. Cấp khí chung cho bể cân bằng, bể oxy hóa và bể lên men hiếu khí.", src=[PID42_4, S_GTW]),
    SW + "/SL1": ent("Bộ tiêu âm quạt 40-PK-2002/SL1A/B/C", "Bộ tiêu âm 170 Nm³/h trên đường hút/đẩy quạt /K1A/B/C.", src=[PID42_4]),
    SW + "/BA4": ent("Bể ổn định bùn 40-PK-2002/BA4", "Bể 3,24 m³ nhận bùn từ bể lắng. Bơm /P2A/B tuần hoàn bùn về bể oxy hóa, phần dư sang bể lên men hiếu khí /BA6A/B.", src=[PID42_4, S_GTW]),
    SW + "/P2": ent("Bơm tuần hoàn bùn 40-PK-2002/P2A/B", "Bơm chìm 3 m³/h, 15,5 m, 1 kW. Đưa bùn hoạt tính về bể oxy hóa để giữ nồng độ bùn.", src=[PID42_4]),
    SW + "/BA6": ent("Bể lên men hiếu khí 40-PK-2002/BA6A/B", "Bể 11 m³ (2.500 × 1.400 × 3.500 mm), sục khí để ổn định bùn dư. Bùn được bơm /P3A~D ra xe định kỳ (dòng 42.4, ≈20 ngày/lần).", src=[PID42_4, PFD42_2]),
    SW + "/P3": ent("Bơm vận chuyển bùn 40-PK-2002/P3A~D", "Bơm chìm 3 m³/h, 15,5 m, 1 kW, chuyển bùn giữa các bể và ra xe bồn.", src=[PID42_4]),
    SW + "/BA9": ent("Hố van 40-PK-2002/BA9", "Hố van 3,8 m³ (2.500 × 1.550 × 1.000 mm) của cụm sinh hoạt.", src=[PID42_4]),
    SW + "/P8": ent("Bơm nước mưa 40-PK-2002/P8", "Bơm chìm 6 m³/h, 15 m, 2 kW, bơm nước mưa đọng trong khu vực cụm.", src=[PID42_4]),
    SW + "/BA5": ent("Bể clo hóa 40-PK-2002/BA5", "Bể 13 m³ (4.000 × 2.800 × 1.800 mm). Nước lắng được khử trùng bằng NaOCl (bồn /TK1 680 l, bơm màng /P7A/B 17,5 l/h). Bơm /P4A/B (3 m³/h, 30 m) đưa qua lọc /FL1.", src=[PID42_5, S_GTW]),
    SW + "/TK1": ent("Bồn NaOCl 40-PK-2002/TK1", "Bồn 680 l (755 ID × 1.530 H) chứa javel. Bơm màng /P7A/B (17,5 l/h, 0,25 kW) châm vào bể clo hóa /BA5.", src=[PID42_5]),
    SW + "/P4": ent("Bơm nước khử trùng 40-PK-2002/P4A/B", "Bơm chìm 3 m³/h, 30 m, 2,1 kW. Bơm từ bể clo hóa qua bộ lọc đa lớp /FL1.", src=[PID42_5]),
    SW + "/FL1": ent("Bộ lọc đa lớp 40-PK-2002/FL1", "Bình lọc 600 ID × 1.800 H, 7 barg. Lọc nước sau khử trùng, nước lọc về bể /BA7. Nước rửa ngược về bể bùn.", src=[PID42_5]),
    SW + "/BA7": ent("Bể nước lọc 40-PK-2002/BA7", "Bể 51 m³ (4.700 × 3.400 × 3.800 mm). Bơm /P5A/B (10 m³/h, 20 m) dùng rửa ngược lọc. Nước tràn sang bể nước sạch /BA8.", src=[PID42_5]),
    SW + "/P5": ent("Bơm bể nước lọc 40-PK-2002/P5A/B", "Bơm chìm 10 m³/h, 20 m, 2,1 kW, đặt trong bể nước lọc /BA7.", src=[PID42_5]),
    SW + "/BA8": ent("Bể nước sạch cuối 40-PK-2002/BA8",
                     "Bể 200 m³ (9.000 × 7.400 × 3.800 mm), là bể gom cuối của toàn hệ thống XLNT. Nhận nước của cụm sinh hoạt và nước qua màng MBR của 40-PK-2003. "
                     "Nước được bơm ra hệ thống xử lý tập trung KCN Phú Mỹ (IZICO) bằng /P6A/B (13 m³/h) hoặc /P9A/B mới (50 m³/h). "
                     "Shock javel định kỳ: hạ mức ≈20 %, dừng /P6A/B, châm 30 l javel 10 % (Cl₂ dư ≥ 1 mg/l). Khi mức 80 % và Cl₂ dư < 2 mg/l thì bơm ra KCN.",
                     src=[PID42_5, S_GTW, S_UFC]),
    SW + "/P6": ent("Bơm nước sạch 40-PK-2002/P6A/B", "Bơm chìm 13 m³/h, 14,5 m, 1,5 kW. Bơm nước từ bể /BA8 ra KCN. Khi shock javel thì dừng để giữ nước trong bể.", src=[PID42_5, S_GTW]),
    SW + "/P9": ent("Bơm nước sạch mới 40-PK-2002/P9A/B", "Bơm ly tâm 50 m³/h, 20 m, 4 kW (motor 380 V, IP55). Bổ sung để bơm lưu lượng lớn hơn từ bể /BA8 ra KCN khi hệ MBR chạy.", src=[PID42_5]),
    "40-PK-2003": ent("Hệ thống xử lý nước thải mới 40-PK-2003 (MBR)",
                      "Hệ khử nitơ + màng sinh học MBR (2012), ≈680 m³/ngày (200 m³/ngày sinh hoạt + 480 m³/ngày nhiễm dầu đã tách dầu), sau mở rộng nhận thêm nước nhà máy CO₂ và UFC85. "
                      "Dòng chính: TK-100 → FS-101 → TK-102 → TK-103 → TK-104 → TK-105 (MBR) → 40-PK-2002/BA8. "
                      "Các bể sinh học giữ MLSS 11.500–15.000 mg/l. Nitrat hóa ở TK-104/TK-105 theo 2 bậc (Nitrosomonas: NH₄⁺ → NO₂⁻; Nitrobacter: NO₂⁻ → NO₃⁻). "
                      "Khử nitrat thành N₂ ở TK-103 nhờ dòng tuần hoàn nước (FM-104C/D ≈4Q) và bùn (PM-105C/D). "
                      "Màng Kubota lỗ 0,4 µm giữ toàn bộ bùn, không cần bể lắng. Hóa chất: H₃PO₄ (dinh dưỡng), mật rỉ (cacbon), NaOH, NaOCl + axit oxalic (rửa màng), polymer (ép bùn). "
                      "Hệ được điều khiển bằng PLC (loop 01~10), đo mức siêu âm LS-100/102/104/105/201.",
                      [{"h": "Thiết bị (P&ID 2539-42-PID-0031-06)",
                        "tb": [["Hạng mục", "Tag", "Thông số"],
                               ["Bể gom", "TK-100, bơm PM-100A/B", "31,5 m³; bơm theo mức (H 2,8 / L 1,5 m)"],
                               ["Máy sàng rác tinh", "FS-101", "Loại rác > 1 mm"],
                               ["Bể điều hòa", "TK-102, bơm PM-102A/B (→TK-103), PM-102C/D (→40-PK-2002)", "256 m³; FM-100, FM-102CD; sục khí BL-102A/B"],
                               ["Bể khử nitơ", "TK-103, khuấy chìm SM/MX-103A~D", "147 m³; thiếu khí, kín, có quạt hút & tháp khử mùi"],
                               ["Bể đệm", "TK-104, sục chìm JE-104A~D, bơm PM-104A/B, PM-104C/D", "205 m³"],
                               ["Bể MBR", "TK-105, module MB-105A1~4/B1~4, bơm PM-105A1~2/B1~2, PM-105C/D", "360 m³; TMP ≤ 20 kPa; khí ≥ 2 m³/ph/module"],
                               ["Thổi khí", "BL-102A/B, BL-105A/B/C (Roots)", "—"],
                               ["Bùn", "TK-201 bể nén, sân phơi TK-202A/B (máy ép BF-202 ngừng 12/2025)", "42 m³; bùn 15–20 m³/ngày"],
                               ["Hóa chất", "DR-401~406, DP-401~404, DP-504", "H₃PO₄, axit oxalic, polymer, NaOCl, NaOH, mật rỉ"]]},
                       {"h": "Lưu ý",
                        "ul": ["Không để bơm bể đệm PM-104A/B ngừng quá 1 giờ khi PM-102A/B vẫn chạy (nguy cơ tràn TK-103/TK-104).",
                               "Lưu lượng sang TK-105 (FM-104A/B) phải luôn nhỏ hơn 0,9 lần lưu lượng hút màng (FM-105A/B).",
                               "Nước UFC85, CO₂ đưa vào không liên tục, phải kiểm soát lưu lượng và chất lượng. Khi tải N cao, giảm tải và bổ sung COD theo G2-00-PA-174.",
                               "Màng MBR đang được xem xét thay bằng nhà sản xuất tương đương (đề xuất STVB127286; so sánh Kubota, KOReD, LG)."]}],
                      [PID42_N, S_GTW, S_STAY, S_SH, S_KUB, S_EP, S_SPB, S_PA174]),
    "40-V-2001": ent("Bình nhúng khí NH₃ 40-V-2001 (cụm tách NH₃ cũ)",
                     "Bình 0,2 m³ chứa đầy nước, nhúng hơi NH₃ thoát ra từ bể cân bằng 40-BA-2001 trước khi thải ra khí quyển. Cụm tách NH₃ (Unit 42 section 100) đã ngừng hoạt động.",
                     src=[PID42_6]),
    "40-P-2001": ent("Bơm cấp tháp tách NH₃ 40-P-2001A/B (đã ngừng)",
                     "Bơm ly tâm 8,1 m³/h, 51 m, 5,5 kW, đặt trong bể cân bằng 40-BA-2001 (420 m³, 16.000 × 7.500 × 3.500 mm). "
                     "Bể này nhận nước nhiễm NH₃ (xả kín NH₃ từ 10-T-5053, nước nhiễm NH₃ cụm 30-PK-1001, nước ngưng đỉnh 40-T-2001…). "
                     "Bơm đưa nước qua 40-E-2001 lên tháp 40-T-2001. Theo P&ID 2025, hệ thống không còn hoạt động, một số thiết bị đã tháo.",
                     src=[PID42_6]),
    "40-T-2001": ent("Tháp tách NH₃ 40-T-2001 (đã ngừng)",
                     "Tháp đĩa 15 đĩa, 700/1.500 ID × 11.560 H, thiết kế 3,5 barg / 235 °C. Dùng hơi LP sục từ đáy (FIC-42003) để tách NH₃ khỏi nước thải. "
                     "Khí NH₃ đỉnh (PIC-42001) đi sang đuốc 40-PK-1001. Nước đáy (LIC-42002) qua 40-E-2001 về bể 30-BA-3001. "
                     "Ghi chú P&ID cập nhật 12/2025: hệ tách NH₃ đã ngừng và thay bằng giải pháp công nghệ khác (MOC M125/2025/DP.XP), một số thiết bị đã tháo.",
                     src=[PID42_7, PID42_6]),
    "40-E-2001": ent("TĐN tấm tháp tách NH₃ 40-E-2001 (đã ngừng)",
                     "TĐN tấm 421,88 kW, 32,4 m², thiết kế 7 barg / 150 °C. Gia nhiệt nước cấp tháp 40-T-2001 bằng nước đáy tháp nóng. Thuộc cụm tách NH₃ đã ngừng (12/2025).",
                     src=[PID42_7]),
    "40-P-2002": ent("Bơm nước đáy tháp tách NH₃ 40-P-2002A/B (đã ngừng)",
                     "Bơm ly tâm 7,1 m³/h, 28 m, 3 kW, 2.950 v/ph, có làm mát seal bằng nước sạch. Bơm nước đáy 40-T-2001 qua 40-E-2001 về bể nước sông 30-BA-3001. Thuộc cụm tách NH₃ đã ngừng.",
                     src=[PID42_7]),
}

# motor / tuabin dẫn động dùng chung đoạn với bơm
for a, b in (("30-MP-3001", "30-P-3001"), ("30-MP-3002", "30-P-3002"), ("30-MP-3010", "30-P-3010"), ("30-STP-3001A", "30-P-3001A"),
             ("30-STP-3002A", "30-P-3002A"), ("30-STP-5002A", "30-P-3002A"), ("30-P-3003A", "30-P-3003")):
    TAGS33[a] = TAGS33[b]
for a, b in (("40-MP-2001", "40-P-2001"), ("40-MP-2002", "40-P-2002")):
    TAGS42[a] = TAGS42[b]

UNITS = {"33": UNIT33, "42": UNIT42}
TAGS = {**TAGS33, **TAGS42}
