"""Công nghệ Unit 45 (kho chứa NH3) và Unit 41 (hệ thống đuốc).

Nguồn: PFD 2539-45-PFD-0010-01-01 as-built, PFD 2098-41-PFD-0010-1/2, mô tả công nghệ revamp 2539-45-CN-0009-01
(bản tiếng Việt "Unit 45 PROCESS DESCRIPTION VIE.docx"), mô tả liên động 2539-45-CN-0009-02 (scan → OCR),
sổ tay 40-PK-5001 (Industrie Technofrigo Dell'Orto, scan → OCR), data sheet bơm Flowserve, mô tả đuốc "descrip.doc",
phiếu đề nghị thay đổi purge đuốc bằng N₂ (2014).
"""
R = "6. Bon chua amonia & Flare/"


def sh(dwg, label):
    return ["sheet:" + dwg, label]


def ent(t, intro, s=None, src=None):
    return {"t": t, "intro": intro, "s": s or [], "src": src or []}


PFD45 = sh("2539-45-PFD-0010-01-01 (trang 1)", "PFD 2539-45 kho NH3 (as-built)")
PID45_1 = sh("2539-45-PID-0031-01", "P&ID 45-01 Bồn chứa NH3")
PID45_2 = sh("2539-45-PID-0031-02", "P&ID 45-02 Bơm & cần nạp hiện hữu")
PID45_3 = sh("2098-45-PID-0031-03", "P&ID 45-03 Cụm làm lạnh 40-PK-5001")
PID45_4 = sh("2539-45-PID-0031-04", "P&ID 45-04 Tuyến nạp mới")
PID45_5 = sh("2539-45-PID-0031-05", "P&ID 45-05 Cụm làm lạnh mới 40-PK-5005")
PFD41_1 = sh("2098-41-PFD-0010-1-2", "PFD 2098-41 Đuốc NH3")
PFD41_2 = sh("2098-41-PFD-0010-2-2", "PFD 2098-41 Đuốc khí tổng hợp")
PID41_1 = sh("2098-41-PID-0031-01", "P&ID 41-01 Đuốc NH3")
PID41_2 = sh("2098-41-PID-0031-02", "P&ID 41-02 Đuốc khí tổng hợp")

S_VIE = [R + "Revamp/1. PROCESS DESCRIPTION/Unit 45 PROCESS DESCRIPTION VIE.docx", "Mô tả công nghệ kho NH3 (tiếng Việt)"]
S_CN = [R + "Revamp/1. PROCESS DESCRIPTION/2539-45-CN-0009-01_0.pdf", "2539-45-CN-0009-01 Mô tả công nghệ revamp"]
S_ILK = [R + "Revamp/5. Tài Liệu Tham Khảo/INTERLOCK PROCESS DESCRIPTION/2539-45-CN-0009-02_0.pdf", "2539-45-CN-0009-02 Mô tả liên động"]
S_PK1C = [R + "40-PK-5001/40-PK-5001/Vendor Data Book/Operating manual/C) Plant & Logic Description.pdf", "40-PK-5001 · C – Logic điều khiển"]
S_PK1A = [R + "40-PK-5001/40-PK-5001/Vendor Data Book/Operating manual/A) Data Sheets.pdf", "40-PK-5001 · A – Data sheet"]
S_PK5CP = [R + "Revamp/5. Tài Liệu Tham Khảo/Process Description  Control Philosophy/2539-4151-01-A0101-001_A_Code 1.pdf", "40-PK-5005 · Mô tả & triết lý điều khiển"]
S_PK5OP = [R + "Revamp/5. Tài Liệu Tham Khảo/40-PK-5005 operation.pdf", "40-PK-5005 · Hướng dẫn vận hành"]
S_PK5DS = [R + "Revamp/4. DATASHEET/40-PK-5005/2539-45-SP-4151-01_PB.pdf", "Data sheet 40-PK-5005"]
S_PDS = [R + "40-P-5001AB 5002/Datasheet.pdf", "Data sheet & thử bơm 40-P-5001/5002"]
S_P3DS = [R + "Revamp/4. DATASHEET/40-P-5003/2539-45-SP-0910-01_A.pdf", "Data sheet 40-P-5003"]
S_E2DS = [R + "Revamp/4. DATASHEET/40-E-5002/2539-45-SP-0710-01_PB.pdf", "Data sheet 40-E-5002"]
S_TKP = [R + "40-TK-5001/Kiểm soát áp suất bồn chứa NH3.doc", "Kiểm soát áp suất bồn chứa NH3"]
S_TKBOG = [R + "40-TK-5001/Doc/L00206.doc", "40-TK-5001 · L00206 tính toán xả an toàn"]
S_TKCD = [R + "40-TK-5001/Doc/L00243.doc", "40-TK-5001 · L00243 đuổi khí & làm lạnh bồn"]
S_FDESC = [R + "40-PK-1001-1002/40-PK-1001-1002&20-PK-1005/descrip.doc", "Mô tả hệ thống đuốc (descrip.doc)"]
S_FN2 = [R + "40-PK-1001-1002/02-2014-CNSX.pdf", "Đề nghị thay đổi purge đuốc bằng N₂ (2014)"]
S_FBD = [R + "40-PK-1001-1002/Report flare BDTT 2023 Rev.1.pdf", "Báo cáo đuốc BDTT 2023"]
S_KO = [R + "Quy trình phương án liên quan/Phương án xử lý nước nhiễm NH3 tại knock out drum 40V1001.pdf", "PA xử lý nước nhiễm NH3 tại 40-V-1001"]

UNIT45 = {
    "t": "Công nghệ Unit 45 – Bồn chứa Amoniac",
    "intro": "Kho NH3 gồm ba phần. Bồn 40-TK-5001 chứa NH3 lỏng −33 °C ở áp suất khí quyển. Hai cụm làm lạnh 40-PK-5001 và 40-PK-5005 hóa lỏng lại hơi NH3 bay ra trong bồn. "
             "Hệ bơm và cần nạp chuyển NH3 sang xưởng Urê, nạp xe bồn và cấp cho xưởng NPK. "
             "Sau revamp (Amoniac 1.620 t/ngày) có thêm cụm làm lạnh 40-PK-5005, bơm 40-P-5003, bộ gia nhiệt 40-E-5002 và hai tuyến cần nạp 40-LA-5003…5006.",
    "s": [
        {"h": "Sơ đồ dòng (PFD as-built)",
         "ul": ["Bình thường (case 2), phần lớn NH3 của xưởng Amoniac đi thẳng sang Urê. Khoảng 11,25 t/h NH3 lỏng −33 °C, 5 barg đi qua đường ống bảo ôn về bồn 40-TK-5001. "
                "Khi Urê dừng (case 3), toàn bộ sản lượng 67,5 t/h về bồn.",
                "Hơi NH3 trong bồn (0,07 barg, −33 °C) được hút về 40-PK-5001 (≈510–681 kg/h) và 40-PK-5005 (≈140–253 kg/h). Hai cụm nén, ngưng và trả NH3 lỏng về bồn. "
                "Một phần hơi (tối đa ≈400 kg/h) có thể đưa về cụm làm lạnh của xưởng Amoniac (10-K4051) qua đường 6\".",
                "Bơm chuyển 40-P-5001A/B (dự phòng 1) cấp NH3 lỏng sang Urê khi xưởng Amoniac không cấp được. Lưu lượng tối đa 96,25 t/h khi Urê lấy NH3 từ bồn.",
                "Nạp xe bồn: bơm 40-P-5002 → bộ gia nhiệt 40-E-5001 → cần nạp 40-LA-5001. Bơm 40-P-5003 → bộ gia nhiệt 40-E-5002 → cần nạp 40-LA-5003/5005. "
                "NH3 được gia nhiệt lên +4 °C ở 24 barg trước khi nạp, khoảng 16,5–20 t/h mỗi tuyến. "
                "Hơi từ xe trả về bồn qua các cần hồi hơi 40-LA-5002/5004/5006 và van PV-45007 / PV-45014.",
                "Cấp NH3 lỏng cho xưởng NPK: thường 3,45 t/h ở 23,3 barg / +4 °C, thiết kế 10,06 t/h.",
                "Hơi dư không thu hồi được và các van an toàn xả về đuốc NH3 40-PK-1001 qua header riêng 10\" của bồn chứa."],
         "src": [PFD45, S_VIE, S_CN]},
        {"h": "Nguồn sinh hơi trong bồn (thiết kế revamp)",
         "tb": [["Nguồn", "kg/h"], ["Nạp NH3 lỏng vào bồn", "181"], ["Thay đổi áp suất bồn (mức 50 %)", "191"], ["Nhiệt rò vào bồn (mức 50 %)", "188"],
                ["Nhiệt từ dòng hồi lưu bơm", "26"], ["Hơi hồi từ cần nạp (2 xe nạp song song, 6 barg / 4 °C)", "304"], ["Tổng", "890"]],
         "p": ["Hai cụm làm lạnh có tổng công suất ≈850 kg/h: 40-PK-5001 600 kg/h (227,8 kW lạnh) và 40-PK-5005 250 kg/h (95 kW lạnh)."],
         "src": [S_VIE, S_CN]},
        {"h": "Thiết bị chính",
         "tb": [["Tag", "Chức năng", "Thông số"],
                ["40-TK-5001", "Bồn chứa NH3 lạnh, vỏ kép kim loại", "35.000 m³, Ø42.700 × 28.500 mm; 23.800 / 20.000 t (thiết kế / làm việc); 0,15 / −0,005 barg; −33 °C"],
                ["40-PK-5001", "Cụm làm lạnh hơi NH3 (Technofrigo, máy nén trục vít Mycom N200MUD-HE)", "600 kg/h hơi; 227,8 kW lạnh; 2 máy nén 180 kW"],
                ["40-PK-5005", "Cụm làm lạnh hơi NH3 mới (revamp)", "250 kg/h hơi; 95 kW lạnh; 2 máy nén trục vít phun dầu (1 chạy, 1 dự phòng)"],
                ["40-P-5001A/B", "Bơm chuyển NH3 sang Urê (vertical barrel)", "85 m³/h; 368 m; 110 kW; 2.950 v/ph"],
                ["40-P-5002 / 40-P-5003", "Bơm nạp xe bồn", "85 m³/h; 368 m; 110 kW (Flowserve 100 WUC-2R-6)"],
                ["40-E-5001 / 40-E-5002", "Bộ gia nhiệt NH3 kiểu quạt không khí (air fin) có cuộn hơi LP", "933,1 kW mỗi bộ; −33 → +4 °C"],
                ["40-LA-5001/5003/5005", "Cần nạp NH3 lỏng", "30 m³/h mỗi cần (5005 dự phòng)"],
                ["40-LA-5002/5004/5006", "Cần hồi hơi", "Tốc độ hơi ≤ 15 m/s"],
                ["40-PK-5002/5003/5004", "Cụm đo đếm NH3 xuất", "2.000–20.000 kg/h"]],
         "src": [PFD45, S_VIE, S_PK1A, S_PDS]},
        {"h": "Liên động bảo vệ (ESD)",
         "ul": ["40-IS45001 mức bồn: mức cao-cao (2/3 LSHH-45001A/B/C) đóng LV-45001 trên đường NH3 từ xưởng Amoniac. "
                "Mức thấp-thấp (2/3 LSLL) dừng bơm 40-P-5001A/B, 40-P-5002, 40-P-5003.",
                "40-IS45002 áp bồn: áp cao-cao (2/3 PSHH-45001) mở hết PV-45005 xả hơi về đuốc NH3. "
                "Áp thấp-thấp dừng máy nén 40-PK-5001/K1A/B và 40-PK-5005/K1A/B, đóng HV-45002 trên đường ra bơm, dừng các bơm. "
                "Áp thấp-thấp-thấp mở hết PV-45001 cấp N₂ đệm chống chân không cho bồn.",
                "40-IS45004 cần hồi hơi: áp cao-cao trên 40-LA-5002/5004/5006 khi đang nạp thì dừng các bơm và đóng các van TV/FV của tuyến nạp.",
                "Tuyến nạp mới (I-N2/I-N3): áp cao-cao, nhiệt độ thấp-thấp sau bộ gia nhiệt, hoặc lưu lượng cao-cao thì đóng TV-45017 / FV-45405 (FV-45406). "
                "Motor quạt bộ gia nhiệt dừng khi rung cao."],
         "src": [S_ILK]},
        {"h": "Điều khiển cụm làm lạnh",
         "ul": ["Tải máy nén được chỉnh bằng slide valve theo áp hút. Tín hiệu lấy từ áp bồn PIC-45004, hoặc ở 40-PK-5005 có thể chọn áp đầu vào PIT-45466. "
                "Điều khiển tỉ lệ có vùng chết, chu kỳ 10 giây (40-PK-5001: PIC-45701).",
                "Mỗi cụm đặt ngưỡng load/unload khác nhau theo PIC-45004. 40-PK-5005 được đặt vào tải trước và giảm tải sau, để 40-PK-5001 chạy ổn định.",
                "Chế độ Auto chỉ chạy 1 máy nén mỗi cụm. Nếu chạy tay cả hai máy, chức năng STOP LOAD / FORCE UNLOAD tự ghi đè khi áp hút thấp, áp đẩy cao hoặc dòng motor cao."],
         "src": [S_VIE, S_PK1C, S_PK5CP]},
    ],
    "src": [S_VIE, S_CN, S_ILK],
}

TAGS45 = {
    "40-TK-5001": ent("Bồn chứa NH3 40-TK-5001",
                      "Bồn chứa NH3 lỏng lạnh −33 °C ở áp gần khí quyển, kết cấu vỏ kép kim loại: cả bồn trong và bồn ngoài đều chứa được toàn bộ NH3. "
                      "Dung tích 35.000 m³ (Ø42.700 × 28.500 mm), sức chứa 23.800 t thiết kế, 20.000 t làm việc. "
                      "Áp thiết kế 0,15 / −0,005 barg; nhiệt độ thiết kế 60 / −45 °C; bảo ôn 100 mm. Bồn do Samsung Heavy Industries chế tạo theo API 620, thép A516-60.",
                      [{"h": "Kiểm soát áp suất",
                        "ul": ["Áp bồn (≈0,07 barg) được giữ bằng hai cụm làm lạnh 40-PK-5001 / 40-PK-5005, theo tín hiệu PIC-45004.",
                               "Áp cao: PV-45005 xả hơi về đuốc NH3 40-PK-1001. Áp cao-cao (2/3) mở hết PV-45005. Bồn có van thở / van an toàn (PVRV); lưu lượng xả tính theo nhiệt rò ≈327 kg/h.",
                               "Áp thấp-thấp: dừng máy nén và bơm, đóng HV-45002. Áp thấp-thấp-thấp: mở PV-45001 cấp N₂ đệm chống chân không.",
                               "Mức: LSHH 2/3 đóng LV-45001 (NH3 từ xưởng Amoniac); LSLL 2/3 dừng các bơm."]},
                       {"h": "Lưu ý",
                        "p": ["Bồn NH3 lạnh có nguy cơ ăn mòn ứng suất (SCC). Thư mục \"SCC NH3 Tank\" có tài liệu tham khảo về kiểm tra bồn. "
                              "Quy trình đuổi khí và làm lạnh bồn bằng N₂ có trong tài liệu L00243."]}],
                      [S_VIE, S_ILK, S_TKP, S_TKBOG, S_TKCD, PID45_1]),
    "40-PK-5001": ent("Cụm làm lạnh hơi NH3 40-PK-5001",
                      "Cụm của Industrie Technofrigo Dell'Orto (MR 2098-MR-4151-50) gồm 2 máy nén trục vít Mycom N200MUD-HE (K1A/K1B, motor 180 kW, 2.950 v/ph). "
                      "Công suất 600 kg/h hơi NH3 (227,8 kW lạnh); hơi hút ≈1 bara, đẩy ≈17,7 bara. "
                      "Hơi nén được tách dầu (V3), ngưng, rồi NH3 lỏng trả về bồn. Một đường 6\" từ đầu hút K1B nối sang máy nén lạnh 10-K4051 của xưởng Amoniac.",
                      [{"h": "Logic điều khiển (vendor)",
                        "ul": ["Khởi động tay hoặc tự động (từ DCS, PLC, tại chỗ). Điều kiện khởi động: không có trip, nhiệt độ dầu ở bình tách V3 đủ cao (TT-45708), có tín hiệu cho phép từ DCS (HS-45799).",
                               "Máy chỉ khởi động khi slide valve ở 0 %. Bơm dầu chạy trước khoảng 10 giây; nếu không đủ áp dầu thì dừng vì áp dầu thấp-thấp. "
                               "Nếu slide valve không về 0 % trong 3 phút thì không khởi động được.",
                               "Máy dự phòng không tự khởi động. Bơm dầu dự phòng tự chạy khi motor bơm dầu chính hỏng.",
                               "Điều khiển tải tự động theo áp hút PIT-45004 / PIC-45701, bằng xung đến van điện từ load/unload, chu kỳ 10 giây, có vùng chết.",
                               "Motor chính khởi động tối đa 3 lần/giờ (chống quá nhiệt, chờ 20 phút). Bộ gia nhiệt dầu E-5001A/B/C chỉ bật khi máy nén dừng."]}],
                      [S_PK1C, S_PK1A, S_VIE, PID45_3]),
    "40-PK-5005": ent("Cụm làm lạnh hơi NH3 mới 40-PK-5005",
                      "Cụm lắp mới khi revamp, chạy song song với 40-PK-5001. Công suất 250 kg/h hơi NH3 (95 kW lạnh) ở −33 °C, áp khí quyển; máy nén định mức ≈378 kg/h kể cả ≈100 kg/h hơi từ sub-cooler. "
                      "Có 2 máy nén trục vít phun dầu (K1A/B, 1 chạy, 1 dự phòng). Mỗi máy có bình tách dầu V3, làm mát dầu E2, lọc dầu FL1 và bơm dầu P1 riêng. "
                      "Thiết bị ngưng E1, bình chứa V2, sub-cooler V1, bình chưng cất dầu V4 và bộ xả khí trơ dùng chung.",
                      [{"h": "Dòng công nghệ",
                        "ul": ["Hơi NH3 từ bồn vào phía vỏ sub-cooler V1; các tấm ngăn tách hạt lỏng, rồi hơi khô vào đầu hút máy nén.",
                               "Hơi nén qua bình tách dầu V3A/B (tách bằng đổi hướng dòng và lọc coalescer, dầu còn ≤ 5 ppm), rồi vào thiết bị ngưng E1 làm mát bằng nước. NH3 lỏng chảy xuống bình chứa V2.",
                               "Lỏng từ V2 chia hai: một phần qua LV-45410 vào phía vỏ V1, bay hơi để làm lạnh sâu phần còn lại đi trong ống. Phần trong ống qua LV-45409 về bồn 40-TK-5001.",
                               "Khi tải thấp, hơi nóng (hot-gas bypass) qua PV-45466 vào vỏ V1 để giữ áp hút.",
                               "Dầu tích tụ trong V1 được thu hồi ở bình V4: xả lỏng xuống, gia nhiệt để đuổi NH3 về V1, rồi xả dầu. Phải đóng van B1-186 trước khi bật heater."],
                        "src": [S_VIE, PID45_5]},
                       {"h": "Dầu bôi trơn",
                        "ul": ["Dầu tuần hoàn qua máy nén để bôi trơn, làm kín và làm mát. Nhiệt độ dầu cấp giữ ổn định bằng van 3 ngả TCV-45730/45731 qua thiết bị làm mát dầu kiểu tấm E2A/B. "
                               "Lọc dầu bằng sợi thủy tinh 1–6 µm.",
                               "Khi máy dừng, heater giữ nóng dầu ở V3 để NH3 không hấp thụ vào dầu gây sủi bọt và mức dầu thấp (có thể gây trip).",
                               "Bơm dầu P1A/B chỉ chạy khi PLC thấy nhu cầu dầu tăng."]},
                       {"h": "Điều khiển", "ul": ["Tải điều khiển bằng slide valve theo PIC-45004 (áp bồn) hoặc PIT-45466 (áp đầu vào), chọn bằng công tắc. Vào tải trước 40-PK-5001.",
                                                  "STOP LOAD / FORCE UNLOAD tự ghi đè khi áp hút thấp, áp đẩy cao hoặc dòng motor cao."]}],
                      [S_VIE, S_PK5CP, S_PK5OP, S_PK5DS]),
    "40-P-5001": ent("Bơm chuyển NH3 40-P-5001A/B",
                     "Bơm ly tâm nhiều cấp kiểu vertical barrel (Flowserve/Worthington 100 WUC-2R-6): 85 m³/h, cột áp 368 m, NPSHr 2,5 m, motor 110 kW, 2.950 v/ph (thử tại xưởng: hiệu suất 65,9 %, 87,8 kW). "
                     "Bơm NH3 lỏng −33 °C từ bồn sang xưởng Urê khi xưởng Amoniac không cấp được. 40-P-5001B dự phòng chung cho 40-P-5001A và bơm nạp 40-P-5002. "
                     "Dừng khi bồn mức thấp-thấp, áp thấp-thấp, HV-45002 đóng, hoặc áp cao-cao trên cần hồi hơi.",
                     src=[S_PDS, S_VIE, S_ILK, PID45_2]),
    "40-P-5002": ent("Bơm nạp xe bồn 40-P-5002",
                     "Cùng kiểu với 40-P-5001 (Flowserve 100 WUC-2R-6, 85 m³/h, 368 m, 110 kW). Cấp tuyến nạp 1: qua bộ gia nhiệt 40-E-5001 đến cần nạp 40-LA-5001 (40-LA-5005 dự phòng). "
                     "Một bơm đủ nạp đồng thời 2 xe (10 t/xe).", src=[S_PDS, S_VIE, S_ILK, PID45_2]),
    "40-P-5003": ent("Bơm nạp xe bồn 40-P-5003 (mới)",
                     "Bơm lắp mới khi revamp: 85 m³/h, 368 m, 110 kW, kiểu vertical barrel, có hệ khí đệm (buffer gas) cho phớt. "
                     "Cấp tuyến nạp 2: qua bộ gia nhiệt 40-E-5002 đến cần nạp 40-LA-5003 (40-LA-5005 dự phòng).", src=[S_P3DS, S_VIE, S_ILK, PID45_4]),
    "40-E-5001": ent("Bộ gia nhiệt NH3 40-E-5001",
                     "Thiết bị trao đổi nhiệt kiểu quạt không khí (air fin) có cuộn gia nhiệt hơi LP (3,4 barg, 220 °C; ≈1,57 t/h). Công suất 933,1 kW. "
                     "Gia nhiệt NH3 lỏng từ −33 °C lên +4 °C trước khi nạp xe bồn, để tránh nạp NH3 quá lạnh vào xe. Motor quạt dừng khi rung cao (VSH-45011A/B).",
                     src=[PFD45, S_VIE, S_ILK]),
    "40-E-5002": ent("Bộ gia nhiệt NH3 40-E-5002 (mới)",
                     "Giống 40-E-5001: kiểu air fin có cuộn hơi, 933,1 kW, cấp cho tuyến nạp 40-P-5003 / 40-LA-5003. "
                     "TV-45017 điều khiển nhiệt độ và đóng khi nhiệt độ sau bộ gia nhiệt thấp-thấp (TT-45017). Motor quạt dừng khi rung cao (VSH-45404/45405).",
                     src=[S_E2DS, S_VIE, S_ILK, PID45_4]),
}
for k, base in (("40-MP-5001", "40-P-5001"), ("40-MP-5002", "40-P-5002"), ("40-MP-5003", "40-P-5003")):
    TAGS45[k] = TAGS45[base]

UNIT41 = {
    "t": "Công nghệ Unit 41 – Hệ thống đuốc",
    "intro": "Hệ thống đuốc đốt bỏ khí xả an toàn và khí thải có NH3 hoặc hydrocacbon của nhà máy. Có hai đuốc riêng: đuốc NH3 40-PK-1001 và đuốc khí tổng hợp 40-PK-1002, kèm bình tách lỏng (KO drum) 40-V-1001. "
             "Khí chứa CO/CO₂ và khí chứa NH3 được tách riêng để tránh tạo carbamate làm tắc đường ống.",
    "s": [
        {"h": "Thiết bị",
         "tb": [["Tag", "Chức năng", "Thông số"],
                ["40-PK-1001", "Đuốc NH3 (giằng cáp)", "298.190 kg/h; ống 42\" × 45 m và 6\" × 45 m (riser riêng cho khí bồn chứa)"],
                ["40-PK-1002", "Đuốc khí tổng hợp (giằng cáp)", "349.674 kg/h; 42\" × 45 m"],
                ["40-V-1001", "Bình tách lỏng (KO drum) đuốc khí tổng hợp", "Ø4.000 × 13.400 mm; 3,5 barg / 360 °C"]],
         "src": [PFD41_1, PFD41_2, S_FDESC]},
        {"h": "Đuốc NH3 40-PK-1001",
         "ul": ["Header 40\" gom khí xả NH3 từ xưởng Amoniac. Header 10\" riêng gom khí từ bồn 40-TK-5001 (khác yêu cầu áp ngược) đi lên riser riêng, có đầu đuốc và fluidic seal riêng. "
                "Một header riêng nữa từ tháp stripping NH3 40-T2001 (hơi nước ≈952 kg/h, NH3 1–199 kg/h).",
                "Trường hợp thiết kế: (1) 10-K-4031 kẹt đầu ra – 298.190 kg/h, 65,9 % H₂; (2) 10-K-4041 đầu đẩy cấp 2 – 83.185 kg/h NH3; "
                "(3) 10-K-4051 hỏng – 6.940 kg/h; (4) bồn NH3 – 1.140 kg/h, −29 °C, 0,01 barg; (5) cháy 40-PK-5001 – 2.508 kg/h. Trường hợp 1 (hoặc 2, 3) có thể xảy ra cùng lúc với trường hợp 4.",
                "Khí nhiên liệu bổ sung ở đỉnh đuốc để khí NH3 cháy được; lưu lượng điều khiển qua FO-41501 và HV-41002 (HIC-41002, FIC-41001A override)."],
         "src": [S_FDESC, PFD41_1, PID41_1]},
        {"h": "Đuốc khí tổng hợp 40-PK-1002",
         "ul": ["Header 36\" gom khí xả từ phần đầu xưởng Amoniac (reforming, tách CO₂), qua KO drum 40-V-1001 rồi vào riser.",
                "Trường hợp thiết kế: (1) khí lọt qua tháp 10-T-3002 – 349.674 kg/h, 75 °C (60 % H₂, 18 % CO₂); (2) đầu ra reforming bị chặn – 213.056 kg/h, 360 °C."],
         "src": [S_FDESC, PFD41_2, PID41_2]},
        {"h": "Mồi lửa, purge & bức xạ",
         "ul": ["Mỗi đầu đuốc có 3 đầu mồi (pilot) với bộ đánh lửa (FFG) và đầu dò lửa riêng. Tủ đánh lửa đặt ngoài vùng an toàn; báo động tổng về phòng điều khiển khi mất lửa mồi.",
                "Mạng đuốc luôn có dòng purge để giữ áp dương, chống không khí lọt vào. Từ 2014, purge được chuyển từ khí nhiên liệu sang N₂. "
                "Lưu lượng tối thiểu: đuốc tổng hợp 36 Nm³/h, đuốc NH3 74,5 Nm³/h. Dòng khí nhiên liệu hỗ trợ cháy cho đuốc NH3 tăng từ 20 lên 22 Nm³/h.",
                "Chiều cao đuốc 45 m, tính theo API 521 để bức xạ (kể cả bức xạ mặt trời) ≤ 3.000 Btu/h·ft² tại kết cấu và ≤ 1.450 Btu/h·ft² trong vùng cấm bán kính 60 m."],
         "src": [S_FDESC, S_FN2]},
    ],
    "src": [S_FDESC],
}

TAGS41 = {
    "40-PK-1001": ent("Đuốc NH3 40-PK-1001",
                      "Đuốc giằng cáp cao 45 m, công suất 298.190 kg/h. Riser 42\" cho khí xả NH3 của xưởng Amoniac và riser 6\" riêng cho khí bồn chứa 40-TK-5001; có header riêng từ tháp stripping 40-T2001. "
                      "Khí nhiên liệu bổ sung ở đỉnh (HV-41002) giúp NH3 cháy được. Có 3 đầu mồi, bộ đánh lửa FFG và đầu dò lửa. Purge mạng đuốc bằng N₂ từ 2014 (≥ 74,5 Nm³/h).",
                      src=[S_FDESC, S_FN2, S_FBD, PFD41_1, PID41_1]),
    "40-PK-1002": ent("Đuốc khí tổng hợp 40-PK-1002",
                      "Đuốc giằng cáp 42\" × 45 m, công suất 349.674 kg/h. Nhận khí xả phần đầu xưởng Amoniac (H₂, N₂, CO, CO₂, CH₄) qua KO drum 40-V-1001. "
                      "Có 3 đầu mồi và bộ đánh lửa; purge bằng N₂ (≥ 36 Nm³/h).", src=[S_FDESC, S_FN2, S_FBD, PFD41_2, PID41_2]),
    "40-V-1001": ent("Bình tách lỏng đuốc 40-V-1001",
                     "Bình nằm ngang Ø4.000 × 13.400 mm, thiết kế 3,5 barg / 360 °C, đặt trước đuốc khí tổng hợp để tách lỏng cuốn theo khí xả. "
                     "Nước ngưng tích tụ có thể nhiễm NH3; mức bình theo dõi qua LI-41011 và xử lý theo phương án riêng.",
                     src=[PFD41_2, S_KO, S_FDESC]),
}

UNITS = {"45": UNIT45, "41": UNIT41}
TAGS = {**TAGS45, **TAGS41}
